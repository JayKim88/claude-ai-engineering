#!/bin/bash
# link-local.sh
# Link all skills and agents to Claude Code for local development
#
# Usage:
#   ./scripts/link-local.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "🔗 Linking skills and agents to Claude Code..."
echo ""

# Ensure Claude directories exist
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/agents"

# Link skills
if [ -d "$REPO_ROOT/skills" ]; then
  for skill in "$REPO_ROOT/skills"/*; do
    if [ -d "$skill" ]; then
      skill_name=$(basename "$skill")
      target="$CLAUDE_DIR/skills/$skill_name"

      # Remove existing link/directory
      if [ -L "$target" ] || [ -d "$target" ]; then
        rm -rf "$target"
      fi

      # Create symlink
      ln -s "$skill" "$target"
      echo "✓ Linked skill: $skill_name"
    fi
  done
fi

# Link agents
if [ -d "$REPO_ROOT/agents" ]; then
  for agent in "$REPO_ROOT/agents"/*; do
    if [ -d "$agent" ]; then
      agent_name=$(basename "$agent")
      target="$CLAUDE_DIR/agents/$agent_name"

      # Remove existing link/directory
      if [ -L "$target" ] || [ -d "$target" ]; then
        rm -rf "$target"
      fi

      # Create symlink
      ln -s "$agent" "$target"
      echo "✓ Linked agent: $agent_name"
    fi
  done
fi

echo ""
echo "✅ All skills and agents linked successfully!"
echo ""
echo "📝 Linked locations:"
echo "   Skills: $CLAUDE_DIR/skills/"
echo "   Agents: $CLAUDE_DIR/agents/"
echo ""
echo "💡 Now you can:"
echo "   - Edit files in: $REPO_ROOT"
echo "   - Test immediately in Claude Code"
echo "   - Commit changes to git"
