from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import Response
from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline
import torch
from PIL import Image
import io
import os

app = FastAPI(title="Stable Diffusion API")

# Verificar se CUDA está disponível
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Usando dispositivo: {device}")

# Carregar modelo txt2img
print("Carregando modelo Stable Diffusion v1.5...")
txt2img_pipeline = StableDiffusionPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
txt2img_pipeline = txt2img_pipeline.to(device)

# Carregar modelo img2img
img2img_pipeline = StableDiffusionImg2ImgPipeline.from_pretrained(
    "runwayml/stable-diffusion-v1-5",
    torch_dtype=torch.float16 if device == "cuda" else torch.float32
)
img2img_pipeline = img2img_pipeline.to(device)

print("Modelos carregados com sucesso!")


@app.get("/")
async def root():
    return {
        "message": "Stable Diffusion API",
        "device": device,
        "endpoints": ["/txt2img", "/img2img"]
    }


@app.post("/txt2img")
async def text_to_image(prompt: str = Form(...)):
    """
    Gera uma imagem a partir de um prompt de texto.
    
    Args:
        prompt: Texto descritivo da imagem desejada
    
    Returns:
        Imagem PNG gerada
    """
    try:
        print(f"Gerando imagem para o prompt: {prompt}")
        
        # Gerar imagem
        image = txt2img_pipeline(
            prompt=prompt,
            num_inference_steps=50,
            guidance_scale=7.5
        ).images[0]
        
        # Converter para PNG em bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return Response(
            content=img_byte_arr.getvalue(),
            media_type="image/png"
        )
    except Exception as e:
        return {"error": str(e)}


@app.post("/img2img")
async def image_to_image(
    prompt: str = Form(...),
    image: UploadFile = File(...),
    strength: float = Form(0.75)
):
    """
    Edita uma imagem existente baseado em um prompt.
    
    Args:
        prompt: Texto descritivo da edição desejada
        image: Arquivo de imagem a ser editado
        strength: Força da edição (0.0 a 1.0). Valores mais altos = mais mudanças
    
    Returns:
        Imagem PNG editada
    """
    try:
        print(f"Editando imagem com prompt: {prompt}")
        
        # Ler e processar imagem de entrada
        image_bytes = await image.read()
        input_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        
        # Redimensionar se necessário (Stable Diffusion espera múltiplos de 8)
        width, height = input_image.size
        width = (width // 8) * 8
        height = (height // 8) * 8
        input_image = input_image.resize((width, height))
        
        # Gerar imagem editada
        result_image = img2img_pipeline(
            prompt=prompt,
            image=input_image,
            strength=strength,
            num_inference_steps=50,
            guidance_scale=7.5
        ).images[0]
        
        # Converter para PNG em bytes
        img_byte_arr = io.BytesIO()
        result_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return Response(
            content=img_byte_arr.getvalue(),
            media_type="image/png"
        )
    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

