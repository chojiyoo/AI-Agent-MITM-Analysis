# agent_b/tool_server.py
from fastapi import FastAPI, Request

app = FastAPI()

@app.post("/tool")
async def handle_tool(request: Request):
    data = await request.json()
    print(f"받은 요청 : {data}")
    return {"status": "ok", "tool": data.get("tool"), "args": data.get("args")}