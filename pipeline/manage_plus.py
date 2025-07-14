# manage.py

import subprocess

import typer
from vod_pipeline.celery_app import app as celery_app
from vod_pipeline.tasks import ingest, metadata, package, publish, upload
from vod_pipeline.workflows.vod_ingest_flow import run_vod_ingest_workflow

cli = typer.Typer(help="VOD Pipeline Management CLI")
task_cli = typer.Typer(help="Run individual pipeline tasks")
cli.add_typer(task_cli, name="task")


@cli.command("run-workflow")
def run_workflow(source_url: str):
    """Trigger full ingest→publish pipeline."""
    result = run_vod_ingest_workflow(source_url)
    typer.echo(f"Workflow started. Root task ID: {result.id}")


@cli.command("worker")
def start_worker():
    """Start Celery worker."""
    subprocess.run(
        ["celery", "-A", "vod_pipeline.celery_app", "worker", "--loglevel=info"]
    )


@cli.command("beat")
def start_beat():
    """Start Celery beat scheduler."""
    subprocess.run(
        ["celery", "-A", "vod_pipeline.celery_app", "beat", "--loglevel=info"]
    )


@cli.command("status")
def worker_status():
    """Ping Celery workers."""
    result = celery_app.control.ping()
    typer.echo(f"Workers active: {result or 'None'}")


@cli.command("replay")
def replay_task(task_id: str):
    """Manually revoke/retry a task."""
    celery_app.control.revoke(task_id, terminate=True)
    typer.echo(f"Task {task_id} revoked. You must manually re-trigger it.")


# ---- Task CLI Subcommands ----


@task_cli.command("ingest")
def run_ingest(source_url: str):
    """Ingest raw media file."""
    result = ingest.ingest_file.delay(source_url)
    typer.echo(f"Ingest task started. Task ID: {result.id}")


@task_cli.command("metadata")
def run_metadata(media_path: str):
    """Extract and normalize metadata."""
    result = metadata.extract_metadata.delay(media_path)
    typer.echo(f"Metadata task started. Task ID: {result.id}")


@task_cli.command("package")
def run_package(media_path: str):
    """Package video into adaptive HLS/DASH."""
    result = package.create_adaptive_package.delay(media_path)
    typer.echo(f"Packaging task started. Task ID: {result.id}")


@task_cli.command("upload")
def run_upload(package_path: str):
    """Upload packaged media to streaming host/CDN."""
    result = upload.upload_to_streaming_host.delay(package_path)
    typer.echo(f"Upload task started. Task ID: {result.id}")


@task_cli.command("publish")
def run_publish(metadata_path: str):
    """Publish metadata to CMS."""
    result = publish.publish_to_cms.delay(metadata_path)
    typer.echo(f"Publishing task started. Task ID: {result.id}")
