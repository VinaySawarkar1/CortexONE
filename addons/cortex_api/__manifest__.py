# License: LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
{
    'name': 'CortexONE REST API',
    'version': '18.0.1.0.0',
    'summary': 'REST API layer for CortexONE ERP (/api/v1/...)',
    'description': """
        Exposes a versioned REST API for CortexONE under /api/v1/.
        Endpoints: auth, partners, products, sales orders, invoices.
        Authentication: API-key header (X-CortexONE-API-Key).
        Returns standardised JSON with our own error format.
        Internal /xmlrpc and /jsonrpc are NOT disabled (web client needs them).
    """,
    'author': 'Cortex AI Technologies',
    'website': 'https://cortexaitechnologies.com',
    'license': 'LGPL-3',
    'category': 'Hidden',
    'depends': ['web', 'base', 'sale', 'account', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'security/cortex_api_security.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
