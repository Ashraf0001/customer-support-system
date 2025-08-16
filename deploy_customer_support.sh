#!/bin/bash

# Customer Support System - Lightweight MVP Deployment Script
# This script sets up and starts the customer support system

set -e  # Exit on any error

echo "🚀 Customer Support System - Lightweight MVP Deployment"
echo "======================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

print_status "Starting deployment process..."

# Step 1: Check if UV is installed
if ! command -v uv &> /dev/null; then
    print_error "UV is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

print_success "UV is installed"

# Step 2: Install dependencies
print_status "Installing Python dependencies..."
uv sync
print_success "Dependencies installed"

# Step 3: Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    print_warning "Ollama is not installed. Installing now..."
    brew install ollama
    print_success "Ollama installed"
else
    print_success "Ollama is already installed"
fi

# Step 4: Start Ollama service
print_status "Starting Ollama service..."
brew services start ollama
sleep 3

# Check if Ollama is running
if curl -s http://localhost:11434/api/tags > /dev/null; then
    print_success "Ollama is running"
else
    print_error "Failed to start Ollama. Please check the installation."
    exit 1
fi

# Step 5: Check if Llama model is available
print_status "Checking Llama model..."
if ollama list | grep -q "llama3.1:8b"; then
    print_success "Llama 3.1 8B model is available"
else
    print_warning "Llama 3.1 8B model not found. Pulling now..."
    ollama pull llama3.1:8b
    print_success "Llama 3.1 8B model downloaded"
fi

# Step 6: Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    print_error "Docker is not running. Please start Docker Desktop first."
    exit 1
fi

print_success "Docker is running"

# Step 7: Start PostgreSQL
print_status "Starting PostgreSQL..."
if docker ps | grep -q "postgres"; then
    print_success "PostgreSQL is already running"
else
    docker run -d --name postgres \
        -e POSTGRES_DB=genai_launchpad \
        -e POSTGRES_USER=postgres \
        -e POSTGRES_PASSWORD=customer_support_password \
        -p 5432:5432 \
        postgres:15
    print_success "PostgreSQL started"
fi

# Step 8: Start Redis
print_status "Starting Redis..."
if docker ps | grep -q "redis"; then
    print_success "Redis is already running"
else
    docker run -d --name redis -p 6379:6379 redis:latest
    print_success "Redis started"
fi

# Step 9: Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 5

# Step 10: Set environment variables
export DATABASE_HOST=localhost
export DATABASE_NAME=genai_launchpad
export DATABASE_USER=postgres
export DATABASE_PASSWORD=customer_support_password
export DATABASE_PORT=5432
export OLLAMA_BASE_URL=http://localhost:11434

print_success "Environment variables set"

# Step 11: Test the system
print_status "Testing the system..."
if python test_customer_support.py; then
    print_success "System test passed!"
else
    print_warning "System test failed. You can still try running the playground."
fi

# Step 12: Show next steps
echo ""
echo "🎉 Deployment completed!"
echo "========================"
echo ""
echo "Next steps:"
echo "1. Test the system:"
echo "   python test_customer_support.py"
echo ""
echo "2. Use the interactive playground:"
echo "   python playground/customer_support_playground.py"
echo ""
echo "3. Start the API server (optional):"
echo "   export DATABASE_HOST=localhost && export DATABASE_NAME=genai_launchpad && export DATABASE_USER=postgres && export DATABASE_PASSWORD=customer_support_password && export DATABASE_PORT=5432 && export OLLAMA_BASE_URL=http://localhost:11434 && uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8080"
echo ""
echo "4. View documentation:"
echo "   cat CUSTOMER_SUPPORT_README.md"
echo ""
echo "Services running:"
echo "✅ Ollama (LLM): http://localhost:11434"
echo "✅ PostgreSQL: localhost:5432"
echo "✅ Redis: localhost:6379"
echo ""
echo "Happy testing! 🚀"





