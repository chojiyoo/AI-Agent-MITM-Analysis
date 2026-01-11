from fastapi import FastAPI, Request
import os

app = FastAPI()

# 실제 기능 실행부
@app.post("/tool")
async def execute_tool(request: Request):
    data = await request.json()
    tool = data.get("tool")
    args = data.get("args", {})
    
    if tool == "read_file":
        # 이미지 구조상 /data/hello.txt 경로를 참조해야 합니다.
        file_path = "/data/hello.txt" 
        if os.path.exists(file_path):
            with open("/data/hello.txt", "r") as f:
                result = f.read()
        else:
            result = "파일을 찾을 수 없습니다."
            
    elif tool == "echo":
        result = f"Echo: {args.get('message')}"
    
    else:
        result = "알 수 없는 도구입니다."

    return {"result": result}