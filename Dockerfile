#immagine ufficiale su base debian slim
FROM python:3.12-slim

#metadati
LABEL org.opencontainers.image.title="finuntius" \
      org.opencontainers.image.description="CLI Terminal for real-time financial news via Finnhub API" \
      org.opencontainers.image.authors="g-projectech" \
      org.opencontainers.image.source="https://github.com/g-projectech/finuntius" \
      org.opencontainers.image.licenses="AGPL-3.0-or-later"

# ottimizza runtime .py
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

#copio ciò che serve per la build del pacchetto
COPY pyproject.toml README.md ./
COPY LICENSE* ./
COPY src/ ./src/

RUN pip install --no-cache-dir .

# crea user linux non privilegiato FINUNTIUS
RUN useradd --create-home --shell /bin/bash finuntius
USER finuntius
WORKDIR /home/finuntius

# sopravvivenza API key al riavvio del container
VOLUME ["/home/finuntius/.config/finuntius"]

ENTRYPOINT ["finuntius"]
CMD ["--help"]