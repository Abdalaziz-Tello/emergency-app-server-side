from fastapi import FastAPI
from database import create_db_and_tables
from router.auth_route import router as auth_router
from router.service_route import router as service_router

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(auth_router)
app.include_router(service_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
