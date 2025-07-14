# manage.py

import subprocess

import typer
from vod_pipeline.celery_app import app as celery_app
from vod_pipeline.workflows.vod_ingest_flow import run_vod_ingest_workflow

cli = typer.Typer(help="VOD Pipeline Management CLI")


@cli.command("run-workflow")
def run_workflow(source_url: str):
    """Trigger a full ingest+publish workflow."""
    result = run_vod_ingest_workflow(source_url)
    typer.echo(f"Triggered VOD ingest flow. Task ID: {result.id}")


@cli.command("worker")
def start_worker():
    """Start a Celery worker."""
    typer.echo("Starting Celery worker...")
    subprocess.run(
        ["celery", "-A", "vod_pipeline.celery_app", "worker", "--loglevel=info"]
    )


@cli.command("beat")
def start_beat():
    """Start a Celery beat scheduler."""
    typer.echo("Starting Celery beat...")
    subprocess.run(
        ["celery", "-A", "vod_pipeline.celery_app", "beat", "--loglevel=info"]
    )


@cli.command("status")
def worker_status():
    """Ping Celery workers."""
    result = celery_app.control.ping()
    if result:
        typer.echo(f"Workers active: {result}")
    else:
        typer.echo("No Celery workers responding.")


@cli.command("replay")
def replay_task(task_id: str):
    """Manually retry a given task (if args are preserved)."""
    typer.echo(f"Attempting to retry task {task_id}...")
    # Assumes retryable task args exist (depends on backend)
    celery_app.control.revoke(task_id, terminate=True)
    # Implement replay logic or pull from DB/audit trail


if __name__ == "__main__":
    cli()
