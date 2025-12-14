# 📚 Guia de Uso da API - Stable Diffusion + Gemini

## 🔐 Autenticação

Todas as requisições (exceto `/`) precisam do header de autenticação:

```
x-api-key: SUA_API_KEY_AQUI
```

## 🌐 Endpoints Disponíveis

### 1. **GET /** - Health Check
Verifica se a API está online e mostra o status do Gemini.

**URL:** `http://SEU_DOMINIO_OU_IP/` ou `http://SEU_DOMINIO_OU_IP:8000/`

**Headers:** Não requer autenticação

**Exemplo com cURL:**
```bash
curl http://seu-dominio.com/
```

**Resposta:**
```json
{
  "status": "online",
  "auth": "enabled",
  "gemini": "enabled"
}
```

---

### 2. **POST /txt2img** - Gerar Imagem a partir de Texto
Gera uma imagem usando Stable Diffusion. Opcionalmente usa Gemini para melhorar o prompt.

**URL:** `http://SEU_DOMINIO_OU_IP/txt2img` ou `http://SEU_DOMINIO_OU_IP:8000/txt2img`

**Headers:**
```
x-api-key: SUA_API_KEY_AQUI
Content-Type: multipart/form-data
```

**Body (form-data):**
- `prompt` (string, obrigatório): Descrição da imagem que você quer gerar
- `use_ai_enhance` (boolean, opcional): Se deve usar Gemini para melhorar o prompt (padrão: `true`)

**Exemplo com cURL:**
```bash
curl -X POST "http://seu-dominio.com/txt2img" \
  -H "x-api-key: sua-chave-api-aqui" \
  -F "prompt=a beautiful sunset over mountains" \
  -F "use_ai_enhance=true" \
  -o imagem_gerada.png
```

**Exemplo sem melhoramento do Gemini:**
```bash
curl -X POST "http://seu-dominio.com/txt2img" \
  -H "x-api-key: sua-chave-api-aqui" \
  -F "prompt=a beautiful sunset over mountains" \
  -F "use_ai_enhance=false" \
  -o imagem_gerada.png
```

**Resposta:** Arquivo PNG (imagem gerada)

---

### 3. **POST /img2img** - Editar Imagem Existente
Edita uma imagem existente baseado em um prompt.

**URL:** `http://SEU_DOMINIO_OU_IP/img2img` ou `http://SEU_DOMINIO_OU_IP:8000/img2img`

**Headers:**
```
x-api-key: SUA_API_KEY_AQUI
Content-Type: multipart/form-data
```

**Body (form-data):**
- `prompt` (string, obrigatório): Descrição da edição que você quer fazer
- `file` (file, obrigatório): Arquivo de imagem a ser editado (JPG, PNG, etc.)
- `strength` (float, opcional): Força da edição de 0.0 a 1.0 (padrão: 0.75)
  - `0.0` = mantém a imagem original
  - `1.0` = transforma completamente a imagem

**Exemplo com cURL:**
```bash
curl -X POST "http://seu-dominio.com/img2img" \
  -H "x-api-key: sua-chave-api-aqui" \
  -F "prompt=make it look like a painting" \
  -F "file=@/caminho/para/sua/imagem.jpg" \
  -F "strength=0.8" \
  -o imagem_editada.png
```

**Resposta:** Arquivo PNG (imagem editada)

---

## 💻 Exemplos em Diferentes Linguagens

### Python (requests)
```python
import requests

# Configurações
API_URL = "http://seu-dominio.com"
API_KEY = "sua-chave-api-aqui"

# Headers
headers = {
    "x-api-key": API_KEY
}

# 1. Health Check
response = requests.get(f"{API_URL}/")
print(response.json())

# 2. Gerar Imagem (txt2img)
data = {
    "prompt": "a beautiful sunset over mountains",
    "use_ai_enhance": True
}
response = requests.post(
    f"{API_URL}/txt2img",
    headers=headers,
    data=data
)
with open("imagem_gerada.png", "wb") as f:
    f.write(response.content)

# 3. Editar Imagem (img2img)
files = {
    "file": open("imagem_original.jpg", "rb")
}
data = {
    "prompt": "make it look like a painting",
    "strength": 0.8
}
response = requests.post(
    f"{API_URL}/img2img",
    headers=headers,
    files=files,
    data=data
)
with open("imagem_editada.png", "wb") as f:
    f.write(response.content)
```

