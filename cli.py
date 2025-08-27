import typer
import subprocess
import os

app = typer.Typer(help="CLI for managing the FastAPI + Celery project")
env_mode = os.environ.get("ENVIRONMENT", "local")
is_dev = env_mode == "development" or env_mode == "local"

@app.command()
def api():
    """Run FastAPI server"""
    subprocess.run(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])


@app.command()
def dev():
    """Run FastAPI in development mode with auto-reload"""
    typer.echo("🚀 Starting FastAPI dev server...")
    subprocess.run(["fastapi", "dev", "main.py"])


@app.command()
def worker():
    """Run Celery worker"""
    typer.echo("👷 Starting Celery worker...")
    subprocess.run(
        [
            "celery",
            "-A",
            "app.worker.celery_app",
            "worker",
            "--loglevel=info",
            "--pool=solo",
        ]
    )


@app.command()
def flower():
    """Run Flower to monitor Celery tasks"""
    typer.echo("🌸 Starting Flower monitoring tool...")
    subprocess.run(["celery", "-A", "app.worker.celery_app", "flower"])


@app.command()
def all():
    """Run FastAPI dev, Celery worker, and Flower together"""
    typer.echo("🚀 Starting FastAPI, Celery worker, and Flower...")
    start_app = ["fastapi", "dev", "main.py"] if is_dev else ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
    processes = [
        start_app,
        ["celery", "-A", "app.worker.celery_app", "worker", "--loglevel=info", "--pool=solo"],
        ["celery", "-A", "app.worker.celery_app", "flower"],
    ]
    procs = [subprocess.Popen(p) for p in processes]
    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        typer.echo("🛑 Shutting down...")
        for p in procs:
            p.terminate()


if __name__ == "__main__":
    app()
