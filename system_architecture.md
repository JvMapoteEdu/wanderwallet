# WanderWallet — System Architecture

## Architecture Overview

WanderWallet follows a traditional **Monolithic MVC** (Model-View-Controller) pattern, hosted on a single server with server-side rendering.

```mermaid
graph TB
    %% ─── Actors ───────────────────────────────────────────────
    User(["👤 User\n(Web Browser)"])
    Admin(["🛡️ Admin\n(Web Browser)"])

    %% ─── Presentation Layer ───────────────────────────────────
    subgraph Presentation ["Presentation Layer — Frontend"]
        direction TB
        Templates["Jinja2 HTML Templates\n─────────────────────\nbase.html · home.html\nlogin.html · register.html\nreport_*.html (×5)"]
        Bootstrap["Bootstrap 5.3.2\n+ Bootstrap Icons 1.11.3\n+ Custom CSS (style.css)"]
    end

    %% ─── Application Layer ────────────────────────────────────
    subgraph Application ["Application Layer — Flask Backend (app.py)"]
        direction TB

        subgraph Auth ["Authentication"]
            R_Login["/login"]
            R_Register["/register"]
            R_Logout["/logout"]
            Session["Flask Session\n(SECRET_KEY)"]
        end

        subgraph TripMgmt ["Trip Management"]
            R_AddTrip["/add-trip"]
            R_EditTrip["/edit-trip"]
            R_DelTrip["/delete-trip"]
        end

        subgraph ExpenseMgmt ["Expense Management"]
            R_AddExp["/add-expense"]
            R_UpdExp["/update-expense"]
            R_DelExp["/delete-expense"]
        end

        subgraph Reports ["Reports (×5)"]
            R_Monthly["/report/monthly"]
            R_Budget["/report/budget"]
            R_Category["/report/category"]
            R_Remaining["/report/remaining"]
            R_UserSpend["/report/user-spending"]
        end

        subgraph AILayer ["AI Insights"]
            R_AI["/ai-insights"]
        end

        Home["/  — Dashboard\n(Stats, Trips, Expenses)"]
    end

    %% ─── Data Layer ───────────────────────────────────────────
    subgraph Data ["Data Layer — MySQL Database (wanderwallet_db)"]
        direction LR
        T_Users[("users\n─────────\nuser_id · username\nemail · password\nrole · timestamps")]
        T_Trips[("trips\n─────────\ntrip_id · user_id\ntrip_name · destination\nstart_date · end_date")]
        T_Budgets[("budgets\n─────────\nbudget_id · trip_id\ntotal_budget\nremaining_budget")]
        T_Expenses[("expenses\n─────────\nexpense_id · trip_id\ncategory_id · amount\ndescription · date")]
        T_Categories[("categories\n─────────\ncategory_id\ncategory_name\n(Food · Transport\nHotel · Shopping\nActivities)")]
    end

    %% ─── External Services ────────────────────────────────────
    subgraph External ["External Services"]
        OpenRouter["OpenRouter API\n─────────────\nAI Budget Analysis\n& Recommendations\n(GPT model)"]
        Bootstrap_CDN["Bootstrap CDN\n(CSS + Icons)"]
    end

    %% ─── Config ───────────────────────────────────────────────
    subgraph Config [".env Configuration"]
        EnvVars["DB_HOST · DB_USER\nDB_PASSWORD · DB_NAME\nSECRET_KEY\nOPENROUTER_API_KEY"]
    end

    %% ─── Connections ──────────────────────────────────────────
    User -->|"HTTPS Requests"| Presentation
    Admin -->|"HTTPS Requests"| Presentation

    Presentation <-->|"Render / Form Submit"| Application
    Bootstrap_CDN -.->|"CDN Assets"| Presentation

    Auth <-->|"Read / Write"| T_Users
    TripMgmt <-->|"Read / Write"| T_Trips
    TripMgmt <-->|"Read / Write"| T_Budgets
    ExpenseMgmt <-->|"Read / Write"| T_Expenses
    ExpenseMgmt -->|"Read"| T_Categories
    Reports -->|"Read"| T_Trips
    Reports -->|"Read"| T_Expenses
    Reports -->|"Read"| T_Budgets
    Home -->|"Read"| T_Trips
    Home -->|"Read"| T_Expenses

    R_AI <-->|"REST API\n(OPENROUTER_API_KEY)"| OpenRouter

    Config -.->|"python-dotenv"| Application

    %% ─── Styling ──────────────────────────────────────────────
    classDef layer fill:#1e3a5f,stroke:#0ea5e9,color:#fff
    classDef db fill:#1a4731,stroke:#22c55e,color:#fff
    classDef external fill:#4a1942,stroke:#f59e0b,color:#fff
    classDef config fill:#3b2a00,stroke:#f59e0b,color:#fff
    classDef actor fill:#1d4ed8,stroke:#93c5fd,color:#fff

    class Presentation,Application layer
    class T_Users,T_Trips,T_Budgets,T_Expenses,T_Categories db
    class OpenRouter,Bootstrap_CDN external
    class EnvVars config
    class User,Admin actor
```

