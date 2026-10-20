# E-Commerce POC Build Log

This log tracks the dual-stack build (Java 25 / Spring Boot 4.x and Python 3.15 / FastAPI).
It follows the step numbers in the build guide (`ecommerce_poc_dual_stack_build_guide.docx`).
Each step is explained and approved before it runs.

**Status key:** ✅ Done · ▶️ Next · ⏳ Pending · ⏭️ Skipped

## Progress

| Step | Description | Status | Date |
|---|---|---|---|
| 0.1 | Verify toolchains (JDK, Maven, Python, uv, Git, Docker) | ✅ Done | 2026-10-20 |
| 0.1a | Add `.gitignore` for both stacks | ✅ Done | 2026-10-20 |
| 0.2 | Start shared PostgreSQL with Docker Compose | ▶️ Next | |
| 0.3 | Code quality tools (Spotless, ruff, mypy, pre-commit) | ⏳ Pending | |
| 1.1 | Create both projects with domain packages | ⏳ Pending | |
| 1.2 | Load configuration from environment | ⏳ Pending | |
| 1.3 | Health check endpoint | ⏳ Pending | |
| 1.4 | First automated test | ⏳ Pending | |
| 2.1 | Product model | ⏳ Pending | |
| 2.2 | In-memory repository | ⏳ Pending | |
| 2.3 | Product service | ⏳ Pending | |
| 2.4 | Product CRUD endpoints | ⏳ Pending | |
| 2.5 | Service unit tests | ⏳ Pending | |
| 3.1 | Connect to PostgreSQL | ⏳ Pending | |
| 3.2 | Schema migrations (Flyway / Alembic) | ⏳ Pending | |
| 3.3 | Entities and relationships | ⏳ Pending | |
| 3.4 | Swap to database repository | ⏳ Pending | |
| 3.5 | Seed sample data | ⏳ Pending | |
| 3.6 | Repository tests with Testcontainers | ⏳ Pending | |
| 4.1 | Request/response models (DTOs) | ⏳ Pending | |
| 4.2 | Input validation | ⏳ Pending | |
| 4.3 | Uniform error format | ⏳ Pending | |
| 4.4 | Central error handling | ⏳ Pending | |
| 5.1 | Pagination | ⏳ Pending | |
| 5.2 | Sorting | ⏳ Pending | |
| 5.3 | Filtering | ⏳ Pending | |
| 5.4 | Categories and product status | ⏳ Pending | |
| 5.5 | API documentation | ⏳ Pending | |
| 6.1 | Users with hashed passwords | ⏳ Pending | |
| 6.2 | Register | ⏳ Pending | |
| 6.3 | Login and JWT | ⏳ Pending | |
| 6.4 | Authenticate each request | ⏳ Pending | |
| 6.5 | Current user endpoint | ⏳ Pending | |
| 6.6 | First admin account | ⏳ Pending | |
| 7.1 | Role-based restrictions | ⏳ Pending | |
| 7.2 | Ownership-scoped queries | ⏳ Pending | |
| 7.3 | Admin read access | ⏳ Pending | |
| 7.4 | Access matrix tests | ⏳ Pending | |
| 8.1 | Address model | ⏳ Pending | |
| 8.2 | Address CRUD | ⏳ Pending | |
| 8.3 | Default address | ⏳ Pending | |
| 9.1 | Cart model | ⏳ Pending | |
| 9.2 | Add / change / remove items | ⏳ Pending | |
| 9.3 | Totals and price-change flag | ⏳ Pending | |
| 10.1 | Inventory model (on hand / reserved) | ⏳ Pending | |
| 10.2 | Read stock | ⏳ Pending | |
| 10.3 | Stock adjustments with reason | ⏳ Pending | |
| 11.1 | Order, order line, stock hold models | ⏳ Pending | |
| 11.2 | Safe stock reservation | ⏳ Pending | |
| 11.3 | Price / address snapshots and totals | ⏳ Pending | |
| 11.4 | Idempotent checkout | ⏳ Pending | |
| 12.1 | Payment gateway interface | ⏳ Pending | |
| 12.2 | Controllable mock gateway | ⏳ Pending | |
| 12.3 | Pay for an order | ⏳ Pending | |
| 13.1 | Order state machine | ⏳ Pending | |
| 13.2 | Status history | ⏳ Pending | |
| 13.3 | Admin status updates | ⏳ Pending | |
| 13.4 | Order cancellation | ⏳ Pending | |
| 14.1 | Hold expiry job | ⏳ Pending | |
| 14.2 | Cleanup jobs | ⏳ Pending | |
| 14.3 | Notifications after commit | ⏳ Pending | |
| 15.1 | End-to-end journey test | ⏳ Pending | |
| 15.2 | Concurrency (no overselling) test | ⏳ Pending | |
| 15.3 | Critical rule tests | ⏳ Pending | |
| 15.4 | CI pipeline | ⏳ Pending | |
| 16.1 | Container images | ⏳ Pending | |
| 16.2 | Docker Compose for everything | ⏳ Pending | |
| 16.3 | Liveness / readiness | ⏳ Pending | |
| 16.4 | Metrics | ⏳ Pending | |
| 16.5 | Logging and tracing | ⏳ Pending | |
| 17.1 | Split into services | ⏳ Pending | |
| 17.2 | API gateway | ⏳ Pending | |
| 17.3 | Synchronous service calls | ⏳ Pending | |
| 17.4 | Events with outbox | ⏳ Pending | |
| 17.5 | Saga for checkout | ⏳ Pending | |

