import React, { useState, useMemo } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  AgentLeaderboardProps, 
  LeaderboardEntry, 
  LeaderboardFilters,
  AgentLevel 
} from '../types/agent';

// Position badges for top 3 positions
const getPositionBadge = (position: number): string => {
  switch (position) {
    case 1: return '🥇';
    case 2: return '🥈';
    case 3: return '🥉';
    default: return `#${position}`;
  }
};

// Level colors for consistent styling
const levelColors = {
  1: 'from-gray-400 to-gray-600',
  2: 'from-green-400 to-green-600', 
  3: 'from-blue-400 to-blue-600',
  4: 'from-purple-400 to-purple-600',
  5: 'from-yellow-400 to-yellow-600'
};

const FilterButton: React.FC<{
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}> = ({ active, onClick, children }) => (
  <motion.button
    className={`
      px-4 py-2 rounded-lg font-medium text-sm transition-all duration-200
      ${active 
        ? 'bg-blue-500 text-white shadow-md' 
        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }
    `}
    onClick={onClick}
    whileHover={{ scale: 1.05 }}
    whileTap={{ scale: 0.95 }}
  >
    {children}
  </motion.button>
);

const LevelProgressAnimation: React.FC<{ 
  progress: number; 
  level: AgentLevel;
  showAnimation?: boolean;
}> = ({ progress, level, showAnimation = true }) => {
  return (
    <div className="w-24 bg-gray-200 rounded-full h-2 overflow-hidden">
      <motion.div
        className={`h-full bg-gradient-to-r ${levelColors[level]}`}
        initial={showAnimation ? { width: 0 } : { width: `${progress * 100}%` }}
        animate={{ width: `${progress * 100}%` }}
        transition={{ duration: showAnimation ? 1.2 : 0, ease: "easeOut" }}
      />
    </div>
  );
};

