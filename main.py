import os

from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Security

from fastapi.security.api_key import APIKeyHeader

from fastapi.responses import Response

from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

import torch

from io import BytesIO

from PIL import Image



app = FastAPI(title="API Nano Banana (Secure)")



# --- CONFIGURAÇÃO DE SEGURANÇA ---

API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)



# Pega a senha das variáveis de ambiente do Docker

SERVER_API_KEY = os.getenv("API_KEY")



async def get_api_key(api_key_header: str = Security(api_key_header)):

    if api_key_header == SERVER_API_KEY:

        return api_key_header

    else:

        raise HTTPException(status_code=403, detail="Acesso negado: API Key inválida")



# --- CARREGAMENTO DO MODELO ---

device = "cuda" if torch.cuda.is_available() else "cpu"

# Usando float16 para economizar VRAM

pipe_txt = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if device=="cuda" else torch.float32)

pipe_txt.to(device)



pipe_img = StableDiffusionImg2ImgPipeline(

    vae=pipe_txt.vae,

    text_encoder=pipe_txt.text_encoder,

    tokenizer=pipe_txt.tokenizer,

    unet=pipe_txt.unet,

    scheduler=pipe_txt.scheduler,

    safety_checker=pipe_txt.safety_checker,

    feature_extractor=pipe_txt.feature_extractor,

).to(device)



@app.get("/")

def health_check():

    return {"status": "online", "auth": "enabled"}



# --- ROTAS PROTEGIDAS (Adicionamos dependencies=[Depends(get_api_key)]) ---



@app.post("/generate", dependencies=[Depends(get_api_key)])

async def generate_image(prompt: str = Form(...)):

    image = pipe_txt(prompt).images[0]

    img_byte_arr = BytesIO()

    image.save(img_byte_arr, format='PNG')

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")



@app.post("/edit", dependencies=[Depends(get_api_key)])

async def edit_image(prompt: str = Form(...), file: UploadFile = File(...), strength: float = Form(0.75)):

    input_image = Image.open(BytesIO(await file.read())).convert("RGB")

    input_image = input_image.resize((512, 512))

    image = pipe_img(prompt=prompt, image=input_image, strength=strength).images[0]

    img_byte_arr = BytesIO()

    image.save(img_byte_arr, format='PNG')

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")

