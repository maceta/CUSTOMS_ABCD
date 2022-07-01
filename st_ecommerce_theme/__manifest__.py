##############################################################################
# 
# Odoo Proprietary License v1.0
# 
# This software and associated files (the "Software") may only be used (executed)
#  if you have purchased a valid license from the authors, typically via Odoo 
#  Apps, or if you have received a written agreement from the authors of the 
#  Software (see the COPYRIGHT file). 
# 
# You may develop Odoo modules that use the Software as a library (typically 
#  by depending on it, importing it and using its resources), but without 
# copying any source code or material from the Software. 
# You may distribute those modules under the license of your choice, provided 
# that this license is compatible with the terms of the Odoo Proprietary License 
# (For example: LGPL, MIT, or proprietary licenses similar to this one). 
# 
# It is forbidden to modify, upgrade, publish, distribute, sublicense, or sell 
# copies of the Software or modified copies of the Software. 
# 
# The above copyright notice and this permission notice must be included in all 
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
# 
###############################################################################
{
    'name': 'E-commerce Theme',
    'version': '14.0.0.1',
    'sequence': 102,
    'author': 'Surekha Technologies',
    'description': "Multi Purpose, Responsive with advance new features in the e-commerce theme.",
    'summary': "Multi Purpose, Responsive with advance new features in the e-commerce theme.",
    'category': 'Theme/Ecommerce',
    'website': 'https://www.surekhatech.com',
    'depends': ['website_sale', 'mass_mailing_sale', 'website_mass_mailing', 'website_sale_wishlist',
                'website_sale_comparison', 'payment_transfer', 'website_sale_delivery', 'portal','mail'],
    'data': [
        'security/product_brand_security.xml',
        'security/ir.model.access.csv',
        'data/ecommerce_mass_mailing_data.xml',
        'views/assets.xml',
        'views/templates.xml',
        'views/product_brand_view.xml',
        'views/product_template_view.xml',
        'views/st_ecommerce_config.xml',
        'views/st_ecommerce_theme_snippets.xml',
        'views/cod_template.xml',
        'views/cod_view.xml',
        'data/cod_journal.xml',
        'data/cod.xml',
        'views/webclient_templates.xml',
        'views/res_config_settings_views.xml',
        'views/whishlist_templates.xml',
    ],
    'images': [
        'images/ecommerce_theme.gif',
        'static/description/ecommerce_screenshot.gif',
    ],
    'application': True,
    'price': 49.00,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'live_test_url': 'https://ecomv14.surekhatech.com/web?db=odoo_14_st_ecommerce_theme',
}
