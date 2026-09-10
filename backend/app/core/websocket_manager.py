import logging
from typing import Set
from fastapi import WebSocket

logger = logging.getLogger(__name__)

class WebSocketManager:
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
    
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        logger.info(f"WebSocket connected. Active connections: {len(self.active_connections)}")
    
    async def disconnect(self, websocket: WebSocket):
        self.active_connections.discard(websocket)
        logger.info(f"WebSocket disconnected. Active connections: {len(self.active_connections)}")
    
    async def broadcast(self, data: dict):
        """Broadcast event to all connected clients"""
        disconnected = set()
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                logger.error(f"Error broadcasting to connection: {e}")
                disconnected.add(connection)
        
        # Clean up disconnected clients
        for conn in disconnected:
            await self.disconnect(conn)
    
    async def broadcast_to_device(self, device_id: str, data: dict):
        """Broadcast to clients subscribed to a specific device"""
        data["device_id"] = device_id
        await self.broadcast(data)
    
    async def disconnect_all(self):
        """Disconnect all clients gracefully"""
        for connection in list(self.active_connections):
            await connection.close()
        self.active_connections.clear()
        logger.info("All WebSocket connections closed")

manager = WebSocketManager()
