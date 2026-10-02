# License: LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
"""
cortex_api — test suite
Tests: authentication, partner listing, invoice listing.
"""

from odoo.tests.common import HttpCase, tagged


@tagged('cortex_api', 'post_install', '-at_install')
class TestCortexApiAuth(HttpCase):
    """Test CortexONE REST API authentication."""

    def setUp(self):
        super().setUp()
        # Register a test API key in config
        self.env['ir.config_parameter'].set_param(
            'cortex_api.api_keys', 'test-key-123',
        )

    def test_missing_api_key(self):
        """Requests without key should return 401."""
        res = self.url_open('/api/v1/partners')
        self.assertEqual(res.status_code, 401)

    def test_invalid_api_key(self):
        """Wrong key should return 401."""
        res = self.url_open(
            '/api/v1/partners',
            headers={'X-CortexONE-API-Key': 'wrong-key'},
        )
        self.assertEqual(res.status_code, 401)

    def test_valid_api_key_partners(self):
        """Valid key should return 200 with items list."""
        res = self.url_open(
            '/api/v1/partners',
            headers={'X-CortexONE-API-Key': 'test-key-123'},
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get('success'))
        self.assertIn('items', data.get('data', {}))

    def test_valid_api_key_products(self):
        """Valid key should return 200 for products."""
        res = self.url_open(
            '/api/v1/products',
            headers={'X-CortexONE-API-Key': 'test-key-123'},
        )
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get('success'))

    def test_nonexistent_partner(self):
        """Non-existent partner ID returns 404."""
        res = self.url_open(
            '/api/v1/partners/9999999',
            headers={'X-CortexONE-API-Key': 'test-key-123'},
        )
        self.assertEqual(res.status_code, 404)


@tagged('cortex_api', 'post_install', '-at_install')
class TestCortexBranding(HttpCase):
    """Test that branding overrides do not break core functionality."""

    def test_login_page_no_odoo_title(self):
        """Login page title should not contain 'Odoo'."""
        res = self.url_open('/web/login')
        self.assertEqual(res.status_code, 200)
        # Title should contain CortexONE
        self.assertNotIn('<title>Odoo', res.text)
