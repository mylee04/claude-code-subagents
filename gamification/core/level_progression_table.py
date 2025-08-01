#!/usr/bin/env python3
"""
SubAgents Achievement Progression Table
Shows XP requirements, tier unlocks, and achievement milestones
"""

def calculate_level_thresholds():
    """Get XP thresholds from achievement system"""
    from xp_system_redesign import XPSystemRedesign
    redesign = XPSystemRedesign()
    return redesign.level_thresholds

def get_tier_unlocks(tier_name):
    """Get tier-specific unlocks and bonuses"""
    tier_unlocks = {
        "Novice": ["Basic XP tracking", "Daily login bonuses", "Simple task multipliers"],
        "Adept": ["Streak bonuses (7-day, 30-day)", "Performance multipliers", "Complex task recognition"],
        "Expert": ["Multi-tool combo bonuses", "Architecture project rewards", "Advanced performance tracking"],
        "Master": ["Elite achievement badges", "Maximum performance multipliers", "Legendary task bonuses"],
        "Grandmaster": ["Prestige recognition", "Ultimate achievement status", "Special leaderboard placement"],
        "Legend": ["Mythical status", "Exclusive recognition", "Ultimate bragging rights"]
    }
    return tier_unlocks.get(tier_name, [])

def get_tier_info(level):
    """Get tier name and information for a level"""
    if level <= 10:
        return {"tier": "Novice", "tier_range": "1-10", "color": "🟢"}
    elif level <= 30:
        return {"tier": "Adept", "tier_range": "11-30", "color": "🔵"}
    elif level <= 70:
        return {"tier": "Expert", "tier_range": "31-70", "color": "🟡"}
    elif level <= 120:
        return {"tier": "Master", "tier_range": "71-120", "color": "🟠"}
    elif level <= 200:
        return {"tier": "Grandmaster", "tier_range": "121-200", "color": "🔴"}
    else:
        return {"tier": "Legend", "tier_range": "201+", "color": "💎"}

