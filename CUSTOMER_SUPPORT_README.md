# 🎯 Customer Support System - Lightweight MVP

A lightweight, AI-powered customer support system built with the GenAI Launchpad boilerplate. This MVP demonstrates a complete workflow from ticket submission to AI-generated responses using local LLM (Ollama).

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- UV package manager
- Docker & Docker Compose
- Ollama (for local LLM)

### 1. Install Dependencies
```bash
uv sync
```

### 2. Install and Start Ollama
```bash
# Install Ollama
brew install ollama

# Start Ollama service
brew services start ollama

# Pull the Llama model
ollama pull llama3.1:8b
```

### 3. Start Database Services
```bash
# Start PostgreSQL and Redis
docker run -d --name postgres -e POSTGRES_DB=genai_launchpad -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=customer_support_password -p 5432:5432 postgres:15

docker run -d --name redis -p 6379:6379 redis:latest
```

### 4. Test the System
```bash
# Run the test script
python test_customer_support.py

# Or use the interactive playground
python playground/customer_support_playground.py
```

## 🏗️ Architecture

### Core Components

#### 1. **Event Schemas** (`app/schemas/customer_support_schema.py`)
- `SupportTicketSchema`: Input ticket structure
- `SimpleClassificationSchema`: AI classification results
- `ResponseSchema`: AI-generated responses
- `TicketProcessingResult`: Complete processing results

#### 2. **Database Model** (`app/database/support_ticket.py`)
- `SupportTicket`: SQLAlchemy model for ticket storage
- Includes AI processing results and metadata
- Optimized for lightweight MVP requirements

#### 3. **AI Workflow Nodes** (`app/workflows/customer_support_nodes/`)
- **`AnalyzeTicketNode`**: Uses Ollama to classify tickets
- **`ClassifyTicketNode`**: Validates and enhances classification
- **`GenerateResponseNode`**: Generates helpful responses

#### 4. **Workflow** (`app/workflows/customer_support_workflow.py`)
- `CustomerSupportWorkflow`: Orchestrates the 3-node pipeline
- Linear processing: Analysis → Classification → Response
- Follows lightweight MVP pattern

#### 5. **API Endpoints** (`app/api/customer_support_endpoint.py`)
- `POST /support/tickets`: Submit new tickets
- `GET /support/tickets/{ticket_id}`: Get ticket status
- `GET /support/tickets`: List tickets with pagination

#### 6. **Prompt Templates** (`app/prompts/`)
- `ticket_analysis.j2`: Classification prompt
- `response_generation.j2`: Response generation prompt
- Uses Jinja2 templating with frontmatter

## 🔄 Workflow Process

```
1. Ticket Submission
   ↓
2. AnalyzeTicketNode (Ollama)
   - Classifies ticket category
   - Detects sentiment
   - Assesses urgency
   ↓
3. ClassifyTicketNode
   - Validates classification
   - Applies business logic
   - Enhances results
   ↓
4. GenerateResponseNode (Ollama)
   - Generates helpful response
   - Determines response type
   - Suggests actions
   ↓
5. Store Results
   - Save to database
   - Return to customer
```

## 🧪 Testing

### Automated Tests
```bash
python test_customer_support.py
```

### Interactive Playground
```bash
python playground/customer_support_playground.py
```

### Sample Tickets
The system includes 3 sample tickets for testing:
1. **Login Issue** (High Priority) - Technical problem
2. **Billing Question** (Medium Priority) - Account inquiry  
3. **Feature Request** (Low Priority) - Enhancement request

## 📊 API Usage

### Submit a Ticket
```bash
curl -X POST "http://localhost:8080/support/tickets" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "ticket_123",
    "customer_email": "customer@example.com",
    "subject": "Login issues",
    "content": "I cannot log into my account",
    "priority": "high"
  }'
```

### Get Ticket Status
```bash
curl "http://localhost:8080/support/tickets/ticket_123"
```

### List Tickets
```bash
curl "http://localhost:8080/support/tickets?limit=10&offset=0"
```

## 🔧 Configuration

### Environment Variables
```bash
# Database
DATABASE_HOST=localhost
DATABASE_NAME=genai_launchpad
DATABASE_USER=postgres
DATABASE_PASSWORD=customer_support_password
DATABASE_PORT=5432

# Ollama (Local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# Redis
REDIS_URL=redis://localhost:6379
```

### Ollama Configuration
- **Model**: Llama 3.1 8B (lightweight, local)
- **Temperature**: 0.1 for classification, 0.3 for responses
- **Timeout**: 30 seconds per request
- **Fallback**: Default responses on failure

## 📈 Performance

### MVP Targets
- **API Response**: < 500ms for ticket submission
- **AI Processing**: < 10 seconds for complete workflow
- **Memory Usage**: < 2GB for local development
- **Model Size**: 4.9GB (Llama 3.1 8B)

### Optimization Features
- **Connection Pooling**: Database connections
- **Error Handling**: Graceful fallbacks
- **Logging**: Structured logging with correlation IDs
- **Caching**: Redis for task queue management

## 🎯 MVP Success Criteria

### ✅ Completed Features
- [x] Ticket submission via API
- [x] Database storage with SQLAlchemy
- [x] AI classification using Ollama
- [x] AI response generation
- [x] Workflow orchestration
- [x] Error handling and logging
- [x] Test scripts and playground
- [x] Documentation

### 🔄 Future Enhancements (Post-MVP)
- [ ] Advanced routing logic
- [ ] Agent assignment
- [ ] SLA tracking
- [ ] Analytics dashboard
- [ ] Cloud LLM integration
- [ ] Complex integrations

## 🛠️ Development

### Project Structure
```
app/
├── api/                          # FastAPI endpoints
├── core/                         # Workflow engine
├── database/                     # SQLAlchemy models
├── prompts/                      # Jinja2 templates
├── schemas/                      # Pydantic models
├── services/                     # Business logic
├── workflows/                    # Workflow definitions
│   └── customer_support_nodes/   # AI workflow nodes
└── worker/                       # Celery tasks
```

### Key Files
- `test_customer_support.py`: Automated testing
- `playground/customer_support_playground.py`: Interactive testing
- `requests/events/customer_support_ticket.json`: Sample data
- `CUSTOMER_SUPPORT_README.md`: This documentation

## 🚨 Troubleshooting

### Common Issues

#### 1. Ollama Connection Failed
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Restart Ollama
brew services restart ollama
```

#### 2. Database Connection Failed
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Restart PostgreSQL
docker restart postgres
```

#### 3. Import Errors
```bash
# Ensure you're in the correct directory
cd "genai-launchpad-main copy"

# Check Python path
python -c "import sys; print(sys.path)"
```

#### 4. Workflow Execution Failed
```bash
# Check Ollama model
ollama list

# Pull model if missing
ollama pull llama3.1:8b
```

## 📝 Logging

The system uses structured logging with correlation IDs:
```python
logger.info("Processing ticket", extra={
    "ticket_id": ticket.id,
    "node": self.node_name,
    "status": "started"
})
```

## 🤝 Contributing

This is a lightweight MVP. For production use, consider:
1. Adding comprehensive tests
2. Implementing security measures
3. Adding monitoring and alerting
4. Optimizing for scale
5. Adding user authentication

## 📄 License

This project follows the same license as the GenAI Launchpad boilerplate.

---

**🎉 Congratulations!** You now have a working AI-powered customer support system that can:
- Accept support tickets
- Classify them using local AI
- Generate helpful responses
- Store everything in a database

The system is ready for testing and can be extended for production use.





