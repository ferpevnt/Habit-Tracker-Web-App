from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.database import engine, Base
from config.config import settings

# Import routers
from routers import auth, categories

# Import limiter
from security.limiter import limiter
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

app = FastAPI(title="API")

# ===== CORS =====
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== Rate limiting =====
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ===== DB tables =====
Base.metadata.create_all(engine)

# ===== Routers =====
app.include_router(auth.router)
app.include_router(categories.router)