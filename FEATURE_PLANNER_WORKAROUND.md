# Feature Planner Workaround Guide

> **TL;DR**: While we work on fixing the feature-planner's coordination with custom agents, here are practical workarounds to get your complex features planned and implemented today.

## Current Limitation

The `feature-planner` agent is designed to orchestrate multiple specialist agents for complex feature development. However, there's currently a limitation where the feature-planner may not properly coordinate with custom agents created by the `agent-assembler`.

**What's Affected:**
- Custom agents generated for your specific tech stack
- Multi-agent workflows involving project-specific specialists
- Automatic agent coordination in complex feature planning

**What Still Works:**
- All 31 built-in specialist agents work perfectly with feature-planner
- Manual coordination between any agents
- Single-agent tasks with custom agents
- The gamification system (XP tracking, levels, achievements)

## Practical Workarounds

### Option 1: Manual Multi-Agent Coordination (Recommended)

Instead of relying on feature-planner to automatically coordinate agents, manually orchestrate them in sequence:

```bash
# Step 1: Break down the feature yourself
"I need to implement user authentication with social login. Let me break this into parts:
1. Backend API design
2. Frontend components  
3. Database schema
4. Security considerations
5. Testing strategy"

# Step 2: Coordinate agents manually
/backend-architect "Design RESTful API for user authentication with OAuth social login (Google, GitHub, Twitter). Include endpoints for registration, login, token refresh, and user profile management."

# Step 3: Use the output to inform the next agent
/frontend-developer "Based on this API design: [paste API design], create React components for social login UI including login buttons, user profile display, and authentication state management."

# Step 4: Continue the chain
/security-auditor "Review this authentication flow for security vulnerabilities: [paste both API and frontend designs]"

# Step 5: Finalize with testing
/test-engineer "Create comprehensive test suite for this authentication system: [paste all previous outputs]"
```

### Option 2: Use Built-in Agents with Feature Planner

If your feature can be implemented using the 31 built-in agents, the feature-planner works perfectly:

```bash
/feature-planner "Implement a real-time dashboard showing system metrics with user authentication"
```

**Built-in agents that work flawlessly:**
- **Development**: python-pro, javascript-pro, golang-pro, rust-pro, sql-pro, backend-architect, frontend-developer, full-stack-architect
- **Infrastructure**: devops-engineer, cloud-architect, database-optimizer, deployment-engineer
- **Quality**: code-reviewer, test-engineer, performance-engineer, security-auditor
- **Data**: data-engineer, ai-engineer, ml-engineer

### Option 3: Hybrid Approach

Combine feature-planner for initial structure, then use custom agents for implementation:

```bash
# Step 1: Get the overall plan from feature-planner
/feature-planner "Create a user dashboard with real-time data visualization"

# Step 2: Use custom agents for specific implementation
/nextjs-app-router-specialist "Implement the dashboard using the plan above, but follow our Next.js 14 app router patterns"

/supabase-backend-specialist "Set up the real-time data pipeline using our Supabase setup from the feature plan"
```

### Option 4: Create Comprehensive Prompts

Write detailed prompts that simulate multi-agent coordination:

```bash
"Act as a tech lead coordinating multiple specialists. I need to implement [feature description]. 

Please provide:
1. Backend architecture (as backend-architect would)
2. Frontend component structure (as frontend-developer would)  
3. Database schema changes (as database-optimizer would)
4. Security considerations (as security-auditor would)
5. Testing strategy (as test-engineer would)
6. Deployment plan (as devops-engineer would)

Format each section clearly and ensure they work together cohesively."
```

## Effective Prompt Patterns

### Pattern 1: Sequential Agent Chain
```bash
# Template:
/[agent-1] "[task] and provide output that [agent-2] can use"
# Then use agent-1's output to inform agent-2
/[agent-2] "Based on this [context from agent-1]: [paste output], do [specific task]"
```

### Pattern 2: Context-Rich Single Prompts
```bash
# Template:
"I'm working on [project context]. My tech stack is [technologies]. 
I need to [specific task]. 
Please consider [constraint 1], [constraint 2], and integrate with [existing system]."
```

