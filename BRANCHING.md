# BRANCHING.md — CortexONE Git Workflow

## Branch Overview

| Branch | Purpose |
|--------|---------|
| `odoo_core` | Pristine, unmodified Odoo Community 18.0. Never add custom code here. Used only to pull upstream security updates. |
| `develop` | Integration branch. All feature branches merge here first. Automatically deployed to staging. |
| `production` | Stable, tested code. Only receives merges from `develop` via reviewed pull requests. Deployed to live. |
| `feature/whitelabel-branding` | CortexONE UI/UX branding overrides |
| `feature/whitelabel-api` | CortexONE REST API layer |
| `feature/whitelabel-deploy` | Docker, CI/CD, server configuration |

## Workflow Diagram

```
upstream/18.0
      │
      ▼
  odoo_core  ◄──── (security updates only, via: git fetch upstream && git merge upstream/18.0)
      │
      ▼
  develop  ◄──────────────────────────┐
      │                               │
      ├──► feature/whitelabel-branding─┤
      ├──► feature/whitelabel-api ─────┤  (PRs into develop)
      └──► feature/whitelabel-deploy──┘
      │
      ▼
  production  ◄── (reviewed PRs from develop only)
```

## Rules

1. **Never commit directly to `odoo_core`** — only merge from `upstream/18.0`.
2. **Never commit directly to `production`** — only merge from `develop` via pull request.
3. **All branding changes go on feature branches**, then PR into `develop`.
4. **`develop` auto-deploys to** `cortexonestage.cortexaitechnologies.com`.
5. **`production` auto-deploys to** `cortexone.cortexaitechnologies.com`.
6. Branch names follow `feature/<short-description>` convention.
7. Commit messages must be descriptive and reference the feature area.

## Pulling Upstream Security Updates

```bash
# Sync upstream Odoo security fixes into odoo_core
git checkout odoo_core
git fetch --depth=1 upstream 18.0
git merge upstream/18.0

# Then rebase develop on top of updated odoo_core
git checkout develop
git rebase odoo_core
```

## Creating a New Feature Branch

```bash
git checkout develop
git checkout -b feature/<name>
# ... make changes ...
git push origin feature/<name>
# Open a pull request → develop
```

## Release to Production

1. All feature branches merged into `develop`.
2. Staging (`cortexonestage.cortexaitechnologies.com`) tested and approved.
3. Open pull request: `develop` → `production`.
4. Requires approval before merge.
5. On merge, GitHub Actions deploys to `cortexone.cortexaitechnologies.com`.
