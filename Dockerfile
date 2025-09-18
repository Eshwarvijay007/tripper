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

# Frontend dependencies (use npm ci if lockfile exists)
COPY tripplanner/package*.json tripplanner/
RUN bash -lc 'cd tripplanner && (npm ci || npm install)'

# Copy source
COPY app/ app/
COPY tripplanner/ tripplanner/

# Startup script to run both frontend and backend
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

# Expose common dev ports
EXPOSE 8000 5173 3000

# Defaults (can be overridden at runtime)
ENV BACKEND_HOST=0.0.0.0 \
    BACKEND_PORT=8000

CMD ["/usr/local/bin/start.sh"]
