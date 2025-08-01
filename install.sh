#!/bin/bash

# Claude Code Subagents Installation Script
# This script installs all agents to your Claude Code configuration

set -e

echo "🤖 Claude Code Subagents Installer"
echo "=================================="
echo ""

# Check if we're in the right directory
if [ ! -d "agents" ]; then
    echo "❌ Error: 'agents' directory not found!"
    echo "   Please run this script from the claude-code-subagents repository root."
    exit 1
fi

# Create the Claude agents directory if it doesn't exist
CLAUDE_AGENTS_DIR="$HOME/.claude/agents"
echo "📁 Creating Claude agents directory: $CLAUDE_AGENTS_DIR"
mkdir -p "$CLAUDE_AGENTS_DIR"

# Count agents to install
AGENT_COUNT=$(find agents -name "*.md" -type f | wc -l)
echo "📦 Found $AGENT_COUNT agents to install"
echo ""

# Copy all agents
echo "📋 Installing agents..."
cp -r agents/* "$CLAUDE_AGENTS_DIR/"

# Verify installation
INSTALLED_COUNT=$(find "$CLAUDE_AGENTS_DIR" -name "*.md" -type f | wc -l)
echo ""
echo "✅ Successfully installed $INSTALLED_COUNT agents!"
echo ""

# List installed agents by category
echo "📚 Installed agents by category:"
echo ""

for category_dir in "$CLAUDE_AGENTS_DIR"/*; do
    if [ -d "$category_dir" ]; then
        category=$(basename "$category_dir")
        echo "🏷️  $category:"
        for agent_file in "$category_dir"/*.md; do
            if [ -f "$agent_file" ]; then
                agent_name=$(basename "$agent_file" .md)
                echo "   • $agent_name"
            fi
        done
        echo ""
    fi
done

# Install gamification system
echo "🎮 Installing SubAgents Gamification System..."
if [ -d "gamification" ]; then
    # Make scripts executable
    chmod +x gamification/scripts/*.sh
    chmod +x gamification/core/*.py
    chmod +x agents-cli
    echo "✅ Gamification system ready!"
    echo ""
fi

echo "🎯 Next steps:"
echo "   1. Try the demo: python3 gamification/scripts/agents-demo.py"
echo "   2. Check agent levels: ./agents-cli"
echo "   3. Create a claude.md file and run: /agent-generator"
echo "   4. Use agents and track XP: ./agents-cli log [agent] [task]"
echo ""
echo "💡 Pro tip: Add this alias to your shell:"
echo "   alias agents='$(pwd)/agents-cli'"
echo ""
echo "🚀 Happy coding with your Elite AI Development Squad!"