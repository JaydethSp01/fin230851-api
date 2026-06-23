from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uvicorn

app = FastAPI(title="Task Management API", version="1.0.0")

# CRUD generico server-side (persistencia multi-dispositivo)
try:
    from app.routers import data as _data_router
    app.include_router(_data_router.router)
except Exception as _e:
    import logging; logging.getLogger('uvicorn').warning('data router: %s', _e)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UsuarioCreate(BaseModel):
    nombre: str
    email: str
    rol: str
    avatar: Optional[str] = None
    activo: bool = True


class PrioridadCreate(BaseModel):
    nombre: str
    nivel: int
    color: str


class ProyectoCreate(BaseModel):
    nombre: str
    descripcion: str
    color: str
    propietario_id: int
    fecha_inicio: str
    fecha_fin: Optional[str] = None
    activo: bool = True


class TareaCreate(BaseModel):
    titulo: str
    descripcion: str
    proyecto_id: int
    asignado_a: int
    prioridad_id: int
    estado: str
    fecha_vencimiento: Optional[str] = None
    completada: bool = False


usuarios_db = [
    {"id": 1, "nombre": "Ana García", "email": "ana.garcia@empresa.com", "rol": "Admin", "avatar": "AG", "activo": True, "fecha_creacion": "2024-01-15"},
    {"id": 2, "nombre": "Carlos López", "email": "carlos.lopez@empresa.com", "rol": "Developer", "avatar": "CL", "activo": True, "fecha_creacion": "2024-02-01"},
    {"id": 3, "nombre": "María Fernández", "email": "maria.fernandez@empresa.com", "rol": "Designer", "avatar": "MF", "activo": True, "fecha_creacion": "2024-02-10"},
    {"id": 4, "nombre": "Jorge Martínez", "email": "jorge.martinez@empresa.com", "rol": "Developer", "avatar": "JM", "activo": True, "fecha_creacion": "2024-03-05"},
    {"id": 5, "nombre": "Laura Sánchez", "email": "laura.sanchez@empresa.com", "rol": "PM", "avatar": "LS", "activo": True, "fecha_creacion": "2024-03-20"},
    {"id": 6, "nombre": "Rubén Torres", "email": "ruben.torres@empresa.com", "rol": "QA", "avatar": "RT", "activo": False, "fecha_creacion": "2024-04-01"},
]

prioridades_db = [
    {"id": 1, "nombre": "Crítica", "nivel": 4, "color": "#ef4444"},
    {"id": 2, "nombre": "Alta", "nivel": 3, "color": "#f97316"},
    {"id": 3, "nombre": "Media", "nivel": 2, "color": "#eab308"},
    {"id": 4, "nombre": "Baja", "nivel": 1, "color": "#22c55e"},
]

proyectos_db = [
    {"id": 1, "nombre": "App Mobile v2.0", "descripcion": "Rediseño completo de la aplicación móvil con nuevas funcionalidades y mejora de UX", "color": "#6366f1", "propietario_id": 1, "fecha_inicio": "2024-01-01", "fecha_fin": "2024-06-30", "activo": True},
    {"id": 2, "nombre": "Portal Cliente", "descripcion": "Portal web para gestión de clientes, pedidos y facturación en línea", "color": "#0ea5e9", "propietario_id": 5, "fecha_inicio": "2024-02-15", "fecha_fin": "2024-08-15", "activo": True},
    {"id": 3, "nombre": "API Integration", "descripcion": "Integración con servicios externos de pagos, logística y ERP corporativo", "color": "#10b981", "propietario_id": 2, "fecha_inicio": "2024-03-01", "fecha_fin": "2024-07-01", "activo": True},
    {"id": 4, "nombre": "Dashboard Analytics", "descripcion": "Panel de analytics y reportes en tiempo real para dirección y operaciones", "color": "#f59e0b", "propietario_id": 1, "fecha_inicio": "2024-04-01", "fecha_fin": "2024-09-30", "activo": True},
    {"id": 5, "nombre": "Sistema de Notificaciones", "descripcion": "Sistema centralizado de notificaciones push, email y Slack", "color": "#8b5cf6", "propietario_id": 5, "fecha_inicio": "2024-05-01", "fecha_fin": "2024-10-01", "activo": False},
    {"id": 6, "nombre": "Migración Cloud", "descripcion": "Migración de infraestructura on-premise a AWS con Kubernetes", "color": "#ec4899", "propietario_id": 4, "fecha_inicio": "2024-06-01", "fecha_fin": "2024-12-31", "activo": True},
]

