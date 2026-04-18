# AI Helpdesk Assistant

## Overview
This project is an AI-powered IT helpdesk assistant that can answer user queries using a knowledge base and automatically create support tickets for unresolved issues.

## Tech Stack
- FastAPI (Backend)
- LangGraph (Agent workflow)
- FAISS (Vector database)
- HuggingFace Transformers (LLM)
- Sentence Transformers (Embeddings)

## Features
- Natural language query handling
- Retrieval-Augmented Generation (RAG)
- Intelligent routing using LangGraph
- Automated ticket fallback system

## How it Works
1. User sends a query
2. RAG retrieves relevant context using FAISS
3. LLM generates response
4. If query is unknown → ticket is created

## Run the Project
```bash
uvicorn app.main:app --reload
