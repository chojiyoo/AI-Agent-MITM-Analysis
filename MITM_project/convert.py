import ssl

# 1. DER 형식의 인증서를 읽습니다.
with open("burp.crt.der", "rb") as f:
    der_data = f.read()

# 2. PEM 형식으로 변환하여 저장합니다.
pem_data = ssl.DER_cert_to_PEM_cert(der_data)
with open("burp.crt", "wb") as f:
    f.write(pem_data.encode('utf-8'))

print("[+] 변환 완료: burp_pem.crt 파일이 생성되었습니다.")