const LeaderboardRow: React.FC<{ 
  entry: LeaderboardEntry; 
  index: number;
  showAnimation: boolean;
}> = ({ entry, index, showAnimation }) => {
  const { agent, position, xpGainedToday, levelProgress } = entry;
  
  const rowVariants = {
    hidden: { opacity: 0, x: -50 },
    visible: { 
      opacity: 1, 
      x: 0,
      transition: { 
        duration: 0.5, 
        delay: showAnimation ? index * 0.1 : 0,
        ease: "easeOut" 
      }
    }
  };

  return (
    <motion.div
      className={`
        flex items-center p-4 rounded-lg border transition-all duration-300
        ${position <= 3 
          ? 'bg-gradient-to-r from-yellow-50 to-orange-50 border-yellow-200 shadow-md' 
          : 'bg-white border-gray-200 hover:bg-gray-50'
        }
      `}
      variants={rowVariants}
      initial="hidden"
      animate="visible"
      whileHover={{ y: -2, shadow: "0 8px 20px rgba(0,0,0,0.1)" }}
    >
      {/* Position */}
      <div className="flex items-center justify-center w-12 h-12 mr-4">
        <motion.div
          className={`
            text-lg font-bold
            ${position <= 3 ? 'text-2xl' : 'text-gray-600'}
          `}
          initial={showAnimation ? { scale: 0, rotate: -180 } : {}}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ duration: 0.6, delay: showAnimation ? index * 0.1 + 0.2 : 0 }}
        >
          {getPositionBadge(position)}
        </motion.div>
      </div>

      {/* Agent Info */}
      <div className="flex items-center flex-1 min-w-0">
        <div className="relative mr-3">
          {agent.avatar ? (
            <img
              src={agent.avatar}
              alt={agent.name}
              className="w-10 h-10 rounded-full object-cover border-2 border-gray-200"
            />
          ) : (
            <div className={`w-10 h-10 rounded-full bg-gradient-to-r ${levelColors[agent.level]} flex items-center justify-center text-white font-bold`}>
              {agent.name.charAt(0).toUpperCase()}
            </div>
          )}
          {agent.isOnline && (
            <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 border-2 border-white rounded-full"></div>
          )}
        </div>

        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2">
            <h3 className="font-semibold text-gray-900 truncate">{agent.name}</h3>
            <span className="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
              Lv.{agent.level}
            </span>
          </div>
          <p className="text-sm text-gray-600 truncate">{agent.specialization}</p>
        </div>
      </div>

      {/* XP Stats */}
      <div className="flex items-center space-x-6 mr-4">
        <div className="text-right">
          <div className="text-sm font-semibold text-gray-900">
            {agent.totalXP.toLocaleString()} XP
          </div>
          <div className="text-xs text-green-600">
            +{xpGainedToday.toLocaleString()} today
          </div>
        </div>

        {/* Level Progress */}
        <div className="flex flex-col items-center">
          <div className="text-xs text-gray-500 mb-1">Next Level</div>
          <LevelProgressAnimation 
            progress={levelProgress} 
            level={agent.level}
            showAnimation={showAnimation}
          />
        </div>
      </div>

      {/* Recent Achievements */}
      <div className="flex space-x-1">
        {agent.recentAchievements.slice(0, 3).map((achievement, idx) => (
          <motion.div
            key={achievement.id}
            className="text-lg"
            initial={showAnimation ? { scale: 0, rotate: -180 } : {}}
            animate={{ scale: 1, rotate: 0 }}
            transition={{ 
              duration: 0.4, 
              delay: showAnimation ? index * 0.1 + idx * 0.1 + 0.5 : 0,
              type: "spring"
            }}
            title={achievement.name}
          >
            {achievement.icon}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export const AgentLeaderboard: React.FC<AgentLeaderboardProps> = ({
  entries,
  filters,
  onFilterChange,
  isLoading = false,
  className = ''
}) => {
  const [showAnimation, setShowAnimation] = useState(true);

  // Filter entries based on current filters
  const filteredEntries = useMemo(() => {
    let filtered = [...entries];
    
    if (filters.specialization) {
      filtered = filtered.filter(entry => 
        entry.agent.specialization.toLowerCase().includes(filters.specialization!.toLowerCase())
      );
    }
    
    if (filters.level) {
      filtered = filtered.filter(entry => entry.agent.level === filters.level);
    }
    
    return filtered;
  }, [entries, filters]);

  const handleFilterChange = (newFilters: Partial<LeaderboardFilters>) => {
    onFilterChange({ ...filters, ...newFilters });
    setShowAnimation(true);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        duration: 0.3,
        staggerChildren: 0.1
      }
    }
  };

  if (isLoading) {
    return (
      <div className={`bg-white rounded-xl shadow-lg p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded mb-4 w-1/4"></div>
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-100 rounded-lg"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-white rounded-xl shadow-lg ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-gray-200">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-2xl font-bold text-gray-900">Agent Leaderboard</h2>
          <div className="text-sm text-gray-500">
            {filteredEntries.length} agents competing
          </div>
        </div>

        {/* Filters */}
        <div className="flex flex-wrap gap-3">
          <div className="flex space-x-2">
            <FilterButton
              active={filters.category === 'overall'}
              onClick={() => handleFilterChange({ category: 'overall' })}
            >
              Overall
            </FilterButton>
            <FilterButton
              active={filters.category === 'daily'}
              onClick={() => handleFilterChange({ category: 'daily' })}
            >
              Daily
            </FilterButton>
            <FilterButton
              active={filters.category === 'weekly'}
              onClick={() => handleFilterChange({ category: 'weekly' })}
            >
              Weekly
            </FilterButton>
            <FilterButton
              active={filters.category === 'monthly'}
              onClick={() => handleFilterChange({ category: 'monthly' })}
            >
              Monthly
            </FilterButton>
          </div>

          <div className="flex space-x-2">
            {[1, 2, 3, 4, 5].map(level => (
              <FilterButton
                key={level}
                active={filters.level === level}
                onClick={() => handleFilterChange({ 
                  level: filters.level === level ? undefined : level as AgentLevel 
                })}
              >
                Lv.{level}
              </FilterButton>
            ))}
          </div>
        </div>
      </div>

      {/* Leaderboard List */}
      <div className="p-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={`${filters.category}-${filters.level}-${filters.specialization}`}
            className="space-y-3"
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            onAnimationComplete={() => setShowAnimation(false)}
          >
            {filteredEntries.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                <div className="text-4xl mb-4">🏆</div>
                <p className="text-lg">No agents found matching your filters</p>
                <p className="text-sm">Try adjusting your search criteria</p>
              </div>
            ) : (
              filteredEntries.map((entry, index) => (
                <LeaderboardRow
                  key={entry.agent.id}
                  entry={entry}
                  index={index}
                  showAnimation={showAnimation}
                />
              ))
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};

export default AgentLeaderboard;