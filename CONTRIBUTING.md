# Contribution Guidelines

Thank you for your interest in contributing to the **Corrective RAG** project! Your help is greatly appreciated. This guide explains how to contribute effectively.

## Getting Started

### Fork and Clone

1. Fork the repository.
2. Clone your fork locally:

```bash
git clone git@github.com:<your-username>/corrective_rag.git
cd corrective_rag
```

### Install Dependencies

Install dependencies using Pipenv:

```bash
make install
make shell
```

## Contribution Workflow

Follow this workflow for your contributions:

1. **Create a new branch** from the main branch:

```bash
git checkout -b feature/my-feature-name
```

2. **Make your changes**, and test them locally.

3. **Format your code** using Black:

```bash
make format
```

3. **Check code quality** using linting tools:

```bash
make lint
```

4. **Run tests**:

```bash
make test
```

3. **Commit your changes** clearly and concisely:

```bash
git commit -m "feat: Add description of the new feature"
```

4. **Push your branch** to your forked repository:

```bash
git push origin feature/my-feature-name
```

5. **Open a Pull Request (PR)** against the main branch of this repository.

## Code Standards

- Format code with **Black**:

```bash
make format
```

- **Lint your code** with Flake8:

```bash
make lint
```

- Follow existing coding patterns and conventions.

## Reporting Issues

- Clearly describe the issue.
- Include steps to reproduce it.
- Mention your environment and software version if relevant.

## Feature Requests

- Clearly describe the feature and its potential benefits.
- Suggest a practical use-case for this feature.

## Pull Request Reviews

Your pull request will be reviewed promptly. Be prepared to discuss your changes and make adjustments if necessary.

## Community Conduct

Please be respectful, inclusive, and constructive in your interactions.

Thank you for helping improve the **Corrective RAG** project!
