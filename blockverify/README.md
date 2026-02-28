# 🔗 BlockVerify — Blockchain-Based Certificate Verification System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-4.2-green?style=for-the-badge&logo=django)
![SQLite](https://img.shields.io/badge/SQLite-3-blue?style=for-the-badge&logo=sqlite)
![Blockchain](https://img.shields.io/badge/Blockchain-SHA256-purple?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Gemma_OCR-orange?style=for-the-badge&logo=google)

**A secure, tamper-proof certificate storage and instant verification platform powered by blockchain technology and AI-driven OCR.**

</div>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Architecture Diagram](#-architecture-diagram)
- [How It Works](#-how-it-works)
- [Blockchain Deep Dive](#-blockchain-deep-dive)
- [AI / OCR Engine](#-ai--ocr-engine)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Tech Stack](#-tech-stack)
- [Setup & Installation](#-setup--installation)
- [Usage Guide](#-usage-guide)
- [API Key Configuration](#-api-key-configuration)
- [Security Notes](#-security-notes)
- [Screenshots Flow](#-screenshots-flow)

---

## 🎯 Overview

BlockVerify solves the problem of **fake and tampered academic certificates** by combining:

| Technology | Role |
|---|---|
| **Blockchain** | Immutable ledger storing certificate hashes — impossible to alter retroactively |
| **SHA-256 Hashing** | Generates a unique 64-char fingerprint for every document |
| **AI OCR (Gemma)** | Extracts text from PDF/Image certificates using Google's Gemma AI |
| **Django** | Full-stack web framework with role-based authentication |

### Two Portals:

```
┌─────────────────────────┐    ┌─────────────────────────┐
│    🎓 COLLEGE PORTAL    │    │    🏢 COMPANY PORTAL    │
│                         │    │                         │
│  • Add Students         │    │  • Upload Certificate   │
│  • Upload Certificates  │    │  • Auto OCR + Hashing   │
│  • OCR → Hash → Chain   │    │  • Compare vs Blockchain│
│  • View Blockchain TX   │    │  • VERIFIED / TAMPERED  │
└─────────────────────────┘    └─────────────────────────┘
```

---

## 🏗 Architecture Diagram

```
                    ┌──────────────────────────────────────────────┐
                    │              BLOCKVERIFY SYSTEM               │
                    └──────────────────┬───────────────────────────┘
                                       │
                    ┌──────────────────┴───────────────────────────┐
                    │                                               │
          ┌─────────┴─────────┐                         ┌──────────┴──────────┐
          │  COLLEGE PORTAL   │                         │  COMPANY PORTAL     │
          │  (Upload Flow)    │                         │  (Verify Flow)      │
          └─────────┬─────────┘                         └──────────┬──────────┘
                    │                                               │
                    ▼                                               ▼
          ┌─────────────────┐                           ┌─────────────────────┐
          │ Upload PDF/IMG  │                           │  Upload PDF/IMG     │
          └────────┬────────┘                           └──────────┬──────────┘
                   │                                               │
                   ▼                                               ▼
          ┌─────────────────┐                           ┌─────────────────────┐
          │  Gemma AI OCR   │                           │   Gemma AI OCR      │
          │  Extract Text   │                           │   Extract Text      │
          └────────┬────────┘                           └──────────┬──────────┘
                   │                                               │
                   ▼                                               ▼
          ┌─────────────────┐                           ┌─────────────────────┐
          │  SHA-256 Hash   │                           │   SHA-256 Hash      │
          │  Generation     │                           │   Generation        │
          └────────┬────────┘                           └──────────┬──────────┘
                   │                                               │
                   ▼                                               ▼
          ┌─────────────────┐                           ┌─────────────────────┐
          │  Store on       │◄─────── Compare ─────────►│   Search Blockchain │
          │  BLOCKCHAIN     │                           │   for Matching Hash │
          └────────┬────────┘                           └──────────┬──────────┘
                   │                                               │
                   ▼                                               ▼
          ┌─────────────────┐                  ┌──────────┐  ┌────────────┐
          │  Save TX ID     │                  │ VERIFIED │  │  TAMPERED  │
          │  in Database    │                  │    ✅     │  │    ❌      │
          └─────────────────┘                  └──────────┘  └────────────┘
```

---

## ⚙️ How It Works

### 🎓 College Upload Flow (Step by Step)

```
Step 1: College logs in → Dashboard
Step 2: Adds a Student (Name, ID, Department, Year)
Step 3: Uploads a Certificate (PDF / Image)
         │
         ├── Step 4: File saved to → media/certificates/YYYY/MM/
         │
         ├── Step 5: Gemma AI OCR extracts text from the document
         │           (or Mock OCR if no API key)
         │
         ├── Step 6: SHA-256 hash computed on the raw file bytes
         │           Example: "a3f2b8c9d1e4..."  (64 hex characters)
         │
         ├── Step 7: New Block created on blockchain containing:
         │           {
         │             "certificate_hash": "a3f2b8c9d1e4...",
         │             "student_name": "John Doe",
         │             "student_id": "STU-2026-001",
         │             "certificate_type": "academic",
         │             "institution": "MIT",
         │             "transaction_id": "uuid-xxxx-xxxx"
         │           }
         │
         └── Step 8: Block index + block hash + transaction ID
                     saved to the Certificate record in database
```

### 🏢 Company Verification Flow (Step by Step)

```
Step 1: Company logs in → Dashboard
Step 2: Clicks "Verify Certificate"
Step 3: Uploads the certificate received from a student
         │
         ├── Step 4: Gemma AI OCR extracts text (same engine)
         │
         ├── Step 5: SHA-256 hash computed on the uploaded file
         │           Example: "a3f2b8c9d1e4..."
         │
         ├── Step 6: Blockchain searched for matching hash
         │           blockchain.find_by_hash("a3f2b8c9d1e4...")
         │
         ├── Step 7a: MATCH FOUND → ✅ VERIFIED
         │            Shows: block index, TX ID, student info,
         │                   institution, block hash, timestamps
         │
         └── Step 7b: NO MATCH → ❌ TAMPERED / INVALID
                      The file was modified, forged, or never
                      registered on the blockchain
```

---

## ⛓ Blockchain Deep Dive

### What is a Blockchain?

A blockchain is a **chain of data blocks** linked together using cryptographic hashes. Each block contains:

```
┌─────────────────────────────────────────────────┐
│                  BLOCK #3                        │
├─────────────────────────────────────────────────┤
│  Index:          3                               │
│  Timestamp:      1740700000.123                  │
│  Data:           { certificate_hash, student... }│
│  Previous Hash:  0a8f3b2c... (Block #2's hash)  │
│  Nonce:          42                              │
│  Current Hash:   0d4e7f1a... (this block's hash)│
└─────────────────────────────────────────────────┘
          │
          │ previous_hash links to ▼
┌─────────────────────────────────────────────────┐
│                  BLOCK #2                        │
├─────────────────────────────────────────────────┤
│  Index:          2                               │
│  Current Hash:   0a8f3b2c...                     │
│  Previous Hash:  0bc1d2e3... (Block #1's hash)  │
└─────────────────────────────────────────────────┘
          │
          │ previous_hash links to ▼
┌─────────────────────────────────────────────────┐
│                  BLOCK #1                        │
├─────────────────────────────────────────────────┤
│  Index:          1                               │
│  Current Hash:   0bc1d2e3...                     │
│  Previous Hash:  0000000000... (Genesis)         │
└─────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────┐
│              GENESIS BLOCK #0                    │
│  (First block - created at system startup)       │
│  Previous Hash:  000000000000000...              │
└─────────────────────────────────────────────────┘
```

### How the Hash is Calculated

```python
block_string = JSON({
    index, timestamp, data, previous_hash, nonce
})
current_hash = SHA-256(block_string)
```

**Key Property:** If you change even 1 bit of data, the hash completely changes:

```
Original:  "Certificate of John Doe"  → hash: a3f2b8c9d1e4...
Tampered:  "Certificate of Jane Doe"  → hash: 7b1e9f3a2c8d...  (COMPLETELY DIFFERENT!)
```

### Why It's Secure

```
Tamper Block #2's data
        │
        ▼
Block #2's hash changes → Block #3's previous_hash no longer matches
                                    │
                                    ▼
                          Chain is BROKEN → is_chain_valid() returns False
```

**To tamper with one block, you'd need to recalculate ALL subsequent blocks** — which is computationally impractical.

### Blockchain Class Methods

| Method | Description |
|---|---|
| `add_block(data)` | Creates a new block with certificate data, links it to the chain |
| `get_block(index)` | Retrieves a specific block by its position |
| `find_by_hash(hash)` | Searches for a block containing the given certificate hash |
| `is_chain_valid()` | Validates the entire chain integrity (hash linkage) |
| `get_chain_length()` | Returns total number of blocks |
| `get_latest_block()` | Returns the most recently added block |
| `get_all_blocks()` | Returns all blocks as dictionaries (for explorer) |

### Proof of Work (Educational)

Our blockchain uses a simple proof-of-work: the block hash must start with `"0"`. The nonce is incremented until this condition is met:

```python
while not new_block.current_hash.startswith('0'):
    new_block.nonce += 1
    new_block.current_hash = new_block.calculate_hash()
```

This is a simplified version of what Bitcoin uses (Bitcoin requires many leading zeros).

---

## 🧠 AI / OCR Engine

### What is OCR?

**OCR (Optical Character Recognition)** converts images/PDFs of text into machine-readable text. This is used to:

1. **Extract meaningful content** from uploaded certificates
2. **Store the extracted text** alongside the blockchain record
3. **Display extracted text** in verification results for review

### Gemma AI Integration

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  Upload File │────►│  OCR Service │────►│  Extracted Text  │
│  (PDF/Image) │     │  (Gemma AI)  │     │  "Certificate..."│
└─────────────┘     └──────────────┘     └─────────────────┘
```

### Service Architecture

```python
OCRService (Unified Interface)
    ├── GemmaOCR (Real API)     ← Used when GEMMA_API_KEY is set
    │   └── Uses google.generativeai (Gemini 1.5 Flash)
    │       └── Supports: PDF, PNG, JPG, JPEG, GIF, BMP, WEBP
    │
    └── MockOCR (Development)   ← Used when key is "mock" or missing
        └── Generates deterministic pseudo-text from file bytes
            └── Same file always produces same output (reproducible)
```

### How to Switch Between Mock and Real

| `.env` Setting | Engine Used |
|---|---|
| `GEMMA_API_KEY=mock` | MockOCR (development/testing) |
| `GEMMA_API_KEY=AIzaSy...` | GemmaOCR (real Google AI) |
| Key not set | MockOCR (fallback) |

The switch is **automatic** — just change the `.env` value and restart the server.

### OCR Flow in Code

```python
# In views.py → upload_certificate()
ocr_text = OCRService.extract_text(file_path)

# OCRService auto-selects engine based on GEMMA_API_KEY
# If real key → GemmaOCR.extract_text() → Google Gemini API
# If mock    → MockOCR.extract_text()   → Deterministic output
```

---

## 📂 Project Structure

```
blockverify/
│
├── .env                          # Environment variables (SECRET_KEY, API keys)
├── .env.example                  # Template for .env (safe to commit)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python package dependencies
├── manage.py                     # Django management CLI
│
├── blockverify/                  # 🔧 Django Project Configuration
│   ├── __init__.py
│   ├── settings.py               # All settings (DB, static, media, env vars)
│   ├── urls.py                   # Root URL router → auth + app URLs
│   ├── wsgi.py                   # WSGI entry point
│   └── asgi.py                   # ASGI entry point
│
├── verification/                 # 📋 Main Django Application
│   ├── __init__.py
│   ├── apps.py                   # App configuration
│   ├── models.py                 # 4 models: UserProfile, Student, Certificate, VerificationLog
│   ├── forms.py                  # 5 forms: Registration, Login, Student, Upload, Verify
│   ├── views.py                  # College + Company portal views
│   ├── views_auth.py             # Authentication views (login/register/logout)
│   ├── urls.py                   # App URL patterns (college, company, blockchain)
│   ├── urls_auth.py              # Auth URL patterns (/auth/login, /auth/register)
│   ├── decorators.py             # @role_required('college'|'company') decorator
│   ├── admin.py                  # Django admin panel configuration
│   └── migrations/               # Database migration files
│       └── 0001_initial.py
│
├── blockchain/                   # ⛓ Pure Python Blockchain
│   ├── __init__.py               # Exports Block, Blockchain
│   └── blockchain.py             # Block class + Blockchain class (singleton, thread-safe)
│
├── services/                     # 🧠 Service Layer
│   ├── __init__.py               # Exports OCRService, HashService
│   ├── ocr_service.py            # Gemma AI OCR (real + mock engines)
│   └── hash_service.py           # SHA-256 hashing (file, text, uploaded file)
│
├── templates/                    # 🎨 HTML Templates
│   ├── base.html                 # Base layout (navbar, footer, messages)
│   ├── home.html                 # Landing page with hero + features
│   ├── blockchain_explorer.html  # Visual blockchain chain display
│   ├── auth/
│   │   ├── login.html            # Login form
│   │   └── register.html         # Registration form (role selection)
│   ├── college/
│   │   ├── dashboard.html        # College stats + quick actions
│   │   ├── add_student.html      # Add student form
│   │   ├── student_list.html     # Student table
│   │   ├── student_detail.html   # Student info + certificates
│   │   ├── upload_certificate.html # Certificate upload form
│   │   ├── certificate_list.html  # Certificate table
│   │   └── certificate_detail.html # Full cert + blockchain details
│   └── company/
│       ├── dashboard.html        # Company stats + recent verifications
│       ├── verify.html           # Upload form for verification
│       ├── verification_result.html # VERIFIED / TAMPERED result
│       └── verification_history.html # All past verifications
│
├── static/                       # 📁 Static Assets
│   ├── css/
│   │   └── style.css             # Complete CSS (3D glassmorphism theme)
│   └── js/
│       └── main.js               # Client-side JS (animations, clipboard, drag-drop)
│
├── media/                        # 📎 Uploaded Files (runtime)
│   └── certificates/             # Stored certificate files (by year/month)
│
└── db.sqlite3                    # 🗃 SQLite Database
```

---

## 🗃 Database Schema

```
┌─────────────────────┐       ┌──────────────────────┐
│     User (Django)    │       │     UserProfile      │
├─────────────────────┤       ├──────────────────────┤
│ id                  │◄──┐   │ id                   │
│ username            │   └───│ user (OneToOne)      │
│ email               │       │ role (college/company)│
│ password            │       │ institution_name     │
└─────────────────────┘       │ created_at           │
        │                     └──────────────────────┘
        │ (ForeignKey)
        ▼
┌─────────────────────┐       ┌──────────────────────┐
│      Student        │       │    Certificate       │
├─────────────────────┤       ├──────────────────────┤
│ id                  │◄──────│ student (FK)         │
│ student_id (unique) │       │ uploaded_by (FK→User)│
│ name                │       │ transaction_id (UUID)│
│ email               │       │ title                │
│ department          │       │ certificate_type     │
│ year_of_passing     │       │ certificate_file     │
│ college (FK→User)   │       │ file_hash (SHA-256)  │
│ created_at          │       │ block_index          │
│ updated_at          │       │ block_hash           │
└─────────────────────┘       │ ocr_text             │
                              │ issued_date          │
                              │ created_at           │
                              └──────────────────────┘
                                        │
                                        │ (FK, nullable)
                                        ▼
                              ┌──────────────────────┐
                              │  VerificationLog     │
                              ├──────────────────────┤
                              │ id                   │
                              │ verified_by (FK→User)│
                              │ uploaded_file_name   │
                              │ uploaded_file_hash   │
                              │ status (verified/    │
                              │   tampered/not_found)│
                              │ matched_certificate  │
                              │ block_index          │
                              │ block_hash           │
                              │ transaction_id       │
                              │ ocr_text             │
                              │ verified_at          │
                              └──────────────────────┘
```

---

## 🛠 Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Backend** | Django 4.2 | Web framework, ORM, authentication |
| **Database** | SQLite 3 | Lightweight relational database |
| **Blockchain** | Pure Python | Custom Block + Blockchain classes |
| **Hashing** | `hashlib` (SHA-256) | Deterministic file fingerprinting |
| **AI / OCR** | Google Gemma AI | Text extraction from PDFs/images |
| **Frontend** | HTML5 + CSS3 + JS | 3D glassmorphism UI with animations |
| **Config** | python-dotenv | Environment variable management |
| **Images** | Pillow | Image processing support |

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.10+ installed
- pip package manager

### Step-by-Step

```powershell
# 1. Navigate to the project
cd blockverify

# 2. Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\Activate.ps1      # Windows PowerShell
# source .venv/bin/activate     # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
# Edit .env file with your settings (or use defaults)

# 5. Run database migrations
python manage.py makemigrations verification
python manage.py migrate

# 6. Create admin superuser (optional)
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver
```

### Open in Browser

```
http://127.0.0.1:8000/
```

---

## 📖 Usage Guide

### 1. Register an Account

- Go to `/auth/register/`
- Choose role: **College** or **Company**
- Enter institution name, username, password

### 2. College Workflow

```
Login → Dashboard → Add Student → Upload Certificate → View on Blockchain
```

1. **Add Student**: Fill in student ID, name, department, year
2. **Upload Certificate**: Select student, choose file (PDF/image), add title
3. System automatically: runs OCR → hashes file → stores on blockchain
4. **View Details**: See transaction ID, block hash, OCR text, file hash

### 3. Company Workflow

```
Login → Dashboard → Verify Certificate → View Result
```

1. **Verify**: Upload the certificate received from a student
2. System: runs OCR → hashes file → searches blockchain
3. **Result**: Shows VERIFIED (green) or TAMPERED (red)
4. If verified: shows student name, institution, block details

### 4. Blockchain Explorer

- Available to all logged-in users at `/blockchain/`
- Visual chain display showing all blocks
- Shows hash linkage, data, nonces
- Chain validity status indicator

---

## 🔑 API Key Configuration

### Using Mock OCR (Default)

No configuration needed. The system uses `MockOCR` which generates deterministic text from file bytes. Good for development and testing.

### Using Real Gemma AI

1. Get an API key from [Google AI Studio](https://aistudio.google.com/)
2. Open `.env` file
3. Set: `GEMMA_API_KEY=your_actual_key_here`
4. Install: `pip install google-generativeai`
5. Restart the server

The `OCRService` will automatically detect the real key and switch to the Gemma AI engine.

---

## 🔐 Security Notes

| Feature | Implementation |
|---|---|
| **Authentication** | Django's built-in auth system (bcrypt password hashing) |
| **Role-Based Access** | Custom `@role_required` decorator on every view |
| **CSRF Protection** | Django CSRF middleware + `{% csrf_token %}` in all forms |
| **Secret Key** | Loaded from `.env` (not hardcoded) |
| **File Hashing** | SHA-256 — cryptographically secure, collision-resistant |
| **Blockchain Integrity** | Hash chain validation via `is_chain_valid()` |
| **Singleton Pattern** | One blockchain instance, thread-safe with locks |

---

## 🖼 Screenshots Flow

```
HOME PAGE          →    REGISTER          →    COLLEGE DASHBOARD
┌─────────────┐         ┌─────────────┐        ┌─────────────────┐
│  Hero +     │         │ Username    │        │ Stats Cards     │
│  Features   │         │ Role Select │        │ Quick Actions   │
│  Get Started│────────►│ Password    │───────►│ Recent Activity │
└─────────────┘         └─────────────┘        └────────┬────────┘
                                                        │
    ┌───────────────────────────────────────────────────┘
    ▼
ADD STUDENT        →    UPLOAD CERT        →    CERT DETAIL
┌─────────────┐         ┌─────────────┐        ┌─────────────────┐
│ Student ID  │         │ Select Stud │        │ Certificate Info│
│ Name, Dept  │────────►│ Upload File │───────►│ Blockchain Data │
│ Year        │         │ Title, Type │        │ OCR Output      │
└─────────────┘         └─────────────┘        │ Block Hash      │
                                                └─────────────────┘

COMPANY DASHBOARD  →    VERIFY PAGE        →    RESULT PAGE
┌─────────────┐         ┌─────────────┐        ┌─────────────────┐
│ Verify Stats│         │ Upload Zone │        │ ✅ VERIFIED     │
│ History     │────────►│ Drag & Drop │───────►│ or              │
│ Quick Links │         │ Verify Btn  │        │ ❌ TAMPERED     │
└─────────────┘         └─────────────┘        │ + Block Details │
                                                └─────────────────┘

BLOCKCHAIN EXPLORER
┌─────────────────────────────────────┐
│ Block #3  ← hash: 0d4e7f...        │
│     ↕                               │
│ Block #2  ← hash: 0a8f3b...        │
│     ↕                               │
│ Block #1  ← hash: 0bc1d2...        │
│     ↕                               │
│ Genesis   ← hash: 000000...        │
│                                     │
│ Chain Status: ✅ Valid              │
└─────────────────────────────────────┘
```

---

## 📝 License

This project is built for **educational purposes** as a demonstration of blockchain technology applied to certificate verification.

---

<div align="center">
<strong>Built with ❤️ using Django + Blockchain + AI</strong>
</div>
