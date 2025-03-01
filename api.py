from fastapi import FastAPI, HTTPException
import requests
import time
import threading

app = FastAPI()

def share_post(cookie: str, share_url: str, share_count: int, interval: float):
    url = "https://graph.facebook.com/me/feed"
    headers = {"User-Agent": "Mozilla/5.0"}
    data = {
        "link": share_url,
        "privacy": '{"value":"SELF"}',
        "no_story": "true",
        "published": "false",
        "access_token": cookie
    }
    
    success_count = 0
    for i in range(share_count):
        try:
            response = requests.post(url, json=data, headers=headers)
            response_data = response.json()
            post_id = response_data.get("id", None)
            if post_id:
                success_count += 1
        except requests.exceptions.RequestException as e:
            pass
        time.sleep(interval)
    
    return {"total_successful_shares": success_count}

@app.post("/share")
def share_post_api(token: str, url: str, count: int, interval: float = 1.0):
    if not token.startswith("EAAAA"):
        raise HTTPException(status_code=400, detail="Invalid access token format")
    if count < 1 or count > 1000000:
        raise HTTPException(status_code=400, detail="Share count must be between 1 and 1,000,000")
    if interval not in [0.1, 0.5, 1, 2, 5, 10]:
        raise HTTPException(status_code=400, detail="Interval must be one of [0.1, 0.5, 1, 2, 5, 10]")
    
    result = share_post(token, url, count, interval)
    return result
