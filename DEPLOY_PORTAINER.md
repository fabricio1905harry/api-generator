# 🐳 Deploy no Portainer - Guia Completo

Este guia mostra como fazer deploy da Stable Diffusion API usando Portainer.

## 📋 Pré-requisitos

- Portainer instalado e acessível
- Acesso ao Portainer (admin)
- Docker e Docker Compose instalados na VPS
- (Opcional) GPU NVIDIA com nvidia-container-toolkit

## 🚀 Método 1: Deploy via Stack (Recomendado)

### Passo 1: Preparar o Repositório

1. **Clone o repositório na sua VPS:**
```bash
git clone https://github.com/fabricio1905harry/api-generator.git
cd api-generator
```

2. **Crie um arquivo `.env` com sua API Key:**
```bash
echo "API_KEY=sua-chave-secreta-super-forte-aqui" > .env
```

### Passo 2: Criar Stack no Portainer

1. **Acesse o Portainer** (geralmente `http://seu-ip:9000`)

2. **Vá em "Stacks"** no menu lateral

3. **Clique em "Add stack"**

4. **Configure a stack:**
   - **Name:** `stable-diffusion-api`
   - **Build method:** Selecione "Repository"
   - **Repository URL:** `https://github.com/fabricio1905harry/api-generator.git`
   - **Repository reference:** `main`
   - **Compose path:** `portainer-stack.yml` (ou `portainer-stack-cpu.yml` se não tiver GPU)

5. **Adicione variáveis de ambiente:**
   - Clique em "Environment variables"
   - Adicione: `API_KEY` = `sua-chave-secreta-super-forte-aqui`

6. **Clique em "Deploy the stack"**

### Passo 3: Verificar Deploy

1. Vá em **"Containers"** no menu lateral
2. Procure por `stable-diffusion-api`
3. Verifique se está rodando (status "Running")
4. Clique no container e veja os logs

## 🔧 Método 2: Deploy via Container (Manual)

### Passo 1: Build da Imagem

1. **No Portainer, vá em "Images"**

2. **Clique em "Build a new image"**

3. **Configure:**
   - **Image name:** `stable-diffusion-api:latest`
   - **Build method:** "Get image(s) from Docker Hub and pull"
   - **Image:** Deixe vazio (vamos fazer build local)

   **OU use via terminal na VPS:**
```bash
cd /caminho/para/api-generator
docker build -t stable-diffusion-api:latest .
```

### Passo 2: Criar Container

1. **No Portainer, vá em "Containers"**

2. **Clique em "Add container"**

3. **Configure:**
   - **Name:** `stable-diffusion-api`
   - **Image:** `stable-diffusion-api:latest`
   - **Publish all exposed ports:** ✅ (marca esta opção)
   - **Port mapping:** `8000:8000`

4. **Vá em "Env" e adicione:**
   - `API_KEY` = `sua-chave-secreta-super-forte-aqui`
   - `NVIDIA_VISIBLE_DEVICES` = `all` (se tiver GPU)

5. **Vá em "Volumes" e adicione:**
   - **Volume mapping:** `/root/.cache/huggingface` → `models_cache` (named volume)

6. **Vá em "Runtime & Resources" (se tiver GPU):**
   - Marque "Use GPU"
   - Selecione sua GPU

7. **Vá em "Restart policy":**
   - Selecione "Unless stopped"

8. **Clique em "Deploy the container"**

## 📝 Método 3: Usar docker-compose.yml via Portainer

### Passo 1: Upload do docker-compose.yml

1. **Clone o repositório na VPS:**
```bash
git clone https://github.com/fabricio1905harry/api-generator.git
cd api-generator
```

2. **Crie o arquivo `.env`:**
```bash
echo "API_KEY=sua-chave-secreta-super-forte-aqui" > .env
```

3. **No Portainer, vá em "Stacks"**

4. **Clique em "Add stack"**

5. **Configure:**
   - **Name:** `stable-diffusion-api`
   - **Build method:** "Web editor"
   - **Compose path:** Cole o conteúdo do `docker-compose.yml`

6. **Adicione variáveis de ambiente:**
   - `API_KEY` = `sua-chave-secreta-super-forte-aqui`

7. **Clique em "Deploy the stack"**

## 🔐 Configurar API Key

### Opção 1: Variável de Ambiente no Portainer

Ao criar a stack/container, adicione:
- **Key:** `API_KEY`
- **Value:** `sua-chave-secreta-super-forte-aqui`

### Opção 2: Arquivo .env

1. Crie um arquivo `.env` na VPS:
```bash
echo "API_KEY=sua-chave-secreta-super-forte-aqui" > .env
```

2. No Portainer, ao criar a stack, use o caminho do arquivo `.env`

## 🧪 Testar a API

Após o deploy, teste os endpoints:

```bash
# Verificar status (não requer autenticação)
curl http://SEU-IP-VPS:8000/

# Gerar imagem (requer API Key)
curl -X POST "http://SEU-IP-VPS:8000/generate" \
  -H "x-api-key: sua-chave-secreta-super-forte-aqui" \
  -F "prompt=a beautiful sunset over mountains" \
  -o output.png

# Editar imagem
curl -X POST "http://SEU-IP-VPS:8000/edit" \
  -H "x-api-key: sua-chave-secreta-super-forte-aqui" \
  -F "prompt=make it look like a painting" \
  -F "file=@input.jpg" \
  -F "strength=0.8" \
  -o output.png
```

## 📊 Monitoramento

### Ver Logs

1. No Portainer, vá em **"Containers"**
2. Clique no container `stable-diffusion-api`
3. Vá na aba **"Logs"**

### Verificar Status

1. Vá em **"Containers"**
2. Verifique se o status está "Running"
3. Verifique o uso de recursos (CPU, RAM, GPU)

## 🔄 Atualizar a Aplicação

### Via Stack

1. No Portainer, vá em **"Stacks"**
2. Clique na stack `stable-diffusion-api`
3. Clique em **"Editor"**
4. Faça as alterações necessárias
5. Clique em **"Update the stack"**

### Via Git Pull

1. Na VPS, vá para o diretório do projeto:
```bash
cd /caminho/para/api-generator
git pull
```

2. No Portainer, recrie a stack ou faça rebuild da imagem

## 🛠️ Troubleshooting

### Container não inicia

- Verifique os logs no Portainer
- Verifique se a porta 8000 está disponível
- Verifique se a API_KEY foi configurada

### Erro de GPU

- Se não tiver GPU, use `portainer-stack-cpu.yml`
- Verifique se o nvidia-container-toolkit está instalado
- No Portainer, verifique se a GPU está disponível em "Runtime & Resources"

### Modelo não carrega

- Verifique o volume `models_cache`
- O primeiro uso pode demorar para baixar o modelo (~4GB)
- Verifique os logs para ver o progresso do download

### Erro 403 (Acesso negado)

- Verifique se a API_KEY está configurada corretamente
- Verifique se está enviando o header `x-api-key` nas requisições
- A API_KEY no container deve ser a mesma usada nas requisições

## 📚 Recursos Adicionais

- **Documentação da API:** `http://SEU-IP-VPS:8000/docs`
- **Repositório:** https://github.com/fabricio1905harry/api-generator
- **Portainer Docs:** https://docs.portainer.io/

