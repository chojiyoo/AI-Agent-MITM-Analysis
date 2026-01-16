#  프록시(Burp Suite)를 이용해 MITM(Man-In-The-Middle) 테스트

## Proxy, Burp Suite 개념 학습 정리

1. 프록시(Proxy) 개념 정리
클라이언트와 서버 사이에서 중계 역할을 수행하는 서버

Forward Proxy : 클라이언트 앞에 위치하여 외부로 나가는 요청을 중계
- 클라이언트의 IP를 숨기거나 내부망 보안 정책 적용에 사용

Reverse Proxy : 웹 서버 앞에 위치하여 클라이언트로 들어오는 요청을 서버로 전달함
- 로드 밸런싱, 보안 강화(WAF), 캐싱 기능 수행

Transparent Proxy : 사용자가 설정하지 않아도 패킷을 가로채서 중계함
- 클라이언트는 프록시의 존재를 인지하지 못함

2. Burp Suite
웹 애플리케이션 보안 테스팅을 위한 통합 플랫폼

3. Burp Suite 핵심 기능

(1) Intercept
역할: 실시간으로 오가는 HTTP 요청(Request) 및 응답(Response)을 중간에 멈춰 세우는 기능
활용: 패킷이 서버로 전달되기 전에 데이터를 수정하거나, 서버의 응답을 클라이언트에 도달하기 전에 변조할 때 사용

(2) HTTP History
역할: 프록시를 통과한 모든 HTTP 통신의 기록을 차례대로 보여주는 로그 탭
활용: 통신이 정상적으로 이루어지는지(200 OK), 어떤 호스트(agent_b, tool_server)와 통신하는지 전반적인 흐름을 파악하는 데 유용

(3) Repeater
역할: 특정 요청을 복사하여 수동으로 수정하고 반복해서 재전송할 수 있는 도구
활용: Raw 탭에서 JSON 데이터 내부의 prompt나 tool-call 인자값을 직접 수정하여 서버의 반응 변화를 관찰할 때 핵심적으로 사용

4. 실습
4-1. a ↔ b 사이, b ↔ server 사이에 Burp Suite 프록시 연결 (test를 위해 환경변수를 이용한 명시적 프록시 설정)

 환경 변수(HTTP_PROXY)를 사용하여 패킷이 호스트의 Burp Suite(host.docker.internal:8080)를 반드시 거치도록 설계
![alt text](3-1.png)

4-2. HTTP history에서 요청 2개(a↔b, b↔tool) & 대응하는 response
![alt text](1-1.png)

4-3. epeater 기능으로 prompt, tool-call, response 변조
![](2-1.png)