### JavaScript (fetch)
```javascript
const API_URL = "http://seu-dominio.com";
const API_KEY = "sua-chave-api-aqui";

// 1. Health Check
fetch(`${API_URL}/`)
  .then(res => res.json())
  .then(data => console.log(data));

// 2. Gerar Imagem (txt2img)
const formData = new FormData();
formData.append("prompt", "a beautiful sunset over mountains");
formData.append("use_ai_enhance", "true");

fetch(`${API_URL}/txt2img`, {
  method: "POST",
  headers: {
    "x-api-key": API_KEY
  },
  body: formData
})
  .then(res => res.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "imagem_gerada.png";
    a.click();
  });

// 3. Editar Imagem (img2img)
const formData = new FormData();
formData.append("prompt", "make it look like a painting");
formData.append("strength", "0.8");
formData.append("file", fileInput.files[0]); // fileInput é um <input type="file">

fetch(`${API_URL}/img2img`, {
  method: "POST",
  headers: {
    "x-api-key": API_KEY
  },
  body: formData
})
  .then(res => res.blob())
  .then(blob => {
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "imagem_editada.png";
    a.click();
  });
```

### Node.js (axios)
```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const API_URL = "http://seu-dominio.com";
const API_KEY = "sua-chave-api-aqui";

// Headers
const headers = {
  "x-api-key": API_KEY
};

// 1. Health Check
axios.get(`${API_URL}/`)
  .then(res => console.log(res.data));

// 2. Gerar Imagem (txt2img)
const formData = new FormData();
formData.append("prompt", "a beautiful sunset over mountains");
formData.append("use_ai_enhance", "true");

axios.post(`${API_URL}/txt2img`, formData, {
  headers: {
    ...headers,
    ...formData.getHeaders()
  },
  responseType: 'arraybuffer'
})
  .then(res => {
    fs.writeFileSync("imagem_gerada.png", res.data);
  });

// 3. Editar Imagem (img2img)
const formData = new FormData();
formData.append("prompt", "make it look like a painting");
formData.append("strength", "0.8");
formData.append("file", fs.createReadStream("imagem_original.jpg"));

axios.post(`${API_URL}/img2img`, formData, {
  headers: {
    ...headers,
    ...formData.getHeaders()
  },
  responseType: 'arraybuffer'
})
  .then(res => {
    fs.writeFileSync("imagem_editada.png", res.data);
  });
```

---

## 📝 Notas Importantes

1. **Autenticação**: Sempre inclua o header `x-api-key` em todas as requisições (exceto `/`)

2. **Formato de Dados**: Use `multipart/form-data` para os endpoints `/txt2img` e `/img2img`

3. **Tamanho da Imagem**: As imagens são geradas/editadas em 512x512 pixels

4. **Tempo de Resposta**: A primeira requisição pode demorar mais (carregamento do modelo). Requisições subsequentes são mais rápidas.

5. **Gemini**: Se `GOOGLE_API_KEY` não estiver configurada, o parâmetro `use_ai_enhance` será ignorado

6. **Erros Comuns**:
   - `403 Forbidden`: API Key inválida ou ausente
   - `422 Unprocessable Entity`: Parâmetros inválidos ou faltando
   - `500 Internal Server Error`: Erro no servidor (verifique os logs)

---

## 🔗 Documentação Interativa

Se a API estiver rodando, você pode acessar a documentação Swagger em:
- `http://seu-dominio.com/docs` (com Nginx)
- `http://seu-dominio.com:8000/docs` (direto na porta)

Lá você pode testar os endpoints diretamente no navegador!

