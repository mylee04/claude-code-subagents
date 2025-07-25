# 🤖 Claude Code Agent Collection

> A comprehensive collection of AI agents for Claude Code that work together as your personalized development team

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Agent%20Collection-blue)](https://github.com/anthropics/claude-code)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Agents](https://img.shields.io/badge/agents-17-orange)](agents/)

## 🚀 Overview

The Claude Code Agent Collection is a curated set of specialized AI agents designed to enhance your development workflow. Unlike traditional static tools, this collection features a dynamic system that assembles a custom AI development team tailored to your specific project needs.

### ✨ Key Features

- **🎯 Dynamic Team Assembly**: The `agent-assembler` reads your project's `claude.md` file and automatically builds a custom crew
- **🤝 Collaborative Agents**: "Lead" agents coordinate multiple specialists to handle complex tasks
- **📁 Organized by Domain**: Agents are categorized for easy discovery and use
- **🔧 Extensible**: Easy to add new agents or customize existing ones

## 📚 Table of Contents

- [Getting Started](#-getting-started)
- [Agent Categories](#-agent-categories)
- [How It Works](#-how-it-works)
- [Usage Examples](#-usage-examples)
- [Contributing](#-contributing)
- [Philosophy](#-philosophy)

## 🏁 Getting Started

### Prerequisites

- [Claude Code](https://github.com/anthropics/claude-code) installed and configured
- A project with a `claude.md` file describing your tech stack and goals

### Quick Start

1. **Clone this repository**:
   ```bash
   git clone https://github.com/mylee04/claude-code-agents.git
   cd claude-code-agents
   ```

2. **Copy agents to your Claude Code directory**:
   ```bash
   cp -r agents/* ~/.claude/agents/
   ```

3. **In your project, create a `claude.md` file**:
   ```markdown
   # Project: My Awesome App
   
   ## Tech Stack
   - Frontend: React, TypeScript, Tailwind CSS
   - Backend: Node.js, Express, PostgreSQL
   - Infrastructure: AWS, Docker
   
   ## Goals
   - Build a scalable SaaS platform
   - Maintain high code quality and test coverage
   ```

4. **Invoke the agent-assembler**:
   ```
   Use the agent-assembler to build a crew for this project
   ```

## 📋 Agent Categories

### 🧠 Conductor & Workflow Leads
Agents that coordinate other agents and manage complex workflows.

| Agent | Description |
|-------|-------------|
| [`agent-assembler`](agents/conductor/agent-assembler.md) | Analyzes your project and builds a custom agent crew |
| [`feature-planner`](agents/conductor/feature-planner.md) | Tech lead that creates comprehensive technical plans |

### 💻 Development & Architecture
Core development agents for building features.

| Agent | Description |
|-------|-------------|
| [`backend-architect`](agents/development/backend-architect.md) | Designs APIs, services, and database schemas |
| [`frontend-developer`](agents/development/frontend-developer.md) | Builds modern UI components and manages state |

### ✅ Quality Assurance
Agents focused on code quality and testing.

| Agent | Description |
|-------|-------------|
| [`code-reviewer`](agents/quality/code-reviewer.md) | Reviews code for quality and best practices |
| [`test-engineer`](agents/quality/test-engineer.md) | Writes comprehensive automated tests |

### 🔒 Security
Security-focused agents for vulnerability detection and compliance.

| Agent | Description |
|-------|-------------|
| [`security-auditor`](agents/security/security-auditor.md) | Scans for vulnerabilities and security issues |

### 🏗️ Infrastructure & Operations
DevOps and infrastructure management agents.

| Agent | Description |
|-------|-------------|
| [`cloud-architect`](agents/infrastructure/cloud-architect.md) | Designs cloud infrastructure on AWS, GCP, or Azure |
| [`deployment-engineer`](agents/infrastructure/deployment-engineer.md) | Manages CI/CD pipelines and containerization |
| [`database-optimizer`](agents/infrastructure/database-optimizer.md) | Optimizes database performance and queries |
| [`devops-troubleshooter`](agents/infrastructure/devops-troubleshooter.md) | Debugs production issues using logs and metrics |


### 📊 Data & AI
Agents for data science and AI/ML tasks.

| Agent | Description |
|-------|-------------|
| [`data-engineer`](agents/data/data-engineer.md) | Builds data pipelines and ETL processes |
| [`ai-engineer`](agents/data/ai-engineer.md) | Implements AI systems and LLM integrations |
| [`ml-engineer`](agents/data/ml-engineer.md) | Deploys and manages ML models in production |

### 🎯 Product & Specialized
Agents focused on product development and specialized tasks.

| Agent | Description |
|-------|-------------|
| [`user-feedback-analyst`](agents/product/user-feedback-analyst.md) | Analyzes user feedback to extract insights |
| [`dx-optimizer`](agents/product/dx-optimizer.md) | Improves developer experience and workflows |
| [`api-documenter`](agents/product/api-documenter.md) | Creates comprehensive API documentation |

## 🔧 How It Works

### 1. Project Analysis
The `agent-assembler` reads your `claude.md` file to understand:
- Your technology stack
- Project architecture
- Development conventions
- Team goals and priorities

### 2. Custom Crew Assembly
Based on the analysis, it:
- Selects relevant agents from the collection
- Creates new specialized agents if needed
- Configures agents with project-specific context

### 3. Collaborative Execution
Agents work together:
- Lead agents coordinate specialists
- Information flows between agents seamlessly
- Complex tasks are broken down and distributed

## 💡 Usage Examples

### Example 1: Planning a New Feature
```
Use the feature-planner to design a user authentication system
```

The feature-planner will:
1. Coordinate with `backend-architect` for API design
2. Consult `frontend-developer` for UI components
3. Include `security-auditor` for security considerations
4. Engage `test-engineer` for testing strategy

### Example 2: Code Review Workflow
```
Use the code-reviewer to review the changes in my pull request
```

### Example 3: Security Audit
```
Use the security-auditor to scan the codebase for vulnerabilities
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Add New Agents**: Create new agents following our template
2. **Improve Existing Agents**: Enhance prompts and capabilities
3. **Share Use Cases**: Document your workflows and examples
4. **Report Issues**: Help us improve the collection

### Creating a New Agent

1. Choose the appropriate category folder
2. Create a markdown file with frontmatter:
   ```markdown
   ---
   name: your-agent-name
   description: Brief description of what this agent does
   ---
   
   You are the "Agent Name," a specialist in...
   ```

3. Submit a pull request with your agent

## 💭 Philosophy

### The Right Tool for the Job
We believe every project deserves a custom-tailored AI team. Generic solutions lead to generic results.

### Collaborative Intelligence
Complex problems require multiple perspectives. Our agents work together, just like a real development team.

### Continuous Evolution
As Claude Code evolves, so does this collection. We're constantly adding new agents and improving existing ones.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the [wshobson/agents](https://github.com/wshobson/agents) collection
- Built for the amazing [Claude Code](https://github.com/anthropics/claude-code) community
- Special thanks to all contributors

---

<p align="center">
  Made with ❤️ for the Claude Code community
</p>