# License: LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
"""
CortexONE REST API — Partners, Products, Sales Orders, Invoices.
All routes require X-CortexONE-API-Key header.
"""

import logging

from odoo import http
from odoo.http import request
from .base import CortexApiBase, _json_response, _error, require_api_key

_logger = logging.getLogger(__name__)


class CortexPartnersController(CortexApiBase):

    @http.route('/api/v1/partners', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    @require_api_key
    def list_partners(self, **kwargs):
        """GET /api/v1/partners — list partners with pagination."""
        data = self._paginate(
            domain=[('active', '=', True)],
            model='res.partner',
            fields=['id', 'name', 'email', 'phone', 'street', 'city',
                    'country_id', 'is_company', 'vat'],
        )
        return _json_response(data)

    @http.route('/api/v1/partners/<int:partner_id>', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    @require_api_key
    def get_partner(self, partner_id, **kwargs):
        """GET /api/v1/partners/:id — single partner."""
        partner = request.env['res.partner'].sudo().browse(partner_id)
        if not partner.exists():
            return _error('Partner not found', 404)
        return _json_response(partner.read([
            'id', 'name', 'email', 'phone', 'mobile', 'street', 'city',
            'zip', 'country_id', 'is_company', 'vat', 'website',
        ])[0])


class CortexProductsController(CortexApiBase):

    @http.route('/api/v1/products', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    @require_api_key
    def list_products(self, **kwargs):
        """GET /api/v1/products — list products with pagination."""
        data = self._paginate(
            domain=[('sale_ok', '=', True)],
            model='product.template',
            fields=['id', 'name', 'list_price', 'standard_price', 'type',
                    'categ_id', 'default_code', 'barcode'],
        )
        return _json_response(data)

    @http.route('/api/v1/products/<int:product_id>', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    @require_api_key
    def get_product(self, product_id, **kwargs):
        """GET /api/v1/products/:id — single product."""
        product = request.env['product.template'].sudo().browse(product_id)
        if not product.exists():
            return _error('Product not found', 404)
        return _json_response(product.read([
            'id', 'name', 'description', 'list_price', 'standard_price',
            'type', 'categ_id', 'default_code', 'barcode', 'active',
        ])[0])


class CortexSalesController(CortexApiBase):

    @http.route('/api/v1/sales', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    @require_api_key
    def list_sales(self, **kwargs):
        """GET /api/v1/sales — list sale orders."""
        data = self._paginate(
            domain=[],
            model='sale.order',
            fields=['id', 'name', 'partner_id', 'date_order', 'amount_total',
                    'state', 'currency_id'],
            order='date_order desc',
        )
        return _json_response(data)

    @http.route('/api/v1/sales/<int:order_id>', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    @require_api_key
    def get_sale(self, order_id, **kwargs):
        """GET /api/v1/sales/:id — single sale order with lines."""
        order = request.env['sale.order'].sudo().browse(order_id)
        if not order.exists():
            return _error('Sale order not found', 404)
        result = order.read([
            'id', 'name', 'partner_id', 'date_order', 'amount_untaxed',
            'amount_tax', 'amount_total', 'state', 'currency_id', 'note',
        ])[0]
        result['lines'] = order.order_line.read([
            'id', 'product_id', 'product_uom_qty', 'price_unit',
            'price_subtotal', 'tax_id', 'name',
        ])
        return _json_response(result)


class CortexInvoicesController(CortexApiBase):

    @http.route('/api/v1/invoices', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    @require_api_key
    def list_invoices(self, **kwargs):
        """GET /api/v1/invoices — list customer invoices."""
        data = self._paginate(
            domain=[('move_type', 'in', ['out_invoice', 'out_refund'])],
            model='account.move',
            fields=['id', 'name', 'partner_id', 'invoice_date', 'invoice_date_due',
                    'amount_total', 'payment_state', 'state', 'currency_id'],
            order='invoice_date desc',
        )
        return _json_response(data)

    @http.route('/api/v1/invoices/<int:invoice_id>', type='http', auth='none',
                methods=['GET'], csrf=False, save_session=False)
    @require_api_key
    def get_invoice(self, invoice_id, **kwargs):
        """GET /api/v1/invoices/:id — single invoice with lines."""
        invoice = request.env['account.move'].sudo().browse(invoice_id)
        if not invoice.exists() or invoice.move_type not in ('out_invoice', 'out_refund'):
            return _error('Invoice not found', 404)
        result = invoice.read([
            'id', 'name', 'partner_id', 'invoice_date', 'invoice_date_due',
            'amount_untaxed', 'amount_tax', 'amount_total', 'payment_state',
            'state', 'currency_id', 'narration',
        ])[0]
        result['lines'] = invoice.invoice_line_ids.read([
            'id', 'name', 'quantity', 'price_unit', 'price_subtotal',
            'tax_ids', 'account_id', 'product_id',
        ])
        return _json_response(result)
