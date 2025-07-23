#!/bin/bash

# Script de inicialización para Odoo - Vidafarma_IA
echo "🚀 Iniciando configuración de Odoo para Vidafarma_IA..."

# Verificar si Docker está corriendo
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker no está corriendo. Por favor inicia Docker y vuelve a intentar."
    exit 1
fi

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env desde env.example..."
    cp env.example .env
    echo "✅ Archivo .env creado. Revisa y ajusta las variables según necesites."
fi

# Construir e iniciar los servicios
echo "🔨 Construyendo e iniciando servicios..."
docker-compose up -d --build

# Esperar a que los servicios estén listos
echo "⏳ Esperando a que los servicios estén listos..."
sleep 30

# Verificar estado de los servicios
echo "📊 Estado de los servicios:"
docker-compose ps

echo ""
echo "🎉 ¡Configuración completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Accede a Odoo en: http://localhost:8069"
echo "2. Crea una nueva base de datos llamada 'agenteia_odoo'"
echo "3. Instala los módulos básicos (Ventas, Compras, Inventario)"
echo "4. Accede a la API en: http://localhost:8000/docs"
echo ""
echo "🔧 Comandos útiles:"
echo "- Ver logs: docker-compose logs -f odoo"
echo "- Reiniciar: docker-compose restart odoo"
echo "- Detener: docker-compose down" 