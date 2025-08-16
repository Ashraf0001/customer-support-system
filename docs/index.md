# Customer Support System

A lightweight MVP for a GenAI-powered customer support workflow using FastAPI, Celery, PostgreSQL, Redis, and a local LLM (Ollama).

## Overview
- Event-driven workflow: Analyze → Classify → Generate Response
- Local LLM via Ollama (llama3.1:8b)
- Simple persistence for tickets and results
- API-first with background processing

## Features
- Ticket submission API
- Celery-based async processing
- Prompt templating via Jinja2
- Typed schemas with Pydantic v2

## Links
- API Docs: /docs
- Health: /healthz, /readyz

## Quick Start
- Install Ollama and pull a model: `ollama pull llama3.1:8b`
- Start API and Worker:
  - `DATABASE_PASSWORD=customer_support_password ./scripts/start_api.sh`
  - `DATABASE_PASSWORD=customer_support_password ./scripts/start_worker.sh`
- Open the UI: `http://localhost:8080/ui`

## Production
See Deployment → Production for environment variables, reverse proxy, hardening, and a deployment checklist.



