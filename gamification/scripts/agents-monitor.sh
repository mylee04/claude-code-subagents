#!/bin/bash

# Elite Squad Monitor
# Watches Claude Code usage and automatically tracks agent XP

SQUAD_DIR="$(dirname "$0")"
CORE_DIR="$(dirname "$SQUAD_DIR")/core"
LOG_FILE="$HOME/.claude/squad-activity.log"
TRACKER="$CORE_DIR/squad_tracker.py"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${RED}    ELITE SQUAD MONITORING SYSTEM ACTIVATED          ${NC}"
echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Function to parse Claude Code output and track agent usage
track_agent_usage() {
    local line="$1"
    local timestamp=$(date +%s)
    
    # Detect agent calls (common patterns)
    # Pattern 1: /agent-name command
    if [[ "$line" =~ ^/([a-z-]+) ]]; then
        agent="${BASH_REMATCH[1]}"
        echo -e "${GREEN}✓ Agent deployed:${NC} $agent"
        
        # Log to tracker (simplified - in real implementation would track success/fail)
        python3 "$TRACKER" log "$agent" "Command execution" success
        
    # Pattern 2: "Use agent-name to..."
    elif [[ "$line" =~ [Uu]se[[:space:]]+([a-z-]+)[[:space:]]+(to|for) ]]; then
        agent="${BASH_REMATCH[1]}"
        echo -e "${GREEN}✓ Agent requested:${NC} $agent"
        python3 "$TRACKER" log "$agent" "Natural language task" success
        
    # Pattern 3: Task tool usage
    elif [[ "$line" =~ "Task tool".*"([a-z-]+)" ]]; then
        agent="${BASH_REMATCH[1]}"
        echo -e "${GREEN}✓ Task tool agent:${NC} $agent"
        python3 "$TRACKER" log "$agent" "Task tool deployment" success
    fi
    
    # Detect errors and resolutions
    if [[ "$line" =~ [Ee]rror|[Ff]ailed ]]; then
        echo -e "${RED}⚠ Error detected${NC}"
        # Would need more context to attribute to specific agent
    fi
}

# Show current stats
echo -e "${BLUE}📊 Current Squad Status:${NC}"
python3 "$TRACKER" leaderboard
echo ""

echo -e "${YELLOW}🎯 Monitoring Claude Code activity...${NC}"
echo -e "${YELLOW}   (Run Claude Code commands to track agent XP)${NC}"
echo ""

# Option 1: Monitor a log file if Claude Code outputs to one
if [ -f "$LOG_FILE" ]; then
    tail -f "$LOG_FILE" | while read line; do
        track_agent_usage "$line"
    done
else
    echo -e "${YELLOW}ℹ To enable automatic tracking:${NC}"
    echo "  1. Pipe Claude Code output through this monitor:"
    echo "     claude code 2>&1 | $0"
    echo ""
    echo "  2. Or manually log agent usage:"
    echo "     $TRACKER log python-elite \"Optimized algorithm\" success"
    echo ""
    echo "  3. View reports:"
    echo "     $TRACKER leaderboard"
    echo "     $TRACKER card python-elite"
    echo "     $TRACKER report"
fi

# If no log file, read from stdin
if [ ! -f "$LOG_FILE" ]; then
    while IFS= read -r line; do
        echo "$line"  # Pass through the output
        track_agent_usage "$line"
    done
fi