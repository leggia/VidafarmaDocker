# Script de inicialización para Odoo - Vidafarma_IA (Windows)
Write-Host "🚀 Iniciando configuración de Odoo para Vidafarma_IA..." -ForegroundColor Green

# Verificar si Docker está corriendo
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker no está corriendo. Por favor inicia Docker Desktop y vuelve a intentar." -ForegroundColor Red
    exit 1
}

# Crear archivo .env si no existe
if (-not (Test-Path ".env")) {
    Write-Host "📝 Creando archivo .env desde env.example..." -ForegroundColor Yellow
    Copy-Item "env.example" ".env"
    Write-Host "✅ Archivo .env creado. Revisa y ajusta las variables según necesites." -ForegroundColor Green
}

# Construir e iniciar los servicios
Write-Host "🔨 Construyendo e iniciando servicios..." -ForegroundColor Yellow
docker-compose up -d --build

# Esperar a que los servicios estén listos
Write-Host "⏳ Esperando a que los servicios estén listos..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Verificar estado de los servicios
Write-Host "📊 Estado de los servicios:" -ForegroundColor Cyan
docker-compose ps

Write-Host ""
Write-Host "🎉 ¡Configuración completada!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos pasos:" -ForegroundColor Cyan
Write-Host "1. Configura las credenciales de Odoo en el archivo .env" -ForegroundColor White
Write-Host "2. Accede a la API en: http://localhost:8000/docs" -ForegroundColor White
Write-Host "3. Prueba la conexión con Odoo usando los endpoints" -ForegroundColor White
Write-Host "4. Accede al frontend en: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Comandos útiles:" -ForegroundColor Cyan
Write-Host "- Ver logs: docker-compose logs -f api" -ForegroundColor White
Write-Host "- Probar API: curl http://localhost:8000/api/odoo/productos" -ForegroundColor White
Write-Host "- Detener: docker-compose down" -ForegroundColor White 