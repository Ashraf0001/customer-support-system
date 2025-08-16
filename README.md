# GenAI Launchpad

With AI innovation moving beyond the speed of light, your time to develop is now more precious than ever. That’s why
we’ve built the GenAI Launchpad – your secret weapon to shipping production-ready AI apps, faster.

## 🚀 Introduction

Welcome to the GenAI Launchpad – your all-in-one repository for building powerful, scalable Generative AI applications.
Whether you’re prototyping or deploying at scale, this Docker-based setup has you covered with everything from
event-driven architecture to seamless AI workflow integration.

No need to start from scratch or waste time on repetitive configurations. The GenAI Launchpad is engineered to get you
up and running fast, with a flexible design that fits your workflow – all while keeping things production-ready from day
one.

> **Note**: This repository has two main branches:
> - [`main`](https://github.com/datalumina/genai-launchpad/tree/main): A stripped-down version with just the core
    components, perfect for starting new projects.
> - [`quickstart`](https://github.com/datalumina/genai-launchpad/tree/boilerplate): Contains a complete example
    implementation to demonstrate the Launchpad's capabilities
>
> We recommend following the Accelerator Course first to understand the example implementation in the `quickstart` branch.

## 🎯 Overview

The GenAI Launchpad isn’t just another framework – it’s your shortcut to a production-ready AI infrastructure. Built for
speed and control, its modular architecture brings together the best tools and design patterns to help you deploy faster
without compromising flexibility.

Here’s what you’re working with:

- FastAPI for lightning-fast API development
- Celery for background task processing
- PostgreSQL to handle all your data, includding embeddings
- Redis for fast task queue management
- Caddy for reverse proxy and automatic HTTPS

All services are containerized using Docker, ensuring consistency across development and deployment environments.

## ⭐ Key Features

- **Event-Driven Architecture**: Built-in support for designing and implementing event-driven systems.
- **AI Workflow Support**: Pre-configured setup for integrating AI models and workflows.
- **Scalability**: Designed with scalability in mind, allowing easy expansion as your application grows.
- **Flexibility**: Modular architecture that allows for easy customization and extension.
- **Production-Ready**: Includes essential components for a production environment, including logging, monitoring, and
  security features.
- **Rapid Development**: Boilerplate code and project structure to accelerate development.
- **Docker-Based Deployment**: Complete Docker-based strategy for straightforward deployment.
- **Supabase**: Full self-hosted Supabase included.

## 📚 Documentation

The docs can be found at:
https://launchpad-docs.datalumina.com/

## 🏗️ Project Structure

The Launchpad follows a logical, scalable, and reasonably standardized project structure for building event-driven GenAI
apps.

```text
├── app
│   ├── alembic            # Database migration scripts
│   ├── api                # API endpoints and routers
│   ├── worker             # Background task definitions
│   ├── core               # Components for workflow and task processing
│   ├── database           # Database models and utilities
│   ├── prompts            # Prompt templates for AI models
│   ├── schemas            # Event schemas
│   ├── services           # Business logic and services
│   ├── workflows          # AI workflow definitions
├── docker                 # Docker configuration files
├── playground             # Run experiments for workflow design
└── requests               # Event definitions and handlers
```

## 💬 Support

For support, questions, and collaboration related to the GenAI Launchpad:

1. **Discord Community**: Join our [Discord server](https://discord.gg/H67KUD6vXe) for quick questions, real-time
   support, and feature discussions. This is the fastest way to get help and connect with other users.

2. **GitHub Issues**: For bug reports and technical problems, please open an issue on
   our [GitHub repository](https://github.com/datalumina/genai-launchpad/issues). This helps us track issues
   systematically and builds a searchable knowledge base for the community.

3. **Email**: For private inquiries or matters that don't fit Discord or GitHub, you can reach us at
   launchpad@datalumina.com. However, we encourage using Discord or GitHub for most support needs to benefit the entire
   community.

## ⚖️ License

This project is licensed under the DATALUMINA License. See the [LICENSE](/LICENSE) file for details.

### Key Points

- You are free to use this code for personal or commercial projects, including client work.
- You can modify and build upon the code.
- You cannot resell or distribute this code as a template or part of a package where the primary value is in the code
  itself.
- The software is provided "AS IS", without warranty of any kind.

For the full license text, please refer to the [LICENSE](/LICENSE) file in the repository.

---

For further assistance or to contribute to the GenAI Launchpad, please consult the project maintainers or refer to the
contribution guidelines.

## Quick Start (Local Dev)

```bash
# 1) Install deps
uv sync

# 2) Ensure services are running
#    - Postgres on localhost:5432 (db: genai_launchpad / user: postgres / pass: customer_support_password)
#    - Redis on localhost:6379
#    - Ollama on localhost:11434 with llama3.1:8b

# 3) Run migrations
cd app && PYTHONPATH="$(dirname "$PWD")" uv run alembic upgrade head && cd ..

# 4) Start API (env can be placed in .env or inline)
DATABASE_HOST=localhost DATABASE_NAME=genai_launchpad DATABASE_USER=postgres \
DATABASE_PASSWORD=customer_support_password DATABASE_PORT=5432 \
OLLAMA_BASE_URL=http://localhost:11434 REDIS_URL=redis://127.0.0.1:6379/0 \
uv run uvicorn app.main:app --host 0.0.0.0 --port 8080

# 5) Submit a test ticket
curl -X POST "http://localhost:8080/support/tickets" \
  -H "Content-Type: application/json" \
  -d '{"id":"test123","customer_email":"user@example.com","subject":"Login issue","content":"Cannot login","priority":"high"}'
```
