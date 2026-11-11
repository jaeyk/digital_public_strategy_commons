#!/usr/bin/env bash
# Preview the website locally (stop with Ctrl+C).
#
#   ./preview_website.sh                 serve docs/ at http://localhost:8000
#   ./preview_website.sh 9000            use port 9000 (also: --port 9000, or PORT=9000 ./preview_website.sh)
#   ./preview_website.sh --rebuild       first re-export model data from the Python models and check the
#                                        JavaScript engine still matches them (needs the .venv and Node.js)
#   ./preview_website.sh --force         take over the port without asking, whatever is using it
#
# If the port is already in use, the script takes it over: an earlier preview server (python http.server)
# is stopped automatically; any other program is stopped only after you confirm (or with --force).
set -euo pipefail
cd "$(dirname "$0")"

PORT="${PORT:-8000}"
REBUILD=false
FORCE=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    --rebuild) REBUILD=true ;;
    --force) FORCE=true ;;
    -p|--port) PORT="${2:?--port needs a number}"; shift ;;
    --port=*) PORT="${1#*=}" ;;
    -h|--help) sed -n '2,12p' "$0"; exit 0 ;;
    *[!0-9]*|"") echo "Unknown option: $1 (see --help)" >&2; exit 1 ;;
    *) PORT="$1" ;;
  esac
  shift
done
if [[ ! "$PORT" =~ ^[0-9]+$ ]] || (( PORT < 1 || PORT > 65535 )); then
  echo "Invalid port: $PORT" >&2
  exit 1
fi

if $REBUILD; then
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
  echo "docs/data/model.json is missing. Run: ./preview_website.sh --rebuild" >&2
  exit 1
fi

# Take over the port if something is already listening on it.
if command -v lsof >/dev/null 2>&1; then
  PIDS="$(lsof -nP -t -iTCP:"$PORT" -sTCP:LISTEN 2>/dev/null | sort -u || true)"
  if [[ -n "$PIDS" ]]; then
    others=""
    for pid in $PIDS; do
      cmd="$(ps -p "$pid" -o command= 2>/dev/null || true)"
      [[ "$cmd" == *http.server* ]] || others+="  $pid  $cmd"$'\n'
    done
    if [[ -n "$others" ]] && ! $FORCE; then
      echo "Port $PORT is in use by:"
      printf '%s' "$others"
      read -r -p "Stop it and use port $PORT? [y/N] " answer
      if [[ ! "$answer" =~ ^[Yy]$ ]]; then
        echo "Not stopped. Choose another port, for example: ./preview_website.sh $((PORT + 1))"
        exit 1
      fi
    fi
    echo "Stopping what is using port $PORT (PID $(echo $PIDS | tr '\n' ' '))..."
    kill $PIDS 2>/dev/null || true
    for _ in 1 2 3 4 5 6 7 8 9 10; do
      lsof -nP -t -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1 || break
      sleep 0.3
    done
    if lsof -nP -t -iTCP:"$PORT" -sTCP:LISTEN >/dev/null 2>&1; then
      kill -9 $PIDS 2>/dev/null || true
      sleep 0.5
    fi
  fi
fi

URL="http://localhost:${PORT}/"
echo "Serving docs/ at ${URL}"
if command -v open >/dev/null 2>&1; then (sleep 1 && open "$URL") >/dev/null 2>&1 &
elif command -v xdg-open >/dev/null 2>&1; then (sleep 1 && xdg-open "$URL") >/dev/null 2>&1 &
fi
exec python3 -m http.server "$PORT" --directory docs
