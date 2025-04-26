from fastapi import FastAPI, Query
from model import evaluate
app = FastAPI()

@app.get("/echo")
async def echo_text(text: str = Query(...)):
    res = evaluate(text)
    return {"received_text": text,
            "out":res}
