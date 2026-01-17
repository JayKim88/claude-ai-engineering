#!/bin/bash
# git-commit.sh
# Auto-commit learning document to git repository
#
# Usage:
#   ./git-commit.sh <repo_path> <file_path> <topic>
#
# Example:
#   ./git-commit.sh \
#     /Users/jaykim/Documents/Projects/ai-learning \
#     learnings/2026-01-17-topic.md \
#     "Claude Code Marketplace"

set -e

# Arguments
REPO_PATH="$1"
FILE_PATH="$2"
TOPIC="$3"

# Validation
if [ -z "$REPO_PATH" ] || [ -z "$FILE_PATH" ] || [ -z "$TOPIC" ]; then
  echo "Usage: $0 <repo_path> <file_path> <topic>" >&2
  echo "" >&2
  echo "Example:" >&2
  echo "  $0 /path/to/repo learnings/file.md \"Topic Name\"" >&2
  exit 1
fi

if [ ! -d "$REPO_PATH" ]; then
  echo "Error: Repository path does not exist: $REPO_PATH" >&2
  exit 1
fi

if [ ! -f "$REPO_PATH/$FILE_PATH" ]; then
  echo "Error: File does not exist: $REPO_PATH/$FILE_PATH" >&2
  exit 1
fi

# Check if git is installed
if ! command -v git &> /dev/null; then
  echo "Error: git is not installed" >&2
  echo "Install git: brew install git (macOS) or apt-get install git (Linux)" >&2
  exit 1
fi

# Change to repo directory
cd "$REPO_PATH"

# Check if it's a git repository
if [ ! -d ".git" ]; then
  echo "Error: Not a git repository: $REPO_PATH" >&2
  echo "Initialize with: cd $REPO_PATH && git init" >&2
  exit 1
fi

# Check if file has changes
if git diff --quiet "$FILE_PATH" && git diff --cached --quiet "$FILE_PATH"; then
  echo "Warning: No changes to commit for $FILE_PATH" >&2
  exit 0
fi

# Add file
echo "Adding $FILE_PATH to git..." >&2
git add "$FILE_PATH"

# Create commit message
COMMIT_MSG="Add learning: $TOPIC

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# Commit
echo "Creating commit..." >&2
if git commit -m "$COMMIT_MSG"; then
  echo "✅ Successfully committed: $FILE_PATH" >&2

  # Show commit hash
  COMMIT_HASH=$(git rev-parse --short HEAD)
  echo "   Commit: $COMMIT_HASH" >&2
else
  echo "Error: Git commit failed" >&2
  exit 1
fi

exit 0
