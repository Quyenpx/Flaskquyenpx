#!/bin/bash

echo "🐳 Flask Multi Store - Docker Setup"
echo "====================================="

echo "📦 Building Docker image..."
docker build -t flask-multi-store .

if [ $? -ne 0 ]; then
    echo "❌ Docker build failed!"
    exit 1
fi

echo "✅ Docker image built successfully!"

echo "🚀 Starting container..."
docker run -d -p 5000:5000 --name flask-store-container flask-multi-store

if [ $? -ne 0 ]; then
    echo "❌ Failed to start container!"
    echo "🔄 Trying to remove existing container..."
    docker rm -f flask-store-container
    docker run -d -p 5000:5000 --name flask-store-container flask-multi-store
fi

echo "✅ Container started successfully!"
echo "🌐 Website: http://localhost:5000"
echo "📊 Container status:"
docker ps | grep flask-store-container

echo ""
echo "🛑 To stop: docker stop flask-store-container"
echo "🗑️  To remove: docker rm flask-store-container"
echo "📋 To view logs: docker logs flask-store-container"
