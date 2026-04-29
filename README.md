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
git clone <repository-url>
cd beagle-ir
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

## Project Structure

```
├── backend_controller   # Orchestrates system workflows and coordinates module interactions
├── corpus               # Storage for raw scientific documents
├── data_ingestion       # Crawling, scraping, and preprocessing pipelines for data acquisition
├── frontend             # Streamlit-based user interface and visualization layer
├── indexing             # Construction and persistence of sparse (BM25F) and dense indexes
├── query_expansion      # Techniques for enhancing queries using dense representations
├── rag                  # Retrieval-Augmented Generation pipeline (context building + LLM prompting)
├── ranking              # Result ranking, scoring, and fusion strategies
├── recommender          # Document recommendation based on historical interactions
├── retrieval            # Core retrieval logic (sparse and dense retrievers)
├── utils                # Shared utilities and common processing functions
├── web_search           # External search integration
```
