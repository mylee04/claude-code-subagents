# 🎮 Claude Code Elite Squad - AI Development RPG

> **Level up your AI agents** as they complete missions, unlock achievements, and form legendary dev teams

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Elite%20Squad-red)](https://github.com/anthropics/claude-code)
[![Agents](https://img.shields.io/badge/agents-31-orange)](agents/)
[![XP System](https://img.shields.io/badge/XP%20System-Active-green)](GAMIFICATION-DESIGN.md)
[![Stars](https://img.shields.io/github/stars/mylee04/claude-code-subagents?style=social)](https://github.com/mylee04/claude-code-subagents)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

<div align="center">

```
🎖️  ELITE AI DEVELOPMENT SQUAD - MISSION CONTROL  🎖️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Status: OPERATIONAL | Squad Size: 31 | Total XP: 12,450
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 🚀 **"It's Pokemon for Developers"** - Your AI agents level up, unlock achievements, and form legendary teams!

</div>

## ⚡ Deploy Your Squad (10 seconds)

```bash
cd ~/.claude && git clone https://github.com/mylee04/claude-code-subagents.git agents
```

**🏆 First Mission Bonus**: Complete your first task and earn **"First Blood"** achievement (+50 XP)

## 🎯 What Makes This Different?

### 🎮 **Gamified AI Development**
- **Level System**: Agents gain XP and level up (Recruit → Specialist → Expert → Master → Elite)
- **Achievements**: Unlock 20+ achievements like "Bug Hunter" 🐛 and "Speed Demon" ⚡
- **Team Synergies**: Discover powerful agent combinations for bonus effectiveness
- **Real-Time Visualization**: Watch your AI squad collaborate with live progress tracking

### 🔬 **Project DNA Scanner** 
Your secret weapon - the enhanced `agent-assembler`:
```bash
/agent-assembler
# Scans your project and generates the PERFECT squad
# with synergy bonuses and formation recommendations
```

### 📊 **Live Mission Tracking**
Watch your AI team in action:

```
┌─────────────────────────────────────────────────────────┐
│                  MISSION: Build User Auth                │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [backend-architect] ═══► [security-auditor]          │
│      Lv.3 ⭐⭐⭐              Lv.4 ⭐⭐⭐⭐               │
│         ║                        ║                      │
│         ╚════► [frontend-developer] ═══► [test-engineer]│
│                    Lv.2 ⭐⭐           Lv.3 ⭐⭐⭐        │
│                                                         │
├─────────────────────────────────────────────────────────┤
│ Progress: ████████████░░░░░░░ 65%  | XP Earned: 120   │
└─────────────────────────────────────────────────────────┘
```

## 🏆 Current Leaderboard

| Rank | Agent | Level | XP | Missions | Specialty |
|------|-------|-------|-----|----------|-----------||
| 🥇 | python-elite | Lv.4 Expert | 850 XP | 127 | Speed Demon 🔥 |
| 🥈 | devops-troubleshooter | Lv.3 Expert | 680 XP | 98 | Bug Hunter 🐛 |
| 🥉 | security-auditor | Lv.5 Elite | 1,250 XP | 156 | Perfect Score 💯 |

## 🎨 Your Elite Squad (31 Specialists)

<table>
<tr>
<td>

**🎯 Command (2)**
- agent-assembler
- feature-planner

**💻 Development (10)**  
- python-elite
- javascript-pro
- golang-pro
- rust-pro
- sql-pro
- backend-architect
- frontend-developer
- full-stack-architect
- git-specialist

</td>
<td>

**⚙️ Infrastructure (6)**
- devops-engineer
- devops-troubleshooter
- cloud-architect
- deployment-engineer
- database-optimizer
- incident-commander

**✅ Quality (4)**
- code-reviewer
- test-engineer
- performance-engineer
- quality-engineer

</td>
<td>

**🔒 Security (1)**
- security-auditor

**🧠 Data & AI (4)**
- data-engineer
- ai-engineer
- ml-engineer
- data-ai-ml-engineer

**📈 Product (4)**
- api-documenter
- dx-optimizer
- user-feedback-analyst
- tech-portfolio-reviewer

</td>
</tr>
</table>

## 📚 Quick Navigation

- [📋 Available Agents](#-available-agents) - Browse all 30+ agents
- [💡 Usage Examples](#-usage-examples) - Real-world workflows
- [🔄 Multi-Agent Workflows](#-multi-agent-workflows) - Complex orchestration patterns
- [⚡ Best Practices](#-best-practices) - Tips for effective use
- [🔧 Troubleshooting](#-troubleshooting) - Common issues and solutions
- [🤝 Contributing](#-contributing) - Add your own agents

## 🚀 Installation

```bash
cd ~/.claude
git clone https://github.com/mylee04/agent-collection.git agents
```

That's it! Your agents are ready to use. 🎉

### Alternative Installation Methods

<details>
<summary>📦 Install with visual feedback</summary>

```bash
git clone https://github.com/mylee04/claude-code-subagents.git
cd claude-code-subagents
./install.sh
```
</details>

<details>
<summary>🔧 Manual installation</summary>

```bash
# Clone anywhere and copy manually
git clone https://github.com/mylee04/claude-code-subagents.git
cp -r claude-code-subagents/agents/* ~/.claude/agents/
```
</details>

## ⚡ Quick Start

### Prerequisites

- [Claude Code](https://github.com/anthropics/claude-code) installed

### Start Using Agents

```bash
# Generate custom agents for your project
/agent-assembler

# Use specific agents
/python-pro optimize this function
/devops-troubleshooter analyze these logs
/feature-planner design user authentication
```

## 🎨 Agent Management Approaches

There are two ways to manage agents in Claude Code:

### 1. Global/Personal Agents (via this repository)
These are general-purpose agents installed to `~/.claude/agents/` that are available across all your projects:

```bash
# Install all agents globally
./install.sh
```

**Benefits:**
- ✅ Available in any project
- ✅ Shared collection of battle-tested agents
- ✅ Easy bulk installation

**Use for:**
- Common development tasks (git, testing, code review)
- General-purpose agents you use frequently
- Base agents that work across different tech stacks

### 2. Project-Specific Agents (via /agents command)
These are custom agents created for specific projects:

```bash
# In Claude Code, use:
/agents → Create new agent
```

**Benefits:**
- ✅ Automatically recognized when using proper YAML frontmatter
- ✅ Works with Task tool when formatted correctly
- ✅ Project-specific knowledge and conventions
- ✅ Generated by agent-assembler for your exact tech stack

**Use for:**
- Agents generated by `/agent-assembler`
- Project-specific conventions and workflows
- Tech stack-specific agents (e.g., `nextjs-app-router-expert`)

💡 **Important**: Agents MUST have proper YAML frontmatter to work with the Task tool and appear in `/agents` command, regardless of how they're created.

## 🎨 Visual Agent Indicators

Claude Code uses visual cues to show agent status:

### ✅ Agents with Correct YAML Frontmatter
![Agent with colored background](docs/images/registered-agent-colored.png)
- **Colored background badges** (orange, blue, etc.)
- Have proper YAML frontmatter format
- Work with both slash commands and Task tool
- Show in `/agents` command list
- Can be organized into "Personal" or "Project" sections

### ❌ Agents with Incorrect Format (Missing YAML Frontmatter)
![Agents without YAML frontmatter](docs/images/file-based-agents.png)
- **Blue arrow icons** without colored backgrounds
- Missing required YAML frontmatter at the top of the file
- Don't appear in `/agents` command list
- Won't work with Task tool
- **Easy fix**: Just add the YAML frontmatter!

### 📁 Project Agents Location
Project agents can be stored in `.claude/agents/` within your project directory. To make them show in the "Project agents" section with proper colors:

1. Create `.claude/agents/` directory in your project
2. Add `.md` files with proper YAML frontmatter
3. Agents automatically appear under "Project agents" in `/agents`
4. You'll see the colored background indicating proper format

## 🔑 CRITICAL: Agent File Format Requirement

**BREAKTHROUGH DISCOVERY!** Agents MUST have YAML frontmatter to be recognized by Claude Code!

### ✅ Correct Format (Works with /agents)
```markdown
---
name: your-agent-name
description: Brief description of what this agent does
color: blue  # optional: blue, green, yellow, red, purple, cyan, orange
---

You are the Agent Name, a specialist in...
```

### ❌ Incorrect Format (Won't be recognized)
```markdown
# Your Agent Name

You are a specialist in...
```

Without the YAML frontmatter:
- ❌ Agent won't appear in `/agents` command
- ❌ Can't be used with Task tool
- ❌ Won't have colored background badge
- ❌ Not recognized by Claude Code due to missing format

**The Fix**: Simply add the YAML frontmatter to any `.md` file in `.claude/agents/` and it will automatically appear in the `/agents` list!

### 📸 Visual Proof

**Before**: Agents without YAML frontmatter (not recognized)
![Agents not showing in /agents command](docs/images/agents-not-recognized.png)

**After**: Same agents with YAML frontmatter added
![All agents now showing in /agents command](docs/images/agents-recognized.png)

Notice how all 6 claude-arena agents now appear in the "Project agents" section!

### 📖 How to Use the Agents

#### Method 1: Using Slash Commands (Recommended)
Once agents are installed in `~/.claude/agents/`, you can use them with slash commands:

```bash
# Generate custom agents for your project
/agent-assembler

# Plan a complex feature
/feature-planner Implement real-time metrics dashboard

# Use specific agents directly
/backend-architect Design the database schema for datasets
/frontend-developer Create the user dashboard component
/security-auditor Review authentication implementation
```

#### Method 2: Using Natural Language
If slash commands aren't working, you can invoke agents naturally:

```
Use the agent-assembler to analyze my claude.md and create custom agents
```

#### Method 3: Using the Task Tool
For more complex operations:

```
Use the feature-planner agent to design a user authentication system
```

### 🎯 Typical Workflow

1. **First, generate project-specific agents**:
   ```
   /agent-assembler
   ```
   This reads your `claude.md` and creates custom agents like `react-specialist` or `postgres-expert`

2. **Then, use conductor agents for complex tasks**:
   ```
   /feature-planner Build a real-time chat feature
   ```

3. **Or use specialist agents directly**:
   ```
   /database-optimizer Analyze and improve query performance
   ```

### ✅ What Happens Next?

After running `/agent-assembler`, you'll receive:
1. **Agent definitions** for your specific tech stack (e.g., `react-typescript-specialist`, `supabase-backend-specialist`)
2. **Instructions** to add each agent via the `/agents` command
3. **Ready-to-use content** for each custom agent

To use your generated agents:
```bash
# 1. Run agent-assembler
/agent-assembler

# 2. For each generated agent:
/agents → Create new agent → Paste the content

# 3. Now use your custom agents!
/react-typescript-specialist Build a data dashboard
```

### 🏷️ Creating Project-Specific Agents

For agents to appear in the "Project agents" section with proper colors:

1. **Create project agents directory**:
   ```bash
   mkdir -p .claude/agents
   ```

2. **Add agent files with YAML frontmatter**:
   ```yaml
   ---
   name: project-agent-name
   description: Description of your project agent
   color: blue  # optional
   ---
   
   You are a specialist for this project...
   ```

3. **Result**:
   - Agent automatically shows under "Project agents (.claude/agents)"
   - Has colored background (orange, blue, etc.)
   - Works with Task tool immediately
   - Only available when in that project

💡 **Pro tip**: The agent-assembler creates agents tailored to YOUR project's specific tech stack, coding standards, and goals from your `claude.md` file!

## 📋 Available Agents

### 🧠 Conductor & Workflow Leads
Agents that coordinate other agents and manage complex workflows.

| Agent | Description | Key Features |
|-------|-------------|--------------|
| [`agent-assembler`](agents/conductor/agent-assembler.md) | Generates custom agents based on your tech stack | Reads claude.md, creates specialized agents |
| [`feature-planner`](agents/conductor/feature-planner.md) | Orchestrates agents for complex features | Multi-agent coordination, technical planning |

### 💻 Development & Architecture
Core development agents for building features and designing systems.

| Agent | Description | Expertise |
|-------|-------------|-----------|
| [`backend-architect`](agents/development/backend-architect.md) | Designs robust backend services and APIs | RESTful APIs, microservices, DDD, scalability |
| [`frontend-developer`](agents/development/frontend-developer.md) | Builds modern UI components | React/Vue/Angular, state management, responsive design |
| [`full-stack-architect`](agents/development/full-stack-architect.md) | Complete system architecture design | Backend, databases, frontend integration |
| [`python-pro`](agents/development/python-pro.md) | Python development expert | Type hints, async, Django/FastAPI, testing |
| [`javascript-pro`](agents/development/javascript-pro.md) | JavaScript/TypeScript specialist | ES6+, React, Node.js, build tools |
| [`golang-pro`](agents/development/golang-pro.md) | Go language expert | Goroutines, channels, interfaces, performance |
| [`rust-pro`](agents/development/rust-pro.md) | Rust programming specialist | Ownership, lifetimes, traits, zero-cost abstractions |
| [`sql-pro`](agents/development/sql-pro.md) | SQL and database query expert | Complex queries, optimization, all SQL dialects |
| [`git-specialist`](agents/development/git-specialist.md) | Git operations expert | Commits, branches, PRs (never commits without permission) |

### ✅ Quality & Testing
Comprehensive quality assurance and testing specialists.

| Agent | Description | Focus Areas |
|-------|-------------|-------------|
| [`quality-engineer`](agents/quality/quality-engineer.md) | Quality assurance expert | Testing, code review, best practices |
| [`code-reviewer`](agents/quality/code-reviewer.md) | Meticulous code review specialist | Security, maintainability, best practices |
| [`test-engineer`](agents/quality/test-engineer.md) | Testing strategy and implementation | TDD, unit/integration/e2e tests |
| [`performance-engineer`](agents/quality/performance-engineer.md) | Performance optimization expert | Profiling, bottlenecks, scalability |

### 🔒 Security
Security-focused agents for vulnerability detection and compliance.

| Agent | Description | Specialization |
|-------|-------------|----------------|
| [`security-auditor`](agents/security/security-auditor.md) | Security vulnerability scanner | OWASP compliance, penetration testing |

### 🏗️ Infrastructure & Operations
DevOps, cloud infrastructure, and operational excellence.

| Agent | Description | Tools & Platforms |
|-------|-------------|-------------------|
| [`cloud-architect`](agents/infrastructure/cloud-architect.md) | Cloud infrastructure design | AWS, GCP, Azure, cost optimization |
| [`devops-engineer`](agents/infrastructure/devops-engineer.md) | Full-stack DevOps specialist | CI/CD, Kubernetes, monitoring |
| [`devops-troubleshooter`](agents/infrastructure/devops-troubleshooter.md) | Production incident responder | Log analysis, debugging, root cause analysis |
| [`deployment-engineer`](agents/infrastructure/deployment-engineer.md) | Deployment automation expert | Pipelines, containers, release strategies |
| [`database-optimizer`](agents/infrastructure/database-optimizer.md) | Database performance specialist | Query optimization, indexing, scaling |

### 📊 Data & AI
Data engineering, machine learning, and AI system specialists.

| Agent | Description | Technologies |
|-------|-------------|--------------|
| [`data-engineer`](agents/data/data-engineer.md) | Data pipeline architect | ETL/ELT, Spark, Kafka, data warehouses |
| [`data-ai-ml-engineer`](agents/data/data-ai-ml-engineer.md) | Comprehensive data & AI specialist | Pipelines, ML ops, LLM deployments |
| [`ai-engineer`](agents/data/ai-engineer.md) | AI systems architect | RAG, LLM integration, agent design |
| [`ml-engineer`](agents/data/ml-engineer.md) | Machine learning engineer | Model training, deployment, MLOps |

### 🎯 Product & Business
Product development, business analysis, and specialized domains.

| Agent | Description | Use Cases |
|-------|-------------|-----------|
| [`api-documenter`](agents/product/api-documenter.md) | API documentation specialist | OpenAPI/Swagger, examples, guides |
| [`dx-optimizer`](agents/product/dx-optimizer.md) | Developer experience expert | Tooling, workflows, productivity |
| [`user-feedback-analyst`](agents/product/user-feedback-analyst.md) | User insight extraction | Feedback analysis, feature prioritization |
| [`business-analyst`](agents/business/business-analyst.md) | Business metrics expert | KPIs, reports, strategic analysis |
| [`content-marketer`](agents/business/content-marketer.md) | Content marketing specialist | SEO, blog posts, social media, email campaigns |
| [`tech-portfolio-resume-review-specialist`](agents/product/tech-portfolio-resume-review-specialist.md) | Career optimization specialist | Portfolio/resume enhancement |

## 🔧 How It Works

### 1. Initial Setup - Agent Generation
The `agent-assembler` reads your `claude.md` file and:
- Analyzes your technology stack and project needs
- Generates new custom agent files specific to your project
- Places them in your `~/.claude/agents/` directory
- Creates agents like `react-specialist` or `postgres-expert` based on your stack

### 2. Task Execution - Agent Orchestration
When you need to accomplish complex tasks:
- Use conductor agents like `feature-planner` to coordinate work
- The conductor invokes relevant specialist agents
- Each specialist handles their domain (backend, frontend, security, etc.)
- Results are synthesized into a cohesive solution

### 3. Collaborative Workflow
The two-layer system ensures:
- You have the right agents for your specific project (via generation)
- Those agents work together effectively (via orchestration)
- Complex tasks are broken down and distributed properly
- No duplicate effort or gaps in coverage

## 💡 Usage Examples

### Single Agent Tasks

#### Development Tasks
```bash
# Python development
"Use python-pro to refactor this class with proper type hints"
"Have python-pro implement async data processing pipeline"

# JavaScript/TypeScript
"Get javascript-pro to optimize this React component performance"
"Use javascript-pro to convert callbacks to async/await"

# Go development
"Have golang-pro implement concurrent worker pool"
"Use golang-pro to optimize memory allocations"

# Backend architecture
"Get backend-architect to design microservice boundaries"
"Use backend-architect to plan API versioning strategy"
```

#### Infrastructure & Operations
```bash
# Troubleshooting production issues
"Use devops-troubleshooter to analyze these error logs"
"Have devops-troubleshooter find root cause of memory leak"

# Deployment and CI/CD
"Get deployment-engineer to set up blue-green deployment"
"Use deployment-engineer to optimize GitHub Actions workflow"

# Database optimization
"Have database-optimizer analyze slow query performance"
"Use database-optimizer to design sharding strategy"
```

#### Quality & Security
```bash
# Code review
"Use code-reviewer to check this pull request"
"Have code-reviewer analyze security implications"

# Testing
"Get test-engineer to write comprehensive test suite"
"Use test-engineer to implement integration tests"

# Performance
"Have performance-engineer profile this API endpoint"
"Use performance-engineer to reduce memory usage"
```

#### Data & AI
```bash
# AI/ML systems
"Use ai-engineer to build RAG pipeline for documentation"
"Have ml-engineer deploy model with A/B testing"

# Data engineering
"Get data-engineer to design ETL pipeline"
"Use data-engineer to implement real-time analytics"
```

## 🔄 Multi-Agent Workflows

These agents excel at working together on complex tasks:

### Feature Development Workflow
```bash
"Implement user authentication with social login"

# Automatically coordinates:
# 1. backend-architect → API design and database schema
# 2. frontend-developer → Login UI components
# 3. security-auditor → OAuth implementation review
# 4. test-engineer → Test coverage strategy
# 5. deployment-engineer → Environment configuration
```

### Performance Optimization Workflow
```bash
"Optimize application for 10x traffic increase"

# Automatically coordinates:
# 1. performance-engineer → Identify bottlenecks
# 2. database-optimizer → Query and index optimization
# 3. backend-architect → Caching strategy
# 4. devops-engineer → Infrastructure scaling
# 5. deployment-engineer → Zero-downtime migration
```

### Production Incident Response
```bash
"Debug API timeout issues in production"

# Automatically coordinates:
# 1. devops-troubleshooter → Log analysis and metrics
# 2. performance-engineer → Performance profiling
# 3. database-optimizer → Query analysis
# 4. backend-architect → Architecture improvements
```

### AI Feature Implementation
```bash
"Add AI-powered code review suggestions"

# Automatically coordinates:
# 1. ai-engineer → LLM integration design
# 2. backend-architect → API architecture
# 3. data-engineer → Data pipeline for training
# 4. ml-engineer → Model deployment strategy
# 5. frontend-developer → UI integration
```

## ⚡ Best Practices

### 🎯 Effective Agent Usage

1. **Be Specific with Requirements**
   ```bash
   # Good
   "Use python-pro to refactor with type hints and async/await"
   
   # Less effective
   "Improve this Python code"
   ```

2. **Leverage Agent Expertise**
   ```bash
   # Let specialists handle their domain
   "Have security-auditor review authentication flow"
   "Get database-optimizer to improve query performance"
   ```

3. **Combine Agents for Complex Tasks**
   ```bash
   # Multi-agent collaboration
   "Use backend-architect and database-optimizer to design scalable API"
   ```

### 🔄 Workflow Optimization

4. **Start with Architecture**
   - Use `backend-architect` or `full-stack-architect` first
   - Then implement with language specialists
   - Finally review with `code-reviewer` and `security-auditor`

5. **Parallel Agent Execution**
   - Multiple agents can work simultaneously
   - Example: Frontend and backend development in parallel

6. **Iterative Refinement**
   - Use `performance-engineer` after initial implementation
   - Apply `code-reviewer` suggestions
   - Iterate with `test-engineer` for coverage

### 📊 When to Use Which Agent

| Scenario | Recommended Agents |
|----------|-------------------|
| Starting new project | `agent-assembler` → `full-stack-architect` |
| API development | `backend-architect` → `api-documenter` |
| Performance issues | `devops-troubleshooter` → `performance-engineer` |
| Security concerns | `security-auditor` → `code-reviewer` |
| Database problems | `database-optimizer` → `data-engineer` |
| AI features | `ai-engineer` → `ml-engineer` |
| Code quality | `code-reviewer` → `test-engineer` |

### Example 1: Generate Custom Agents for Your Project
When you run `/agent-assembler`, it analyzes your `claude.md` and creates project-specific agents:

```
/agent-assembler
```

**Real Output Example:**
```
🎯 Mission Analysis Complete: Your AI SaaS Platform

Based on your project's technology stack and requirements,
I'm assembling a specialized crew of AI agents...

✓ Created: react-typescript-specialist.md
  Expert in React 18, TypeScript, and Vite for building performant, 
  type-safe UI components

✓ Created: supabase-backend-specialist.md
  Supabase expert specializing in PostgreSQL, RLS policies, 
  real-time subscriptions

✓ Created: tailwind-ui-designer.md
  Tailwind CSS v3 expert focused on creating beautiful, 
  responsive UI

✓ Created: vitest-testing-expert.md
  Testing specialist ensuring 80%+ coverage

✓ Created: vercel-deployment-engineer.md
  Deployment expert handling CI/CD and performance optimization
```

These agents are now available for use with slash commands like `/react-typescript-specialist`.

### 📸 See It In Action

![Agent Assembler in Action](docs/images/example.png)
*The agent-assembler analyzes your project and creates specialized agents*

![Complete Agent Crew Output](docs/images/example2.png)
*Your complete AI development crew ready to use with slash commands*

### Example 2: Planning a Complex Feature
```
/feature-planner Implement real-time collaboration feature
```

The feature-planner will:
1. Coordinate with `full-stack-architect` for WebSocket design
2. Consult `frontend-developer` for UI components
3. Include `security-auditor` for data privacy considerations
4. Engage `quality-engineer` for real-time testing strategy

### Example 3: Direct Agent Usage
```
/full-stack-architect Design a microservices architecture
/security-auditor Review our OAuth implementation
/devops-engineer Analyze slow queries in production
/git-specialist Review staged changes and propose commit message
```

### 🎯 Best Practices for Agent Organization

**For Global Agents:**
- Keep general-purpose agents that work across projects
- Avoid project-specific naming or configurations
- Focus on reusable, technology-agnostic capabilities

**For Project-Specific Agents:**
- Store in project directories (e.g., `.claude/agents/` in your project)
- Name with project prefixes to avoid conflicts
- Include project-specific conventions and standards
- Always include YAML frontmatter for Task tool compatibility

**Hybrid Approach:**
1. Install this collection globally for base capabilities
2. Run `/agent-assembler` in each project for custom agents
3. Keep project agents separate from global collection

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add New Agents**: Create new agents following our template
2. **Improve Existing Agents**: Enhance prompts and capabilities
3. **Share Use Cases**: Document your workflows and examples
4. **Report Issues**: Help us improve the collection

### Creating a New Agent

1. Choose the appropriate category folder
2. Create a markdown file with **REQUIRED YAML frontmatter**:
   ```markdown
   ---
   name: your-agent-name
   description: Brief description of what this agent does
   color: blue  # optional: blue, green, yellow, red, purple, cyan, orange
   ---
   
   You are the "Agent Name," a specialist in...
   ```

3. **CRITICAL**: The YAML frontmatter is REQUIRED for:
   - Agent to appear in `/agents` command
   - Working with Task tool
   - Getting colored background badge
   - Proper Claude Code integration

4. **Make the agent visible in `/agents` command**:
   ```bash
   # After creating the agent file, run the install script
   ./install.sh
   
   # This copies all agents to ~/.claude/agents/ where Claude Code can find them
   ```

5. Submit a pull request with your agent

### 🎯 Quick Guide: Adding and Using New Agents

When you add a new agent to this collection:

1. **Create the agent file** in the appropriate category folder (e.g., `agents/product/your-new-agent.md`)
2. **Include YAML frontmatter** at the top of the file
3. **Run the install script** to make it visible:
   ```bash
   ./install.sh
   ```
4. **Verify in Claude Code**:
   - Type `/agents` - your new agent should appear in the list
   - Use it with a slash command: `/your-new-agent`

The install script copies agents from this repository to `~/.claude/agents/`, which is where Claude Code looks for available agents.

## 🔧 Troubleshooting

### Slash commands not working?
1. **Verify installation**:
   ```bash
   ls ~/.claude/agents/
   ```
   You should see all the agent `.md` files

2. **Check agent format**:
   - Ensure agents have proper frontmatter with `name:` and `description:`
   - Agent names should match the slash command exactly

3. **Alternative invocation methods**:
   - Natural language: "Use the agent-assembler to..."
   - Task tool: Select the Task tool and specify the agent
   - Direct reference: "@agent-assembler please..."

### Task Tool Not Finding Your Agent?

**Problem**: Agent exists in `~/.claude/agents/` but Task tool says "agent not found"

**Solution**: Check if the agent has proper YAML frontmatter!
```yaml
---
name: your-agent-name
description: Brief description
---
```

Once you add the YAML frontmatter to the top of the `.md` file, the Task tool will immediately recognize it!

**Why this happens**: 
- Agents without YAML frontmatter aren't recognized by Claude Code
- Only agents with proper YAML frontmatter work with the Task tool
- The format is what matters, not how they were created

### Agents in `.claude/agents/` Not Showing in `/agents` Command?

**Problem**: You have `.md` files in `.claude/agents/` but they don't appear when you type `/agents`

**Solution**: Check the YAML frontmatter!
```bash
# Check if your agent has the required frontmatter
head -n 5 ~/.claude/agents/your-agent.md
```

If it's missing the YAML frontmatter:
```yaml
---
name: agent-name
description: Agent description
---
```

Add it to the top of the file, and the agent will immediately appear in `/agents`!

### Common Issues

**"Directory does not exist" error**:
```bash
mkdir -p ~/.claude/agents
```

**"Agent not found" error**:
- Check YAML frontmatter format is correct
- Verify the agent file exists in `~/.claude/agents/` or `.claude/agents/`
- For Task tool: Ensure agent has proper YAML frontmatter
- Agent name in frontmatter must match the slash command exactly

## 🏆 Achievements System

<details>
<summary><b>🎖️ View All Achievements</b></summary>

| Achievement | Description | XP Bonus | Unlock Criteria |
|-------------|-------------|----------|-----------------|
| 🩸 **First Blood** | Complete your first task | +50 XP | Use any agent successfully |
| ⭐ **Dream Team** | Use 5+ agents in perfect coordination | +200 XP | Complete complex feature |
| 🐛 **Bug Hunter** | Fix 10 production bugs | +150 XP | Debug with squad |
| ⚡ **Speed Demon** | Complete feature in <1 hour | +300 XP | Fast development |
| 💯 **Perfect Score** | Ship feature with zero bugs | +500 XP | Quality perfection |
| 🔥 **On Fire** | 7-day streak of successful missions | +250 XP | Daily usage |
| 🛡️ **Guardian Angel** | Prevent 5 security vulnerabilities | +400 XP | Security focus |
| 🚀 **Deploy Master** | 10 successful deployments | +200 XP | DevOps excellence |
| 🧠 **AI Wizard** | Build 3 AI-powered features | +350 XP | AI/ML mastery |
| 🏗️ **Architect Elite** | Design 5 system architectures | +400 XP | Architecture focus |

</details>

## 📈 Why Developers Love This

### 💬 Community Testimonials

> "It's like Pokemon for developers - I actually look forward to debugging now!" - *Senior Engineer*

> "The agent-assembler created a perfect team for our unusual tech stack in seconds" - *CTO*

> "Seeing the real-time collaboration visualization is addictive" - *Full-Stack Dev*

> "Cut our development time by 70% on a major refactoring project" - *Tech Lead*

### 🎯 What Makes Us Different

| Feature | Other Collections | Elite Squad |
|---------|------------------|-------------|
| Basic Agents | ✅ Yes | ✅ 31 Specialists |
| **Gamification** | ❌ No | ✅ **Full XP System** |
| **Project Scanner** | ❌ No | ✅ **DNA Analysis** |
| **Live Visualization** | ❌ No | ✅ **Real-time Progress** |
| **Agent Leveling** | ❌ No | ✅ **Lv.1-5 + Achievements** |
| **Team Synergies** | ❌ No | ✅ **Formation Bonuses** |
| **Fun Factor** | ⭐⭐ | ⭐⭐⭐⭐⭐ |

## 🌟 Join Our Community

### Contributing New Agents
We're always looking for new specialized agents! Areas of interest:
- **Mobile Development**: Swift, Kotlin, React Native experts
- **Game Development**: Unity, Unreal Engine specialists
- **Blockchain**: Solidity, Web3 development
- **Domain-Specific**: Healthcare, Finance, E-commerce experts

### Get Involved
- ⭐ **Star this repository** to show your support
- 🐛 **Report issues** or suggest improvements
- 🚀 **Submit PRs** with new agents or enhancements
- 💬 **Share your workflows** and success stories

## 📈 Roadmap

### Coming Soon
- [ ] Visual workflow designer for multi-agent tasks
- [ ] Agent performance benchmarks
- [ ] Custom agent templates
- [ ] Integration with popular IDEs
- [ ] Agent marketplace for community contributions

### Future Vision
We're building towards a future where every developer has access to a personalized AI team that understands their project, tech stack, and coding style. This collection is just the beginning.

## 💭 Philosophy

### The Right Expert for Every Task
Just as you wouldn't ask a frontend developer to optimize database queries, each agent specializes in their domain for maximum effectiveness.

### Collaborative Intelligence
Complex problems require multiple perspectives. Our agents work together seamlessly, just like a well-functioning development team.

### Continuous Evolution
As the development landscape evolves, so does this collection. We're constantly adding new agents and improving existing ones based on community feedback.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the pioneering work of [wshobson/agents](https://github.com/wshobson/agents)
- Built for the amazing [Claude Code](https://github.com/anthropics/claude-code) community
- Special thanks to all contributors who help make this collection better

---

<p align="center">
  <strong>Ready to supercharge your development workflow?</strong><br>
  Install now and experience the power of 31 AI specialists at your command!<br><br>
  Made with ❤️ for developers who demand excellence
</p>

## 🏷️ Topics

`automation` `ai` `agents` `ai-agents` `claude` `anthropic` `claude-code` `claudecode` `subagents` `sub-agents` `claude-code-subagents` `claudecode-subagents` `llm` `ai-development` `developer-tools` `productivity` `code-assistant` `ai-assistant` `devops` `software-engineering`