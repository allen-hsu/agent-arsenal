#!/bin/bash
# Install reddit-scanner CLI
set -e

REPO="allen-hsu/reddit-scanner"

if command -v reddit-scanner &>/dev/null; then
  echo "✅ reddit-scanner already installed: $(which reddit-scanner)"
  exit 0
fi

# Detect OS and arch
OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)
case "$ARCH" in
  x86_64) ARCH="amd64" ;;
  aarch64|arm64) ARCH="arm64" ;;
esac

# Try downloading pre-built binary from GitHub Releases
LATEST=$(curl -sL "https://api.github.com/repos/$REPO/releases/latest" | grep '"tag_name"' | cut -d'"' -f4)

if [ -n "$LATEST" ]; then
  URL="https://github.com/$REPO/releases/download/${LATEST}/reddit-scanner_${OS}_${ARCH}.tar.gz"
  echo "📦 Downloading $LATEST for ${OS}/${ARCH}..."
  TMPDIR=$(mktemp -d)
  if curl -sL "$URL" | tar xz -C "$TMPDIR" 2>/dev/null; then
    sudo mv "$TMPDIR/reddit-scanner" /usr/local/bin/ 2>/dev/null || mv "$TMPDIR/reddit-scanner" "$HOME/.local/bin/"
    rm -rf "$TMPDIR"
    echo "✅ Installed reddit-scanner $LATEST"
    exit 0
  fi
  rm -rf "$TMPDIR"
  echo "⚠️  Binary download failed, falling back to source build..."
fi

# Fallback: build from source
if command -v go &>/dev/null; then
  echo "📦 Building from source..."
  go install "github.com/$REPO@latest"
  echo "✅ Installed via go install"
else
  echo "❌ Need either a GitHub release or Go installed. Install Go: https://go.dev/dl/"
  exit 1
fi
