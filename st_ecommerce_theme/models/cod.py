# -*- coding: utf-8 -*-
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
import pprint

from odoo import models, fields, api
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare
from odoo.tools.translate import _

_logger = logging.getLogger(__name__)


class UiView(models.Model):
    """Class Inheriting Ui View for Customize Show method"""
    _inherit = 'ir.ui.view'

    @api.model
    def _update_customize_show(self):  
        """To hide the Alternative Products Toggle button from Customize"""
        view_ids = self.sudo().search([('key', '=', 'website_sale.recommended_products')])
        view_ids.customize_show = False
        return True

class AcquirerCod(models.Model):
    """Class Inheriting Payment Acquirer for COD payment method"""
    _inherit = 'payment.acquirer'

    # Add COD as payment method
    provider = fields.Selection(selection_add=[('cod', 'Cash on Delivery')], default='cod',
                                ondelete={'cod': 'set default'})
    min_order_amount = fields.Float()
    max_order_amount = fields.Float()
    availability_message = fields.Text('Availability Message', translate=True,
                                       default=lambda str: _(
                                           'Cash On Delivery Available!'),
        help='Message displayed, if the cash on delivery is available in the product')
    unavailability_message = fields.Text('Unavailability Message', translate=True,
                                         default=lambda str: _(
        'Product(s) in your cart can not be delivered through Cash On Delivery.'),
        help='Message displayed, if product is added in the cart that not allowed cod')
    min_max_amount_message = fields.Text('Min/Max Amount Policy Message', translate=True,
                                         default=lambda str: _(
                                            'Order Amount Must Be in Between '),
        help='Message displayed, if ordered amount is not in between the minimum and '
        'maximum order amount')

    def cod_get_form_action_url(self):
        """Method returning form action url"""
        return '/payment/cod/feedback'


class CodPaymentTransaction(models.Model):
    """Class inheriting Payment Transaction"""
    _inherit = 'payment.transaction'

    @api.model
    def _cod_form_get_tx_from_data(self, data):
        """Method to get transaction details from the data posted in form."""
        reference, amount, currency_name = data.get(
            'reference'), data.get('amount'), data.get('currency_name')
        payment_tx = self.search([('reference', '=', reference)])

        if not payment_tx or len(payment_tx) > 1:
            error_msg = _('received data for reference %s') % (
                pprint.pformat(reference))
            if not payment_tx:
                error_msg += _('; no order found')
            else:
                error_msg += _('; multiple order found')
            _logger.info(error_msg)
            raise ValidationError(error_msg)

        return payment_tx

    def _cod_form_get_invalid_parameters(self, data):
        """Method to check invalid parameters in the data posted in form"""
        invalid_parameters = []

        if float_compare(float(data.get('amount', '0.0')), self.amount, 2) != 0:
            invalid_parameters.append(
                ('amount', data.get('amount'), '%.2f' % self.amount))
        if data.get('currency') != self.currency_id.name:
            invalid_parameters.append(
                ('currency', data.get('currency'), self.currency_id.name))

        return invalid_parameters

    def _cod_form_validate(self, data):
        """Method to validate the data posted in form"""
        _logger.info(
            'Validated transfer payment for tx %s: set as pending' % self.reference)
        self._set_transaction_pending()
        return True


class ProductCod(models.Model):
    """Class inheriting product template to add additional fields."""
    _inherit = 'product.template'

    cod_available = fields.Boolean(string="COD Available",
        help="Available cash on delivery payment option for this product.")
