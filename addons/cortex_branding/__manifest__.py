# License: LGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html
# Copyright (C) 2024 Cortex AI Technologies
{
    'name': 'CortexONE Branding',
    'version': '18.0.1.0.0',
    'summary': 'White-label branding for CortexONE ERP',
    'description': """
        Replaces all Odoo Community branding with CortexONE branding.

        - Logo, favicon, login page
        - Browser/window title
        - Email and PDF report layouts
        - SCSS colour theme
        - Removes odoo.com links from user menu
        - Hides enterprise upsell banners
    """,
    'author': 'Cortex AI Technologies',
    'website': 'https://cortexaitechnologies.com',
    'license': 'LGPL-3',
    'category': 'Hidden',
    'depends': ['web', 'mail', 'base_setup'],
    'data': [
        'data/cortex_branding_data.xml',
        'views/cortex_login_template.xml',
        'views/cortex_mail_layout.xml',
        'views/cortex_report_layout.xml',
        'views/cortex_settings.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'cortex_branding/static/src/scss/cortex_variables.scss',
            'cortex_branding/static/src/scss/cortex_theme.scss',
        ],
        'web.assets_backend': [
            'cortex_branding/static/src/scss/cortex_variables.scss',
            'cortex_branding/static/src/scss/cortex_theme.scss',
            'cortex_branding/static/src/js/cortex_branding.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'sequence': 1,
}
