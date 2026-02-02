# QuickPay API 💳

QuickPay API is a backend wallet and payment system built using **FastAPI** and **SQLAlchemy**.  
It simulates the core backend functionality of a digital payment platform, focusing on authentication, wallet management, and transaction handling.

This project was built as a **backend-focused portfolio project** to practice real-world API development, database modeling, and authentication workflows.

---

## Features

-  JWT-based authentication
-  Secure password hashing using bcrypt
-  User registration & login
-  Automatic wallet creation for users
-  Add money to wallet
-  Transaction history tracking
-  Proper database relationships (User ↔ Wallet ↔ Transactions)
-  Environment-based configuration for secrets

---

## 🛠 Tech Stack

- **Python**
- **FastAPI**
- **SQLAlchemy (ORM)**
- **SQLite** (development database)
- **Pydantic**
- **JWT (JSON Web Tokens)**

---
##  Project Structure
```bash
QuickPay-API/
│
├── app/
│ ├── api/
│ │ ├── auth_routes.py
│ │ └── wallet_routes.py
│ ├── auth.py
│ ├── config.py
│ ├── database.py
│ ├── models.py
│ ├── schemas.py
│ └── main.py
│
├── .gitignore
├── sample.env
└── README.md
```


##  Setup & Run Locally

### Clone the repository

```bash
git clone https://github.com/TejasBLD/QuickPay-API.git
cd QuickPay-API
```
### Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # Windows
```
### Install dependencies
```bash
pip install -r requirements.txt
```
### Run the application
```bash
uvicorn app.main:app --reload
```
## Authentication Flow
```bash
1.Register a new user
2.Login to receive a JWT access token
3.Use the token in request via the header:

Authorization: Bearer <access_token>

4.Access protected wallet and transaction endpoints
```
## API ENDPOINTS

### Authentication
```bash
1.POST /api/auth/register — Register a new user
2.POST /api/auth/login — Login and get JWT token
3.GET /api/auth/me — Get current authenticated user
```
### Wallet
```bash
1.GET /api/wallet — Get wallet details
2.GET /api/wallet/balance — Get wallet balance
3.POST /api/wallet/add-money — Add money to wallet
```
### Learning outcome
```bash
1.Implemented JWT authentication in FastAPI
2.Designed relational database models using SQLAlchemy
3.Built secure password handling using bcrypt
4.Managed environment variables securely using .env
5.Handled real-world ORM bugs and schema mismatches
6.Designed business logic beyond basic CRUD APIs 
```
### Currently working on:
```bash
1.Wallet-to-wallet transfers
2.Transaction rollback handling
3.Alembic database migrations
4.Role-based access control (Admin/User)
5.Unit & integration testing
6.Rate limiting and security hardening
```


