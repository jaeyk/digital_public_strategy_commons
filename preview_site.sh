#!/usr/bin/env bash
# Preview the website locally at http://localhost:8000 (stop with Ctrl+C).
#
#   ./preview_site.sh            serve the site as it is
#   ./preview_site.sh --rebuild  first re-export model data from the Python models and check the
#                                JavaScript engine still matches them (needs the .venv and Node.js)
#   PORT=9000 ./preview_site.sh  use a different port
set -euo pipefail
cd "$(dirname "$0")"
PORT="${PORT:-8000}"

if [[ "${1:-}" == "--rebuild" ]]; then
  PYTHON=".venv/bin/python"
  [[ -x "$PYTHON" ]] || PYTHON="python3"
  echo "Exporting model data for the site..."
  "$PYTHON" -m models.export_site_data
  if command -v node >/dev/null 2>&1; then
    node tests/site_engine.test.mjs
  else
    echo "Node.js not found; skipping the JavaScript engine check."
  fi
fi

if [[ ! -f docs/data/model.json ]]; then
  echo "docs/data/model.json is missing. Run: ./preview_site.sh --rebuild" >&2
  exit 1
fi

URL="http://localhost:${PORT}/"
echo "Serving docs/ at ${URL}"
if command -v open >/dev/null 2>&1; then (sleep 1 && open "$URL") >/dev/null 2>&1 &
elif command -v xdg-open >/dev/null 2>&1; then (sleep 1 && xdg-open "$URL") >/dev/null 2>&1 &
fi
exec python3 -m http.server "$PORT" --directory docs
