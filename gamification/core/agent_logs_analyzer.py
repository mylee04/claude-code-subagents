#!/usr/bin/env python3
"""
Agent-Specific Logs Analyzer for Claude Code Subagents
Parses Claude Code logs to detect agent invocations and calculate XP based on agent usage

Features:
- Advanced agent invocation detection from /agent-name patterns
- Squad formation and collaboration tracking
- XP calculation based on real agent usage patterns
- Agent-specific performance metrics
- Collaboration bonus system
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any, Set
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentInvocation:
    """Enhanced agent invocation with collaboration tracking"""
    agent_name: str
    session_id: str
    timestamp: datetime
    project_path: str
    task_description: str
    tools_used: List[str]
    success: bool
    error_message: Optional[str] = None
    duration_seconds: float = 0.0
    tokens_used: int = 0
    model: str = ""
    git_branch: str = ""
    collaboration_agents: List[str] = None  # Other agents used in same session
    specialization_bonus: int = 0
    collaboration_bonus: int = 0
    complexity_score: float = 0.0

@dataclass
class SquadFormation:
    """Represents a squad of agents working together"""
    session_id: str
    agents: List[str]
    start_time: datetime
    end_time: datetime
    project_path: str
    total_tasks: int
    success_rate: float
    synergy_score: float  # How well agents worked together
    formation_type: str  # e.g., "full-stack", "data-pipeline", "devops"

@dataclass
class AgentXPCalculation:
    """Detailed XP breakdown for an agent"""
    agent_name: str
    base_xp: int
    success_bonus: int
    tool_mastery_bonus: int
    complexity_bonus: int
    collaboration_bonus: int
    specialization_bonus: int
    consistency_bonus: int
    total_xp: int
    level: int
    next_level_xp: int

class AgentLogsAnalyzer:
    """
    Advanced Claude Code log analyzer focused on agent-specific analytics
    
    This analyzer goes beyond basic log parsing to provide:
    - Agent invocation pattern recognition
    - Squad formation detection
    - Collaboration analysis
    - Performance-based XP calculation
    """
    
    def __init__(self, log_directory: str = None):
        """
        Initialize the analyzer
        
        Args:
            log_directory: Path to Claude Code logs (defaults to ~/.claude/projects/)
        """
        if log_directory is None:
            log_directory = Path.home() / ".claude" / "projects"
        
        self.log_directory = Path(log_directory)
        
        # Enhanced agent patterns - looking for specific invocation patterns
        self.agent_patterns = {
            # Direct agent calls - /agent-name format
            "direct_call": r'/(?:agents?/)?([a-zA-Z0-9\-_]+(?:\-(?:pro|elite|engineer|architect|specialist|analyst|developer|commander|optimizer|auditor))?)',
            
            # Agent mentions in context
            "context_mention": r'\b(?:using|with|invoke|call|run)\s+([a-zA-Z0-9\-_]+(?:\-(?:pro|elite|engineer|architect|specialist|analyst|developer|commander|optimizer|auditor)))\b',
            
            # Squad formations - multiple agents mentioned together
            "squad_mention": r'\b(?:squad|team|collaboration|together)\b.*?([a-zA-Z0-9\-_]+(?:\-(?:pro|elite|engineer|architect|specialist|analyst|developer|commander|optimizer|auditor)))',
        }
        
        # Agent specialization categories for bonus calculation
        self.specialization_categories = {
            "python": ["python-elite", "python-pro", "data-engineer", "ai-engineer", "ml-engineer"],
            "javascript": ["javascript-pro", "frontend-developer", "full-stack-architect"],
            "backend": ["backend-architect", "golang-pro", "rust-pro", "sql-pro"],
            "infrastructure": ["devops-engineer", "cloud-architect", "deployment-engineer", "incident-commander"],
            "quality": ["test-engineer", "code-reviewer", "performance-engineer", "quality-engineer"],
            "security": ["security-auditor"],
            "data": ["data-engineer", "data-ai-ml-engineer", "ml-engineer", "ai-engineer"],
            "business": ["business-analyst", "content-marketer", "user-feedback-analyst"],
            "product": ["api-documenter", "dx-optimizer", "tech-portfolio-resume-review-specialist"]
        }
        
        # Squad formation patterns - identify collaborative workflows
        self.squad_formations = {
            "full-stack": ["frontend-developer", "backend-architect", "database-optimizer"],
            "data-pipeline": ["data-engineer", "ai-engineer", "devops-engineer"],
            "security-audit": ["security-auditor", "code-reviewer", "devops-engineer"],
            "performance-optimization": ["performance-engineer", "database-optimizer", "cloud-architect"],
            "feature-development": ["frontend-developer", "backend-architect", "test-engineer"],
            "ml-deployment": ["ml-engineer", "devops-engineer", "cloud-architect"],
            "incident-response": ["incident-commander", "devops-troubleshooter", "security-auditor"]
        }
        
        # XP level thresholds
        self.xp_levels = [
            (0, 1), (100, 2), (300, 3), (600, 4), (1000, 5),
            (1500, 6), (2500, 7), (4000, 8), (6000, 9), (10000, 10)
        ]

    def detect_agent_invocations(self, text: str) -> List[str]:
        """
        Advanced agent detection from text content
        Looks for direct calls, context mentions, and collaboration patterns
        """
        agents_found = set()
        text_lower = text.lower()
        
        # Direct agent calls (/agent-name format)
        direct_matches = re.findall(self.agent_patterns["direct_call"], text_lower, re.IGNORECASE)
        for match in direct_matches:
            if self._is_valid_agent_name(match):
                agents_found.add(match)
        
        # Context mentions
        context_matches = re.findall(self.agent_patterns["context_mention"], text_lower, re.IGNORECASE)
        for match in context_matches:
            if self._is_valid_agent_name(match):
                agents_found.add(match)
        
        # Squad mentions
        squad_matches = re.findall(self.agent_patterns["squad_mention"], text_lower, re.IGNORECASE)
        for match in squad_matches:
            if self._is_valid_agent_name(match):
                agents_found.add(match)
        
        return list(agents_found)
    
    def _is_valid_agent_name(self, name: str) -> bool:
        """Check if detected name is a valid agent"""
        # Basic validation - should contain relevant keywords
        agent_keywords = [
            "pro", "elite", "engineer", "architect", "specialist", 
            "analyst", "developer", "commander", "optimizer", "auditor",
            "python", "javascript", "golang", "rust", "frontend", "backend",
            "data", "ml", "ai", "devops", "cloud", "security", "test"
        ]
        
        name_parts = name.split('-')
        return any(keyword in name_parts for keyword in agent_keywords)
    
    def parse_conversation_logs(self, days_back: int = 30) -> List[AgentInvocation]:
        """
        Parse conversation logs to extract agent invocations
        
        Args:
            days_back: Only analyze logs from the last N days
            
        Returns:
            List of enhanced AgentInvocation objects
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        all_invocations = []
        
        log_files = self._get_log_files(cutoff_date)
        
        for log_file in log_files:
            logger.info(f"Analyzing {log_file.name}...")
            
            entries = self._parse_jsonl_file(log_file)
            if not entries:
                continue
            
            project_path = self._extract_project_path(log_file)
            invocations = self._extract_agent_invocations_from_entries(entries, project_path)
            
            all_invocations.extend(invocations)
            logger.info(f"  Found {len(invocations)} agent invocations")
        
        # Post-process to add collaboration context
        all_invocations = self._add_collaboration_context(all_invocations)
        
        logger.info(f"Total agent invocations found: {len(all_invocations)}")
        return all_invocations
    
    def _get_log_files(self, cutoff_date: datetime) -> List[Path]:
        """Get relevant log files within the date range"""
        log_files = []
        
        if not self.log_directory.exists():
            logger.warning(f"Log directory does not exist: {self.log_directory}")
            return log_files
        
        for project_dir in self.log_directory.iterdir():
            if project_dir.is_dir():
                for log_file in project_dir.glob("*.jsonl"):
                    if log_file.stat().st_mtime >= cutoff_date.timestamp():
                        log_files.append(log_file)
        
        return sorted(log_files)
    
    def _parse_jsonl_file(self, log_file: Path) -> List[Dict[str, Any]]:
        """Parse a JSONL log file"""
        entries = []
        
        try:
            with open(log_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        entry = json.loads(line)
                        entries.append(entry)
                    except json.JSONDecodeError as e:
                        logger.warning(f"JSON decode error in {log_file}:{line_num}: {e}")
        
        except Exception as e:
            logger.error(f"Error reading log file {log_file}: {e}")
        
        return entries
    
    def _extract_project_path(self, log_file_path: Path) -> str:
        """Extract project path from log directory structure"""
        parent_dir = log_file_path.parent.name
        
        if parent_dir.startswith('-') and parent_dir.endswith('-'):
            decoded_path = parent_dir[1:-1].replace('-', '/')
            return f"/{decoded_path}"
        
        return parent_dir
    
    def _extract_agent_invocations_from_entries(self, entries: List[Dict[str, Any]], 
                                              project_path: str) -> List[AgentInvocation]:
        """Extract agent invocations from log entries with enhanced analysis"""
        invocations = []
        
        for i, entry in enumerate(entries):
            if entry.get("type") not in ["user", "assistant"]:
                continue
            
            timestamp_str = entry.get("timestamp", "")
            if not timestamp_str:
                continue
            
            try:
                timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
            except:
                continue
            
            session_id = entry.get("sessionId", "unknown")
            
            # Extract message content
            content = self._extract_message_content(entry)
            if not content:
                continue
            
            # Detect agent mentions
            agents_mentioned = self.detect_agent_invocations(content)
            
            if agents_mentioned:
                # Extract additional context
                tools_used = self._extract_tools_from_entry(entry)
                tokens_used = self._extract_token_usage(entry)
                model = self._extract_model_info(entry)
                
                # Determine success and complexity
                success, error_message = self._determine_task_success(entries, i)
                complexity_score = self._calculate_complexity_score(content, tools_used, tokens_used)
                
                # Create invocations for each agent mentioned
                for agent_name in agents_mentioned:
                    invocation = AgentInvocation(
                        agent_name=agent_name,
                        session_id=session_id,
                        timestamp=timestamp,
                        project_path=project_path,
                        task_description=content[:500],  # Extended task description
                        tools_used=tools_used,
                        success=success,
                        error_message=error_message,
                        tokens_used=tokens_used,
                        model=model,
                        git_branch=entry.get("gitBranch", ""),
                        collaboration_agents=[],  # Will be filled in post-processing
                        complexity_score=complexity_score
                    )
                    invocations.append(invocation)
        
        return invocations
    
    def _extract_message_content(self, entry: Dict[str, Any]) -> str:
        """Extract text content from message entry"""
        message = entry.get("message", {})
        content = ""
        
        if isinstance(message, dict) and "content" in message:
            if isinstance(message["content"], str):
                content = message["content"]
            elif isinstance(message["content"], list):
                for item in message["content"]:
                    if isinstance(item, dict) and item.get("type") == "text":
                        content += item.get("text", "") + " "
        
        return content.strip()
    
    def _extract_tools_from_entry(self, entry: Dict[str, Any]) -> List[str]:
        """Extract tool names from entry"""
        tools = []
        
        if entry.get("type") == "assistant" and "message" in entry:
            content = str(entry["message"].get("content", ""))
            
            tool_patterns = {
                "bash": r'"name":\s*"Bash"',
                "edit": r'"name":\s*"Edit"',
                "read": r'"name":\s*"Read"',
                "write": r'"name":\s*"Write"',
                "grep": r'"name":\s*"Grep"',
                "glob": r'"name":\s*"Glob"',
                "ls": r'"name":\s*"LS"',
                "multiedit": r'"name":\s*"MultiEdit"',
                "webfetch": r'"name":\s*"WebFetch"',
                "websearch": r'"name":\s*"WebSearch"'
            }
            
            for tool_name, pattern in tool_patterns.items():
                if re.search(pattern, content):
                    tools.append(tool_name)
        
        return tools
    
    def _extract_token_usage(self, entry: Dict[str, Any]) -> int:
        """Extract token usage from entry"""
        tokens = 0
        
        if entry.get("type") == "assistant" and "message" in entry:
            usage = entry["message"].get("usage", {})
            tokens = (usage.get("input_tokens", 0) + 
                     usage.get("output_tokens", 0) +
                     usage.get("cache_read_input_tokens", 0))
        
        return tokens
    
    def _extract_model_info(self, entry: Dict[str, Any]) -> str:
        """Extract model information from entry"""
        if entry.get("type") == "assistant" and "message" in entry:
            return entry["message"].get("model", "")
        return ""
    
    def _determine_task_success(self, entries: List[Dict[str, Any]], start_idx: int) -> Tuple[bool, Optional[str]]:
        """Determine if a task was successful based on subsequent entries"""
        success = True
        error_message = None
        
        # Look at next few entries for error indicators
        for i in range(start_idx, min(start_idx + 5, len(entries))):
            entry = entries[i]
            
            # Check for tool use errors
            if "toolUseResult" in entry and entry["toolUseResult"] == "Error":
                success = False
                error_message = str(entry.get("message", {}).get("content", "Tool use error"))
                break
            
            # Check for error messages in content
            content = self._extract_message_content(entry)
            if content and ("error" in content.lower() or "failed" in content.lower()):
                success = False
                error_message = content[:200]
                break
        
        return success, error_message
    
    def _calculate_complexity_score(self, content: str, tools_used: List[str], tokens_used: int) -> float:
        """Calculate task complexity score"""
        score = 0.0
        
        # Base complexity from content length
        score += min(len(content) / 1000, 2.0)
        
        # Tool diversity bonus
        score += len(set(tools_used)) * 0.3
        
        # Token usage indicates complexity
        if tokens_used > 2000:
            score += 2.0
        elif tokens_used > 1000:
            score += 1.0
        elif tokens_used > 500:
            score += 0.5
        
        # Content complexity indicators
        complexity_indicators = [
            "architecture", "design", "refactor", "optimize", "debug",
            "implement", "deploy", "test", "analyze", "review"
        ]
        
        content_lower = content.lower()
        for indicator in complexity_indicators:
            if indicator in content_lower:
                score += 0.2
        
        return min(score, 5.0)  # Cap at 5.0
    
    def _add_collaboration_context(self, invocations: List[AgentInvocation]) -> List[AgentInvocation]:
        """Add collaboration context to invocations"""
        # Group by session
        sessions = {}
        for inv in invocations:
            if inv.session_id not in sessions:
                sessions[inv.session_id] = []
            sessions[inv.session_id].append(inv)
        
        # Update collaboration context
        for session_invocations in sessions.values():
            if len(session_invocations) > 1:
                # Multiple agents in same session - collaboration detected
                agent_names = [inv.agent_name for inv in session_invocations]
                
                for inv in session_invocations:
                    inv.collaboration_agents = [name for name in agent_names if name != inv.agent_name]
        
        return invocations
    
    def detect_squad_formations(self, invocations: List[AgentInvocation]) -> List[SquadFormation]:
        """Detect squad formations from invocations"""
        formations = []
        
        # Group by session and time window
        sessions = {}
        for inv in invocations:
            if inv.session_id not in sessions:
                sessions[inv.session_id] = []
            sessions[inv.session_id].append(inv)
        
        for session_id, session_invocations in sessions.items():
            if len(session_invocations) < 2:
                continue  # Need at least 2 agents for a squad
            
            # Sort by timestamp
            session_invocations.sort(key=lambda x: x.timestamp)
            
            agents = list(set(inv.agent_name for inv in session_invocations))
            if len(agents) < 2:
                continue
            
            # Determine formation type
            formation_type = self._classify_squad_formation(agents)
            
            # Calculate metrics
            start_time = session_invocations[0].timestamp
            end_time = session_invocations[-1].timestamp
            total_tasks = len(session_invocations)
            success_count = sum(1 for inv in session_invocations if inv.success)
            success_rate = success_count / total_tasks if total_tasks > 0 else 0
            synergy_score = self._calculate_synergy_score(agents, session_invocations)
            
            formation = SquadFormation(
                session_id=session_id,
                agents=agents,
                start_time=start_time,
                end_time=end_time,
                project_path=session_invocations[0].project_path,
                total_tasks=total_tasks,
                success_rate=success_rate,
                synergy_score=synergy_score,
                formation_type=formation_type
            )
            
            formations.append(formation)
        
        return formations
    
    def _classify_squad_formation(self, agents: List[str]) -> str:
        """Classify the type of squad formation"""
        agent_set = set(agents)
        
        for formation_name, formation_agents in self.squad_formations.items():
            if len(agent_set.intersection(set(formation_agents))) >= 2:
                return formation_name
        
        # Generic classification based on specializations
        specializations = []
        for agent in agents:
            for spec, spec_agents in self.specialization_categories.items():
                if agent in spec_agents:
                    specializations.append(spec)
        
        if len(set(specializations)) >= 3:
            return "multi-disciplinary"
        elif len(set(specializations)) == 2:
            return f"{'-'.join(sorted(set(specializations)))}"
        else:
            return "specialized"
    
    def _calculate_synergy_score(self, agents: List[str], invocations: List[AgentInvocation]) -> float:
        """Calculate how well agents worked together"""
        if len(agents) < 2:
            return 0.0
        
        # Base synergy from diverse specializations
        specializations = set()
        for agent in agents:
            for spec, spec_agents in self.specialization_categories.items():
                if agent in spec_agents:
                    specializations.add(spec)
        
        specialization_score = len(specializations) / len(agents)
        
        # Success rate bonus
        success_rate = sum(1 for inv in invocations if inv.success) / len(invocations)
        
        # Temporal coordination (agents used close in time)
        timestamps = [inv.timestamp for inv in invocations]
        timestamps.sort()
        time_spans = [(timestamps[i+1] - timestamps[i]).total_seconds() for i in range(len(timestamps)-1)]
        avg_gap = sum(time_spans) / len(time_spans) if time_spans else 0
        
        # Closer in time = better coordination (max 1 hour for full bonus)
        coordination_score = max(0, 1 - (avg_gap / 3600))
        
        return (specialization_score + success_rate + coordination_score) / 3
    
    def calculate_agent_xp(self, invocations: List[AgentInvocation]) -> Dict[str, AgentXPCalculation]:
        """Calculate detailed XP breakdown for each agent"""
        agent_xp = {}
        
        # Group invocations by agent
        agent_invocations = {}
        for inv in invocations:
            if inv.agent_name not in agent_invocations:
                agent_invocations[inv.agent_name] = []
            agent_invocations[inv.agent_name].append(inv)
        
        for agent_name, agent_invs in agent_invocations.items():
            xp_calc = self._calculate_individual_agent_xp(agent_name, agent_invs)
            agent_xp[agent_name] = xp_calc
        
        return agent_xp
    
    def _calculate_individual_agent_xp(self, agent_name: str, invocations: List[AgentInvocation]) -> AgentXPCalculation:
        """Calculate XP for individual agent with detailed breakdown"""
        base_xp = len(invocations) * 20  # Base XP per invocation
        
        # Success bonus
        success_count = sum(1 for inv in invocations if inv.success)
        success_bonus = success_count * 30
        
        # Tool mastery bonus
        unique_tools = set()
        for inv in invocations:
            unique_tools.update(inv.tools_used)
        tool_mastery_bonus = len(unique_tools) * 15
        
        # Complexity bonus
        avg_complexity = sum(inv.complexity_score for inv in invocations) / len(invocations)
        complexity_bonus = int(avg_complexity * 40 * len(invocations))
        
        # Collaboration bonus
        collaboration_count = sum(1 for inv in invocations if inv.collaboration_agents)
        collaboration_bonus = collaboration_count * 25
        
        # Specialization bonus (consistent use in same domain)
        specialization_bonus = self._calculate_specialization_bonus(agent_name, invocations)
        
        # Consistency bonus (regular usage over time)
        consistency_bonus = self._calculate_consistency_bonus(invocations)
        
        total_xp = (base_xp + success_bonus + tool_mastery_bonus + 
                   complexity_bonus + collaboration_bonus + 
                   specialization_bonus + consistency_bonus)
        
        level = self._calculate_level_from_xp(total_xp)
        next_level_xp = self._get_next_level_xp(level)
        
        return AgentXPCalculation(
            agent_name=agent_name,
            base_xp=base_xp,
            success_bonus=success_bonus,
            tool_mastery_bonus=tool_mastery_bonus,
            complexity_bonus=complexity_bonus,
            collaboration_bonus=collaboration_bonus,
            specialization_bonus=specialization_bonus,
            consistency_bonus=consistency_bonus,
            total_xp=total_xp,
            level=level,
            next_level_xp=next_level_xp
        )
    
    def _calculate_specialization_bonus(self, agent_name: str, invocations: List[AgentInvocation]) -> int:
        """Calculate bonus for staying within specialization"""
        # Find agent's primary specialization
        agent_specialization = None
        for spec, spec_agents in self.specialization_categories.items():
            if agent_name in spec_agents:
                agent_specialization = spec
                break
        
        if not agent_specialization:
            return 0
        
        # Count projects in same specialization domain
        specialization_projects = set()
        for inv in invocations:
            # Simple heuristic: if project path contains specialization keywords
            project_lower = inv.project_path.lower()
            if agent_specialization in project_lower or any(
                keyword in project_lower for keyword in self.specialization_categories[agent_specialization]
            ):
                specialization_projects.add(inv.project_path)
        
        return len(specialization_projects) * 20
    
    def _calculate_consistency_bonus(self, invocations: List[AgentInvocation]) -> int:
        """Calculate bonus for consistent usage over time"""
        if len(invocations) < 2:
            return 0
        
        # Calculate usage days
        usage_dates = set(inv.timestamp.date() for inv in invocations)
        
        # More days = higher consistency bonus
        if len(usage_dates) >= 7:
            return 100  # Weekly consistency
        elif len(usage_dates) >= 3:
            return 50   # Multi-day consistency
        elif len(usage_dates) >= 2:
            return 25   # Basic consistency
        else:
            return 0
    
    def _calculate_level_from_xp(self, xp: int) -> int:
        """Calculate level from XP"""
        for threshold, level in reversed(self.xp_levels):
            if xp >= threshold:
                return level
        return 1
    
    def _get_next_level_xp(self, current_level: int) -> int:
        """Get XP needed for next level"""
        for threshold, level in self.xp_levels:
            if level > current_level:
                return threshold
        return self.xp_levels[-1][0]  # Max level reached


# CLI Interface
if __name__ == "__main__":
    import sys
    
    analyzer = AgentLogsAnalyzer()
    
    if len(sys.argv) < 2:
        print("Usage: python agent_logs_analyzer.py [command] [args]")
        print("Commands:")
        print("  analyze                  - Full agent analysis")
        print("  invocations              - Show agent invocations")
        print("  squads                   - Show squad formations")
        print("  xp [agent]               - Show XP calculations")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "analyze":
        print("🔍 Analyzing agent usage from Claude Code logs...")
        invocations = analyzer.parse_conversation_logs()
        formations = analyzer.detect_squad_formations(invocations)
        xp_data = analyzer.calculate_agent_xp(invocations)
        
        print(f"\n📊 Analysis Results:")
        print(f"   Agent invocations: {len(invocations)}")
        print(f"   Squad formations: {len(formations)}")
        print(f"   Agents with XP: {len(xp_data)}")
        
        # Top agents by XP
        top_agents = sorted(xp_data.values(), key=lambda x: x.total_xp, reverse=True)[:5]
        print(f"\n🏆 Top Agents:")
        for agent in top_agents:
            print(f"   {agent.agent_name}: Level {agent.level} ({agent.total_xp:,} XP)")
    
    elif command == "invocations":
        invocations = analyzer.parse_conversation_logs()
        print(f"Found {len(invocations)} agent invocations:")
        for inv in invocations[:10]:
            collab = f" (+{len(inv.collaboration_agents)} collab)" if inv.collaboration_agents else ""
            print(f"  {inv.timestamp.strftime('%m-%d %H:%M')} | {inv.agent_name} | {inv.project_path.split('/')[-1]} | {'✓' if inv.success else '✗'}{collab}")
    
    elif command == "squads":
        invocations = analyzer.parse_conversation_logs()
        formations = analyzer.detect_squad_formations(invocations)
        print(f"Found {len(formations)} squad formations:")
        for formation in formations:
            print(f"  {formation.formation_type}: {', '.join(formation.agents)} ({formation.success_rate:.1%} success)")
    
    elif command == "xp":
        invocations = analyzer.parse_conversation_logs()
        xp_data = analyzer.calculate_agent_xp(invocations)
        
        if len(sys.argv) > 2:
            agent_name = sys.argv[2]
            if agent_name in xp_data:
                xp = xp_data[agent_name]
                print(f"XP Breakdown for {agent_name}:")
                print(f"  Base XP: {xp.base_xp}")
                print(f"  Success Bonus: {xp.success_bonus}")
                print(f"  Tool Mastery: {xp.tool_mastery_bonus}")
                print(f"  Complexity: {xp.complexity_bonus}")
                print(f"  Collaboration: {xp.collaboration_bonus}")
                print(f"  Specialization: {xp.specialization_bonus}")
                print(f"  Consistency: {xp.consistency_bonus}")
                print(f"  Total XP: {xp.total_xp}")
                print(f"  Level: {xp.level}")
            else:
                print(f"Agent {agent_name} not found in XP data")
        else:
            # Show all agents
            for agent_name, xp in sorted(xp_data.items(), key=lambda x: x[1].total_xp, reverse=True):
                print(f"  {agent_name}: Level {xp.level} ({xp.total_xp:,} XP)")
    
    else:
        print("Invalid command")