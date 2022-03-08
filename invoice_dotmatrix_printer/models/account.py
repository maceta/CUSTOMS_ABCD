# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class AccountDotmatrixReceipt(models.TransientModel):
    _name = 'account.dotmatrix.receipt'

    name = fields.Char("Test")


class AccountMove(models.Model):
    _inherit = "account.move"
 
    def print_new_receipt(self):
        templ = self.env.ref("invoice_dotmatrix_printer.template_dotmatrix_ai")
        if templ:
            data = self.env['mail.render.mixin']._render_template(templ.body_html, 'account.move', [self.id])
            view_id = self.env.ref('invoice_dotmatrix_printer.account_dotmatrix_receipt_form').id
            res = {
            	"name":data[self.id],
            }
            wizard_id = self.env['account.dotmatrix.receipt'].create(res)
            context = self._context.copy()
            return {
                'name':'Print Receipt',
                'view_type':'form',
                'view_mode':'tree',
                'views' : [(view_id,'form')],
                'res_model':'account.dotmatrix.receipt',
                'view_id':view_id,
                'type':'ir.actions.act_window',
                'res_id':wizard_id.id,
                'target':'new',
                'context':context,

            }






