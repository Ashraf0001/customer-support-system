# User Guide

## Where to go
- Web app: `http://localhost:8080/ui`
- Help site: `http://127.0.0.1:9000`

## Submit a ticket
1. Open the web app
2. Enter Email, Subject, Message, and Priority
3. Click Submit – the ticket appears in the list
4. The list auto-refreshes every 10 seconds; you can also click Refresh

## See the response
- A background worker processes your ticket and generates an AI response
- The ticket card shows Status, Category, Sentiment, Urgency, and AI Response
- If an error occurs, it will show under the ticket card

## If responses don’t show
- Ensure the worker is running
- The first run of the AI model can take some time to warm up
- Submit again after a minute if needed

## Privacy
- This runs locally; your data stays on your machine


