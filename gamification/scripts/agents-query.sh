#!/bin/bash

# Agents Query - Quick level checks for agents
# Use this alongside Claude Code to see agent levels

AGENTS_DIR="$(dirname "$0")"
CORE_DIR="$(dirname "$AGENTS_DIR")/core"
PYTHON="python3"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Function to show help
show_help() {
    echo -e "${BLUE}🎮 Agents Analytics - Agent Usage & Gamification${NC}"
    echo ""
    echo "Usage:"
    echo "  agents                    - Show all agents with levels"
    echo "  agents [agent-name]       - Check specific agent level"
    echo "  agents badge [agent]      - Show agent's level badge"
    echo "  agents log [agent] [task] - Log agent usage"
    echo ""
    echo "Analytics Commands:"
    echo "  agents stats              - Show comprehensive usage analytics"
    echo "  agents leaderboard        - Show XP-based agent leaderboard"
    echo "  agents analyze            - Run full agent log analysis"
    echo "  agents teams              - Show team formations"
    echo "  agents insights           - Get usage insights & tips"
    echo ""
    echo "Examples:"
    echo "  agents                    # See all your agents"
    echo "  agents python-elite       # Check python-elite's level"
    echo "  agents stats              # View comprehensive analytics"
    echo "  agents leaderboard        # See XP rankings"
    echo "  agents log data-engineer \"Built ETL pipeline\""
}

# Get the root directory for analytics script
ROOT_DIR="$(dirname "$AGENTS_DIR")/.."
ANALYTICS_SCRIPT="$ROOT_DIR/analyze_agent_usage.py"

# Main logic
if [ $# -eq 0 ]; then
    # Show all agents with levels
    $PYTHON "$CORE_DIR/agents-levels.py"
    
elif [ "$1" == "help" ] || [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    show_help
    
elif [ "$1" == "stats" ]; then
    # Show comprehensive analytics
    echo -e "${BLUE}📊 Running comprehensive agent analytics...${NC}"
    $PYTHON "$ANALYTICS_SCRIPT"
    
elif [ "$1" == "leaderboard" ]; then
    # Show XP-based leaderboard
    echo -e "${BLUE}🏆 Agent XP Leaderboard${NC}"
    $PYTHON "$ANALYTICS_SCRIPT" --xp-leaderboard
    
elif [ "$1" == "analyze" ]; then
    # Run full agent log analysis
    echo -e "${BLUE}🔍 Analyzing agent logs...${NC}"
    $PYTHON "$CORE_DIR/agent_logs_analyzer.py" analyze
    
elif [ "$1" == "teams" ]; then
    # Show team formations
    echo -e "${BLUE}🤝 Team Formations Analysis${NC}"
    $PYTHON "$ANALYTICS_SCRIPT" --squads
    
elif [ "$1" == "insights" ]; then
    # Show usage insights
    echo -e "${BLUE}💡 Usage Insights & Recommendations${NC}"
    $PYTHON "$ANALYTICS_SCRIPT" --insights
    
elif [ "$1" == "badge" ] && [ $# -ge 2 ]; then
    # Show badge for specific agent
    $PYTHON "$CORE_DIR/agents-levels.py" badge "$2"
    
elif [ "$1" == "log" ] && [ $# -ge 3 ]; then
    # Log agent usage
    agent="$2"
    task="$3"
    $PYTHON "$CORE_DIR/agents_tracker.py" log "$agent" "$task" success
    echo -e "${GREEN}✓ Logged activity for $agent${NC}"
    $PYTHON "$CORE_DIR/agents-levels.py" check "$agent"
    
elif [ $# -eq 1 ]; then
    # Quick check for specific agent or show help for unknown commands
    if [ -f "$ANALYTICS_SCRIPT" ] && $PYTHON "$CORE_DIR/agents-levels.py" check "$1" 2>/dev/null; then
        # Valid agent name
        $PYTHON "$CORE_DIR/agents-levels.py" check "$1"
    else
        echo -e "${RED}Unknown command or agent: $1${NC}"
        echo ""
        show_help
    fi
    
else
    show_help
fi

# Add alias suggestion
if ! alias agents &>/dev/null; then
    echo ""
    echo -e "${YELLOW}💡 Tip: Add this alias to your shell:${NC}"
    echo -e "   alias agents='$(cd "$AGENTS_DIR/../.." && pwd)/agents-cli'"
    echo -e "   Then just type: agents"
fi