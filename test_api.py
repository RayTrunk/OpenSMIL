import requests
import time
import subprocess
import os

BASE_URL = "http://localhost:8000/api/v1"

def test_api():
    print("Starting FastAPI server...")
    server = subprocess.Popen(["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"], cwd=".")
    time.sleep(3)  # Wait for server to start

    try:
        # 1. Test Login
        print("Testing Login...")
        login_data = {"username": "admin", "password": "admin"}
        response = requests.post(f"{BASE_URL}/login/access-token", data=login_data)
        assert response.status_code == 200, f"Login failed: {response.text}"
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        print("✓ Login successful")

        # 2. Test Create Player
        print("Testing Create Player...")
        player_data = {
            "name": "Test Player 1",
            "mac_address": "AA:BB:CC:DD:EE:01",
            "description": "A test player"
        }
        response = requests.post(f"{BASE_URL}/players/", json=player_data, headers=headers)
        assert response.status_code == 200, f"Create Player failed: {response.text}"
        player_id = response.json()["id"]
        print(f"✓ Player created with ID: {player_id}")

        # 3. Test SMIL Generation (Unauthenticated player access)
        print("Testing SMIL Generation...")
        response = requests.get(f"{BASE_URL}/smil/AA:BB:CC:DD:EE:01/smil.xml")
        assert response.status_code == 200, f"SMIL generation failed: {response.text}"
        assert "smil" in response.text
        print("✓ SMIL XML generated")

        print("\nAll tests passed successfully!")

    finally:
        server.terminate()

if __name__ == "__main__":
    test_api()
