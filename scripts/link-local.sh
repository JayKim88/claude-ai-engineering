#!/bin/bash
# link-local.sh
# Link all skills, agents, and commands to Claude Code for local development
#
# Usage:
#   ./scripts/link-local.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$HOME/.claude"

echo "🔗 Linking plugins to Claude Code..."
echo ""

# Ensure Claude directories exist
mkdir -p "$CLAUDE_DIR/skills"
mkdir -p "$CLAUDE_DIR/agents"
mkdir -p "$CLAUDE_DIR/commands"

# Counter for reporting
skills_count=0
agents_count=0
commands_count=0

# Link all plugins
if [ -d "$REPO_ROOT/plugins" ]; then
  for plugin in "$REPO_ROOT/plugins"/*; do
    if [ -d "$plugin" ]; then
      plugin_name=$(basename "$plugin")
      echo "📦 Plugin: $plugin_name"

      # Link skills from this plugin
      if [ -d "$plugin/skills" ]; then
        for skill in "$plugin/skills"/*; do
          if [ -d "$skill" ]; then
            skill_name=$(basename "$skill")
            target="$CLAUDE_DIR/skills/$skill_name"

            # Remove existing link/directory
            if [ -L "$target" ] || [ -d "$target" ]; then
              rm -rf "$target"
            fi

            # Create symlink
            ln -s "$skill" "$target"
            echo "  ✓ Linked skill: $skill_name"
            ((skills_count++))
          fi
        done
      fi

      # Link agents from this plugin (individual .md files)
      if [ -d "$plugin/agents" ]; then
        for agent in "$plugin/agents"/*.md; do
          if [ -f "$agent" ]; then
            agent_name=$(basename "$agent")
            target="$CLAUDE_DIR/agents/$agent_name"

            # Remove existing link/file
            if [ -L "$target" ] || [ -f "$target" ]; then
              rm -f "$target"
            fi

            # Create symlink
            ln -s "$agent" "$target"
            echo "  ✓ Linked agent: $agent_name"
            ((agents_count++))
          fi
        done
      fi

      # Link commands from this plugin (directory structure)
      if [ -d "$plugin/commands" ]; then
        for command in "$plugin/commands"/*; do
          if [ -d "$command" ]; then
            command_name=$(basename "$command")
            target="$CLAUDE_DIR/commands/$command_name"

            # Remove existing link/directory
            if [ -L "$target" ] || [ -d "$target" ]; then
              rm -rf "$target"
            fi

            # Create symlink
            ln -s "$command" "$target"
            echo "  ✓ Linked command: $command_name"
            ((commands_count++))
          fi
        done
      fi

      echo ""
    fi
  done
fi

echo "✅ All plugins linked successfully!"
echo ""
echo "📊 Summary:"
echo "   Skills:   $skills_count"
echo "   Agents:   $agents_count"
echo "   Commands: $commands_count"
echo ""
echo "📝 Linked locations:"
echo "   Skills:   $CLAUDE_DIR/skills/"
echo "   Agents:   $CLAUDE_DIR/agents/"
echo "   Commands: $CLAUDE_DIR/commands/"
echo ""
echo "💡 Now you can:"
echo "   - Edit files in: $REPO_ROOT/plugins/"
echo "   - Test immediately in Claude Code"
echo "   - Commit changes to git"
