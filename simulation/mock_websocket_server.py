import asyncio
import json
import random
import datetime
import sys

try:
    import websockets
except ImportError:
    print("\n" + "="*80, file=sys.stderr)
    print("ERREUR : Le module Python 'websockets' n'est pas installé dans votre environnement global.", file=sys.stderr)
    print("Veuillez lancer ce serveur en utilisant l'environnement virtuel du projet :", file=sys.stderr)
    print("  ./venv/bin/python simulation/mock_websocket_server.py", file=sys.stderr)
    print("Ou activez l'environnement virtuel d'abord :", file=sys.stderr)
    print("  source venv/bin/activate && python simulation/mock_websocket_server.py", file=sys.stderr)
    print("="*80 + "\n", file=sys.stderr)
    sys.exit(1)

# Mock WebSocket Server for Urban Glow Grid
# Broadcasts localized city sensor energy load rates.

clients = set()

def generate_sensor_data():
    """Generates mock energy load data for the 3 main districts."""
    # Base loads
    base_haussmann = 40.0
    base_defense = 35.0
    base_monuments = 20.0
    
    # Introduce random fluctuations (± 15%)
    fluct_h = base_haussmann * random.uniform(0.85, 1.15)
    fluct_d = base_defense * random.uniform(0.85, 1.15)
    fluct_m = base_monuments * random.uniform(0.85, 1.15)
    
    # Simulate a sudden peak occasionally
    if random.random() > 0.8:
        fluct_d += random.uniform(20.0, 40.0)
        
    # Occasionally trigger a blackout scenario if total goes very high
    if random.random() > 0.95:
        fluct_h += 50.0

    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": "energy_load_update",
        "data": {
            "haussmann_load": round(fluct_h, 2),
            "defense_load": round(fluct_d, 2),
            "monuments_load": round(fluct_m, 2),
            "total_load": round(fluct_h + fluct_d + fluct_m + 5.0, 2) # +5 for base consumption
        }
    }

async def handler(websocket, path=None):
    # Register client
    clients.add(websocket)
    print(f"Client connected. Total clients: {len(clients)}")
    try:
        # Keep connection open, though we'll primarily broadcast
        async for message in websocket:
            print(f"Received message from client: {message}")
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected.")
    finally:
        # Unregister client
        clients.remove(websocket)

async def broadcast_data():
    while True:
        if clients:
            data = generate_sensor_data()
            message = json.dumps(data)
            # Create a task for each send operation to send concurrently
            # websockets.broadcast is available in newer versions, but we'll do it manually to be safe
            websockets.broadcast(clients, message)
            print(f"Broadcasted: {message}")
        await asyncio.sleep(3) # Broadcast every 3 seconds

async def main():
    # Start the websocket server on port 8080
    async with websockets.serve(handler, "localhost", 8080):
        print("Mock WebSocket server started at ws://localhost:8080")
        # Run the broadcast loop concurrently
        await broadcast_data()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by user.")
