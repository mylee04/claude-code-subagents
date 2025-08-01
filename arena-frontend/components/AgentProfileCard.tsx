import React from 'react';
import { motion } from 'framer-motion';
import { 
  AgentProfileCardProps, 
  AgentProfile, 
  Achievement, 
  PerformanceMetric,
  AgentLevel 
} from '../types/agent';

// Level to star mapping for visual representation
const levelToStars = (level: AgentLevel): string => {
  return '⭐'.repeat(level) + '☆'.repeat(5 - level);
};

// Level to color mapping for styling
const levelColors = {
  1: 'from-gray-400 to-gray-600',
  2: 'from-green-400 to-green-600', 
  3: 'from-blue-400 to-blue-600',
  4: 'from-purple-400 to-purple-600',
  5: 'from-yellow-400 to-yellow-600'
};

const XPProgressBar: React.FC<{ current: number; total: number; level: AgentLevel }> = ({ 
  current, 
  total, 
  level 
}) => {
  const progress = Math.min((current / total) * 100, 100);
  
  return (
    <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
      <motion.div
        className={`h-full bg-gradient-to-r ${levelColors[level]} shadow-sm`}
        initial={{ width: 0 }}
        animate={{ width: `${progress}%` }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      />
      <div className="absolute inset-0 flex items-center justify-center text-xs font-semibold text-white drop-shadow-sm">
        {current.toLocaleString()} / {total.toLocaleString()} XP
      </div>
    </div>
  );
};

const AchievementBadge: React.FC<{ achievement: Achievement; isRecent?: boolean }> = ({ 
  achievement, 
  isRecent = false 
}) => {
  const rarityColors = {
    common: 'bg-gray-100 border-gray-300 text-gray-700',
    rare: 'bg-blue-100 border-blue-300 text-blue-700',
    epic: 'bg-purple-100 border-purple-300 text-purple-700',
    legendary: 'bg-yellow-100 border-yellow-300 text-yellow-700'
  };

  return (
    <motion.div
      className={`
        inline-flex items-center px-2 py-1 rounded-full text-xs font-medium border
        ${rarityColors[achievement.rarity]}
        ${isRecent ? 'ring-2 ring-yellow-400 ring-opacity-50' : ''}
      `}
      initial={isRecent ? { scale: 0, rotate: -180 } : { opacity: 0 }}
      animate={isRecent ? { scale: 1, rotate: 0 } : { opacity: 1 }}
      transition={{ duration: 0.5, type: "spring" }}
      title={achievement.description}
    >
      <span className="mr-1">{achievement.icon}</span>
      {achievement.name}
    </motion.div>
  );
};

const PerformanceChart: React.FC<{ metric: PerformanceMetric }> = ({ metric }) => {
  const progress = (metric.value / metric.maxValue) * 100;
  
  return (
    <div className="flex items-center space-x-3">
      <div className="flex-1">
        <div className="flex justify-between text-sm mb-1">
          <span className="font-medium text-gray-700">{metric.label}</span>
          <span className="text-gray-500">
            {metric.value.toLocaleString()}{metric.unit}
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-2">
          <motion.div
            className={`h-2 rounded-full`}
            style={{ backgroundColor: metric.color }}
            initial={{ width: 0 }}
            animate={{ width: `${progress}%` }}
            transition={{ duration: 0.6, ease: "easeOut" }}
          />
        </div>
      </div>
      <div className="flex items-center">
        {metric.trend === 'up' && <span className="text-green-500">↗️</span>}
        {metric.trend === 'down' && <span className="text-red-500">↘️</span>}
        {metric.trend === 'stable' && <span className="text-gray-500">➡️</span>}
      </div>
    </div>
  );
};

export const AgentProfileCard: React.FC<AgentProfileCardProps> = ({
  agent,
  showFullMetrics = false,
  onViewDetails,
  className = ''
}) => {
  const cardVariants = {
    hidden: { opacity: 0, y: 20 },
    visible: { 
      opacity: 1, 
      y: 0,
      transition: { duration: 0.5, ease: "easeOut" }
    },
    hover: {
      y: -5,
      shadow: "0 20px 40px rgba(0,0,0,0.1)",
      transition: { duration: 0.2 }
    }
  };

  return (
    <motion.div
      className={`
        bg-white rounded-xl shadow-lg border border-gray-200 p-6 
        hover:shadow-xl transition-all duration-300 cursor-pointer
        ${className}
      `}
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
      onClick={() => onViewDetails?.(agent.id)}
    >
      {/* Header Section */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="relative">
            {agent.avatar ? (
              <img
                src={agent.avatar}
                alt={agent.name}
                className="w-12 h-12 rounded-full object-cover border-2 border-gray-200"
              />
            ) : (
              <div className={`w-12 h-12 rounded-full bg-gradient-to-r ${levelColors[agent.level]} flex items-center justify-center text-white font-bold text-lg`}>
                {agent.name.charAt(0).toUpperCase()}
              </div>
            )}
            {agent.isOnline && (
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 border-2 border-white rounded-full"></div>
            )}
          </div>
          <div>
            <h3 className="text-lg font-bold text-gray-900">{agent.name}</h3>
            <p className="text-sm text-gray-600">{agent.specialization}</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-sm font-medium text-gray-700">
            Level {agent.level} {agent.rank}
          </div>
          <div className="text-lg">{levelToStars(agent.level)}</div>
        </div>
      </div>

      {/* XP Progress Section */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Experience Progress</span>
          <span className="text-sm text-gray-500">
            {((agent.currentXP / agent.xpToNextLevel) * 100).toFixed(1)}%
          </span>
        </div>
        <div className="relative">
          <XPProgressBar 
            current={agent.currentXP} 
            total={agent.xpToNextLevel} 
            level={agent.level}
          />
        </div>
        <div className="text-xs text-gray-500 mt-1 text-center">
          Total XP: {agent.totalXP.toLocaleString()}
        </div>
      </div>

      {/* Recent Achievements */}
      {agent.recentAchievements.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Recent Achievements</h4>
          <div className="flex flex-wrap gap-2">
            {agent.recentAchievements.slice(0, 3).map((achievement) => (
              <AchievementBadge 
                key={achievement.id} 
                achievement={achievement} 
                isRecent={true}
              />
            ))}
          </div>
        </div>
      )}

      {/* Performance Metrics */}
      {showFullMetrics && agent.performanceMetrics.length > 0 && (
        <div className="mb-4">
          <h4 className="text-sm font-semibold text-gray-700 mb-3">Performance Metrics</h4>
          <div className="space-y-3">
            {agent.performanceMetrics.slice(0, 3).map((metric, index) => (
              <PerformanceChart key={index} metric={metric} />
            ))}
          </div>
        </div>
      )}

      {/* Footer Stats */}
      <div className="flex justify-between items-center pt-4 border-t border-gray-100 text-xs text-gray-500">
        <span>Joined {agent.joinedAt.toLocaleDateString()}</span>
        <span>
          Active {new Date(agent.lastActive).toLocaleDateString() === new Date().toLocaleDateString() 
            ? 'today' 
            : agent.lastActive.toLocaleDateString()
          }
        </span>
      </div>
    </motion.div>
  );
};

export default AgentProfileCard;