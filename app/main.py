import uvicorn
from fastapi import FastAPI
from app.controllers.url_analysis_controller import url_analysis_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(url_analysis_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
