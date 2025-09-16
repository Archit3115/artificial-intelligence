---
title: LiveKit Architecture
---

# LiveKit Architecture (Mermaid)

This document contains a Mermaid diagram that visualizes the core LiveKit architecture: clients, signaling, SFU routing, TURN/STUN, recording/ingestion, and optional external services.

```mermaid
flowchart LR
  subgraph Clients
    A[Web Client]:::client
    B[Mobile Client]:::client
    C[SDK Consumer]:::client
  end

  subgraph LiveKit_Server
    direction TB
    S(SFU Router):::server
    Sig(Signaling):::server
    Recorder(Recording/RTMP Ingest):::server
    Storage[(Object Storage)]:::storage
  end

  subgraph Network
    TURN[TURN/STUN]:::infra
    CDN[CDN/RTMP/Streaming]:::infra
  end

  A -->|Websocket/WSS| Sig
  B -->|Websocket/WSS| Sig
  C -->|SDK| Sig

  Sig --> S
  S --> TURN
  S --> Recorder
  Recorder --> Storage
  S --> CDN

  classDef client fill:#E3F2FD,stroke:#0D47A1;
  classDef server fill:#E8F5E9,stroke:#1B5E20;
  classDef infra fill:#FFF3E0,stroke:#E65100;
  classDef storage fill:#F3E5F5,stroke:#6A1B9A;

  click Sig href "https://docs.livekit.io/architecture/overview" "LiveKit Signaling docs"
```

Notes:
- Paste this Markdown file into your repository and GitHub will render the Mermaid diagram on the file page (GitHub supports Mermaid in Markdown).
- You can edit nodes and edges in the `flowchart` block to match your exact LiveKit deployment (participants, rooms, media servers, scale-out patterns).
