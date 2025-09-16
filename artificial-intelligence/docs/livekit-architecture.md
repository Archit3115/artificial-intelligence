# LiveKit — Architecture Documentation (Markdown)

> Purpose: comprehensive architecture doc + deep dive on LiveKit internals, explicit workflow diagrams, and executable diagrams in **mermaid.js**.  
> Audience: engineers who need to design, operate, or extend LiveKit (self-hosted or Cloud).

---

## Table of contents
1. [Executive summary](#executive-summary)  
2. [High-level components](#high-level-components)  
3. [Control plane vs Media plane](#control-plane-vs-media-plane)  
4. [Key workflows (with mermaid diagrams)](#key-workflows-with-mermaid-diagrams)  
   - Client Join / Token flow  
   - Publish / Subscribe sequence (two PeerConnections)  
   - Simulcast / Layer selection & SFU forwarding  
   - Multi-node routing & Redis mesh  
   - Recording / Ingest / Server API usage  
5. [Deep dive: SFU internals & media pipeline](#deep-dive-sfu-internals--media-pipeline)  
6. [Scaling, HA, and deployment patterns](#scaling-ha-and-deployment-patterns)  
7. [Operational considerations & troubleshooting tips](#operational-considerations--troubleshooting-tips)  
8. [Appendix — mermaid templates you can paste anywhere](#appendix---mermaid-templates-you-can-paste-anywhere)  
9. [References](#references)

---

## Executive summary
LiveKit is an open-source WebRTC stack built to act as a scalable SFU (Selective Forwarding Unit). It provides client SDKs, a server (written in Go using Pion), server APIs for room/participant management, and an architecture that supports single-node deployments as well as multi-node, globally-distributed Cloud deployments. LiveKit separates signaling/control (WebSocket + protobuf) from the media forwarding plane (WebRTC RTP PeerConnections) and uses a distributed routing layer (Redis) when used in multi-node mode.

---

## High-level components
- **Client SDKs** (browser, iOS, Android, server SDKs): handle capture, rendering, encoding/decoding, and the LiveKit client protocol. Clients speak a protobuf over WebSocket to the server for signaling and open up WebRTC PeerConnections to the SFU.  
- **LiveKit Server (SFU)**: the media node that receives RTP from publishers and forwards RTP to subscribers (selective forwarding). Implemented in Go using Pion. Can run as one node or as many nodes.  
- **Redis (routing layer)**: used to coordinate multi-node deployments (peer routing / room-to-node mapping). Required for distributed setups.  
- **STUN/TURN**: for NAT traversal and relaying media as needed. (Standard WebRTC components.)  
- **Application Server / Auth**: your application issues JWT tokens (or uses LiveKit auth patterns) and calls LiveKit Server APIs (manage rooms, participants, SIP trunking, recording).  
- **Optional components**: recording workers, ingestion (RTMP), media processors (transcription/AI pipelines), SIP gateways.

---

## Control plane vs Media plane
- **Control plane**: WebSocket + protobuf messages between client and server (join, publish intent, subscription updates, metadata, data channel control). This is reliable, ordered, and used to coordinate state.  
- **Media plane**: UDP (RTP/RTCP) over WebRTC PeerConnections. Typically two PeerConnections per client: one for subscribing (always open), one for publishing (opened when the client actually publishes). SFU receives RTP, performs any transformations (e.g., SSRC mapping, simulcast selection, RTX/FEC), and forwards RTP to subscribers.

---

## Key workflows (with mermaid diagrams)

### 1) Client Join / Token issuance (high level)
```mermaid
sequenceDiagram
  participant AppServer
  participant Client
  participant LiveKitAPI
  participant LiveKitSFU

  AppServer->>AppServer: Create JWT (API key / claims)
  AppServer->>Client: Return join token (JWT)
  Client->>LiveKitAPI: WebSocket connect + token (proto)
  LiveKitAPI-->>Client: Auth OK, room state (participants, tracks)
  Client->>LiveKitSFU: Open subscriber PeerConnection (SDP)
  LiveKitSFU-->>Client: Subscriber SDP answer
```

---

### 2) Publish / Subscribe sequence (two PeerConnections)
```mermaid
sequenceDiagram
  participant Client
  participant LiveKit (Control)
  participant LiveKitSFU (Media)
  participant OtherClient

  Client->>LiveKit (Control): "I will publish track X" (proto)
  LiveKit-->>Client: ack/offer to create publisher PC
  Client->>LiveKitSFU: Create publisher PeerConnection (SDP offer)
  LiveKitSFU-->>Client: publisher SDP answer
  Client->>LiveKitSFU: Send RTP (video/audio)
  LiveKitSFU->>OtherClient: Forward RTP (subscriber PC)
```

---

### 3) Simulcast + layer selection (Video quality adaptation)
```mermaid
flowchart TD
  subgraph Publisher
    A(Camera) -->|encodes| B[Simulcast L0 (low)]
    A -->|encodes| C[Simulcast L1 (med)]
    A -->|encodes| D[Simulcast L2 (high)]
  end
  B -->|RTP| SFU
  C -->|RTP| SFU
  D -->|RTP| SFU
  subgraph SFU
    SFU -->|select layer per subscriber| E(Subscriber 1)
    SFU -->|select different layer| F(Subscriber 2)
  end
```

---

### 4) Multi-node routing and Redis mesh
```mermaid
graph TD
  subgraph Region-A
    LK1[LiveKit Node A]
    ClientA -->|WebSocket| LK1
    ClientB -->|WebSocket| LK1
  end
  subgraph Region-B
    LK2[LiveKit Node B]
    ClientC -->|WebSocket| LK2
  end

  LK1 ---|pubsub/room routing| Redis
  LK2 ---|pubsub/room routing| Redis

  LK1 -->|RTP direct to| LK2
  LK2 -->|RTP direct to| LK1
```

---

### 5) Recording & Ingest pipeline (typical)
```mermaid
sequenceDiagram
  participant Client
  participant LiveKitSFU
  participant RecorderWorker
  participant Storage

  Client->>LiveKitSFU: Publish track(s)
  LiveKitSFU->>RecorderWorker: Stream copies (RTP / internal API)
  RecorderWorker->>Storage: Persist segments / files
```

---

## Deep dive: SFU internals & media pipeline
- Written in **Go** using **Pion**.  
- Publisher sends RTP → SFU maps SSRCs → optionally selects simulcast layers → forwards RTP to subscribers.  
- Bandwidth estimation done per-subscriber, informs simulcast selection.  
- Two PeerConnections: subscriber (always), publisher (on demand).

---

## Scaling, HA, and deployment patterns
- **Single-node**: simple but limited.  
- **Multi-node with Redis**: recommended for scale. Redis manages pub/sub, presence, and routing.  
- **Global clusters**: mesh design, regional nodes, 99.99% uptime possible.  
- **Kubernetes**: containers, autoscaling, Redis as stable store.

---

## Operational considerations
- Monitor CPU, bandwidth, PeerConnections, packet loss.  
- Use TURN for NAT traversal reliability.  
- Debug with RTCP and LiveKit verbose logs.

---

## Appendix — mermaid templates

### System architecture
```mermaid
flowchart LR
  subgraph Clients
    A[Browser SDK]
    B[iOS/Android SDK]
  end
  subgraph AppLayer
    AppServer[Your App Server (issue tokens)]
  end
  subgraph LiveKitCluster
    LK1[LiveKit Node 1]
    LK2[LiveKit Node 2]
    Redis[(Redis)]
    TURN[(TURN)]
  end
  A -->|WebSocket + Token| LK1
  B -->|WebSocket + Token| LK2
  AppServer -->|JWT / REST| LK1
  LK1 --- Redis
  LK2 --- Redis
  LK1 --- TURN
  LK2 --- TURN
```

### Join → Publish → Subscribe
```mermaid
sequenceDiagram
  participant App
  participant Client
  participant LiveKit
  participant SFU

  App->>Client: JWT token
  Client->>LiveKit: WS connect (token)
  LiveKit-->>Client: room state
  Client->>SFU: create publisher PC (offer)
  SFU-->>Client: publisher answer
  Client->>SFU: RTP -> publish
  SFU->>OtherClient: RTP -> subscriber
```