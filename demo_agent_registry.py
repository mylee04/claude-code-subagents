#!/usr/bin/env python3
"""
SubAgents Agent Registry Demo
A visually appealing demonstration of the AgentRegistry system
"""

import sys
import os
import time
from pathlib import Path

# Add the project root to Python path to import the registry
sys.path.insert(0, str(Path(__file__).parent))

from gamification.core.agent_registry import AgentRegistry

# ANSI Color Codes for Terminal Output
class Colors:
    # Text colors
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    
    # Background colors
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # Text styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    DIM = '\033[2m'
    
    # Reset
    RESET = '\033[0m'
    
    # Special effects
    BLINK = '\033[5m'

def print_header(title: str, subtitle: str = ""):
    """Print a fancy header with colors"""
    width = 80
    print(f"\n{Colors.CYAN}{'='*width}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.WHITE}{title.center(width)}{Colors.RESET}")
    if subtitle:
        print(f"{Colors.DIM}{subtitle.center(width)}{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*width}{Colors.RESET}\n")

def print_section(title: str):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.YELLOW}🔸 {title}{Colors.RESET}")
    print(f"{Colors.YELLOW}{'─' * (len(title) + 3)}{Colors.RESET}")

def print_subsection(title: str):
    """Print a subsection header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}  ▸ {title}{Colors.RESET}")

def print_success(message: str):
    """Print a success message"""
    print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

def print_info(message: str):
    """Print an info message"""
    print(f"{Colors.CYAN}ℹ {message}{Colors.RESET}")

def print_warning(message: str):
    """Print a warning message"""
    print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

def print_stat(label: str, value: str, color: str = Colors.WHITE):
    """Print a statistic with nice formatting"""
    print(f"  {Colors.BOLD}{color}{label:.<25} {value}{Colors.RESET}")

def animate_dots(message: str, duration: float = 2.0):
    """Show animated loading dots"""
    print(f"{Colors.DIM}{message}", end="", flush=True)
    for _ in range(int(duration * 2)):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print(f" Done!{Colors.RESET}")

def demo_agent_discovery():
    """Demonstrate agent discovery with visual feedback"""
    print_section("🔍 AGENT DISCOVERY")
    
    animate_dots("Initializing Agent Registry", 1.5)
    registry = AgentRegistry()
    
    animate_dots("Scanning agent directories", 2.0)
    agents = registry.discover_agents(force_refresh=True)
    
    print_success(f"Successfully discovered {len(agents)} agents")
    
    # Show discovery statistics
    print_subsection("Discovery Statistics")
    categories = registry.get_categories()
    tech_stacks = registry.get_tech_stacks()
    
    print_stat("Total Agents Found", str(len(agents)), Colors.GREEN)
    print_stat("Categories Discovered", str(len(categories)), Colors.BLUE)
    print_stat("Tech Stacks Available", str(len(tech_stacks)), Colors.MAGENTA)
    
    return registry, agents

def demo_category_breakdown(registry: AgentRegistry):
    """Show category breakdown with visual appeal"""
    print_section("📊 CATEGORY BREAKDOWN")
    
    categories = registry.get_categories()
    
    # Category colors mapping
    category_colors = {
        'Development': Colors.GREEN,
        'Infrastructure': Colors.BLUE,
        'Quality Assurance': Colors.YELLOW,
        'Data & AI': Colors.MAGENTA,
        'Security': Colors.RED,
        'Product': Colors.CYAN,
        'Business': Colors.WHITE,
        'Coordination': Colors.BOLD + Colors.GREEN
    }
    
    max_count = 0
    category_stats = []
    
    for category in sorted(categories):
        agents = registry.get_agents_by_category(category)
        count = len(agents)
        max_count = max(max_count, count)
        category_stats.append((category, count))
    
    print()
    for category, count in category_stats:
        color = category_colors.get(category, Colors.WHITE)
        
        # Create a visual bar
        bar_length = int((count / max_count) * 20) if max_count > 0 else 0
        bar = '█' * bar_length + '░' * (20 - bar_length)
        
        print(f"  {color}{category:<20}{Colors.RESET} │{color}{bar}{Colors.RESET}│ {Colors.BOLD}{count:>2}{Colors.RESET} agents")

def demo_development_agents(registry: AgentRegistry):
    """Showcase development agents specifically"""
    print_section("💻 DEVELOPMENT AGENTS SHOWCASE")
    
    dev_agents = registry.get_agents_by_category("Development")
    
    print_info(f"Found {len(dev_agents)} development specialists")
    
    # Group by tech stack
    tech_groups = {}
    for agent in dev_agents:
        for tech in agent.tech_stack:
            if tech not in tech_groups:
                tech_groups[tech] = []
            tech_groups[tech].append(agent)
    
    print_subsection("Tech Stack Specialists")
    tech_colors = {
        'python': Colors.GREEN,
        'javascript': Colors.YELLOW,
        'golang': Colors.CYAN,
        'rust': Colors.RED,
        'sql': Colors.BLUE,
        'frontend': Colors.MAGENTA,
        'backend': Colors.GREEN,
        'testing': Colors.YELLOW
    }
    
    for tech, agents in sorted(tech_groups.items()):
        if len(agents) > 0:
            color = tech_colors.get(tech, Colors.WHITE)
            agent_names = [agent.name for agent in agents]
            print(f"  {color}◆ {tech.upper():<12}{Colors.RESET} → {Colors.DIM}{', '.join(agent_names)}{Colors.RESET}")

def demo_feature_planning(registry: AgentRegistry):
    """Demonstrate feature planning and squad recommendation"""
    print_section("🎯 FEATURE PLANNING & SQUAD RECOMMENDATION")
    
    # Simulate different project scenarios
    scenarios = [
        {
            "name": "E-Commerce Web Application",
            "type": "web-app",
            "tech_stack": ["javascript", "python", "sql", "cloud"],
            "description": "Building a full-stack e-commerce platform with modern tech"
        },
        {
            "name": "REST API Service",
            "type": "api", 
            "tech_stack": ["golang", "sql", "cloud"],
            "description": "High-performance microservice API"
        },
        {
            "name": "ML Data Pipeline",
            "type": "data-pipeline",
            "tech_stack": ["python", "sql", "cloud"],
            "description": "Machine learning data processing pipeline"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print_subsection(f"Scenario {i}: {scenario['name']}")
        print(f"  {Colors.DIM}📝 {scenario['description']}{Colors.RESET}")
        print(f"  {Colors.DIM}🛠️  Tech Stack: {', '.join(scenario['tech_stack'])}{Colors.RESET}")
        
        # Get recommended squad
        squad = registry.get_recommended_squad(scenario['type'], tuple(scenario['tech_stack']))
        
        print(f"\n  {Colors.BOLD}{Colors.GREEN}🚀 RECOMMENDED SQUAD:{Colors.RESET}")
        
        squad_roles = {
            'full-stack-architect': '🏗️  Full-Stack Architect',
            'frontend-developer': '🎨 Frontend Developer', 
            'backend-architect': '⚙️  Backend Architect',
            'test-engineer': '🧪 Test Engineer',
            'security-auditor': '🔒 Security Auditor',
            'cloud-architect': '☁️  Cloud Architect',
            'python-elite': '🐍 Python Elite',
            'golang-pro': '🔷 Golang Pro',
            'data-engineer': '📊 Data Engineer',
            'devops-engineer': '🔧 DevOps Engineer'
        }
        
        for j, agent_name in enumerate(squad, 1):
            role_display = squad_roles.get(agent_name, f"👤 {agent_name}")
            print(f"    {Colors.CYAN}{j}.{Colors.RESET} {role_display}")
        
        if i < len(scenarios):
            print()

def demo_search_capabilities(registry: AgentRegistry):
    """Demonstrate search and filtering capabilities"""
    print_section("🔎 ADVANCED SEARCH CAPABILITIES")
    
    # Search examples
    search_examples = [
        {
            "query": "python",
            "description": "Finding Python specialists"
        },
        {
            "query": "security",
            "description": "Security-focused agents"  
        },
        {
            "query": "cloud",
            "description": "Cloud expertise agents"
        }
    ]
    
    for example in search_examples:
        print_subsection(f"Search: '{example['query']}'")
        print(f"  {Colors.DIM}{example['description']}{Colors.RESET}")
        
        results = registry.search_agents(example['query'])
        
        if results:
            print(f"  {Colors.GREEN}Found {len(results)} matching agents:{Colors.RESET}")
            for agent in results[:3]:  # Show top 3
                tech_display = ', '.join(agent.tech_stack[:3]) if agent.tech_stack else 'N/A'
                print(f"    • {Colors.BOLD}{agent.name}{Colors.RESET} ({Colors.CYAN}{agent.category}{Colors.RESET}) - {Colors.DIM}{tech_display}{Colors.RESET}")
        else:
            print(f"  {Colors.YELLOW}No agents found{Colors.RESET}")
        print()

def demo_registry_stats(registry: AgentRegistry):
    """Show comprehensive registry statistics"""
    print_section("📈 REGISTRY STATISTICS")
    
    agents = registry.discover_agents()
    categories = registry.get_categories()
    tech_stacks = registry.get_tech_stacks()
    
    # Calculate some interesting stats
    total_specialties = sum(len(agent.specialties) for agent in agents.values())
    avg_specialties = total_specialties / len(agents) if agents else 0
    
    difficulty_counts = {}
    for agent in agents.values():
        diff = agent.difficulty_level
        difficulty_counts[diff] = difficulty_counts.get(diff, 0) + 1
    
    print_subsection("Overview")
    print_stat("Total Agents", str(len(agents)), Colors.GREEN)
    print_stat("Categories", str(len(categories)), Colors.BLUE)
    print_stat("Tech Stacks", str(len(tech_stacks)), Colors.MAGENTA)
    print_stat("Avg Specialties/Agent", f"{avg_specialties:.1f}", Colors.CYAN)
    
    print_subsection("Difficulty Distribution")
    for difficulty, count in sorted(difficulty_counts.items()):
        color = {
            'beginner': Colors.GREEN,
            'intermediate': Colors.YELLOW, 
            'advanced': Colors.RED,
            'expert': Colors.MAGENTA + Colors.BOLD
        }.get(difficulty, Colors.WHITE)
        
        print_stat(f"{difficulty.title()} Level", str(count), color)

def main():
    """Main demo function"""
    # Clear screen for better presentation
    os.system('clear' if os.name == 'posix' else 'cls')
    
    print_header(
        "🚀 ELITE SQUAD AGENT REGISTRY DEMO 🚀",
        "Showcasing Advanced Agent Discovery & Coordination"
    )
    
    try:
        # Run the demo sections
        registry, agents = demo_agent_discovery()
        
        demo_category_breakdown(registry)
        
        demo_development_agents(registry)
        
        demo_feature_planning(registry)
        
        demo_search_capabilities(registry)
        
        demo_registry_stats(registry)
        
        # Final summary
        print_section("✨ DEMO COMPLETE")
        print_success("Agent Registry system successfully demonstrated!")
        print_info("The registry provides comprehensive agent discovery and smart squad recommendations")
        print(f"\n{Colors.BOLD}{Colors.GREEN}🎉 Ready to assemble your elite development squad! 🎉{Colors.RESET}\n")
        
    except Exception as e:
        print(f"\n{Colors.RED}❌ Demo Error: {e}{Colors.RESET}")
        print(f"{Colors.DIM}Make sure you're running from the project root directory{Colors.RESET}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())