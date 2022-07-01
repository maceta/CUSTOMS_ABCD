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
"""The code in this file is used to extend config settings."""
import base64
import io
import sys
from PIL import Image
from odoo import _, api, exceptions, fields, models
from odoo.tools.mimetypes import guess_mimetype


class ResConfigSettings(models.TransientModel):
    """This class is used to extend res config settings for PWA configuration."""
    _inherit = "res.config.settings"
    _pwa_icon = "/st_ecommerce_theme/icon"

    pwa_name = fields.Char("Progressive Web App Name",
                           help="Name of the Progressive Web Application")
    pwa_short_name = fields.Char(
        "Progressive Web App Short Name",
        help="Short Name of the Progressive Web Application",
    )
    pwa_icon = fields.Binary("Icon", readonly=False)
    pwa_background_color = fields.Char("Background Color")
    pwa_theme_color = fields.Char("Theme Color")

    @api.model
    def get_values(self):
        """This method is used to get the values of the System Parameters."""
        config_param_obj = self.env["ir.config_parameter"].sudo()
        res = super(ResConfigSettings, self).get_values()
        res["pwa_name"] = config_param_obj.get_param(
            "pwa.manifest.name", default="ST PWA"
        )
        res["pwa_short_name"] = config_param_obj.get_param(
            "pwa.manifest.short_name", default="PWA"
        )
        pwa_icon_ir_attachment = (
            self.env["ir.attachment"].sudo()
            .search([("url", "like", self._pwa_icon + ".")])
        )
        res["pwa_icon"] = (
            pwa_icon_ir_attachment.datas if pwa_icon_ir_attachment else False
        )
        res["pwa_background_color"] = config_param_obj.get_param(
            "pwa.manifest.background_color", default="#9B4DCA"
        )
        res["pwa_theme_color"] = config_param_obj.get_param(
            "pwa.manifest.theme_color", default="#9B4DCA"
        )
        return res

    def _unpack_icon(self, icon):
        # Wrap decoded_icon in BytesIO object
        decoded_icon = base64.b64decode(icon)
        icon_bytes = io.BytesIO(decoded_icon)
        return Image.open(icon_bytes)

    def _write_icon_to_attachment(self, extension, mimetype, size=None):
        url = self._pwa_icon + extension
        icon = self.pwa_icon
        # Resize image
        if size:
            image = self._unpack_icon(icon)
            resized_image = image.resize(size)
            icon_bytes_output = io.BytesIO()
            resized_image.save(icon_bytes_output,
                               format=extension.lstrip(".").upper())
            icon = base64.b64encode(icon_bytes_output.getvalue())
            url = "{}{}x{}{}".format(
                self._pwa_icon, str(size[0]), str(size[1]), extension,
            )
        existing_attachment = (
            self.env["ir.attachment"].sudo().search([("url", "like", url)]))

        values = {
            "datas": icon,
            "db_datas": icon,
            "url": url,
            "name": url,
            "type": "binary",
            "mimetype": mimetype,
        }

        if existing_attachment:
            existing_attachment.sudo().write(values)
        else:
            self.env["ir.attachment"].sudo().create(values)

    @api.model
    def set_values(self):
        """This method is used to set the values of the System Parameters."""
        config_param_obj = self.env["ir.config_parameter"].sudo()
        res = super(ResConfigSettings, self).set_values()
        config_param_obj.set_param("pwa.manifest.name", self.pwa_name)
        config_param_obj.set_param(
            "pwa.manifest.short_name", self.pwa_short_name
        )
        config_param_obj.set_param(
            "pwa.manifest.background_color", self.pwa_background_color
        )
        config_param_obj.set_param(
            "pwa.manifest.theme_color", self.pwa_theme_color
        )
        # Retrieve previous value for pwa_icon from ir_attachment
        ir_attachments_icons = (
            self.env["ir.attachment"].sudo()
            .search([("url", "like", self._pwa_icon)])
        )
        # Delete if no icon provided
        if not self.pwa_icon:
            if ir_attachments_icons:
                ir_attachments_icons.unlink()
            return res

        if sys.getsizeof(self.pwa_icon) > 2097152:
            raise exceptions.UserError(
                _("Please upload a file of size upto 2 MB only.")
            )

        decoded_pwa_icon = base64.b64decode(self.pwa_icon)

        pwa_icon_mimetype = guess_mimetype(decoded_pwa_icon)
        pwa_icon_extension = "." + \
            pwa_icon_mimetype.split("/")[-1].split("+")[0]
        if not pwa_icon_mimetype.startswith(
            "image/svg"
        ) and not pwa_icon_mimetype.startswith("image/png"):
            raise exceptions.UserError(
                _("Please upload SVG or PNG files only."))
        # Delete all previous records if we are updating the new ones
        if ir_attachments_icons:
            ir_attachments_icons.unlink()
        self._write_icon_to_attachment(pwa_icon_extension, pwa_icon_mimetype)

        if pwa_icon_extension != ".svg":
            for size in [
                (128, 128),
                (144, 144),
                (152, 152),
                (192, 192),
                (256, 256),
                (512, 512),
            ]:
                self._write_icon_to_attachment(
                    pwa_icon_extension, pwa_icon_mimetype, size=size
                )
