<!--
═══════════════════════════════════════════════════════════════════════════════
SYNC IMPACT REPORT
═══════════════════════════════════════════════════════════════════════════════
Version Change: INITIAL → 1.0.0
Status: Initial constitution ratification

Principle Changes:
  - ADDED: I. AI-Native & Spec-Driven Development
  - ADDED: II. The Golden Rule: No Task = No Code
  - ADDED: III. Single Source of Truth (Markdown Specifications)
  - ADDED: IV. Iterative Evolution Through Phases
  - ADDED: V. No Manual Coding Mandate
  - ADDED: VI. Strict Workflow Adherence
  - ADDED: VII. Statelessness & Database Persistence

Section Changes:
  - ADDED: Technology Stack
  - ADDED: Development Workflow
  - ADDED: Coding Standards
  - ADDED: Project Phases
  - ADDED: Agent Behavior Rules
  - ADDED: Submission & Evaluation Requirements

Template Dependencies:
  ✅ plan-template.md - Constitution Check section will reference these principles
  ✅ spec-template.md - User story priorities align with iterative evolution principle
  ✅ tasks-template.md - Task breakdown aligns with No Task = No Code principle
  ⚠️  Command files - No agent-specific references found; templates remain generic

Follow-up TODOs:
  - None: All placeholders resolved

Rationale for MAJOR version (1.0.0):
  This is the initial constitution establishing all foundational governance principles
  and technical constraints for the project. Starting at 1.0.0 to indicate production
  readiness and formal adoption.
═══════════════════════════════════════════════════════════════════════════════
-->

# The Evolution of Todo - Project Constitution

## Core Principles

### I. AI-Native & Spec-Driven Development

**Role of Engineer**: "System Architect," not "Syntax Writer."

Development MUST follow the strict lifecycle without exception:
1. **Specify** → Define requirements, user journeys, acceptance criteria
2. **Plan** → Define architecture, schema, components, service boundaries
3. **Tasks** → Break down into atomic, testable units with unique IDs
4. **Implement** → Execute based only on authorized tasks

**Rationale**: This principle ensures that architecture and design decisions are made deliberately and documented before implementation begins. It prevents ad-hoc coding and maintains project coherence across all phases of evolution.

### II. The Golden Rule: No Task = No Code

**NON-NEGOTIABLE**: No agent or human is allowed to write or modify code until a corresponding task exists in the specification and has been approved.

**Enforcement**:
- Every code file MUST contain a comment linking it to the specific Task ID and Spec section
- Agents MUST stop and request clarification if no task exists for proposed work
- Code reviews MUST verify task linkage before approval

**Rationale**: This constraint ensures traceability, prevents scope creep, and maintains alignment between specification and implementation. It is the cornerstone of specification-driven development.

### III. Single Source of Truth (Markdown Specifications)

The Markdown specification files are the absolute authority for:
- Requirements (`specs/<feature>/spec.md`)
- Architecture decisions (`specs/<feature>/plan.md`)
- Task breakdowns (`specs/<feature>/tasks.md`)
- Project principles (`.specify/memory/constitution.md`)

**Rules**:
- If a requirement is missing, agents MUST stop and request clarification rather than improvising
- In case of conflict: **Constitution > Spec > Plan > Tasks**
- All specification files are versioned in Git alongside code

**Rationale**: Centralized, version-controlled specifications prevent ambiguity, enable automated validation, and serve as the contract between stakeholders and implementation teams.

### IV. Iterative Evolution Through Phases

The project MUST progress through five distinct phases sequentially, with each phase building upon the previous one without skipping steps:

**Phase I**: In-Memory Console App (Basic CRUD: Add, Delete, Update, View, Mark Complete)
**Phase II**: Full-Stack Web App (Persistent storage, RESTful API, User Authentication)
**Phase III**: AI-Powered Chatbot (Conversational interface, MCP integration, conversation persistence)
**Phase IV**: Local Kubernetes Deployment (Containerization, Minikube, AI-assisted DevOps)
**Phase V**: Advanced Cloud Deployment (Event-driven with Kafka, Dapr, production Kubernetes)

**Rules**:
- No phase may begin until the previous phase is complete and validated
- Each phase must be independently deployable and demonstrable
- Regression testing from previous phases is mandatory before advancing

