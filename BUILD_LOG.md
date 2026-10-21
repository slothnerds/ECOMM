# E-Commerce POC Build Log

This log tracks the dual-stack build (Java 25 / Spring Boot 4.x and Python 3.15 / FastAPI).
It follows the step numbers in the build guide (`ecommerce_poc_dual_stack_build_guide.docx`).
Each step is explained and approved before it runs.

> **Folder names:** since 2026-10-21 the apps live in `ecomm-java-app/` and `ecomm-py-app/` (Step 4.1b). Entries before that say `java-app/` and `python-app/`.

**Status key:** ✅ Done · ▶️ Next · ⏳ Pending · ⏭️ Skipped

## Progress

| Step | Description | Status | Date |
|---|---|---|---|
| 0.1 | Verify toolchains (JDK, Maven, Python, uv, Git, Docker) | ✅ Done | 2026-10-20 |
| 0.1a | Add `.gitignore` for both stacks | ✅ Done | 2026-10-20 |
| 0.2 | Start shared PostgreSQL with Docker Compose | ✅ Done (postgres:18) | 2026-10-20 |
| 0.2b | Single shared DB `ecomm_db` + pgAdmin web portal | ✅ Done | 2026-10-20 |
| 1.1 | Create both projects with domain packages (done before 0.3) | ✅ Done | 2026-10-20 |
| 1.1b | Upgrade FastAPI 0.153.0 → 0.154.0 | ✅ Done | 2026-10-20 |
| 0.3 | Code quality tools (Spotless, ruff, mypy, pre-commit) | ✅ Done (after 1.1) | 2026-10-20 |
| 1.2 | Load configuration from environment | ✅ Done | 2026-10-20 |
| 1.3 | Health check endpoint (`/health` in both apps) | ✅ Done | 2026-10-20 |
| 1.4 | First automated tests | ✅ Done (6 Java + 6 Python) | 2026-10-20 |
| 2.1 | Product model | ✅ Done | 2026-10-20 |
| 2.2 | In-memory repository | ✅ Done | 2026-10-20 |
| 2.3 | Product service | ✅ Done | 2026-10-20 |
| 2.4 | Product CRUD endpoints | ✅ Done | 2026-10-20 |
| 2.5 | Coverage reports + 80% gate (service tests were done in 2.3) | ✅ Done | 2026-10-20 |
| 2.6 | Config moved into each app; root `.env` removed | ✅ Done | 2026-10-20 |
| 2.7 | Postman collection (v3 YAML) + `java-dev` / `python-dev` environments | ✅ Done (redone in v3) | 2026-10-20 |
| 2.8 | Database profiles `local` (installed Postgres, 5433) and `docker` (5432) | ✅ Done (setup SQL to be run by user) | 2026-10-20 |
| 2.9 | `db-scripts/`: schema `ecomm` + DDL for all 14 tables | ✅ Done, merged into one file in 2.10 | 2026-10-20 |
| 2.10 | Single setup file `db-scripts/ecomm-setup.sql` | ✅ Done | 2026-10-20 |
| 2.11 | No app login: everything uses `postgres`/`password`; schema created on local Postgres | ✅ Done | 2026-10-20 |
| 2.12 | pgAdmin removed from Docker (a local pgAdmin is used instead) | ✅ Done | 2026-10-21 |
| 2.13 | `db/` folder (compose + scripts) and day-1 sample data (DML) for all 14 tables | ✅ Done (local and Docker) | 2026-10-21 |
| 3.1 | Connect to PostgreSQL (both apps, both profiles) | ✅ Done | 2026-10-21 |
| 3.2 | Schema migrations (Flyway / Alembic) | ▶️ Next (schema currently owned by `db/scripts/ecomm-setup.sql`) | |
| 3.3 | Entities and relationships (Product mapped; others later) | ✅ Done for products | 2026-10-21 |
| 3.4 | Swap to database repository | ✅ Done | 2026-10-21 |
| 3.5 | Seed sample data | ⏳ Pending | |
| 3.6 | Repository tests with Testcontainers | ✅ Done for products | 2026-10-21 |
| 4.1 | Request/response models (DTOs), entity kept internal | ✅ Done for products | 2026-10-21 |
| 4.1a | Same JSON formats in both apps: price as 2-decimal string, UTC timestamps with Z | ✅ Done | 2026-10-21 |
| 4.1b | Folders renamed: `java-app` → `ecomm-java-app`, `python-app` → `ecomm-py-app` | ✅ Done | 2026-10-21 |
| 4.2 | Input validation | ⏳ Pending | |
| 4.3 | Uniform error format | ⏳ Pending | |
| 4.4 | Central error handling | ⏳ Pending | |
| 5.1 | Pagination | ⏳ Pending | |
| 5.2 | Sorting | ⏳ Pending | |
| 5.3 | Filtering | ⏳ Pending | |
| 5.4 | Categories and product status | ⏳ Pending (status + soft delete done early in 3.3) | |
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

**Later change (by user):** The Secrets and Word sections were removed on purpose. `.env` is therefore **not ignored** and shows in `git status`. Don't stage it (avoid `git add .`).

### Step 0.2: Shared PostgreSQL with Docker Compose (2026-10-20)

**Goal:** One local PostgreSQL server for both apps, with a separate database and login per app.

**Decision:** `postgres:18` instead of the guide's `postgres:16` (user's choice). The running server is PostgreSQL 18.6.

**Files changed:**

| File | Purpose | Commit? |
|---|---|---|
| `.env.example` | Template listing the variables, with `change-me` placeholders | Yes |
| `.env` | Real local passwords (randomly generated with Python `secrets`) | **No**: not ignored, see note above |
| `docker/postgres/init/01-create-databases.sh` | Creates users `ecomm_java` and `ecomm_py`, each owning its database; revokes CONNECT from PUBLIC | Yes |
| `docker-compose.yml` | `postgres:18` service, port 5432, named volume `pgdata`, `pg_isready` health check, init folder mounted read-only | Yes |
| `.gitattributes` | Keeps `*.sh` files with LF line endings, so the script still runs in Linux after a Windows checkout | Yes |

**Commands run:**
- `docker compose config --quiet` validates the file and the `.env` substitution.
- `docker compose up -d postgres` pulls the image and starts the container in the background.
- `docker exec ecomm-postgres psql -U postgres -c "\l ecomm_*"` lists the databases.
- `psql` as each app user, to test access.

**Result:**
- Container `ecomm-postgres` is **healthy** on `localhost:5432`.
- The init script ran once: 2 × `CREATE ROLE`, 2 × `CREATE DATABASE`.
- `ecomm_java` is owned by `ecomm_java`, and `ecomm_py` by `ecomm_py`.
- `ecomm_java` → `ecomm_java`: ✅ connects. `ecomm_java` → `ecomm_py`: ❌ "User does not have CONNECT privilege" (as intended). `ecomm_py` → `ecomm_py`: ✅ connects.
- Not committed yet.

**Learned:**
- Scripts in `/docker-entrypoint-initdb.d` run **only when the data volume is empty**. To re-run them: `docker compose down -v` (this deletes all data).
- PostgreSQL 18 images store data in `/var/lib/postgresql/18/docker`, so the volume mounts at `/var/lib/postgresql` (older images used `/var/lib/postgresql/data`).
- `$${POSTGRES_USER}` in compose escapes `$`: the variable is expanded inside the container at health-check time, not by Compose.
- `REVOKE CONNECT ... FROM PUBLIC` matters because by default **every** role can connect to every database. Owning a database doesn't make it private.
- Useful commands: `docker compose ps`, `docker compose logs -f postgres`, `docker compose stop` / `start`, and `docker exec -it ecomm-postgres psql -U postgres` for a SQL shell.

### Step 1.1: Create both projects with domain packages (2026-10-20)

**Goal:** Two empty but runnable apps with the same structure, one package per business domain.

**Decision:** Done before Step 0.3, because the code quality tools are configured inside `pom.xml` / `pyproject.toml`, which this step creates.

#### Java: `java-app/`

- **Generated with:** start.spring.io (`curl .../starter.zip`), Spring Boot **4.1.1** (current stable), Java 25, Maven, group `com.example`, artifact `ecommerce`.
- **Dependencies:** `spring-boot-starter-webmvc`, `-validation`, `-actuator`, `spring-boot-devtools`, `lombok`, plus a matching `*-test` starter for each.
- **Added:** `package-info.java` in each of `core, auth, product, cart, order, inventory, payment` under `com.example.ecommerce`.
- **Key files:** `pom.xml`, `mvnw`/`mvnw.cmd` (Maven wrapper), `EcommerceApplication.java` (`@SpringBootApplication` + `main()`), `application.properties`, `EcommerceApplicationTests.java` (a generated context-load test).
- **Verified:** `./mvnw package -DskipTests`, then `java -jar target/ecommerce-0.0.1-SNAPSHOT.jar`. It started in 1.99 s on Tomcat port 8080, using Java 25.0.4.1. `GET /` → 404 (no endpoints yet). `GET /actuator/health` → `{"status":"UP"}`, since Actuator gives a health check for free.

#### Python: `python-app/`

- **Created with:** `uv init --package --name ecommerce --python 3.15 python-app`, which gives the src layout: code in `src/ecommerce/`.
- **Dependencies:** `fastapi 0.153`, `uvicorn 0.54` (plain, see the issue below), `pydantic-settings 2.16`. Dev group: `pytest 9.1`, `httpx 0.28`, `ruff 0.17`, `mypy 2.4`.
- **Added:** `main.py` with `app = FastAPI(...)` and a `run()` function (wired as the `ecommerce` script in `pyproject.toml`). `__init__.py` with a docstring in each of the same 7 domain packages.
- **Key files:** `pyproject.toml` (project + dependencies), `uv.lock` (exact pinned versions), `.python-version` (`3.15`), `.venv/` (ignored).
- **Verified:** `uv run uvicorn ecommerce.main:app --port 8000` started. `GET /` → 404. `GET /docs` → 200 (Swagger UI comes for free). `/openapi.json` shows title "E-Commerce POC" and no paths yet.

#### Issue found and how it was solved

- `uv add "uvicorn[standard]"` failed: its extra **PyYAML 6.0.3 has no prebuilt Windows wheel for Python 3.15** yet, and compiling it needs the Microsoft C++ Build Tools. The whole `uv add` was rolled back, so FastAPI wasn't installed either.
- **Decision (user):** use plain `uvicorn` and stay on Python 3.15. `--reload` still works through uvicorn's built-in polling reloader. `[standard]` (httptools, watchfiles, websockets, pyyaml) can be added once 3.15 wheels exist.

#### Spring Boot vs FastAPI: what this step shows

| Concept | Spring Boot | FastAPI |
|---|---|---|
| Project generator | start.spring.io | `uv init` |
| Build/dependency file | `pom.xml` | `pyproject.toml` |
| Exact versions locked by | Spring Boot parent BOM (manages versions centrally) | `uv.lock` (records every resolved version) |
| Build tool without a global install | Maven wrapper `mvnw` | uv manages the venv and the Python version |
| A folder is a package because | it matches the `package` declaration in the `.java` files | it contains `__init__.py` |
| App object | `SpringApplication.run(...)` in `main()` | `app = FastAPI()`, served by uvicorn (an ASGI server) |
| Server | Embedded Tomcat, inside the jar | uvicorn, a separate process that imports `app` |
| Free endpoints | `/actuator/health` (Actuator) | `/docs`, `/openapi.json` |

**Learned:**
- Spring Boot 4 splits starters into modules: `spring-boot-starter-webmvc` replaces the old `-web`, and each starter has its own `-test` companion.
- The Lombok `sun.misc.Unsafe` warning during the Java build is harmless on Java 25 (Lombok still uses an internal JDK API).
- A brand-new Python release often lacks prebuilt wheels for C-extension packages. Pure-Python packages work immediately.
- uv's "failed to hardlink" warning appears because the uv cache (C:) and the project (D:) are on different drives. Set `UV_LINK_MODE=copy` as a user environment variable to silence it.

**Not committed yet.**

### Step 1.1b: Upgrade FastAPI 0.153.0 → 0.154.0 (2026-10-20)

**Why:** FastAPI 0.154.0 was released the same day, shortly after the project was created. `uv.lock` had pinned 0.153.0.

**Commands:** `uv lock --upgrade-package fastapi` (re-resolves only FastAPI in the lock), then `uv sync` (installs it into `.venv`).

**Result:** `fastapi 0.154.0` installed. All other packages were already the latest. `pyproject.toml` still says `>=0.153.0`; the lock is what pins the exact version.

**Learned:** A lock file never upgrades on its own, which is what makes installs reproducible. FastAPI is still 0.x, so minor versions can contain small breaking changes; check the release notes before upgrading.

### Step 0.3: Code quality tools (2026-10-20)

**Goal:** Automatic formatting and static checks in both apps, enforced by a Git pre-commit hook.

#### Java: `java-app/pom.xml`

