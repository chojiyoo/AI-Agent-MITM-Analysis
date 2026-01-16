import requests
from fastapi import FastAPI, Request

app = FastAPI()
TOOL_SERVER_URL = "http://tool_server:8000/tool"

@app.post("/process")
async def process_prompt(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    trace_id = data.get("trace_id")

    # [규칙 기반 처리] 'file' 키워드 여부 판단
    if "file" in prompt.lower():
        tool = "read_file"
        args = {"path": "hello.txt"}
    else:
        tool = "echo"
        args = {"message": prompt}

    # Tool Server에 실행 요청
    response = requests.post(TOOL_SERVER_URL, json={
        "tool": tool,
        "args": args
    })
    
    return {
    "trace_id": trace_id,
    "stage": "result",      # 단계(stage)를 'result'로 표시
    "prompt": prompt,       # 요청받은 프롬프트 내용을 그대로 포함
    "decided_tool": tool,   # 결정된 도구 이름
    "result": response.json().get("result") # 'response' 대신 'result' 키 사용
}