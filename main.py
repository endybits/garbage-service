from fastapi import FastAPI


app = FastAPI()

@app.get('/')
async def home():
    return {"greeting": "Hello Garbage Service API"}