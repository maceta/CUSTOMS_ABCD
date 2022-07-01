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

from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers import main
from odoo.addons.website_sale.controllers.main import WebsiteSale, TableCompute

main.PPG = 20  # Products Per Page
main.PPR = 3  # Products Per Row

class WebsiteProductBrand(WebsiteSale):
    """Class Inheriting WebsiteSale to extend its features as per Product Brands."""

    def get_product_per_page(self, ppg=False, **post):
        """return: product per page and post"""
        if ppg:
            try:
                ppg = int(ppg)
            except ValueError:
                ppg = main.PPG
            post["ppg"] = ppg
        else:
            ppg = main.PPG
        return ppg, post

    def get_product_domain(self, search, category, post, response):
        """Method to return product domain and url
            param: search: input string user searched with
            param: category: category user selected
            return: domain and url"""
        attrib_values = response.qcontext['attrib_values']
        attrib_list = request.httprequest.args.getlist('attrib')
        url = "/shop"
        if search:
            post["search"] = search
        if category:
            category = request.env['product.public.category'].browse(
                int(category))
            url = "/shop/category/%s" % slug(category)
        if attrib_list:
            post['attrib'] = attrib_list

        domain = self._get_search_domain(
            search, category, attrib_values)

        return domain, url

    def get_product_brands(self, brand_ids):
        """Method used to search product brands and return objects.
            param: brand_ids: ids of the brands
            return: objects of product.brand model based on brand_ids passed"""
        brand_obj = request.env['product.brand']
        product_brands = brand_obj.sudo().search(
            [('id', 'in', brand_ids)],
            order='name asc')
        return product_brands

    @http.route()
    def shop(self, page=0, category=None, search='', brand='', ppg=False,
             **post):
        """
        Filter products by brand.
        """
        response = super(WebsiteProductBrand, self).shop(
            page=page, category=category, search=search, ppg=ppg, **post)

        # execute below block if url contains brand parameter
        brand_obj = request.env['product.brand']
        product_temp_obj = request.env['product.template']
        brands_list = request.httprequest.args.getlist('brand')
        ppg, post = self.get_product_per_page(ppg, **post)
        domain, url = self.get_product_domain(search, category, post, response)

        if brands_list:
            brand = self.get_product_brands(brands_list)
            if brand:
                attrib_list = request.httprequest.args.getlist('attrib')

                try:
                    brand_values = [int(x) for x in request.httprequest.args.getlist('brand')]
                except Exception as e:
                    brand_values = []

                product_brands = brand_obj.sudo().browse(brand_values).exists()
                post["brand"] = brands_list

                domain += [('product_brand_id', 'in', product_brands.ids)]
                product_count = product_temp_obj.search_count(domain)
                pager = request.website.pager(
                    url=url, total=product_count, page=page, step=ppg,
                    scope=7, url_args=post)

                products = product_temp_obj.search(domain, limit=ppg,
                                                   offset=pager['offset'],
                                                   order=self._get_search_order(post))

                keep = QueryURL('/shop',
                                category=category and int(category),
                                search=search, brand=brands_list,
                                attrib=attrib_list, order=post.get('order'))

                values = {
                    'products': products,
                    'bins': TableCompute().process(products, ppg),
                    'pager': pager,
                    'search_count': product_count,
                    'search': search,
                    'product_brands': brand_obj.sudo().search([], order='name asc'),
                    'product_brand_set': set(brand_values),
                    'request_brands': brand,
                    'keep': keep,
                    'order_by': post.get('order', ''),
                }
                response.qcontext.update(values)
                return response

        try:
            brand_list = [int(x) for x in request.httprequest.args.getlist('brand')]
        except Exception as e:
            brand_list = []

        product_count = product_temp_obj.search_count(domain)
        pager1 = request.website.pager(
            url=url, total=product_count, page=page, step=ppg,
            scope=7, url_args=post)
        products = product_temp_obj.search(domain, limit=ppg,
                                           offset=pager1['offset'],
                                           order=self._get_search_order(post))

        if products:
            product_brands = self.get_product_brands(products.mapped('product_brand_id').ids)
        else:
            product_brands = self.get_product_brands(brand_list)

        values = {
            'product_brands': product_brands,
            'product_brand_set': set(brand_list),
            'search_count': len(products),
            'order_by': post.get('order', ''),
        }

        response.qcontext.update(values)
        return response
