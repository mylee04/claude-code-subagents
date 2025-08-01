"""
WebSocket Router for Real-time Notifications
Handles WebSocket connections for XP updates, achievements, and leaderboard changes
"""

from uuid import UUID
from typing import Optional

from fastapi import APIRouter, WebSocket, Depends, HTTPException, Query
from fastapi.security import HTTPBearer
from starlette.websockets import WebSocketDisconnect

from ..core.auth import get_current_user_websocket  # Placeholder for WebSocket auth
from ..services.notification_service import websocket_handler, connection_manager, notification_service


router = APIRouter(prefix="/ws", tags=["WebSocket"])
security = HTTPBearer()


@router.websocket("/notifications/{user_id}")
async def websocket_notifications(
    websocket: WebSocket,
    user_id: UUID,
    token: Optional[str] = Query(None)
):
    """
    WebSocket endpoint for real-time notifications
    Handles XP updates, achievements, level-ups, and team updates
    """
    try:
        # Validate user authentication (simplified for example)
        # In production, you'd validate the JWT token here
        if not token:
            await websocket.close(code=4001, reason="Authentication required")
            return
        
        # TODO: Validate token and get user info
        # user = await validate_websocket_token(token)
        # if str(user.id) != str(user_id):
        #     await websocket.close(code=4003, reason="Unauthorized")
        #     return
        
        # Handle the WebSocket connection
        await websocket_handler.handle_connection(websocket, user_id)
        
    except WebSocketDisconnect:
        # Connection closed normally
        pass
    except Exception as e:
        print(f"WebSocket error: {e}")
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass


@router.websocket("/team/{team_id}")
async def websocket_team_notifications(
    websocket: WebSocket,
    team_id: str,
    user_id: UUID = Query(...),
    token: Optional[str] = Query(None)
):
    """
    WebSocket endpoint for team-specific notifications
    Handles team leaderboard updates and collaborative achievements
    """
    try:
        # Validate authentication
        if not token:
            await websocket.close(code=4001, reason="Authentication required")
            return
        
        # Connect to personal notifications first
        await connection_manager.connect(websocket, user_id, {"team_id": team_id})
        
        # Subscribe to team notifications
        connection_manager.subscribe_to_team(user_id, team_id)
        
        # Handle connection
        await websocket_handler.handle_connection(websocket, user_id)
        
    except WebSocketDisconnect:
        # Clean up team subscription
        connection_manager.unsubscribe_from_team(user_id, team_id)
    except Exception as e:
        print(f"Team WebSocket error: {e}")
        connection_manager.unsubscribe_from_team(user_id, team_id)
        try:
            await websocket.close(code=1011, reason="Internal server error")
        except:
            pass


# Admin endpoints for testing notifications
@router.post("/admin/test-notification/{user_id}")
async def test_notification(
    user_id: UUID,
    notification_type: str,
    message: str
):
    """Admin endpoint to test notifications (development only)"""
    await notification_service.send_system_notification(
        user_id=user_id,
        notification_type=notification_type,
        data={"message": message, "test": True}
    )
    return {"status": "sent", "user_id": str(user_id)}


@router.get("/admin/connections")
async def get_connection_stats():
    """Get WebSocket connection statistics (admin only)"""
    return {
        "total_connections": connection_manager.get_connection_count(),
        "unique_users": len(connection_manager.active_connections),
        "team_subscriptions": len(connection_manager.team_subscriptions)
    }