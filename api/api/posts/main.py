from fastapi import FastAPI
import uvicorn
import model
import db
from fastapi.middleware.cors import CORSMiddleware
from post_routes import router as auth_router

app = FastAPI(
    title="API"
)
origins = [
    "http://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

model.Base.metadata.create_all(bind=db.engine)


app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app=app, host='0.0.0.0', port=int(8001))
