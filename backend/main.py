from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.verify import router as verify_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
   # allow_origins=["http://localhost:3000","https://signature-verifier-sigma.vercel.app/"],  # React frontend
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(verify_router, prefix="/api")