def display_full_progression_table():
    """Display the complete achievement progression table"""
    thresholds = calculate_level_thresholds()
    
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                      ELITE SQUAD ACHIEVEMENT PROGRESSION                    ║")
    print("║                           XP Requirements & Rewards                          ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    current_tier = ""
    for level in range(1, min(len(thresholds), 51)):  # Show first 50 levels in detail
        tier_info = get_tier_info(level)
        xp_required = thresholds[level - 1] if level > 1 else 0
        
        if level == 1:
            xp_to_next = thresholds[1] - 0
        elif level < len(thresholds):
            xp_to_next = thresholds[level] - thresholds[level - 1]
        else:
            xp_to_next = "MAX"
        
        # Print tier header when changing tiers
        if tier_info["tier"] != current_tier:
            current_tier = tier_info["tier"]
            print(f"║                                                                              ║")
            print(f"║ {tier_info['color']} {tier_info['tier'].upper()} TIER ({tier_info['tier_range']})                                                     ║")
            print(f"║ {'─' * 76} ║")
        
        # Format the level line
        level_str = f"Lv.{level:<3}"
        xp_str = f"{xp_required:,}" if xp_required > 0 else "0"
        next_str = f"{xp_to_next:,}" if isinstance(xp_to_next, int) else xp_to_next
        
        print(f"║ {level_str} │ Total XP: {xp_str:>12} │ XP to Next: {next_str:>10} │ {tier_info['color']} {tier_info['tier']:<12} ║")
    
    # Show milestone levels for higher tiers
    print(f"║                                                                              ║")
    print(f"║ ⚡ KEY MILESTONES IN HIGHER TIERS:                                          ║")
    print(f"║ {'─' * 76} ║")
    
    milestone_levels = [60, 70, 100, 120, 150, 200, 220, 250]
    for level in milestone_levels:
        if level < len(thresholds):
            tier_info = get_tier_info(level)
            xp_required = thresholds[level - 1]
            level_str = f"Lv.{level:<3}"
            xp_str = f"{xp_required:,}"
            print(f"║ {level_str} │ Total XP: {xp_str:>12} │ {tier_info['color']} {tier_info['tier']:<12}                      ║")
    
    print("╚══════════════════════════════════════════════════════════════════════════════╝")

def display_tier_summary():
    """Display achievement tiers with unlocks and XP ranges"""
    print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                         ACHIEVEMENT TIER BREAKDOWN                          ║")
    print("║                        Unlocks & XP Requirements                            ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    thresholds = calculate_level_thresholds()
    
    tiers = [
        {"name": "Novice", "range": "1-10", "color": "🟢", "xp_range": "0 - 7,500 XP"},
        {"name": "Adept", "range": "11-30", "color": "🔵", "xp_range": "7,500 - 60,000 XP"},
        {"name": "Expert", "range": "31-70", "color": "🟡", "xp_range": "60,000 - 300,000 XP"},
        {"name": "Master", "range": "71-120", "color": "🟠", "xp_range": "300,000 - 800,000 XP"},
        {"name": "Grandmaster", "range": "121-200", "color": "🔴", "xp_range": "800,000 - 2,000,000 XP"},
        {"name": "Legend", "range": "201+", "color": "💎", "xp_range": "2,000,000+ XP"}
    ]
    
    for tier in tiers:
        print(f"║                                                                              ║")
        print(f"║ {tier['color']} {tier['name'].upper():<12} TIER (Levels {tier['range']:<8})                                ║")
        print(f"║   XP Range: {tier['xp_range']:<62} ║")
        print(f"║   Unlocks:                                                                   ║")
        
        unlocks = get_tier_unlocks(tier['name'])
        for unlock in unlocks:
            print(f"║   • {unlock:<70} ║")
    
    print("║                                                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")

def calculate_time_estimates():
    """Calculate estimated time to reach each tier"""
    print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                         TIME TO ACHIEVEMENT ESTIMATES                       ║")
    print("║                    (Based on 800 XP per day realistic usage)                ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    thresholds = calculate_level_thresholds()
    daily_xp = 800  # Realistic XP per day for regular user
    
    milestones = [
        {"level": 10, "name": "Novice Mastery"},
        {"level": 30, "name": "Adept Status"},
        {"level": 70, "name": "Expert Tier"},
        {"level": 120, "name": "Master Rank"},
        {"level": 200, "name": "Grandmaster"},
        {"level": 220, "name": "Legend Entry"}
    ]
    
    for milestone in milestones:
        if milestone["level"] < len(thresholds):
            xp_needed = thresholds[milestone["level"] - 1]
            days = xp_needed // daily_xp
            weeks = days // 7
            months = days // 30
            
            print(f"║ {milestone['name']:<20} (Lv.{milestone['level']:<3}): {xp_needed:>10,} XP                      ║")
            if months > 0:
                print(f"║   Estimated time: ~{months} months ({days} days)                              ║")
            elif weeks > 0:
                print(f"║   Estimated time: ~{weeks} weeks ({days} days)                                ║")
            else:
                print(f"║   Estimated time: ~{days} days                                             ║")
            print(f"║                                                                              ║")
    
    print("╚══════════════════════════════════════════════════════════════════════════════╝")

def show_milestone_achievements():
    """Show key milestone achievements and their XP requirements"""
    print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                          MILESTONE ACHIEVEMENTS                             ║")
    print("║                        Key Progression Landmarks                            ║")
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    
    thresholds = calculate_level_thresholds()
    
    milestones = [
        {"level": 10, "name": "Novice Master", "achievement": "Completed basic training"},
        {"level": 30, "name": "Adept Status", "achievement": "Unlocked advanced features"},
        {"level": 70, "name": "Expert Tier", "achievement": "Mastered complex workflows"},
        {"level": 120, "name": "Master Rank", "achievement": "Achieved elite performance"},
        {"level": 200, "name": "Grandmaster", "achievement": "Legendary status attained"},
        {"level": 250, "name": "Legend Entry", "achievement": "Ultimate mastery achieved"}
    ]
    
    print("║                                                                              ║")
    for milestone in milestones:
        if milestone["level"] < len(thresholds):
            xp_needed = thresholds[milestone["level"] - 1]
            tier_info = get_tier_info(milestone["level"])
            print(f"║ {tier_info['color']} {milestone['name']:<18} (Lv.{milestone['level']:<3}): {xp_needed:>12,} XP             ║")
            print(f"║   → {milestone['achievement']:<66} ║")
            print("║                                                                              ║")
    
    print("╠══════════════════════════════════════════════════════════════════════════════╣")
    print("║                                                                              ║")
    print("║ 🎆 ACHIEVEMENT PHILOSOPHY:                                                  ║")
    print("║ ─────────────────────────────────────────────────────────────────────── ║")
    print("║ • Every level is an achievement, not a deadline                             ║")
    print("║ • Progress is measured by unlocks and capabilities, not time               ║")
    print("║ • Celebrate the journey: each tier brings new possibilities                 ║")
    print("║ • XP reflects mastery: higher tiers = deeper system understanding          ║")
    print("║                                                                              ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "full":
            display_full_progression_table()
        elif command == "tiers":
            display_tier_summary()
        elif command == "guide":
            show_xp_earning_guide()
        elif command == "milestones":
            show_milestone_achievements()
        elif command == "all":
            display_tier_summary()
            show_xp_earning_guide()
            show_milestone_achievements()
        else:
            print("Usage:")
            print("  python level_progression_table.py [command]")
            print("Commands:")
            print("  full       - Show detailed level progression table")
            print("  tiers      - Show achievement tier breakdown with unlocks")
            print("  guide      - Show XP earning strategies and session examples")
            print("  milestones - Show key milestone achievements")
            print("  all        - Show everything")
    else:
        # Default: show tier summary with unlocks
        display_tier_summary()
        print("\nRun with 'all' argument to see complete achievement guide")