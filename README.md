# Claude Code Elite Squad

> **"Pokemon for Developers"** - Your AI agents level up, form teams, and tackle any coding challenge

**Quick Start**: `cd ~/.claude && git clone https://github.com/mylee04/claude-code-subagents.git agents` (10 seconds)

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Elite%20Squad-red)](https://github.com/anthropics/claude-code)
[![Agents](https://img.shields.io/badge/agents-31-orange)](agents/)
[![XP System](https://img.shields.io/badge/XP%20System-Active-green)](GAMIFICATION-DESIGN.md)

## What Is This?

A **gamified collection of 31 specialized AI agents** that work together like a development team. Each agent levels up as you use them, unlocks achievements, and forms powerful combinations for complex tasks.

**Core Value**: Instead of one generic AI assistant, you get a specialized squad where each agent is an expert in their domain (Python, DevOps, Security, etc.).

## Key Features

- **31 Specialist Agents** - From Python experts to security auditors
- **Gamification System** - Agents gain XP, level up (Recruit → Elite), earn achievements
- **Project DNA Scanner** - Automatically generates custom agents for your tech stack
- **Team Formations** - Agents work together with synergy bonuses
- **Real Progress Tracking** - Watch your AI squad collaborate in real-time

## Interactive Demo

Try it now - see the XP system, achievements, and agent collaboration in action:

```bash
cd ~/.claude/agents && python3 gamification/scripts/squad-demo.py
```

Watch agents level up, earn achievements like "Speed Demon" and "Bug Hunter", and see real-time mission progress.

## Basic Usage

```bash
# Generate custom agents for your project
/agent-assembler

# Use specific agents
/python-pro optimize this function
/devops-troubleshooter analyze these logs
/security-auditor review authentication flow

# Complex multi-agent tasks
/feature-planner Implement user dashboard with real-time data
```

<details>
<summary><strong>📋 All 31 Agents (Click to expand)</strong></summary>

### Command & Planning
- **agent-assembler** - Generates custom agents for your tech stack
- **feature-planner** - Orchestrates complex multi-agent workflows

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

### Agent Levels
- **Lv.1 Recruit** (0-99 XP) - Learning your patterns
- **Lv.2 Specialist** (100-299 XP) - Understanding project conventions
- **Lv.3 Expert** (300-599 XP) - Anticipating your needs  
- **Lv.4 Master** (600-999 XP) - Proactive recommendations
- **Lv.5 Elite** (1000+ XP) - Legendary project insight

### Sample Achievements
- 🩸 **First Blood** - Complete your first task (+50 XP)
- ⚡ **Speed Demon** - Fast completions (+300 XP)
- 🐛 **Bug Hunter** - Resolve 10 production bugs (+150 XP)
- 🛡️ **Guardian Angel** - Prevent security vulnerabilities (+400 XP)

### XP Tracking
```bash
./squad                    # View all agent levels
./squad python-pro         # Check specific agent  
./squad log python-pro "Built API"  # Manual XP logging
```

</details>

<details>
<summary><strong>🧬 Project DNA Scanner (Advanced)</strong></summary>

The **agent-assembler** analyzes your `claude.md` file and creates specialized agents for your exact tech stack:

```bash
/agent-assembler
# Scans your project → Creates custom agents like:
# - react-typescript-specialist  
# - supabase-backend-expert
# - tailwind-ui-designer
```

**Why This Matters**: Instead of generic responses, you get agents that know your specific frameworks, coding standards, and architecture patterns.

**Example Output**:
```
🎯 Mission Analysis Complete: Your AI SaaS Platform

✓ Created: nextjs-app-router-specialist.md
  Expert in Next.js 14, TypeScript, and Vite

✓ Created: supabase-backend-specialist.md  
  Supabase expert with RLS policies and real-time

✓ Created: tailwind-ui-designer.md
  Tailwind CSS v3 component architect
```

</details>

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
# Coordinates: backend-architect → frontend-developer → security-auditor → test-engineer

# Performance Optimization  
"Optimize application for 10x traffic increase"
# Coordinates: performance-engineer → database-optimizer → cloud-architect → deployment-engineer

# Production Issues
"Debug API timeout issues in production"  
# Coordinates: devops-troubleshooter → performance-engineer → database-optimizer
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

| Feature | Other Collections | Elite Squad |
|---------|------------------|-------------|
| Basic Agents | ✅ Yes | ✅ 31 Specialists |
| **Gamification** | ❌ No | ✅ **Full XP System** |
| **Project Scanner** | ❌ No | ✅ **DNA Analysis** |
| **Team Synergies** | ❌ No | ✅ **Formation Bonuses** |

## Get Started

1. **Install**: `cd ~/.claude && git clone https://github.com/mylee04/claude-code-subagents.git agents`
2. **Try the demo**: `python3 gamification/scripts/squad-demo.py`
3. **Generate custom agents**: `/agent-assembler`
4. **Start coding**: `/python-pro optimize this function`

**First Mission Bonus**: Complete your first task and earn the "First Blood" achievement (+50 XP)

---

**Ready to level up your development workflow?** Install now and experience the power of 31 AI specialists working as your personal dev team.

Made with ❤️ for developers who demand excellence | [License: MIT](LICENSE) | [Issues & Support](https://github.com/mylee04/claude-code-subagents/issues)