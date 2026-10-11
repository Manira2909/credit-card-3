from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, auth, cards, payments
from .dashboard import router as dashboard_router
from routers.statement import router as statement_router

# Single FastAPI instance - IMPORTANT
app = FastAPI(
    title="Credit Card Payment System API",
    description="Secure fintech API with JWT, no CVV storage, encrypted cards",
    version="1.0.0"
)

# Create tables
models.Base.metadata.create_all(bind=database.engine)

# CORS - Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers - Ellam oru idathula
app.include_router(auth.router, prefix="/api", tags=["Auth"])
app.include_router(cards.router, prefix="/api", tags=["Cards"])
app.include_router(payments.router, prefix="/api", tags=["Payments"])
app.include_router(dashboard_router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(statement_router, prefix="/api", tags=["Statement"])

@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Credit Card Payment API is running",
        "docs": "/docs",
        "version": "1.0.0",
        "security": ["JWT mandatory", "No CVV storage", "Bcrypt passwords", "Luhn validation"]
    }

@app.get("/health", tags=["Root"])
def health():
    return {"status": "ok"}