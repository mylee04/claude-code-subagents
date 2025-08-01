#!/usr/bin/env python3
"""
SubAgents Agent Registry System
Comprehensive agent discovery, metadata management, and categorization
"""

import json
import os
import re
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass, asdict
from functools import lru_cache

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentMetadata:
    """Structured agent metadata from YAML frontmatter"""
    name: str
    description: str
    category: str
    file_path: str
    color: Optional[str] = None
    tools: Optional[str] = None
    tech_stack: List[str] = None
    specialties: List[str] = None
    difficulty_level: str = "intermediate"
    last_modified: Optional[str] = None
    file_size: int = 0
    
    def __post_init__(self):
        if self.tech_stack is None:
            self.tech_stack = []
        if self.specialties is None:
            self.specialties = []

@dataclass
class AgentStats:
    """Agent usage and performance statistics"""
    total_calls: int = 0
    successful_tasks: int = 0
    failed_tasks: int = 0
    avg_rating: float = 0.0
    last_used: Optional[str] = None
    xp: int = 0
    level: int = 1
    achievements: List[str] = None
    
    def __post_init__(self):
        if self.achievements is None:
            self.achievements = []

class AgentRegistry:
    """
    Unified agent discovery and management system
    
    Features:
    - Multi-location agent discovery
    - YAML frontmatter parsing
    - Category and tech stack filtering
    - Performance caching
    - Integration with XP tracking
    """
    
    def __init__(self, cache_timeout: int = 300):
        """
        Initialize the Agent Registry
        
        Args:
            cache_timeout: Cache expiration time in seconds (default: 5 minutes)
        """
        self.cache_timeout = cache_timeout
        self.cache_file = Path.home() / ".claude" / "agent_registry_cache.json"
        self.stats_file = Path.home() / ".claude" / "agent_stats.json"
        
        # Default agent search locations
        self.search_paths = [
            Path.cwd() / "agents",
            Path.home() / ".claude" / "agents",
            Path.cwd() / "custom_agents",
        ]
        
        # Category mappings based on directory structure
        self.category_mappings = {
            "business": "Business",
            "conductor": "Coordination", 
            "data": "Data & AI",
            "development": "Development",
            "infrastructure": "Infrastructure",
            "product": "Product",
            "quality": "Quality Assurance",
            "security": "Security"
        }
        
        # Tech stack extraction patterns
        self.tech_patterns = {
            "python": r"\b(?:python|django|fastapi|flask|pandas|numpy|pytorch)\b",
            "javascript": r"\b(?:javascript|typescript|node\.?js|react|vue|angular|next\.?js)\b",
            "golang": r"\b(?:go|golang|gin|echo|fiber)\b",
            "rust": r"\b(?:rust|cargo|tokio|actix|warp)\b",
            "java": r"\b(?:java|spring|maven|gradle|junit)\b",
            "sql": r"\b(?:sql|postgresql|mysql|sqlite|mongodb|redis)\b",
            "cloud": r"\b(?:aws|azure|gcp|docker|kubernetes|terraform)\b",
            "frontend": r"\b(?:html|css|react|vue|angular|svelte|tailwind)\b",
            "backend": r"\b(?:api|rest|graphql|microservices|database)\b",
            "devops": r"\b(?:devops|ci\/cd|jenkins|github actions|deployment)\b",
            "testing": r"\b(?:test|testing|jest|pytest|cypress|selenium)\b"
        }
        
        self._cache = {}
        self._cache_timestamp = None
        self._stats_cache = {}
        
        # Ensure directories exist
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        
    def add_search_path(self, path: Path) -> None:
        """Add additional search path for agents"""
        if path.exists() and path not in self.search_paths:
            self.search_paths.append(path)
            self._invalidate_cache()
            logger.info(f"Added search path: {path}")
    
    def _invalidate_cache(self) -> None:
        """Invalidate the internal cache"""
        self._cache = {}
        self._cache_timestamp = None
    
    def _is_cache_valid(self) -> bool:
        """Check if the cache is still valid"""
        if not self._cache or not self._cache_timestamp:
            return False
        
        elapsed = datetime.now() - self._cache_timestamp
        return elapsed.total_seconds() < self.cache_timeout
    
    def _parse_yaml_frontmatter(self, content: str) -> Tuple[Dict[str, Any], str]:
        """
        Parse YAML frontmatter from markdown content using simple regex-based parser
        
        Returns:
            Tuple of (frontmatter_dict, content_without_frontmatter)
        """
        frontmatter = {}
        body = content
        
        # Check for YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                try:
                    frontmatter = self._parse_simple_yaml(parts[1]) or {}
                    body = parts[2].strip()
                except Exception as e:
                    logger.warning(f"Failed to parse YAML frontmatter: {e}")
                    frontmatter = {}
        
        return frontmatter, body
    
    def _parse_simple_yaml(self, yaml_content: str) -> Dict[str, Any]:
        """
        Simple YAML parser for frontmatter - handles basic key-value pairs and lists
        
        Supports:
        - Simple key: value pairs
        - Lists with - items
        - Quoted and unquoted strings
        - Basic nested structures (one level)
        
        Args:
            yaml_content: Raw YAML content string
            
        Returns:
            Dictionary of parsed YAML data
        """
        result = {}
        lines = yaml_content.strip().split('\n')
        current_key = None
        current_list = None
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Handle list items
            if line.startswith('- '):
                if current_key and current_list is not None:
                    item = line[2:].strip()
                    # Remove quotes if present
                    if (item.startswith('"') and item.endswith('"')) or \
                       (item.startswith("'") and item.endswith("'")):
                        item = item[1:-1]
                    current_list.append(item)
                continue
            
            # Handle key-value pairs
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()
                
                # Check if this starts a list
                if not value:
                    current_key = key
                    current_list = []
                    result[key] = current_list
                    continue
                
                # Reset list context for new key-value pair
                current_key = None
                current_list = None
                
                # Parse the value
                parsed_value = self._parse_yaml_value(value)
                result[key] = parsed_value
        
        return result
    
    def _parse_yaml_value(self, value: str) -> Any:
        """
        Parse a single YAML value, handling different types
        
        Args:
            value: Raw value string
            
        Returns:
            Parsed value (str, int, float, bool, or None)
        """
        value = value.strip()
        
        if not value:
            return None
        
        # Handle quoted strings
        if (value.startswith('"') and value.endswith('"')) or \
           (value.startswith("'") and value.endswith("'")):
            return value[1:-1]
        
        # Handle boolean values
        if value.lower() in ('true', 'yes', 'on'):
            return True
        elif value.lower() in ('false', 'no', 'off'):
            return False
        elif value.lower() in ('null', 'none', '~'):
            return None
        
        # Handle numbers
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # Default to string
        return value
    
    def _extract_tech_stack(self, content: str) -> List[str]:
        """Extract technology stack from agent content"""
        content_lower = content.lower()
        tech_stack = []
        
        for tech, pattern in self.tech_patterns.items():
            if re.search(pattern, content_lower, re.IGNORECASE):
                tech_stack.append(tech)
        
        return list(set(tech_stack))  # Remove duplicates
    
    def _extract_specialties(self, content: str) -> List[str]:
        """Extract specialties from agent content"""
        specialties = []
        
        # Look for common specialty indicators
        specialty_patterns = [
            r"## (?:Core )?Competencies?.*?(?=##|\Z)",
            r"## (?:My )?Specialt(?:ies|y).*?(?=##|\Z)",
            r"## (?:My )?Approach.*?(?=##|\Z)",
            r"## (?:Key )?(?:Skills?|Expertise).*?(?=##|\Z)"
        ]
        
        for pattern in specialty_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                # Extract bullet points and key phrases
                lines = match.split('\n')
                for line in lines:
                    line = line.strip()
                    if line.startswith('- ') or line.startswith('* '):
                        specialty = line[2:].strip()
                        if len(specialty) < 100:  # Reasonable length limit
                            specialties.append(specialty)
        
        return specialties[:5]  # Limit to top 5 specialties
    
    def _analyze_agent_file(self, file_path: Path) -> Optional[AgentMetadata]:
        """
        Analyze a single agent file and extract metadata
        
        Args:
            file_path: Path to the agent markdown file
            
        Returns:
            AgentMetadata object or None if parsing fails
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse YAML frontmatter
            frontmatter, body = self._parse_yaml_frontmatter(content)
            
            # Extract basic info from frontmatter
            name = frontmatter.get('name', file_path.stem)
            description = frontmatter.get('description', 'No description available')
            color = frontmatter.get('color')
            tools = frontmatter.get('tools')
            
            # Determine category from file path
            category = "Uncategorized"
            for search_path in self.search_paths:
                try:
                    relative_path = file_path.relative_to(search_path)
                    if relative_path.parts:
                        category_dir = relative_path.parts[0]
                        category = self.category_mappings.get(category_dir, category_dir.title())
                        break
                except ValueError:
                    continue
            
            # Extract tech stack and specialties from content
            full_content = frontmatter.get('description', '') + ' ' + body
            tech_stack = self._extract_tech_stack(full_content)
            specialties = self._extract_specialties(body)
            
            # Determine difficulty level
            difficulty_indicators = {
                'beginner': ['simple', 'basic', 'getting started', 'intro'],
                'intermediate': ['experience', 'skilled', 'proficient'],
                'advanced': ['expert', 'master', 'elite', 'senior', 'architect'],
                'expert': ['elite', 'battle-tested', 'legendary', 'guru']
            }
            
            difficulty_level = "intermediate"  # default
            content_lower = full_content.lower()
            for level, indicators in difficulty_indicators.items():
                if any(indicator in content_lower for indicator in indicators):
                    difficulty_level = level
                    break
            
            # Get file stats
            stat = file_path.stat()
            
            return AgentMetadata(
                name=name,
                description=description,
                category=category,
                file_path=str(file_path),
                color=color,
                tools=tools,
                tech_stack=tech_stack,
                specialties=specialties,
                difficulty_level=difficulty_level,
                last_modified=datetime.fromtimestamp(stat.st_mtime).isoformat(),
                file_size=stat.st_size
            )
            
        except Exception as e:
            logger.warning(f"Failed to analyze agent file {file_path}: {e}")
            return None
    
    def discover_agents(self, force_refresh: bool = False) -> Dict[str, AgentMetadata]:
        """
        Discover all agents from configured search paths
        
        Args:
            force_refresh: Force cache refresh even if cache is valid
            
        Returns:
            Dictionary mapping agent names to AgentMetadata objects
        """
        # Check cache first
        if not force_refresh and self._is_cache_valid():
            return self._cache
        
        logger.info("Discovering agents from search paths...")
        agents = {}
        
        for search_path in self.search_paths:
            if not search_path.exists():
                logger.debug(f"Search path does not exist: {search_path}")
                continue
            
            logger.debug(f"Scanning: {search_path}")
            
            # Find all .md files recursively
            for md_file in search_path.rglob("*.md"):
                if md_file.is_file():
                    agent_metadata = self._analyze_agent_file(md_file)
                    if agent_metadata:
                        agents[agent_metadata.name] = agent_metadata
                        logger.debug(f"Discovered agent: {agent_metadata.name}")
        
        # Update cache
        self._cache = agents
        self._cache_timestamp = datetime.now()
        
        # Persist cache to disk
        self._save_cache_to_disk()
        
        logger.info(f"Discovered {len(agents)} agents")
        return agents
    
    def _save_cache_to_disk(self) -> None:
        """Save cache to disk for persistence"""
        try:
            cache_data = {
                'timestamp': self._cache_timestamp.isoformat() if self._cache_timestamp else None,
                'agents': {name: asdict(metadata) for name, metadata in self._cache.items()}
            }
            
            with open(self.cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"Failed to save cache to disk: {e}")
    
    def _load_cache_from_disk(self) -> None:
        """Load cache from disk"""
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r') as f:
                    cache_data = json.load(f)
                
                # Check if cache is recent enough
                if cache_data.get('timestamp'):
                    cache_time = datetime.fromisoformat(cache_data['timestamp'])
                    if (datetime.now() - cache_time).total_seconds() < self.cache_timeout:
                        self._cache_timestamp = cache_time
                        self._cache = {
                            name: AgentMetadata(**data) 
                            for name, data in cache_data.get('agents', {}).items()
                        }
                        logger.debug("Loaded agents from disk cache")
        except Exception as e:
            logger.warning(f"Failed to load cache from disk: {e}")
    
    def get_agents_by_category(self, category: str) -> List[AgentMetadata]:
        """Get all agents in a specific category"""
        agents = self.discover_agents()
        return [agent for agent in agents.values() if agent.category.lower() == category.lower()]
    
    def get_agents_by_tech_stack(self, tech_stack: List[str]) -> List[AgentMetadata]:
        """Get agents that work with specific technologies"""
        agents = self.discover_agents()
        matching_agents = []
        
        for agent in agents.values():
            if any(tech.lower() in [t.lower() for t in agent.tech_stack] for tech in tech_stack):
                matching_agents.append(agent)
        
        return matching_agents
    
    def search_agents(self, query: str, categories: List[str] = None, 
                     tech_stack: List[str] = None, difficulty: str = None) -> List[AgentMetadata]:
        """
        Search agents with flexible filtering
        
        Args:
            query: Search term for name/description
            categories: Filter by categories
            tech_stack: Filter by tech stack
            difficulty: Filter by difficulty level
            
        Returns:
            List of matching AgentMetadata objects
        """
        agents = self.discover_agents()
        results = []
        
        for agent in agents.values():
            # Text search
            if query:
                query_lower = query.lower()
                if (query_lower not in agent.name.lower() and 
                    query_lower not in agent.description.lower() and
                    not any(query_lower in spec.lower() for spec in agent.specialties)):
                    continue
            
            # Category filter
            if categories and agent.category not in categories:
                continue
            
            # Tech stack filter
            if tech_stack:
                if not any(tech.lower() in [t.lower() for t in agent.tech_stack] for tech in tech_stack):
                    continue
            
            # Difficulty filter
            if difficulty and agent.difficulty_level != difficulty.lower():
                continue
            
            results.append(agent)
        
        return results
    
    def get_agent_stats(self, agent_name: str) -> AgentStats:
        """Get usage statistics for an agent"""
        if not self._stats_cache:
            self._load_stats()
        
        return self._stats_cache.get(agent_name, AgentStats())
    
    def update_agent_stats(self, agent_name: str, success: bool, xp_gained: int = 0) -> None:
        """Update agent usage statistics"""
        if not self._stats_cache:
            self._load_stats()
        
        if agent_name not in self._stats_cache:
            self._stats_cache[agent_name] = AgentStats()
        
        stats = self._stats_cache[agent_name]
        stats.total_calls += 1
        stats.last_used = datetime.now().isoformat()
        
        if success:
            stats.successful_tasks += 1
        else:
            stats.failed_tasks += 1
        
        if xp_gained > 0:
            stats.xp += xp_gained
            # Simple level calculation (can be enhanced)
            stats.level = min(100, 1 + stats.xp // 100)
        
        self._save_stats()
    
    def _load_stats(self) -> None:
        """Load agent statistics from disk"""
        try:
            if self.stats_file.exists():
                with open(self.stats_file, 'r') as f:
                    stats_data = json.load(f)
                
                self._stats_cache = {
                    name: AgentStats(**data) 
                    for name, data in stats_data.items()
                }
        except Exception as e:
            logger.warning(f"Failed to load agent stats: {e}")
            self._stats_cache = {}
    
    def _save_stats(self) -> None:
        """Save agent statistics to disk"""
        try:
            stats_data = {
                name: asdict(stats) 
                for name, stats in self._stats_cache.items()
            }
            
            with open(self.stats_file, 'w') as f:
                json.dump(stats_data, f, indent=2)
                
        except Exception as e:
            logger.warning(f"Failed to save agent stats: {e}")
    
    def get_categories(self) -> List[str]:
        """Get all available agent categories"""
        agents = self.discover_agents()
        return sorted(list(set(agent.category for agent in agents.values())))
    
    def get_tech_stacks(self) -> List[str]:
        """Get all available tech stacks"""
        agents = self.discover_agents()
        tech_stacks = set()
        for agent in agents.values():
            tech_stacks.update(agent.tech_stack)
        return sorted(list(tech_stacks))
    
    def get_agent_by_name(self, name: str) -> Optional[AgentMetadata]:
        """Get specific agent by name"""
        agents = self.discover_agents()
        return agents.get(name)
    
    def get_similar_agents(self, agent_name: str, limit: int = 5) -> List[AgentMetadata]:
        """Find agents similar to the specified agent"""
        agents = self.discover_agents()
        target_agent = agents.get(agent_name)
        
        if not target_agent:
            return []
        
        similar_agents = []
        target_tech = set(target_agent.tech_stack)
        
        for name, agent in agents.items():
            if name == agent_name:
                continue
            
            # Calculate similarity score
            similarity_score = 0
            
            # Category match
            if agent.category == target_agent.category:
                similarity_score += 3
            
            # Tech stack overlap
            overlap = len(target_tech.intersection(set(agent.tech_stack)))
            similarity_score += overlap * 2
            
            # Difficulty level match
            if agent.difficulty_level == target_agent.difficulty_level:
                similarity_score += 1
            
            if similarity_score > 0:
                similar_agents.append((agent, similarity_score))
        
        # Sort by similarity score and return top results
        similar_agents.sort(key=lambda x: x[1], reverse=True)
        return [agent for agent, _ in similar_agents[:limit]]
    
    @lru_cache(maxsize=128)
    def get_recommended_squad(self, project_type: str, tech_stack: List[str]) -> List[str]:
        """
        Get recommended agent squad for a project type
        
        Args:
            project_type: Type of project (web-app, api, data-pipeline, etc.)
            tech_stack: List of technologies used
            
        Returns:
            List of recommended agent names
        """
        agents = self.discover_agents()
        
        # Define squad templates
        squad_templates = {
            "web-app": ["full-stack-architect", "frontend-developer", "backend-architect", "test-engineer"],
            "api": ["backend-architect", "api-documenter", "security-auditor", "test-engineer"],
            "data-pipeline": ["data-engineer", "python-elite", "cloud-architect", "performance-engineer"],
            "mobile-app": ["frontend-developer", "backend-architect", "cloud-architect", "test-engineer"],
            "devops": ["devops-engineer", "cloud-architect", "security-auditor", "incident-commander"],
            "ai-ml": ["ai-engineer", "data-engineer", "python-elite", "ml-engineer"]
        }
        
        base_squad = squad_templates.get(project_type, ["full-stack-architect", "test-engineer"])
        
        # Enhance squad based on tech stack
        tech_specific_agents = {
            "python": "python-elite",
            "javascript": "javascript-pro", 
            "typescript": "javascript-pro",
            "golang": "golang-pro",
            "rust": "rust-pro",
            "sql": "sql-pro",
            "react": "frontend-developer",
            "security": "security-auditor",
            "cloud": "cloud-architect",
            "devops": "devops-engineer"
        }
        
        recommended = list(base_squad)
        
        for tech in tech_stack:
            agent = tech_specific_agents.get(tech.lower())
            if agent and agent not in recommended and agent in agents:
                recommended.append(agent)
        
        return recommended[:6]  # Limit squad size
    
    def generate_registry_report(self) -> str:
        """Generate a comprehensive registry report"""
        agents = self.discover_agents()
        
        if not agents:
            return "No agents found in registry."
        
        categories = self.get_categories()
        tech_stacks = self.get_tech_stacks()
        
        report = []
        report.append("╔══════════════════════════════════════════════════════════════════════════════╗")
        report.append("║                        AGENT REGISTRY REPORT                                ║")
        report.append("╠══════════════════════════════════════════════════════════════════════════════╣")
        report.append("║                                                                              ║")
        report.append(f"║  Total Agents: {len(agents):<4}                                                   ║")
        report.append(f"║  Categories: {len(categories):<4}                                                     ║")
        report.append(f"║  Tech Stacks: {len(tech_stacks):<4}                                                   ║")
        report.append("║                                                                              ║")
        
        # Category breakdown
        report.append("║  📊 CATEGORY BREAKDOWN:                                                     ║")
        report.append("║  ─────────────────────────────────────────────────────────────────────── ║")
        
        for category in categories:
            category_agents = self.get_agents_by_category(category)
            report.append(f"║  • {category:<25}: {len(category_agents):>3} agents                            ║")
        
        report.append("║                                                                              ║")
        
        # Tech stack breakdown
        report.append("║  🛠️  TOP TECH STACKS:                                                       ║")
        report.append("║  ─────────────────────────────────────────────────────────────────────── ║")
        
        tech_counts = {}
        for agent in agents.values():
            for tech in agent.tech_stack:
                tech_counts[tech] = tech_counts.get(tech, 0) + 1
        
        top_tech = sorted(tech_counts.items(), key=lambda x: x[1], reverse=True)[:8]
        for tech, count in top_tech:
            report.append(f"║  • {tech:<15}: {count:>3} agents                                            ║")
        
        report.append("║                                                                              ║")
        report.append("╚══════════════════════════════════════════════════════════════════════════════╝")
        
        return "\n".join(report)

    def __init_cache__(self):
        """Initialize cache from disk on startup"""
        self._load_cache_from_disk()


# CLI Interface
if __name__ == "__main__":
    import sys
    
    registry = AgentRegistry()
    
    if len(sys.argv) < 2:
        print("Usage: python agent_registry.py [command] [args]")
        print("Commands:")
        print("  discover                     - Discover all agents")
        print("  search <query>               - Search agents by name/description")  
        print("  category <category>          - List agents by category")
        print("  tech <tech_stack>            - List agents by tech stack")
        print("  report                       - Generate registry report")
        print("  similar <agent_name>         - Find similar agents")
        print("  squad <project_type> <tech>  - Get recommended squad")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "discover":
        agents = registry.discover_agents(force_refresh=True)
        print(f"Discovered {len(agents)} agents:")
        for name in sorted(agents.keys()):
            agent = agents[name]
            print(f"  • {name:<25} ({agent.category})")
    
    elif command == "search" and len(sys.argv) >= 3:
        query = sys.argv[2]
        results = registry.search_agents(query)
        print(f"Search results for '{query}':")
        for agent in results:
            print(f"  • {agent.name:<25} - {agent.description[:60]}...")
    
    elif command == "category" and len(sys.argv) >= 3:
        category = sys.argv[2]
        agents = registry.get_agents_by_category(category)
        print(f"Agents in category '{category}':")
        for agent in agents:
            print(f"  • {agent.name:<25} - {agent.description[:60]}...")
    
    elif command == "tech" and len(sys.argv) >= 3:
        tech = sys.argv[2].split(',')
        agents = registry.get_agents_by_tech_stack(tech)
        print(f"Agents with tech stack {tech}:")
        for agent in agents:
            print(f"  • {agent.name:<25} - Tech: {', '.join(agent.tech_stack)}")
    
    elif command == "report":
        print(registry.generate_registry_report())
    
    elif command == "similar" and len(sys.argv) >= 3:
        agent_name = sys.argv[2]
        similar = registry.get_similar_agents(agent_name)
        print(f"Agents similar to '{agent_name}':")
        for agent in similar:
            print(f"  • {agent.name:<25} ({agent.category}) - {', '.join(agent.tech_stack)}")
    
    elif command == "squad" and len(sys.argv) >= 4:
        project_type = sys.argv[2]
        tech_stack = sys.argv[3].split(',')
        squad = registry.get_recommended_squad(project_type, tuple(tech_stack))
        print(f"Recommended squad for {project_type} with {tech_stack}:")
        for agent_name in squad:
            print(f"  • {agent_name}")
    
    else:
        print("Invalid command or missing arguments")