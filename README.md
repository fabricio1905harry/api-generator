# Stable Diffusion API com FastAPI

API REST para geração e edição de imagens usando Stable Diffusion v1.5.

## 🚀 Como publicar no GitHub

1. **Crie um repositório no GitHub** (via web interface)

2. **Inicialize o Git no projeto** (se ainda não fez):
```bash
git init
```

3. **Adicione todos os arquivos**:
```bash
git add .
```

4. **Faça o primeiro commit**:
```bash
git commit -m "Initial commit: Stable Diffusion API com FastAPI"
```

5. **Conecte ao repositório remoto** (substitua `seu-usuario` e `nome-do-repo`):
```bash
git remote add origin https://github.com/seu-usuario/nome-do-repo.git
```

6. **Envie para o GitHub**:
```bash
git branch -M main
git push -u origin main
```

**Nota**: Se usar autenticação via token, você precisará usar:
```bash
git remote add origin https://seu-token@github.com/seu-usuario/nome-do-repo.git
```

## 🐳 Deploy no Portainer

Para fazer deploy usando Portainer, consulte o guia completo em **[DEPLOY_PORTAINER.md](DEPLOY_PORTAINER.md)**

**Resumo rápido:**
1. Acesse o Portainer
2. Vá em "Stacks" → "Add stack"
3. Use o arquivo `portainer-stack.yml` (com GPU) ou `portainer-stack-cpu.yml` (sem GPU)
4. Configure a variável de ambiente `API_KEY`
5. Deploy!

## 🖥️ Deploy na VPS

### Pré-requisitos na VPS

1. **Conecte-se à sua VPS via SSH:**
```bash
ssh usuario@seu-ip-vps
```

2. **Atualize o sistema:**
```bash
sudo apt update && sudo apt upgrade -y
```

3. **Instale Docker e Docker Compose:**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Reiniciar sessão (ou fazer logout/login)
newgrp docker
```

4. **Se tiver GPU NVIDIA, instale nvidia-container-toolkit:**
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

### Deploy do Projeto

1. **Clone o repositório:**
```bash
git clone https://github.com/fabricio1905harry/api-generator.git
cd api-generator
```

2. **Configure a API Key:**
```bash
# Crie um arquivo .env ou exporte a variável
export API_KEY="sua-chave-secreta-aqui"
```

3. **Inicie o serviço:**

**Opção A - Com GPU (recomendado):**
```bash
# Modo interativo (para ver logs)
docker-compose up --build

# Modo background (recomendado para produção)
docker-compose up -d --build
```

**Opção B - Sem GPU (CPU apenas):**
```bash
docker-compose -f docker-compose.cpu.yml up -d --build
```

**Opção C - Script automatizado:**
```bash
chmod +x deploy.sh
./deploy.sh
```

4. **Verifique se está rodando:**
```bash
docker-compose ps
docker-compose logs -f
```

5. **A API estará disponível em:**
- `http://SEU-IP-VPS:8000`
- `http://SEU-IP-VPS:8000/docs` (documentação Swagger)

### Consumir a API da VPS

**De qualquer lugar, use o IP da sua VPS:**

```bash
# Gerar imagem
curl -X POST "http://SEU-IP-VPS:8000/generate" \
  -H "x-api-key: sua-chave-secreta-aqui" \
  -F "prompt=a beautiful sunset over mountains" \
  -o output.png

# Editar imagem
curl -X POST "http://SEU-IP-VPS:8000/edit" \
  -H "x-api-key: sua-chave-secreta-aqui" \
  -F "prompt=make it look like a painting" \
  -F "file=@input.jpg" \
  -F "strength=0.8" \
  -o output.png
```

### Gerenciar o Serviço

```bash
# Parar o serviço
docker-compose down

# Parar e remover volumes (limpa cache de modelos)
docker-compose down -v

# Ver logs
docker-compose logs -f

# Reiniciar
docker-compose restart

# Atualizar código (após git pull)
docker-compose up -d --build
```

### Configurar Firewall (se necessário)

```bash
# Permitir porta 8000
sudo ufw allow 8000/tcp
sudo ufw reload
```

## Requisitos

- Docker e Docker Compose
- NVIDIA GPU com drivers e nvidia-container-toolkit instalados (opcional, funciona com CPU também)

## Instalação Local

1. Instale o nvidia-container-toolkit (se ainda não tiver):
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

## Uso

### Configurar API Key

Antes de iniciar o serviço, configure a variável de ambiente `API_KEY`:

**No Linux/Mac:**
```bash
export API_KEY="sua-chave-secreta-aqui"
```

**No Windows (PowerShell):**
```powershell
$env:API_KEY="sua-chave-secreta-aqui"
```

**Ou crie um arquivo `.env` na raiz do projeto:**
```
API_KEY=sua-chave-secreta-aqui
```

E atualize o `docker-compose.yml` para usar o arquivo `.env`:
```yaml
env_file:
  - .env
```

### Iniciar o serviço

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`

### Documentação interativa

Acesse `http://localhost:8000/docs` para ver a documentação Swagger da API.

## Endpoints

### GET /

Verifica o status da API (não requer autenticação).

**Resposta:**
```json
{
  "status": "online",
  "auth": "enabled"
}
```

### POST /generate

Gera uma imagem a partir de um prompt de texto.

**Autenticação:** Requer header `x-api-key` com a chave configurada

**Parâmetros:**
- `prompt` (form-data): Texto descritivo da imagem

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/generate" \
  -H "x-api-key: sua-chave-secreta-aqui" \
  -F "prompt=a beautiful sunset over mountains" \
  -o output.png
```

### POST /edit

Edita uma imagem existente baseado em um prompt.

**Autenticação:** Requer header `x-api-key` com a chave configurada

**Parâmetros:**
- `prompt` (form-data): Texto descritivo da edição
- `file` (file): Arquivo de imagem a ser editado
- `strength` (form-data, opcional): Força da edição (0.0 a 1.0, padrão: 0.75)

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/edit" \
  -H "x-api-key: sua-chave-secreta-aqui" \
  -F "prompt=make it look like a painting" \
  -F "file=@input.jpg" \
  -F "strength=0.8" \
  -o output.png
```

## Notas

- O primeiro uso pode demorar alguns minutos para baixar o modelo (~4GB)
- Os modelos são armazenados em cache no volume `./models_cache`
- Para usar CPU (sem GPU), use `docker-compose.cpu.yml` ou remova a seção `deploy` do docker-compose.yml
- A geração de imagens é mais rápida com GPU, mas funciona com CPU (mais lento)
- Certifique-se de ter pelo menos 8GB de RAM disponível

