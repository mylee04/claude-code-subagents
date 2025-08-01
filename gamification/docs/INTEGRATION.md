# 🎮 Level System Integration Guide

## Quick Setup

1. **Add the squad alias to your shell** (~/.bashrc or ~/.zshrc):
```bash
alias squad='~/.claude/agents/squad-query.sh'
```

2. **Check your agents' levels anytime**:
```bash
# See all agents with levels
squad

# Check specific agent
squad backend-architect

# Show level badge
squad badge python-elite
```

## How to Use with Claude Code

### Workflow Example:

1. **Use Claude Code normally**:
```bash
/data-engineer build ETL pipeline
```

2. **After completing tasks, log the activity**:
```bash
squad log data-engineer "Built ETL pipeline"
```

3. **Check your agent's progress**:
```bash
squad data-engineer
# Output: data-engineer: Lv.1 Recruit ★☆☆☆☆ (65 XP)
```

## Visual Level Display

When you run `squad`, you'll see:

```
╔═══════════════════════════════════════════════════════════════╗
║                    ELITE SQUAD AGENT LEVELS                    ║
╠═══════════════════════════════════════════════════════════════╣
║ Total Agents: 30                                              ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║ 📁 Personal agents (~/.claude/agents)                         ║
║ ─────────────────────────────────────────────────────────── ║
║ data-engineer             Lv.2 Specialist ★★☆☆☆ │             ║
║ backend-architect         Lv.3 Expert     ★★★☆☆ │             ║
║ python-elite              Lv.4 Master     ★★★★☆ │             ║
```

## Automatic Tracking (Optional)

For automatic tracking, pipe Claude Code through the monitor:
```bash
# Add to your shell alias
alias cc='claude code 2>&1 | ~/.claude/agents/squad-monitor.sh'
```

## Level Progression

- **Lv.1 Recruit** (0-100 XP): ★☆☆☆☆
- **Lv.2 Specialist** (100-300 XP): ★★☆☆☆  
- **Lv.3 Expert** (300-600 XP): ★★★☆☆
- **Lv.4 Master** (600-1000 XP): ★★★★☆
- **Lv.5 Elite** (1000+ XP): ★★★★★

## Tips

- Log complex tasks for bonus XP
- Track error resolutions for +20 XP
- Check leaderboards with `./squad_tracker.py leaderboard`
- View full reports with `./squad_tracker.py report`

This integrates seamlessly with YOUR actual agents!