# Contributing to Claude Code Agent Collection

Thank you for your interest in contributing to the Claude Code Agent Collection! This guide will help you get started.

## 🤝 Ways to Contribute

### 1. Add New Agents
Create specialized agents for new domains or technologies:
- Choose the appropriate category folder under `agents/`
- Follow the agent template format
- Include clear descriptions and use cases

### 2. Improve Existing Agents
Enhance current agents with:
- Better prompts and instructions
- Additional capabilities
- Bug fixes and improvements
- More comprehensive examples

### 3. Documentation
Help others understand and use the agents:
- Write tutorials and guides
- Document use cases and workflows
- Improve setup instructions
- Add examples and best practices

### 4. Testing and Feedback
- Test agents in real projects
- Report issues and bugs
- Suggest improvements
- Share success stories

## 📝 Agent Template

When creating a new agent, use this template:

```markdown
---
name: agent-name
description: Brief description of what this agent does and when to use it
---

You are the "[Agent Name]," a [role description] on this AI crew. [Expanded description of expertise and purpose].

## My Core Competencies

- **Competency 1:** Description of this skill area
- **Competency 2:** Description of this skill area
- **Competency 3:** Description of this skill area

## My Approach

1. **Step 1:** What I do first
2. **Step 2:** How I proceed
3. **Step 3:** How I validate results

## My Deliverables

- **Deliverable 1:** What I produce
- **Deliverable 2:** Additional outputs
- **Deliverable 3:** Documentation or reports
```

## 🚀 Submission Process

1. **Fork the Repository**
   ```bash
   git clone https://github.com/mylee04/claude-code-agents.git
   cd claude-code-agents
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b add-agent-name
   ```

3. **Add Your Agent**
   - Place in appropriate category folder
   - Follow naming convention: `agent-name.md`
   - Ensure proper frontmatter format

4. **Test Your Agent**
   - Copy to `~/.claude/agents/`
   - Test with Claude Code
   - Verify it works as expected

5. **Submit Pull Request**
   - Clear description of the agent
   - Example use cases
   - Any special requirements

## 📋 Guidelines

### Do's
- ✅ Follow existing patterns and conventions
- ✅ Write clear, concise agent descriptions
- ✅ Include practical examples
- ✅ Test thoroughly before submitting
- ✅ Keep agents focused on specific tasks

### Don'ts
- ❌ Create overly broad agents
- ❌ Duplicate existing functionality
- ❌ Include sensitive information
- ❌ Use unclear or ambiguous language
- ❌ Submit untested agents

## 🏷️ Categories

Place agents in the appropriate folder:
- `conductor/` - Agents that coordinate other agents
- `development/` - Core development tasks
- `quality/` - Testing and code quality
- `security/` - Security analysis and auditing
- `infrastructure/` - DevOps and deployment
- `programming/` - Language-specific experts
- `data/` - Data science and analytics
- `product/` - Product and business logic

## 💬 Questions?

- Open an issue for discussion
- Check existing issues first
- Be respectful and constructive
- Help others in the community

Thank you for helping make Claude Code Agent Collection better! 🎉