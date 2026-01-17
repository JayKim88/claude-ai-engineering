#!/bin/bash
# save-learning.sh
# Complete workflow for saving learning document with optional git commit
#
# Usage:
#   ./save-learning.sh <filename> <topic> [content_file]
#
# Example:
#   ./save-learning.sh \
#     2026-01-17-claude-code.md \
#     "Claude Code Marketplace" \
#     /tmp/content.md

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Arguments
FILENAME="$1"
TOPIC="$2"
CONTENT_FILE="$3"

# Validation
if [ -z "$FILENAME" ] || [ -z "$TOPIC" ]; then
  echo "Usage: $0 <filename> <topic> [content_file]" >&2
  echo "" >&2
  echo "Example:" >&2
  echo "  $0 2026-01-17-topic.md \"Topic Name\" /tmp/content.md" >&2
  exit 1
fi

# Parse configuration
source "$SCRIPT_DIR/parse-config.sh"

# Determine save location
if [ -z "$LEARNING_REPO" ]; then
  # No learning_repo configured, use current directory
  SAVE_DIR="./learnings"
  echo "Warning: learning_repo not configured. Saving to $SAVE_DIR" >&2
else
  SAVE_DIR="$LEARNING_REPO/$OUTPUT_DIR"
fi

# Ensure save directory exists
if [ ! -d "$SAVE_DIR" ]; then
  echo "Error: Directory does not exist: $SAVE_DIR" >&2
  echo "Create it with: mkdir -p $SAVE_DIR" >&2
  exit 1
fi

# Full file path
FULL_PATH="$SAVE_DIR/$FILENAME"

# Save content
if [ -n "$CONTENT_FILE" ]; then
  # Copy from content file
  if [ ! -f "$CONTENT_FILE" ]; then
    echo "Error: Content file not found: $CONTENT_FILE" >&2
    exit 1
  fi

  echo "Saving learning document..." >&2
  cp "$CONTENT_FILE" "$FULL_PATH"
  echo "✅ Saved to: $FULL_PATH" >&2
else
  echo "Error: Content file not provided" >&2
  echo "Claude should use Write tool directly instead of this script" >&2
  exit 1
fi

# Git operations (if auto_commit enabled)
if [ "$AUTO_COMMIT" = "true" ]; then
  echo "" >&2
  echo "Auto-commit is enabled. Committing to git..." >&2

  # Determine relative path from repo root
  if [ -n "$LEARNING_REPO" ]; then
    RELATIVE_PATH="$OUTPUT_DIR/$FILENAME"

    if "$SCRIPT_DIR/git-commit.sh" "$LEARNING_REPO" "$RELATIVE_PATH" "$TOPIC"; then
      echo "✅ Git commit successful" >&2

      # Auto-push (if enabled)
      if [ "$AUTO_PUSH" = "true" ]; then
        echo "" >&2
        echo "Auto-push is enabled. Pushing to remote..." >&2

        cd "$LEARNING_REPO"
        if git push; then
          echo "✅ Git push successful" >&2
        else
          echo "Warning: Git push failed. You may need to push manually." >&2
        fi
      fi
    else
      echo "Warning: Git commit failed. Document saved but not committed." >&2
    fi
  else
    echo "Warning: Cannot commit without learning_repo configured" >&2
  fi
else
  echo "" >&2
  echo "Auto-commit is disabled. To commit manually:" >&2
  echo "  cd $SAVE_DIR" >&2
  echo "  git add $FILENAME" >&2
  echo "  git commit -m \"Add learning: $TOPIC\"" >&2
fi

# Summary
echo "" >&2
echo "==================================" >&2
echo "Learning document saved!" >&2
echo "==================================" >&2
echo "Location: $FULL_PATH" >&2
echo "Topic: $TOPIC" >&2

if [ "$AUTO_COMMIT" = "true" ]; then
  echo "Git: Committed" >&2
  if [ "$AUTO_PUSH" = "true" ]; then
    echo "Push: Pushed to remote" >&2
  else
    echo "Push: Not pushed (auto_push disabled)" >&2
  fi
else
  echo "Git: Not committed (auto_commit disabled)" >&2
fi

exit 0
