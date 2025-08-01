"""
Real-time Notification Service
WebSocket-based notifications for XP updates, achievements, and leaderboard changes
"""

import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Set
from uuid import UUID
from contextlib import asynccontextmanager

from fastapi import WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from ..schemas.xp_tracking import XPNotification, WebSocketMessage, XPEventResponse


class ConnectionManager:
    """Manages WebSocket connections for real-time notifications"""
    
    def __init__(self):
        # Active connections by user_id
        self.active_connections: Dict[UUID, Set[WebSocket]] = {}
        # Team/group subscriptions
        self.team_subscriptions: Dict[str, Set[UUID]] = {}
        # Connection metadata
        self.connection_metadata: Dict[WebSocket, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: UUID, metadata: Optional[Dict] = None):
        """Accept WebSocket connection and register user"""
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        self.connection_metadata[websocket] = {
            "user_id": user_id,
            "connected_at": datetime.utcnow(),
            "last_ping": datetime.utcnow(),
            **(metadata or {})
        }
        
        # Send connection confirmation
        await self.send_personal_message(
            user_id,
            WebSocketMessage(
                type="connection_established",
                data={"user_id": str(user_id), "timestamp": datetime.utcnow().isoformat()}
            )
        )
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.connection_metadata:
            user_id = self.connection_metadata[websocket]["user_id"]
            
            # Remove from active connections
            if user_id in self.active_connections:
                self.active_connections[user_id].discard(websocket)
                if not self.active_connections[user_id]:
                    del self.active_connections[user_id]
            
            # Clean up metadata
            del self.connection_metadata[websocket]
    
    async def send_personal_message(self, user_id: UUID, message: WebSocketMessage):
        """Send message to all connections for a specific user"""
        if user_id in self.active_connections:
            message_json = message.json()
            
            # Send to all user's connections
            disconnected = set()
            for websocket in self.active_connections[user_id].copy():
                try:
                    await websocket.send_text(message_json)
                except Exception:
                    # Connection is dead, mark for cleanup
                    disconnected.add(websocket)
            
            # Clean up dead connections
            for websocket in disconnected:
                self.disconnect(websocket)
    
    async def send_team_message(self, team_id: str, message: WebSocketMessage):
        """Send message to all users in a team"""
        if team_id in self.team_subscriptions:
            for user_id in self.team_subscriptions[team_id]:
                await self.send_personal_message(user_id, message)
    
    async def broadcast_message(self, message: WebSocketMessage):
        """Send message to all connected users"""
        for user_id in self.active_connections.keys():
            await self.send_personal_message(user_id, message)
    
    def subscribe_to_team(self, user_id: UUID, team_id: str):
        """Subscribe user to team notifications"""
        if team_id not in self.team_subscriptions:
            self.team_subscriptions[team_id] = set()
        self.team_subscriptions[team_id].add(user_id)
    
    def unsubscribe_from_team(self, user_id: UUID, team_id: str):
        """Unsubscribe user from team notifications"""
        if team_id in self.team_subscriptions:
            self.team_subscriptions[team_id].discard(user_id)
            if not self.team_subscriptions[team_id]:
                del self.team_subscriptions[team_id]
    
    def get_connection_count(self) -> int:
        """Get total number of active connections"""
        return sum(len(connections) for connections in self.active_connections.values())
    
    def get_user_connections(self, user_id: UUID) -> int:
        """Get number of connections for a specific user"""
        return len(self.active_connections.get(user_id, set()))
    
    async def ping_all_connections(self):
        """Send ping to all connections to keep them alive"""
        ping_message = WebSocketMessage(
            type="ping",
            data={"timestamp": datetime.utcnow().isoformat()}
        )
        
        disconnected = []
        for user_id, connections in self.active_connections.items():
            for websocket in connections.copy():
                try:
                    await websocket.send_text(ping_message.json())
                    # Update last ping time
                    if websocket in self.connection_metadata:
                        self.connection_metadata[websocket]["last_ping"] = datetime.utcnow()
                except Exception:
                    disconnected.append(websocket)
        
        # Clean up disconnected sockets
        for websocket in disconnected:
            self.disconnect(websocket)


