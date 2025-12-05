#!/bin/bash
# Quick deployment script for VPS

set -e

echo "🚀 Deepfake Detector — Auto Deployment"
echo "======================================"

# Step 1: Install Docker
echo "📦 Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sudo bash
    sudo usermod -aG docker $USER
    newgrp docker
    echo "✓ Docker installed"
else
    echo "✓ Docker already installed"
fi

# Step 2: Clone or pull repo
echo "📂 Setting up project..."
if [ -d "deepfake-detector" ]; then
    cd deepfake-detector
    git pull origin main
else
    git clone <your-repo-url> deepfake-detector
    cd deepfake-detector
fi

# Step 3: Prompt for domain
echo ""
echo "🌐 Enter your domain (e.g., detector.example.com):"
read DOMAIN

# Step 4: Update Caddyfile
echo "⚙️ Configuring domain..."
sed -i "s/example.com/$DOMAIN/g" Caddyfile

# Step 5: Start services
echo "🐳 Starting Docker services..."
docker-compose up -d

# Step 6: Wait for services
echo "⏳ Waiting for services to be ready..."
sleep 10

# Step 7: Check health
echo ""
echo "✓ Deployment complete!"
echo ""
echo "📍 Visit: https://$DOMAIN"
echo "🏥 Health check: https://$DOMAIN/health"
echo ""
echo "📋 View logs: docker-compose logs -f"
echo ""
