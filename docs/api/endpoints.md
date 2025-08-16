# API Endpoints

## Health
- `GET /healthz` → ok
- `GET /readyz` → ready

## Support Tickets
- `POST /support/tickets`
  - body: SupportTicketSchema
  - returns: 202 Accepted with `ticket_id`, `task_id`
- `GET /support/tickets`
  - query: `limit`, `offset`, `status`, `customer_email`
  - returns: list of tickets (filtered if query provided)
- `GET /support/tickets/{ticket_id}`
  - returns: ticket details
- `POST /support/tickets/{ticket_id}/retry`
  - re-queue a failed ticket for processing; 202 on success

