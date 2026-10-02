# CortexONE ERP

**CortexONE** is a powerful, fully integrated Enterprise Resource Planning (ERP)
platform built for modern businesses — from manufacturing and distribution to
professional services and retail.

> CortexONE is built on the open-source Odoo Community framework, licensed under LGPL v3.
> See [NOTICE.md](NOTICE.md) for details.

---

## Features

- **Financial Management** — Accounting, invoicing, expense tracking
- **Sales & CRM** — Opportunity pipeline, quotations, sales orders
- **Inventory** — Multi-warehouse, stock moves, barcode scanning
- **Manufacturing** — MRP, work orders, quality control
- **Purchasing** — Vendor management, RFQs, purchase orders
- **Human Resources** — Employees, attendance, leave management
- **Projects & Timesheets** — Task management, time tracking
- **REST API** — Full `/api/v1/` REST API with token authentication

---

## Quick Start (Docker)

### Prerequisites

- Docker 24+ and Docker Compose v2
- A domain pointed to your server (DNS A records)
- SSL certificates (Let's Encrypt recommended)

### 1. Clone & configure

```bash
git clone https://github.com/VinaySawarkar1/CortexONE.git
cd CortexONE
cp .env.example .env
# Edit .env and fill in all CHANGE_ME values
nano .env
```

### 2. Add SSL certificates

```bash
mkdir -p nginx/ssl
# Copy your certificates:
cp /path/to/cert.pem nginx/ssl/cortexone.crt
cp /path/to/key.pem  nginx/ssl/cortexone.key
cp /path/to/cert.pem nginx/ssl/cortexonestage.crt
cp /path/to/key.pem  nginx/ssl/cortexonestage.key
```

### 3. Start the stack

```bash
docker compose up -d
```

### 4. Initialize database

```bash
docker compose exec app cortexone \
  --database cortexone_prod \
  --init base,web,mail,contacts,sale,account,cortex_branding,cortex_api \
  --stop-after-init
```

### 5. Access

- **Production**: https://cortexone.cortexaitechnologies.com
- **Staging**: https://cortexonestage.cortexaitechnologies.com
- **Default login**: admin / (your `CORTEXONE_ADMIN_PASSWD`)

---

## Branch Workflow

See [BRANCHING.md](BRANCHING.md) for the complete Git workflow.

| Branch | Purpose | Auto-deploys to |
|--------|---------|----------------|
| `odoo_core` | Pristine upstream Odoo 18.0 | — |
| `develop` | Integration | Staging |
| `production` | Stable releases | Production |
| `feature/*` | Feature development | — |

---

## Custom Addons

| Addon | Description |
|-------|-------------|
| `cortex_branding` | White-label branding — logo, colours, email layouts |
| `cortex_api` | REST API at `/api/v1/` — auth, partners, products, sales, invoices |

---

## API Documentation

See [docs/openapi.yaml](docs/openapi.yaml) for the full OpenAPI 3.1 specification.

**Quick example:**

```bash
# Get an API key
curl -X POST https://cortexone.cortexaitechnologies.com/api/v1/auth/token \
  -H "Content-Type: application/json" \
  -d '{"login": "admin", "password": "yourpassword", "db": "cortexone_prod"}'

# List partners
curl https://cortexone.cortexaitechnologies.com/api/v1/partners \
  -H "X-CortexONE-API-Key: <your-key>"
```

---

## Legal

- [NOTICE.md](NOTICE.md) — Open-source notice
- [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) — Third-party licenses
- [LICENSE](LICENSE) — LGPL-3.0

---

## Support

- **Email**: support@cortexaitechnologies.com
- **Website**: https://cortexaitechnologies.com
