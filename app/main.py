from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import books, users, auther, publisher, auth

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(users.router)
app.include_router(auther.router)
app.include_router(publisher.router)

@app.get("/")
def read_items():
    return {"message": "Hello World"}