**Rationale**: Incremental complexity prevents overwhelming architectural decisions and allows for course correction at each milestone. Each phase delivers value while building toward the complete system.

### V. No Manual Coding Mandate

**STRICT PROHIBITION**: Manual code writing is prohibited.

**Process**:
- All code MUST be generated by Claude Code based on refined Specs and Plans
- If generated code is incorrect, the user MUST refine the **Spec** until the generated code is correct
- Agents MUST NOT "fix" code directly; instead, they identify specification gaps

**Rationale**: This enforces specification quality and completeness. If specifications are clear enough for AI code generation, they are clear enough for human understanding and maintenance. It also serves as a validation mechanism for specification clarity.

### VI. Strict Workflow Adherence (Agentic Dev Stack)

**Required Sequence**:
1. **Constitution (WHY)**: Define principles and non-negotiables
2. **Specify (WHAT)**: Define requirements, user journeys, acceptance criteria
3. **Plan (HOW)**: Define architecture, schema, components, service boundaries
4. **Tasks (BREAKDOWN)**: Atomic, testable units with unique IDs
5. **Implement (CODE)**: Execution based only on authorized tasks

**Enforcement**:
- Agents MUST create Prompt History Records (PHRs) for each major interaction
- Architectural Decision Records (ADRs) MUST be suggested for significant decisions
- All workflow artifacts are stored in Git

**Rationale**: This workflow ensures that decisions are documented, traceable, and reviewable. It prevents "black box" development and enables knowledge transfer and audit trails.

### VII. Statelessness & Database Persistence

**Requirement**: Chat APIs and MCP tools MUST remain stateless.

**Rules**:
- All state (conversations, tasks, user sessions) MUST persist in the database
- JWT tokens for authentication (stateless, no server-side sessions)
- Services must be horizontally scalable without shared in-memory state

**Rationale**: Statelessness enables cloud-native scalability, simplifies deployment to Kubernetes, and aligns with distributed system best practices required in later phases.

## Technology Stack

### Core Technologies (NON-NEGOTIABLE)

**Package Management**: UV

**Frontend Stack**:
- Next.js 14+ (App Router)
- TypeScript
- Tailwind CSS
- OpenAI ChatKit

**Backend Stack**:
- Python 3.13+
- FastAPI
- SQLModel (ORM)

**Database**: Neon Serverless PostgreSQL

**Authentication**: Better Auth with JWT Tokens (Stateless)

**AI Frameworks**:
- OpenAI Agents SDK
- Official MCP (Model Context Protocol) SDK

**Infrastructure (Phase IV+)**:
- Docker
- Kubernetes (Minikube for local, DOKS/AKS/GKE for production)
- Helm Charts

**Distributed Systems (Phase V)**:
- Kafka (Redpanda or Confluent)
- Dapr (Distributed Application Runtime)

**AIOps Tools (Phase IV+)**:
- kubectl-ai
- kagent
- Docker AI Agent (Gordon)

**Justification for Stack Changes**:
Any deviation from this stack requires:
1. Documented technical justification
2. ADR (Architectural Decision Record) creation
3. Constitutional amendment approval
4. Migration plan with rollback strategy

## Development Workflow

### Agentic Development Process

All development follows this mandatory sequence:

1. **Constitution (WHY)**:
   - Establish project principles and constraints
   - Define success criteria and non-negotiables
   - Document governance and amendment process

2. **Specify (WHAT)**:
   - Define user stories with priorities (P1, P2, P3...)
   - Write acceptance criteria in Given/When/Then format
   - Identify functional requirements with FR-XXX IDs
   - Define edge cases and error scenarios

3. **Plan (HOW)**:
   - Conduct technical research (Phase 0)
   - Design data models and schemas (Phase 1)
   - Define API contracts and interfaces
   - Create architecture diagrams and component breakdown
   - Write quickstart guides for implementation

4. **Tasks (BREAKDOWN)**:
   - Convert plan into atomic, testable tasks with unique IDs
   - Mark parallelizable tasks with [P] flag
   - Link each task to user story (e.g., [US1], [US2])
   - Define dependencies and execution order
   - Include file paths in task descriptions