---

## Component Breakdown

### Presentation Layer
| Component | Technology | Role |
|-----------|-----------|------|
| HTML Templates | Jinja2 (9 files) | Server-side rendered views |
| UI Framework | Bootstrap 5.3.2 | Responsive layout & components |
| Icons | Bootstrap Icons 1.11.3 | UI iconography |
| Custom Styles | CSS (`style.css`, 7.7 KB) | Brand colours & overrides |

### Application Layer (Flask — `app.py`)
| Module | Routes | Responsibility |
|--------|--------|---------------|
| Authentication | `/login`, `/register`, `/logout` | Session-based auth (Werkzeug hashing) |
| Dashboard | `/` | Overview stats, trip list, expense log |
| Trip Management | `/add-trip`, `/edit-trip`, `/delete-trip` | CRUD for trips & linked budgets |
| Expense Management | `/add-expense`, `/update-expense`, `/delete-expense` | CRUD for expenses |
| Reports | `/report/monthly`, `/report/budget`, `/report/category`, `/report/remaining`, `/report/user-spending` | Aggregated data views |
| AI Insights | `/ai-insights` | OpenRouter API call → JSON response |

### Data Layer (MySQL — `wanderwallet_db`)
| Table | Key Relationships |
|-------|-------------------|
| `users` | Root entity; owns trips |
| `trips` | Belongs to user; has one budget |
| `budgets` | One-to-one with trips; tracks remaining |
| `expenses` | Belongs to trip & category |
| `categories` | Lookup table (5 predefined types) |

### External Services
| Service | Purpose | Integration |
|---------|---------|-------------|
| OpenRouter API | AI-powered spending analysis | `requests` HTTP POST from `/ai-insights` |
| Bootstrap CDN | UI framework assets | `<link>` tag in `base.html` |

---

## Data Flow — Typical User Journey

```mermaid
sequenceDiagram
    actor U as User
    participant B as Browser
    participant F as Flask (app.py)
    participant DB as MySQL
    participant AI as OpenRouter API

    U->>B: Opens WanderWallet URL
    B->>F: GET /login
    F->>B: Render login.html

    U->>B: Submit credentials
    B->>F: POST /login
    F->>DB: SELECT user WHERE username=?
    DB-->>F: User record
    F-->>B: Redirect → / (Dashboard)

    U->>B: Create new trip
    B->>F: POST /add-trip
    F->>DB: INSERT INTO trips + budgets
    DB-->>F: OK
    F-->>B: Redirect → /

    U->>B: Add expense to trip
    B->>F: POST /add-expense
    F->>DB: INSERT INTO expenses
    F->>DB: UPDATE budgets SET remaining_budget
    DB-->>F: OK
    F-->>B: Redirect → /

    U->>B: View AI Insights
    B->>F: GET /ai-insights
    F->>DB: SELECT expenses, budgets (aggregated)
    DB-->>F: Spending data
    F->>AI: POST /chat/completions (OpenRouter)
    AI-->>F: AI analysis JSON
    F-->>B: JSON response → rendered in dashboard
```

---

## Deployment Topology

```mermaid
graph LR
    Dev["Developer Machine\n(localhost:5000)\n───────────────\n• Python 3.13 + venv\n• Flask dev server\n• MySQL (local)\n• .env secrets"]

    style Dev fill:#1e3a5f,stroke:#0ea5e9,color:#fff
```

> **Current state**: Local development only — no production deployment, Docker, or cloud infrastructure configured.
