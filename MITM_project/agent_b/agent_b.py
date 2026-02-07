import requests
import hmac
import hashlib
import json
import ssl
from fastapi import FastAPI, Request
from requests.adapters import HTTPAdapter
from urllib3.poolmanager import PoolManager

app = FastAPI()

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1_2
        )

SECRET_KEY = b"winter_evision_secret_key"
TOOL_SERVER_URL = "https://tool-server:8000/tool"

# [수정] 프록시 프로토콜은 둘 다 http://여야 함
PROXIES = {
    "http": "http://host.docker.internal:8080",
    "https": "http://host.docker.internal:8080",
}

# [수정] docker-compose에서 마운트한 경로와 일치시킴
CA_CERT_PATH = "/usr/local/share/ca-certificates/burp.crt"

@app.post("/process")
async def process_prompt(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")

    if "정보" in prompt:
        tool = "get_user_info"
        args = {"user_id": "me"}
    else:
        tool = "echo"
        args = {"message": prompt}

    payload = {"tool": tool, "args": args}
    # sort_keys=True를 사용해야 서버와 해시값이 일치함
    payload_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")

    signature = hmac.new(SECRET_KEY, payload_bytes, hashlib.sha256).hexdigest()

    headers = {
        "X-Signature": signature,
        "Content-Type": "application/json"
    }

    session = requests.Session()
    session.mount("https://", TLSAdapter())

    try:
        response = session.post(
            TOOL_SERVER_URL,
            proxies=PROXIES,
            data=payload_bytes,
            headers=headers,
            verify=CA_CERT_PATH,
            timeout=60
        )
        response.raise_for_status()
        result = response.json().get("result")
    except Exception as e:
        result = f"Error connecting to Tool Server: {str(e)}"

    return {"decided_tool": tool, "sent_args": args, "result": result}