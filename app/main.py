from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import books, users

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(users.router)

@app.get("/")
def read_items():
    return {"message": "Hello World"}