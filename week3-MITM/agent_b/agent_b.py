import os
import requests
import urllib3
from fastapi import FastAPI, Request

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# [명시적 프록시 설정] Tool Server로 가는 패킷을 Burp Suite로 우회
os.environ['http_proxy'] = 'http://host.docker.internal:8080'
os.environ['https_proxy'] = 'http://host.docker.internal:8080'
os.environ['CURL_CA_BUNDLE'] = '' 

app = FastAPI()
TOOL_SERVER_URL = "http://tool_server:8000/tool"

@app.post("/process")
async def process_prompt(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    trace_id = data.get("trace_id")

    if "file" in prompt.lower():
        tool = "read_file"
        args = {"path": "hello.txt"}
    else:
        tool = "echo"
        args = {"message": prompt}

    # Tool Server로의 요청도 Burp Suite를 통과하도록 verify=False 적용
    response = requests.post(
        TOOL_SERVER_URL, 
        json={"tool": tool, "args": args},
        verify=False,
        timeout=5
    )
    
    return {
        "trace_id": trace_id,
        "stage": "result",
        "prompt": prompt,
        "decided_tool": tool,
        "result": response.json().get("result")
    }