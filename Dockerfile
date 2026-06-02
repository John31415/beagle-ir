FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501

COPY requirements.txt .
RUN pip install --no-cache-dir --timeout 1000 --retries 10 -r requirements.txt
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('multi-qa-mpnet-base-dot-v1')"

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "frontend/interface.py", "--server.address=0.0.0.0", "--server.port=8501"]