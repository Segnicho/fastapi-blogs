from fastapi import FastAPI
from src.core.database import init_db
from src.api.v1.router import router
import uvicorn

app = FastAPI(title="Blog API")

@app.on_event("startup")
def on_startup():
    init_db()
    
app.include_router(router)

# if __name__ == "__main__":
#     uvicorn.run(app=app, host="localhost", port=8080)
    