class NotificationService:
    """Service for sending various types of notifications"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
    
    async def send_xp_notification(
        self, 
        user_id: UUID, 
        agent_name: str, 
        xp_response: XPEventResponse
    ):
        """Send XP gain notification"""
        notification = XPNotification(
            user_id=user_id,
            agent_name=agent_name,
            xp_gained=xp_response.xp_gained,
            total_xp=xp_response.total_xp,
            level_up=xp_response.level_up,
            new_level=xp_response.level_after if xp_response.level_up else None,
            achievements=xp_response.achievements_unlocked
        )
        
        await self.connection_manager.send_personal_message(
            user_id, 
            notification.to_websocket_message()
        )
    
    async def send_achievement_notification(
        self, 
        user_id: UUID, 
        achievement_name: str, 
        achievement_display: str,
        xp_reward: int
    ):
        """Send achievement unlock notification"""
        message = WebSocketMessage(
            type="achievement_unlocked",
            data={
                "achievement_name": achievement_name,
                "achievement_display": achievement_display,
                "xp_reward": xp_reward,
                "unlocked_at": datetime.utcnow().isoformat()
            }
        )
        
        await self.connection_manager.send_personal_message(user_id, message)
    
    async def send_level_up_notification(
        self, 
        user_id: UUID, 
        agent_name: str, 
        old_level: int, 
        new_level: int
    ):
        """Send level up notification"""
        message = WebSocketMessage(
            type="level_up",
            data={
                "agent_name": agent_name,
                "old_level": old_level,
                "new_level": new_level,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        await self.connection_manager.send_personal_message(user_id, message)
    
    async def send_team_leaderboard_update(self, team_id: str, leaderboard_data: Dict):
        """Send team leaderboard update"""
        message = WebSocketMessage(
            type="team_leaderboard_update",
            data={
                "team_id": team_id,
                "leaderboard": leaderboard_data,
                "updated_at": datetime.utcnow().isoformat()
            }
        )
        
        await self.connection_manager.send_team_message(team_id, message)
    
    async def send_system_notification(self, user_id: UUID, notification_type: str, data: Dict):
        """Send generic system notification"""
        message = WebSocketMessage(
            type=notification_type,
            data=data
        )
        
        await self.connection_manager.send_personal_message(user_id, message)


# WebSocket connection handler
class WebSocketHandler:
    """Handles WebSocket connection lifecycle"""
    
    def __init__(self, connection_manager: ConnectionManager):
        self.connection_manager = connection_manager
    
    async def handle_connection(self, websocket: WebSocket, user_id: UUID):
        """Handle WebSocket connection with proper error handling"""
        await self.connection_manager.connect(websocket, user_id)
        
        try:
            while True:
                # Wait for messages from client
                data = await websocket.receive_text()
                
                try:
                    message = json.loads(data)
                    await self.handle_client_message(websocket, user_id, message)
                except json.JSONDecodeError:
                    # Send error response
                    error_msg = WebSocketMessage(
                        type="error",
                        data={"error": "Invalid JSON format"}
                    )
                    await websocket.send_text(error_msg.json())
                
        except WebSocketDisconnect:
            self.connection_manager.disconnect(websocket)
        except Exception as e:
            # Log error and disconnect
            print(f"WebSocket error for user {user_id}: {e}")
            self.connection_manager.disconnect(websocket)
    
    async def handle_client_message(self, websocket: WebSocket, user_id: UUID, message: Dict):
        """Handle incoming messages from client"""
        message_type = message.get("type")
        data = message.get("data", {})
        
        if message_type == "ping":
            # Respond to ping
            pong_message = WebSocketMessage(
                type="pong",
                data={"timestamp": datetime.utcnow().isoformat()}
            )
            await websocket.send_text(pong_message.json())
        
        elif message_type == "subscribe_team":
            # Subscribe to team notifications
            team_id = data.get("team_id")
            if team_id:
                self.connection_manager.subscribe_to_team(user_id, team_id)
                
                response = WebSocketMessage(
                    type="subscription_confirmed",
                    data={"team_id": team_id, "subscribed": True}
                )
                await websocket.send_text(response.json())
        
        elif message_type == "unsubscribe_team":
            # Unsubscribe from team notifications
            team_id = data.get("team_id")
            if team_id:
                self.connection_manager.unsubscribe_from_team(user_id, team_id)
                
                response = WebSocketMessage(
                    type="subscription_confirmed",
                    data={"team_id": team_id, "subscribed": False}
                )
                await websocket.send_text(response.json())
        
        elif message_type == "get_status":
            # Send connection status
            status = WebSocketMessage(
                type="connection_status",
                data={
                    "user_id": str(user_id),
                    "connected_at": self.connection_manager.connection_metadata[websocket]["connected_at"].isoformat(),
                    "total_connections": self.connection_manager.get_connection_count()
                }
            )
            await websocket.send_text(status.json())


# Global connection manager instance
connection_manager = ConnectionManager()
notification_service = NotificationService(connection_manager)
websocket_handler = WebSocketHandler(connection_manager)


# Background task for connection health checks
async def connection_health_check():
    """Background task to check connection health"""
    while True:
        try:
            await connection_manager.ping_all_connections()
            await asyncio.sleep(30)  # Ping every 30 seconds
        except Exception as e:
            print(f"Error in connection health check: {e}")
            await asyncio.sleep(5)  # Wait before retrying


# Context manager for background tasks
@asynccontextmanager
async def notification_service_lifespan():
    """Context manager for notification service lifecycle"""
    # Start background tasks
    health_check_task = asyncio.create_task(connection_health_check())
    
    try:
        yield
    finally:
        # Clean up background tasks
        health_check_task.cancel()
        try:
            await health_check_task
        except asyncio.CancelledError:
            pass