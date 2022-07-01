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
import logging
from odoo import http
from odoo.addons.web.controllers.main import Home
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.http import request
from odoo.exceptions import AccessError

import werkzeug
import werkzeug.exceptions
import werkzeug.utils
import werkzeug.wrappers
import werkzeug.wsgi

_logger = logging.getLogger(__name__)


class Home(Home):
    """
    Inherited home class of web controller
    """

    @http.route('/web', type='http', auth="none")
    def web_client(self, s_action=None, **kw):
        """
        By default redirect to the home page before login
        """
        if not request.session.uid:
            return werkzeug.utils.redirect('/', 303)

        if kw.get('redirect'):
            return werkzeug.utils.redirect(kw.get('redirect'), 303)

        request.uid = request.session.uid
        try:
            context = request.env['ir.http'].webclient_rendering_context()
            response = request.render(
                'web.webclient_bootstrap', qcontext=context)
            response.headers['X-Frame-Options'] = 'DENY'
            return response
        except AccessError:
            return werkzeug.utils.redirect('/web/login?error=access')


class CodController(http.Controller):
    """Class to handle COD payments"""
    _accept_url = '/payment/cod/feedback'

    @http.route(['/payment/cod/feedback'], type='http', auth='public', csrf=False)
    def cod_form_feedback(self, **post):
        """
        Give a feedback to user for payment pending process of order
        :param post: dict of placed order
        :return: feedback message for placed order
        """
        if post:
            # After choosing a payment method make the cart empty
            order = request.env['sale.order'].search([
                ('name', '=', post.get('reference').split('-')[0])
            ])
            if order.cart_quantity:
                request.session.update({
                    'sale_order_id': False,
                    'website_sale_current_pl': False,
                })
            # proceed to further payment process
            request.env['payment.transaction'].sudo(
            ).form_feedback(post, 'cod')
        return werkzeug.utils.redirect('/payment/process')


class WebsiteSaleInherit(WebsiteSale):
    """Class Inheriting WebSite Sale to extend its functonality"""

    def _get_shop_payment_values(self, order, **kwargs):
        """
        :param order: record of sale order
        :return: dict
        Checked minimum and maximum order amount for COD.
        Added unavailability message, if cod is not available for the order.
        """

        res = super(WebsiteSaleInherit, self)._get_shop_payment_values(
            order, **kwargs)
        acquirers = res.get('acquirers')
        cod_payment = request.env.ref(
            'st_ecommerce_theme.payment_acquirer_cod')

        # if shipping country is not in available countries of cod
        if cod_payment in acquirers:
            acquirers.remove(cod_payment)

        # if shipping country is in available countries of cod
        if order.partner_shipping_id.country_id in cod_payment.country_ids \
            and cod_payment not in acquirers:
            acquirers.append(cod_payment)

        if cod_payment.state == 'enabled':
            cod_available = order.order_line.filtered(
                lambda line: line.is_delivery is False).mapped('product_id').filtered(
                lambda product: product.cod_available is False)

            if not cod_available:
                res_partner = request.env['res.partner'].browse(
                    res.get('partner'))
                res.update({
                    'payment_acquirer': cod_payment,
                    'res_partner': res_partner
                })
                if (order.amount_total <= cod_payment.min_order_amount or order.amount_total >=
                        cod_payment.max_order_amount):
                    if cod_payment in acquirers:
                        acquirers.remove(cod_payment)
            else:
                res.update(
                    {'unavailability_msg': cod_payment.unavailability_message})
                if cod_payment in acquirers:
                    acquirers.remove(cod_payment)
        return res

    def _prepare_product_values(self, product, category='', search='', **kwargs):
        """
        Added cod availability message to display custom message, if cod available in the product
        :param product: products of the SO line
        :param category: product category
        :param search: name of a method that implement search on the field (optional)
        :return: dict
        """
        res = super(WebsiteSaleInherit, self)._prepare_product_values(
            product, category, search)
        cod_payment = request.env.ref(
            'st_ecommerce_theme.payment_acquirer_cod')

        if cod_payment.state == 'enabled':
            if product.cod_available:
                cod_payment = request.env.ref(
                    'st_ecommerce_theme.payment_acquirer_cod')
                res.update(
                    {'cod_available_msg': cod_payment.availability_message})
        return res
