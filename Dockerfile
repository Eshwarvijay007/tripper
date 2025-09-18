FROM node:20-bookworm

# Install Python and pip
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src

# Backend dependencies in an isolated venv (avoid PEP 668)
COPY app/requirements.txt app/requirements.txt
RUN python3 -m venv /opt/venv
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install --no-cache-dir -r app/requirements.txt

# Prepare and build frontend (Vite)
COPY tripplanner/package*.json tripplanner/
RUN bash -lc 'cd tripplanner && (npm ci || npm install)'
COPY tripplanner/ tripplanner/
RUN bash -lc 'cd tripplanner && npm run build && mkdir -p /opt/frontend && cp -a dist/. /opt/frontend/'

# Copy backend source
COPY app/ app/

# Startup script to run backend (serves static build)
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Expose dev ports locally; Cloud Run injects $PORT
EXPOSE 8000 5173 3000

# Defaults (override at runtime as needed)
ENV BACKEND_HOST=0.0.0.0 \
    BACKEND_PORT=8000 \
    FRONTEND_DIST=/opt/frontend

CMD ["/usr/local/bin/start.sh"]
