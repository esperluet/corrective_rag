# Corrective RAG

This project implements a Retrieval-Augmented Generation (RAG) pipeline with Corrective Retrieval-Augmented Generation (CRAG) enhancements, enabling precise, relevant, and context-aware responses using modern AI and NLP techniques.

## 🚀 Features

- **Corrective RAG Workflow**: Automatically reformulates queries for improved accuracy before web searches.
- **Flexible Data Sources**: Supports indexing and retrieval from URLs and PDF documents.
- **Modular Workflow Integration**: Built using LangChain and LangGraph for easy extensibility.
- **Interactive CLI and API**: Easily manageable via CLI commands and REST APIs (FastAPI).

## Project Structure

```
corrective_rag
├── app
│   ├── routes
│   │   ├── add_url.py
│   │   ├── rag.py
│   │   └── upload.py
│   ├── config.py
│   ├── environment.py
│   └── loader_factory.py
├── generation
│   ├── chains.py
│   ├── llm_manager.py
│   └── prompters.py
├── repository
│   ├── article_repository.py
│   └── base_repository.py
├── retrieval
│   ├── base_loader.py
│   ├── pdf_loader.py
│   └── url_loader.py
├── store
│   ├── base_store.py
│   └── chroma_db_store.py
├── utils
│   ├── base_spliter.py
│   ├── id_utils.py
│   └── tiktoken_spliter.py
├── cli.py
├── api.py
├── Dockerfile
├── Makefile
├── Pipfile
├── Pipfile.lock
└── .env
```

---

## Getting Started

### 🚩 **Prerequisites**

- Python 3.9 or higher
- Docker (optional, for containerized deployment)

---

### 🚀 **Installation**

Install dependencies using `pipenv`:

```bash
make install
make shell
```

### Running the Application

**CLI Mode**  
To add data sources and run queries via command-line interface:

```bash
make run-cli
```

Example:

```bash
python cli.py add-source --source-type url --value "https://example.com"
python cli.py run-rag --question "What is Corrective RAG?"
```

**API Mode (FastAPI)**

Start the API:

```bash
make run-api
```

Access API at:

```
http://localhost:5054/docs
```

### Docker Deployment

Build and launch your containerized application easily:

```bash
make docker-build
make docker-run
```

To persist indexed data with Docker volume:

```bash
docker run -d --name corrective-rag -p 5054:5054 -v /path/to/data:/app/data corrective-rag
```

Stop and remove the container:

```bash
make docker-stop
```

Open an interactive shell in the running Docker container:

```bash
make docker-sh
```

### Infrastructure Management & Maintenance

- **Cleaning temporary files**:

```bash
make clean
```

- **Formatting and Linting** (ensure good code quality):

```bash
make format
make lint
```

### Running Tests

To ensure that your project runs correctly, use:

```bash
make test
```

---

## Contribution Guidelines

We welcome contributions to improve the project. Please follow the instructions in the [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

Licensed under the MIT License.