from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router

from app.api.auth import router as admin_auth_router

from app.api.customer_auth import router as customer_auth_router



app = FastAPI(title="Sellince Agent API")



app.add_middleware(

    CORSMiddleware,

    allow_origins=["http://localhost:5173", "http://localhost:5174"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)



app.include_router(admin_auth_router, prefix="/api/v1/auth", tags=["Admin Auth"])

app.include_router(customer_auth_router, prefix="/api/v1/customer-auth", tags=["Customer Auth"])

# Changed prefix from "/api/v1/chat" to "/api/v1" to prevent doubled paths

app.include_router(chat_router, prefix="/api/v1", tags=["Chat"])