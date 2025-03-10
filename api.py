import sys
import uvicorn
import click
from fastapi import FastAPI
from app.routes import upload, rag, add_url

app = FastAPI()

app.include_router(upload.router)
app.include_router(rag.router)
app.include_router(add_url.router)

@click.group()
def main():
    """Main entry point to launch either the CLI or the API."""
    pass

@main.command("start")
@click.option("--port", default = 5054, help="Port where to launch the local server")
def api(port: str):
    """Starts the FastAPI application."""
    uvicorn.run("api:app", host="0.0.0.0", port=port, reload=True)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main()  # Run the selected command (CLI or API)
    else:
        click.echo("Please specify a mode: 'cli' or 'api'")
        click.echo("Example: python main.py api")
