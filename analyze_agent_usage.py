#!/usr/bin/env python3
"""
Elite Agent Usage Analytics
Main analytics script that transforms AgentRegistry into a comprehensive analytics engine

Features:
- Real Claude Code log analysis
- Agent usage statistics and rankings
- Beautiful visualized reports
- XP calculations based on actual usage
- Tech stack and project insights
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
import argparse

# Add the gamification core to path
sys.path.append(str(Path(__file__).parent / "gamification" / "core"))

try:
    from agent_registry import AgentRegistry
    from log_parser import ClaudeCodeLogParser, AgentInvocation
    from agents_tracker import AgentsTracker
    from agent_logs_analyzer import AgentLogsAnalyzer, SquadFormation, AgentXPCalculation
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Please ensure the gamification core modules are available")
    sys.exit(1)

@dataclass
class AgentAnalytics:
    """Comprehensive agent analytics"""
    name: str
    total_invocations: int
    successful_tasks: int
    failed_tasks: int
    success_rate: float
    total_xp: int
    current_level: int
    tokens_consumed: int
    tools_used: List[str]
    projects_worked_on: List[str]
    tech_stack_focus: List[str]
    last_used: datetime
    avg_session_duration: float
    specialization_score: float
    
@dataclass 
class ProjectAnalytics:
    """Project-level analytics"""
    project_path: str
    total_agent_calls: int
    unique_agents_used: List[str]
    primary_tech_stack: List[str]
    success_rate: float
    total_tokens: int
    active_days: int
    last_activity: datetime

class EliteAgentAnalytics:
    """
    Elite Agent Analytics Engine
    
    Combines AgentRegistry metadata with real Claude Code usage data
    to provide comprehensive insights and gamification
    """
    
    def __init__(self):
        """Initialize the analytics engine"""
        self.registry = AgentRegistry()
        self.log_parser = ClaudeCodeLogParser()
        self.agents_tracker = AgentsTracker()
        self.agent_analyzer = AgentLogsAnalyzer()  # New agent-specific analyzer
        
        # Load fresh data
        self._load_usage_data()
        
    def _load_usage_data(self):
        """Load and parse recent usage data"""
        print("🔍 Analyzing Claude Code logs with enhanced agent detection...")
        
        # Use both parsers for comprehensive analysis
        self.invocations = self.log_parser.parse_all_logs(days_back=30)
        self.session_metrics = self.log_parser.calculate_session_metrics(self.invocations)
        
        # Enhanced agent-specific analysis
        self.agent_invocations = self.agent_analyzer.parse_conversation_logs(days_back=30)
        self.squad_formations = self.agent_analyzer.detect_squad_formations(self.agent_invocations)
        self.agent_xp_data = self.agent_analyzer.calculate_agent_xp(self.agent_invocations)
        
        print(f"   Found {len(self.invocations)} basic invocations + {len(self.agent_invocations)} enhanced agent invocations")
        print(f"   Detected {len(self.squad_formations)} squad formations across {len(self.session_metrics)} sessions")
    
    def calculate_agent_analytics(self) -> List[AgentAnalytics]:
        """Calculate comprehensive agent analytics"""
        agent_data = {}
        
        # Process all invocations
        for inv in self.invocations:
            if inv.agent_name not in agent_data:
                agent_data[inv.agent_name] = {
                    "invocations": [],
                    "projects": set(),
                    "tools": set(),
                    "total_tokens": 0,
                    "success_count": 0,
                    "fail_count": 0
                }
            
            data = agent_data[inv.agent_name]
            data["invocations"].append(inv)
            data["projects"].add(inv.project_path)
            data["tools"].update(inv.tools_used)
            data["total_tokens"] += inv.tokens_used
            
            if inv.success:
                data["success_count"] += 1
            else:
                data["fail_count"] += 1
        
        # Calculate analytics for each agent
        analytics = []
        
        for agent_name, data in agent_data.items():
            invocations = data["invocations"]
            total_calls = len(invocations)
            success_rate = data["success_count"] / total_calls if total_calls > 0 else 0
            
            # Get registry metadata
            registry_metadata = self.registry.get_agent_by_name(agent_name)
            tech_stack_focus = registry_metadata.tech_stack if registry_metadata else []
            
            # Calculate XP based on real usage
            total_xp = self._calculate_real_xp(invocations)
            current_level = self._calculate_level(total_xp)
            
            # Calculate session duration
            session_durations = []
            agent_sessions = {}
            for inv in invocations:
                if inv.session_id not in agent_sessions:
                    agent_sessions[inv.session_id] = []
                agent_sessions[inv.session_id].append(inv.timestamp)
            
            for session_times in agent_sessions.values():
                if len(session_times) > 1:
                    session_times.sort()
                    duration = (session_times[-1] - session_times[0]).total_seconds() / 60
                    session_durations.append(duration)
            
            avg_session_duration = sum(session_durations) / len(session_durations) if session_durations else 0
            
            # Calculate specialization score (focus on specific tech/projects)
            specialization_score = self._calculate_specialization_score(data)
            
            # Get most recent usage
            last_used = max(inv.timestamp for inv in invocations) if invocations else datetime.min
            
            analytics_obj = AgentAnalytics(
                name=agent_name,
                total_invocations=total_calls,
                successful_tasks=data["success_count"],
                failed_tasks=data["fail_count"],
                success_rate=success_rate,
                total_xp=total_xp,
                current_level=current_level,
                tokens_consumed=data["total_tokens"],
                tools_used=list(data["tools"]),
                projects_worked_on=list(data["projects"]),
                tech_stack_focus=tech_stack_focus,
                last_used=last_used,
                avg_session_duration=avg_session_duration,
                specialization_score=specialization_score
            )
            
            analytics.append(analytics_obj)
        
        return sorted(analytics, key=lambda x: x.total_xp, reverse=True)
    
    def _calculate_real_xp(self, invocations: List[AgentInvocation]) -> int:
        """Calculate XP based on real usage patterns"""
        total_xp = 0
        
        for inv in invocations:
            # Base XP
            base_xp = 25
            
            # Success bonus
            if inv.success:
                base_xp += 25
            
            # Tool usage bonus
            base_xp += len(inv.tools_used) * 5
            
            # Token usage bonus (for complex tasks)
            if inv.tokens_used > 1000:
                base_xp += 20
            elif inv.tokens_used > 500:
                base_xp += 10
            
            # Project diversity bonus
            if len(set(i.project_path for i in invocations)) > 3:
                base_xp += 5
            
            total_xp += base_xp
        
        return total_xp
    
    def _calculate_level(self, xp: int) -> int:
        """Calculate level from XP"""
        if xp < 100:
            return 1
        elif xp < 300:
            return 2
        elif xp < 600:
            return 3
        elif xp < 1000:
            return 4
        elif xp < 1500:
            return 5
        elif xp < 2500:
            return 6
        elif xp < 4000:
            return 7
        elif xp < 6000:
            return 8
        elif xp < 10000:
            return 9
        else:
            return 10
    
    def _calculate_specialization_score(self, agent_data: Dict) -> float:
        """Calculate how specialized an agent is (0-1 scale)"""
        # More focused on fewer projects/tools = higher specialization
        num_projects = len(agent_data["projects"])
        num_tools = len(agent_data["tools"])
        total_invocations = len(agent_data["invocations"])
        
        if total_invocations == 0:
            return 0.0
        
        # Inverse relationship - fewer projects/tools with more usage = more specialized
        project_focus = min(1.0, 5.0 / max(num_projects, 1))
        tool_focus = min(1.0, 10.0 / max(num_tools, 1))
        usage_intensity = min(1.0, total_invocations / 20.0)
        
        return (project_focus + tool_focus + usage_intensity) / 3.0
    
    def calculate_project_analytics(self) -> List[ProjectAnalytics]:
        """Calculate project-level analytics"""
        project_data = {}
        
        for inv in self.invocations:
            if inv.project_path not in project_data:
                project_data[inv.project_path] = {
                    "invocations": [],
                    "agents": set(),
                    "days": set(),
                    "success_count": 0,
                    "total_tokens": 0
                }
            
            data = project_data[inv.project_path]
            data["invocations"].append(inv)
            data["agents"].add(inv.agent_name)
            data["days"].add(inv.timestamp.date())
            data["total_tokens"] += inv.tokens_used
            
            if inv.success:
                data["success_count"] += 1
        
        analytics = []
        
        for project_path, data in project_data.items():
            invocations = data["invocations"]
            total_calls = len(invocations)
            success_rate = data["success_count"] / total_calls if total_calls > 0 else 0
            
            # Determine primary tech stack from agents used
            tech_stack = set()
            for agent_name in data["agents"]:
                agent_metadata = self.registry.get_agent_by_name(agent_name)
                if agent_metadata:
                    tech_stack.update(agent_metadata.tech_stack)
            
            last_activity = max(inv.timestamp for inv in invocations) if invocations else datetime.min
            
            project_analytics = ProjectAnalytics(
                project_path=project_path,
                total_agent_calls=total_calls,
                unique_agents_used=list(data["agents"]),
                primary_tech_stack=list(tech_stack),
                success_rate=success_rate,
                total_tokens=data["total_tokens"],
                active_days=len(data["days"]),
                last_activity=last_activity
            )
            
            analytics.append(project_analytics)
        
        return sorted(analytics, key=lambda x: x.total_agent_calls, reverse=True)
    
    def generate_leaderboard_report(self) -> str:
        """Generate beautiful leaderboard report"""
        analytics = self.calculate_agent_analytics()
        
        if not analytics:
            return "No agent usage data found. Start using agents to see the leaderboard!"
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                           🏆 ELITE AGENT LEADERBOARD 🏆                      ║")
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append("║                                                                              ║")
        
        # Top 10 agents
        for i, agent in enumerate(analytics[:10], 1):
            # Level indicators
            if agent.current_level >= 8:
                level_icon = "🌟"
                tier = "LEGENDARY"
            elif agent.current_level >= 6:
                level_icon = "⭐"
                tier = "ELITE"
            elif agent.current_level >= 4:
                level_icon = "🔥"
                tier = "EXPERT"
            elif agent.current_level >= 2:
                level_icon = "💪"
                tier = "SKILLED"
            else:
                level_icon = "🌱"
                tier = "NOVICE"
            
            # Format stats
            name_display = f"{agent.name[:20]:<20}"
            xp_display = f"{agent.total_xp:,}"
            level_display = f"L{agent.current_level}"
            success_display = f"{agent.success_rate:.1%}"
            calls_display = f"{agent.total_invocations}"
            
            report.append(f"║ {i:2}. {level_icon} {name_display} │ {level_display:<3} │ {tier:<9} │ {xp_display:>6} XP │ {calls_display:>4} calls │ ║")
            report.append(f"║     └─ Success: {success_display} │ Tools: {len(agent.tools_used)} │ Projects: {len(agent.projects_worked_on)} │ Tokens: {agent.tokens_consumed:,}   ║")
            report.append("║                                                                              ║")
        
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        
        # Quick stats
        total_agents = len(analytics)
        avg_success_rate = sum(a.success_rate for a in analytics) / total_agents if total_agents > 0 else 0
        total_xp = sum(a.total_xp for a in analytics)
        total_invocations = sum(a.total_invocations for a in analytics)
        
        report.append(f"║  📊 Squad Stats: {total_agents} agents active │ {avg_success_rate:.1%} avg success │ {total_xp:,} total XP     ║")
        report.append(f"║  🎯 Total Missions: {total_invocations:,} │ Last 30 days of epic agent action!           ║")
        report.append("║                                                                              ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(report)
    
    def generate_tech_stack_report(self) -> str:
        """Generate tech stack focus report"""
        analytics = self.calculate_agent_analytics()
        
        # Aggregate tech stack usage
        tech_usage = {}
        for agent in analytics:
            for tech in agent.tech_stack_focus:
                if tech not in tech_usage:
                    tech_usage[tech] = {"agents": [], "total_xp": 0, "total_calls": 0}
                tech_usage[tech]["agents"].append(agent.name)
                tech_usage[tech]["total_xp"] += agent.total_xp
                tech_usage[tech]["total_calls"] += agent.total_invocations
        
        # Sort by total XP
        sorted_tech = sorted(tech_usage.items(), key=lambda x: x[1]["total_xp"], reverse=True)
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                        🛠️  TECH STACK MASTERY REPORT 🛠️                      ║")
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append("║                                                                              ║")
        
        for tech, data in sorted_tech[:10]:
            agent_count = len(set(data["agents"]))
            xp_display = f"{data['total_xp']:,}"
            calls_display = f"{data['total_calls']:,}"
            
            report.append(f"║  🔧 {tech:<20} │ {agent_count:2} agents │ {xp_display:>8} XP │ {calls_display:>6} calls    ║")
            report.append(f"║     Specialists: {', '.join(list(set(data['agents']))[:3])}{'...' if agent_count > 3 else ''}                    ║")
            report.append("║                                                                              ║")
        
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(report)
    
    def generate_project_activity_report(self) -> str:
        """Generate project activity report"""
        project_analytics = self.calculate_project_analytics()
        
        if not project_analytics:
            return "No project activity found."
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                       📊 PROJECT ACTIVITY REPORT 📊                         ║")
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append("║                                                                              ║")
        
        for project in project_analytics[:10]:
            # Shorten project path for display
            project_name = Path(project.project_path).name or project.project_path.split('/')[-1]
            if len(project_name) > 25:
                project_name = project_name[:22] + "..."
            
            calls_display = f"{project.total_agent_calls}"
            agents_display = f"{len(project.unique_agents_used)}"
            success_display = f"{project.success_rate:.1%}"
            days_display = f"{project.active_days}"
            
            report.append(f"║  📁 {project_name:<25} │ {calls_display:>4} calls │ {agents_display:>2} agents │ {success_display} success ║")
            report.append(f"║     Tech: {', '.join(project.primary_tech_stack[:3])}{'...' if len(project.primary_tech_stack) > 3 else ''}                                       ║")
            report.append(f"║     Active: {days_display} days │ Tokens: {project.total_tokens:,}                              ║")
            report.append("║                                                                              ║")
        
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(report)
    
    def generate_squad_formations_report(self) -> str:
        """Generate squad formations analysis report"""
        if not self.squad_formations:
            return "No squad formations detected. Try collaborating with multiple agents!"
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                        🤝 SQUAD FORMATIONS ANALYSIS 🤝                      ║")
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append("║                                                                              ║")
        
        # Sort by synergy score
        sorted_formations = sorted(self.squad_formations, key=lambda x: x.synergy_score, reverse=True)
        
        for i, formation in enumerate(sorted_formations[:10], 1):
            # Formation type icon
            formation_icons = {
                "full-stack": "🏗️", "data-pipeline": "📊", "security-audit": "🔒",
                "performance-optimization": "⚡", "feature-development": "✨",
                "ml-deployment": "🤖", "incident-response": "🚨", 
                "multi-disciplinary": "🌟", "specialized": "🎯"
            }
            icon = formation_icons.get(formation.formation_type, "👥")
            
            # Format squad info
            agents_display = ", ".join(formation.agents[:3])
            if len(formation.agents) > 3:
                agents_display += f" + {len(formation.agents) - 3} more"
            
            duration = (formation.end_time - formation.start_time).total_seconds() / 60
            
            report.append(f"║ {i:2}. {icon} {formation.formation_type.upper():<20}                               ║")
            report.append(f"║     Squad: {agents_display:<50}              ║")
            report.append(f"║     Synergy: {formation.synergy_score:.2f} │ Success: {formation.success_rate:.1%} │ Tasks: {formation.total_tasks} │ Duration: {duration:.0f}m ║")
            report.append(f"║     Project: {formation.project_path.split('/')[-1][:30]:<30}                        ║")
            report.append("║                                                                              ║")
        
        # Squad statistics
        total_formations = len(self.squad_formations)
        avg_synergy = sum(f.synergy_score for f in self.squad_formations) / total_formations
        avg_success = sum(f.success_rate for f in self.squad_formations) / total_formations
        
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append(f"║  📈 Squad Stats: {total_formations} formations │ {avg_synergy:.2f} avg synergy │ {avg_success:.1%} avg success    ║")
        report.append("║  💡 Tip: Higher synergy = better agent collaboration and timing!             ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(report)
    
    def generate_xp_leaderboard_report(self) -> str:
        """Generate XP-based leaderboard using the enhanced analyzer"""
        if not self.agent_xp_data:
            return "No XP data available. Start using agents to earn XP!"
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                      ⚡ ELITE AGENT XP LEADERBOARD ⚡                        ║")
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append("║                                                                              ║")
        
        # Sort by total XP
        sorted_agents = sorted(self.agent_xp_data.values(), key=lambda x: x.total_xp, reverse=True)
        
        for i, agent_xp in enumerate(sorted_agents[:10], 1):
            # Level indicators with enhanced tiers
            if agent_xp.level >= 9:
                level_icon = "🏆"
                tier = "GRANDMASTER"
            elif agent_xp.level >= 7:
                level_icon = "💎"
                tier = "MASTER"
            elif agent_xp.level >= 5:
                level_icon = "⭐"
                tier = "ELITE"
            elif agent_xp.level >= 3:
                level_icon = "🔥"
                tier = "EXPERT"
            else:
                level_icon = "🌱"
                tier = "APPRENTICE"
            
            # Format displays
            name_display = f"{agent_xp.agent_name[:22]:<22}"
            xp_display = f"{agent_xp.total_xp:,}"
            level_display = f"L{agent_xp.level}"
            progress = agent_xp.total_xp - (agent_xp.next_level_xp - agent_xp.total_xp) if agent_xp.level < 10 else agent_xp.total_xp
            
            report.append(f"║ {i:2}. {level_icon} {name_display} │ {level_display:<3} │ {tier:<11} │ {xp_display:>7} XP ║")
            
            # XP breakdown for top 3
            if i <= 3:
                report.append(f"║     🎯 Success: +{agent_xp.success_bonus} │ 🔧 Tools: +{agent_xp.tool_mastery_bonus} │ 🤝 Collab: +{agent_xp.collaboration_bonus} │ 📈 Spec: +{agent_xp.specialization_bonus}  ║")
            
            report.append("║                                                                              ║")
        
        # Overall XP stats
        total_xp = sum(agent.total_xp for agent in sorted_agents)
        avg_level = sum(agent.level for agent in sorted_agents) / len(sorted_agents)
        
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append(f"║  🏅 Total Squad XP: {total_xp:,} │ Average Level: {avg_level:.1f} │ Active Agents: {len(sorted_agents)}     ║")
        report.append("║  🚀 XP earned through real agent usage, collaboration, and consistency!     ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(report)
    
    def generate_insights_report(self) -> str:
        """Generate insights and recommendations based on usage patterns"""
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                          💡 USAGE INSIGHTS & TIPS 💡                        ║")
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append("║                                                                              ║")
        
        insights = []
        
        # Most productive agent
        if self.agent_xp_data:
            top_agent = max(self.agent_xp_data.values(), key=lambda x: x.total_xp)
            insights.append(f"🏆 Your most productive agent is {top_agent.agent_name} with {top_agent.total_xp:,} XP!")
        
        # Squad collaboration insights
        if self.squad_formations:
            best_formation = max(self.squad_formations, key=lambda x: x.synergy_score)
            insights.append(f"🤝 Best squad formation: {best_formation.formation_type} ({best_formation.synergy_score:.2f} synergy)")
            
            if len(self.squad_formations) >= 3:
                insights.append("🌟 You're great at squad formations! Keep collaborating for bonus XP!")
            else:
                insights.append("💡 Try using multiple agents together for squad formation bonuses!")
        
        # Tool usage insights
        if self.agent_invocations:
            all_tools = set()
            for inv in self.agent_invocations:
                all_tools.update(inv.tools_used)
            
            if len(all_tools) >= 5:
                insights.append(f"🔧 Tool master! You've used {len(all_tools)} different tools effectively!")
            else:
                insights.append("🛠️ Explore more tools to boost your tool mastery XP bonus!")
        
        # Consistency insights
        if self.agent_invocations:
            usage_dates = set(inv.timestamp.date() for inv in self.agent_invocations)
            if len(usage_dates) >= 7:
                insights.append("📅 Excellent consistency! Daily agent usage is paying off!")
            elif len(usage_dates) >= 3:
                insights.append("📈 Good consistency! Try daily agent usage for bigger bonuses!")
            else:
                insights.append("⏰ Use agents more regularly for consistency bonuses!")
        
        # Project diversity insights
        if self.agent_invocations:
            projects = set(inv.project_path for inv in self.agent_invocations)
            if len(projects) >= 3:
                insights.append(f"🎯 Multi-project expertise! Working across {len(projects)} projects!")
            else:
                insights.append("📂 Try agents on different projects for diversity bonuses!")
        
        # Performance insights
        if self.agent_invocations:
            success_rate = sum(1 for inv in self.agent_invocations if inv.success) / len(self.agent_invocations)
            if success_rate >= 0.9:
                insights.append("⭐ Exceptional success rate! Your agent usage is highly effective!")
            elif success_rate >= 0.7:
                insights.append("👍 Good success rate! Keep refining your agent collaboration!")
            else:
                insights.append("🎯 Focus on agent specializations to improve success rates!")
        
        # Display insights
        for i, insight in enumerate(insights[:8], 1):
            report.append(f"║  {i}. {insight:<73} ║")
            if i < len(insights):
                report.append("║                                                                              ║")
        
        if not insights:
            report.append("║  Start using agents to get personalized insights and recommendations!        ║")
        
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(report)
    
    def generate_comprehensive_report(self) -> str:
        """Generate comprehensive analytics report"""
        report_sections = [
            self.generate_xp_leaderboard_report(),
            "",
            self.generate_squad_formations_report(),
            "",
            self.generate_tech_stack_report(), 
            "",
            self.generate_project_activity_report(),
            "",
            self.generate_insights_report()
        ]
        
        return "\n".join(report_sections)
    
    def export_analytics_data(self, output_file: str = None) -> Dict[str, Any]:
        """Export complete analytics data to JSON"""
        if output_file is None:
            output_file = Path.home() / ".claude" / "elite_agent_analytics.json"
        
        agent_analytics = self.calculate_agent_analytics()
        project_analytics = self.calculate_project_analytics()
        
        export_data = {
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_agents": len(agent_analytics),
                "total_projects": len(project_analytics),
                "total_invocations": sum(a.total_invocations for a in agent_analytics),
                "total_xp": sum(a.total_xp for a in agent_analytics),
                "avg_success_rate": sum(a.success_rate for a in agent_analytics) / len(agent_analytics) if agent_analytics else 0,
                "analysis_period_days": 30
            },
            "agent_analytics": [
                {
                    "name": a.name,
                    "total_invocations": a.total_invocations,
                    "successful_tasks": a.successful_tasks,
                    "failed_tasks": a.failed_tasks,
                    "success_rate": a.success_rate,
                    "total_xp": a.total_xp,
                    "current_level": a.current_level,
                    "tokens_consumed": a.tokens_consumed,
                    "tools_used": a.tools_used,
                    "projects_worked_on": a.projects_worked_on,
                    "tech_stack_focus": a.tech_stack_focus,
                    "last_used": a.last_used.isoformat(),
                    "avg_session_duration": a.avg_session_duration,
                    "specialization_score": a.specialization_score
                }
                for a in agent_analytics
            ],
            "project_analytics": [
                {
                    "project_path": p.project_path,
                    "total_agent_calls": p.total_agent_calls,
                    "unique_agents_used": p.unique_agents_used,
                    "primary_tech_stack": p.primary_tech_stack,
                    "success_rate": p.success_rate,
                    "total_tokens": p.total_tokens,
                    "active_days": p.active_days,
                    "last_activity": p.last_activity.isoformat()
                }
                for p in project_analytics
            ],
            "raw_invocations": len(self.invocations),
            "raw_sessions": len(self.session_metrics)
        }
        
        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)
        
        print(f"📊 Analytics data exported to: {output_file}")
        return export_data


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Elite Agent Usage Analytics - Comprehensive analysis of your Claude Code agent usage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyze_agent_usage.py                    # Show comprehensive report
  python analyze_agent_usage.py --xp-leaderboard   # Show XP-based leaderboard
  python analyze_agent_usage.py --squads           # Show squad formations
  python analyze_agent_usage.py --insights         # Get usage insights
  python analyze_agent_usage.py --tech-stack       # Show tech stack analysis  
  python analyze_agent_usage.py --projects         # Show project activity
  python analyze_agent_usage.py --export data.json # Export to JSON file
  
Quick Access via Squad Command:
  squad stats                                      # Comprehensive analytics
  squad leaderboard                                # XP leaderboard
  squad squads                                     # Squad formations
  squad insights                                   # Usage insights
        """
    )
    
    parser.add_argument("--leaderboard", action="store_true", 
                       help="Show agent leaderboard only")
    parser.add_argument("--xp-leaderboard", action="store_true",
                       help="Show enhanced XP-based leaderboard")
    parser.add_argument("--squads", action="store_true",
                       help="Show squad formations analysis")
    parser.add_argument("--insights", action="store_true",
                       help="Show usage insights and recommendations")
    parser.add_argument("--tech-stack", action="store_true",
                       help="Show tech stack mastery report")  
    parser.add_argument("--projects", action="store_true",
                       help="Show project activity report")
    parser.add_argument("--export", type=str, metavar="FILE",
                       help="Export analytics data to JSON file")
    parser.add_argument("--raw", action="store_true",
                       help="Show raw invocation data")
    
    args = parser.parse_args()
    
    # Initialize analytics engine
    print("🚀 Initializing Elite Agent Analytics Engine...")
    analytics = EliteAgentAnalytics()
    
    try:
        if args.export:
            analytics.export_analytics_data(args.export)
        elif args.leaderboard:
            print(analytics.generate_leaderboard_report())
        elif args.xp_leaderboard:
            print(analytics.generate_xp_leaderboard_report())
        elif args.squads:
            print(analytics.generate_squad_formations_report())
        elif args.insights:
            print(analytics.generate_insights_report())
        elif args.tech_stack:
            print(analytics.generate_tech_stack_report())
        elif args.projects:
            print(analytics.generate_project_activity_report())
        elif args.raw:
            print(f"Raw data: {len(analytics.invocations)} basic + {len(analytics.agent_invocations)} enhanced invocations")
            print(f"Sessions: {len(analytics.session_metrics)}, Squad formations: {len(analytics.squad_formations)}")
            for inv in analytics.agent_invocations[:10]:
                collab = f" (+{len(inv.collaboration_agents)} collab)" if inv.collaboration_agents else ""
                print(f"  {inv.timestamp.strftime('%m-%d %H:%M')} | {inv.agent_name} | {inv.project_path.split('/')[-1]} | {'✓' if inv.success else '✗'}{collab}")
        else:
            # Show comprehensive report
            print(analytics.generate_comprehensive_report())
    
    except Exception as e:
        print(f"❌ Error generating analytics: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()