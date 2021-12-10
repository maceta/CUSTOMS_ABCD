from odoo import fields, models, api

class Product(models.Model):
    _inherit = 'product.product'
    
    qty_avail = fields.Float(
        related='qty_available',
        store=True
    )
    
    def search_from_ui(self,product_id):
        product_name = []
        product_qty = []
        count = 0
        for product in range(len(product_id)):
            product = product_id[count].get('id')
            count += 1
            name = self.browse(product).name
            qty = int(self.browse(product).qty_available)
            
            product_name.append(name)
            product_qty.append(qty)
        return product_name, product_qty
