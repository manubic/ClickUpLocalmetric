# Localmetric Task Automation Tool

Este repositorio contiene la herramienta desarrollada para Localmetric, diseñada para automatizar la creación y gestión de tareas en ClickUp. La herramienta abarca dos funcionalidades principales:

1. **Gestión de Tareas para Reseñas Negativas.**
2. **Fase 1: Creación de Tareas para Nuevos Clientes con Subtareas.**

## Funcionalidades

### 1. Gestión de Tareas para Reseñas Negativas

- **Descripción:** Crea tareas para reseñas negativas sin responder, con una fecha límite de tres días. Si la tarea se retrasa una semana, se marca como prioridad urgente. Además, si la reseña tiene más de 200 caracteres, se marca como prioridad alta; de lo contrario, se marca como normal.
- **Integración:** Utiliza la API de ClickUp para gestionar las tareas.
- **Reglas de Prioridad:**
  - **Normal:** Tareas sin características especiales.
  - **Alta:** Reseñas con más de 200 caracteres.
  - **Urgente:** Tareas retrasadas una semana.

### 2. Fase 1: Creación de Tareas para Nuevos Clientes

- **Descripción:** Crea diversas tareas con subtareas en la carpeta del cliente, con una fecha límite de cinco días.
- **Integración:** Utiliza la API de ClickUp para la creación y organización de tareas.
- **Proceso:**
  - Crea una carpeta para el nuevo cliente.
  - Añade tareas principales con sus respectivas subtareas.

## Instalación

### Requisitos Previos

- **Cuenta de ClickUp y acceso a ClickUp API.**
- **Token de API de ClickUp.**
- **Python 3.8 o superior.**
