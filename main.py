import os

import google.generativeai as genai

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Security, Depends

from fastapi.security.api_key import APIKeyHeader

from fastapi.responses import Response

from diffusers import StableDiffusionPipeline, StableDiffusionImg2ImgPipeline

import torch

from io import BytesIO

from PIL import Image



app = FastAPI(title="API Stable Diffusion + Gemini")



# --- SEGURANÇA ---

API_KEY_NAME = "x-api-key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

SERVER_API_KEY = os.getenv("API_KEY") # Senha da sua API

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") # Chave do Google



# Configura o Google Gemini se a chave existir

if GOOGLE_API_KEY:

    genai.configure(api_key=GOOGLE_API_KEY)



async def get_api_key(api_key_header: str = Security(api_key_header)):

    if api_key_header == SERVER_API_KEY:

        return api_key_header

    raise HTTPException(status_code=403, detail="API Key Inválida")



# --- CARREGAR MODELO (Nano Banana/Stable Diffusion) ---

device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Carregando modelos em: {device}...")



pipe_txt = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if device=="cuda" else torch.float32)

pipe_txt.to(device)



pipe_img = StableDiffusionImg2ImgPipeline(

    vae=pipe_txt.vae, text_encoder=pipe_txt.text_encoder, tokenizer=pipe_txt.tokenizer,

    unet=pipe_txt.unet, scheduler=pipe_txt.scheduler, safety_checker=pipe_txt.safety_checker,

    feature_extractor=pipe_txt.feature_extractor

).to(device)



# --- FUNÇÃO AUXILIAR GEMINI ---

def enhance_prompt(prompt: str):

    if not GOOGLE_API_KEY:

        return prompt

    try:

        model = genai.GenerativeModel('gemini-pro')

        # Instrução para o Gemini criar um prompt melhor

        response = model.generate_content(f"Act as a professional prompt engineer for Stable Diffusion. Rewrite this simple description into a detailed, high-quality prompt (max 50 words), focusing on lighting, style and texture. Output ONLY the prompt: '{prompt}'")

        return response.text

    except Exception as e:

        print(f"Erro no Gemini: {e}")

        return prompt



@app.get("/")

def health_check():

    return {"status": "online", "auth": "enabled", "gemini": "enabled" if GOOGLE_API_KEY else "disabled"}



# --- ROTAS ---

@app.post("/txt2img", dependencies=[Depends(get_api_key)])

async def txt2img(prompt: str = Form(...), use_ai_enhance: bool = Form(True)):

    

    final_prompt = prompt

    if use_ai_enhance and GOOGLE_API_KEY:

        final_prompt = enhance_prompt(prompt)

        print(f"Prompt Original: {prompt} | Prompt Gemini: {final_prompt}")



    image = pipe_txt(final_prompt).images[0]

    

    img_byte_arr = BytesIO()

    image.save(img_byte_arr, format='PNG')

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")



@app.post("/img2img", dependencies=[Depends(get_api_key)])

async def img2img(prompt: str = Form(...), file: UploadFile = File(...), strength: float = Form(0.75)):

    # Nota: Geralmente não alteramos o prompt no img2img para não desviar demais, mas pode ativar se quiser

    input_image = Image.open(BytesIO(await file.read())).convert("RGB").resize((512, 512))

    image = pipe_img(prompt=prompt, image=input_image, strength=strength).images[0]

    

    img_byte_arr = BytesIO()

    image.save(img_byte_arr, format='PNG')

    return Response(content=img_byte_arr.getvalue(), media_type="image/png")

