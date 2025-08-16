#!/usr/bin/env python3
"""
Simple test script for Customer Support System
Tests the workflow without the full API stack
"""

import os
import sys
import time
import json
from datetime import datetime
import pytest

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Set environment variables
os.environ['DATABASE_HOST'] = 'localhost'
os.environ['DATABASE_NAME'] = 'genai_launchpad'
os.environ['DATABASE_USER'] = 'postgres'
os.environ['DATABASE_PASSWORD'] = 'customer_support_password'
os.environ['DATABASE_PORT'] = '5432'
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434'

@pytest.mark.integration
def test_ollama_connection():
    """Test if Ollama is running and accessible"""
    import requests
    response = requests.get("http://localhost:11434/api/tags")
    assert response.status_code == 200
    models = response.json().get("models", [])
    assert isinstance(models, list)

def test_workflow_imports():
    """Test if we can import our workflow components"""
    from app.schemas.customer_support_schema import SupportTicketSchema  # noqa: F401
    from app.workflows.customer_support_workflow import CustomerSupportWorkflow  # noqa: F401
    from app.workflows.customer_support_nodes.analyze_ticket_node import AnalyzeTicketNode  # noqa: F401
    from app.workflows.customer_support_nodes.classify_ticket_node import ClassifyTicketNode  # noqa: F401
    from app.workflows.customer_support_nodes.generate_response_node import GenerateResponseNode  # noqa: F401

@pytest.mark.integration
def test_workflow_execution():
    """Test the complete workflow execution (integration with Ollama)."""
    from app.schemas.customer_support_schema import SupportTicketSchema
    from app.workflows.customer_support_workflow import CustomerSupportWorkflow

    # Create test ticket
    test_ticket = SupportTicketSchema(
        id="test_ticket_001",
        customer_email="test@example.com",
        subject="Test login issue",
        content="I'm having trouble logging into my account. The system keeps saying my password is incorrect.",
        priority="high",
    )

    workflow = CustomerSupportWorkflow()
    result = workflow.run(test_ticket)
    assert isinstance(result.nodes, dict)

def test_prompt_templates():
    """Test prompt template loading"""
    from app.services.prompt_loader import PromptManager

    # Test ticket analysis prompt
    test_ticket = {
        "subject": "Login issue",
        "content": "Cannot log in",
        "priority": "high",
    }

    prompt = PromptManager.get_prompt("ticket_analysis", ticket=test_ticket)
    assert "Ticket Information" in prompt

def main():
    """Run all tests"""
    print("🚀 Customer Support System - Lightweight MVP Test")
    print("=" * 60)
    
    tests = [
        ("Ollama Connection", test_ollama_connection),
        ("Workflow Imports", test_workflow_imports),
        ("Prompt Templates", test_prompt_templates),
        ("Workflow Execution", test_workflow_execution),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 40)
        
        try:
            result_val = test_func()
            success = True if result_val is None else bool(result_val)
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 Test Summary:")
    print("=" * 60)
    
    passed = 0
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Results: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("🎉 All tests passed! Your customer support system is working!")
    else:
        print("⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()


