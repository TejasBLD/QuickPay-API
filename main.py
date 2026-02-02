from fastapi import FastAPI
from app.database import engine,Base
from app.api.auth_routes import router as auth_router
from app.api.auth_routes import router as wallet_routes

Base.metadata.create_all(bind=engine)

app=FastAPI(
    title="QuickPay API",
    description="A  payment gateway api",
    version="1.0"
)
app.include_router(auth_router,prefix="/api")
app.include_router(wallet_routes,prefix="/api")
@app.get("/")
def root():
    return{
        "Message":"Welcome to QuickPay Api"
        ,"status":"Active",
        "docs":"/docs"
    }
@app.get("/health")
def health():
    return{"status":"healthy"}