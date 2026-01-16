import os
import uuid
import requests
import time

PROMPT = os.getenv("PROMPT", "read file")
AGENT_B_URL = "http://agent_b:8001/process" # Agent B의 포트

def main():
    trace_id = str(uuid.uuid4())
    
    # 이미지에 나온 payload 구조 그대로 사용
    payload = {
        "trace_id": trace_id,
        "stage": "prompt",
        "prompt": PROMPT,
    }

    # Agent B에게 요청 및 재시도 로직
    for i in range(1, 10):
        try:
            res = requests.post(AGENT_B_URL, json=payload)
            if res.status_code == 200:
                print(f"최종 결과: {res.json()}")
                break
        except:
            time.sleep(1)

if __name__ == "__main__":
    main()