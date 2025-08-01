#!/usr/bin/env python3
"""
Claude Code Log Parser for Agent Analytics
Parses Claude Code conversation logs to extract agent usage data
"""

import json
import os
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentInvocation:
    """Represents a single agent invocation from Claude Code logs"""
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
    
@dataclass
class SessionMetrics:
    """Session-level analytics"""
    session_id: str
    start_time: datetime
    end_time: datetime
    duration_minutes: float
    total_tokens: int
    tools_used: List[str]
    success_rate: float
    error_count: int
    agents_invoked: List[str]

class ClaudeCodeLogParser:
    """
    Parses Claude Code conversation logs to extract agent usage analytics
    
    Features:
    - Agent invocation detection from conversation context
    - Tool usage tracking
    - Token consumption analysis
    - Success/failure pattern recognition
    - Session-based metrics
    """
    
    def __init__(self, log_directory: str = None):
        """
        Initialize log parser
        
        Args:
            log_directory: Path to Claude Code logs (defaults to ~/.claude/projects/)
        """
        if log_directory is None:
            log_directory = Path.home() / ".claude" / "projects"
        
        self.log_directory = Path(log_directory)
        
        # Agent name patterns - these help identify when agents are mentioned
        self.agent_patterns = {
            # Development agents
            "python-elite": r"\b(?:python.elite|python elite|elite python)\b",
            "javascript-pro": r"\b(?:javascript.pro|javascript pro|js pro)\b", 
            "golang-pro": r"\b(?:golang.pro|golang pro|go pro)\b",
            "rust-pro": r"\b(?:rust.pro|rust pro)\b",
            "full-stack-architect": r"\b(?:full.?stack.?architect|fullstack architect)\b",
            "backend-architect": r"\b(?:backend.?architect|backend architect)\b",
            "frontend-developer": r"\b(?:frontend.?developer|frontend developer)\b",
            
            # Data & AI agents
            "data-engineer": r"\b(?:data.?engineer|data engineer)\b",
            "ai-engineer": r"\b(?:ai.?engineer|ai engineer)\b",
            "ml-engineer": r"\b(?:ml.?engineer|ml engineer|machine learning engineer)\b",
            
            # Infrastructure agents
            "devops-engineer": r"\b(?:devops.?engineer|devops engineer)\b",
            "cloud-architect": r"\b(?:cloud.?architect|cloud architect)\b",
            "deployment-engineer": r"\b(?:deployment.?engineer|deployment engineer)\b",
            
            # Quality agents
            "test-engineer": r"\b(?:test.?engineer|test engineer)\b",
            "code-reviewer": r"\b(?:code.?reviewer|code reviewer)\b",
            "performance-engineer": r"\b(?:performance.?engineer|performance engineer)\b",
            
            # Security agents
            "security-auditor": r"\b(?:security.?auditor|security auditor)\b",
            
            # Business agents
            "business-analyst": r"\b(?:business.?analyst|business analyst)\b",
            "product-manager": r"\b(?:product.?manager|product manager)\b"
        }
        
        # Tool usage patterns
        self.tool_patterns = {
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
        
    def get_all_log_files(self) -> List[Path]:
        """Get all .jsonl log files from the projects directory"""
        log_files = []
        
        if not self.log_directory.exists():
            logger.warning(f"Log directory does not exist: {self.log_directory}")
            return log_files
            
        # Recursively find all .jsonl files
        for project_dir in self.log_directory.iterdir():
            if project_dir.is_dir():
                for log_file in project_dir.glob("*.jsonl"):
                    log_files.append(log_file)
        
        logger.info(f"Found {len(log_files)} log files")
        return sorted(log_files)
    
    def parse_log_file(self, log_file: Path) -> List[Dict[str, Any]]:
        """Parse a single .jsonl log file"""
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
                        continue
                        
        except Exception as e:
            logger.error(f"Error reading log file {log_file}: {e}")
            
        return entries
    
    def extract_project_path_from_filename(self, log_file_path: Path) -> str:
        """Extract project path from log directory structure"""
        # Log files are stored like: ~/.claude/projects/-Users-mylee-Desktop-mylee-project-name/uuid.jsonl
        parent_dir = log_file_path.parent.name
        
        # Convert encoded path back to normal path
        if parent_dir.startswith('-') and parent_dir.endswith('-'):
            # Remove leading and trailing dashes, replace - with /
            decoded_path = parent_dir[1:-1].replace('-', '/')
            return f"/{decoded_path}"
        
        return parent_dir
    
    def detect_agent_mentions(self, text: str) -> List[str]:
        """Detect agent names mentioned in conversation text"""
        agents_found = []
        text_lower = text.lower()
        
        for agent_name, pattern in self.agent_patterns.items():
            if re.search(pattern, text_lower, re.IGNORECASE):
                agents_found.append(agent_name)
        
        return agents_found
    
    def extract_tools_from_message(self, message: Dict[str, Any]) -> List[str]:
        """Extract tool names from assistant messages"""
        tools = []
        
        if message.get("type") == "assistant" and "message" in message:
            msg_content = message["message"]
            if isinstance(msg_content, dict) and "content" in msg_content:
                content = str(msg_content["content"])
                
                for tool_name, pattern in self.tool_patterns.items():
                    if re.search(pattern, content):
                        tools.append(tool_name)
        
        return tools
    
    def determine_task_success(self, entries: List[Dict[str, Any]], start_idx: int) -> Tuple[bool, Optional[str]]:
        """
        Determine if a task was successful based on subsequent entries
        Look for error patterns, successful tool completions, etc.
        """
        success = True
        error_message = None
        
        # Look at the next few entries for error indicators
        for i in range(start_idx, min(start_idx + 10, len(entries))):
            entry = entries[i]
            
            # Check for tool use errors
            if "toolUseResult" in entry:
                if entry["toolUseResult"] == "Error":
                    success = False
                    error_message = str(entry.get("message", {}).get("content", "Tool use error"))
                    break
            
            # Check for error messages in content
            if "message" in entry and isinstance(entry["message"], dict):
                content = str(entry["message"].get("content", ""))
                if "error" in content.lower() or "failed" in content.lower():
                    success = False
                    error_message = content[:200]  # First 200 chars
                    break
        
        return success, error_message
    
    def extract_invocations_from_entries(self, entries: List[Dict[str, Any]], 
                                       project_path: str) -> List[AgentInvocation]:
        """Extract agent invocations from log entries"""
        invocations = []
        
        for i, entry in enumerate(entries):
            # Skip non-user and non-assistant messages
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
            
            # Look for agent mentions in message content
            message = entry.get("message", {})
            content = ""
            
            if isinstance(message, dict) and "content" in message:
                if isinstance(message["content"], str):
                    content = message["content"]
                elif isinstance(message["content"], list):
                    # Handle structured content
                    for item in message["content"]:
                        if isinstance(item, dict) and item.get("type") == "text":
                            content += item.get("text", "") + " "
            
            # Detect agent mentions
            agents_mentioned = self.detect_agent_mentions(content)
            
            if agents_mentioned:
                # Extract additional context
                tools_used = self.extract_tools_from_message(entry)
                tokens_used = 0
                model = ""
                
                # Extract usage info from assistant messages
                if entry.get("type") == "assistant" and "message" in entry:
                    msg = entry["message"]
                    if "usage" in msg:
                        usage = msg["usage"]
                        tokens_used = (usage.get("input_tokens", 0) + 
                                     usage.get("output_tokens", 0) +
                                     usage.get("cache_read_input_tokens", 0))
                    model = msg.get("model", "")
                
                # Determine success
                success, error_message = self.determine_task_success(entries, i)
                
                # Create invocation for each agent mentioned
                for agent_name in agents_mentioned:
                    invocation = AgentInvocation(
                        agent_name=agent_name,
                        session_id=session_id,
                        timestamp=timestamp,
                        project_path=project_path,
                        task_description=content[:300],  # First 300 chars as task description
                        tools_used=tools_used,
                        success=success,
                        error_message=error_message,
                        tokens_used=tokens_used,
                        model=model,
                        git_branch=entry.get("gitBranch", "")
                    )
                    invocations.append(invocation)
        
        return invocations
    
    def parse_all_logs(self, days_back: int = 30) -> List[AgentInvocation]:
        """
        Parse all log files and extract agent invocations
        
        Args:
            days_back: Only parse logs from the last N days
            
        Returns:
            List of AgentInvocation objects
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        all_invocations = []
        
        log_files = self.get_all_log_files()
        
        for log_file in log_files:
            # Check file modification time
            if log_file.stat().st_mtime < cutoff_date.timestamp():
                continue
                
            logger.info(f"Parsing {log_file.name}...")
            
            entries = self.parse_log_file(log_file)
            if not entries:
                continue
                
            project_path = self.extract_project_path_from_filename(log_file)
            invocations = self.extract_invocations_from_entries(entries, project_path)
            
            all_invocations.extend(invocations)
            logger.info(f"  Found {len(invocations)} agent invocations")
        
        logger.info(f"Total agent invocations found: {len(all_invocations)}")
        return all_invocations
    
    def calculate_session_metrics(self, invocations: List[AgentInvocation]) -> List[SessionMetrics]:
        """Calculate session-level metrics from invocations"""
        sessions = {}
        
        # Group by session
        for inv in invocations:
            if inv.session_id not in sessions:
                sessions[inv.session_id] = []
            sessions[inv.session_id].append(inv)
        
        session_metrics = []
        
        for session_id, session_invocations in sessions.items():
            if not session_invocations:
                continue
                
            # Sort by timestamp
            session_invocations.sort(key=lambda x: x.timestamp)
            
            start_time = session_invocations[0].timestamp
            end_time = session_invocations[-1].timestamp
            duration_minutes = (end_time - start_time).total_seconds() / 60
            
            # Calculate metrics
            total_tokens = sum(inv.tokens_used for inv in session_invocations)
            tools_used = list(set(tool for inv in session_invocations for tool in inv.tools_used))
            success_count = sum(1 for inv in session_invocations if inv.success)
            success_rate = success_count / len(session_invocations) if session_invocations else 0
            error_count = sum(1 for inv in session_invocations if not inv.success)
            agents_invoked = list(set(inv.agent_name for inv in session_invocations))
            
            metrics = SessionMetrics(
                session_id=session_id,
                start_time=start_time,
                end_time=end_time,
                duration_minutes=duration_minutes,
                total_tokens=total_tokens,
                tools_used=tools_used,
                success_rate=success_rate,
                error_count=error_count,
                agents_invoked=agents_invoked
            )
            session_metrics.append(metrics)
        
        return session_metrics
    
    def export_analytics_data(self, output_file: str = None) -> Dict[str, Any]:
        """
        Parse logs and export comprehensive analytics data
        
        Returns:
            Dictionary containing all analytics data
        """
        if output_file is None:
            output_file = Path.home() / ".claude" / "agent_analytics.json"
        
        logger.info("Starting comprehensive log analysis...")
        
        # Parse all recent logs
        invocations = self.parse_all_logs(days_back=30)
        session_metrics = self.calculate_session_metrics(invocations)
        
        # Calculate overall statistics
        analytics_data = {
            "generated_at": datetime.now().isoformat(),
            "total_invocations": len(invocations),
            "total_sessions": len(session_metrics),
            "date_range_days": 30,
            "invocations": [asdict(inv) for inv in invocations],
            "session_metrics": [asdict(sm) for sm in session_metrics],
            "summary_stats": self._calculate_summary_stats(invocations, session_metrics)
        }
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(analytics_data, f, indent=2, default=str)
        
        logger.info(f"Analytics data exported to {output_file}")
        return analytics_data
    
    def _calculate_summary_stats(self, invocations: List[AgentInvocation], 
                                sessions: List[SessionMetrics]) -> Dict[str, Any]:
        """Calculate summary statistics"""
        if not invocations:
            return {}
        
        # Agent usage stats
        agent_counts = {}
        agent_success_rates = {}
        
        for inv in invocations:
            agent_counts[inv.agent_name] = agent_counts.get(inv.agent_name, 0) + 1
            
            if inv.agent_name not in agent_success_rates:
                agent_success_rates[inv.agent_name] = {"success": 0, "total": 0}
            
            agent_success_rates[inv.agent_name]["total"] += 1
            if inv.success:
                agent_success_rates[inv.agent_name]["success"] += 1
        
        # Calculate success rates
        for agent in agent_success_rates:
            stats = agent_success_rates[agent]
            stats["rate"] = stats["success"] / stats["total"] if stats["total"] > 0 else 0
        
        # Tool usage stats
        tool_counts = {}
        for inv in invocations:
            for tool in inv.tools_used:
                tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        # Project activity
        project_counts = {}
        for inv in invocations:
            project_counts[inv.project_path] = project_counts.get(inv.project_path, 0) + 1
        
        return {
            "most_used_agents": sorted(agent_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "agent_success_rates": {k: v["rate"] for k, v in agent_success_rates.items()},
            "most_used_tools": sorted(tool_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "most_active_projects": sorted(project_counts.items(), key=lambda x: x[1], reverse=True)[:10],
            "total_tokens_consumed": sum(inv.tokens_used for inv in invocations),
            "average_session_duration": sum(s.duration_minutes for s in sessions) / len(sessions) if sessions else 0,
            "overall_success_rate": sum(1 for inv in invocations if inv.success) / len(invocations) if invocations else 0
        }


# CLI Interface
if __name__ == "__main__":
    import sys
    
    parser = ClaudeCodeLogParser()
    
    if len(sys.argv) < 2:
        print("Usage: python log_parser.py [command] [args]")
        print("Commands:")
        print("  parse                    - Parse all logs and show summary")
        print("  export [file]            - Export analytics data to JSON")
        print("  agents                   - Show agent usage statistics")
        print("  sessions                 - Show session metrics")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "parse":
        invocations = parser.parse_all_logs()
        print(f"Found {len(invocations)} agent invocations")
        
        if invocations:
            agent_counts = {}
            for inv in invocations:
                agent_counts[inv.agent_name] = agent_counts.get(inv.agent_name, 0) + 1
            
            print("\nTop Agents:")
            for agent, count in sorted(agent_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {agent}: {count} invocations")
    
    elif command == "export":
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        data = parser.export_analytics_data(output_file)
        print(f"Exported {data['total_invocations']} invocations from {data['total_sessions']} sessions")
    
    elif command == "agents":
        invocations = parser.parse_all_logs()
        agent_stats = {}
        
        for inv in invocations:
            if inv.agent_name not in agent_stats:
                agent_stats[inv.agent_name] = {"calls": 0, "success": 0, "tokens": 0}
            
            stats = agent_stats[inv.agent_name]
            stats["calls"] += 1
            stats["tokens"] += inv.tokens_used
            if inv.success:
                stats["success"] += 1
        
        print("Agent Statistics:")
        print("=" * 80)
        print(f"{'Agent':<25} {'Calls':<8} {'Success':<8} {'Rate':<8} {'Tokens':<10}")
        print("-" * 80)
        
        for agent, stats in sorted(agent_stats.items(), key=lambda x: x[1]["calls"], reverse=True):
            success_rate = stats["success"] / stats["calls"] if stats["calls"] > 0 else 0
            print(f"{agent:<25} {stats['calls']:<8} {stats['success']:<8} {success_rate:.1%} {stats['tokens']:<10}")
    
    elif command == "sessions":
        invocations = parser.parse_all_logs()
        sessions = parser.calculate_session_metrics(invocations)
        
        print(f"Session Metrics ({len(sessions)} sessions):")
        print("=" * 80)
        
        for session in sorted(sessions, key=lambda x: x.start_time, reverse=True)[:10]:
            print(f"Session: {session.session_id[:8]}...")
            print(f"  Duration: {session.duration_minutes:.1f} minutes")
            print(f"  Agents: {', '.join(session.agents_invoked)}")
            print(f"  Success Rate: {session.success_rate:.1%}")
            print(f"  Tokens: {session.total_tokens:,}")
            print()
    
    else:
        print("Invalid command")