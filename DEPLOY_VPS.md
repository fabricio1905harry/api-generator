# 🚀 Guia Completo de Deploy na VPS

Este guia mostra passo a passo como fazer deploy da API na sua VPS.

## 📋 Pré-requisitos

- VPS com acesso SSH
- Acesso root ou sudo
- (Opcional) GPU NVIDIA

## 🔧 Passo 1: Conectar na VPS

```bash
ssh usuario@seu-ip-vps
```

## 📦 Passo 2: Instalar Docker e Docker Compose

### Atualizar o sistema
```bash
sudo apt update && sudo apt upgrade -y
```

### Instalar Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### Instalar Docker Compose
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Reiniciar sessão (para aplicar mudanças do Docker)
```bash
newgrp docker
# OU faça logout e login novamente
```

### Verificar instalação
```bash
docker --version
docker-compose --version
```

## 🎮 Passo 3: Instalar NVIDIA Container Toolkit (Se tiver GPU)

```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Verificar GPU
```bash
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```

## 📥 Passo 4: Clonar o Repositório

```bash
cd ~
git clone https://github.com/fabricio1905harry/api-generator.git
cd api-generator
```

## 🔐 Passo 5: Configurar API Key

```bash
# Criar arquivo .env
echo "API_KEY=sua-chave-secreta-super-forte-aqui" > .env

# OU editar manualmente
nano .env
```

**Conteúdo do arquivo `.env`:**
```
API_KEY=sua-chave-secreta-super-forte-aqui
```

## 🌐 Passo 6: Escolher Método de Deploy

### Opção A: Deploy Simples (sem domínio, apenas IP)

**Com GPU:**
```bash
docker-compose up -d --build
```

**Sem GPU (CPU apenas):**
```bash
docker-compose -f docker-compose.cpu.yml up -d --build
```

**Acesse:** `http://SEU-IP-VPS:8000`

---

### Opção B: Deploy com Domínio (Recomendado)

#### 6.1. Configurar DNS

No seu provedor de domínio (ex: Cloudflare, Namecheap), configure:
- **Tipo:** A
- **Nome:** `api` (ou `@` para raiz)
- **Valor:** IP da sua VPS
- **TTL:** 3600

Exemplo: `api.seudominio.com` → IP da VPS

#### 6.2. Editar nginx.conf

```bash
nano nginx.conf
```

Altere a linha:
```nginx
server_name _;
```

Para:
```nginx
server_name api.seudominio.com;
```

Salve e saia (Ctrl+X, Y, Enter)

#### 6.3. Configurar Firewall

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

#### 6.4. Fazer Deploy

**Com GPU:**
```bash
docker-compose -f docker-compose-with-nginx.yml up -d --build
```

**Sem GPU:**
```bash
docker-compose -f docker-compose-with-nginx-cpu.yml up -d --build
```

**Acesse:** `http://api.seudominio.com`

---

## ✅ Passo 7: Verificar se Está Funcionando

### Ver status dos containers
```bash
docker ps
```

### Ver logs
```bash
# Logs da API
docker logs stable-diffusion-api -f

# Logs do Nginx (se usar domínio)
docker logs nginx-proxy -f
```

### Testar API

**Sem domínio (via IP):**
```bash
# Status
curl http://SEU-IP-VPS:8000/

# Gerar imagem
curl -X POST "http://SEU-IP-VPS:8000/txt2img" \
  -H "x-api-key: sua-chave-secreta-super-forte-aqui" \
  -F "prompt=a beautiful sunset" \
  -o imagem.png
```

**Com domínio:**
```bash
# Status
curl http://api.seudominio.com/

# Gerar imagem
curl -X POST "http://api.seudominio.com/txt2img" \
  -H "x-api-key: sua-chave-secreta-super-forte-aqui" \
  -F "prompt=a beautiful sunset" \
  -o imagem.png
```

## 🔒 Passo 8: Configurar SSL/HTTPS (Opcional mas Recomendado)

### 8.1. Instalar Certbot

```bash
sudo apt install certbot python3-certbot-nginx -y
```

### 8.2. Parar Nginx temporariamente

```bash
docker-compose -f docker-compose-with-nginx.yml stop nginx
```

