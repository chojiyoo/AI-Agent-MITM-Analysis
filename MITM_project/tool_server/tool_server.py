import hmac       # [추가] HMAC 검증을 위한 라이브러리
import hashlib    # [추가] 해시 알고리즘 사용을 위한 라이브러리
import json       # [추가] 바이트 데이터를 JSON으로 변환하기 위한 라이브러리
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()
# [추가] agent_b.py와 동일한 비밀키 (무결성 검증의 핵심)
SECRET_KEY = b"winter_evision_secret_key"

# 모의 데이터베이스
MOCK_DB = {
    "me": {"name": "일반사용자", "email": "user@example.com", "role": "USER"},
    "admin": {"name": "관리자", "email": "admin@internal.system", "role": "ADMIN", "secret_key": "SUPER_SECRET_1234"}
}

@app.post("/tool")
async def execute_tool(request: Request):
    # 1. 원본 데이터 및 헤더 추출 (중복 제거)
    raw_body = await request.body()
    received_signature = request.headers.get("X-Signature")
    
    # 2. 서명 재계산
    expected_signature = hmac.new(SECRET_KEY, raw_body, hashlib.sha256).hexdigest()

    # 3. 무결성 검증 (hmac.compare_digest로 타이밍 공격 방지)
    if not received_signature or not hmac.compare_digest(expected_signature, received_signature):
        return JSONResponse(
            status_code=403,
            content={"result": "Access Denied: 데이터 변조가 감지되었습니다. (Invalid Signature)"}
        )

    # 4. 검증 통과 시 JSON 파싱 및 로직 수행
    data = json.loads(raw_body)
    tool = data.get("tool")
    args = data.get("args", {})

    if tool == "get_user_info":
        user_id = args.get("user_id")
        user_data = MOCK_DB.get(user_id)
        return {"result": user_data} if user_data else {"result": "User not found"}

    elif tool == "echo":
        return {"result": args.get("message")}

    return {"result": "Unknown tool"}