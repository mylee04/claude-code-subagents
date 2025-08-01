# 📁 Project Structure

```
claude-code-subagents/
│
├── README.md                    # Main documentation with gamification info
├── LICENSE                      # MIT License
├── _config.yml                  # GitHub Pages config
├── squad                        # Main entry point for gamification system
│
├── agents/                      # All agent definitions
│   ├── business/               # Business & marketing agents
│   ├── conductor/              # Orchestration agents (agent-assembler, etc.)
│   ├── data/                   # Data & AI/ML agents
│   ├── development/            # Programming language specialists
│   ├── infrastructure/         # DevOps & cloud agents
│   ├── product/                # Product & UX agents
│   ├── quality/                # Testing & code review agents
│   └── security/               # Security audit agents
│
├── gamification/               # Gamification system
│   ├── core/                   # Core Python modules
│   │   ├── squad_tracker.py    # XP and achievement tracking
│   │   └── squad-levels.py     # Level display system
│   │
│   ├── scripts/                # Executable scripts
│   │   ├── squad-demo.py       # Interactive demo
│   │   ├── squad-monitor.sh    # Real-time usage monitor
│   │   └── squad-query.sh      # Quick level queries
│   │
│   └── docs/                   # Gamification documentation
│       ├── README.md           # How gamification works
│       └── INTEGRATION.md      # Integration guide
│
└── .claude/                    # Runtime data (git-ignored)
    └── squad-tracker.json      # Persistent XP/level data
```

## 🚀 Quick Start

1. **Install agents**:
   ```bash
   cd ~/.claude && git clone https://github.com/mylee04/claude-code-subagents.git agents
   ```

2. **Use the gamification system**:
   ```bash
   ./squad                      # Check all agent levels
   ./squad python-elite         # Check specific agent
   ./squad log backend-architect "Built API"  # Log usage
   ```

3. **Run the demo**:
   ```bash
   python3 gamification/scripts/squad-demo.py
   ```

## 📦 Main Components

### Agents (`/agents`)
- 31 specialized AI agents organized by category
- Each with YAML frontmatter for Claude Code compatibility
- Ready to use with `/agent-name` commands

### Gamification System (`/gamification`)
- **Core**: Python modules for tracking XP, levels, achievements
- **Scripts**: Shell and Python scripts for interaction
- **Docs**: Detailed documentation for the gamification features

### Entry Points
- `squad`: Main command for checking levels and logging usage
- Individual scripts in `gamification/scripts/` for specific functions

## 🔧 Development

To add new features:
1. Core logic goes in `gamification/core/`
2. User-facing scripts go in `gamification/scripts/`
3. Documentation goes in `gamification/docs/`
4. Keep agents organized in their category folders