### 8.3. Obter Certificado SSL

```bash
sudo certbot certonly --standalone -d api.seudominio.com --email seu-email@exemplo.com --agree-tos
```

### 8.4. Configurar Nginx com SSL

Edite `nginx-ssl.conf`:
```bash
nano nginx-ssl.conf
```

Ajuste:
- `server_name` com seu domínio
- Caminhos dos certificados (geralmente `/etc/letsencrypt/live/api.seudominio.com/`)

### 8.5. Atualizar docker-compose

Edite `docker-compose-with-nginx.yml` e descomente as linhas de SSL:
```yaml
volumes:
  - ./nginx-ssl.conf:/etc/nginx/conf.d/default.conf:ro
  - /etc/letsencrypt:/etc/letsencrypt:ro
```

### 8.6. Reiniciar

```bash
docker-compose -f docker-compose-with-nginx.yml up -d
```

### 8.7. Renovação Automática

```bash
# Testar renovação
sudo certbot renew --dry-run

# Adicionar ao crontab
sudo crontab -e

# Adicione esta linha:
0 3 * * * certbot renew --quiet && docker-compose -f /home/usuario/api-generator/docker-compose-with-nginx.yml restart nginx
```

## 🛠️ Comandos Úteis

### Gerenciar o Serviço

```bash
# Parar
docker-compose down
# OU com Nginx
docker-compose -f docker-compose-with-nginx.yml down

# Reiniciar
docker-compose restart
# OU com Nginx
docker-compose -f docker-compose-with-nginx.yml restart

# Ver logs
docker-compose logs -f
# OU com Nginx
docker-compose -f docker-compose-with-nginx.yml logs -f

# Reconstruir após atualizações
docker-compose up -d --build
# OU com Nginx
docker-compose -f docker-compose-with-nginx.yml up -d --build
```

### Atualizar Código

```bash
cd ~/api-generator
git pull
docker-compose -f docker-compose-with-nginx.yml up -d --build
```

### Limpar Cache de Modelos

```bash
docker-compose down -v
# Isso remove o volume com os modelos (será baixado novamente)
```

## 📊 Monitoramento

### Ver uso de recursos
```bash
docker stats
```

### Ver espaço em disco
```bash
df -h
docker system df
```

### Ver logs em tempo real
```bash
docker-compose logs -f stable-diffusion-api
```

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs detalhados
docker logs stable-diffusion-api

# Verificar se a porta está em uso
sudo netstat -tulpn | grep :8000

# Verificar se há erros no build
docker-compose build --no-cache
```

### Erro 502 Bad Gateway (com Nginx)

```bash
# Verificar se a API está rodando
docker ps | grep stable-diffusion-api

# Testar API diretamente
curl http://localhost:8000/

# Ver logs do Nginx
docker logs nginx-proxy
```

### Domínio não resolve

```bash
# Verificar DNS
nslookup api.seudominio.com
dig api.seudominio.com

# Aguardar propagação (pode levar até 48h, geralmente minutos)
```

### Erro de GPU

```bash
# Verificar se GPU está disponível
nvidia-smi

# Verificar se nvidia-container-toolkit está instalado
docker run --rm --gpus all nvidia/cuda:11.0.3-base-ubuntu20.04 nvidia-smi
```

### Timeout na geração

Aumente os timeouts no `nginx.conf`:
```nginx
proxy_connect_timeout 600s;
proxy_send_timeout 600s;
proxy_read_timeout 600s;
```

## 📚 Próximos Passos

- ✅ API funcionando
- ✅ Domínio configurado (opcional)
- ✅ SSL/HTTPS configurado (opcional)
- 📖 Consulte `CONFIGURAR_DOMINIO.md` para mais detalhes sobre domínio
- 📖 Consulte `DEPLOY_PORTAINER.md` para deploy via Portainer

## 🎉 Pronto!

Sua API está no ar! Acesse:
- **Sem domínio:** `http://SEU-IP-VPS:8000`
- **Com domínio:** `http://api.seudominio.com`
- **Documentação:** `http://SEU-IP-VPS:8000/docs` ou `http://api.seudominio.com/docs`

