# 🌐 Configurar Domínio para a API

Este guia mostra como configurar um domínio para acessar a API via URL personalizada (ex: `https://api.seudominio.com`).

## 📋 Pré-requisitos

- VPS com Docker e Docker Compose instalados
- Domínio apontando para o IP da sua VPS
- Acesso root/sudo na VPS

## 🚀 Método 1: Com Nginx (Recomendado)

### Passo 1: Configurar DNS

1. **No seu provedor de domínio, configure um registro A:**
   - **Tipo:** A
   - **Nome:** `api` (ou `@` para o domínio raiz)
   - **Valor:** IP da sua VPS
   - **TTL:** 3600 (ou padrão)

   Exemplo: Se seu domínio é `meusite.com`, você pode criar:
   - `api.meusite.com` → IP da VPS
   - Ou `meusite.com` → IP da VPS

### Passo 2: Atualizar nginx.conf

1. **Edite o arquivo `nginx.conf`:**
```bash
nano nginx.conf
```

2. **Substitua `server_name _;` pelo seu domínio:**
```nginx
server_name api.seudominio.com;
```

### Passo 3: Deploy com Nginx

1. **Use o docker-compose com Nginx:**
```bash
# Com GPU
docker-compose -f docker-compose-with-nginx.yml up -d --build

# OU sem GPU
docker-compose -f docker-compose-with-nginx-cpu.yml up -d --build
```

### Passo 4: Configurar Firewall

```bash
# Permitir portas HTTP e HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

### Passo 5: Testar

```bash
# Teste sem SSL (HTTP)
curl http://api.seudominio.com/

# Teste gerando imagem
curl -X POST "http://api.seudominio.com/txt2img" \
  -H "x-api-key: sua-chave-secreta" \
  -F "prompt=a beautiful sunset" \
  -o imagem.png
```

## 🔒 Método 2: Com SSL/HTTPS (Recomendado para Produção)

### Passo 1: Instalar Certbot

```bash
sudo apt update
sudo apt install certbot python3-certbot-nginx -y
```

### Passo 2: Obter Certificado SSL

```bash
# Parar o Nginx temporariamente
docker-compose -f docker-compose-with-nginx.yml stop nginx

# Obter certificado (substitua pelo seu domínio e email)
sudo certbot certonly --standalone -d api.seudominio.com --email seu-email@exemplo.com --agree-tos

# Ou se quiser www também:
sudo certbot certonly --standalone -d api.seudominio.com -d www.api.seudominio.com --email seu-email@exemplo.com --agree-tos
```

### Passo 3: Configurar Nginx com SSL

1. **Edite `nginx-ssl.conf` e ajuste:**
   - `server_name` com seu domínio
   - Caminhos dos certificados (geralmente `/etc/letsencrypt/live/seu-dominio.com/`)

2. **Atualize o `docker-compose-with-nginx.yml` para usar nginx-ssl.conf:**
```yaml
volumes:
  - ./nginx-ssl.conf:/etc/nginx/conf.d/default.conf:ro
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

3. **Reinicie os containers:**
```bash
docker-compose -f docker-compose-with-nginx.yml up -d
```

### Passo 4: Renovação Automática do SSL

```bash
# Testar renovação
sudo certbot renew --dry-run

# Adicionar ao crontab para renovação automática
sudo crontab -e

# Adicione esta linha (renova todo dia às 3h da manhã):
0 3 * * * certbot renew --quiet && docker-compose -f /caminho/para/projeto/docker-compose-with-nginx.yml restart nginx
```

### Passo 5: Testar HTTPS

```bash
# Teste com SSL
curl https://api.seudominio.com/

# Teste gerando imagem via HTTPS
curl -X POST "https://api.seudominio.com/txt2img" \
  -H "x-api-key: sua-chave-secreta" \
  -F "prompt=a beautiful sunset" \
  -o imagem.png
```

## 🔧 Método 3: Usando Cloudflare (Alternativa)

Se você usa Cloudflare, pode configurar SSL/TLS facilmente:

1. **Configure o DNS no Cloudflare:**
   - Adicione registro A: `api` → IP da VPS

2. **Configure SSL/TLS:**
   - Vá em SSL/TLS → Overview
   - Selecione "Full" ou "Full (strict)"

3. **Use o Nginx sem certificados locais:**
   - O Cloudflare faz o SSL/TLS para você
   - Use apenas `nginx.conf` (sem SSL)

## 📝 Exemplo Completo de Uso

### Configuração Inicial

```bash
# 1. Clone o repositório
git clone https://github.com/fabricio1905harry/api-generator.git
cd api-generator

# 2. Configure a API Key
echo "API_KEY=sua-chave-super-secreta" > .env

# 3. Edite nginx.conf com seu domínio
nano nginx.conf
# Altere: server_name api.seudominio.com;

# 4. Inicie os serviços
docker-compose -f docker-compose-with-nginx.yml up -d --build

# 5. Verifique os logs
docker-compose -f docker-compose-with-nginx.yml logs -f
```

### Consumir a API

```bash
# Via domínio HTTP
curl -X POST "http://api.seudominio.com/txt2img" \
  -H "x-api-key: sua-chave-super-secreta" \
  -F "prompt=a beautiful sunset over mountains" \
  -o output.png

# Via domínio HTTPS (se configurado SSL)
curl -X POST "https://api.seudominio.com/txt2img" \
  -H "x-api-key: sua-chave-super-secreta" \
  -F "prompt=a beautiful sunset over mountains" \
  -o output.png
```

## 🐳 Deploy no Portainer com Domínio

1. **No Portainer, crie uma stack usando `docker-compose-with-nginx.yml`**

2. **Configure as variáveis de ambiente:**
   - `API_KEY` = sua chave secreta

3. **Antes de fazer deploy, edite o `nginx.conf` no repositório:**
   - Altere `server_name _;` para `server_name api.seudominio.com;`

4. **Ou crie um volume para o nginx.conf:**
   - No Portainer, ao criar a stack, adicione um volume
   - Mapeie o arquivo `nginx.conf` local para `/etc/nginx/conf.d/default.conf`

## 🔍 Verificar Configuração

```bash
# Verificar se o DNS está correto
nslookup api.seudominio.com

# Verificar se a porta 80 está aberta
sudo netstat -tulpn | grep :80

# Ver logs do Nginx
docker logs nginx-proxy

# Ver logs da API
docker logs stable-diffusion-api

# Testar conectividade
curl -I http://api.seudominio.com
```

## 🛠️ Troubleshooting

### Erro 502 Bad Gateway

- Verifique se o container da API está rodando: `docker ps`
- Verifique os logs: `docker logs stable-diffusion-api`
- Verifique se a API está acessível internamente: `curl http://localhost:8000`

### Domínio não resolve

- Aguarde a propagação do DNS (pode levar até 48h, geralmente minutos)
- Verifique o DNS: `nslookup api.seudominio.com`
- Verifique se o registro A está correto no provedor de domínio

### SSL não funciona

- Verifique se os certificados existem: `sudo ls -la /etc/letsencrypt/live/`
- Verifique se o caminho no `nginx-ssl.conf` está correto
- Verifique os logs do Nginx: `docker logs nginx-proxy`

### Timeout na geração de imagens

- Aumente os timeouts no `nginx.conf`:
```nginx
proxy_connect_timeout 600s;
proxy_send_timeout 600s;
proxy_read_timeout 600s;
```

## 📚 Recursos Adicionais

- [Nginx Documentation](https://nginx.org/en/docs/)
- [Let's Encrypt](https://letsencrypt.org/)
- [Certbot Documentation](https://certbot.eff.org/)

