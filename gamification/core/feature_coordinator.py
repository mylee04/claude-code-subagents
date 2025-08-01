#!/usr/bin/env python3
"""
SubAgents Feature Coordinator
Runtime coordination, agent recommendation, and team formation system
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum

from agent_registry import AgentRegistry, AgentMetadata
from agents_tracker import AgentsTracker

# Configure logging
logging.basicConfig(level=logging.INFO)  
logger = logging.getLogger(__name__)

class TaskComplexity(Enum):
    SIMPLE = "simple"
    MEDIUM = "medium" 
    COMPLEX = "complex"
    MISSION = "mission"

class CoordinationStatus(Enum):
    PLANNING = "planning"
    COORDINATING = "coordinating"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Task:
    """Individual task within a feature"""
    id: str
    description: str
    complexity: TaskComplexity
    required_agent_categories: List[str]
    preferred_agents: List[str] = None
    dependencies: List[str] = None
    estimated_duration: int = 30  # minutes
    status: str = "pending"
    assigned_agent: str = None
    result: Dict = None
    
    def __post_init__(self):
        if self.preferred_agents is None:
            self.preferred_agents = []
        if self.dependencies is None:
            self.dependencies = []
        if self.result is None:
            self.result = {}

@dataclass 
class FeaturePlan:
    """Complete feature development plan"""
    id: str
    name: str
    description: str
    project_type: str
    tech_stack: List[str]
    tasks: List[Task]
    recommended_squad: List[str]
    coordination_status: CoordinationStatus
    created_at: str
    estimated_total_duration: int = 0
    actual_duration: int = 0
    success_rate: float = 0.0
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()

class FeatureCoordinator:
    """
    Runtime coordination system for multi-agent feature development
    
    Features:
    - Intelligent agent recommendation
    - Dynamic squad formation
    - Task dependency management
    - Real-time coordination
    - XP tracking integration
    - Performance analytics
    """
    
    def __init__(self):
        self.registry = AgentRegistry()
        self.tracker = SquadTracker()
        
        self.plans_file = Path.home() / ".claude" / "feature_plans.json"
        self.coordination_log = Path.home() / ".claude" / "coordination.log"
        
        # Ensure directories exist
        self.plans_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Active plans cache
        self._active_plans = {}
        self._load_plans()
        
        # Task templates for different project types
        self.task_templates = {
            "web-app": [
                {
                    "description": "Design system architecture and component structure",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Development"],
                    "preferred": ["full-stack-architect", "backend-architect"]
                },
                {
                    "description": "Design and implement backend API endpoints",
                    "complexity": TaskComplexity.COMPLEX, 
                    "categories": ["Development"],
                    "preferred": ["backend-architect", "python-elite", "javascript-pro"]
                },
                {
                    "description": "Implement frontend components and user interface",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Development"],
                    "preferred": ["frontend-developer", "javascript-pro"]
                },
                {
                    "description": "Set up database schema and data models",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Development"],
                    "preferred": ["database-optimizer", "sql-pro"]
                },
                {
                    "description": "Implement authentication and security measures", 
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Security", "Development"],
                    "preferred": ["security-auditor", "backend-architect"]
                },
                {
                    "description": "Write comprehensive tests and quality assurance",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Quality Assurance"],
                    "preferred": ["test-engineer", "quality-engineer"]
                },
                {
                    "description": "Set up deployment pipeline and infrastructure",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Infrastructure"],
                    "preferred": ["devops-engineer", "cloud-architect"]
                }
            ],
            "api": [
                {
                    "description": "Design RESTful API architecture and endpoints",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Development"],
                    "preferred": ["backend-architect", "api-documenter"]
                },
                {
                    "description": "Implement API business logic and data access",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Development"],
                    "preferred": ["python-elite", "golang-pro", "javascript-pro"]
                },
                {
                    "description": "Set up authentication and authorization",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Security"],
                    "preferred": ["security-auditor"]
                },  
                {
                    "description": "Create comprehensive API documentation",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Product"],
                    "preferred": ["api-documenter"]
                },
                {
                    "description": "Implement rate limiting and performance optimization",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Quality Assurance"],
                    "preferred": ["performance-engineer"]
                },
                {
                    "description": "Write API tests and integration tests",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Quality Assurance"],
                    "preferred": ["test-engineer"]
                }
            ],
            "data-pipeline": [
                {
                    "description": "Design data pipeline architecture and flow",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Data & AI"],
                    "preferred": ["data-engineer", "ai-engineer"]
                },
                {
                    "description": "Implement data ingestion and processing logic",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Data & AI", "Development"],
                    "preferred": ["data-engineer", "python-elite"]
                },
                {
                    "description": "Set up data storage and warehousing",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Infrastructure"],
                    "preferred": ["database-optimizer", "cloud-architect"]
                },
                {
                    "description": "Implement data validation and quality checks",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Quality Assurance"],
                    "preferred": ["test-engineer", "data-engineer"]
                },
                {
                    "description": "Create monitoring and alerting system",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Infrastructure"],
                    "preferred": ["devops-engineer", "incident-commander"]
                }
            ],
            "ai-ml": [
                {
                    "description": "Design ML model architecture and data flow",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Data & AI"],
                    "preferred": ["ai-engineer", "ml-engineer"]
                },
                {
                    "description": "Implement data preprocessing and feature engineering",
                    "complexity": TaskComplexity.COMPLEX,  
                    "categories": ["Data & AI"],
                    "preferred": ["data-engineer", "ai-engineer"]
                },
                {
                    "description": "Train and optimize ML models",
                    "complexity": TaskComplexity.COMPLEX,
                    "categories": ["Data & AI"],
                    "preferred": ["ml-engineer", "ai-engineer"]
                },
                {
                    "description": "Create model serving infrastructure", 
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Infrastructure", "Development"],
                    "preferred": ["cloud-architect", "python-elite"]
                },
                {
                    "description": "Implement model monitoring and evaluation",
                    "complexity": TaskComplexity.MEDIUM,
                    "categories": ["Quality Assurance"],
                    "preferred": ["performance-engineer", "ai-engineer"]
                }
            ]
        }
    
    def _load_plans(self) -> None:
        """Load existing feature plans from disk"""
        try:
            if self.plans_file.exists():
                with open(self.plans_file, 'r') as f:
                    plans_data = json.load(f)
                
                for plan_id, plan_data in plans_data.items():
                    # Reconstruct Task objects
                    tasks = []
                    for task_data in plan_data.get('tasks', []):
                        task_data['complexity'] = TaskComplexity(task_data['complexity'])
                        tasks.append(Task(**task_data))
                    
                    plan_data['tasks'] = tasks
                    plan_data['coordination_status'] = CoordinationStatus(
                        plan_data['coordination_status']
                    )
                    
                    self._active_plans[plan_id] = FeaturePlan(**plan_data)
                    
        except Exception as e:
            logger.warning(f"Failed to load feature plans: {e}")
            self._active_plans = {}
    
    def _save_plans(self) -> None:
        """Save feature plans to disk"""
        try:
            plans_data = {}
            for plan_id, plan in self._active_plans.items():
                plan_dict = asdict(plan)
                # Convert enums to strings for JSON serialization
                plan_dict['coordination_status'] = plan.coordination_status.value
                for task_dict in plan_dict['tasks']:
                    task_dict['complexity'] = task_dict['complexity'].value
                
                plans_data[plan_id] = plan_dict
            
            with open(self.plans_file, 'w') as f:
                json.dump(plans_data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"Failed to save feature plans: {e}")
    
    def analyze_feature_request(self, description: str, tech_stack: List[str] = None, 
                               project_type: str = None) -> Dict[str, Any]:
        """
        Analyze a feature request and provide recommendations
        
        Args:
            description: Natural language feature description
            tech_stack: List of technologies (optional, will be inferred)
            project_type: Type of project (optional, will be inferred)
            
        Returns:
            Analysis results with recommendations
        """
        if tech_stack is None:
            tech_stack = []
        
        # Infer project type if not provided
        if not project_type:
            project_type = self._infer_project_type(description)
        
        # Infer tech stack if not provided
        if not tech_stack:
            tech_stack = self._infer_tech_stack(description)
        
        # Get recommended squad
        recommended_squad = self.registry.get_recommended_squad(project_type, tuple(tech_stack))
        
        # Analyze complexity
        complexity_score = self._analyze_complexity(description)
        
        # Estimate duration
        estimated_duration = self._estimate_duration(project_type, complexity_score)
        
        return {
            "project_type": project_type,
            "tech_stack": tech_stack,
            "recommended_squad": recommended_squad,
            "complexity_score": complexity_score,
            "estimated_duration": estimated_duration,
            "task_breakdown": self._suggest_task_breakdown(project_type, complexity_score)
        }
    
    def _infer_project_type(self, description: str) -> str:
        """Infer project type from description"""
        description_lower = description.lower()
        
        patterns = {
            "web-app": ["web app", "website", "frontend", "ui", "user interface", "dashboard"],
            "api": ["api", "rest", "endpoint", "service", "microservice", "backend"],
            "data-pipeline": ["data", "pipeline", "etl", "analytics", "warehouse", "processing"],
            "ai-ml": ["ai", "ml", "machine learning", "model", "prediction", "classification"],
            "mobile-app": ["mobile", "ios", "android", "app store", "react native"],
            "devops": ["deploy", "infrastructure", "ci/cd", "docker", "kubernetes", "aws"]
        }
        
        for project_type, keywords in patterns.items():
            if any(keyword in description_lower for keyword in keywords):
                return project_type
        
        return "web-app"  # default
    
    def _infer_tech_stack(self, description: str) -> List[str]:
        """Infer tech stack from description"""
        description_lower = description.lower()
        tech_stack = []
        
        tech_patterns = {
            "python": ["python", "django", "fastapi", "flask"],
            "javascript": ["javascript", "js", "node", "react", "vue", "angular"],
            "typescript": ["typescript", "ts"],
            "golang": ["go", "golang"],
            "rust": ["rust"],
            "java": ["java", "spring"],
            "sql": ["sql", "database", "postgres", "mysql"],
            "cloud": ["aws", "azure", "gcp", "docker", "kubernetes"],
            "frontend": ["react", "vue", "angular", "html", "css"],
            "backend": ["api", "server", "backend"]
        }
        
        for tech, patterns in tech_patterns.items():
            if any(pattern in description_lower for pattern in patterns):
                tech_stack.append(tech)
        
        return tech_stack
    
    def _analyze_complexity(self, description: str) -> int:
        """Analyze feature complexity (1-10 scale)"""
        description_lower = description.lower()
        
        complexity_indicators = {
            1: ["simple", "basic", "small", "quick"],
            3: ["standard", "typical", "regular"],
            5: ["complex", "advanced", "multiple", "integration"],
            7: ["enterprise", "scalable", "distributed", "architecture"],
            10: ["mission-critical", "large-scale", "real-time", "high-performance"]
        }
        
        base_score = 3  # default
        
        for score, indicators in complexity_indicators.items():
            if any(indicator in description_lower for indicator in indicators):
                base_score = max(base_score, score)
        
        # Adjust based on technical keywords
        technical_keywords = [
            "authentication", "authorization", "real-time", "scalability",
            "microservices", "distributed", "machine learning", "ai",
            "data processing", "analytics", "security", "performance"
        ]
        
        technical_count = sum(1 for keyword in technical_keywords 
                            if keyword in description_lower)
        
        return min(10, base_score + technical_count)
    
    def _estimate_duration(self, project_type: str, complexity_score: int) -> int:
        """Estimate development duration in hours"""
        base_durations = {
            "web-app": 40,
            "api": 20,
            "data-pipeline": 30,
            "ai-ml": 50,
            "mobile-app": 60,
            "devops": 25
        }
        
        base = base_durations.get(project_type, 30)
        complexity_multiplier = 1 + (complexity_score - 3) * 0.3
        
        return int(base * complexity_multiplier)
    
    def _suggest_task_breakdown(self, project_type: str, complexity_score: int) -> List[str]:
        """Suggest task breakdown for the project"""
        template = self.task_templates.get(project_type, self.task_templates["web-app"])
        
        tasks = []
        for task_template in template:
            # Adjust complexity based on overall project complexity
            if complexity_score <= 3:
                # Simplify complex tasks for simple projects
                if task_template["complexity"] == TaskComplexity.COMPLEX:
                    tasks.append(f"Simplified: {task_template['description']}")
                else:
                    tasks.append(task_template["description"])
            elif complexity_score >= 7:
                # Add more detail for complex projects
                tasks.append(f"Advanced: {task_template['description']}")
            else:
                tasks.append(task_template["description"])
        
        return tasks
    
    def create_feature_plan(self, name: str, description: str, 
                           tech_stack: List[str] = None,
                           project_type: str = None) -> FeaturePlan:
        """
        Create a comprehensive feature development plan
        
        Args:
            name: Feature name
            description: Feature description
            tech_stack: List of technologies
            project_type: Type of project
            
        Returns:
            Complete FeaturePlan object
        """
        # Analyze the feature request
        analysis = self.analyze_feature_request(description, tech_stack, project_type)
        
        # Generate unique plan ID
        plan_id = f"feature_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Create tasks from template
        tasks = []
        task_templates = self.task_templates.get(
            analysis["project_type"], 
            self.task_templates["web-app"]
        )
        
        for i, task_template in enumerate(task_templates):
            task_id = f"{plan_id}_task_{i+1}"
            
            task = Task(
                id=task_id,
                description=task_template["description"],
                complexity=task_template["complexity"],
                required_agent_categories=task_template["categories"],
                preferred_agents=task_template["preferred"]
            )
            
            # Set dependencies (each task depends on previous ones by default)
            if i > 0:
                task.dependencies = [f"{plan_id}_task_{i}"]
            
            tasks.append(task)
        
        # Create the feature plan
        plan = FeaturePlan(
            id=plan_id,
            name=name,
            description=description,
            project_type=analysis["project_type"],
            tech_stack=analysis["tech_stack"],
            tasks=tasks,
            recommended_squad=analysis["recommended_squad"],
            coordination_status=CoordinationStatus.PLANNING,
            created_at=datetime.now().isoformat(),
            estimated_total_duration=analysis["estimated_duration"]
        )
        
        # Store the plan
        self._active_plans[plan_id] = plan
        self._save_plans()
        
        logger.info(f"Created feature plan: {plan_id}")
        return plan
    
    def recommend_agent_squad(self, project_type: str, tech_stack: List[str], 
                             complexity: str = "medium") -> List[str]:
        """
        Convenience method to get squad recommendations without creating a full plan
        
        Args:
            project_type: Type of project (e.g., "web-app", "api", "data-pipeline", "ai-ml")
            tech_stack: List of technologies being used
            complexity: Complexity level ("simple", "medium", "complex", "mission")
            
        Returns:
            List of recommended agent names for the squad
        """
        # Create a temporary feature description for analysis
        complexity_descriptions = {
            "simple": "A simple, straightforward project with basic requirements",
            "medium": "A standard project with typical complexity and multiple components",
            "complex": "A complex project with advanced features and integrations",
            "mission": "A mission-critical project with enterprise-scale requirements"
        }
        
        temp_description = f"A {complexity} {project_type} project using {', '.join(tech_stack)}. {complexity_descriptions.get(complexity, '')}"
        
        # Use the existing analysis method to get recommendations
        analysis = self.analyze_feature_request(
            description=temp_description,
            tech_stack=tech_stack,
            project_type=project_type
        )
        
        return analysis["recommended_squad"]
    
    def get_next_task(self, plan_id: str) -> Optional[Task]:
        """Get the next available task for execution"""
        plan = self._active_plans.get(plan_id)
        if not plan:
            return None
        
        for task in plan.tasks:
            if task.status == "pending":
                # Check if dependencies are completed
                if all(self._is_task_completed(plan, dep_id) for dep_id in task.dependencies):
                    return task
        
        return None
    
    def _is_task_completed(self, plan: FeaturePlan, task_id: str) -> bool:
        """Check if a task is completed"""
        for task in plan.tasks:
            if task.id == task_id:
                return task.status == "completed"
        return False
    
    def recommend_agent_for_task(self, task: Task, exclude_busy: bool = True) -> List[str]:
        """
        Recommend best agents for a specific task
        
        Args:
            task: Task to find agents for
            exclude_busy: Whether to exclude currently busy agents
            
        Returns:
            List of recommended agent names, ordered by suitability
        """
        recommendations = []
        
        # Start with preferred agents
        for agent_name in task.preferred_agents:
            agent = self.registry.get_agent_by_name(agent_name)
            if agent:
                stats = self.registry.get_agent_stats(agent_name)
                score = self._calculate_agent_score(agent, task, stats)
                recommendations.append((agent_name, score))
        
        # Add agents from required categories
        for category in task.required_agent_categories:
            category_agents = self.registry.get_agents_by_category(category)
            for agent in category_agents:
                if agent.name not in [r[0] for r in recommendations]:
                    stats = self.registry.get_agent_stats(agent.name)
                    score = self._calculate_agent_score(agent, task, stats)
                    recommendations.append((agent.name, score))
        
        # Sort by score (higher is better)
        recommendations.sort(key=lambda x: x[1], reverse=True)
        
        return [agent_name for agent_name, _ in recommendations[:5]]
    
    def _calculate_agent_score(self, agent: AgentMetadata, task: Task, stats) -> float:
        """Calculate suitability score for an agent-task pairing"""
        score = 0.0
        
        # Base score from success rate
        if stats.total_calls > 0:
            success_rate = stats.successful_tasks / stats.total_calls
            score += success_rate * 40
        else:
            score += 20  # No history, neutral score
        
        # Level bonus
        score += min(stats.level * 2, 20)
        
        # Preferred agent bonus
        if agent.name in task.preferred_agents:
            score += 30
        
        # Category match bonus
        if agent.category in task.required_agent_categories:
            score += 20
        
        # Complexity match
        complexity_levels = {
            TaskComplexity.SIMPLE: ["beginner", "intermediate"],
            TaskComplexity.MEDIUM: ["intermediate", "advanced"],
            TaskComplexity.COMPLEX: ["advanced", "expert"],
            TaskComplexity.MISSION: ["expert"]
        }
        
        if agent.difficulty_level in complexity_levels.get(task.complexity, []):
            score += 15
        
        # Recent usage penalty (to distribute work)
        if stats.last_used:
            last_used = datetime.fromisoformat(stats.last_used)
            hours_since = (datetime.now() - last_used).total_seconds() / 3600
            if hours_since < 1:
                score -= 10
        
        return score
    
    def assign_task(self, plan_id: str, task_id: str, agent_name: str) -> bool:
        """Assign a task to a specific agent"""
        plan = self._active_plans.get(plan_id)
        if not plan:
            return False
        
        # Find the task
        task = None
        for t in plan.tasks:
            if t.id == task_id:
                task = t
                break
        
        if not task or task.status != "pending":
            return False
        
        # Check agent exists
        agent = self.registry.get_agent_by_name(agent_name)
        if not agent:
            return False
        
        # Assign the task
        task.assigned_agent = agent_name
        task.status = "assigned"
        
        # Update plan status
        if plan.coordination_status == CoordinationStatus.PLANNING:
            plan.coordination_status = CoordinationStatus.COORDINATING
        
        self._save_plans()
        
        logger.info(f"Assigned task {task_id} to {agent_name}")
        return True
    
    def complete_task(self, plan_id: str, task_id: str, success: bool, 
                     result: Dict = None, duration_minutes: int = 0) -> bool:
        """Mark a task as completed and update statistics"""
        plan = self._active_plans.get(plan_id)
        if not plan:
            return False
        
        # Find the task
        task = None
        for t in plan.tasks:
            if t.id == task_id:
                task = t
                break
        
        if not task or task.status != "assigned":
            return False
        
        # Complete the task
        task.status = "completed" if success else "failed"
        task.result = result or {}
        
        # Update agent stats if assigned
        if task.assigned_agent:
            # Calculate XP based on task complexity
            xp_multipliers = {
                TaskComplexity.SIMPLE: 1.0,
                TaskComplexity.MEDIUM: 2.0,
                TaskComplexity.COMPLEX: 3.0,
                TaskComplexity.MISSION: 5.0
            }
            
            base_xp = 100
            xp_gained = int(base_xp * xp_multipliers[task.complexity])
            
            if success:
                xp_gained = int(xp_gained * 1.2)  # Success bonus
            
            # Track in squad tracker
            self.tracker.log_agent_call(
                agent_name=task.assigned_agent,
                task=task.description,
                success=success,
                duration_seconds=duration_minutes * 60
            )
            
            # Update registry stats
            self.registry.update_agent_stats(task.assigned_agent, success, xp_gained)
        
        # Update plan stats
        plan.actual_duration += duration_minutes
        
        # Check if all tasks are completed
        all_completed = all(t.status in ["completed", "failed"] for t in plan.tasks)
        if all_completed:
            successful_tasks = sum(1 for t in plan.tasks if t.status == "completed")
            plan.success_rate = successful_tasks / len(plan.tasks)
            
            if plan.success_rate >= 0.8:
                plan.coordination_status = CoordinationStatus.COMPLETED
            else:
                plan.coordination_status = CoordinationStatus.FAILED
        
        self._save_plans()
        
        logger.info(f"Completed task {task_id}: {'success' if success else 'failed'}")
        return True
    
    def get_plan_status(self, plan_id: str) -> Optional[Dict]:
        """Get comprehensive status of a feature plan"""
        plan = self._active_plans.get(plan_id)
        if not plan:
            return None
        
        completed_tasks = sum(1 for t in plan.tasks if t.status == "completed")
        failed_tasks = sum(1 for t in plan.tasks if t.status == "failed")
        in_progress_tasks = sum(1 for t in plan.tasks if t.status == "assigned")
        pending_tasks = sum(1 for t in plan.tasks if t.status == "pending")
        
        return {
            "plan_id": plan.id,
            "name": plan.name,
            "status": plan.coordination_status.value,
            "progress": {
                "completed": completed_tasks,
                "failed": failed_tasks,
                "in_progress": in_progress_tasks,
                "pending": pending_tasks,
                "total": len(plan.tasks)
            },
            "duration": {
                "estimated": plan.estimated_total_duration,
                "actual": plan.actual_duration
            },
            "success_rate": plan.success_rate,
            "next_task": self.get_next_task(plan_id).description if self.get_next_task(plan_id) else None
        }
    
    def get_active_plans(self) -> List[Dict]:
        """Get summary of all active plans"""
        summaries = []
        
        for plan_id, plan in self._active_plans.items():
            if plan.coordination_status not in [CoordinationStatus.COMPLETED, CoordinationStatus.FAILED]:
                status = self.get_plan_status(plan_id)
                summaries.append(status)
        
        return summaries
    
    def generate_coordination_report(self) -> str:
        """Generate comprehensive coordination report"""
        active_plans = self.get_active_plans()
        completed_plans = [p for p in self._active_plans.values() 
                          if p.coordination_status == CoordinationStatus.COMPLETED]
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                      FEATURE COORDINATION REPORT                            ║")
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append("║                                                                              ║")
        report.append(f"║  Active Plans: {len(active_plans):<4}                                                   ║")
        report.append(f"║  Completed Plans: {len(completed_plans):<4}                                             ║")
        report.append("║                                                                              ║")
        
        if active_plans:
            report.append("║  🚀 ACTIVE PLANS:                                                           ║")
            report.append("║  ─────────────────────────────────────────────────────────────────────── ║")
            
            for plan in active_plans[:5]:  # Show top 5
                name = plan["name"][:25]
                progress = plan["progress"]
                completed = progress["completed"]
                total = progress["total"]
                report.append(f"║  • {name:<25}: {completed}/{total} tasks ({plan['status']})                    ║")
        
        if completed_plans:
            report.append("║                                                                              ║")  
            report.append("║  ✅ RECENT COMPLETIONS:                                                     ║")
            report.append("║  ─────────────────────────────────────────────────────────────────────── ║")
            
            recent_completed = sorted(completed_plans, 
                                    key=lambda x: x.created_at, reverse=True)[:3]
            
            for plan in recent_completed:
                name = plan.name[:25]  
                success_rate = int(plan.success_rate * 100)
                report.append(f"║  • {name:<25}: {success_rate}% success rate                         ║")
        
        report.append("║                                                                              ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(report)


# CLI Interface
if __name__ == "__main__":
    import sys
    
    coordinator = FeatureCoordinator()
    
    if len(sys.argv) < 2:
        print("Usage: python feature_coordinator.py [command] [args]")
        print("Commands:")
        print("  analyze '<description>' [tech_stack] [project_type]  - Analyze feature request")
        print("  create '<name>' '<description>' [tech_stack]         - Create feature plan")
        print("  status <plan_id>                                     - Get plan status")
        print("  assign <plan_id> <task_id> <agent_name>              - Assign task to agent") 
        print("  complete <plan_id> <task_id> <success> [duration]    - Complete task")
        print("  plans                                                - List active plans")
        print("  report                                               - Generate coordination report")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "analyze" and len(sys.argv) >= 3:
        description = sys.argv[2]
        tech_stack = sys.argv[3].split(',') if len(sys.argv) > 3 else None
        project_type = sys.argv[4] if len(sys.argv) > 4 else None
        
        analysis = coordinator.analyze_feature_request(description, tech_stack, project_type)
        print(f"Analysis for: {description}")
        print(f"Project Type: {analysis['project_type']}")
        print(f"Tech Stack: {', '.join(analysis['tech_stack'])}")
        print(f"Complexity: {analysis['complexity_score']}/10")
        print(f"Estimated Duration: {analysis['estimated_duration']} hours")
        print(f"Recommended Squad: {', '.join(analysis['recommended_squad'])}")
    
    elif command == "create" and len(sys.argv) >= 4:
        name = sys.argv[2]
        description = sys.argv[3]
        tech_stack = sys.argv[4].split(',') if len(sys.argv) > 4 else None
        
        plan = coordinator.create_feature_plan(name, description, tech_stack)
        print(f"Created plan: {plan.id}")
        print(f"Tasks: {len(plan.tasks)}")
        print(f"Recommended Squad: {', '.join(plan.recommended_squad)}")
    
    elif command == "status" and len(sys.argv) >= 3:
        plan_id = sys.argv[2] 
        status = coordinator.get_plan_status(plan_id)
        if status:
            print(f"Plan: {status['name']} ({status['plan_id']})")
            print(f"Status: {status['status']}")
            print(f"Progress: {status['progress']['completed']}/{status['progress']['total']} tasks")
            if status['next_task']:
                print(f"Next Task: {status['next_task']}")
        else:
            print("Plan not found")
    
    elif command == "plans":
        plans = coordinator.get_active_plans()
        print("Active Feature Plans:")
        for plan in plans:
            print(f"  • {plan['name']} ({plan['plan_id']}): {plan['progress']['completed']}/{plan['progress']['total']} tasks")
    
    elif command == "report":
        print(coordinator.generate_coordination_report())
    
    else:
        print("Invalid command or missing arguments")