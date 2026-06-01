# beagle-ir
Beagle-IR is a modular scientific Information Retrieval system designed to search, retrieve, and verify scientific content across multiple domains.  It helps users find research papers, while also assisting in fact-checking or debunking scientific claims.

> [!IMPORTANT]
> The **beagle-ir** repository uses [**Git LFS**](https://git-lfs.github.com/) (Large File Storage) to manage large files such as document corpora, indexes, and databases. Some files in this project may exceed standard Git size limits.

## Index

- [Index](#index)
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Project Structure](#project-structure)

## Overview

Beagle-IR is built to support scientific search and verification workflows through a modular pipeline. The system is designed to help users explore scientific documents, retrieve relevant information efficiently, and contrast claims against available evidence.

The project is intended for use cases such as:

- Searching for scientific papers and related documents.
- Retrieving relevant passages from a document collection.
- Supporting fact-checking tasks with evidence-based retrieval.
- Assisting in the debunking or validation of scientific claims.

## Features

- Modular architecture for scientific information retrieval.
- Fast document search and retrieval.
- Interface built with Streamlit.
- Designed to support scientific fact-checking workflows.
- Easy to extend with new retrieval, ranking, or verification components.

## Requirements

Before running the project, make sure you have:

- Python installed
- `pip` available in your environment
- The dependencies listed in `requirements.txt`

## Installation

Clone the repository:

```bash
git clone https://github.com/John31415/beagle-ir.git
cd beagle-ir
```

Environment Setup

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

Install the project dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

To start the Streamlit frontend, run:

```bash
streamlit run frontend/interface.py
```

After executing the command, Streamlit will start a local server and open the application in your browser.  
By default, the app is available at: http://localhost:8501

## Advanced Feature: Corpus Analyzer (Visualizations)

The project includes a specialized script, `corpus_analyzer.py` (located in `pdf_stats`), which generates word clouds and visual statistics from the processed documents. 

Because the `wordcloud` library can be heavy and requires specific system C-compilers to build during the Docker installation, it is commented out by default to keep the core image lightweight.

If you want to use this analytics feature, follow these steps **before** building the Docker image:

1. Open your `requirements.txt` file in the root directory.
2. Locate the `# wordcloud` line and **uncomment** it (remove the `#`).
3. Save the file.
4. Install:

```bash
pip install -r requirements.txt
```

## Project Structure

```
├── backend_controller   # Orchestrates system workflows and coordinates module interactions
├── corpus               # Storage for raw scientific documents
├── data_ingestion       # Crawling, scraping, and preprocessing pipelines for data acquisition
├── docs                 # PDF and LaTeX, project documentation
├── frontend             # Streamlit-based user interface and visualization layer
├── indexing             # Construction and persistence of sparse (BM25F) and dense indexes
├── pdf_stats            # Corpus analyzer, general structure of PDF files
├── query_expansion      # Techniques for enhancing queries using dense representations
├── rag                  # Retrieval-Augmented Generation pipeline (context building + LLM prompting)
├── ranking              # Result ranking, scoring, and fusion strategies
├── recommender          # Document recommendation based on historical interactions
├── retrieval            # Core retrieval logic (sparse and dense retrievers)
├── utils                # Shared utilities and common processing functions
├── web_search           # External search integration
```
