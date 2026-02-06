import os, requests
from app.config.settings import config 

def debug_token(token: str, graph_version="v24.0") -> dict:
    r = requests.get(
        f"https://graph.facebook.com/{graph_version}/debug_token",
        params={"input_token": token, "access_token": token},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["data"]

def post_photo_to_facebook_page(image_path: str, caption: str, page_id: str, page_access_token: str, graph_version: str = "v24.0"):
    info = debug_token(page_access_token, graph_version)
    if info.get("type") != "PAGE":
        raise RuntimeError(f"Need PAGE token. Got type={info.get('type')}")

    url = f"https://graph.facebook.com/{graph_version}/{page_id}/photos"
    with open(image_path, "rb") as f:
        r = requests.post(
            url,
            files={"source": f},
            data={"caption": caption, "published": "true", "access_token": page_access_token},
            timeout=60,
        )

    if not r.ok:
        raise RuntimeError(f"Facebook API error {r.status_code}: {r.text}")
    return r.json()





# print(post_photo_to_facebook_page(
#     image_path="app/db/images/red_tshirt.jpg",
#     caption="Red T-Shirt\nPrice: 499\nSize: M/L\nDM to order.",
#     page_id=config.FB_PAGE_ID,
#     page_access_token=config.FB_PAGE_ACCESS_TOKEN,
#     graph_version="v24.0",
# ))