tareas_db = [
    {"id": 1, "titulo": "Diseño pantalla principal", "descripcion": "Crear wireframes y mockups de alta fidelidad para la pantalla principal de la app", "proyecto_id": 1, "asignado_a": 3, "prioridad_id": 2, "estado": "En Progreso", "fecha_vencimiento": "2024-04-15", "fecha_creacion": "2024-03-01", "completada": False},
    {"id": 2, "titulo": "Implementar autenticación JWT", "descripcion": "Desarrollar sistema de login y registro con JWT, refresh tokens y 2FA", "proyecto_id": 1, "asignado_a": 2, "prioridad_id": 1, "estado": "En Progreso", "fecha_vencimiento": "2024-04-10", "fecha_creacion": "2024-03-05", "completada": False},
    {"id": 3, "titulo": "Setup base de datos PostgreSQL", "descripcion": "Configurar y migrar esquema de base de datos en entorno de producción", "proyecto_id": 2, "asignado_a": 4, "prioridad_id": 1, "estado": "Completada", "fecha_vencimiento": "2024-03-20", "fecha_creacion": "2024-02-20", "completada": True},
    {"id": 4, "titulo": "Integración Stripe Payments", "descripcion": "Implementar pasarela de pago con Stripe para suscripciones y pagos únicos", "proyecto_id": 3, "asignado_a": 2, "prioridad_id": 2, "estado": "Pendiente", "fecha_vencimiento": "2024-05-01", "fecha_creacion": "2024-03-10", "completada": False},
    {"id": 5, "titulo": "Librería de componentes UI", "descripcion": "Crear sistema de diseño y librería de componentes reutilizables con Storybook", "proyecto_id": 1, "asignado_a": 3, "prioridad_id": 3, "estado": "En Progreso", "fecha_vencimiento": "2024-04-30", "fecha_creacion": "2024-03-15", "completada": False},
    {"id": 6, "titulo": "Dashboard KPIs principales", "descripcion": "Implementar visualizaciones de KPIs con gráficas interactivas y filtros", "proyecto_id": 4, "asignado_a": 4, "prioridad_id": 2, "estado": "Pendiente", "fecha_vencimiento": "2024-05-15", "fecha_creacion": "2024-04-01", "completada": False},
    {"id": 7, "titulo": "Testing E2E con Playwright", "descripcion": "Escribir suite completa de tests end-to-end para todos los flujos críticos", "proyecto_id": 2, "asignado_a": 6, "prioridad_id": 3, "estado": "Pendiente", "fecha_vencimiento": "2024-06-01", "fecha_creacion": "2024-04-05", "completada": False},
    {"id": 8, "titulo": "Documentación API REST", "descripcion": "Documentar todos los endpoints con OpenAPI/Swagger y ejemplos de uso reales", "proyecto_id": 3, "asignado_a": 5, "prioridad_id": 4, "estado": "En Progreso", "fecha_vencimiento": "2024-05-20", "fecha_creacion": "2024-04-10", "completada": False},
]

_usuario_counter = 7
_prioridad_counter = 5
_proyecto_counter = 7
_tarea_counter = 9


@app.get("/")
def root():
    return {
        "api": "Task Management API",
        "version": "1.0.0",
        "entities": ["usuarios", "proyectos", "tareas", "prioridades"],
    }


@app.get("/usuarios")
def get_usuarios():
    return usuarios_db


@app.get("/usuarios/{usuario_id}")
def get_usuario(usuario_id: int):
    for u in usuarios_db:
        if u["id"] == usuario_id:
            return u
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.post("/usuarios", status_code=201)
def create_usuario(usuario: UsuarioCreate):
    global _usuario_counter
    nuevo = {
        "id": _usuario_counter,
        **usuario.model_dump(),
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
    }
    usuarios_db.append(nuevo)
    _usuario_counter += 1
    return nuevo


