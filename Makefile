.PHONY: help build up down logs clean restart status test

# Colores para output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
NC := \033[0m # No Color

help: ## Muestra esta ayuda
	@echo "$(CYAN)╔══════════════════════════════════════════════════════════════════════════════╗$(NC)"
	@echo "$(CYAN)║                    PIPELINE GIS CATASTRAL - COMANDOS                         ║$(NC)"
	@echo "$(CYAN)╚══════════════════════════════════════════════════════════════════════════════╝$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""

build: ## Construir las imágenes Docker
	@echo "$(YELLOW)🏗️  Construyendo imágenes Docker...$(NC)"
	docker-compose build

up: ## Iniciar los servicios
	@echo "$(YELLOW)🚀 Iniciando servicios...$(NC)"
	docker-compose up -d
	@echo "$(GREEN)✅ Servicios iniciados$(NC)"
	@echo ""
	@echo "$(CYAN)🌐 Acceso:$(NC)"
	@echo "   Frontend: http://localhost"
	@echo "   Backend:  http://localhost:8000"
	@echo "   API Docs: http://localhost:8000/docs"

down: ## Detener los servicios
	@echo "$(YELLOW)🛑 Deteniendo servicios...$(NC)"
	docker-compose down

logs: ## Ver logs de todos los servicios
	docker-compose logs -f

logs-backend: ## Ver logs del backend
	docker-compose logs -f backend

logs-frontend: ## Ver logs del frontend
	docker-compose logs -f frontend

status: ## Ver estado de los servicios
	@echo "$(CYAN)📊 Estado de los servicios:$(NC)"
	@docker-compose ps

restart: ## Reiniciar los servicios
	@echo "$(YELLOW)🔄 Reiniciando servicios...$(NC)"
	@make down
	@make up

clean: ## Limpiar contenedores, imágenes y volúmenes
	@echo "$(YELLOW)🧹 Limpiando...$(NC)"
	docker-compose down -v
	docker system prune -f

deploy: ## Construir e iniciar (despliegue completo)
	@make build
	@make up

shell-backend: ## Abrir shell en el contenedor del backend
	docker-compose exec backend /bin/bash

shell-frontend: ## Abrir shell en el contenedor del frontend
	docker-compose exec frontend /bin/sh

test: ## Ejecutar tests (placeholder)
	@echo "$(YELLOW)🧪 Tests no implementados aún$(NC)"