5. **Implement (CODE)**:
   - Generate code only for approved tasks
   - Link code files to Task IDs in comments
   - Run tests for each task completion
   - Commit with task ID references
   - Create PHRs for implementation sessions

### Prompt History Records (PHRs)

**Requirement**: Create PHR after every significant user interaction.

**When to Create PHRs**:
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Routing** (all under `history/prompts/`):
- Constitution updates → `history/prompts/constitution/`
- Feature-specific work → `history/prompts/<feature-name>/`
- General development → `history/prompts/general/`

**Format**: Follow `.specify/templates/phr-template.prompt.md`

### Architecture Decision Records (ADRs)

**Trigger**: When significant architectural decisions are made during `/sp.plan` or `/sp.tasks`, test for ADR significance:
- **Impact**: Long-term consequences? (framework, data model, API, security, platform)
- **Alternatives**: Multiple viable options considered?
- **Scope**: Cross-cutting and influences system design?

**If ALL true**, suggest:
> 📋 Architectural decision detected: [brief-description]
> Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`

**Process**:
- Wait for user consent; never auto-create ADRs
- Group related decisions (stacks, authentication, deployment) when appropriate
- Store in `history/adr/` with sequential numbering

## Coding Standards

### Documentation Requirements

**Every code file MUST contain**:
- Comment at top linking to specific Task ID (e.g., `# Task: T042 - Implement user authentication service`)
- Reference to Spec section (e.g., `# Spec: specs/002-auth/spec.md#FR-005`)
- Brief description of file purpose
- API contract documentation for public interfaces

### Code Quality

**Python Projects**:
- Follow PEP 8 style guidelines
- Type hints required for all function signatures
- Docstrings for all public functions/classes
- Proper project structure: `src/`, `tests/`, separation of concerns

**Next.js Projects**:
- Server Components by default (use 'use client' only when necessary)
- TypeScript strict mode enabled
- ESLint and Prettier configured and enforced
- Component structure: `src/components/`, `src/app/`, `src/lib/`

**Test Coverage**:
- Target: 90% code coverage
- Contract tests for all API boundaries
- Integration tests for user journeys
- Unit tests for business logic
- Tests written BEFORE implementation (TDD where feasible)

### Clean Code Principles

- **Smallest viable diff**: Prefer minimal changes over refactoring unrelated code
- **Explicit error paths**: Document and handle all error scenarios
- **No secrets in code**: Use environment variables and `.env` files
- **Cite existing code**: Use code references (file:line) when proposing changes
- **Testable acceptance criteria**: Every requirement must be independently verifiable

## Project Scope

### Phase I: In-Memory Console App

**Deliverables**:
- Basic CRUD operations: Add, Delete, Update, View, Mark Complete
- In-memory data structure (no persistence)
- Command-line interface
- Unit tests for all operations

**Success Criteria**:
- All CRUD operations functional
- Commands execute within <100ms
- Test coverage ≥ 90%

### Phase II: Full-Stack Web App

**Deliverables**:
- Persistent storage using Neon PostgreSQL
- RESTful API endpoints (FastAPI backend)
- Web UI (Next.js frontend)
- User Authentication (Better Auth with JWT)
- Database migrations

**Success Criteria**:
- Data persists across server restarts
- Authenticated users can manage their own todos
- API responds within <200ms p95
- Frontend deployed to Vercel

### Phase III: AI-Powered Chatbot

**Deliverables**:
- Conversational interface for natural language task management
- MCP server integration for task operations
- Conversation history persistence
- OpenAI Agents SDK integration
- Multi-turn dialogue support

**Success Criteria**:
- Users can create, update, delete todos via natural language
- Context maintained across conversation turns
- Chatbot understands intent with >90% accuracy
- Conversation history stored in database

### Phase IV: Local Kubernetes Deployment

**Deliverables**:
- Dockerfiles for all services
- Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets)
- Helm charts for application deployment
- Minikube local cluster setup
- AI-assisted DevOps integration (kubectl-ai, kagent)

**Success Criteria**:
- Application runs in local Kubernetes cluster
- Services communicate via Kubernetes DNS
- Deployment automated via Helm
- Logs and metrics accessible via kubectl

### Phase V: Advanced Cloud Deployment

