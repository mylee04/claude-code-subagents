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

echo "🎯 Next steps:"
echo "   1. Create a claude.md file in your project"
echo "   2. Run: /agent-assembler"
echo "   3. Use your custom agents with slash commands!"
echo ""
echo "🚀 Happy coding with your AI development team!"