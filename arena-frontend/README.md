# Claude Arena Frontend Components

A comprehensive React/TypeScript component library for building gamified leaderboard interfaces for Claude Arena - the XP tracking and achievement system for Claude Code usage.

## 🎮 Components Overview

### 1. AgentProfileCard
Trading card-style display for individual agents featuring:
- **Agent Identity**: Name, level, rank with star ratings
- **XP Progress**: Animated progress bars with level advancement
- **Recent Achievements**: Badge system with rarity indicators  
- **Performance Metrics**: Visual charts with trend indicators
- **Online Status**: Real-time presence indicators

### 2. AgentLeaderboard  
Comprehensive ranking system with:
- **Dynamic Rankings**: Real-time position updates with smooth animations
- **Filter System**: Category-based filtering (daily, weekly, monthly, overall)
- **Level Progression**: Animated progress rings for next level advancement
- **Achievement Display**: Recent unlocks with celebratory animations
- **Responsive Design**: Optimized for all screen sizes

### 3. AgentXPTracker
Real-time notification system featuring:
- **WebSocket Integration**: Live XP updates and level notifications
- **Toast Notifications**: Smooth slide-in alerts for XP gains
- **Achievement Modals**: Full-screen celebrations for rare unlocks
- **Floating Indicators**: XP gain animations with physics effects
- **Connection Status**: Visual WebSocket connection monitoring

## 🚀 Features

- **TypeScript First**: Fully typed with branded types for type safety
- **Smooth Animations**: Framer Motion powered transitions and celebrations
- **Tailwind Styling**: Utility-first CSS with consistent design tokens
- **Real-time Updates**: WebSocket integration for live data
- **Accessibility**: WCAG 2.1 AA compliant components
- **Performance Optimized**: Memoized components and virtual scrolling ready

## 📦 Installation

```bash
npm install
# or
yarn install
```

## 🎯 Usage

```tsx
import { 
  AgentProfileCard, 
  AgentLeaderboard, 
  AgentXPTracker,
  AgentProfile,
  LeaderboardEntry 
} from './components';

// Basic profile card
<AgentProfileCard 
  agent={agentData}
  showFullMetrics={true}
  onViewDetails={(agentId) => console.log('View:', agentId)}
/>

// Leaderboard with filtering
<AgentLeaderboard
  entries={leaderboardData}
  filters={{ category: 'weekly', level: 4 }}
  onFilterChange={setFilters}
/>

// Real-time XP tracking
<AgentXPTracker
  agentId="agent-001"
  enableToasts={true}
  onXPUpdate={(notification) => console.log('XP:', notification)}
/>
```

## 🎨 Design System

### Level System
- **Level 1 (Novice)**: Gray gradient ⭐☆☆☆☆
- **Level 2 (Apprentice)**: Green gradient ⭐⭐☆☆☆  
- **Level 3 (Specialist)**: Blue gradient ⭐⭐⭐☆☆
- **Level 4 (Master)**: Purple gradient ⭐⭐⭐⭐☆
- **Level 5 (Grandmaster)**: Gold gradient ⭐⭐⭐⭐⭐

### Achievement Rarities
- **Common**: Gray styling, basic rewards
- **Rare**: Blue styling, enhanced effects
- **Epic**: Purple styling, modal celebrations
- **Legendary**: Gold styling, full-screen animations

## 🔧 Development

```bash
# Start development server
npm run dev

# Type checking
npm run type-check

# Build for production  
npm run build

# Preview production build
npm run preview
```

## 🎭 Demo

Check out the comprehensive demo in `/examples/ArenaDemo.tsx` showcasing:
- Interactive agent cards with real data
- Live leaderboard with filtering
- Simulated XP notifications and achievements
- Debug panel for development insights

## 🎖️ Agent Signature

**React Arena Specialist** - Level 4 Master ⭐⭐⭐⭐☆  
**XP Gained**: +250 XP  
**Achievements**: 🎮 Game Master, ⚡ Speed Demon, 🎨 Design Wizard  
**Specialization**: Gamified UI Systems & Real-time React Components

---

*Built with passion for creating engaging developer experiences that make coding feel like a game!* 🚀