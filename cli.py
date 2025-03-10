import click
import logging
from app.loader_factory import LoaderFactory
from utils.tiktoken_spliter import TiktokenSpliter
from repository.article_repository import ArticleRepository
from workflow.graph import run_workflow  # Import workflow logic

# Initialize dependencies
article_repository = ArticleRepository()
spliter = TiktokenSpliter()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@click.group()
def cli():
    """
    CLI for managing various tasks:
    - add-source: Add and index a new data source.
    - run-rag: Execute the RAG workflow.
    """
    pass


@cli.command("add-source")
@click.option("--source-type", type=click.Choice(["url", "pdf"]), default="url", help="Type of source (URL, PDF).")
@click.option("--value", multiple=True, required=True, help="List of URLs or a single PDF file path.")
def add_source(source_type: str, value: tuple[str]):
    """
    Adds a data source (URL, PDF, etc.) and indexes it in the vector store.

    Args:
        source_type (str): The type of source ("url" or "pdf").
        value (tuple[str]): URLs or file paths.
    """
    if not value:
        click.echo("Error: No source provided.", err=True)
        return

    try:
        # 1) Create the loader using the factory
        if source_type == "url":
            loader = LoaderFactory.create_loader("url", urls=value)
        elif source_type == "pdf":
            loader = LoaderFactory.create_loader("pdf", file_path=value[0])
        else:
            click.echo("Error: Unsupported source type.", err=True)
            return

        # 2) Load documents
        docs = loader.load()
        click.echo(f"✅ Loaded {len(docs)} documents from {source_type}.")

        # 3) Split documents into smaller chunks
        docs_splits = spliter.split(docs)
        click.echo(f"✅ After splitting, {len(docs_splits)} documents available.")

        # 4) Store in the vector database
        article_repository.add(docs_splits)
        click.echo("✅ Source successfully indexed!")
    
    except Exception as e:
        logging.error(f"Error while adding source: {e}")
        click.echo(f"❌ Failed to index source: {e}", err=True)


@cli.command("run-rag")
@click.option("--question", prompt="Your question", help="The question to ask the RAG workflow.")
def run_rag(question: str):
    """
    Runs the RAG workflow: retrieve, grade, generate.

    Args:
        question (str): The input question.
    """
    try:
        retriever = article_repository
        final_state = run_workflow(question, retriever)
        click.echo(f"💡 Answer: {final_state['generation']}")
        click.echo(f"🔄 Steps followed: {final_state['steps']}")
    
    except Exception as e:
        logging.error(f"Error while running RAG workflow: {e}")
        click.echo(f"❌ Failed to run RAG workflow: {e}", err=True)


# Entry point
if __name__ == "__main__":
    cli()
