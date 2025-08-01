import React, { useState, useEffect, useCallback, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  AgentXPTrackerProps, 
  XPNotification, 
  WebSocketMessage,
  Achievement,
  AgentLevel 
} from '../types/agent';

// Toast notification component
const XPToast: React.FC<{ 
  notification: XPNotification; 
  onClose: () => void; 
}> = ({ notification, onClose }) => {
  const toastVariants = {
    hidden: { opacity: 0, y: -50, scale: 0.8 },
    visible: { 
      opacity: 1, 
      y: 0, 
      scale: 1,
      transition: { 
        type: "spring", 
        stiffness: 500, 
        damping: 30 
      }
    },
    exit: { 
      opacity: 0, 
      y: -20, 
      scale: 0.8,
      transition: { duration: 0.2 }
    }
  };

  const getToastConfig = () => {
    switch (notification.type) {
      case 'level_up':
        return {
          bg: 'from-yellow-400 to-orange-500',
          icon: '🎉',
          title: 'Level Up!',
          message: `Congratulations! You reached Level ${notification.newLevel}!`
        };
      case 'achievement_unlocked':
        return {
          bg: 'from-purple-400 to-pink-500',
          icon: notification.achievement?.icon || '🏆',
          title: 'Achievement Unlocked!',
          message: notification.achievement?.name || notification.message
        };
      case 'xp_gained':
      default:
        return {
          bg: 'from-blue-400 to-cyan-500',
          icon: '⚡',
          title: 'XP Gained!',
          message: `+${notification.xpAmount} XP earned!`
        };
    }
  };

  const config = getToastConfig();

  useEffect(() => {
    const timer = setTimeout(onClose, 4000);
    return () => clearTimeout(timer);
  }, [onClose]);

  return (
    <motion.div
      className={`fixed top-4 right-4 z-50 bg-gradient-to-r ${config.bg} text-white rounded-lg shadow-xl p-4 max-w-sm cursor-pointer`}
      variants={toastVariants}
      initial="hidden"
      animate="visible"
      exit="exit"
      onClick={onClose}
      whileHover={{ scale: 1.05 }}
    >
      <div className="flex items-start space-x-3">
        <div className="text-2xl">{config.icon}</div>
        <div className="flex-1">
          <h4 className="font-bold text-lg">{config.title}</h4>
          <p className="text-sm opacity-90">{config.message}</p>
          {notification.type === 'achievement_unlocked' && notification.achievement && (
            <div className="mt-2 text-xs opacity-75">
              +{notification.achievement.xpReward} XP • {notification.achievement.rarity}
            </div>
          )}
        </div>
        <button 
          onClick={(e) => {
            e.stopPropagation();
            onClose();
          }}
          className="text-white hover:bg-white hover:bg-opacity-20 rounded-full p-1"
        >
          ✕
        </button>
      </div>
    </motion.div>
  );
};

// Floating XP gain indicator
const XPFloatingIndicator: React.FC<{ 
  amount: number; 
  onComplete: () => void;
}> = ({ amount, onComplete }) => {
  return (
    <motion.div
      className="fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-40 pointer-events-none"
      initial={{ opacity: 0, scale: 0.5, y: 0 }}
      animate={{ 
        opacity: [0, 1, 1, 0], 
        scale: [0.5, 1.2, 1, 0.8], 
        y: [0, -50, -80, -100] 
      }}
      transition={{ 
        duration: 2,
        times: [0, 0.2, 0.8, 1],
        ease: "easeOut"
      }}
      onAnimationComplete={onComplete}
    >
      <div className="bg-green-500 text-white px-4 py-2 rounded-full font-bold text-lg shadow-lg">
        +{amount} XP
      </div>
    </motion.div>
  );
};

// Achievement unlock animation
const AchievementUnlockAnimation: React.FC<{ 
  achievement: Achievement; 
  onComplete: () => void;
}> = ({ achievement, onComplete }) => {
  return (
    <motion.div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
    >
      <motion.div
        className="bg-white rounded-xl p-8 max-w-md mx-4 text-center"
        initial={{ scale: 0, rotate: -180 }}
        animate={{ scale: 1, rotate: 0 }}
        transition={{ 
          type: "spring", 
          stiffness: 300, 
          damping: 20,
          delay: 0.2
        }}
      >
        <motion.div
          className="text-6xl mb-4"
          initial={{ scale: 0 }}
          animate={{ scale: [0, 1.3, 1] }}
          transition={{ 
            duration: 0.6, 
            delay: 0.5,
            times: [0, 0.6, 1] 
          }}
        >
          {achievement.icon}
        </motion.div>
        
        <motion.h2
          className="text-2xl font-bold text-gray-900 mb-2"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7 }}
        >
          Achievement Unlocked!
        </motion.h2>
        
        <motion.h3
          className="text-xl text-purple-600 font-semibold mb-2"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.8 }}
        >
          {achievement.name}
        </motion.h3>
        
        <motion.p
          className="text-gray-600 mb-4"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.9 }}
        >
          {achievement.description}
        </motion.p>
        
        <motion.div
          className="flex justify-center space-x-4 text-sm text-gray-500"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.0 }}
        >
          <span>+{achievement.xpReward} XP</span>
          <span>•</span>
          <span className="capitalize">{achievement.rarity}</span>
        </motion.div>
        
        <motion.button
          className="mt-6 px-6 py-2 bg-purple-500 text-white rounded-lg hover:bg-purple-600 transition-colors"
          onClick={onComplete}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 1.2 }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Awesome!
        </motion.button>
      </motion.div>
    </motion.div>
  );
};

