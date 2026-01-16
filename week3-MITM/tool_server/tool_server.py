from fastapi import FastAPI, Request
import os

app = FastAPI()

@app.post("/tool")
async def execute_tool(request: Request):
    data = await request.json()
    tool = data.get("tool")
    args = data.get("args", {})
    
    if tool == "read_file":
        file_path = "/data/hello.txt" 
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                result = f.read()
        else:
            result = "파일을 찾을 수 없습니다."
    elif tool == "echo":
        result = f"Echo: {args.get('message')}"
    else:
        result = "알 수 없는 도구입니다."

    return {"result": result}