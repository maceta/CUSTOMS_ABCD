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
from odoo import http
from odoo.http import request


class PopularProductCarousel(http.Controller):
    """Class to define Product Carousel"""
    @http.route(
        '/website/slider/popular_products',
        type='http',
        auth='public',
        methods=['GET'],
        website=True,
    )
    def get_popular_products(self, **kwargs):
        """
        get all the popular products as per the conditions
        """
        limit = kwargs.get('limit', 5)
        request.env.cr.execute(
            "SELECT pt.id, SUM(product_uom_qty) from sale_order_line so, "
            "product_product pp, product_template pt "
            "where so.product_id=pp.id and so.state != 'cancel' and so.state = 'sale' "
            "and pp.product_tmpl_id=pt.id and pt.is_published=True "
            "GROUP BY pt.id ORDER BY SUM(product_uom_qty) DESC limit %s" % limit
        )

        product_ids = [product_data[0]
                       for product_data in request.env.cr.fetchall()]
        products = request.env['product.template'].sudo().browse(product_ids)

        popular_product_carousel = ""
        html_template = """
            <div class="owl-product-item item">
                <div class="item-img">
                    <img src="%s" height="77" width="77" alt=""/>
                    <div class="item-img-ho">

                     <a itemprop="url" href="%s"> 
                        <i class="fa fa-eye" title="View"/> 
                     </a>

                    </div>
                </div>
                <p><a itemprop="url" href="%s">%s</a></p>
                <strong>%s%s</strong>
            </div>                            
        """
        for product in products:
            product_link = 'shop/product/%s' % (product.id,)

            popular_product_carousel += html_template % (
                'web/image/product.template/' +
                str(product.id) + '/image_1024',
                product_link,
                product_link,
                product.name, round(product.list_price, 2),
                ' ' + request.website.get_current_pricelist().currency_id.symbol)

        response = request.make_response(popular_product_carousel)
        return response
