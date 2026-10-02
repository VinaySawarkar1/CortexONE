# License: LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
"""
CortexONE REST API — Authentication endpoints.

POST /api/v1/auth/token   — Exchange username+password for an API token stored
                            in ir.config_parameter (simple stateless approach).
DELETE /api/v1/auth/token — Revoke the key.
"""

import logging
import secrets

from odoo import http
from odoo.http import request

from .base import HEADER_API_KEY, CortexApiBase, _error, _json_response, require_api_key

_logger = logging.getLogger(__name__)


class CortexAuthController(CortexApiBase):

    @http.route('/api/v1/auth/token', type='http', auth='none',
                methods=['POST'], csrf=False, save_session=False)
    def get_token(self, **kwargs):
        """
        Exchange credentials for an API key.

        Body (JSON): {"login": "...", "password": "...", "db": "..."}
        Response:    {"success": true, "data": {"api_key": "...", "uid": ...}}
        """
        try:
            payload = request.get_json_data()
        except (TypeError, ValueError, AttributeError):
            return _error('Request body must be JSON', 400)

        login = payload.get('login', '').strip()
        password = payload.get('password', '').strip()
        db = payload.get('db') or request.db

        if not login or not password:
            return _error('login and password are required', 400)

        uid = request.env['res.users'].sudo()._login(db, login, password)
        if not uid:
            return _error('Invalid credentials', 401)

        # Generate a secure token and store it
        new_key = secrets.token_urlsafe(40)
        ICP = request.env['ir.config_parameter'].sudo()
        existing = ICP.get_param('cortex_api.api_keys', '')
        keys = {k.strip() for k in existing.split(',') if k.strip()}
        keys.add(new_key)
        ICP.set_param('cortex_api.api_keys', ','.join(keys))

        _logger.info('CortexONE API: issued token for uid=%s', uid)
        return _json_response({'api_key': new_key, 'uid': uid}, status=200)

    @http.route('/api/v1/auth/token', type='http', auth='none',
                methods=['DELETE'], csrf=False, save_session=False)
    @require_api_key
    def revoke_token(self, **kwargs):
        """Revoke the current API key."""
        api_key = request.httprequest.headers.get(HEADER_API_KEY, '').strip()
        ICP = request.env['ir.config_parameter'].sudo()
        existing = ICP.get_param('cortex_api.api_keys', '')
        keys = {k.strip() for k in existing.split(',') if k.strip()}
        keys.discard(api_key)
        ICP.set_param('cortex_api.api_keys', ','.join(keys))
        return _json_response({'message': 'Token revoked'}, status=200)
