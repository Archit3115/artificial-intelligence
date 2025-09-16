# LiveKit + ElevenLabs Architecture

This document describes a production-ready architecture for a real-time voice agent using LiveKit (WebRTC) and ElevenLabs' speech models.

## 🚀 Key Technologies

* **WebRTC**: The foundational real-time media transport protocol (`RTCPeerConnection`, `MediaStream`, `RTCDataChannel`). It enables direct browser-to-browser communication.
* **LiveKit**: A scalable, open-source WebRTC platform that provides a Selective Forwarding Unit (SFU), SDKs, and server APIs/webhooks to simplify building real-time applications.
* **ElevenLabs**: A service providing high-quality, natural-sounding speech synthesis. For real-time conversational agents, the low-latency `eleven_flash_v2_5` model is recommended.

## 📊 Architecture Diagram

The diagram below shows the high-level components and the main data flows between them. 

```mermaid
# LiveKit + ElevenLabs Architecture

This document explains a production-ready architecture for a real-time voice agent using LiveKit (WebRTC) and ElevenLabs. It contains a single, GitHub-friendly Mermaid diagram, component notes, a typical interaction flow, and tips for rendering.

## Key technologies

- **WebRTC** — real-time media transport (`RTCPeerConnection`, `MediaStream`, `RTCDataChannel`)
- **LiveKit** — scalable SFU, SDKs, and server APIs/webhooks
- **ElevenLabs** — high-quality speech synthesis (consider `eleven_flash_v2_5` for low-latency scenarios)

## Architecture diagram (Mermaid)

The diagram below uses compact node labels and `graph TD` so GitHub's Mermaid renderer handles it reliably.

```mermaid
graph TD
    subgraph ClientApp
        Client[User App]
        SDK[LiveKit SDK]
    end

    subgraph Backend
        Server[App Server]
        Auth[Auth Service]
        Agent[AI Agent]
        Adapter[ElevenLabs Adapter]
        LiveKitAPI[LiveKit Management API]
    end

    subgraph LiveKit
        SFU[LiveKit SFU]
        API[LiveKit API]
        Egress[Egress]
    end

    subgraph External
        Eleven[ElevenLabs API]
    end

    Client --> SDK
    SDK -->|WSS token| SFU
    Auth -->|token| SDK
    SDK -->|publish| SFU
    SFU -->|subscribe| SDK

    Server --> Auth
    Server --> Agent
    Agent --> Adapter
    Server --> LiveKitAPI

    LiveKitAPI --> API
    API --> SFU
    Agent -->|AI audio| SFU
    Adapter -->|HTTP| Eleven
    Eleven --> Adapter

    classDef client fill:#E3F2FD,stroke:#0D47A1
    classDef server fill:#E8F5E9,stroke:#1B5E20
    classDef infra fill:#FFF3E0,stroke:#E65100
    classDef ext fill:#F3E5F5,stroke:#6A1B9A

    class Client,SDK client
    class Server,Auth,Agent,Adapter,LiveKitAPI server
    class SFU,API,Egress infra
    class Eleven ext
```

## Component notes

- **Auth Service**: Issues short-lived LiveKit tokens and controls room permissions.
- **App Server**: Orchestrates room lifecycle, issues tokens, and manages control-plane actions.
- **AI Agent**: Joins rooms (or uses egress/ingress), subscribes to audio, runs models/transcription, and publishes synthesized audio.
- **ElevenLabs Adapter**: Calls ElevenLabs APIs to synthesize audio for the AI Agent to publish.
- **LiveKit SFU**: Routes publish/subscribe media; use server API/webhooks for room events.

## Typical interaction flow

1. Client requests a LiveKit token from App Server.
2. Client connects to LiveKit SFU using that token (WSS) and establishes PeerConnections.
3. Client publishes microphone/audio tracks to the SFU.
4. App Server launches or signals an AI Agent into the room.
5. Agent subscribes to user audio, transcribes/processes it, generates a response, and sends text to ElevenLabs.
6. ElevenLabs returns synthesized audio; Agent publishes the audio track back into the room.
7. Clients hearing the room receive and play the AI audio.

## Tips for reliable rendering

- Refer to the Mermaid docs: https://mermaid.js.org/intro/ for syntax and examples.
- Keep labels short and avoid punctuation like parentheses and slashes inside node IDs/labels.
- For deterministic previews, add a GitHub Action to run the Mermaid CLI (`mmdc`) to output an SVG into `docs/diagrams`.

---

If you want, I can add a small GitHub Action that renders this diagram to `docs/diagrams/livekit-architecture.svg`, or open a PR from `dev-101` to `main` with this change.