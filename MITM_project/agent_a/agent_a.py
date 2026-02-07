import requests
import time

def run_experiment():
    url = "http://agent_b:8001/process"
    payload = {"prompt": "내 정보 보여줘"}  # 공격 트리거 프롬프트

    try:
        print(f"[+] 요청 전송: {payload['prompt']}")
        response = requests.post(url, json=payload)
        print(f"[+] 최종 결과: {response.json().get('result')}")
    except Exception as e:
        print(f"[-] 에러 발생: {e}")

if __name__ == "__main__":
    time.sleep(2)
    run_experiment()