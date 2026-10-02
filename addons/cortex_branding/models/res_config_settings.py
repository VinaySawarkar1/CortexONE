# License: LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Extend settings to store CortexONE branding values."""
    _inherit = 'res.config.settings'

    cortex_product_name = fields.Char(
        string='Product Name',
        default='CortexONE',
        config_parameter='cortex_branding.product_name',
    )
    cortex_support_email = fields.Char(
        string='Support Email',
        default='support@cortexaitechnologies.com',
        config_parameter='cortex_branding.support_email',
    )
    cortex_website_url = fields.Char(
        string='Website URL',
        default='https://cortexaitechnologies.com',
        config_parameter='cortex_branding.website_url',
    )
