import os
import uuid
import requests
import time
import urllib3

# SSL 인증서 경고 무시 (Burp Suite 인증서 사용 시 필수)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# [명시적 프록시 설정] 윈도우 호스트의 Burp Suite(8080)로 경로 지정
os.environ['http_proxy'] = 'http://host.docker.internal:8080'
os.environ['https_proxy'] = 'http://host.docker.internal:8080'
os.environ['CURL_CA_BUNDLE'] = '' 

# URL은 도커 서비스 이름을 그대로 사용 (Burp DNS 설정 필요)
AGENT_B_URL = "http://agent_b:8001/process" 
PROMPT = os.getenv("PROMPT", "echo hello")

def main():
    trace_id = str(uuid.uuid4())
    payload = {
        "trace_id": trace_id,
        "stage": "prompt",
        "prompt": PROMPT,
    }

    for i in range(1, 10):
        try:
            # verify=False를 통해 Burp Suite의 자체 서명 인증서를 허용
            res = requests.post(AGENT_B_URL, json=payload, verify=False, timeout=5)
            if res.status_code == 200:
                print(f"최종 결과: {res.json()}")
                break
        except Exception as e:
            print(f"연결 시도 중... ({i}/10)")
            time.sleep(1)

if __name__ == "__main__":
    main()