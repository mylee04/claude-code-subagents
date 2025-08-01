import React, { useState, useEffect } from 'react';
import { 
  AgentProfileCard, 
  AgentLeaderboard, 
  AgentXPTracker,
  AgentProfile,
  LeaderboardEntry,
  LeaderboardFilters,
  XPNotification,
  createXP,
  createUserID,
  createAchievementKey
} from '../components';

// Sample data for demonstration
const sampleAgents: AgentProfile[] = [
  {
    id: createUserID('agent-001'),
    name: 'React Arena Specialist',
    level: 4,
    currentXP: createXP(750),
    xpToNextLevel: createXP(1000),
    totalXP: createXP(3750),
    specialization: 'Gamified UI Systems',
    rank: 'Master',
    avatar: '',
    joinedAt: new Date('2024-01-15'),
    lastActive: new Date(),
    isOnline: true,
    achievements: [
      {
        id: createAchievementKey('game-master'),
        name: 'Game Master',
        description: 'Built complete gamification UI system',
        icon: '🎮',
        unlockedAt: new Date('2024-03-01'),
        xpReward: createXP(100),
        rarity: 'epic'
      },
      {
        id: createAchievementKey('speed-demon'),
        name: 'Speed Demon',
        description: 'All interactions under 100ms',
        icon: '⚡',
        unlockedAt: new Date('2024-02-15'),
        xpReward: createXP(75),
        rarity: 'rare'
      },
      {
        id: createAchievementKey('design-wizard'),
        name: 'Design Wizard',
        description: 'Created cohesive design system',
        icon: '🎨',
        unlockedAt: new Date('2024-02-01'),
        xpReward: createXP(85),
        rarity: 'rare'
      }
    ],
    recentAchievements: [
      {
        id: createAchievementKey('design-wizard'),
        name: 'Design Wizard',
        description: 'Created cohesive design system',
        icon: '🎨',
        unlockedAt: new Date('2024-02-01'),
        xpReward: createXP(85),
        rarity: 'rare'
      }
    ],
    performanceMetrics: [
      {
        label: 'Code Quality',
        value: 95,
        maxValue: 100,
        unit: '%',
        trend: 'up',
        color: '#10B981'
      },
      {
        label: 'Response Time',
        value: 85,
        maxValue: 100,
        unit: 'ms',
        trend: 'up',
        color: '#3B82F6'
      },
      {
        label: 'User Satisfaction',
        value: 98,
        maxValue: 100,
        unit: '%',
        trend: 'stable',
        color: '#8B5CF6'
      }
    ]
  },
  {
    id: createUserID('agent-002'),
    name: 'Python Elite',
    level: 5,
    currentXP: createXP(1200),
    xpToNextLevel: createXP(1500),
    totalXP: createXP(8750),
    specialization: 'Backend Architecture',
    rank: 'Grandmaster',
    avatar: '',
    joinedAt: new Date('2023-11-10'),
    lastActive: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
    isOnline: false,
    achievements: [
      {
        id: createAchievementKey('code-architect'),
        name: 'Code Architect',
        description: 'Designed scalable backend systems',
        icon: '🏗️',
        unlockedAt: new Date('2024-01-20'),
        xpReward: createXP(150),
        rarity: 'legendary'
      }
    ],
    recentAchievements: [],
    performanceMetrics: [
      {
        label: 'System Performance',
        value: 99,
        maxValue: 100,
        unit: '%',
        trend: 'up',
        color: '#F59E0B'
      }
    ]
  },
  {
    id: createUserID('agent-003'),
    name: 'DevOps Troubleshooter',
    level: 3,
    currentXP: createXP(450),
    xpToNextLevel: createXP(600),
    totalXP: createXP(2100),
    specialization: 'Infrastructure & Deployment',
    rank: 'Specialist',
    avatar: '',
    joinedAt: new Date('2024-02-01'),
    lastActive: new Date(),
    isOnline: true,
    achievements: [
      {
        id: createAchievementKey('crisis-resolver'),
        name: 'Crisis Resolver',
        description: 'Resolved critical production issues',
        icon: '🚨',
        unlockedAt: new Date('2024-03-10'),
        xpReward: createXP(120),
        rarity: 'epic'
      }
    ],
    recentAchievements: [
      {
        id: createAchievementKey('crisis-resolver'),
        name: 'Crisis Resolver',
        description: 'Resolved critical production issues',
        icon: '🚨',
        unlockedAt: new Date('2024-03-10'),
        xpReward: createXP(120),
        rarity: 'epic'
      }
    ],
    performanceMetrics: [
      {
        label: 'Uptime',
        value: 99.9,
        maxValue: 100,
        unit: '%',
        trend: 'stable',
        color: '#EF4444'
      }
    ]
  }
];