@app.put("/usuarios/{usuario_id}")
def update_usuario(usuario_id: int, usuario: UsuarioCreate):
    for i, u in enumerate(usuarios_db):
        if u["id"] == usuario_id:
            usuarios_db[i] = {
                "id": usuario_id,
                **usuario.model_dump(),
                "fecha_creacion": u["fecha_creacion"],
            }
            return usuarios_db[i]
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.delete("/usuarios/{usuario_id}")
def delete_usuario(usuario_id: int):
    for i, u in enumerate(usuarios_db):
        if u["id"] == usuario_id:
            eliminado = usuarios_db.pop(i)
            return {"message": "Usuario eliminado", "id": eliminado["id"]}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")


@app.get("/prioridades")
def get_prioridades():
    return sorted(prioridades_db, key=lambda p: p["nivel"], reverse=True)


@app.get("/prioridades/{prioridad_id}")
def get_prioridad(prioridad_id: int):
    for p in prioridades_db:
        if p["id"] == prioridad_id:
            return p
    raise HTTPException(status_code=404, detail="Prioridad no encontrada")


@app.post("/prioridades", status_code=201)
def create_prioridad(prioridad: PrioridadCreate):
    global _prioridad_counter
    nueva = {"id": _prioridad_counter, **prioridad.model_dump()}
    prioridades_db.append(nueva)
    _prioridad_counter += 1
    return nueva


@app.put("/prioridades/{prioridad_id}")
def update_prioridad(prioridad_id: int, prioridad: PrioridadCreate):
    for i, p in enumerate(prioridades_db):
        if p["id"] == prioridad_id:
            prioridades_db[i] = {"id": prioridad_id, **prioridad.model_dump()}
            return prioridades_db[i]
    raise HTTPException(status_code=404, detail="Prioridad no encontrada")


@app.delete("/prioridades/{prioridad_id}")
def delete_prioridad(prioridad_id: int):
    for i, p in enumerate(prioridades_db):
        if p["id"] == prioridad_id:
            eliminado = prioridades_db.pop(i)
            return {"message": "Prioridad eliminada", "id": eliminado["id"]}
    raise HTTPException(status_code=404, detail="Prioridad no encontrada")


@app.get("/proyectos")
def get_proyectos():
    return proyectos_db


@app.get("/proyectos/{proyecto_id}")
def get_proyecto(proyecto_id: int):
    for p in proyectos_db:
        if p["id"] == proyecto_id:
            return p
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


@app.get("/proyectos/{proyecto_id}/tareas")
def get_tareas_por_proyecto(proyecto_id: int):
    proyecto = next((p for p in proyectos_db if p["id"] == proyecto_id), None)
    if not proyecto:
        raise HTTPException(status_code=404, detail="Proyecto no encontrado")
    return [t for t in tareas_db if t["proyecto_id"] == proyecto_id]


@app.post("/proyectos", status_code=201)
def create_proyecto(proyecto: ProyectoCreate):
    global _proyecto_counter
    nuevo = {"id": _proyecto_counter, **proyecto.model_dump()}
    proyectos_db.append(nuevo)
    _proyecto_counter += 1
    return nuevo


@app.put("/proyectos/{proyecto_id}")
def update_proyecto(proyecto_id: int, proyecto: ProyectoCreate):
    for i, p in enumerate(proyectos_db):
        if p["id"] == proyecto_id:
            proyectos_db[i] = {"id": proyecto_id, **proyecto.model_dump()}
            return proyectos_db[i]
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


@app.delete("/proyectos/{proyecto_id}")
def delete_proyecto(proyecto_id: int):
    for i, p in enumerate(proyectos_db):
        if p["id"] == proyecto_id:
            eliminado = proyectos_db.pop(i)
            return {"message": "Proyecto eliminado", "id": eliminado["id"]}
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


