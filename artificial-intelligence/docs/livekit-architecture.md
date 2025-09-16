---
title: LiveKit Architecture
---

# LiveKit Architecture

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
  # LiveKit Architecture (Mermaid)

  This document shows a concise, easy-to-read diagram of a typical LiveKit deployment. The diagram highlights the main components and the primary media/signaling flows:

  - Clients: web, mobile, and SDK-based participants
  - Signaling: connection and room control (WSS/websocket)
  - SFU Router: real-time media routing for efficient multi-party audio/video
  - TURN/STUN: NAT traversal for peer connectivity
  - Recording / RTMP ingest: capture or stream-out components
  - Storage: object store for recorded media or assets
  - CDN / RTMP: optional streaming/ingest paths

  The Mermaid block below renders the diagram on GitHub and in editors that support Mermaid.

  ```mermaid
  flowchart LR
    subgraph Clients
      A[Web Client]:::client
      B[Mobile Client]:::client
      C[SDK Consumer]:::client
    end

    subgraph LiveKit_Server
      direction TB
      Sig[Signaling (WSS / WebSocket)]:::server
      S[SFU Router (media plane)]:::server
      Recorder[Recording / RTMP Ingest]:::server
      Storage[(Object Storage)]:::storage
    end

    subgraph Network
      TURN[TURN / STUN (NAT traversal)]:::infra
      CDN[CDN / RTMP / Streaming]:::infra
    end

    A -->|WSS| Sig
    B -->|WSS| Sig
    C -->|SDK| Sig

    Sig -->|room control| S
    S -->|media relay| TURN
    S -->|stream out| CDN
    S -->|recording stream| Recorder
    Recorder -->|store| Storage

    classDef client fill:#E3F2FD,stroke:#0D47A1;
    classDef server fill:#E8F5E9,stroke:#1B5E20;
    classDef infra fill:#FFF3E0,stroke:#E65100;
    classDef storage fill:#F3E5F5,stroke:#6A1B9A;

    click Sig href "https://docs.livekit.io/architecture/overview" "LiveKit Signaling docs"
  ```

  ## How to use

  - Edit the Mermaid `flowchart` block to reflect your deployment (for example, add separate SFU worker pools, load balancers, or separate ingest clusters).
  - GitHub renders Mermaid diagrams inside Markdown files automatically — open this file in the repo to see the diagram.
  - For higher-fidelity or exportable images, consider using the Mermaid CLI (`mmdc`) in CI to generate PNG/SVG artifacts.

  ## Component notes

  - Signaling: handles room join/leave, participant metadata, and connection negotiation. Implemented over WSS.
  - SFU Router: relays media streams, handles simulcast, and performs RTP-level routing. Scales horizontally with worker nodes.
  - TURN/STUN: provides NAT traversal when direct peer connectivity is not possible.
  - Recording / RTMP Ingest: optional components that capture streams for storage or broadcast.
  - Storage: object stores (S3, GCS) used for saving recordings, logs, and assets.

  You can expand this diagram with swimlanes, more detailed subgraphs, or use `graph TD` for layered flows.
