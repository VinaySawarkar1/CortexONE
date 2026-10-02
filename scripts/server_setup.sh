#!/bin/bash
# CortexONE Oracle Cloud Server Setup Script
# License: LGPL-3 — https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
#
# Run once on a fresh Oracle Cloud Ubuntu 22.04 instance.
# Usage: sudo bash scripts/server_setup.sh
#
# Prerequisites:
#   - Ubuntu 22.04 LTS (Oracle Cloud ARM or x86)
#   - Ports 22, 80, 443 open in Oracle Security List
#   - GitHub deploy key added (or use HTTPS clone with token)

set -e

CORTEXONE_USER="ubuntu"        # Oracle Cloud default user
APP_DIR="/opt/cortexone"
REPO_URL="https://github.com/VinaySawarkar1/CortexONE.git"

echo "======================================================"
echo " CortexONE Server Setup — Oracle Cloud"
echo "======================================================"

# ── Update system ──────────────────────────────────────────────────────────────
apt-get update && apt-get upgrade -y

# ── Install Docker ─────────────────────────────────────────────────────────────
if ! command -v docker &>/dev/null; then
    echo "Installing Docker..."
    curl -fsSL https://get.docker.com | sh
    usermod -aG docker "$CORTEXONE_USER"
    systemctl enable docker
    systemctl start docker
fi

# ── Install Docker Compose v2 ──────────────────────────────────────────────────
if ! docker compose version &>/dev/null; then
    echo "Installing Docker Compose v2..."
    apt-get install -y docker-compose-plugin
fi

# ── Install Certbot (Let's Encrypt) ───────────────────────────────────────────
if ! command -v certbot &>/dev/null; then
    echo "Installing Certbot..."
    apt-get install -y certbot python3-certbot-nginx
fi

# ── Install Nginx (for certbot) ───────────────────────────────────────────────
if ! command -v nginx &>/dev/null; then
    apt-get install -y nginx
    systemctl enable nginx
fi

# ── Clone/update the repo ─────────────────────────────────────────────────────
if [ ! -d "$APP_DIR/.git" ]; then
    echo "Cloning CortexONE repository..."
    git clone "$REPO_URL" "$APP_DIR"
else
    echo "Repository already exists, skipping clone."
fi

chown -R "$CORTEXONE_USER:$CORTEXONE_USER" "$APP_DIR"

# ── Create ssl directory ──────────────────────────────────────────────────────
mkdir -p "$APP_DIR/nginx/ssl"

# ── Obtain SSL certificates ───────────────────────────────────────────────────
echo ""
echo "======================================================"
echo " NEXT STEPS (manual — run after this script):"
echo "======================================================"
echo ""
echo "1. Copy your .env file to the server:"
echo "   scp -i oci_a1.pem .env ubuntu@130.210.25.122:/opt/cortexone/.env"
echo ""
echo "2. Obtain SSL certificates (run on server):"
echo "   certbot certonly --standalone -d cortexone.cortexaitechnologies.com"
echo "   certbot certonly --standalone -d cortexonestage.cortexaitechnologies.com"
echo "   cp /etc/letsencrypt/live/cortexone.cortexaitechnologies.com/fullchain.pem /opt/cortexone/nginx/ssl/cortexone.crt"
echo "   cp /etc/letsencrypt/live/cortexone.cortexaitechnologies.com/privkey.pem   /opt/cortexone/nginx/ssl/cortexone.key"
echo "   cp /etc/letsencrypt/live/cortexonestage.cortexaitechnologies.com/fullchain.pem /opt/cortexone/nginx/ssl/cortexonestage.crt"
echo "   cp /etc/letsencrypt/live/cortexonestage.cortexaitechnologies.com/privkey.pem   /opt/cortexone/nginx/ssl/cortexonestage.key"
echo ""
echo "3. Start the stack:"
echo "   cd /opt/cortexone && docker compose up -d"
echo ""
echo "4. Initialize the databases:"
echo "   # Production:"
echo "   docker compose exec app cortexone --database cortexone_prod --init base,web,mail,contacts,sale,account,cortex_branding,cortex_api --stop-after-init"
echo "   # Staging:"
echo "   docker compose exec app cortexone --database cortexone_stage --init base,web,mail,contacts,sale,account,cortex_branding,cortex_api --stop-after-init"
echo ""
echo "5. Add GitHub Actions secret:"
echo "   Name:  CORTEXONE_SSH"
echo "   Value: (contents of your oci_a1.pem file)"
echo ""
echo "======================================================"
echo " Server setup complete!"
echo "======================================================"