**Deliverables**:
- Event-driven architecture using Kafka (Redpanda/Confluent)
- Dapr integration for distributed runtime (Pub/Sub, State, Secrets)
- Production Kubernetes deployment (DOKS/AKS/GKE)
- Horizontal pod autoscaling
- Production monitoring and alerting

**Success Criteria**:
- Events processed via Kafka topics
- Dapr handles service-to-service communication
- Application scales automatically under load
- Uptime ≥ 99.9%
- Production deployment accessible via public URL

## Agent Behavior Rules

### Mandatory Agent Actions

**Stop and Request**:
- If an agent cannot find a required spec, it MUST stop and request it
- If a requirement is ambiguous, agent MUST ask for clarification
- If multiple valid approaches exist, agent MUST present options to user

**Hierarchy of Authority**:
In case of conflict, follow this precedence:
1. **Constitution** (this document)
2. **Specify** (`specs/<feature>/spec.md`)
3. **Plan** (`specs/<feature>/plan.md`)
4. **Tasks** (`specs/<feature>/tasks.md`)

### Prohibited Actions

Agents MUST NOT:
- Engage in "freestyle" coding or architecture without specification
- Alter the technology stack without documented justification and ADR
- Invent features or flows not defined in specifications
- Produce "creative" implementations that violate the plan
- Skip phases or workflow steps
- Commit code without linking to Task IDs
- Generate code for unapproved tasks

### Required Behaviors

Agents MUST:
- Create PHRs for all significant interactions
- Suggest ADRs when architecturally significant decisions are detected
- Link all code to Task IDs and Spec sections
- Request clarification rather than making assumptions
- Follow the specified development workflow strictly
- Stop work if specifications are incomplete
- Validate against constitution principles before proceeding

## Submission & Evaluation Requirements

### Repository Requirements

**Public GitHub Repository** containing:
- All source code
- Complete `/specs` history with all phases documented
- `.specify/memory/constitution.md` (this file)
- PHR history in `history/prompts/`
- ADR history in `history/adr/`
- Git commit history showing incremental development

### Documentation Requirements

**Each phase requires**:
- `README.md` with setup instructions, architecture overview, and usage examples
- `CLAUDE.md` with agent-specific instructions and development guidelines
- API documentation (OpenAPI/Swagger for REST endpoints)
- Database schema documentation
- Deployment instructions

### Demonstration Requirements

**For evaluation, provide**:
1. **Deployment Links**:
   - Frontend: Vercel deployment URL
   - Backend: DOKS/AKS/GKE production URL (Phase V)
   - API documentation: Swagger UI URL

2. **Demo Video** (< 90 seconds):
   - Show user journey from console app to AI chatbot
   - Demonstrate key features in each phase
   - Show Kubernetes deployment (Phase IV+)
   - Highlight AI-powered task management (Phase III+)

3. **Test Results**:
   - Test coverage reports
   - Integration test results
   - Performance benchmarks for each phase

## Governance

### Amendment Process

**Constitutional amendments require**:
1. Documented technical justification
2. Impact analysis on existing specifications and code
3. User approval
4. Version increment following semantic versioning
5. Sync impact report documenting affected artifacts
6. Migration plan with rollback strategy

**Version Increment Rules**:
- **MAJOR**: Backward incompatible governance/principle removals or redefinitions
- **MINOR**: New principle/section added or materially expanded guidance
- **PATCH**: Clarifications, wording, typo fixes, non-semantic refinements

### Compliance Review

**All PRs/reviews MUST verify**:
- Code links to approved Task IDs
- Tasks link to Specifications
- No violations of core principles
- Technology stack adherence
- Test coverage meets standards
- Documentation is complete

**Complexity Justification**:
Any complexity exceeding simple CRUD operations MUST be justified in the plan with:
- Why the complexity is needed
- What simpler alternative was rejected and why
- Risk assessment and mitigation strategy

### Runtime Development Guidance

For agent-specific runtime guidance, see:
- `CLAUDE.md` in project root (agent instructions)
- `.specify/templates/commands/*.md` (command-specific workflows)

---

**Version**: 1.0.0 | **Ratified**: 2026-01-01 | **Last Amended**: 2026-01-01
