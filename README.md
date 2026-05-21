# ProyectoFinalDJ

Sistema de gestión de inventario desarrollado con Django.

## 🌐 Aplicación en Producción

**URL:** https://proyectofinaldj.onrender.com

---

## 🔐 Credenciales de Acceso

### 👨‍💼 Cuenta Administrador
| Campo | Valor |
|-------|-------|
| **Usuario** | `admin` |
| **Contraseña** | `admin123` |
| **Acceso** | Dashboard completo, productos, categorías, proveedores, compras, ventas y reportes |

### 👨‍💻 Cuenta Operador
| Campo | Valor |
|-------|-------|
| **Usuario** | `operador` |
| **Contraseña** | `operador123` |
| **Acceso** | Dashboard limitado, registro de ventas y visualización de productos |

---

## 🗂️ Funcionalidades

### Administrador
- ✅ Dashboard con métricas y gráficos
- ✅ Gestión de productos (CRUD)
- ✅ Gestión de categorías (CRUD)
- ✅ Gestión de proveedores (CRUD)
- ✅ Registro de compras
- ✅ Registro de ventas
- ✅ Reportes de inventario y ventas
- ✅ Exportación a Excel
- ✅ Alertas de stock bajo

### Operador
- ✅ Dashboard con sus ventas
- ✅ Visualización de productos
- ✅ Registro de ventas

---

## 🛠️ Tecnologías

- **Backend:** Django 5.0.8
- **Base de datos:** PostgreSQL (producción) / SQLite (desarrollo)
- **Frontend:** Bootstrap 5 + Bootstrap Icons
- **Deployment:** Render
- **Servidor:** Gunicorn + WhiteNoise

---

## 🚀 Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/DavidSalas0273/ProyectoFinalDJ.git
cd ProyectoFinalDJ

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

Acceder en: http://127.0.0.1:8000
