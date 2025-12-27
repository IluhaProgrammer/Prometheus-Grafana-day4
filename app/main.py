import time
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import Response
from prometheus_client import Counter, Histogram, generate_latest


app = FastAPI()


http_requests_total = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)


request_duration_seconds = Histogram(
    "request_duration_seconds",
    "Request latency",
    ["endpoint"]
)


@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
        start_time = time.time()
        
        response = await call_next(request)
        
        duration = time.time() - start_time
        
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        request_duration_seconds.labels(
            endpoint=request.url.path
        ).observe(duration)
        
        return response
    

@app.get("/")
def root():
    return {"message": "Hello metrics"}


@app.get("/slow")
def slow():
    time.sleep(1)
    return {"message": "Slow endpoint"}


@app.get("/error")
def error():
    raise HTTPException(500, "Test error")


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")
