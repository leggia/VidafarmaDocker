# Integración con Odoo - Vidafarma_IA

## Descripción
Este proyecto se conecta a una instancia remota de Odoo 18 Community para la gestión de farmacias.

## Estructura
```
odoo/
├── addons/          # Addons personalizados (si se necesitan)
├── config/          # Archivos de configuración de referencia
│   └── odoo.conf    # Configuración de ejemplo
└── README.md        # Este archivo
```

## Configuración

### Variables de Entorno
Copia el archivo `env.example` a `.env` en la raíz del proyecto y configura las variables con tus credenciales de Odoo:

```bash
# Configuración de Odoo (instancia remota)
ODOO_HOST=tu-servidor-odoo.com
ODOO_PORT=443
ODOO_DB=tu_base_de_datos
ODOO_USER=tu_usuario
ODOO_PASSWORD=tu_contraseña
```

### Acceso a Odoo
- **URL:** https://tu-servidor-odoo.com
- **Usuario:** Tu usuario de Odoo
- **Contraseña:** Tu contraseña de Odoo

## Desarrollo

### Agregar Addons Personalizados
Si necesitas addons personalizados, contacta al administrador de tu instancia de Odoo para instalarlos.

### Desarrollo de Integración
La API se conecta a Odoo usando XML-RPC para:
- Obtener productos del catálogo
- Consultar movimientos de inventario
- Gestionar órdenes de compra y venta
- Obtener información de clientes y proveedores

## Integración con la API
La API de FastAPI se conecta a Odoo usando XML-RPC para:
- Obtener productos
- Consultar inventario
- Gestionar órdenes de compra/venta
- Obtener información de partners

## Comandos Útiles

### Iniciar servicios
```bash
docker-compose up -d
```

### Ver logs de la API
```bash
docker-compose logs -f api
```

### Probar conexión con Odoo
```bash
curl http://localhost:8000/api/odoo/productos
```

### Verificar estado de servicios
```bash
docker-compose ps
```

## Troubleshooting

### Problema: No se puede conectar a Odoo
1. Verifica las credenciales en el archivo `.env`
2. Revisa los logs de la API: `docker-compose logs api`
3. Verifica que tu instancia de Odoo esté accesible desde internet
4. Comprueba que el puerto y protocolo sean correctos (HTTPS/HTTP)

### Problema: Error de autenticación
1. Verifica usuario y contraseña en `.env`
2. Asegúrate de que el usuario tenga permisos de acceso a la API
3. Verifica que la base de datos especificada exista

### Problema: Timeout en conexiones
1. Verifica la conectividad de red
2. Revisa si hay firewall bloqueando las conexiones
3. Considera usar un proxy si es necesario 