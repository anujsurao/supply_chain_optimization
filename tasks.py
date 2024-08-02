from celery import Celery
from optimization import optimize_supply_chain

app = Celery('tasks', broker='redis://localhost:6379/0')

@app.task
def scheduled_optimization():
    return optimize_supply_chain()
