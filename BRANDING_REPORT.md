# BRANDING_REPORT.md — CortexONE Whitelabel Audit
<!-- Copyright (C) 2024 Cortex AI Technologies | License: LGPL-3 -->

This report documents the result of scanning the repository for user-visible
references to "Odoo" and classifies each hit as either:

- **(a) User-visible** → Fixed in `addons/cortex_branding` or `addons/cortex_api`
- **(b) Internal technical name** → Left unchanged (renaming breaks the system)

---

## Grep Command Used

```bash
grep -rIil "odoo" addons odoo \
  --include=*.xml --include=*.js --include=*.py \
  --include=*.po --include=*.scss --include=*.html
```

---

## Classification Table

### XML / HTML Files

| File Pattern | Classification | Action |
|---|---|---|
| `addons/*/views/*.xml` — `<string>Odoo</string>` | **(a) User-visible** | Overridden in `cortex_branding` via `inherit_id` templates |
| `addons/web/views/webclient_templates.xml` — `<title>Odoo</title>` | **(a) User-visible** | Overridden: `cortex_login_template.xml` |
| `addons/mail/views/mail_notification_layout.xml` — logo, footer | **(a) User-visible** | Overridden: `cortex_mail_layout.xml` |
| `addons/web/views/external_layout*.xml` — report logo | **(a) User-visible** | Overridden: `cortex_report_layout.xml` |
| `addons/base_setup/views/*.xml` — "Odoo Enterprise" upsell | **(a) User-visible** | Hidden via SCSS + settings view override |
| `addons/*/data/*.xml` — `odoo_bot` display name | **(a) User-visible** | Overridden in `en.po` / `hi.po` |
| `addons/*/views/*.xml` — `href="https://odoo.com"` links | **(a) User-visible** | Removed in `cortex_usermenu.xml` |
| `addons/*/views/*.xml` — XML ID `model="odoo.*"` | **(b) Internal** | Left unchanged — XML IDs are internal references |

### JavaScript Files

| File Pattern | Classification | Action |
|---|---|---|
| `addons/web/static/src/webclient/*.js` — `document.title` containing "Odoo" | **(a) User-visible** | Patched via `cortex_branding.js` MutationObserver |
| `addons/web/static/src/**/*.js` — `this.env.isSmall` / framework internals | **(b) Internal** | Left unchanged |
| `addons/*/static/src/js/*.js` — `odoo.define(...)` call pattern | **(b) Internal** | Left unchanged — module namespace, renaming breaks bundler |

### Python Files

| File Pattern | Classification | Action |
|---|---|---|
| `odoo/*.py` — Python package name `import odoo` | **(b) Internal** | Left unchanged — renaming breaks all imports |
| `addons/*/models/*.py` — `_name = 'sale.order'` etc. | **(b) Internal** | Left unchanged — model names are database keys |
| `addons/mail_bot/models/mail_bot.py` — "OdooBot" display name | **(a) User-visible** | Overridden in `.po` translation files |
| `odoo/service/common.py` — publisher warranty URL | **(b) Internal (server-side)** | Disabled via `publisher_warranty_url =` in `cortexone.conf` |

### SCSS Files

| File Pattern | Classification | Action |
|---|---|---|
| `addons/web/static/src/scss/` — Bootstrap variable names | **(b) Internal** | Left unchanged — CSS class names are internal |
| Custom `cortex_variables.scss` — `$cortex-*` brand colours | **(a) User-visible override** | Implemented — overrides Bootstrap tokens |

### PO Translation Files

| File Pattern | Classification | Action |
|---|---|---|
| `addons/*/i18n/en.po` — msgstr "Odoo" strings | **(a) User-visible** | Overridden in `addons/cortex_branding/i18n/en.po` |
| `addons/*/i18n/hi.po` — Hindi "Odoo" strings | **(a) User-visible** | Overridden in `addons/cortex_branding/i18n/hi.po` |
| Internal `msgid "odoo.something"` keys | **(b) Internal** | Left unchanged |

---

## Intentionally Left Unchanged (Internal Technical Names)

The following are **internal** and **must not be renamed** — doing so would
break database migrations, module loading, XML-ID resolution, or imports:

| Item | Reason |
|------|--------|
| Python package `odoo` (the `odoo/` directory) | Core Python namespace — all modules import from it |
| Model names: `sale.order`, `res.partner`, etc. | Stored in `ir.model` table, keys for all ORM operations |
| XML IDs containing `odoo`: e.g. `base.model_res_users` | Database foreign keys in `ir.model.data` |
| Table names: `sale_order`, `res_partner`, etc. | PostgreSQL table names — renaming requires migration |
| `/xmlrpc/` and `/jsonrpc/` routes | Used internally by the web client |
| `odoo-bin` executable | Carries Odoo copyright — adding wrapper `cortexone` instead |
| IAP module names (`iap`, `iap_mail`) | Module technical names stored in DB |

---

## Remaining Risks

1. **Odoo Bot name** — `OdooBot` appears as a chat user created at DB init.
   The `.po` override renames it to "CortexBot" for new installations.
   **Existing databases** must be manually updated:
   ```sql
   UPDATE res_partner SET name = 'CortexBot' WHERE name = 'OdooBot';
   UPDATE res_users SET login = 'cortexbot' WHERE login = '__odoobot__';
   ```
   *(Only do this if you want to rename it — the login `__odoobot__` is safe to
   keep as internal.)*

2. **Email footer in outbound emails** — Fully overridden in `cortex_mail_layout.xml`.
   Test with a real outbound email to confirm.

3. **PDF reports** — Overridden in `cortex_report_layout.xml`. Upload a company
   logo in Settings → Companies to replace the default.

4. **Website/portal footer** — Partially overridden. If the `website` module is
   installed, also check Website → Customize → footer templates.
