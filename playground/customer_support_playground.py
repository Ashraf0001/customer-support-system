#!/usr/bin/env python3
"""
Customer Support System Playground
Interactive testing environment for the customer support workflow
"""

import os
import sys
import json
import time
from datetime import datetime

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

# Set environment variables
os.environ['DATABASE_HOST'] = 'localhost'
os.environ['DATABASE_NAME'] = 'genai_launchpad'
os.environ['DATABASE_USER'] = 'postgres'
os.environ['DATABASE_PASSWORD'] = 'customer_support_password'
os.environ['DATABASE_PORT'] = '5432'
os.environ['OLLAMA_BASE_URL'] = 'http://localhost:11434'

def create_sample_tickets():
    """Create sample tickets for testing"""
    return [
        {
            "id": "ticket_001",
            "customer_email": "john@example.com",
            "subject": "Login issues with my account",
            "content": "I'm unable to log into my account. I keep getting an error message saying 'Invalid credentials' even though I'm sure my password is correct. I've tried resetting my password twice but the issue persists.",
            "priority": "high"
        },
        {
            "id": "ticket_002", 
            "customer_email": "sarah@example.com",
            "subject": "Billing question about my subscription",
            "content": "I noticed an unexpected charge on my credit card for $29.99. I don't remember upgrading my subscription. Can you help me understand what this charge is for?",
            "priority": "medium"
        },
        {
            "id": "ticket_003",
            "customer_email": "mike@example.com", 
            "subject": "Feature request: Dark mode",
            "content": "I love your application! It would be really helpful if you could add a dark mode option. I work late hours and the bright interface strains my eyes. This would be a great improvement for user experience.",
            "priority": "low"
        }
    ]

def run_workflow_test(ticket_data):
    """Run a single workflow test"""
    try:
        from app.schemas.customer_support_schema import SupportTicketSchema
        from app.workflows.customer_support_workflow import CustomerSupportWorkflow
        
        # Create ticket schema
        ticket = SupportTicketSchema(**ticket_data)
        
        print(f"\n📝 Processing Ticket: {ticket.subject}")
        print(f"   Customer: {ticket.customer_email}")
        print(f"   Priority: {ticket.priority}")
        print(f"   Content: {ticket.content[:100]}...")
        
        # Run workflow
        workflow = CustomerSupportWorkflow()
        start_time = time.time()
        
        print("\n🔄 Running AI workflow...")
        result = workflow.run(ticket)
        
        processing_time = time.time() - start_time
        
        # Display results
        print(f"\n✅ Workflow completed in {processing_time:.2f} seconds")
        print("\n📊 Results:")
        print("=" * 60)
        
        for node_name, node_result in result.nodes.items():
            print(f"\n🔹 {node_name}:")
            
            if node_result.get("status") == "completed":
                print(f"   Status: ✅ {node_result['status']}")
                
                # Analysis results
                if "classification" in node_result:
                    classification = node_result["classification"]
                    print(f"   📊 Classification:")
                    print(f"      Category: {classification.get('category', 'N/A')}")
                    print(f"      Sentiment: {classification.get('sentiment', 'N/A')}")
                    print(f"      Urgency: {classification.get('urgency', 'N/A')}")
                    print(f"      Confidence: {classification.get('confidence', 'N/A')}")
                
                # Response results
                if "response" in node_result:
                    response = node_result["response"]
                    print(f"   💬 AI Response:")
                    print(f"      Type: {response.response_type}")
                    print(f"      Confidence: {response.confidence}")
                    print(f"      Response: {response.response_text}")
                    
                    if response.suggested_actions:
                        print(f"      Suggested Actions: {', '.join(response.suggested_actions)}")
                
                # Performance
                if "processing_time" in node_result:
                    print(f"   ⏱️  Processing Time: {node_result['processing_time']:.2f}s")
                    
            else:
                print(f"   Status: ❌ {node_result.get('status', 'unknown')}")
                if "error" in node_result:
                    print(f"   Error: {node_result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def interactive_mode():
    """Run interactive mode for custom tickets"""
    print("\n🎮 Interactive Mode")
    print("Enter your own ticket details:")
    
    try:
        ticket_id = input("Ticket ID: ").strip() or "custom_ticket"
        customer_email = input("Customer Email: ").strip() or "customer@example.com"
        subject = input("Subject: ").strip() or "Custom ticket"
        content = input("Content: ").strip() or "This is a custom ticket for testing."
        priority = input("Priority (low/medium/high): ").strip() or "medium"
        
        ticket_data = {
            "id": ticket_id,
            "customer_email": customer_email,
            "subject": subject,
            "content": content,
            "priority": priority
        }
        
        return run_workflow_test(ticket_data)
        
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        return False

def main():
    """Main playground function"""
    print("🎯 Customer Support System - Lightweight MVP Playground")
    print("=" * 70)
    
    while True:
        print("\n📋 Choose an option:")
        print("1. Run sample tickets")
        print("2. Interactive mode (custom ticket)")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n🧪 Running sample tickets...")
            sample_tickets = create_sample_tickets()
            
            for i, ticket_data in enumerate(sample_tickets, 1):
                print(f"\n{'='*70}")
                print(f"Sample Ticket {i}/{len(sample_tickets)}")
                print(f"{'='*70}")
                
                success = run_workflow_test(ticket_data)
                
                if not success:
                    print(f"❌ Sample ticket {i} failed")
                    break
                
                if i < len(sample_tickets):
                    input("\nPress Enter to continue to next ticket...")
            
            print(f"\n✅ Completed {len(sample_tickets)} sample tickets")
            
        elif choice == "2":
            interactive_mode()
            
        elif choice == "3":
            print("\n👋 Thanks for testing! Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()





