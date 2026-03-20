import requests
import json

# 1. Update these from your FRESH browser session (must be done NOW)
next_action_id = "7f25cd7f274b40f654d530bda994dbbabc4b2c6c8d"
cookie_string = "_ga=GA1.1.1506113303.1770801640; accessToken=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9uYW1laWRlbnRpZmllciI6IjI0MzU1IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvc2lkIjoiMGZmZDc2YzUtYmNkMy00MjI3LThkYjEtN2U4NjA4NzRkNTg5IiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZ2l2ZW5uYW1lIjoiTmFyYXlhbiIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL3N1cm5hbWUiOiJTaGFzdHJpIiwiaHR0cDovL3NjaGVtYXMueG1sc29hcC5vcmcvd3MvMjAwNS8wNS9pZGVudGl0eS9jbGFpbXMvZW1haWxhZGRyZXNzIjoiZnBvZHVuZWRpbjgzQGdtYWlsLmNvbSIsImh0dHA6Ly9zY2hlbWFzLnhtbHNvYXAub3JnL3dzLzIwMDUvMDUvaWRlbnRpdHkvY2xhaW1zL2NvdW50cnkiOiIxNTgiLCJpcGFkZHIiOiIxMzkuODAuMjM5LjY1IiwiaHR0cDovL3NjaGVtYXMubWljcm9zb2Z0LmNvbS93cy8yMDA4LzA2L2lkZW50aXR5L2NsYWltcy9yb2xlIjoiVXNlciIsImV4cCI6MTc3MzAwNzMxNywiaXNzIjoiZmFudGFzeS1oZXJkIiwiYXVkIjoiZmFudGFzeS1oZXJkLXVzZXJzIn0.M10QEWh10RAH-q_-cKVenfW43uTNaHCemeu3eUkKdA4; accessTokenExpiresAt=2026-03-08T22%3A01%3A57.368Z; refreshToken=xyZnm6bmLuMqis760xjJVOAbUH9Ct30CoibW2PeR%2Fs%2BNKsVJnPMecvqw%2BxIuqqmY%2FpUqsfXS%2Fct1iL3xj4qM2g%3D%3D; refreshTokenExpiresAt=2026-03-15T21%3A01%3A57.368Z; _ga_4VSVNMX6C1=GS2.1.s1773003707$o16$g1$t1773004455$j56$l0$h0; lastActivity=2026-03-08T21%3A17%3A08.569Z"


url = "https://fantasyherd.co.nz/results"
headers = {
    "Next-Action": next_action_id,
    "Content-Type": "text/plain;charset=UTF-8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Cookie": cookie_string
}

# Try just one cow (Bellucci - 317)
cow_id = 317 

print(f"--- Debugging Request for Cow {cow_id} ---")
response = requests.post(url, headers=headers, data=json.dumps([cow_id]))

print(f"Status Code: {response.status_code}")
print(f"Headers Received: {response.headers.get('Content-Type')}")
print("-" * 30)
print("Raw Response (First 500 chars):")
print(response.text[:500])
print("-" * 30)

if "1:{" in response.text:
    print("✅ SUCCESS: The ID and Cookie are working. You can run the full script.")
else:
    print("❌ FAIL: The server didn't send cow data. Check if the Action ID changed.")