const ArenaDemo: React.FC = () => {
  const [selectedAgent, setSelectedAgent] = useState<AgentProfile | null>(sampleAgents[0]);
  const [leaderboardFilters, setLeaderboardFilters] = useState<LeaderboardFilters>({
    category: 'overall'
  });
  const [notifications, setNotifications] = useState<XPNotification[]>([]);

  // Create leaderboard entries from sample agents
  const leaderboardEntries: LeaderboardEntry[] = sampleAgents
    .sort((a, b) => b.totalXP - a.totalXP)
    .map((agent, index) => ({
      position: index + 1,
      agent,
      xpGainedToday: createXP(Math.floor(Math.random() * 100) + 10),
      xpGainedThisWeek: createXP(Math.floor(Math.random() * 500) + 50),
      levelProgress: agent.currentXP / agent.xpToNextLevel
    }));

  const handleXPUpdate = (notification: XPNotification) => {
    setNotifications(prev => [...prev, notification]);
    console.log('XP Update received:', notification);
  };

  const handleViewAgentDetails = (agentId: string) => {
    const agent = sampleAgents.find(a => a.id === agentId);
    if (agent) {
      setSelectedAgent(agent);
    }
  };

  // Simulate some XP updates for demo purposes
  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() > 0.7) { // 30% chance every 5 seconds
        const mockNotification: XPNotification = {
          id: Date.now().toString(),
          type: 'xp_gained',
          agentId: createUserID('agent-001'),
          message: 'Task completed successfully!',
          xpAmount: createXP(Math.floor(Math.random() * 50) + 10),
          timestamp: new Date()
        };
        handleXPUpdate(mockNotification);
      }
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      {/* Header */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-8">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🏆 Claude Arena Dashboard
          </h1>
          <p className="text-lg text-gray-600 mb-8">
            Gamified leaderboard for Claude Code agents
          </p>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        {/* Agent Profile Cards Grid */}
        <section>
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Featured Agents</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sampleAgents.map((agent) => (
              <AgentProfileCard
                key={agent.id}
                agent={agent}
                showFullMetrics={agent.id === selectedAgent?.id}
                onViewDetails={handleViewAgentDetails}
                className="hover:ring-2 hover:ring-blue-500 hover:ring-opacity-50"
              />
            ))}
          </div>
        </section>

        {/* Leaderboard */}
        <section>
          <AgentLeaderboard
            entries={leaderboardEntries}
            filters={leaderboardFilters}
            onFilterChange={setLeaderboardFilters}
            isLoading={false}
          />
        </section>

        {/* Real-time XP Tracker */}
        <AgentXPTracker
          agentId={createUserID('agent-001')}
          onXPUpdate={handleXPUpdate}
          enableToasts={true}
        />

        {/* Debug Panel */}
        <section className="mt-12">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Debug Information
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Recent Notifications:</h4>
                <div className="bg-gray-50 rounded p-3 max-h-40 overflow-y-auto">
                  {notifications.length === 0 ? (
                    <p className="text-gray-500 italic">No notifications yet...</p>
                  ) : (
                    notifications.slice(-5).map((notif) => (
                      <div key={notif.id} className="mb-2 pb-2 border-b border-gray-200 last:border-b-0">
                        <div className="font-medium">{notif.type}</div>
                        <div className="text-gray-600">{notif.message}</div>
                        <div className="text-xs text-gray-500">
                          {notif.timestamp.toLocaleTimeString()}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
              <div>
                <h4 className="font-medium text-gray-700 mb-2">Selected Agent:</h4>
                <div className="bg-gray-50 rounded p-3">
                  {selectedAgent ? (
                    <div>
                      <div className="font-medium">{selectedAgent.name}</div>
                      <div className="text-gray-600">Level {selectedAgent.level} {selectedAgent.rank}</div>
                      <div className="text-sm text-gray-500">
                        {selectedAgent.totalXP} total XP
                      </div>
                    </div>
                  ) : (
                    <p className="text-gray-500 italic">No agent selected</p>
                  )}
                </div>
              </div>
            </div>
          </div>
        </section>
      </div>

      {/* Agent Signature */}
      <footer className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-16 py-8 border-t border-gray-200">
        <div className="text-center text-gray-600">
          <div className="flex items-center justify-center space-x-4 mb-2">
            <span className="text-2xl">⚡</span>
            <span className="font-semibold">React Arena Specialist</span>
            <span className="text-2xl">⚡</span>
          </div>
          <div className="text-sm">
            <span className="font-medium">Level 4 Master</span> ⭐⭐⭐⭐☆ | 
            <span className="text-green-600 font-medium"> +250 XP Gained</span> | 
            <span className="ml-2">Achievements: 🎮 Game Master, ⚡ Speed Demon, 🎨 Design Wizard</span>
          </div>
          <div className="text-xs text-gray-500 mt-1">
            Specialized in Gamified UI Systems & Real-time React Components
          </div>
        </div>
      </footer>
    </div>
  );
};

export default ArenaDemo;