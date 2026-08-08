# Aleksejs Moisejevs


**AI Systems Architect & Agentic Product Builder**


Agent runtimes · grounded AI · multimodal AI products  
Latvia (EU) · open to remote roles worldwide · [LinkedIn](https://www.linkedin.com/in/moisejevs/) · [GitHub](https://github.com/amois3)


---


I build AI-native products where the difficult part is not demonstrating an agent, but making it safe, observable, and dependable enough to run with real access. My work spans agent runtimes, permission-aware and source-grounded AI, persistent memory, multimodal product experiences, and production delivery.


## Public technical case studies

[**AI NCP — permission and grounding core**](https://github.com/amois3/ai_ncp_case_study) · [**TITAN Marketing Agent — deterministic experimentation core**](https://github.com/amois3/titan_marketing_agent_case_study)

## Selected systems


**TITAN Code — independent TypeScript coding-agent CLI** · [public security-core case study](https://github.com/amois3/titan_code_case_study)


An independent coding agent with its own tool loop, ANSI terminal renderer, sessions, permissions, MCP, subagents, skills, hooks, and context management. The security model uses OS confinement where supported: bubblewrap on Linux and Seatbelt on macOS, with deliberate policy and confirmation on Windows. The public case study is a runnable, dependency-free security core covering shell parsing, symlink-aware path containment, process isolation, and SSRF checks, with 62 tests and CI across nine platform/version combinations.


**TITAN — self-hosted personal AI platform** · [public provider-and-memory-core case study](https://github.com/amois3/titan_agent_case_study)


A self-hosted personal AI platform with an original ReAct runtime, dynamic model and tool routing, persistent graph and vector memory, proactive scheduled work, and approval gates for irreversible actions. It runs unattended on a single Linux host behind FastAPI, a Next.js PWA, and WebSockets, with integrations for files, email, devices, and supervised trading workflows.


**TITAN Marketing Agent — autonomous growth experimentation engine** · [public case study](https://github.com/amois3/titan_marketing_agent_case_study)


A controlled experimentation loop for product marketing: model-assisted hypothesis and content generation, Thompson-sampling planning, tracked clicks and conversion events, deterministic rewards, and durable insight memory. Channel autonomy is explicit; voice quality is bounded by approved samples, critic passes, deterministic gates, and restart-safe database-backed orchestration.


**AI NCP — AI-native community operating system** · [public case study](https://github.com/amois3/ai_ncp_case_study)


A memory-first social platform for invite-only professional communities - not a chatbot, feed clone, or generic RAG layer. Its core object is a living Space: people, rooms, threads, presence, permissions, events, memory, and AI-native navigation.


The AI layer is bounded by product architecture. It retrieves only sources a member may access; answers are source-linked; private rooms remain isolated; memory carries scope, visibility, confidence, correction history, and auditability; providers are controlled by execution policy. The local-alpha foundation spans Next.js, NestJS, Expo, workers, PostgreSQL/pgvector, Redis, and shared TypeScript packages.


**Multimodal AI products**


[**nutrition_bot**](https://github.com/amois3/nutrition_bot) is an AI nutrition assistant with photo, voice, and natural-language meal logging, personal context, scheduled reports, analytics, access controls, and Docker deployment.


[**Snapence**](https://github.com/amois3/snapence_android) is a multilingual nutrition product across FastAPI, React PWA, and Kotlin/Jetpack Compose Android, with Firebase identity, MongoDB, nine checked locales, and Google Play entitlements.


[**Meet AI Summary**](https://github.com/amois3/meet_ai_summary) is a Google Meet Chrome Extension and meeting-analysis service: live English-to-Russian caption translation, user-initiated audio recovery for incomplete captions, canonical transcripts, verified reports, meeting chat, and search.


## How I work


Agentic development. I design the architecture, orchestrate the agents that implement it, and own the outcome.


The bar for what ships does not move because of that. Tests that fail for a real reason rather than for a changed string. CI on every platform the thing claims to support. Documentation checked against the code instead of written from memory. Security decided by what the operating system enforces, not by what a command looks like.
