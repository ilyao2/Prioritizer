"""Точка входа"""

import uvicorn
from fastapi import FastAPI

from idea import router as idea_router
from metric import router as metric_router
from rate import router as rate_router

app = FastAPI()
app.include_router(idea_router)
app.include_router(metric_router)
app.include_router(rate_router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