export const AgentXPTracker: React.FC<AgentXPTrackerProps> = ({
  agentId,
  onXPUpdate,
  enableToasts = true,
  className = ''
}) => {
  const [notifications, setNotifications] = useState<XPNotification[]>([]);
  const [floatingXP, setFloatingXP] = useState<{ id: string; amount: number }[]>([]);
  const [achievementModal, setAchievementModal] = useState<Achievement | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const websocketRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const reconnectAttempts = useRef(0);

  const connectWebSocket = useCallback(() => {
    try {
      // Connect to WebSocket server (adjust URL based on your backend)
      const wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws';
      websocketRef.current = new WebSocket(`${wsUrl}/${agentId}`);
      
      websocketRef.current.onopen = () => {
        console.log('WebSocket connected for agent:', agentId);
        setIsConnected(true);
        reconnectAttempts.current = 0;
      };
      
      websocketRef.current.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          handleWebSocketMessage(message);
        } catch (error) {
          console.error('Error parsing WebSocket message:', error);
        }
      };
      
      websocketRef.current.onclose = () => {
        console.log('WebSocket disconnected');
        setIsConnected(false);
        
        // Attempt to reconnect with exponential backoff
        if (reconnectAttempts.current < 5) {
          const delay = Math.pow(2, reconnectAttempts.current) * 1000;
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectAttempts.current++;
            connectWebSocket();
          }, delay);
        }
      };
      
      websocketRef.current.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
      
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
    }
  }, [agentId]);

  const handleWebSocketMessage = useCallback((message: WebSocketMessage) => {
    const notification: XPNotification = {
      id: Date.now().toString(),
      type: message.type as any,
      agentId: message.agentId,
      message: '',
      timestamp: new Date(message.timestamp)
    };

    switch (message.type) {
      case 'xp_update':
        notification.xpAmount = message.payload.amount;
        notification.message = `Gained ${message.payload.amount} XP`;
        
        // Show floating XP indicator
        setFloatingXP(prev => [...prev, { 
          id: notification.id, 
          amount: message.payload.amount 
        }]);
        break;
        
      case 'level_up':
        notification.newLevel = message.payload.newLevel;
        notification.message = `Level up! Reached Level ${message.payload.newLevel}`;
        break;
        
      case 'achievement_unlock':
        notification.achievement = message.payload.achievement;
        notification.message = `Unlocked: ${message.payload.achievement.name}`;
        
        // Show achievement modal for significant achievements
        if (message.payload.achievement.rarity === 'epic' || message.payload.achievement.rarity === 'legendary') {
          setAchievementModal(message.payload.achievement);
        }
        break;
    }

    // Add to notifications list for toasts
    if (enableToasts) {
      setNotifications(prev => [...prev, notification]);
    }

    // Call the callback if provided
    onXPUpdate?.(notification);
  }, [enableToasts, onXPUpdate]);

  const removeNotification = useCallback((id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  }, []);

  const removeFloatingXP = useCallback((id: string) => {
    setFloatingXP(prev => prev.filter(fp => fp.id !== id));
  }, []);

  useEffect(() => {
    connectWebSocket();
    
    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, [connectWebSocket]);

  return (
    <div className={className}>
      {/* Connection Status Indicator */}
      <div className="fixed bottom-4 right-4 z-30">
        <motion.div
          className={`
            flex items-center space-x-2 px-3 py-2 rounded-full text-sm font-medium
            ${isConnected 
              ? 'bg-green-100 text-green-800 border border-green-200' 
              : 'bg-red-100 text-red-800 border border-red-200'
            }
          `}
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
        >
          <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </motion.div>
      </div>

      {/* Toast Notifications */}
      <AnimatePresence>
        {notifications.map((notification, index) => (
          <motion.div
            key={notification.id}
            style={{ top: `${1 + index * 5}rem` }}
            className="relative"
          >
            <XPToast
              notification={notification}
              onClose={() => removeNotification(notification.id)}
            />
          </motion.div>
        ))}
      </AnimatePresence>

      {/* Floating XP Indicators */}
      <AnimatePresence>
        {floatingXP.map((xp) => (
          <XPFloatingIndicator
            key={xp.id}
            amount={xp.amount}
            onComplete={() => removeFloatingXP(xp.id)}
          />
        ))}
      </AnimatePresence>

      {/* Achievement Unlock Modal */}
      <AnimatePresence>
        {achievementModal && (
          <AchievementUnlockAnimation
            achievement={achievementModal}
            onComplete={() => setAchievementModal(null)}
          />
        )}
      </AnimatePresence>
    </div>
  );
};

export default AgentXPTracker;