### Pattern 3: Iterative Refinement
```bash
# Round 1: Get initial design
/backend-architect "Design API for user management system"

# Round 2: Refine with constraints  
/backend-architect "Refine the previous API design to work with our PostgreSQL database and include rate limiting"

# Round 3: Add specific requirements
/backend-architect "Add bulk user operations and audit logging to the refined API design"
```

## Manual Coordination Best Practices

### 1. Start with Architecture
Always begin with high-level design before diving into implementation:
```bash
/full-stack-architect "Design overall system architecture for [feature]"
```

### 2. Define Contracts Early
Establish API contracts and data structures before parallel development:
```bash
/backend-architect "Define API endpoints and request/response formats"
# Share this with frontend developers
```

### 3. Consider Dependencies
Plan your agent sequence to respect dependencies:
```bash
# Correct order:
1. Database schema → 2. Backend API → 3. Frontend components → 4. Tests

# Wrong order (creates confusion):
1. Frontend components → 2. Database schema → 3. Backend API
```

### 4. Maintain Context
Keep important context available for each agent:
```bash
# Good:
/test-engineer "Create tests for this authentication system [paste full context including API design, database schema, security requirements]"

# Less effective:
/test-engineer "Create tests for authentication"
```

### 5. Review and Integrate
Use code-reviewer to ensure consistency across agent outputs:
```bash
/code-reviewer "Review these designs from multiple agents and identify any inconsistencies or integration issues: [paste all outputs]"
```

## When to Use Each Approach

| Scenario | Recommended Approach | Why |
|----------|---------------------|-----|
| **Standard tech stack** (React, Node.js, PostgreSQL) | Feature-planner with built-in agents | Fully supported, automatic coordination |
| **Custom tech stack** (Next.js 14, Supabase, custom tools) | Manual coordination with custom agents | Best output quality for your specific setup |
| **Simple features** (< 3 components) | Single specialized agent | Fastest for straightforward tasks |
| **Complex features** (> 5 components) | Hybrid approach | Balance of automation and customization |
| **Learning/exploration** | Comprehensive single prompts | Good for understanding architectural decisions |

## Quick Reference Commands

### Check Available Agents
```bash
ls ~/.claude/agents/  # List all agents
./squad              # Check agent levels and XP
```

### Most Useful Agent Combinations
```bash
# Full-Stack Feature
/full-stack-architect → /backend-architect → /frontend-developer → /test-engineer

# Performance Feature  
/performance-engineer → /database-optimizer → /cloud-architect → /devops-engineer

# Security Feature
/security-auditor → /backend-architect → /devops-engineer → /test-engineer

# Data Feature
/data-engineer → /backend-architect → /ai-engineer → /test-engineer
```

### Emergency Debugging Chain
```bash
/devops-troubleshooter → /performance-engineer → /database-optimizer → /incident-commander
```

## Expected Timeline for Fix

The development team is actively working on improving feature-planner's coordination with custom agents. Expected improvements:

- **Short-term** (1-2 weeks): Better error messages when coordination fails
- **Medium-term** (3-4 weeks): Automatic detection and inclusion of custom agents  
- **Long-term** (6-8 weeks): Full integration with dynamic agent discovery

## Need Help?

If you're stuck with a specific workflow:

1. **Check the examples** above for similar patterns
2. **Use the hybrid approach** - it works for 90% of cases
3. **Share your specific use case** in the project issues for tailored advice

## Pro Tips

### Maximize XP While Using Workarounds
```bash
./squad log feature-planning "Manually coordinated 4-agent workflow for user dashboard"
# Earn XP for coordination work even when doing it manually
```

### Save Successful Patterns
Keep a note of agent sequences that work well for your project:
```bash
# Create a personal reference
echo "/backend-architect → /frontend-developer → /security-auditor" > my-auth-workflow.txt
```

### Use Agent Specializations
Remember that agents are more effective when you play to their strengths:
```bash
# Instead of:
/python-pro "Design the entire system"

# Do this:
/backend-architect "Design the system" 
/python-pro "Implement the Python components from this design"
```

---

**Remember**: These workarounds are temporary solutions. The core functionality remains powerful, and manual coordination often produces even better results because you maintain full control over the process.

The Elite Squad is still your most effective development team - you're just acting as the project manager until the feature-planner coordination is fully automated.