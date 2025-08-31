import typer
import subprocess
import os

app = typer.Typer(help="CLI for managing the FastAPI + Celery project")
env_mode = os.environ.get("ENVIRONMENT", "local")
is_dev = env_mode == "development" or env_mode == "local"

# Command definitions
API_CMD = ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
DEV_CMD = ["fastapi", "dev", "main.py"]
WORKER_CMD = [
    "celery",
    "-A",
    "app.worker.celery_app",
    "worker",
    "--loglevel=info",
    "--pool=solo",
]
BEAT_CMD = ["celery", "-A", "app.worker.celery_app", "beat", "--loglevel=info"]
FLOWER_USER = os.environ.get("FLOWER_USER")
FLOWER_PASS = os.environ.get("FLOWER_PASS")
FLOWER_PORT = os.environ.get("FLOWER_PORT", "5555")
FLOWER_ROUTE = os.environ.get("FLOWER_ROUTE", "/worker")
FLOWER_ADDRESS = os.environ.get("FLOWER_ADDRESS", "0.0.0.0")
FLOWER_CMD = [
    "celery",
    "-A",
    "app.worker.celery_app",
    "flower",
    f"--basic_auth={FLOWER_USER}:{FLOWER_PASS}",
    f"--port={FLOWER_PORT}",
    f"--address={FLOWER_ADDRESS}",
    f"--url_prefix={FLOWER_ROUTE}",
]


@app.command()
def api():
    """Run FastAPI server"""
    subprocess.run(API_CMD)


@app.command()
def dev():
    """Run FastAPI in development mode with auto-reload"""
    typer.echo("🚀 Starting FastAPI dev server...")
    subprocess.run(DEV_CMD)


@app.command()
def worker():
    """Run Celery worker"""
    typer.echo("👷 Starting Celery worker...")
    subprocess.run(WORKER_CMD)


@app.command()
def beat():
    """Run Celery beat"""
    typer.echo("🕰️ Starting Celery beat...")
    subprocess.run(BEAT_CMD)


@app.command()
def flower():
    """Run Flower to monitor Celery tasks (with basic auth)"""
    typer.echo(
        f"🌸 Starting Flower monitoring tool with basic auth ({FLOWER_USER}:{FLOWER_PASS})..."
    )
    subprocess.run(FLOWER_CMD)


@app.command()
def all():
    """Run FastAPI dev, Celery worker, beat, and Flower together"""
    typer.echo("🚀 Starting FastAPI, Celery worker, beat, and Flower...")
    start_app = DEV_CMD if is_dev else API_CMD
    processes = [
        start_app,
        WORKER_CMD,
        BEAT_CMD,
    ]
    procs = [subprocess.Popen(p) for p in processes]
    try:
        for p in procs:
            p.wait()
    except KeyboardInterrupt:
        typer.echo("🛑 Shutting down...")
        for p in procs:
            try:
                p.terminate()
            except Exception:
                pass
        for p in procs:
            try:
                p.wait(timeout=5)
            except Exception:
                pass


if __name__ == "__main__":
    app()
