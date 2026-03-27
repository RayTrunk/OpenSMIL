import requests
import xml.etree.ElementTree as ET

BASE_URL = "http://localhost:8000/api/v1"
MAC = "AA:BB:CC:DD:EE:01"

def verify_smil():
    print(f"--- SMIL Verification for Player {MAC} ---")
    
    # 1. Get Token
    print("Logging in...")
    login_res = requests.post(f"{BASE_URL}/login/access-token", data={"username": "admin", "password": "admin"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create a Playlist
    print("Creating test playlist...")
    pl_res = requests.post(f"{BASE_URL}/playlists/", json={"name": "Verification Loop", "description": "Test Playlist"}, headers=headers)
    try:
        playlist_id = pl_res.json()["id"]
    except Exception as e:
        print(f"FAILED to create playlist. Status: {pl_res.status_code}")
        print(f"Response: {pl_res.text}")
        raise e

    # 3. Upload a Dummy Media
    print("Uploading test image...")
    # Create a small dummy file
    with open("test_image.png", "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82")
    
    with open("test_image.png", "rb") as f:
        media_res = requests.post(f"{BASE_URL}/media/", files={"file": f}, data={"name": "VerifyImg"}, headers=headers)
    media_id = media_res.json()["id"]

    # 4. Add Media to Playlist
    print("Adding item to playlist...")
    requests.post(f"{BASE_URL}/playlists/{playlist_id}/items", json={"media_id": media_id, "duration": 15, "position": 0}, headers=headers)

    # 5. Assign Playlist to Player
    print(f"Assigning playlist {playlist_id} to player {MAC}...")
    # First find player ID
    players = requests.get(f"{BASE_URL}/players/", headers=headers).json()
    player = next((p for p in players if p["mac_address"] == MAC), None)
    
    if not player:
        # Create player if not exists
        player = requests.post(f"{BASE_URL}/players/", json={"name": "Verify Player", "mac_address": MAC}, headers=headers).json()
    
    player_id = player["id"]
    # Update player (simulated PUT/PATCH)
    requests.put(f"{BASE_URL}/players/{player_id}", json={**player, "playlist_id": playlist_id}, headers=headers)

    # 6. Fetch SMIL XML
    print("Fetching SMIL XML...")
    smil_res = requests.get(f"{BASE_URL}/smil/{MAC}/smil.xml")
    
    print("\n--- GENERATED SMIL ---")
    print(smil_res.text)
    print("----------------------\n")

    # 7. Validate XML Structure
    try:
        ns = {"smil": "http://www.w3.org/2001/SMIL20/Language"}
        root = ET.fromstring(smil_res.text)
        assert "{http://www.w3.org/2001/SMIL20/Language}smil" in root.tag or "smil" in root.tag
        
        body = root.find("smil:body", ns)
        seq = body.find("smil:seq", ns)
        img = seq.find("smil:img", ns)
        
        assert img.get("dur") == "15s"
        assert "/media/" in img.get("src")
        
        print("✓ SMIL Structure is valid!")
        print("✓ Namespace: Correct")
        print("✓ Content: Correct")
        print("✓ Duration: Correct")
    except Exception as e:
        print(f"✗ Validation failed: {e}")
        import traceback
        traceback.print_exc()

    # Cleanup dummy file
    import os
    if os.path.exists("test_image.png"):
        os.remove("test_image.png")

if __name__ == "__main__":
    verify_smil()