- **Spotless Maven plugin 3.10.4** with `<googleJavaFormat/>` (Spotless's default, google-java-format **1.36.1**), `<removeUnusedImports/>` and `<importOrder/>`.
- **Compiler warnings:** `-Xlint:all,-processing` in `maven-compiler-plugin` (all warnings except Lombok's annotation-processing noise).
- `./mvnw spotless:apply` reformatted the generated code to Google style (2-space indent). One-line Javadocs were collapsed to `/** ... */`, and the long one was wrapped at 100 characters.
- **Result:** `spotless:check` ✅, `clean compile test-compile` with `-Xlint:all` → **0 warnings**.

#### Python: `python-app/pyproject.toml`

- `[tool.ruff]`: line length 100, target `py315`. Lint rules `E, W, F, I, UP, B, SIM, N`. FastAPI's `Depends`/`Query`/`Header`/`Path` are marked as safe default arguments for rule B008.
- `[tool.mypy]`: `strict = true` with the `pydantic.mypy` plugin.
- **Result:** ruff found **E501** (line too long) in my own `core/__init__.py` docstring, which I fixed by hand; `ruff format` doesn't wrap docstrings. Then `ruff check` ✅, `ruff format --check` ✅, `mypy src` ✅ (9 files).

#### Pre-commit hook (repo root)

- **Tool:** `pre-commit 4.7.0`, installed with `uv tool install pre-commit --python 3.14`, a global tool with its own Python 3.14. **Decision (user):** pre-commit depends on PyYAML, which has no 3.15 wheel yet (same issue as Step 1.1). The project itself stays on 3.15.
- **`.pre-commit-config.yaml`:** `ruff-check --fix` and `ruff-format` (from `astral-sh/ruff-pre-commit` v0.17.1) on `python-app/`, plus a local `spotless-check` hook running `./mvnw spotless:check` when `.java` files are staged.
- `pre-commit install` → `.git/hooks/pre-commit`. This is local to the clone; every new clone must run it once.
- **Proof:** with a badly formatted demo file in each app (deleted afterwards), the hooks **failed** as intended:
  - ruff auto-fixed 3 issues (unused imports, spacing) and blocked on **N802** (function name `Add` must be lowercase).
  - Spotless blocked and printed the correct formatting as a diff.
- On the real code: all 3 hooks ✅.

#### Issues found and how they were solved

| Issue | Cause | Fix |
|---|---|---|
| Spotless crashed with `InvocationTargetException` on every file | google-java-format **1.37.0** is newer than Spotless 3.10.4's integration (the formatter itself works on Java 25, shown by running its jar standalone) | Don't pin the formatter version; use Spotless's tested default, 1.36.1. A `.mvn/jvm.config` with `--add-exports` was tried, proved unnecessary, and was removed |
| `pre-commit run --all-files` skipped everything | `--all-files` only covers files **tracked** by Git, and the app folders aren't committed yet | Used `pre-commit run --files ...` for verification. After the first commit, `--all-files` will work |
| `uv tool install pre-commit` failed | PyYAML has no Python 3.15 wheel | Install the tool on Python 3.14 |

#### Spring Boot vs FastAPI: what this step shows

| | Java | Python |
|---|---|---|
| Formatter | Spotless + google-java-format (a Maven plugin) | `ruff format` |
| Linter | Mostly the compiler (`-Xlint`); Checkstyle/Error Prone optional | `ruff check` (800+ rules, some auto-fixable) |
| Type checking | Built into `javac`; a type error stops the build | Optional: **mypy** checks type hints, which Python ignores at runtime |
| Where configured | `<plugin>` blocks in `pom.xml` | `[tool.*]` tables in `pyproject.toml` |

**Daily commands:**
- Java: `./mvnw spotless:apply`
- Python: `uv run ruff check --fix . && uv run ruff format . && uv run mypy src`

**Learned:** Pin plugin and tool versions explicitly, because "latest" combinations can break. A Git hook is just a script in `.git/hooks`; it isn't pushed, so each developer installs it.

**Not committed yet.**

### Step 1.2: Load configuration from the environment (2026-10-20)

**Goal:** Both apps read typed, validated settings from config files and environment variables. Secrets never appear in code or logs. A bad configuration stops startup immediately (fail fast).

**Shared:** New variables in `.env.example` (placeholders) and `.env` (real values; a random 64-char JWT secret): `APP_ENV=dev`, `JWT_SECRET`, `HOLD_DURATION=PT15M` (ISO-8601 duration, which both apps parse).

#### Java

| File | Change |
|---|---|
| `application.properties` | **Deleted**, replaced by YAML |
| `src/main/resources/application.yml` | Base config. `spring.profiles.default: dev`, `spring.config.import: optional:file:../.env[.properties]` (Spring doesn't read `.env` natively), `server.port: ${SERVER_PORT:8080}`, Actuator exposure, `app.*` keys using `${ENV_VAR:default}` placeholders |
| `src/main/resources/application-dev.yml` | Dev profile: DEBUG logging for `com.example.ecommerce` |
| `src/test/resources/application-test.yml` | Test profile: fixed `app.*` values, so tests never depend on `.env` |
| `core/config/AppProperties.java` | `@ConfigurationProperties(prefix = "app") @Validated record` with `@Pattern` environment, `@Size(min = 32)` jwtSecret, `@NotNull Duration` holdDuration. `toString()` is overridden to mask the secret |
| `core/config/ConfigLogger.java` | `ApplicationRunner` (Lombok `@Slf4j`, `@RequiredArgsConstructor`) that logs the settings at startup |
| `EcommerceApplication.java` | `@ConfigurationPropertiesScan` registers `AppProperties` |
| `EcommerceApplicationTests.java` | `@ActiveProfiles("test")` |

#### Python

| File | Change |
|---|---|
| `src/ecommerce/core/config.py` | `class Settings(BaseSettings)`: `env_file=("../.env", ".env")`, `extra="ignore"`. Fields: `environment` (`Literal["dev","test","prod"]`, alias `APP_ENV`), `jwt_secret: SecretStr = Field(min_length=32)`, `hold_duration: timedelta`, `port`. Plus a cached `get_settings()` (`@lru_cache`) |
| `src/ecommerce/main.py` | Loads settings at import (fail fast), a `lifespan` context manager logs them at startup, `run()` uses `settings.port` |

#### Verification

- Java `mvn clean package`: 0 compiler warnings, test passes with the `test` profile. Python: ruff ✅, format ✅, mypy strict ✅.
- **Startup with `.env`:**
  - Java: `No active profile set, falling back to 1 default profile: "dev"` … `Configuration loaded: AppProperties[environment=dev, jwtSecret=**********, holdDuration=PT15M]`
  - Python: `Configuration loaded: Settings(app_name='E-Commerce POC', environment='dev', jwt_secret=SecretStr('**********'), hold_duration=datetime.timedelta(seconds=900), port=8000)`
- **Fail fast with `JWT_SECRET=too-short`** (an environment variable overrides `.env` in both apps): both exit with code 1.
  - Java: `APPLICATION FAILED TO START … Property: app.jwtSecret … Reason: must be at least 32 characters`
  - Python: `ValidationError: 1 validation error for Settings / jwt_secret / Value should have at least 32 items after validation, not 9`

#### Spring Boot vs FastAPI

| | Spring Boot | FastAPI / Pydantic |
|---|---|---|
| Typed settings | `@ConfigurationProperties` record | `BaseSettings` subclass |
| Validation | Bean Validation (`@Size`, `@NotNull`) + `@Validated` | Pydantic `Field(min_length=...)`, types |
| Reads `.env` | No; needs `spring.config.import` with `[.properties]` | Yes, `env_file=` |
| Name mapping | `JWT_SECRET` → `${JWT_SECRET}` placeholder → `app.jwt-secret` → `jwtSecret` (relaxed binding) | `JWT_SECRET` → `jwt_secret` (case-insensitive); `alias` for other names |
| Profiles | `application-{profile}.yml`, `SPRING_PROFILES_ACTIVE` | No built-in profiles; an `environment` field + different env files/overrides |
| Secret type | None built in; mask by overriding `toString()` | `SecretStr`; reading it needs `.get_secret_value()` |
| One shared instance | A Spring bean (singleton) | `@lru_cache` on `get_settings()` |
| Startup hook | `ApplicationRunner` | `lifespan` async context manager |
| Precedence | OS env > config files (incl. imported `.env`) | OS env > `.env` file > defaults |

**Learned:**
- mypy strict reported my `# type: ignore` as **unused**, because the Pydantic plugin already understands that `BaseSettings` fields come from the environment. Strict mode keeps workarounds from piling up.
- ⚠️ **Both frameworks print the rejected value in validation errors**, even for secrets (`Value: "too-short"`, `input_value='too-short'`). Before production, make sure startup errors don't end up in shared logs, or validate secrets without echoing them (Stage 16).
- `spring.config.import` paths are relative to the **working directory**, the same as Pydantic's `env_file`. Both apps must be started from their own folder (`java-app/`, `python-app/`) to find `../.env`.

**Not committed yet.**

### Step 0.2b: Single shared database + pgAdmin (2026-10-20)

**Change requested by the user:** One database for both apps instead of one per app, and a web admin portal for PostgreSQL.

**Decisions (user):**
- Database name `ecomm_db`, lowercase so no quoting is needed in SQL.
- **One login (`ecomm`) and one schema (`public`)** shared by both apps. This replaces the per-app logins and databases `ecomm_java`/`ecomm_py` from Step 0.2.

**Files changed:**

| File | Change |
|---|---|
| `.env.example` / `.env` | `JAVA_DB_PASSWORD`/`PY_DB_PASSWORD` removed. Added `DB_NAME=ecomm_db`, `DB_USER=ecomm`, `DB_PASSWORD`, `PGADMIN_EMAIL`, `PGADMIN_PASSWORD`. Existing Postgres password and JWT secret kept; new passwords random |
| `docker/postgres/init/01-create-databases.sh` | Creates user `${DB_USER}` and database `${DB_NAME}` owned by it, `REVOKE CONNECT ... FROM PUBLIC`, and **`ALTER SCHEMA public OWNER TO ecomm`** |
| `docker-compose.yml` | Postgres gets `DB_*` variables. **New `pgadmin` service:** `dpage/pgadmin4:9.18`, port **5050**, volume `pgadmin-data`, `depends_on: postgres (service_healthy)`, master password prompt disabled |
| `docker/pgadmin/servers.json` | **New.** Pre-registers server "ECOMM (local)" → host `postgres`, port 5432, database `ecomm_db`, user `ecomm` |

**Commands:** `docker compose down -v` (deleted the old, empty `pgdata` volume so the init script runs again), then `docker compose up -d`.

**Result:**
- Init log: `CREATE ROLE`, `CREATE DATABASE`, `REVOKE`, `GRANT`, `ALTER SCHEMA`.
- Databases: `postgres` (owner postgres) and `ecomm_db` (owner ecomm).
- `ecomm` can create and drop a table in `ecomm_db.public` ✅.
- pgAdmin: `/misc/ping` → 200, log says `Added 0 Server Group(s) and 1 Server(s)`, and it reaches `postgres:5432` over the Compose network ✅.

**How to use pgAdmin:** open http://localhost:5050 and log in with `PGADMIN_EMAIL` / `PGADMIN_PASSWORD` from `.env`. Expand **Servers → ECOMM (local)** and enter `DB_PASSWORD` from `.env` the first time; tick "Save password".

**Learned:**
- Containers in one Compose project share a network, where each **service name is a hostname**. pgAdmin connects to `postgres:5432`, while your host machine uses `localhost:5432`.
- Since **PostgreSQL 15**, ordinary users can't create tables in `public` unless they own it or are granted `CREATE`. That's why the script changes the schema owner.
- `servers.json` is only imported on pgAdmin's **first** start (it's stored in the `pgadmin-data` volume). Edits later need `docker compose down -v` or a manual import.

**⚠️ Impact on Stage 3:** Both apps now use the same tables. Only **one** migration tool should own the schema (for example Flyway in Java, with the Python app mapping to the same tables, and Alembic used only for checks), or the two will try to create `product` twice. We'll decide this at Step 3.2.

### Step 1.3: Health check endpoint (2026-10-20)

**Goal:** `GET /health` → `{"status": "UP"}` on the **same path in both apps** (user approved the change from the guide's `/actuator/health`).

#### Java: configuration only (`application.yml`)

- `management.endpoints.web.base-path: /` puts Actuator endpoints at the root: `/health`, `/info` (and `/actuator/*` is gone).
- `management.info.env.enabled: true` + `info.app.{name, description, version, java}` publishes app info on `/info`. `${java.version}` resolves to the running JVM.

#### Python: code

- **New `src/ecommerce/core/health.py`:** `router = APIRouter(tags=["health"])`, `class HealthResponse(BaseModel): status: Literal["UP"]`, and `@router.get("/health")` returning `HealthResponse`. The return type annotation doubles as the response model.
- **`main.py`:** `app.include_router(health.router)`.

#### Shared

- **New `http/health.http`:** requests for both apps' `/health`, Java `/info` and Python `/openapi.json`. Runs in IntelliJ or the VS Code REST Client.

#### Verification

| Request | Result |
|---|---|
| `GET :8080/health` | 200 `{"groups":["liveness","readiness"],"status":"UP"}` |
| `GET :8000/health` | 200 `{"status":"UP"}` |
| `GET :8080/info` | 200 `{"app":{"name":"ecommerce","description":"E-Commerce POC (Spring Boot)","version":"0.0.1-SNAPSHOT","java":"25.0.4.1"}}` |
| `GET :8080/actuator/health` | 404 (moved, as intended) |
| Python OpenAPI | path `/health`, schema `HealthResponse` with `status` `const: "UP"` |

Checks: ruff ✅, format ✅, mypy ✅ (11 files), Spotless ✅, Java build and test ✅.

#### Spring Boot vs FastAPI

| | Spring Boot | FastAPI |
|---|---|---|
| Where the endpoint comes from | Auto-configured by Actuator; we only moved it | Written by us: function + router |
| Splitting endpoints into modules | One `@RestController` class per area, found by component scanning | One `APIRouter` per module, registered explicitly with `include_router` |
| Response shape | Actuator's fixed JSON, with its own media type `application/vnd.spring-boot.actuator.v3+json` | Pydantic model; the shape appears in `/docs` |
| Liveness/readiness | Built-in groups (`/health/liveness`, `/health/readiness`) | Write them yourself (Stage 16) |

**Learned:**
- Spring Boot finds controllers automatically (component scanning), while FastAPI only serves the routers you include. That's more explicit, but forgetting `include_router` means a silent 404.
- PowerShell's `Invoke-WebRequest` showed Actuator's JSON as **bytes**, because it doesn't recognize the vendor media type as text. curl or the `.http` file show it normally.
- A Java process started with `Start-Process` kept running after a test and **locked the jar**, so `mvn clean` failed. On Windows, an open file can't be deleted. Always check for and stop leftover app processes.

**Not committed yet.**

### Step 1.4: First automated tests (2026-10-20)

**Goal:** Tests that start each app in-process and call `/health`, plus tests proving bad configuration is rejected.

#### Java: `./mvnw test`, 6 tests ✅

| Test class | What it does |
|---|---|
| `core/HealthEndpointTest` | `@SpringBootTest` + `@AutoConfigureMockMvc` + `@ActiveProfiles("test")`. MockMvc `GET /health` → 200, `jsonPath("$.status") == "UP"`; `GET /actuator/health` → 404 |
| `core/config/AppPropertiesTest` | `ApplicationContextRunner` with only `AppProperties` + `ValidationAutoConfiguration`. Valid values bind, the 15-minute `Duration` parses, and `toString()` masks the secret; a short secret makes the context fail with "must be at least 32 characters"; `environment=staging` fails |
| `EcommerceApplicationTests` (generated) | Context loads with the test profile (0.35 s: the Spring context was **reused from the cache**) |

#### Python: `uv run pytest`, 6 tests ✅

| File | What it does |
|---|---|
| `tests/conftest.py` | Sets `APP_ENV=test` and a test `JWT_SECRET` **before** importing `ecommerce.main` (settings load at import). Has the `client` fixture: `with TestClient(app)`, which also runs the lifespan |
| `tests/test_health.py` | `GET /health` → 200 `{"status": "UP"}`; `/health` is listed in `/openapi.json` |
| `tests/test_config.py` | `Settings.model_validate` parses `"PT15M"` → 15 min; the secret is masked in `repr`/`str` and readable via `get_secret_value()`; a short secret raises `ValidationError`; `APP_ENV=staging` (set with `monkeypatch.setenv`) is rejected |

`pyproject.toml`: `[tool.pytest.ini_options]` with `testpaths = ["tests"]` and `addopts = "-ra --strict-markers"`.

#### Changes made along the way

| What | Why |
|---|---|
| Dev dependency **`httpx` → `httpx2` 2.15.1** | Starlette 1.9 warned: *"Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead."* httpx2 is the Pydantic team's successor to httpx, and Starlette now tries it first |
| mypy now checks **`src tests`** | Tests are code too. It found 3 real type errors: `Settings(jwt_secret="...")` passes `str` where `SecretStr` is declared (`init_typed = true` from Step 0.3). Fixed by passing `SecretStr(...)` |

#### Spring Boot vs FastAPI

| | Spring Boot | FastAPI / pytest |
|---|---|---|
| Test framework | JUnit 5 (`@Test`), assertions with AssertJ (`assertThat`) | pytest: plain functions + plain `assert` |
| Shared setup | Annotations on each class (`@SpringBootTest`, `@ActiveProfiles`) | `conftest.py` + **fixtures** passed in as function arguments (`client`) |
| Calling the app without a real port | MockMvc | `TestClient` |
| Small, focused config test | `ApplicationContextRunner` (a mini Spring context) | Just instantiate `Settings(...)`; no framework needed |
| Overriding the environment | `@ActiveProfiles` / `withPropertyValues` | `os.environ` in conftest, `monkeypatch.setenv` per test (restored automatically) |
| Speed | ~4 s total (Spring context startup, then cached) | 0.04 s |
| Test discovery | Surefire runs `*Test`/`*Tests` classes | pytest collects `test_*.py` / `test_*` functions |

**Learned:**
- Boot 4 moved test classes into module packages: `org.springframework.boot.webmvc.test.autoconfigure.AutoConfigureMockMvc`, `org.springframework.boot.validation.autoconfigure.ValidationAutoConfiguration`.
- **Import-time side effects** in Python (settings loaded when `main.py` is imported) force tests to set the environment *before* importing, hence the `# noqa: E402` import in conftest. A factory function (`create_app()`) avoids this. Worth considering when the app grows.
- Spring's test context cache makes later `@SpringBootTest` classes nearly free, but only if they share the same configuration (profile, mocks). Different configs mean new contexts and slow tests.

**Daily commands updated:** `uv run mypy src tests`.

**Stage 1 complete.** Not committed yet.

### Step 2.1: Product model (2026-10-20)

**Goal:** The `Product` type every layer passes around: id, SKU, name, description, price (exact decimal, rule **SN-3**) and an active flag. Mutable on purpose, because it becomes a JPA entity / SQLAlchemy model in Stage 3.

| | Java: `product/model/Product.java` | Python: `product/models.py` |
|---|---|---|
| Type | Class with Lombok `@Getter @Setter @Builder @NoArgsConstructor @AllArgsConstructor @ToString` | `@dataclass(slots=True, eq=False)` |
| Money | `BigDecimal price` | `price: Decimal` |
| Id | `Long id` (null until saved) | `id: int \| None = None` |
| Default active | `@Builder.Default private boolean active = true` | `active: bool = True` |
| Equality | Hand-written `equals`/`hashCode` | Hand-written `__eq__`/`__hash__` |

**Design decision: entity equality (same in both apps)**
- `equals`: same object, **or** both ids set and identical. Two unsaved products are never equal.
- `hashCode`: **constant per class** (`Product.class.hashCode()` / `hash(Product)`), so the hash doesn't change when the id is assigned on save. Otherwise an object put in a `HashSet`/`set` before saving can't be found afterwards.
- **Why not Lombok `@EqualsAndHashCode(onlyExplicitlyIncluded = true)` on id?** It treats two unsaved products (`null == null`) as **equal**, so two new products in a `Set` would collapse into one. This is a classic JPA pitfall; I caught it before writing the tests and replaced it in both apps.

**Tests**

| Case | Java `ProductTest` | Python `tests/product/test_models.py` |
|---|---|---|
| Builder/constructor defaults (active, id null) | ✅ | ✅ |
| `0.1 + 0.2 != 0.3` with double/float, exact with BigDecimal/Decimal | ✅ | ✅ |
| `new BigDecimal(0.1)` / `Decimal(0.1)` carry the float error, so always build from a string | ✅ | ✅ |
| Same id → equal + same hash, even with a different price | ✅ | ✅ |
| Two unsaved products are not equal | ✅ | ✅ |
| Still found in a set after the id is assigned | ✅ | ✅ |
| `slots=True` rejects a typo'd attribute (`prise`) | n/a (Java can't add fields at runtime) | ✅ |

**Result:** Java **12 tests** ✅ (6 new), Python **13 tests** ✅ (7 new). ruff, format, mypy (16 files) and Spotless ✅.

**Learned:**
- **Lombok** generates code at compile time (getters, builder, constructors). It's convenient, but its defaults aren't always right for entities. Know what each annotation generates.
- `@Builder` ignores field initializers unless they're marked `@Builder.Default`.
- **dataclass** is Python's built-in alternative to Lombok: `slots=True` saves memory and blocks unknown attributes; `eq=False` lets us write our own equality.
- A `# type: ignore[...]` comment must be followed by a separate `# ...` comment for any explanation. mypy reported the deliberate typo `prise` statically ("maybe price?"), so the typo is caught twice: by mypy before running, and by `slots` at runtime.
- The constant hash makes hash-based collections of products fall back to `equals` comparisons. That's fine for the small sets an app holds; the database does the real lookups by id.

**Not committed yet.**

### Step 2.2: In-memory repository (2026-10-20)

**Goal:** A storage contract (interface) plus an in-memory implementation. In Stage 3 a PostgreSQL implementation of the **same contract** replaces it, without changes above it.

**Operations:** `save` (assigns the next id when the id is empty, otherwise replaces), `findById`, `findBySku`, `findAll` (ordered by id), `deleteById` (returns whether something was deleted).

| | Java | Python |
|---|---|---|
| Contract | `product/repository/ProductRepository.java`: `interface` | `product/repository.py`: `class ProductRepository(Protocol)` |
| Not found | `Optional<Product>` | `Product \| None` |
| Implementation | `InMemoryProductRepository implements ProductRepository`, annotated `@Repository` (a Spring bean) | `InMemoryProductRepository`, no base class; it fits the Protocol structurally |
| Storage | `ConcurrentHashMap<Long, Product>` + `AtomicLong` | `dict[int, Product]` + `itertools.count(1)` + `threading.Lock` |
| Copies | `product.toBuilder().build()` (added `@Builder(toBuilder = true)` to `Product`) | `dataclasses.replace(product)` |

**Design decision: copies in and out.** A real database always gives you a fresh object. A plain map hands out the stored object itself, so code changing a product without saving would silently change the "database". Storing and returning copies makes the fake behave like the real thing.

**Tests:** 7 identical cases in both apps:
- sequential ids
- find by id and SKU, plus not found
- saving with an existing id replaces
- `findAll` ordered by id
- delete (true, then false)
- returned objects are copies
- **100 parallel saves on 16 threads → 100 unique ids**

**Result:** Java **19 tests** ✅ (7 new), Python **20 tests** ✅ (7 new). ruff, format, mypy (18 files), Spotless ✅.

**Learned:**
- **Nominal vs structural typing:** Java needs `implements ProductRepository`. Python's `Protocol` matches any class with the right method signatures, and mypy checks that when the fixture returns `InMemoryProductRepository` as a `ProductRepository`.
- **Thread safety is needed in both:** Tomcat handles requests on many threads, and FastAPI runs `def` endpoints in a thread pool.
- **Honest note on the Python concurrency test:** with the GIL, `next()` on `itertools.count` is effectively atomic, so the test would likely pass **without** the lock. The lock is still right: it protects compound operations (e.g. "find by SKU, then save") and free-threaded Python (`3.15t`, no GIL). A passing concurrency test doesn't prove code is thread-safe.
- `Optional` (Java) and `X | None` (Python) both make "might be missing" part of the type. mypy forces an `is not None` check before using the value, which is why the tests contain `assert saved.id is not None`.
- `@BeforeEach` (JUnit) and a function-scoped `@pytest.fixture` both give each test a fresh repository, so tests can't affect each other.

**Not committed yet.**

### Step 2.3: Product service (2026-10-20)

**Goal:** The business-rule layer between the API and the repository.

**Rules implemented (same in both apps):**
- **Create:** the SKU must be unique, otherwise `DuplicateSkuException`/`DuplicateSkuError` (409 in Stage 4). Any id on the input is ignored.
- **Get:** a missing id gives `ProductNotFoundException`/`ProductNotFoundError` (404 in Stage 4).
- **List:** returns all products.
- **Update:** changes name, description, price and active. **The SKU never changes** (user decision: orders will reference it). Missing → not found.
- **Delete:** missing → not found.

| | Java | Python |
|---|---|---|
| Exceptions | `product/exception/ProductNotFoundException`, `DuplicateSkuException` (extend `RuntimeException`, carry the id/SKU) | `product/exceptions.py`: `ProductNotFoundError`, `DuplicateSkuError` (subclass `Exception`) |
| Update input | `product/model/ProductUpdate` record (no id, no SKU) | `ProductUpdate` frozen dataclass in `models.py` |
| Service | `product/service/ProductService`: `@Service` + Lombok `@RequiredArgsConstructor`, so Spring injects the `ProductRepository` bean | `product/service.py`: `ProductService(repository)`, wired by hand (Step 2.4 does it with `Depends`) |

**Tests**

| | Java `ProductServiceTest`, 8 tests | Python `tests/product/test_service.py`, 9 tests |
|---|---|---|
| Style | **Mockito mocks**: `@Mock` repository, `@InjectMocks` service, `when(...).thenReturn(...)`, `verify(..., never())`, `ArgumentCaptor` | **Fake**: a real `InMemoryProductRepository` via fixtures, checking outcomes. Plus **one mock-style test** with `Mock(spec=ProductRepository)`, `assert_called_once_with`, `assert_not_called` |
| Covered | create; id ignored on create (captor shows `save` received id null); duplicate SKU **never calls save**; get missing; update keeps SKU; update missing never saves; delete missing/present | create; id ignored; duplicate SKU (store still has 1); get missing; update keeps SKU **and is persisted**; update missing; delete; delete missing; duplicate never calls save (mock) |

**Fix along the way: Mockito agent warning (Java)**
- **Warning:** "A Java agent has been loaded dynamically … will be disallowed by default in a future release". Mockito attaches byte-buddy at runtime, and Java 21+ warns about that.
- **Fix in `pom.xml`:** the `maven-dependency-plugin` `properties` goal (exposes `${org.mockito:mockito-core:jar}`) + `maven-surefire-plugin` `<argLine>@{argLine} -javaagent:${org.mockito:mockito-core:jar}</argLine>` + an empty `<argLine></argLine>` property.
- **Mistake on the way:** without the empty property, `@{argLine}` was passed literally and the test JVM failed with `could not open '{argLine}'`. `@{...}` is resolved late by Surefire, so the property must exist.

**Result:** Java **27 tests** ✅ (8 new), no agent warning. Python **29 tests** ✅ (9 new). ruff, format, mypy (21 files), Spotless ✅.

**Learned:**
- **Constructor injection:** Spring sees one constructor + one matching bean and wires them automatically. In Python you pass the dependency yourself (FastAPI's `Depends` automates it per request in Step 2.4). Both make the service easy to test with a different repository.
- **Mocks vs fakes:** mocks verify *interactions* ("save was never called") and need no real implementation. Fakes verify *outcomes* and catch more real bugs (e.g. the "persisted, not just returned" check). Mocks can't catch a bug where the code calls the right method but the behaviour is wrong.
- `Mock(spec=...)` in Python is like Mockito's type safety: calling a method the Protocol doesn't have raises an error instead of silently returning a new Mock.
- **Known gap:** "find by SKU, then save" is a check-then-act race. Two parallel creates with the same SKU could both pass the check. The database's unique constraint closes this in Stage 3.

**Not committed yet.**

### Step 2.4: Product CRUD endpoints (2026-10-20)

**Goal:** The first usable HTTP API. It's thin: request → service → response with the right status code.

| Endpoint | Success | Errors |
|---|---|---|
| `GET /api/v1/products` | 200 | n/a |
| `GET /api/v1/products/{id}` | 200 | 404 |
| `POST /api/v1/products` | **201** + `Location` header | 409 duplicate SKU |
| `PUT /api/v1/products/{id}` | 200 | 404 |
| `DELETE /api/v1/products/{id}` | **204** | 404 |

#### Java

| File | Change |
|---|---|
| `product/web/ProductController.java` | **New.** `@RestController @RequestMapping("/api/v1/products")`, `@Get/Post/Put/DeleteMapping`, `@PathVariable`, `@RequestBody`, `ResponseEntity.created(uri)` / `noContent()`. The service is injected by constructor |
| `product/exception/*Exception.java` | `@ResponseStatus(NOT_FOUND / CONFLICT)` (**temporary**, Stage 4 centralizes it), plus `serialVersionUID` |
| `product/model/Product.java` | `@AllArgsConstructor(access = PRIVATE)`; see the bug below |
| `ProductControllerTest.java` | **New, 7 tests.** `@WebMvcTest(ProductController.class)` slice + `@MockitoBean ProductService` + `@ActiveProfiles("test")` |
| `ProductTest.java` | +1 test: `new Product().isActive()` is true |

#### Python

| File | Change |
|---|---|
| `product/dependencies.py` | **New.** `get_product_repository()` with `@lru_cache` (**singleton store**) and `get_product_service(repository = Depends(...))` |
| `product/router.py` | **New.** `APIRouter(prefix="/api/v1/products")`, `Service = Annotated[ProductService, Depends(get_product_service)]`, typed path params, `status_code=201/204`, `Response` for the Location header, domain errors → `HTTPException(404/409)` (**temporary**) |
| `main.py` | `app.include_router(product_router.router)` |
| `tests/product/test_router.py` | **New, 8 tests.** An autouse fixture swaps in a fresh store via `app.dependency_overrides`, plus a regression test that data survives between requests with the real singleton (`cache_clear()` before and after) |

#### Shared

**`http/products.http`** (new): the 7-request CRUD flow; switch `@host` between 8080 and 8000.

#### Bug found by the slice test: Jackson 3 + Lombok

- **Symptom:** `POST` returned **400**: `Cannot map 'null' into type 'boolean'`.
- **Cause:** Spring Boot 4 uses **Jackson 3**, which automatically deserializes through a class's (public) all-args constructor. Lombok's `@AllArgsConstructor` provided one, so a missing `"active"` became `null` for a primitive `boolean`, and the `= true` default never applied.
- **Fix:** `@AllArgsConstructor(access = AccessLevel.PRIVATE)`. Only the builder uses it; Jackson falls back to the no-args constructor + setters. Tests added: the no-args constructor defaults to active, and the controller receives `active=true` when the JSON omits it (`ArgumentCaptor`).
- **Lesson:** a real client would have hit this. Stage 4 DTOs (records with validation) remove the problem at the root.

#### Verification

- Java **35 tests** ✅ (8 new), **0 compiler warnings** (`-Xlint` flagged the missing `serialVersionUID`; fixed). Python **37 tests** ✅ (8 new). ruff, format, mypy (24 files), Spotless ✅.
- **Live run with curl against both apps:** identical status codes for all 7 requests (200, 201+Location, 409, 200, 200, 204, 404).

**Differences seen in the live run (Stage 4 unifies them):**

| | Java | Python |
|---|---|---|
| `price` in JSON | number `12.50` | string `"12.50"` (Pydantic keeps `Decimal` exact as text) |
| Error body | Spring default `{timestamp, status, error, path}`, **no message** | `{"detail": "A product with SKU MUG-1 already exists"}` |
| Field order | alphabetical | declaration order |

#### Spring Boot vs FastAPI

| | Spring Boot | FastAPI |
|---|---|---|
| Route definition | Annotations on methods in a `@RestController` class | Decorators on functions in an `APIRouter` |
| Path/body binding | `@PathVariable`, `@RequestBody` | By type: simple types → path/query, models → body |
| Status codes and headers | `ResponseEntity` | `status_code=` on the decorator, a `Response` parameter for headers |
| Dependency lifetime | Beans are **singletons** by default | `Depends` runs **per request**; a singleton needs `@lru_cache` |
| Swap a dependency in tests | `@MockitoBean` | `app.dependency_overrides[...]` |
| Web-only test | `@WebMvcTest` slice (no service or repository beans) | No built-in slice; override the dependency instead |

**Learned:**
- The `.dumpstream` files in `target/surefire-reports` were leftovers from earlier runs. "See dump files" in the Maven output was misleading; the real cause was 2 failing assertions further up. Read the `Tests run:` lines first.
- Without `@lru_cache` on `get_product_repository`, every request would create an empty store and every `GET` after a `POST` would return 404. The regression test guards against that.

**Not committed yet.**

### Step 2.5: Coverage reports + 80% gate (2026-10-20)

**Decision (user):** Service unit tests already exist from Step 2.3, so Step 2.5 became **coverage measurement** with an 80% minimum in both apps.

#### Java: JaCoCo 0.8.15 (`pom.xml`)

- `prepare-agent` puts the JaCoCo agent into the `argLine` property, which Surefire's `@{argLine}` (prepared in Step 2.3) picks up.
- `report` (phase `test`) → `target/site/jacoco/index.html` (+ `jacoco.csv`).
- `check` (phase `verify`): `BUNDLE` / `LINE` / `COVEREDRATIO` ≥ `${jacoco.minimum.line}` (property, default `0.80`, override with `-Djacoco.minimum.line=0.95`).
- **Run:** `./mvnw clean verify`.

#### Python: pytest-cov 7.1.0 + coverage 7.16.2 (`pyproject.toml`)

- `addopts` adds `--cov=ecommerce --cov-report=term-missing --cov-report=html`, so **every** `uv run pytest` measures coverage → terminal table + `htmlcov/index.html`.
- `[tool.coverage.run]`: `branch = true`, `source = ["ecommerce"]`.
- `[tool.coverage.report]`: `fail_under = 80`, `show_missing`, `exclude_also` for the `run()` dev-server launcher and `if TYPE_CHECKING:`.
- **Mistake caught:** I first wrote the regex `"def run\(\) -> None:"` in a TOML double-quoted string, where `\(` is an invalid escape. Single-quoted TOML literal strings keep backslashes as-is.

#### Results

| | First run | Gaps found | After gap tests |
|---|---|---|---|
| **Java** | 90.2% lines (55/61), branches 14/16 | `ProductService.list()` untested; `ProductController.get()` success untested; `Product.equals` vs another type; exception getters (used in Stage 4); `main()` (never run by tests) | **93.4% lines (57/61), branches 15/16**, 38 tests |
| **Python** | 98.93% | `models.py:28`: `__eq__` returning `NotImplemented` for a non-Product | **100%** (175 statements, 12 branches), 38 tests |

New tests: `listReturnsWhatTheRepositoryHas`, `getReturnsProduct`, `productIsNeverEqualToAnotherType` (Java); `test_product_is_never_equal_to_another_type` (Python).

#### Proof that the gate fails

| Run | Result |
|---|---|
| Python, only `tests/test_health.py` | `FAIL Required test coverage of 80.0% not reached. Total coverage: 57.75%`, exit 1 ✅ |
| Java, only `HealthEndpointTest`, **without `clean`** | ⚠️ BUILD SUCCESS: **stale data** merged from the previous run |
| Java, only `HealthEndpointTest`, **with `clean`** | `lines covered ratio is 0.16, but expected minimum is 0.80`, BUILD FAILURE ✅ |
| Java, all tests, `-Djacoco.minimum.line=0.95` | `lines covered ratio is 0.93, but expected minimum is 0.95`, BUILD FAILURE ✅ |

**Learned:**
- **JaCoCo appends** to `target/jacoco.exec` by default, so a partial run without `clean` can pass on old data. Always use `./mvnw clean verify` for coverage (and in CI). pytest-cov erases its data at the start of each run.
- **Lombok-generated code doesn't count:** Lombok adds `@lombok.Generated`, and JaCoCo skips annotated methods. Coverage reflects code we wrote.
- **Python counts branches** in its percentage (statements + branches combined), while the Java gate counts **lines only**. The numbers aren't directly comparable.
- Coverage shows what code ran, **not** whether the tests check the right thing. The Jackson bug in 2.4 had 100% line coverage before the slice test asserted on behaviour.
- Coverage reports are git-ignored (`target/`, `htmlcov/`, `.coverage`).

**Daily commands:**
- Java: `./mvnw clean verify` → open `target/site/jacoco/index.html`
- Python: `uv run pytest` → open `htmlcov/index.html`

**Stage 2 complete.** Not committed yet.

### Step 2.6: Config moved into each app; root `.env` removed (2026-10-20)

**Change requested by the user:** No env file at the repo root; each app keeps its own properties.

**Decisions (user):**
1. Java config in `application-dev.yml`; Python config in `python-app/.env`.
2. Docker Compose uses **literal dev values** in `docker-compose.yml`.
3. **Simple dev passwords, committed** (the `.gitignore` no longer ignores `.env`). Fine for a POC that only runs locally.

**Local dev credentials (committed on purpose):**

| What | Value |
|---|---|
| Postgres superuser | `postgres` / `postgres` |
| App database login | `ecomm` / `ecomm` on `ecomm_db` |
| pgAdmin (http://localhost:5050) | `admin@example.com` / `admin` |
| JWT secret (dev) | `dev-only-jwt-secret-change-me-0123456789` (40 chars) |

**Files changed:**

| File | Change |
|---|---|
| `.env`, `.env.example` (root) | **Deleted** |
| `docker-compose.yml` | `${...}` variables replaced by the literal dev values above |
| `java-app/.../application.yml` | `spring.config.import` of `../.env` **removed**. `app.jwt-secret: ${JWT_SECRET}` stays **without a default**, so any non-dev profile must supply it |
| `java-app/.../application-dev.yml` | Now holds the dev values with overridable placeholders: `${JWT_SECRET:dev-only-...}`, `${HOLD_DURATION:PT15M}`, `environment: dev` |
| `java-app/.../application-test.yml` | Comment updated (no `.env` mention) |
| `python-app/.env` | **New:** `APP_ENV`, `JWT_SECRET`, `HOLD_DURATION` |
| `python-app/.../core/config.py` | `env_file=".env"` (was `("../.env", ".env")`) |

**Commands:** `docker compose down -v` (both volumes deleted, because Postgres and pgAdmin only read their passwords on first start), then `docker compose up -d`.

**Verification:**
- `docker compose config` is valid with no env file.
- `ecomm`/`ecomm` connects to `ecomm_db`.
- pgAdmin user `admin@example.com` exists (Administrator, active), checked with `setup.py get-users`. **The password isn't verified:** pgAdmin's login page is a JavaScript app and can't be checked with a scripted POST. Log in once in the browser to confirm.
- Both apps started **without environment variables** and loaded `environment=dev`, a masked secret and a 15-minute hold from their own config.
- Java 38 tests ✅ + coverage gate; Python 38 tests ✅ (100%); ruff, format, mypy, Spotless ✅.

**Learned:**
- **Spring:** a value in a profile file beats the base file, and an OS environment variable beats both. `${JWT_SECRET:default}` in the dev profile keeps env overrides working, while the base file's `${JWT_SECRET}` (no default) makes production fail fast if the secret is missing.
- **Postgres and pgAdmin images read their credentials only on first start** (when the volume is empty). Changing them later needs a volume reset or a manual `ALTER USER`.
- **Trade-off:** each app is now self-contained, but the DB credentials appear in two places (`docker-compose.yml` and, from Step 3.1, each app's config). They must be kept in sync by hand.

**Not committed yet.**

### Step 2.7: Postman collection (v3) with switchable environments (2026-10-20)

**Requested by the user:** One collection and two environments, `java-dev` and `python-dev`, to switch between the apps.

**History:** The first version (v2.1 JSON files) got messed up after Postman opened the folder, and the user deleted it. Postman had treated `ECOMM/postman` as a **local workspace** (it created an empty `.postman/` there), and local workspaces use the **v3** format. Regenerated in v3.

**Decision (user):** Keep `ECOMM/postman` as the workspace root, so the resources live in `ECOMM/postman/postman/...`.

**How it was generated (with Postman's own tooling, Postman CLI 1.75.0, already installed):**
1. A script (scratchpad) built a v2.1 JSON with the same requests and tests as before.
2. `postman collection migrate <v21.json> --output "postman/collections/ECOMM POC"` produced the v3 YAML.
3. `postman environment new java-dev` / `python-dev`, then `postman environment var set <key> <value> --environment <file>` for each variable.

**Files:**

```
postman/                                   <- Postman local workspace root
├── .postman/                              (created by Postman; workspace config)
└── postman/
    ├── collections/ECOMM POC/
    │   ├── .resources/definition.yaml     (collection description)
    │   ├── Health/                        Health.request.yaml
    │   ├── Products (CRUD flow)/          1. List … 7. Get deleted product (404) .request.yaml
    │   └── App-specific/                  Java only - app info, Python only - OpenAPI document
    └── environments/
        ├── java-dev.environment.yaml      baseUrl=http://localhost:8080, app=Spring Boot, sku=MUG-1, productId
        └── python-dev.environment.yaml    baseUrl=http://localhost:8000, app=FastAPI,     sku=MUG-1, productId
```

**v3 format notes:**
- One `*.request.yaml` per request: `$kind: http-request`, `url`, `method`, `headers`, `body` (`type: json`, `content`), `scripts` (test scripts are `type: afterResponse`), and `order` (fractional ordering: 1000, 2000…).
- Folders and the collection have `.resources/definition.yaml` (`$kind: collection`, `description`, `order`).
- Environments: `name` + `values` list of `{key, value, enabled}`.

**Improvement over v2.1:** the two app-specific requests now **pass in both environments**. Their test reads the `app` variable and expects 200 in its own app and 404 in the other.

**Verification:**
- `postman collection lint … --fail-severity warning`: **10 scanned, 0 errors, 0 warnings**. `postman environment lint`: **2 scanned, 0 errors, 0 warnings**.
- `postman collection run "…/ECOMM POC" --environment …/<env>.environment.yaml --no-report-events` against both running apps, which **executes the JavaScript tests**:
  - java-dev: **10 requests, 18 assertions, 0 failed**
  - python-dev: **10 requests, 18 assertions, 0 failed**
- The run doesn't write `productId` back into the environment files.
- "No authorization data found" is only a notice; local runs don't need `postman login`. `--no-report-events` keeps run results from being sent to Postman's cloud.

**How to use:**
- **Postman app:** open/connect the `ECOMM/postman` folder as a local workspace (as before). The collection "ECOMM POC" and both environments appear; pick **java-dev** or **python-dev** at the top right.
- **Command line** (both apps running), using absolute paths because the CLI resolved relative paths from another folder:

```powershell
postman collection run "D:\ClaudeWS\ECOMM\postman\postman\collections\ECOMM POC" --environment "D:\ClaudeWS\ECOMM\postman\postman\environments\java-dev.environment.yaml" --no-report-events
```

**Learned:**
- **Newman can't run v3 collections**; the Postman CLI can.
- `postman collection migrate` is the reliable way to produce v3: hand-written YAML would have to match an undocumented-in-prose schema, and `lint` checks it.
- Git doesn't track empty folders, so `.postman/` (empty) won't be committed. Postman recreates it when connecting.
- If Postman can't reach the Python app via `localhost`, use `http://127.0.0.1:8000` (uvicorn listens on IPv4 only).

**Not committed yet.**

### Step 2.8: Database profiles `local` and `docker` (2026-10-20)

**Requested by the user:** Use the PostgreSQL now installed on this machine (**localhost:5433**), and have two profiles, `local` and `docker`, to switch between databases.

**What was found:**
- Local PostgreSQL **18.6**, Windows service `postgresql-x64-18` (automatic start), port **5433**. The installer avoided 5432, which the Docker container held at install time.
- `psql` is at `C:\Program Files\PostgreSQL\18\bin\psql.exe` (not on PATH).
- Docker Desktop was not running.

**Design: profile = which database; `dev` = shared app settings**

| Profile | Database | Java | Python |
|---|---|---|---|
| `local` (**default**) | Installed Postgres `localhost:5433/ecomm_db` | `application-local.yml` | `.env.local` |
| `docker` | Compose Postgres `localhost:5432/ecomm_db` | `application-docker.yml` | `.env.docker` |
| (shared) | JWT secret, hold duration, `APP_ENV=dev` | `application-dev.yml`, pulled in by profile **groups** `local: dev`, `docker: dev` | `.env` |

**How to switch:**
- Java: `SPRING_PROFILES_ACTIVE=docker` (unset = `local`).
- Python: `APP_PROFILE=docker` (unset = `local`).
- For example in PowerShell: `$env:SPRING_PROFILES_ACTIVE='docker'; .\mvnw.cmd spring-boot:run`, or `$env:APP_PROFILE='docker'; uv run ecommerce`.

**Files changed:**

| File | Change |
|---|---|
| `java-app/.../application.yml` | `spring.profiles.default: local` + `spring.profiles.group: {local: dev, docker: dev}` |
| `java-app/.../application-local.yml` | **New:** `spring.datasource.url: jdbc:postgresql://${DB_HOST:localhost}:${DB_PORT:5433}/${DB_NAME:ecomm_db}`, username/password `ecomm` (overridable) |
| `java-app/.../application-docker.yml` | **New:** the same with port 5432 |
| `java-app/.../core/config/ConfigLogger.java` | Also logs the profiles (falls back to the default profiles, marked "(default)") and `Database: <url> as user <user>` (never the password) |
| `java-app/.../core/config/ProfilesTest.java` | **New, 2 tests:** starts the app without a web server; default → `getDefaultProfiles()` contains `local`, URL port 5433, dev settings applied via the group; `docker` → active `[docker, dev]`, port 5432 |
| `python-app/.env` | Shared settings only (comment updated) |
| `python-app/.env.local`, `.env.docker` | **New:** `APP_PROFILE`, `DB_HOST`, `DB_PORT` (5433 / 5432), `DB_NAME`, `DB_USER`, `DB_PASSWORD` |
| `python-app/.../core/config.py` | `profile` (`APP_PROFILE`, `Literal["local","docker"]`), `db_*` fields (defaults = local), `database_url` property (SQLAlchemy URL, used in Step 3.1), `database_display` (no password, for logs). `get_settings()` reads `Settings(_env_file=(".env", f".env.{profile}"))`, so the profile file wins |
| `python-app/.../main.py` | Lifespan also logs `Profile:` and `Database:` |
| `python-app/tests/test_config.py` | **+3 tests:** parametrized local/docker → port + URL; default profile is local |
| `db-scripts/00-local-setup.sql` | **New:** creates `ecomm`/`ecomm` and `ecomm_db` (owner), revokes PUBLIC connect, makes `ecomm` owner of schema `public`. **Run by the user**, see below |
| `docker/pgadmin/servers.json` | Two servers: "ECOMM (docker, 5432)" → `postgres:5432` and "ECOMM (local, 5433)" → `host.docker.internal:5433` |

**Verification:**
- Java **40 tests** ✅ (2 new) + coverage gate. Python **41 tests** ✅ (3 new), 100% coverage. ruff, format, mypy, Spotless ✅.
- **Real startups:**
  - Java default: `Profiles: [local, dev] (default)` / `jdbc:postgresql://localhost:5433/ecomm_db`
  - Java `docker`: `Profiles: [docker, dev]` / `jdbc:postgresql://localhost:5432/ecomm_db`
  - Python default: `Profile: local` / `localhost:5433/ecomm_db as user ecomm`
  - Python `docker`: `Profile: docker` / `localhost:5432/...`
- `ecomm`/`ecomm` on local 5433 → **password authentication failed for user "ecomm"**, as expected: the login doesn't exist until `db-scripts/00-local-setup.sql` has run.

**⏳ To do by the user (needs the local `postgres` superuser password, which Claude doesn't type):**

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5433 -U postgres -f db\local-setup.sql
```

**Not verified yet:**
- The pgAdmin "local" server entry: Docker wasn't running, and `servers.json` is only read on pgAdmin's first start (needs `docker volume rm ecomm_pgadmin-data`, or add the server by hand).
- Whether your local Postgres accepts connections coming from a container (`pg_hba.conf`) is also untested. The apps connect from the host, so they're unaffected.

**Learned:**
- **Spring default vs active profiles:** without `SPRING_PROFILES_ACTIVE`, `getActiveProfiles()` is **empty** and the fallback shows in `getDefaultProfiles()`. My first test assumed otherwise and failed. Profile **groups also expand default profiles**: `local` (default) still pulled in `dev`, as the test proves via the dev JWT secret.
- **Python has no profiles**, so the pattern was built by hand: a selector variable + `_env_file=(".env", f".env.{profile}")`. Later files win, and real environment variables still beat both.
- **Leftover Java processes (Steps 1.3 and 2.8):** on this machine `java` on the PATH is Oracle's `javapath\java.exe` **launcher stub**, which starts the real JDK `java.exe` as a child. Stopping the stub left the real app running on 8080, so the next start failed with "Failed to start bean 'webServerStartStop'" (port in use). Stop the app by its command line (the jar name), not by the PID `Start-Process` returns.
- Two Postgres servers now coexist: local on 5433, Docker on 5432.

**Not committed yet.**

### Step 2.9: `db-scripts/`: schema and DDL for all tables (2026-10-20)

**Requested by the user:** A new root folder for DB scripts, containing the schema and the DDL for all tables.

**Decisions (mine, flagged to the user):**
- Folder `db-scripts` (hyphen instead of a space, so commands stay easy to type). `db/local-setup.sql` moved in as `00-local-setup.sql`; references in `application-local.yml` and `.env.local` updated.
- A dedicated schema **`ecomm`** owned by login `ecomm`, with `ALTER ROLE ecomm IN DATABASE ecomm_db SET search_path = ecomm, public`, so the apps use plain table names.

**Files:**

| Script | Run as | Purpose |
|---|---|---|
| `00-local-setup.sql` | `postgres`, once | Login `ecomm`/`ecomm`, database `ecomm_db` (local Postgres only) |
| `01-create-schema.sql` | `ecomm` | Schema `ecomm` + `search_path`; idempotent |
| `02-create-tables.sql` | `ecomm` | All tables, constraints and indexes in **one transaction** |
| `99-drop-schema.sql` | `ecomm` | `DROP SCHEMA ecomm CASCADE` (reset) |
| `README.md` | n/a | Run order, table overview, **Mermaid ER diagram**, design decisions |

**The 14 tables (from spec Parts 3 and 4):**

| Area | Tables |
|---|---|
| Auth | `users`, `addresses` |
| Catalog | `categories`, `products` |
| Inventory | `inventory`, `stock_adjustments` |
| Cart | `carts`, `cart_items` |
| Orders | `orders`, `order_lines`, `order_status_history` |
| Checkout | `stock_holds`, `payments`, `idempotency_records` |

**Design rules enforced in the DDL:**
- `numeric(12,2)` money
- `varchar + CHECK` for statuses, roles and reasons (no PG ENUMs)
- `bigint GENERATED ALWAYS AS IDENTITY` keys and `timestamptz` timestamps
- an index on **every** foreign key
- `version` columns on `products`, `inventory` and `orders`
- address and price **snapshots** on orders [SN-1, SN-2]
- `reserved <= on_hand` [ST-4]
- one default address per user (partial unique index) [AD-2]
- `line_total = unit_price * quantity`
- a tracking number required for SHIPPED/DELIVERED [SM-3]
- a unique `(user_id, idempotency_key)` on `orders` and `idempotency_records` [ID-2]
- `ON DELETE RESTRICT` protects ordered products [SN-4]

**Verification on a throwaway PostgreSQL 18.6** (`initdb` + `pg_ctl` from the local install, port 55432, trust auth, in the scratchpad; deleted afterwards; your installed server untouched):
- Scripts `00` → `01` → `01` again (idempotent: only an "already exists, skipping" notice) → `02`: all succeeded.
- A new `ecomm` connection gets `search_path = ecomm, public`, and the 14 tables are listed.
- **19 foreign keys, 0 without an index**, 24 CHECK constraints, 41 indexes.
- **Happy path:** a full flow (users, address, category, product, inventory + adjustment, cart + item, order + line + history, reservation, hold, payment, idempotency record) inserts cleanly, leaving 8 of 10 available.
- **12 rule-breaking writes, all rejected by the intended constraint:** upper-case email, unknown role, second default address, duplicate SKU, price 0, reserved > on_hand, cart quantity 11, wrong line total, SHIPPED without tracking, unknown status, duplicate idempotency key, deleting an ordered product. SHIPPED **with** a tracking number is accepted.
- `99-drop-schema.sql` dropped all 14 tables, and `01` + `02` recreated them.

**⏳ To do by the user, on the installed Postgres (5433):**

```powershell
$psql = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
& $psql -h localhost -p 5433 -U postgres -f db-scripts\00-local-setup.sql
& $psql -h localhost -p 5433 -U ecomm -d ecomm_db -f db-scripts\01-create-schema.sql
& $psql -h localhost -p 5433 -U ecomm -d ecomm_db -f db-scripts\02-create-tables.sql
```

**Relation to the apps (important for Stage 3):**
- This is the **target** schema for the whole POC. The Stage 2 `Product` model still has `active: boolean`, while the table has `status` (DRAFT/ACTIVE/DISCONTINUED, from Stage 5). The models will be aligned when Stage 3 maps them.
- **Step 3.2 (migrations):** `02-create-tables.sql` can become the first migration of the **one** tool that owns the shared schema (e.g. Flyway `V1__create_tables.sql`). Running these scripts by hand now and adding Flyway later would need Flyway's **baseline** feature, or a reset with `99-drop-schema.sql`.

**Learned:**
- **`pg_ctl start` hangs a piped shell on Windows:** the server inherits the console handles, so the command never "finishes". Start it with `Start-Process` (detached). Stopping the hung shell also killed the server, since it was a child process.
- PostgreSQL **doesn't index foreign keys automatically**. Without an index, deleting a parent row or joining scans the whole child table, so the verification query checks that none are missing.
- A role can set its **own** per-database defaults (`ALTER ROLE ecomm IN DATABASE ... SET search_path`) without being a superuser; that's why `01` runs as `ecomm`. It applies to **new** connections only.
- `GENERATED ALWAYS AS IDENTITY` is the SQL-standard successor of `serial`, and it prevents accidental manual ids. ORMs read the generated id back on insert.

**Not committed yet.**

### Step 2.10: Single setup file `db-scripts/ecomm-setup.sql` (2026-10-20)

**Requested by the user:** One single executable **SQL** file instead of separate setup, schema and table scripts.

**What changed:**
- **New `ecomm-setup.sql`, run once as `postgres`:**
  1. login `ecomm` (only if missing)
  2. database `ecomm_db` (only if missing)
  3. REVOKE/GRANT CONNECT
  4. `\connect ecomm_db`
  5. `public` owned by `ecomm`, schema `ecomm`, `search_path`
  6. **`SET ROLE ecomm`**, then all tables in one transaction
  7. `RESET ROLE`
  8. a summary listing every table and its owner
- **Re-runnable:**
  - `CREATE ROLE` and `CREATE DATABASE` are generated with `SELECT ... WHERE NOT EXISTS ... \gexec` (psql runs the generated statement only when a row comes back; `CREATE DATABASE` has no `IF NOT EXISTS` and can't run inside a `DO` block).
  - Tables and indexes use `IF NOT EXISTS`.
- **Built from the already-verified DDL** (the table section of the old `02-create-tables.sql` with `IF NOT EXISTS` added), so the table definitions are unchanged.
- **Removed:** `00-local-setup.sql`, `01-create-schema.sql`, `02-create-tables.sql`. **Kept:** `99-drop-schema.sql` (its header now points to `ecomm-setup.sql`).
- Updated: `README.md` (scripts table and run commands), comments in `application-local.yml` and `.env.local`.
- Also works against the **Docker** database: `-p 5432 -U postgres` (password `postgres`). The login and database already exist there and are skipped.

**Verification on a fresh throwaway PostgreSQL 18.6** (port 55432, deleted afterwards):
- **Run 1:** exit 0, 14 tables, **all owned by `ecomm`** (proves `SET ROLE` works).
- **Run 2:** exit 0, only 34 "already exists, skipping" notices (1 schema + 14 tables + 19 indexes), no changes.
- The same checks as Step 2.9 on the result: `search_path = ecomm, public`, 19 FKs with 0 unindexed, 24 checks, 41 indexes, happy path OK, **12 of 12** rule-breaking writes rejected, SHIPPED with tracking allowed.
- `99-drop-schema.sql`, then `ecomm-setup.sql` again: rebuilt the 14 tables.

**On your local Postgres:** the command was opened in a Terminal tab for you to enter the `postgres` password:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5433 -U postgres -f db-scripts\ecomm-setup.sql
```

**Learned:**
- **`SET ROLE`:** a superuser can act as another role, and objects created afterwards belong to that role. Without it, `postgres` would own the tables and the app login could read them only with extra grants.
- **`\gexec`** is psql's way to do "create if not exists" for statements that have no such option.
- **Escaping trap (again):** writing Windows paths through a Python string turned `\18\bin` into control characters (`\1` octal, `\b` backspace) in the README. Fixed with a regex replace; checked for 0 control characters. Raw strings or `chr(92)` avoid it.

**Not committed yet.**

### Step 2.11: Superuser only (`postgres`/`password`), schema created on local Postgres (2026-10-20)

**Requested by the user:** Don't create a separate login. Use the root user `postgres` with password `password`.

**Decision (mine, flagged):** applied to the **Docker** database too, so both profiles behave the same and one setup file serves both.

**Changes:**

| File | Change |
|---|---|
| `db-scripts/ecomm-setup.sql` | No `CREATE ROLE`, no REVOKE/GRANT, no `SET ROLE`. Creates `ecomm_db` (if missing), schema `ecomm`, `ALTER ROLE postgres IN DATABASE ecomm_db SET search_path = ecomm, public`, and the 14 tables (now owned by `postgres`) |
| `db-scripts/99-drop-schema.sql` | Header: run as `postgres` with `-d ecomm_db` |
| `db-scripts/README.md` | Credentials and run commands updated |
| `application-local.yml`, `application-docker.yml` | `username: ${DB_USER:postgres}`, `password: ${DB_PASSWORD:password}` |
| `python-app/.env.local`, `.env.docker`; `core/config.py` defaults | `DB_USER=postgres`, `DB_PASSWORD=password` |
| `python-app/tests/test_config.py` | Expected URL `postgresql+psycopg://postgres:password@...` |
| `docker-compose.yml` | `POSTGRES_PASSWORD: password`; `DB_*` variables removed; **mounts `db-scripts/ecomm-setup.sql` as the init script**, so the Docker DB is built from the same file |
| `docker/postgres/init/01-create-databases.sh` | **Deleted** (with its folders) |
| `docker/pgadmin/servers.json` | Both servers log in as `postgres` |

**Run on the local Postgres (5433), by Claude, with the password the user gave:**
- **Before:** only the `postgres` database and role existed.
- `ecomm-setup.sql` → exit 0: `ecomm_db`, schema `ecomm`, **14 tables** (owner `postgres`).
- **Verification** (test data inside a rolled-back transaction):
  - `search_path = ecomm, public`
  - 19 FKs, 0 without an index; 24 checks; 41 indexes
  - happy path OK
  - **12 of 12** rule-breaking writes rejected; SHIPPED with tracking allowed
  - **0 rows left** afterwards
- Re-running `ecomm-setup.sql` → exit 0.
- Java 40 tests + coverage gate ✅; Python 41 tests, 100% ✅; ruff, mypy, Spotless ✅.

**Not verified:** the Docker side. Docker Desktop isn't running, and the existing `ecomm_pgdata` volume still has the **old** setup (`ecomm` login, password `postgres`). Before using the `docker` profile, reset it: `docker compose down -v`, then `docker compose up -d`. The init script only runs on an empty volume.

**Trade-off (worth knowing):** apps connecting as a **superuser** can do anything: drop databases, read every schema, bypass permission checks. That's fine for a local learning POC. A real deployment uses a dedicated least-privilege login, which is what Steps 0.2 to 2.10 had.

**Not committed yet.**

### Step 2.12: pgAdmin removed from Docker (2026-10-21)

**Requested by the user:** Remove pgAdmin from Docker; a local pgAdmin is used instead.

**Changes:**
- `docker-compose.yml`: `pgadmin` service and `pgadmin-data` volume removed. Only the optional `postgres` service (port 5432, `docker` profile) is left; the header now says so.
- `docker/` folder **deleted**: `docker/pgadmin/servers.json` plus the empty `docker/postgres/init` folders left over from Step 2.11.
- Docker: the stopped container `ecomm-pgadmin` and the volume `ecomm_pgadmin-data` (pgAdmin's own settings only) removed with `docker rm` / `docker volume rm`.
- **Not touched:** the container `ecomm-postgres` and the volume `ecomm_pgdata` (still the old pre-2.11 setup; reset with `docker compose down -v` before using the `docker` profile).

**Verification:** `docker compose config` is valid. Only `ecomm-postgres` and `ecomm_pgdata` remain.

**To connect your local pgAdmin:**

| Server | Host | Port | Database | User / password |
|---|---|---|---|---|
| Local Postgres | `localhost` | `5433` | `ecomm_db` (tables in schema `ecomm`) | `postgres` / `password` |
| Docker Postgres (only when started) | `localhost` | `5432` | `ecomm_db` | `postgres` / `password` |

**Not committed yet.**

### Step 2.13: `db/` folder and day-1 sample data (2026-10-21)

**Requested by the user:** A `db` folder holding the Postgres Docker Compose file and the DB scripts (in a subfolder), plus DML with sample data for all tables, as "day 1".

**New layout:**

```
db/
├── README.md                   (replaces db-scripts/README.md; covers compose + scripts)
├── docker-compose.yml          (moved from the repo root)
└── scripts/
    ├── ecomm-setup.sql         (moved from db-scripts/)
    ├── day1-sample-data.sql    (NEW)
    └── 99-drop-schema.sql      (moved from db-scripts/)
```

`db-scripts/` and the root `docker-compose.yml` are gone. Compose now runs as `docker compose -f db/docker-compose.yml ...` (or from inside `db/`). `name: ecomm` keeps the same volume names.

**`day1-sample-data.sql`:**
- **Re-runnable:** `TRUNCATE` all 14 tables `RESTART IDENTITY CASCADE`, then insert, in one transaction, so ids are always the same.
- Starts with `\connect ecomm_db`, so it works however psql was started (Docker's init connects to `postgres`).
- Explicit ids via `OVERRIDING SYSTEM VALUE` for readable references; at the end a `DO` block calls `setval(pg_get_serial_sequence(...))` so the next app insert gets `max(id) + 1`.
- Fixed timestamps for 2026-10-21 (America/Chicago).
- **Seed password `Password123!` for all users**, stored as a bcrypt hash (`$2b$10$…`), generated with Python `bcrypt` and checked against the right and a wrong password. Spring Security and Python can both verify it.

| Table | Rows | Scenario it provides |
|---|---|---|
| users | 5 | 1 ADMIN; dave has **no address** (checkout must ask) [AD-3] |
| addresses | 4 | one default per user [AD-2]; alice has two |
| categories | 5 | Accessories nested under Electronics |
| products | 12 | DRAFT (`ACC-3102`), DISCONTINUED (`BOK-4002`), price raised during the day (`ELE-3002`) |
| inventory | 12 | `OFF-2003` out of stock; `KIT-1003` **last unit**, held (0 available) |
| stock_adjustments | 13 | 11 RESTOCK, 1 CORRECTION, 1 DAMAGE [ST-3] |
| carts / cart_items | 3 / 4 | bob's item at the **old price** [SN-5]; carol's item now discontinued |
| orders | 6 | CONFIRMED, SHIPPED, PENDING_PAYMENT, PAYMENT_FAILED, CANCELLED, DELIVERED |
| order_lines | 10 | snapshots; `line_total = unit_price × quantity` |
| order_status_history | 17 | full path per order [SM-2] |
| stock_holds | 2 | order 3, **already expired** (input for the Stage 14 expiry job) |
| payments | 7 | SUCCEEDED, TIMEOUT [PM-4], DECLINED, REFUND |
| idempotency_records | 6 | one per order, `request_hash` = SHA-256 hex |

**Docker:** the compose file mounts `ecomm-setup.sql` as `01-…` and `day1-sample-data.sql` as `02-…` in `/docker-entrypoint-initdb.d`, so a fresh Docker DB gets schema **and** data. Not tested yet: Docker's `ecomm_pgdata` volume still has the pre-2.11 setup and needs `docker compose -f db/docker-compose.yml down -v` first.

**References updated:**
- `ecomm-setup.sql` header (paths, "Next: day1-sample-data.sql")
- comments in `application-local.yml`, `application-docker.yml`, `.env.local`, `.env.docker`

**Verification on the local Postgres (5433):**
- The DML ran **twice**, both exit 0 (re-runnable), and also when connected to database `postgres` (as Docker does).
- Every insert passed the schema's 24 CHECK constraints and 19 foreign keys.
- **12 cross-table consistency checks, 0 problems:**
  - order subtotal = sum of lines
  - order status = last history entry
  - history chain (`from_status` = previous `to_status`)
  - `reserved` = held quantity; holds only on PENDING_PAYMENT orders
  - `on_hand` = adjustments − sold (CONFIRMED and later)
  - paid orders have a SUCCEEDED charge = grand total; the cancelled order is fully refunded; unpaid orders have no successful charge
  - the ship-to address matches a buyer address
  - line SKU = product SKU
  - every order has its idempotency record
- **Next ids:** a probe insert (rolled back) got id **6** for both `categories` and `users`.

**Learned:**
- `GENERATED ALWAYS AS IDENTITY` refuses explicit ids unless you write **`OVERRIDING SYSTEM VALUE`**, and then the sequence isn't advanced. Without the `setval` step, the app's first insert would fail with a duplicate key on id 1.
- `TRUNCATE ... RESTART IDENTITY CASCADE` is the fast, complete reset for seed data, but it **deletes everything** in those tables, so it's only for dev databases.
- Constraints check rows one at a time. Rules that span tables (totals vs lines, stock vs sales) need either application logic or verification queries like the 12 above.

**Not committed yet.**

### Step 2.13a: Docker Postgres rebuilt from the scripts (2026-10-21)

**Requested by the user:** Rerun Docker Compose.

**Commands:**
- `docker compose -f db/docker-compose.yml down -v`: removed the container and the old `ecomm_pgdata` volume (pre-2.11 setup, no real data).
- `docker compose -f db/docker-compose.yml up -d`

**Result:**
- `ecomm-postgres` (postgres:18) is **healthy** on `localhost:5432`.
- The container log shows both init scripts ran in order without errors: `running /docker-entrypoint-initdb.d/01-ecomm-setup.sql` → "Setup complete", then `02-day1-sample-data.sql` → "Day 1 sample data loaded", then "PostgreSQL init process complete".
- On 5432 (`postgres`/`password`): `search_path = ecomm, public`, row counts identical to the local DB in all 14 tables, **12 of 12 consistency checks with 0 problems**, the same 6 orders and statuses as on 5433.
- The apps' `docker` profile wasn't started: the apps don't connect to a database until Step 3.1.

**Learned:**
- Docker's health check (`pg_isready`) can report **healthy while the init scripts are still running**: the image starts a temporary server for them first. Wait for "PostgreSQL init process complete" in the log before relying on the data.
- Both databases (local 5433, Docker 5432) are now built from the **same two files** in `db/scripts/`.

**Not committed yet.**

### Step 3.1: Connect both apps to PostgreSQL, both profiles (2026-10-21)

**Requested by the user:** Connect both apps to the local (5433) and Docker (5432) databases for both profiles.

**Goal (guide Step 3.1):** Both apps open a connection pool at startup, prove it by reading from the database, **fail fast** when it's unreachable, and report the database in `/health`. Tests use a throwaway database.

#### Java

| File | Change |
|---|---|
| `pom.xml` | `spring-boot-starter-data-jpa` (Hibernate + HikariCP), `org.postgresql:postgresql` (runtime). Test: `spring-boot-testcontainers`, `org.testcontainers:testcontainers-postgresql` (**Testcontainers 2.0.5**, managed by Boot's BOM) |
| `application.yml` | `spring.datasource.hikari.initialization-fail-timeout: 1` (fail at startup), `connection-timeout: 5000`, `spring.jpa.open-in-view: false`, `hibernate.ddl-auto: validate` (Hibernate never changes the schema), `hibernate.default_schema: ecomm`, `management.endpoint.health.show-components: always` |
| `core/db/DatabaseInfoLogger.java` | **New.** An `ApplicationRunner` with `JdbcTemplate`: logs server version, port, database, schema and product count |
| `TestcontainersConfiguration.java` (test) | **New.** `@TestConfiguration` with a `@Bean @ServiceConnection PostgreSQLContainer("postgres:18")`: database `ecomm_db`, `postgres`/`password`, and `db/scripts/ecomm-setup.sql` copied to `/docker-entrypoint-initdb.d/`, so the real schema is used |
| `EcommerceApplicationTests`, `HealthEndpointTest` | `@Import(TestcontainersConfiguration.class)` |
| `ProfilesTest` | Rewritten with `ApplicationContextRunner` + `ConfigDataApplicationContextInitializer`: loads only the `application*.yml` files, with no beans and no database connection. Also checks username `postgres` |

The connection settings themselves were already in `application-local.yml` / `application-docker.yml` (Step 2.8).

#### Python

| File | Change |
|---|---|
| `pyproject.toml` / `uv.lock` | `sqlalchemy 2.1.5`, `psycopg[binary] 3.3.6`. Dev: `testcontainers[postgres] 4.15.0`. All have Python 3.15 wheels |
| `core/db.py` | **New.** `get_engine()` (`@lru_cache`, created on first use; `pool_pre_ping`, pool 5 + 5, `connect_timeout`), `get_session_factory()`, `get_db()` **generator dependency** (one session per request, closed in `finally`), `database_info()`, `is_database_up()` |
| `core/config.py` | `db_connect_timeout_s: int = 3` |
| `main.py` | The lifespan logs `Connected to PostgreSQL …` (raises → no startup if unreachable), and disposes the engine on shutdown |
| `core/health.py` | `/health` now runs `SELECT 1`: `{"status":"UP","components":{"db":"UP"}}`, or **503** `DOWN` (mirrors Actuator) |
| `tests/conftest.py` | Starts `PostgresContainer("postgres:18")` with `ecomm-setup.sql` mounted as init script, waits until `ecomm.products` exists, sets `DB_*` env vars **before** importing the app, and stops the container in `pytest_sessionfinish` |
| `tests/test_db.py` | **New, 3 tests:** connects to `ecomm_db`/schema `ecomm` with 0 products; `get_db` yields a working session and closes it; `/health` → 503 DOWN when the DB is unreachable (dependency override) |
| `tests/test_health.py`, `test_config.py` | Expect `components`; the profile tests drop the container's `DB_*` env vars |

#### Verification

- **Java 40 tests** ✅ + coverage gate, Testcontainers log `Container postgres:18 started in PT2.0S`. **Python 44 tests** ✅, 100% coverage, **3 s**.
- **Real startups, 4 combinations:**

| | local → 5433 | docker → 5432 |
|---|---|---|
| Java | `Connected to PostgreSQL 18.6 on port 5433: database ecomm_db, schema ecomm, 12 products`; `/health` 200 (`db: UP`) | `PostgreSQL 18.6 (Debian 18.6-1.pgdg13+2) on port 5432 … 12 products`; `/health` 200 |
| Python | `… 18.6 on port 5433 … 12 products`; `/health` 200 `{"status":"UP","components":{"db":"UP"}}` | `… 18.6 (Debian …) on port 5432 … 12 products`; `/health` 200 |

The version string shows two different servers: the Windows install vs the Debian build in Docker.

#### Issues found and fixed

| Issue | Cause | Fix |
|---|---|---|
| The Python suite took **131 s**, all in the "DB unreachable" test | On Windows a connection to a closed port isn't refused at once, and **libpq has no connect timeout by default**, so `/health` would also hang during a real outage | `connect_args={"connect_timeout": 3}` on the app engine (setting `db_connect_timeout_s`), 1 s in the test → **3 s** total. Java: Hikari `connection-timeout` 30 s → 5 s |
| `DeprecationWarning: testcontainers.postgres is deprecated` | Module moved in testcontainers 4.x | `from testcontainers.community.postgres import PostgresContainer` |
| mypy: `Iterator[Session]` has no `close` | `get_db` is a generator; `Iterator` doesn't declare `.close()` | Annotated as `Generator[Session]` |
| `ProfilesTest` would connect to the real databases | It started the full app to read config | Config-only `ApplicationContextRunner` |

#### Spring Boot vs FastAPI

| | Spring Boot | FastAPI |
|---|---|---|
| Pool | HikariCP, auto-configured from `spring.datasource.*` | SQLAlchemy `create_engine(...)`, written by hand |
| Per-request session | Managed by Spring (transaction-bound `EntityManager`) | `get_db()` generator dependency: `yield` + `finally` |
| Fail fast | `initialization-fail-timeout` + Hibernate's startup metadata check | The lifespan runs a query; an exception aborts startup |
| DB in `/health` | Automatic `db` health indicator | Written by hand |
| Test DB | `@ServiceConnection` overrides URL/user/password automatically | Set `DB_*` env vars before importing the app |
| Container lifecycle | One per Spring test context (2 here: MockMvc vs plain context) | One per pytest session |

**Learned:**
- **Always set connect timeouts.** Defaults are unlimited (libpq) or long (Hikari 30 s), so a dead database turns into hanging requests instead of fast errors.
- Testcontainers 2.x renamed the Java artifacts (`testcontainers-postgresql`) and package (`org.testcontainers.postgresql.PostgreSQLContainer`). testcontainers-python 4.x moved modules to `testcontainers.community.*`.
- Both test setups reuse **`db/scripts/ecomm-setup.sql`** through the image's init folder, so tests, Docker and the local DB share one schema definition.
- The Python engine is now created **lazily** (`@lru_cache` function), not at import, which avoids the import-order trap from Step 1.4.

**Not committed yet.**

### Steps 3.3 + 3.4 (+ 3.6): Products read and written in PostgreSQL (2026-10-21)

**Why:** The user saw `GET /api/v1/products` return `[]` with the app running. Step 3.1 had only **connected** the apps; the endpoints still used the Stage 2 in-memory store.

**Decisions (user):**
1. The API switches from `active` to **`status`** (`DRAFT` / `ACTIVE` / `DISCONTINUED`), like the table. This pulls part of Stage 5.4 forward.
2. `DELETE` is a **soft delete**: it sets `DISCONTINUED`, the product stays readable, `204` (spec rule SN-4). The table's `ON DELETE RESTRICT` would block hard deletes of ordered products anyway.
3. Both apps together.

#### Java

| File | Change |
|---|---|
| `product/model/ProductStatus.java` | **New** enum |
| `product/model/Product.java` | **JPA entity** for `products`: `@Id @GeneratedValue(IDENTITY)`, column lengths/precision, `@Enumerated(STRING) status` (default ACTIVE), `categoryId`, `@CreationTimestamp createdAt`, `@UpdateTimestamp updatedAt`, `@Version version`. Hand-written equality kept |
| `product/model/ProductUpdate.java` | `active` → `status` |
| `product/repository/ProductRepository.java` | `deleteById` removed (products are only discontinued) |
| `product/repository/ProductJpaRepository.java` | **New.** Spring Data `JpaRepository<Product, Long>` + derived `findBySku` |
| `product/repository/JpaProductRepository.java` | **New.** `@Repository` adapter implementing our contract (`findAll` sorted by id) |
| `product/repository/InMemoryProductRepository.java` (+ test) | **Deleted**: Mockito covers the service, Testcontainers the repository |
| `product/service/ProductService.java` | `@Transactional` on every method (`readOnly` for reads); create resets id/version/timestamps; update sets status; delete = set DISCONTINUED |
| `pom.xml` | + `spring-boot-starter-data-jpa-test` |
| Tests | `ProductTest`/`ProductServiceTest`/`ProductControllerTest` updated (soft delete, reset fields). **New `JpaProductRepositoryTest`** (`@DataJpaTest` + Testcontainers, 6 tests: generated columns, findBySku/findAll order, version increment, duplicate SKU, price ≤ 0, optimistic lock). **New `ProductApiIntegrationTest`** (full app → DB: create → list → 409 → soft delete → DISCONTINUED, version 1) |

#### Python

| File | Change |
|---|---|
| `product/models.py` | `ProductStatus(StrEnum)`; `Product.active` → `status`; + `category_id`, `version`, `created_at`, `updated_at`; `ProductUpdate.status` |
| `core/db.py` | `Base(DeclarativeBase)` with `MetaData(schema="ecomm")` |
| `product/orm.py` | **New.** `ProductRow` mapped to `ecomm.products` (`Identity(always=True)`, `Numeric(12,2)`, `server_default`/`onupdate` timestamps, `version_id_col` with a generator starting at **0**, like Hibernate) |
| `product/repository.py` | Protocol without `delete_by_id`. **New `SqlProductRepository(session)`**: maps row ↔ dataclass, commits per save, refreshes generated values, raises `StaleDataError` on a version mismatch or a missing row. `InMemoryProductRepository` kept as a **fake** for service and router tests (now with versions) |
| `product/service.py` | Create resets managed fields; update sets status; delete = soft delete |
| `product/dependencies.py` | `get_product_repository(session = Depends(get_db))` → `SqlProductRepository` (the `@lru_cache` singleton store is gone; the pool is the shared part) |
| `tests/conftest.py` | `clean_products` fixture (`TRUNCATE ecomm.products RESTART IDENTITY CASCADE` after the test) |
| Tests | models/service/router/in-memory tests updated. **New `test_sql_repository.py`** (7 tests, same cases as Java + a missing row). Router: **new DB round-trip test** through the real providers |

#### Postman and `.http`

- `2. Create product`: **pre-request script** sets `sku = TST-<timestamp>` (soft-deleted products keep their SKU, so a fixed SKU would 409 on re-runs); asserts `status == "ACTIVE"`.
- `5. Update product`: body `"status": "ACTIVE"`.
- `7. Get deleted product (404)` → **`7. Get discontinued product`**: expects 200 + `DISCONTINUED`.
- `postman collection lint` → 10 scanned, 0 errors, 0 warnings (the `beforeRequest` script type is valid v3).
- `http/products.http`: `@sku` variable, `status`, soft-delete comments, ids for your own product.

#### Verification

- **Java 41 tests** ✅ + coverage gate; **Python 53 tests** ✅, 100% coverage, 3.3 s. ruff, format, mypy, Spotless ✅.
- `ddl-auto: validate` accepted the entity against the real table (the app starts).
- **Live, local profile (your 5433 database):**
  - New Java jar on **8081**: `GET /api/v1/products` → **12 products** (first `KIT-1001 Coffee mug 12.50 ACTIVE`; ACTIVE 10, DRAFT 1, DISCONTINUED 1). Postman run → **10 requests, 19 assertions, 0 failed**.
  - Python on **8000**: 13 products (the 12 plus Java's Postman test product, which shows **both apps share the table**). Postman → 10 requests, 19 assertions, 0 failed.
  - Afterwards `day1-sample-data.sql` was reloaded to remove the 2 `TST-…` test products (12 products again).
- The user's **IntelliJ app on 8080** was left running. DevTools had already reloaded it from the rebuilt `target/classes`, and it serves the DB products.

#### Spring Boot vs FastAPI

| | Spring Boot (JPA) | FastAPI (SQLAlchemy) |
|---|---|---|
| Mapping lives on | The domain class itself (`@Entity Product`) | A separate row class (`ProductRow`); the domain dataclass stays plain |
| Repository code | Spring Data **generates** it from an interface (`findBySku` from the method name) | Hand-written queries (`select(...).where(...)`) |
| Transactions | `@Transactional` on service methods (proxy-based) | Per-request session; this repository commits per save |
| Optimistic locking | `@Version` → `ObjectOptimisticLockingFailureException` | `version_id_col` + an explicit version check → `StaleDataError` |
| JSON field names | camelCase (`categoryId`, `createdAt`) | snake_case (`category_id`, `created_at`); Stage 4 DTOs will align them |

**Learned:**
- **IDENTITY ids make Hibernate INSERT immediately on `save()`**: it must ask the database for the id. So constraint violations surface at `save()`, not at a later `flush()` (two tests first expected the latter).
- `ddl-auto: validate` is a free safety net: a column name or type typo in the entity stops startup instead of failing on a later query.
- With soft deletes, **unique keys are never freed**. Test flows and fixtures need fresh values (`TST-<timestamp>`) or a cleanup step (`clean_products`, the day-1 reload).
- IntelliJ + DevTools reloads from `target/classes`. Running `mvn clean` while the IDE app runs makes it reload whatever the build leaves there.

**Not committed yet.**

### Step 4.1: Request/response models (DTOs); entities stay internal (2026-10-21)

**Requested by the user:** All JPA entity objects were exposed as API responses. Create separate request/response classes and keep the JPA entity model separate, in both apps.

**Why it matters:** with the entity as the JSON, internal fields leak out (`version`), a client can send fields it shouldn't control (`id`, `version`), and any database change silently changes the API.

#### Java: new package `product/web/dto`

| Record | Role |
|---|---|
| `CreateProductRequest(sku, name, description, price, status, categoryId)` | POST body; `toProduct()` builds an unsaved entity (description defaults to `""`, status to ACTIVE) |
| `UpdateProductRequest(name, description, price, status)` | PUT body (no SKU); `toUpdate()` → the service's `ProductUpdate` |
| `ProductResponse(id, sku, name, description, price, status, categoryId, createdAt, updatedAt)` | Response; `from(Product)`; **no `version`** |

- `ProductController` accepts and returns only DTOs; the entity stays in service + repository.
- Mapping is hand-written (the guide's MapStruct is an option for larger models).
- `Product.java` comments updated: JSON no longer touches the entity.
- Tests: `ProductApiIntegrationTest` now asserts `$.version` **doesNotExist** and `createdAt` exists. `ProductControllerTest` +2: the response has no internal fields and gets defaults; a POST with `"id": 99, "version": 5` reaches the service as id/version **null**. **43 tests** ✅ + coverage gate.

#### Python: new `product/schemas.py`

| Model | Role |
|---|---|
| `ApiModel` | Base: `alias_generator=to_camel`, `populate_by_name=True`, so JSON is **camelCase like Java**, and snake_case is accepted too |
| `ProductCreateRequest` | POST body; `to_product()` → `Product` dataclass |
| `ProductUpdateRequest` | PUT body; `to_update()` → `ProductUpdate` |
| `ProductResponse` | `from_attributes=True`, so `ProductResponse.model_validate(product)` reads the dataclass; **no `version`** |

- `router.py` uses only the schemas.
- Tests +3: the exact response field set (camelCase, no version); `id`/`version` in a POST are ignored; snake_case `category_id` is accepted. The DB round-trip test asserts `version` is absent. **56 tests** ✅, 100%.

#### Live comparison (`GET /api/v1/products/8` from both apps, local DB)

```
JAVA   {"id":8,"sku":"ELE-3002","name":"Mechanical keyboard","description":"Tenkeyless, brown switches","price":89.90,"status":"ACTIVE","categoryId":3,"createdAt":"2026-10-21T12:14:00Z","updatedAt":"2026-10-21T16:00:00Z"}
PYTHON {"id":8,"sku":"ELE-3002","name":"Mechanical keyboard","description":"Tenkeyless, brown switches","price":"89.90","status":"ACTIVE","categoryId":3,"createdAt":"2026-10-21T07:14:00-05:00","updatedAt":"2026-10-21T11:00:00-05:00"}
```

- **Identical field names and order**; `version` exposed by neither.
- Postman on both: 10 requests, 19 assertions, 0 failed. Day-1 data reset afterwards (12 products).

**Remaining value-format differences (same values; open for a decision):**

| Field | Java | Python |
|---|---|---|
| `price` | JSON number `89.90` | JSON string `"89.90"` (Pydantic keeps Decimal exact as text) |
| timestamps | UTC `…Z` | the DB session's time zone `…-05:00` |

**Learned:**
- **DTOs are the API contract.** The entity and the ORM row can now change (new columns, renames) without clients noticing, and clients can't set fields like `version` or `id`.
- Unknown JSON fields are ignored by default in both stacks (Spring Boot sets Jackson's FAIL_ON_UNKNOWN_PROPERTIES off; Pydantic's default `extra="ignore"`). Stage 4.2 validation can make that strict if wanted.
- Pydantic `alias_generator=to_camel` is the one-line way to match Java/JavaScript naming conventions while keeping snake_case in Python code.

**Not committed yet.**

### Step 4.1a: Identical JSON formats: price as a string, UTC timestamps (2026-10-21)

**Requested by the user:** Both apps return `price` as a string like `"89.90"` and all timestamps in UTC with a `Z` suffix.

**Changes (response DTOs only; requests still accept `"12.50"` or `12.50`):**

| | Java `ProductResponse` | Python `schemas.py` |
|---|---|---|
| Price | `@JsonFormat(shape = STRING)` + `setScale(2, HALF_UP)` in `from(...)` | `Money = Annotated[Decimal, PlainSerializer(_money)]`, `quantize(0.01, ROUND_HALF_UP)` → str |
| Timestamps | Already right: `Instant` is always UTC, written as `…Z` | `UtcDateTime = Annotated[datetime, PlainSerializer(_utc_iso)]`: `astimezone(UTC)`, `+00:00` → `Z` |

**Edge case handled:** a client sending `"14.5"` now gets `"14.50"` back. Without the explicit scale, Java's POST response (the saved entity, not re-read) would have said `"14.5"` while the column stores `14.50`.

**Tests:**
- Java: `ProductControllerTest` +1 (price `"14.50"` from `14.5`, `createdAt` exactly `2026-10-21T12:14:00Z`); `price` assertions changed to strings; the integration test checks `"11.25"` and `createdAt` ends with `Z`. **44 tests** ✅.
- Python: **new `tests/product/test_schemas.py`** (07:14 at −05:00 → `2026-10-21T12:14:00Z`, microseconds kept, price `"14.50"`, `None` timestamps stay null); router test for `"14.5"` → `"14.50"`; the DB round trip asserts a `Z` timestamp. **59 tests** ✅, 100%.

**Live comparison** (`GET /api/v1/products/8`, local DB): Java and Python responses are **byte-for-byte identical**:

```
{"id":8,"sku":"ELE-3002","name":"Mechanical keyboard","description":"Tenkeyless, brown switches","price":"89.90","status":"ACTIVE","categoryId":3,"createdAt":"2026-10-21T12:14:00Z","updatedAt":"2026-10-21T16:00:00Z"}
```

Postman: 10 requests, 19 assertions, 0 failed on both. Day-1 data reset afterwards.

**Learned:**
- **Money as a JSON string** avoids clients (especially JavaScript) parsing it into a binary float. Many payment APIs do this.
- Python's `datetime.isoformat()` writes `+00:00`, not `Z`. Java's `Instant` writes `Z`. Normalising in the serializer, not in the database session, keeps it independent of the DB's time zone setting.
- Jackson 3 (`tools.jackson.*`) still uses the **old annotation package** `com.fasterxml.jackson.annotation` (jackson-annotations 2.21), so existing `@JsonFormat` code keeps working.

**Not committed yet.**

### Step 4.1b: App folders renamed (2026-10-21)

**Requested by the user:** `java-app` → **`ecomm-java-app`**, `python-app` → **`ecomm-py-app`**.

**Done:**
- The user closed IntelliJ, PyCharm and VS Code first (open IDEs lock folders on Windows and keep pointing at old paths).
- `Rename-Item` for both folders. `python-app` first failed with "being used by another process": **Claude's own shell** still had its working directory inside it. After `cd` out, the rename worked.
- **References updated:** `.pre-commit-config.yaml` (`files: ^ecomm-py-app/`, `^ecomm-java-app/…`, `cd ecomm-java-app`) and the docstring and comments in `core/config.py`.
- **No change needed:** the Java `TestcontainersConfiguration` (`../db/scripts/...`) and Python `conftest.py` (`parents[2] / "db"`) use relative paths; `db/docker-compose.yml`, Postman and `http/` don't mention the folders. The uv project/package name stays `ecommerce`.
- **Python `.venv` rebuilt** (`rm -rf .venv && uv sync --frozen`): the old one had absolute paths to `...\python-app\src` in `ecommerce.pth` and in its launcher `.exe` files.
- Stale `.coverage` deleted. `.idea/` files left untouched (IDE state).

**Verification:**
- Java `clean verify` → **44 tests** ✅ + coverage gate.
- Python ruff/format/mypy + **59 tests** ✅ (100%).
- `pre-commit run` on one file per app → ruff check, ruff format and spotless check (ecomm-java-app) all **Passed**.

**When reopening the IDEs:**
- IntelliJ: **File → Open → `D:\ClaudeWS\ECOMM\ecomm-java-app`** (it re-imports the Maven project).
- PyCharm: **File → Open → `D:\ClaudeWS\ECOMM\ecomm-py-app`**, then **Settings → Python Interpreter → Add → existing → `ecomm-py-app\.venv\Scripts\python.exe`** (the old interpreter entry points at the deleted `python-app\.venv`). Run configurations: working directory `D:\ClaudeWS\ECOMM\ecomm-py-app`.

**Learned:** On Windows a folder can't be renamed while **any** process has it as its current directory or holds a file in it open: IDEs, terminals, even a shell's `cd`. Virtual environments aren't relocatable (absolute paths inside), so after moving a project, rebuild `.venv` from the lock file.

**Not committed yet.** For Git it's a move; `git add -A` records it as renames.
