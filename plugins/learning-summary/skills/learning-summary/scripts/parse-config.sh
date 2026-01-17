#!/bin/bash
# parse-config.sh
# Parse learning-summary config.yaml and extract settings
#
# Usage:
#   source ./parse-config.sh
#   echo "$LEARNING_REPO"
#   echo "$OUTPUT_DIR"
#   echo "$AUTO_COMMIT"
#   echo "$AUTO_PUSH"

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/../config.yaml"

# Default values
LEARNING_REPO=""
OUTPUT_DIR="learnings"
AUTO_COMMIT="false"
AUTO_PUSH="false"
LANGUAGE="auto"

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
  echo "Warning: Config file not found at $CONFIG_FILE" >&2
  echo "Using defaults: output_dir=$OUTPUT_DIR, auto_commit=$AUTO_COMMIT" >&2
  return 0 2>/dev/null || exit 0
fi

# Parse YAML (simple approach, no dependencies)
# Note: This is a simplified parser. For complex YAML, use yq or python.

while IFS=': ' read -r key value; do
  # Skip comments and empty lines
  [[ "$key" =~ ^#.*$ ]] && continue
  [[ -z "$key" ]] && continue

  # Remove leading/trailing whitespace
  key=$(echo "$key" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
  value=$(echo "$value" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')

  # Remove quotes from value
  value=$(echo "$value" | sed 's/^["'\''"]//;s/["'\''"]$//')

  case "$key" in
    learning_repo)
      LEARNING_REPO="$value"
      ;;
    output_dir)
      OUTPUT_DIR="$value"
      ;;
    auto_commit)
      AUTO_COMMIT="$value"
      ;;
    auto_push)
      AUTO_PUSH="$value"
      ;;
    language)
      LANGUAGE="$value"
      ;;
  esac
done < "$CONFIG_FILE"

# Expand tilde in learning_repo
if [[ "$LEARNING_REPO" =~ ^~.*$ ]]; then
  LEARNING_REPO="${LEARNING_REPO/#\~/$HOME}"
fi

# Export variables
export LEARNING_REPO
export OUTPUT_DIR
export AUTO_COMMIT
export AUTO_PUSH
export LANGUAGE

# Debug output (comment out in production)
# echo "DEBUG: LEARNING_REPO=$LEARNING_REPO" >&2
# echo "DEBUG: OUTPUT_DIR=$OUTPUT_DIR" >&2
# echo "DEBUG: AUTO_COMMIT=$AUTO_COMMIT" >&2
# echo "DEBUG: AUTO_PUSH=$AUTO_PUSH" >&2