@app.get("/tareas")
def get_tareas(
    proyecto_id: Optional[int] = None,
    asignado_a: Optional[int] = None,
    prioridad_id: Optional[int] = None,
    estado: Optional[str] = None,
    completada: Optional[bool] = None,
):
    resultado = list(tareas_db)
    if proyecto_id is not None:
        resultado = [t for t in resultado if t["proyecto_id"] == proyecto_id]
    if asignado_a is not None:
        resultado = [t for t in resultado if t["asignado_a"] == asignado_a]
    if prioridad_id is not None:
        resultado = [t for t in resultado if t["prioridad_id"] == prioridad_id]
    if estado is not None:
        resultado = [t for t in resultado if t["estado"].lower() == estado.lower()]
    if completada is not None:
        resultado = [t for t in resultado if t["completada"] == completada]
    return resultado


@app.get("/tareas/{tarea_id}")
def get_tarea(tarea_id: int):
    for t in tareas_db:
        if t["id"] == tarea_id:
            return t
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@app.post("/tareas", status_code=201)
def create_tarea(tarea: TareaCreate):
    global _tarea_counter
    proyecto = next((p for p in proyectos_db if p["id"] == tarea.proyecto_id), None)
    if not proyecto:
        raise HTTPException(status_code=400, detail="El proyecto especificado no existe")
    usuario = next((u for u in usuarios_db if u["id"] == tarea.asignado_a), None)
    if not usuario:
        raise HTTPException(status_code=400, detail="El usuario asignado no existe")
    prioridad = next((p for p in prioridades_db if p["id"] == tarea.prioridad_id), None)
    if not prioridad:
        raise HTTPException(status_code=400, detail="La prioridad especificada no existe")
    nueva = {
        "id": _tarea_counter,
        **tarea.model_dump(),
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d"),
    }
    tareas_db.append(nueva)
    _tarea_counter += 1
    return nueva


@app.put("/tareas/{tarea_id}")
def update_tarea(tarea_id: int, tarea: TareaCreate):
    for i, t in enumerate(tareas_db):
        if t["id"] == tarea_id:
            tareas_db[i] = {
                "id": tarea_id,
                **tarea.model_dump(),
                "fecha_creacion": t["fecha_creacion"],
            }
            return tareas_db[i]
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@app.patch("/tareas/{tarea_id}/completar")
def completar_tarea(tarea_id: int):
    for i, t in enumerate(tareas_db):
        if t["id"] == tarea_id:
            tareas_db[i]["completada"] = not t["completada"]
            tareas_db[i]["estado"] = "Completada" if tareas_db[i]["completada"] else "En Progreso"
            return tareas_db[i]
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@app.delete("/tareas/{tarea_id}")
def delete_tarea(tarea_id: int):
    for i, t in enumerate(tareas_db):
        if t["id"] == tarea_id:
            eliminado = tareas_db.pop(i)
            return {"message": "Tarea eliminada", "id": eliminado["id"]}
    raise HTTPException(status_code=404, detail="Tarea no encontrada")


@app.get("/stats")
def get_stats():
    total_tareas = len(tareas_db)
    completadas = sum(1 for t in tareas_db if t["completada"])
    en_progreso = sum(1 for t in tareas_db if t["estado"] == "En Progreso" and not t["completada"])
    pendientes = sum(1 for t in tareas_db if t["estado"] == "Pendiente")
    proyectos_activos = sum(1 for p in proyectos_db if p["activo"])
    usuarios_activos = sum(1 for u in usuarios_db if u["activo"])
    tareas_por_prioridad = {}
    for p in prioridades_db:
        tareas_por_prioridad[p["nombre"]] = sum(1 for t in tareas_db if t["prioridad_id"] == p["id"])
    return {
        "tareas": {
            "total": total_tareas,
            "completadas": completadas,
            "en_progreso": en_progreso,
            "pendientes": pendientes,
            "porcentaje_completado": round((completadas / total_tareas * 100), 1) if total_tareas else 0,
        },
        "proyectos": {
            "total": len(proyectos_db),
            "activos": proyectos_activos,
        },
        "usuarios": {
            "total": len(usuarios_db),
            "activos": usuarios_activos,
        },
        "tareas_por_prioridad": tareas_por_prioridad,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)