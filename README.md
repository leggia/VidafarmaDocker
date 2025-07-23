# Vidafarma_IA (agente-ia)

Plataforma inteligente para la gestión de farmacias, con agente IA, automatización de tareas, integración OCR y conexión con Odoo.

## Estructura del monorepo

```
Vidafarma_IA/
├── backend/      # Microservicios (api, ocr, odoo, ia)
├── frontend/     # PWA (React) con soporte de voz
├── odoo/         # Configuración y addons de Odoo
├── scripts/      # Scripts de inicialización
├── docs/         # Documentación adicional
├── docker-compose.yml
├── README.md
└── .gitignore
```

- Documentación detallada en `/docs` y en los README.md de cada microservicio.
- Cada microservicio y el frontend tienen su propio README.md y Dockerfile.

---

## Microservicios principales
- **api:** FastAPI, lógica de negocio, integración IA, endpoints para frontend.
- **odoo:** Integración con Odoo 18 Community (instancia remota en la nube).
- **redis:** Caché para optimizar consultas a Odoo.
- **ocr:** Reconocimiento de texto en facturas (PDF/foto) - futuro.
- **ia:** Microservicio IA (futuro, GPU/nube).

## Frontend
- PWA (React) con soporte para cámara, micrófono y consultas por voz.

## Inicio Rápido

### Prerrequisitos
- Docker y Docker Compose instalados
- Git

### Configuración Inicial
1. Clona el repositorio
2. Ejecuta el script de inicialización:
   ```bash
   # Linux/Mac
   chmod +x scripts/init-odoo.sh
   ./scripts/init-odoo.sh
   
   # Windows (PowerShell)
   .\scripts\init-odoo.ps1
   ```

3. Accede a los servicios:
   - **API:** http://localhost:8000/docs
   - **Frontend:** http://localhost:3000
   - **Odoo:** Tu instancia remota (configurada en .env)

## Documentación
- Ver `/docs` para decisiones técnicas, diagramas y guías de uso.
- Ver `/odoo/README.md` para configuración específica de Odoo. 