FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# System packages: build-essential + libpq-dev are needed for psycopg2 to compile;
# curl is handy for healthchecks.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install PyTorch CPU-only first — this is ~150 MB instead of ~750 MB.
# Doing it before requirements.txt means pip won't re-resolve torch later.
RUN pip install --no-cache-dir torch \
    --index-url https://download.pytorch.org/whl/cpu

# Install the rest of the Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download NLTK data at build time so the first chat request doesn't hang
RUN python -c "import nltk; \
    nltk.download('wordnet', quiet=True); \
    nltk.download('averaged_perceptron_tagger_eng', quiet=True); \
    nltk.download('omw-1.4', quiet=True)"

# Copy the project (including the vendored ml/ folder with the SGM weights)
COPY . .

# Collect static files (admin UI css/js etc.) — `|| true` so the build doesn't
# fail in environments that don't have STATIC_ROOT configured yet.
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

# Gunicorn is the production WSGI server. 3 workers is a reasonable default for
# a small Azure Container App (1 vCPU). Bump it up if you upsize the container.
CMD ["gunicorn", "muayien_core.wsgi:application", \
    "--bind", "0.0.0.0:8000", \
    "--workers", "3", \
    "--timeout", "60", \
    "--access-logfile", "-", \
    "--error-logfile", "-"]