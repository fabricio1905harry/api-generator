# 🐳 Deploy no Portainer via Stack

Guia completo para fazer deploy usando Stack no Portainer.

## 📋 Pré-requisitos

- Portainer instalado e acessível
- Acesso admin no Portainer
- (Opcional) GPU NVIDIA configurada

## 🚀 Método 1: Stack Simples (CPU)

### Passo 1: Acessar Portainer

1. Acesse o Portainer (geralmente `http://seu-ip:9000`)
2. Faça login
3. Vá em **"Stacks"** no menu lateral
4. Clique em **"Add stack"**

### Passo 2: Configurar Stack

**Nome da Stack:**
```
stable-diffusion-api
```

**Build method:** Selecione **"Repository"**

**Repository URL:**
```
https://github.com/fabricio1905harry/api-generator.git
```

**Repository reference:** `main`

**Compose path:** `portainer-stack-completo.yml`

### Passo 3: Variáveis de Ambiente

Clique em **"Environment variables"** e adicione:

| Key | Value |
|-----|-------|
| `API_KEY` | `sua-chave-secreta-super-forte-aqui` |

### Passo 4: Deploy

Clique em **"Deploy the stack"**

---

## 🎮 Método 2: Stack com GPU

Siga os mesmos passos do Método 1, mas use:

**Compose path:** `portainer-stack-gpu.yml`

**Importante:** Certifique-se de que a GPU está disponível no Portainer:
- Vá em **"Settings"** → **"Environments"**
- Verifique se a GPU está habilitada

---

## 🌐 Método 3: Stack com Domínio (Nginx)

### Passo 1: Preparar Nginx Config

1. Na VPS, crie o arquivo `nginx.conf`:
```bash
nano /caminho/para/nginx.conf
```

2. Cole este conteúdo (ajuste o `server_name`):
```nginx
server {
    listen 80;
    server_name api.seudominio.com;

    client_max_body_size 100M;

    location / {
        proxy_pass http://stable-diffusion-api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

### Passo 2: Criar Stack no Portainer

1. Vá em **"Stacks"** → **"Add stack"**
2. **Nome:** `stable-diffusion-api-nginx`
3. **Build method:** **"Repository"**
4. **Repository URL:** `https://github.com/fabricio1905harry/api-generator.git`
5. **Compose path:** `portainer-stack-com-domínio.yml`

### Passo 3: Configurar Volume do Nginx

1. Vá em **"Volumes"**
2. Edite o volume `nginx_config`
3. Configure o caminho para o arquivo `nginx.conf` criado

### Passo 4: Variáveis de Ambiente

Adicione:
- `API_KEY` = `sua-chave-secreta`

### Passo 5: Deploy

Clique em **"Deploy the stack"**

---

## 📝 Método 4: Stack via Web Editor (Mais Controle)

### Passo 1: Copiar Conteúdo

Copie o conteúdo de um dos arquivos:
- `portainer-stack-completo.yml` (CPU)
- `portainer-stack-gpu.yml` (GPU)
- `portainer-stack-com-domínio.yml` (com Nginx)

### Passo 2: Criar Stack

1. No Portainer, vá em **"Stacks"** → **"Add stack"**
2. **Nome:** `stable-diffusion-api`
3. **Build method:** Selecione **"Web editor"**
4. Cole o conteúdo do arquivo YAML
5. **Importante:** Substitua `${API_KEY}` por sua chave ou configure como variável

### Passo 3: Variáveis de Ambiente

Se usar `${API_KEY}`, adicione nas variáveis de ambiente:
- Key: `API_KEY`
- Value: `sua-chave-secreta`

### Passo 4: Deploy

Clique em **"Deploy the stack"**

---

## 🔧 Configuração Avançada

### Usar Imagem Pré-construída

Se você já construiu a imagem localmente:

1. **Tag a imagem:**
```bash
docker tag minha-api-cpu:latest seu-registry/minha-api-cpu:latest
```

2. **Push para registry:**
```bash
docker push seu-registry/minha-api-cpu:latest
```

3. **No Portainer, use:**
```yaml
services:
  stable-diffusion-api:
    image: seu-registry/minha-api-cpu:latest
    # Remova a seção 'build'
```

### Build Local na VPS

Se preferir fazer build na VPS antes:

1. **Na VPS:**
```bash
git clone https://github.com/fabricio1905harry/api-generator.git
cd api-generator
docker build -t minha-api-cpu:latest .
```

2. **No Portainer, use o stack file com:**
```yaml
services:
  stable-diffusion-api:
    image: minha-api-cpu:latest
    # Remova ou comente a seção 'build'
```

---

## ✅ Verificar Deploy

### Ver Status

1. Vá em **"Containers"**
2. Procure por `stable-diffusion-api`
3. Verifique se está "Running"

### Ver Logs

1. Clique no container `stable-diffusion-api`
2. Vá na aba **"Logs"**
3. Verifique se não há erros

### Testar API

```bash
# Status
curl http://seu-ip:8000/

# Gerar imagem
curl -X POST "http://seu-ip:8000/txt2img" \
  -H "x-api-key: sua-chave-secreta" \
  -F "prompt=a beautiful sunset" \
  -o imagem.png
```

---

## 🔄 Atualizar Stack

### Método 1: Via Portainer

1. Vá em **"Stacks"**
2. Clique na stack `stable-diffusion-api`
3. Clique em **"Editor"**
4. Faça as alterações
5. Clique em **"Update the stack"**

### Método 2: Via Git

1. No repositório, faça as alterações
2. No Portainer, vá na stack
3. Clique em **"Editor"**
4. Clique em **"Pull and redeploy"** (se configurado com repositório)

---

## 🛠️ Troubleshooting

### Stack não inicia

- Verifique os logs no Portainer
- Verifique se a porta 8000 está disponível
- Verifique se a API_KEY foi configurada

### Erro de build

- Verifique se o repositório está acessível
- Verifique se o caminho do dockerfile está correto
- Tente fazer build manual na VPS primeiro

### Erro de GPU

- Verifique se nvidia-container-toolkit está instalado
- Verifique se a GPU está disponível no Portainer
- Use `portainer-stack-completo.yml` (CPU) se não tiver GPU

### Volume não funciona

- Verifique se o caminho do volume está correto
- Verifique permissões do diretório
- Use volumes nomeados em vez de bind mounts

---

## 📚 Arquivos Disponíveis

- **`portainer-stack-completo.yml`** - Stack CPU (recomendado para começar)
- **`portainer-stack-gpu.yml`** - Stack com GPU NVIDIA
- **`portainer-stack-com-domínio.yml`** - Stack com Nginx para domínio

---

## 🎉 Pronto!

Sua API está rodando no Portainer! Acesse:
- **API:** `http://seu-ip:8000`
- **Docs:** `http://seu-ip:8000/docs`

