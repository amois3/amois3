# Aleksejs Moisejevs

**AI Software Engineer — agent runtimes, grounded AI, multimodal SaaS**

Latvia (EU) · open to remote roles worldwide · [amoisejevs3@gmail.com](mailto:amoisejevs3@gmail.com) · [LinkedIn](https://www.linkedin.com/in/moisejevs/)

---

I build agents that run unattended and are trusted with real access — to a
filesystem, to devices, to money. That last part is most of the work: an agent
is easy to demonstrate and hard to leave running, and the difference is
approval gates, kernel-level confinement, permission matrices, and failure
that announces itself instead of going quiet.

Architecture, APIs, safety model, interface, deployment — and the part where it
still works the next morning.

---

## Selected systems

**TITAN — self-hosted personal AI platform** · [`titan_agent_case_study`](https://github.com/amois3/titan_agent_case_study)<br>
An original ReAct runtime with dynamic model and tool routing, 61 registered
tools, persistent vector and graph memory, proactive scheduled workflows, and
approval gates on anything irreversible. Runs unattended on Linux and Docker
behind a FastAPI + Next.js PWA with WebSockets, voice, file handling,
scheduling, monitoring, device integration, event journaling and remote coding
sessions.

The linked repository is the provider and memory core, extracted and runnable:
role-to-model routing with a provider fallback, the memory graph, atomic
storage, and 17 tests pinning two defects that failed silently — an empty
answer returned as a success, and an image dropped from the request without a
word. The four design documents ship with it, including the one about giving an
agent access to money.

**AI NCP — grounded, permission-aware platform**<br>
Memory-first architecture with permission-aware semantic and lexical recall,
source-validated generation, private-room isolation, human review and
correction, and per-provider execution policy. TypeScript monorepo across
Next.js, NestJS, workers, Expo and PostgreSQL/pgvector. Verified at 20/20 on
grounding and refusal evaluations, and 110/110 on the permission matrix.

**TITAN Code — coding agent CLI** · [`titan_code_case_study`](https://github.com/amois3/titan_code_case_study)<br>
TypeScript, with its own tool loop and a terminal interface written directly
against ANSI — an alternate screen buffer, scroll regions, eight zones — rather
than on a UI framework. MCP over stdio and Streamable HTTP with tools,
resources and prompts. Subagents, skills, hooks, session persistence, context
compaction, and 35 slash commands.

Shell commands are confined by the operating system: bubblewrap on Linux,
Seatbelt on macOS. Command text is parsed rather than pattern-matched, paths
are resolved through symlinks before the containment check, and anything
irreversible is confirmed. Runs on Linux, macOS and Windows, with CI on all
three across three Node versions.

The linked repository is that security core, extracted and runnable: the shell
lexer and the policy over it, path containment through symlinks, the bubblewrap
and Seatbelt backends, and the SSRF checks. Zero runtime dependencies, 62 tests,
CI on nine platform and version combinations.

**Snapence / NutriAI — multimodal nutrition SaaS**<br>
Meal logging by photo, voice or text. Firebase auth, Stripe, FastAPI and
MongoDB behind an installable PWA in nine languages, with medical-safety
guardrails on generated advice.

**TITAN Marketing / Meet AI Summary**<br>
Hypothesis-to-measurement experiments with Thompson sampling, deterministic
rewards and attribution reporting. Caption–audio fusion with live translation,
evidence-backed reports and searchable meeting memory.

---

## How I work

Agentic development. I design the architecture, orchestrate the agents that
implement it, and own the outcome.

The bar for what ships does not move because of that. Tests that fail for a
real reason rather than for a changed string. CI on every platform the thing
claims to support. Documentation checked against the code instead of written
from memory. Security decided by what the operating system enforces, not by
what a command looks like.

---

## Open source

**[Matrix Watcher](https://matrixwatcher.space)** · [`matrixwatcher.space`](https://github.com/amois3/matrixwatcher.space)<br>
Monitors nine independent real-world systems — crypto markets, earthquakes,
space weather, quantum randomness and others — for cross-domain correlation.
Pure statistics, no model in the loop. Running 24/7 and publishing the result
it actually found: no significant signal so far. Reporting an absence is the
point; a monitor that only announces discoveries is not measuring anything.

**[`yield_monitor`](https://github.com/amois3/yield_monitor)**<br>
Manufacturing test-yield dashboard, built to a written specification. FastAPI
and SQLite behind a three-panel dashboard — daily volume, part distribution,
yield gauge — with a manual entry form, a natural-language query endpoint, and
a Selenium script that drives the browser end to end and asserts the yield
calculation is correct.

---

## Stack

| | |
|---|---|
| **Languages** | Python · TypeScript |
| **Backend** | FastAPI · NestJS · WebSockets · PostgreSQL/pgvector · MongoDB · SQLite |
| **Frontend** | Next.js · React · Expo · PWA |
| **Infrastructure** | Linux · Docker · self-hosted deployment · GitHub Actions |
| **Models** | OpenRouter · OpenAI · Anthropic · Google |
| **Practice** | agentic tool calling · RAG and grounded generation · vector and graph memory · human-in-the-loop approval · AI safety and evaluations · multimodal systems · test automation |

---

Open to remote full-time and contract work.
[amoisejevs3@gmail.com](mailto:amoisejevs3@gmail.com)
