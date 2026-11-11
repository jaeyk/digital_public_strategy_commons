#!/usr/bin/env bash
# Update the live website (GitHub Pages serves the docs/ folder on the main branch).
#
#   ./update_website.sh                  refresh, test, then ask before committing and pushing
#   ./update_website.sh "Message"        same, with your own commit message
#
# Steps:
#   1. Re-export the website's model data from the Python models (docs/data/).
#   2. Run the Python tests and check that the website's JavaScript engine still matches Python.
#   3. Show what changed, ask for confirmation, then commit and push to main.
# The site is live at https://jaeyk.github.io/digital_public_strategy_commons/ a minute or two later.
set -euo pipefail
cd "$(dirname "$0")"

PYTHON=".venv/bin/python"
[[ -x "$PYTHON" ]] || PYTHON="python3"
MESSAGE="${1:-Update website}"

echo "1/3 Exporting model data for the website..."
"$PYTHON" -m models.export_site_data

echo "2/3 Running checks..."
"$PYTHON" -m unittest discover tests
if command -v node >/dev/null 2>&1; then
  node tests/site_engine.test.mjs
else
  echo "Node.js not found; skipping the JavaScript engine check (CI will run it)."
fi

echo "3/3 Changes to publish:"
if [[ -z "$(git status --porcelain)" ]]; then
  echo "Nothing has changed. The website is already up to date."
  exit 0
fi
git status --short

branch="$(git rev-parse --abbrev-ref HEAD)"
if [[ "$branch" != "main" ]]; then
  echo "You are on branch '$branch'. The website publishes from 'main'; switch to main first." >&2
  exit 1
fi

read -r -p "Commit all of these changes and push to main? [y/N] " answer
if [[ ! "$answer" =~ ^[Yy]$ ]]; then
  echo "Stopped. Nothing was committed."
  exit 0
fi

git add -A
git commit -m "$MESSAGE"
git push origin main
echo "Pushed. The website updates in a minute or two: https://jaeyk.github.io/digital_public_strategy_commons/"
