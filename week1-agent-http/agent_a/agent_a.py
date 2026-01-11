# agent_a/agent_a.py
import requests
import time

url = "http://agent_b:8000/tool" # Docker Compose 서비스 이름 사용
payload = {
    "tool": "read_file",
    "args": {"path": "/hello.txt"}
}

for i in range(1, 31):
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"서버 응답: {response.json()}")
            break
    except:
        print(f"[{i}/30] 아직 서버 준비 안 됨... 재시도")
        time.sleep(1)