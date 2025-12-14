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

## 🌐 Configurar Domínio

Para acessar a API via domínio (ex: `https://api.seudominio.com`), consulte o guia completo em **[CONFIGURAR_DOMINIO.md](CONFIGURAR_DOMINIO.md)**

**Resumo rápido:**
1. Configure DNS apontando para o IP da VPS
2. Use `docker-compose-with-nginx.yml` (com Nginx como proxy reverso)
3. Edite `nginx.conf` com seu domínio
4. Deploy: `docker-compose -f docker-compose-with-nginx.yml up -d --build`

## Requisitos

- Docker e Docker Compose
- NVIDIA GPU com drivers e nvidia-container-toolkit instalados (opcional, funciona com CPU)

## Instalação

1. Instale o nvidia-container-toolkit (se ainda não tiver):
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

## Uso

### Iniciar o serviço

```bash
docker-compose up --build
```

A API estará disponível em `http://localhost:8000`

### Documentação interativa

Acesse `http://localhost:8000/docs` para ver a documentação Swagger da API.

## Endpoints

### POST /txt2img

Gera uma imagem a partir de um prompt de texto.

**Parâmetros:**
- `prompt` (form-data): Texto descritivo da imagem

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/txt2img" \
  -F "prompt=a beautiful sunset over mountains" \
  -o output.png
```

### POST /img2img

Edita uma imagem existente baseado em um prompt.

**Parâmetros:**
- `prompt` (form-data): Texto descritivo da edição
- `image` (file): Arquivo de imagem a ser editado
- `strength` (form-data, opcional): Força da edição (0.0 a 1.0, padrão: 0.75)

**Exemplo:**
```bash
curl -X POST "http://localhost:8000/img2img" \
  -F "prompt=make it look like a painting" \
  -F "image=@input.jpg" \
  -F "strength=0.8" \
  -o output.png
```

## Notas

- O primeiro uso pode demorar alguns minutos para baixar o modelo (~4GB)
- Os modelos são armazenados em cache no volume `./models_cache`
- Para usar CPU (sem GPU), remova a seção `deploy` do docker-compose.yml

