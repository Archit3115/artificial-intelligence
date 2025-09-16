Architecture Overview: LiveKit, ElevenLabs v3 & WebRTC

This document outlines the architecture of a real-time communication system utilising the LiveKit platform, which is built on WebRTC, and integrates with ElevenLabs' v3 speech synthesis models for advanced AI-driven audio experiences.
1. Core Technologies
• WebRTC (Web Real-Time Communication): This is the foundational technology that enables peer-to-peer streaming of audio, video, and arbitrary data directly between browsers and applications without needing plugins. It is optimised for media, resilient to poor network conditions, and natively supported by modern browsers. Key components include RTCPeerConnection for managing connections between peers, MediaStream for audio/video tracks, and RTCDataChannel for arbitrary data exchange.
• LiveKit: An open-source platform that simplifies the development of real-time media applications by managing the complexities of production-grade WebRTC infrastructure. It provides scalable media servers, comprehensive SDKs for various platforms, and a rich ecosystem for building features like AI assistants, video conferencing, and interactive livestreaming.
• ElevenLabs v3: An advanced, emotionally rich speech synthesis model designed for creating natural, life-like speech. It is particularly effective for character discussions, audiobook production, and emotional dialogue, supporting over 70 languages. While not intended for ultra-low-latency real-time applications itself, it can be used to generate high-quality audio assets that are then streamed via LiveKit. For real-time conversational AI, other models like Eleven Flash v2.5 are recommended due to their low latency.
2. System Architecture Diagram (Mermaid JS)
Here is a Mermaid JS diagram illustrating how these components interact. This shows a common use case where a client application connects to a LiveKit Room, and an AI Agent (powered by your backend server and ElevenLabs) also joins the room to interact with the user.
graph TD
    subgraph "Client Application (Web/Mobile)"
        A[User's Browser/App]
        SDK[LiveKit Client SDK]
        A -- Manages Connection --> SDK
    end

    subgraph "Your Backend Infrastructure"
        B[Application Server]
        C[Authentication Service]
        D[AI Agent Logic]
        E[ElevenLabs API Integration]
        F[LiveKit Server API/Webhooks]

        B -- Generates Token --> C
        B -- Controls Agent --> D
        D -- "Generates speech (e.g., Eleven v3 for high quality, Flash for low latency)" --> E
        B -- "Manages Rooms/Participants" --> F
    end

    subgraph "LiveKit Platform (Cloud or Self-Hosted)"
        G[LiveKit Server / Media Server]
        H[Server API Endpoint]
        I[Egress/Ingress Services]

        G -- Handles Media Streams --> I
    end

    subgraph "External Services"
        J[ElevenLabs API]
    end

    %% Connections and Data Flow
    SDK -- "Connects with Token (WSS)" --> G
    C -- "Returns Access Token" --> SDK
    SDK -- "Publishes Audio/Video Tracks" --> G
    G -- "Subscribes to Remote Tracks" --> SDK

    F -- Interacts with --> H
    H -- Forwards to --> G
    D -- "Publishes AI-Generated Audio Track" --> G
    E -- "HTTP/WebSocket Request to" --> J
    J -- "Returns Synthesised Audio" --> E

    style A fill:#cde4ff,stroke:#333
    style B fill:#d5e8d4,stroke:#333
    style G fill:#fff2cc,stroke:#333
    style J fill:#f8cecc,stroke:#333
---
title: LiveKit + ElevenLabs Architecture
---

# LiveKit + ElevenLabs Architecture

This document describes a production-ready architecture for a real-time voice agent using LiveKit (WebRTC) and ElevenLabs' speech models. It includes a clear Mermaid diagram, component breakdown, and an example interaction flow.

## Key technologies

- **WebRTC**: Real-time media transport (RTCPeerConnection, MediaStream, RTCDataChannel).
- **LiveKit**: Scalable WebRTC SFU and SDKs for building rooms, publishing/subscribing to media, and server APIs/webhooks.
- **ElevenLabs**: High-quality speech synthesis (use `eleven_flash_v2_5` for low-latency real-time scenarios).

## Architecture diagram (Mermaid)

The diagram below shows the high-level components and main data flows.

```mermaid
graph TD
    subgraph ClientApp[Client Application (Web / Mobile)]
        A[User Browser / App]
        SDK[LiveKit Client SDK]
        A --> SDK
    end

    subgraph Backend[Your Backend Infrastructure]
        B[Application Server]
        C[Auth Service]
        D[AI Agent]
        E[ElevenLabs Integration]
        F[LiveKit Management API]
        B --> C
        B --> D
        D --> E
        B --> F
    end

    subgraph LiveKit[LiveKit Platform]
        G[LiveKit SFU / Media Server]
        H[API / Webhooks]
        I[Egress / Ingress]
        G --> I
    end

    subgraph External[External Services]
        J[ElevenLabs API]
    end

    %% Connections
    SDK -->|WSS (token)| G
    C -->|Access Token| SDK
    SDK -->|publish tracks| G
    G -->|subscribe tracks| SDK

    F --> H
    H --> G
    D -->|publish AI audio| G
    E -->|HTTP/WS| J
    J --> E

    classDef client fill:#E3F2FD,stroke:#0D47A1;
    classDef server fill:#E8F5E9,stroke:#1B5E20;
    classDef infra fill:#FFF3E0,stroke:#E65100;
    classDef storage fill:#F3E5F5,stroke:#6A1B9A;
```

## Component notes

- **Auth Service**: Issues time-limited LiveKit tokens that identify users and grant room permissions.
- **AI Agent**: Backend process that can join rooms as a participant, subscribe to user audio, and publish synthesized audio responses.
- **ElevenLabs Integration**: Calls ElevenLabs' API to synthesize audio; choose `eleven_flash_v2_5` for low-latency use cases.

## Typical flow

1. Client requests a LiveKit token from `Application Server`.
2. Client connects to LiveKit SFU using the token (WSS) and establishes a WebRTC PeerConnection.
3. Client publishes local microphone/audio tracks to the SFU.
4. Backend spawns or signals an `AI Agent` to join the same room.
5. `AI Agent` subscribes to the user's audio, processes/transcribes it, generates a response, and sends text to ElevenLabs.
6. ElevenLabs returns synthesized audio, which the `AI Agent` publishes back to the LiveKit room.
7. Clients subscribed to the AI Agent hear the generated audio in real time.

## Tips

- For deterministic rendering or export, use the Mermaid CLI (`mmdc`) in CI to generate PNG/SVG images of the diagram.
- Keep node labels short in Mermaid; avoid nested parentheses and slashes where possible to reduce parser issues.

*** End Patch
