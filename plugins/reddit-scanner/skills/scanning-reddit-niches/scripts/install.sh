#!/bin/bash
# Install reddit-scanner CLI
set -e

if command -v reddit-scanner &>/dev/null; then
  echo "✅ reddit-scanner already installed: $(which reddit-scanner)"
  exit 0
fi

if command -v go &>/dev/null; then
  echo "📦 Installing via go install..."
  go install github.com/allen-hsu/reddit-scanner@latest
  echo "✅ Installed: $(which reddit-scanner)"
else
  echo "⚠️  Go not found. Installing from source..."
  TMPDIR=$(mktemp -d)
  git clone --depth 1 https://github.com/allen-hsu/reddit-scanner.git "$TMPDIR/reddit-scanner"
  cd "$TMPDIR/reddit-scanner"
  go build -o /usr/local/bin/reddit-scanner .
  rm -rf "$TMPDIR"
  echo "✅ Installed to /usr/local/bin/reddit-scanner"
fi
