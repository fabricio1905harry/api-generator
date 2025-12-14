#!/bin/bash

# Script de deploy para VPS
# Uso: ./deploy.sh

echo "🚀 Iniciando deploy da Stable Diffusion API..."

# Verificar se Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não encontrado. Instalando..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    echo "✅ Docker instalado. Por favor, faça logout e login novamente, depois execute este script novamente."
    exit 1
fi

# Verificar se Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "📦 Instalando Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Parar containers existentes
echo "🛑 Parando containers existentes..."
docker-compose down

# Construir e iniciar
echo "🔨 Construindo e iniciando containers..."
docker-compose up -d --build

# Aguardar alguns segundos
sleep 5

# Verificar status
echo "📊 Status dos containers:"
docker-compose ps

echo ""
echo "✅ Deploy concluído!"
echo "🌐 API disponível em: http://$(hostname -I | awk '{print $1}'):8000"
echo "📚 Documentação: http://$(hostname -I | awk '{print $1}'):8000/docs"
echo ""
echo "Para ver os logs: docker-compose logs -f"
echo "Para parar: docker-compose down"