## Execution Notes

Each executed step gets an entry here: what changed, the commands run, the result, and anything learned.

### Step 0.1: Verify toolchains (2026-10-20)

**Goal:** Confirm that every tool both apps need is installed and on the PATH.

**Commands run:** `java -version`, `mvn -v`, `python --version`, `uv --version`, `git --version`, `docker --version`

| Tool | Needed for | Result |
|---|---|---|
| Java (JDK) | Compiling and running the Spring Boot app | ✅ 25.0.4.1 LTS (Oracle) |
| Maven | Java build and dependency management | ✅ 3.10.0, using JDK 25 |
| Python | Running the FastAPI app | ✅ 3.15.0 |
| uv | Python dependencies and virtual environments | ❌ Not installed (pip 3.15 is available) |
| Git | Version control | ✅ 2.56.0 |
| Docker | PostgreSQL (Step 0.2) and containers (Stage 16) | ❌ Not installed |

**Outcome:** Java and Python toolchains are ready. **Blocking:** install `uv` before Step 1.1 (Python), and Docker before Step 0.2.

**Learned:** Maven runs on whichever JDK `JAVA_HOME` / `PATH` points to. `mvn -v` shows which one, and here it correctly uses JDK 25.

**Follow-up (2026-10-20):** The user installed the missing tools, initialized Git and pushed to GitHub.

| Tool | Result |
|---|---|
| uv | ✅ 0.13.3 |
| Docker | ✅ Engine 29.9.1, Compose v5.6.0 (per-user install under `%LOCALAPPDATA%\Programs\DockerDesktop`) |
| Git repo | ✅ Branch `main` tracking `origin` = `git@github.com:slothnerds/ECOMM.git`, 1 commit |

**Learned:** A program installed while a terminal is open isn't on that terminal's PATH. Windows only reads PATH when a process starts, so open a new terminal after installing tools.

**Step 0.1 status:** ✅ Done.

### Step 0.1a: Add `.gitignore` (2026-10-20)

**Goal:** Keep build output, virtual environments, caches and secrets out of Git from the very first code commit.

**Files changed:** `.gitignore` (new).

**What it ignores:**
- **Java/Maven:** `target/`, `*.class`, `*.jar` (except the Maven wrapper jar), JVM crash logs.
- **Python:** `.venv/`, `__pycache__/`, `*.pyc`, pytest/mypy/ruff caches, coverage output, packaging folders.
- **Secrets:** `.env` and `.env.*`, but `.env.example` stays tracked (`!` re-includes a file).
- **IDE/OS:** `.idea/`, `.vscode/`, `Thumbs.db`, `.DS_Store`.
- **Word:** `~$*.docx` lock files and `*-old.docx` backups.

**Result:** `git status` shows `?? .gitignore` (new, untracked) and `M BUILD_LOG.md`. Nothing that should be tracked is ignored. Not committed yet.

**Learned:** A `!pattern` line un-ignores something an earlier line matched. Order matters, because the last matching line wins. `.gitignore` only affects untracked files; a file that is already committed must be removed with `git rm --cached` before ignoring takes effect.
