from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "NIC AWS Fargate RDS App"}


@app.get("/health")
def health_check():
    return {"status": "ok"}