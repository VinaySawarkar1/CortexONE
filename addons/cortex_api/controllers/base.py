# License: LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
"""
CortexONE REST API — Base controller utilities.

Provides:
- API-key authentication mixin
- Standard JSON response helpers
- Error format: {"success": bool, "error": str, "data": ...}
"""

import functools
import json
import logging

from odoo import http
from odoo.http import Response, request

_logger = logging.getLogger(__name__)

HEADER_API_KEY = 'X-CortexONE-API-Key'


def _json_response(data=None, success=True, error=None, status=200):
    """Return a standardised JSON response."""
    body = {
        'success': success,
        'data': data,
        'error': error,
    }
    return Response(
        json.dumps(body, default=str),
        status=status,
        headers={'Content-Type': 'application/json'},
    )


def _error(message, status=400):
    return _json_response(success=False, error=message, status=status)


def require_api_key(fn):
    """Decorator: validates X-CortexONE-API-Key header against ir.config_parameter."""
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        api_key = request.httprequest.headers.get(HEADER_API_KEY, '').strip()
        if not api_key:
            return _error('Missing API key header (X-CortexONE-API-Key)', 401)
        # Key is stored as a comma-separated list in ir.config_parameter
        stored = request.env['ir.config_parameter'].sudo().get_param(
            'cortex_api.api_keys', '',
        )
        valid_keys = {k.strip() for k in stored.split(',') if k.strip()}
        if api_key not in valid_keys:
            return _error('Invalid or expired API key', 401)
        return fn(*args, **kwargs)
    return wrapper


class CortexApiBase(http.Controller):
    """Base helpers shared by all CortexONE API controllers."""

    def _paginate(self, domain, model, fields, order='id asc'):
        """Apply limit/offset from query-string."""
        limit = min(int(request.httprequest.args.get('limit', 50)), 500)
        offset = int(request.httprequest.args.get('offset', 0))
        records = request.env[model].sudo().search_read(
            domain, fields, limit=limit, offset=offset, order=order,
        )
        total = request.env[model].sudo().search_count(domain)
        return {'items': records, 'total': total, 'limit': limit, 'offset': offset}
