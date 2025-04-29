from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from metrics_server.metrics import *
from prometheus_client import generate_latest
import uvicorn


app = FastAPI()


@app.get("/metrics")
def get_metrics():
    metrics = generate_latest()
    return PlainTextResponse(content=metrics, media_type="text/plain")

@app.post("/update_metrics/")
def update_metrics(score: int, comments: int):
    SCORE_HISTOGRAM.observe(score)
    COMMENT_HISTOGRAM.observe(comments)
    POSTS_FETCHED_COUNTER.inc()
    return {"status": "success"}
    
@app.post("/set_post_count/{count}")
def set_post_count(count: int):
    POST_COUNT_GAUGE.set(count)
    return {"status": "success", "count": count}

@app.post("/observe_time/{seconds}")
def observe_time(seconds: float):
    FETCH_TIME_SUMMARY.observe(seconds)
    return {"status": "success", "seconds": seconds}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
