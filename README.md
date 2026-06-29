# AI Knowledge Assistant (RAG System)

## 📖 Overview
A production-ready Retrieval-Augmented Generation (RAG) system that answers questions based on internal documentation.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)
![License](https://img.shields.io/badge/License-MIT-green)

## 🎯 Problem Statement
Teams waste hours searching wikis, PDFs, and Slack history. This system provides instant answers with source citations.


## 🛠️ Tech Stack
- **FastAPI** – API framework
- **LangChain** – RAG orchestration
- **OpenRouter** – LLM (nvidia/nemotron-3-ultra)
- **ChromaDB** – Vector database
- **Redis** – Response caching
- **Docker** – Containerization
- **AWS S3** – Document storage

## 🚀 Quick Start
```bash
git clone https://github.com/yourusername/ai-knowledge-assistant
cd ai-knowledge-assistant/docker
docker-compose up --build
curl http://localhost:8000/health