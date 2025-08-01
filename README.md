# Claude Code SubAgents

> **"Pokemon for Developers"** - Your AI agents level up, form teams, and tackle any coding challenge

**Quick Start**: `cd ~/.claude && git clone https://github.com/mylee04/claude-code-subagents.git agents` (10 seconds)

[![Claude Code](https://img.shields.io/badge/Claude%20Code-SubAgents-red)](https://github.com/anthropics/claude-code)
[![Agents](https://img.shields.io/badge/agents-31-orange)](agents/)
[![XP System](https://img.shields.io/badge/XP%20System-Active-green)](GAMIFICATION-DESIGN.md)

## What Is This?

A **gamified collection of 31 specialized AI agents** that work together like a development team. Each agent levels up as you use them, unlocks achievements, and forms powerful combinations for complex tasks.

**Core Value**: Instead of one generic AI assistant, you get a specialized team where each agent is an expert in their domain (Python, DevOps, Security, etc.).

## Key Features

- **31 Specialist Agents** - From Python experts to security auditors
- **Gamification System** - Agents gain XP, level up (Novice → Legend), earn achievements
- **Smart Agent Registry** - Automatically discovers and coordinates all available agents
- **Team Formations** - Agents work together with synergy bonuses
- **Real Progress Tracking** - Watch your AI team collaborate in real-time

## Interactive Demo

Try it now - see the XP system, achievements, and agent collaboration in action:

```bash
cd ~/.claude/agents && python3 gamification/scripts/agents-demo.py
```

Watch agents level up, earn achievements like "Speed Demon" and "Bug Hunter", and see real-time mission progress.

## Basic Usage

```bash
# Use specific agents
/python-pro optimize this function
/devops-troubleshooter analyze these logs
/security-auditor review authentication flow

# Complex multi-agent tasks
# Use Claude Code's built-in orchestration for complex workflows
```

## 🔍 Agent Discovery & Coordination System

The SubAgents system now features an advanced **AgentRegistry** that automatically discovers and coordinates agents from multiple locations:

### Live Demo - See It In Action!

```ansi
🔍 AGENT DISCOVERY
─────────────────
✓ Successfully discovered 34 agents

  ▸ Discovery Statistics
  Total Agents Found....... 34
  Categories Discovered.... 8
  Tech Stacks Available.... 11

📊 CATEGORY BREAKDOWN
───────────────────────

  Development         │████████████████████│ 10 agents
  Infrastructure      │████████████        │  6 agents
  Data & AI           │████████            │  4 agents
  Quality Assurance   │████████            │  4 agents
  Product             │████████            │  4 agents
  Coordination        │██████              │  3 agents
  Business            │████                │  2 agents
  Security            │██                  │  1 agents

🎯 FEATURE PLANNING & TEAM RECOMMENDATION
────────────────────────────────────────

  ▸ Building E-Commerce Web Application
  📝 Tech Stack: ["react", "typescript", "python", "postgresql"]
  
  ✓ Recommended Team (6 agents):
  • full-stack-architect - Complete system architecture design
  • python-elite - Python/Django/FastAPI development
  • frontend-developer - Modern UI components and frameworks
  • database-optimizer - Database performance specialist
  • devops-engineer - Full-stack DevOps specialist
  • security-auditor - Security vulnerability scanner
```

### Run the Demo Yourself

```bash
# Run the colorful interactive demo
python3 demo_agent_registry.py

# Or try the simple test
python3 test_agent_registry.py
```

### Key Features

- **Unified Discovery**: Finds agents from `/agents/`, `~/.claude/agents/`, and `.claude/agents/`
- **Built-in Orchestration**: Claude Code handles agent coordination automatically
- **Team Formation**: Intelligently recommends 3-6 agents based on your project needs
- **No External Dependencies**: Works with built-in Python libraries only

<details>
<summary><strong>📋 All 31 Agents (Click to expand)</strong></summary>

### Command & Planning
- Use Claude Code's built-in orchestration capabilities for multi-agent workflows

### Development
- **python-pro** - Python/Django/FastAPI expert
- **javascript-pro** - JavaScript/TypeScript/React specialist
- **golang-pro** - Go language expert
- **rust-pro** - Rust programming specialist
- **sql-pro** - Database query optimization
- **backend-architect** - API design and microservices
- **frontend-developer** - Modern UI components and frameworks
- **full-stack-architect** - Complete system design

### Infrastructure & DevOps
- **devops-engineer** - CI/CD and containerization
- **devops-troubleshooter** - Production incident response
- **cloud-architect** - AWS/GCP/Azure infrastructure
- **deployment-engineer** - Release automation
- **database-optimizer** - Performance tuning
- **incident-commander** - Emergency response coordination

### Quality & Security
- **code-reviewer** - Code quality and best practices
- **test-engineer** - Testing strategy and implementation
- **performance-engineer** - Optimization and profiling
- **quality-engineer** - QA processes and standards
- **security-auditor** - Vulnerability scanning and compliance

### Data & AI
- **data-engineer** - ETL pipelines and data architecture
- **ai-engineer** - LLM integration and RAG systems
- **ml-engineer** - Model training and deployment
- **data-ai-ml-engineer** - Full-stack data science

### Product & Business
- **api-documenter** - Documentation and guides
- **dx-optimizer** - Developer experience improvement
- **user-feedback-analyst** - User research and insights
- **business-analyst** - Metrics and KPI analysis
- **content-marketer** - Content strategy and SEO
- **tech-portfolio-reviewer** - Resume and portfolio optimization

### Tools
- **git-specialist** - Version control operations

</details>

<details>
<summary><strong>🎮 How the Gamification Works</strong></summary>

### Agent Levels & Tiers
- **🟢 Novice** (Lv.1-10) - Learning the basics, understanding your patterns
- **🔵 Adept** (Lv.11-30) - Developing expertise, understanding project conventions
- **🟡 Expert** (Lv.31-70) - Mastering techniques, anticipating your needs
- **🟠 Master** (Lv.71-120) - Elite performance, proactive recommendations
- **🔴 Grandmaster** (Lv.121-200) - Legendary status, deep project insight
- **💎 Legend** (Lv.201+) - Ultimate mastery, transcendent capabilities

### Sample Achievements
- 🩸 **First Blood** - Complete your first task (+50 XP)
- ⚡ **Speed Demon** - Fast completions (+300 XP)
- 🐛 **Bug Hunter** - Resolve 10 production bugs (+150 XP)
- 🛡️ **Guardian Angel** - Prevent security vulnerabilities (+400 XP)

### XP Tracking
```bash
./agents                    # View all agent levels
./agents python-pro         # Check specific agent  
./agents log python-pro "Built API"  # Manual XP logging
```

</details>

<details>
<summary><strong>🤖 Smart Agent Registry (Advanced)</strong></summary>

The **Agent Registry System** automatically discovers and coordinates all available agents, including custom ones you create:

```bash
# Claude Code automatically coordinates agents based on your request
"Build a React TypeScript dashboard with real-time data"
# Automatically coordinates: react-specialist → typescript-pro → data-engineer → test-engineer
```

**Why This Matters**: No more manual coordination - the system intelligently selects agents based on:
- Your project's tech stack
- Agent expertise and performance history  
- Task complexity and requirements
- Agent availability and XP levels

**Features**:
- ✅ Automatic agent discovery from multiple locations
- ✅ Tech stack analysis and matching
- ✅ Performance-based recommendations
- ✅ XP tracking integration
- ✅ Smart team formation

</details>

## 📊 SubAgents Analytics System

Experience the power of data-driven AI development with our comprehensive analytics system. Track agent performance, monitor team effectiveness, and optimize your development workflow with beautiful visualizations.

### 🏆 XP Leaderboard - See Your Champions Rise

```ansi
╔══════════════════════════════════════════════════════════════════════╗
║                           🏆 AGENT LEADERBOARD 🏆                    ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  🥇 #1  python-pro              ████████████████████ 💎 Legend       ║
║         Level 247 • 124,750 XP • 🏅 Speed Demon • Bug Hunter        ║
║                                                                      ║
║  🥈 #2  devops-troubleshooter   ███████████████████▒ 🔴 Grandmaster  ║
║         Level 183 • 91,500 XP  • 🛡️ Guardian Angel • Fire Fighter   ║
║                                                                      ║
║  🥉 #3  full-stack-architect    ██████████████████▒▒ 🟠 Master       ║
║         Level 156 • 78,000 XP  • 🏗️ System Builder • Team Player    ║
║                                                                      ║
║  4   security-auditor           ███████████████▒▒▒▒▒ 🟠 Master       ║
║      Level 142 • 71,000 XP     • 🔒 Vault Keeper • Threat Hunter    ║
║                                                                      ║
║  5   frontend-developer         ████████████▒▒▒▒▒▒▒▒ 🟡 Expert       ║
║      Level 89 • 44,500 XP      • ✨ UI Wizard • Performance Pro     ║
║                                                                      ║
║  💫 Recent Achievements                                              ║
║  • python-pro earned "Code Ninja" (+500 XP) - 50 perfect reviews   ║
║  • devops-troubleshooter earned "Crisis Hero" (+750 XP)             ║
║  • security-auditor earned "Vault Keeper" (+400 XP)                 ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 🎯 Team Formation Analysis - Perfect Team Chemistry

```ansi
╔══════════════════════════════════════════════════════════════════════╗
║                      🎯 TEAM FORMATION INSIGHTS                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  🚀 MOST EFFECTIVE TEAM COMBINATIONS                                ║
║  ────────────────────────────────────────────────────────────────   ║
║                                                                      ║
║  1. "Full-Stack Dream Team" (Success Rate: 94%)                     ║
║     🏗️ full-stack-architect → 🐍 python-pro → ⚛️ frontend-developer ║
║     💡 Synergy Bonus: +25% XP when working together                 ║
║     📈 Avg Completion Time: 23% faster than individual work         ║
║                                                                      ║
║  2. "Security & Performance Team" (Success Rate: 91%)               ║
║     🔒 security-auditor → ⚡ performance-engineer → 🛠️ devops-engineer║
║     💡 Synergy Bonus: +30% XP for critical infrastructure tasks     ║
║     🎯 Speciality: Zero-downtime deployments with security audits   ║
║                                                                      ║
║  3. "Data Intelligence Unit" (Success Rate: 88%)                    ║
║     📊 data-engineer → 🤖 ai-engineer → 🧪 ml-engineer              ║
║     💡 Synergy Bonus: +35% XP for ML/AI pipeline tasks             ║
║     🚀 Achievement Unlock: "Data Wizards" team achievement          ║
║                                                                      ║
║  📊 FORMATION STATS THIS MONTH                                      ║
║  • Total Teams Formed: 47                                           ║
║  • Average Team Size: 3.2 agents                                    ║
║  • Most Popular Agent: python-pro (32 formations)                   ║
║  • Highest XP Team: "Backend Legends" (1,247 XP earned)             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 📈 Usage Insights - Your Development Patterns

```ansi
╔══════════════════════════════════════════════════════════════════════╗
║                        📈 USAGE INSIGHTS DASHBOARD                   ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  🕐 PEAK PERFORMANCE HOURS                                          ║
║  ─────────────────────────                                          ║
║  09:00-11:00  ████████████████████████████████ 87% efficiency       ║
║  14:00-16:00  ██████████████████████████████▒▒ 82% efficiency       ║
║  20:00-22:00  ████████████████████████▒▒▒▒▒▒▒▒ 68% efficiency       ║
║                                                                      ║
║  📊 TASK CATEGORY BREAKDOWN (Last 30 Days)                         ║
║  ──────────────────────────────────────────                        ║
║  Bug Fixes        ████████████████████ 34% (127 tasks)             ║
║  Feature Dev      ███████████████████▒ 31% (116 tasks)             ║
║  Code Review      ███████████▒▒▒▒▒▒▒▒▒ 18% (67 tasks)              ║
║  Optimization     ████████▒▒▒▒▒▒▒▒▒▒▒▒ 12% (45 tasks)              ║
║  Security Audit   ███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ 5% (19 tasks)               ║
║                                                                      ║
║  🏆 ACHIEVEMENT PROGRESS                                            ║
║  ─────────────────────                                              ║
║  🩸 First Blood        ✅ Unlocked  (+50 XP)                       ║
║  ⚡ Speed Demon       ✅ Unlocked  (+300 XP)                       ║
║  🐛 Bug Hunter        ✅ Unlocked  (+150 XP)                       ║
║  🛡️ Guardian Angel    ▓▓▓▓▓▓▓▓░░  80% Complete (+400 XP pending)   ║
║  🏗️ System Builder   ▓▓▓▓▓▓░░░░  60% Complete (+500 XP pending)   ║
║  💎 Code Ninja       ▓▓▓░░░░░░░  30% Complete (+750 XP pending)   ║
║                                                                      ║
║  📈 PRODUCTIVITY TRENDS                                             ║
║  • 23% faster task completion vs last month                         ║
║  • 67% increase in multi-agent collaborations                      ║
║  • 91% user satisfaction rate (based on task success)              ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 💻 Analytics Commands - Unlock Your Team's Potential

Master these commands to get the most out of your SubAgents analytics:

```bash
# 🏆 LEADERBOARD & RANKINGS
./agents leaderboard                    # View full XP leaderboard
./agents top 10                        # Show top 10 agents
./agents levels                         # Display all agent levels
./agents achievements                   # Show recent achievements

# 📊 DETAILED AGENT ANALYTICS  
./agents stats python-pro              # Individual agent performance
./agents history devops-troubleshooter # Task completion history
./agents efficiency frontend-developer # Performance metrics & trends

# 🎯 TEAM FORMATION INSIGHTS
./agents formations                     # Most effective team combinations
./agents synergy                       # Current team synergy bonuses
./agents recommend "web app project"   # Get team recommendations
./agents chemistry                     # Analyze team compatibility

# 📈 USAGE & PRODUCTIVITY INSIGHTS
./agents insights                      # Personal usage patterns
./agents trends                        # 30-day productivity trends
./agents peak-hours                    # Your most productive times
./agents categories                    # Task breakdown analysis

# 🎮 GAMIFICATION FEATURES
./agents xp-log "Built REST API" 150  # Manually log XP for custom tasks
./agents missions                      # View available achievements
./agents progress "Bug Hunter"        # Track specific achievement progress
./agents celebrate                    # View recent accomplishments

# 📊 EXPORT & REPORTING
./agents export-stats                  # Export analytics to CSV
./agents weekly-report                 # Generate weekly summary
./agents compare-agents                # Side-by-side agent comparison
./agents project-dna "my-project"     # Analyze project requirements
```

### 🎨 Real-Time Mission Tracking

Watch your agents collaborate in real-time with beautiful progress visualizations:

```ansi
╔══════════════════════════════════════════════════════════════════════╗
║                    🚀 MISSION IN PROGRESS: "API Optimization"        ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  👥 ACTIVE TEAM: Performance Dream Team                             ║
║  • ⚡ performance-engineer    [████████████████████] 100% Complete   ║
║  • 🐍 python-pro             [███████████████████▒] 95% Complete    ║
║  • 📊 database-optimizer     [████████████████▒▒▒▒] 80% Complete    ║
║                                                                      ║
║  📈 REAL-TIME METRICS                                               ║
║  ────────────────────                                               ║
║  Mission XP Earned: 1,247 XP (+25% team synergy bonus)             ║
║  Estimated Completion: 12 minutes                                   ║
║  Current Efficiency: 127% (above average)                           ║
║                                                                      ║
║  🎯 ACTIVE ACHIEVEMENTS                                             ║
║  • Speed Demon: 8/10 fast completions                              ║
║  • Team Player: 15/20 successful collaborations                    ║
║  • Performance Pro: 4/5 optimization tasks                         ║
║                                                                      ║
║  💫 RECENT ACTIVITY                                                 ║
║  • python-pro identified 3 bottlenecks (+75 XP)                   ║
║  • performance-engineer optimized query performance (+100 XP)       ║
║  • database-optimizer suggested index improvements (+50 XP)        ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 🎯 Getting Started with Analytics

1. **View Your Leaderboard**: `./agents leaderboard` - See which agents are leading the pack
2. **Check Team Chemistry**: `./agents formations` - Discover your most effective team combinations  
3. **Analyze Your Patterns**: `./agents insights` - Understand your development workflow
4. **Track Achievements**: `./agents achievements` - Monitor progress toward unlocking new badges
5. **Export Data**: `./agents export-stats` - Get detailed analytics for reporting

**Pro Tip**: Use `./agents recommend "your project description"` to get AI-powered team suggestions based on your specific needs and historical performance data.

<details>
<summary><strong>🚀 Installation Options</strong></summary>

### Standard Installation
```bash
cd ~/.claude && git clone https://github.com/mylee04/claude-code-subagents.git agents
```

### With Visual Feedback
```bash
git clone https://github.com/mylee04/claude-code-subagents.git
cd claude-code-subagents
./install.sh
```

### Manual Installation  
```bash
git clone https://github.com/mylee04/claude-code-subagents.git
cp -r claude-code-subagents/agents/* ~/.claude/agents/
```

</details>

<details>
<summary><strong>💡 Usage Examples</strong></summary>

### Single Agent Tasks
```bash
# Development
/python-pro "refactor this class with proper type hints"
/javascript-pro "optimize this React component performance"
/golang-pro "implement concurrent worker pool"

# Infrastructure  
/devops-troubleshooter "analyze these error logs"
/database-optimizer "optimize this slow query"
/cloud-architect "design auto-scaling strategy"

# Quality & Security
/code-reviewer "review this pull request"
/security-auditor "audit authentication flow"
/test-engineer "create comprehensive test suite"
```

### Multi-Agent Workflows
```bash
# Feature Development
"Implement user authentication with social login"
# Claude Code coordinates: backend-architect → frontend-developer → security-auditor → test-engineer

# Performance Optimization  
"Optimize application for 10x traffic increase"
# Claude Code coordinates: performance-engineer → database-optimizer → cloud-architect → deployment-engineer

# Production Issues
"Debug API timeout issues in production"  
# Claude Code coordinates: devops-troubleshooter → performance-engineer → database-optimizer
```

</details>

<details>
<summary><strong>🔧 Troubleshooting</strong></summary>

### Slash Commands Not Working?
1. **Check installation**: `ls ~/.claude/agents/` should show agent files
2. **Verify agent format**: Agents need YAML frontmatter:
   ```yaml
   ---
   name: agent-name
   description: Agent description
   ---
   ```
3. **Alternative methods**: Use natural language ("Use python-pro to...") or Task tool

### Agents Not Appearing in `/agents`?
**Problem**: Files exist but don't show in command list  
**Solution**: Add YAML frontmatter to the top of each `.md` file

### Task Tool Says "Agent Not Found"?
**Cause**: Missing YAML frontmatter  
**Fix**: Add the required YAML header and the agent will work immediately

</details>

<details>
<summary><strong>🤝 Contributing</strong></summary>

### Adding New Agents
1. Create `.md` file in appropriate category folder
2. **REQUIRED**: Include YAML frontmatter:
   ```yaml
   ---
   name: your-agent-name
   description: Brief description
   color: blue  # optional
   ---
   ```
3. Run `./install.sh` to make agent available
4. Submit pull request

### Areas We Need
- Mobile Development (Swift, Kotlin, React Native)
- Game Development (Unity, Unreal Engine)  
- Blockchain (Solidity, Web3)
- Domain-specific experts (Healthcare, Finance, E-commerce)

</details>

## Why Developers Love This

> "It's like Pokemon for developers - I actually look forward to debugging now!" - *Senior Engineer*

> "Cut our development time by 70% on a major refactoring project" - *Tech Lead*

| Feature | Other Collections | SubAgents |
|---------|------------------|-------------|
| Basic Agents | ✅ Yes | ✅ 31 Specialists |
| **Gamification** | ❌ No | ✅ **Full XP System** |
| **Project Scanner** | ❌ No | ✅ **DNA Analysis** |
| **Team Synergies** | ❌ No | ✅ **Formation Bonuses** |

## Get Started

1. **Install**: `cd ~/.claude && git clone https://github.com/mylee04/claude-code-subagents.git agents`
2. **Try the demo**: `python3 gamification/scripts/agents-demo.py`
3. **Plan a feature**: "Build user authentication system"
4. **Use specific agents**: `/python-pro optimize this function`

**First Mission Bonus**: Complete your first task and earn the "First Blood" achievement (+50 XP)

---

**Ready to level up your development workflow?** Install now and experience the power of 31 AI specialists working as your personal dev team.

Made with ❤️ for developers who demand excellence | [License: MIT](LICENSE) | [Issues & Support](https://github.com/mylee04/claude-code-subagents/issues)