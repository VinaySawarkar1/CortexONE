# CortexONE ERP — Dockerfile
# License: LGPL-3 — https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
#
# Base: official Python 3.12 slim (no Odoo branding in image name)
# This image contains unmodified Odoo Community 18.0 source + CortexONE addons.

FROM python:3.12-slim-bookworm AS base

LABEL maintainer="Cortex AI Technologies <devops@cortexaitechnologies.com>" \
      org.opencontainers.image.title="CortexONE ERP" \
      org.opencontainers.image.description="CortexONE ERP built on Odoo Community 18.0 (LGPL-3)" \
      org.opencontainers.image.vendor="Cortex AI Technologies" \
      org.opencontainers.image.licenses="LGPL-3.0"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# ── System dependencies ───────────────────────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    # Build tools
    build-essential \
    # PostgreSQL client
    libpq-dev \
    # Rendering
    wkhtmltopdf \
    # LDAP
    libldap2-dev libsasl2-dev \
    # XML / images
    libxml2-dev libxslt1-dev libjpeg-dev zlib1g-dev \
    # Git (needed for some pip installs)
    git \
    # Utilities
    curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ── System user (non-root) ────────────────────────────────────────────────────
RUN groupadd -r cortexone && useradd -r -g cortexone -d /opt/cortexone cortexone

# ── Python dependencies ───────────────────────────────────────────────────────
WORKDIR /opt/cortexone
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ── Application source ────────────────────────────────────────────────────────
COPY --chown=cortexone:cortexone . /opt/cortexone

# ── CortexONE wrapper script ──────────────────────────────────────────────────
# We do NOT rename odoo-bin (it's the real executable with Odoo copyright).
# We add a thin wrapper called "cortexone" for product-level usage.
COPY --chown=cortexone:cortexone scripts/cortexone /usr/local/bin/cortexone
RUN chmod +x /usr/local/bin/cortexone

# ── Config and data directories ───────────────────────────────────────────────
RUN mkdir -p /etc/cortexone /var/log/cortexone /var/lib/cortexone/filestore \
    && chown -R cortexone:cortexone /etc/cortexone /var/log/cortexone /var/lib/cortexone

# ── Runtime ───────────────────────────────────────────────────────────────────
USER cortexone
EXPOSE 8069 8072

ENTRYPOINT ["cortexone"]
CMD ["--config=/etc/cortexone/cortexone.conf"]
