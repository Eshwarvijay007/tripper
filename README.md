# tripper
sequenceDiagram
  autonumber
  participant FE as Frontend (ChatPanel)
  participant API as Backend /api/chat
  participant Store as In-memory Stores

  FE->>API: POST /api/chat/messages {content, conversation_id?}
  API->>Store: Create/append message
  API-->>FE: {conversation_id, message_id, stream_url}

  FE->>API: GET /api/chat/stream/{conversation_id}
  Note over API: NDJSON stream (start, tokens..., done)
  API-->>FE: data: {"event":"start"}
  API-->>FE: data: {"event":"token","text":"..."}
  API-->>FE: data: {"event":"done"}
