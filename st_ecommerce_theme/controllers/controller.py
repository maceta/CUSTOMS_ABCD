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
"""This file contains all the controllers and functions for PWA"""
import json
from odoo.http import request, Controller, route

class PWA(Controller):
    """Class for Progressive Web App"""

    def get_asset_urls(self, asset_xml_id):
        """This function is used to return the assets urls for worker."""
        qweb = request.env['ir.qweb'].sudo()
        assets = qweb._get_asset_nodes(asset_xml_id, {}, True, True)
        urls = []
        for asset in assets:
            if asset[0] == 'link':
                urls.append(asset[1]['href'])
            if asset[0] == 'script':
                urls.append(asset[1]['src'])
        return urls

    @route('/portal-service-worker.js', type='http', auth="public")
    def service_worker(self):
        """Renders service_worker template with cache name and files to cache."""
        qweb = request.env['ir.qweb'].sudo()
        urls = []
        urls.extend(self.get_asset_urls("web.assets_common"))
        urls.extend(self.get_asset_urls("web.assets_frontend"))
        version_list = []
        for url in urls:
            version_list.append(url.split('/')[3])
        cache_version = '-'.join(version_list)
        mimetype = 'text/javascript;charset=utf-8'
        content = qweb._render('st_ecommerce_theme.service_worker', {
            'pwa_cache_name': cache_version,
            'pwa_files_to_cache': urls,
        })
        return request.make_response(content, [('Content-Type', mimetype)])

    def _get_pwa_manifest_icons(self, pwa_icon):
        """Returns default icons if no icon is uploaded else returns the uploaded icon."""
        icons = []
        if not pwa_icon:
            for size in [
                (128, 128),
                (144, 144),
                (152, 152),
                (192, 192),
                (256, 256),
                (512, 512),
            ]:
                icons.append(
                    {
                        "src": "/st_ecommerce_theme/static/img/icons/icon-%sx%s.png"
                        % (str(size[0]), str(size[1])),
                        "sizes": "{}x{}".format(str(size[0]), str(size[1])),
                        "type": "image/png",
                    }
                )
        elif not pwa_icon.mimetype.startswith("image/svg"):
            all_icons = (
                request.env["ir.attachment"]
                .sudo()
                .search(
                    [
                        ("url", "like", "/st_ecommerce_theme/icon"),
                        (
                            "url",
                            "not like",
                            "/st_ecommerce_theme/icon.",
                        ),  # Get only resized icons
                    ]
                )
            )
            for icon in all_icons:
                icon_size_name = icon.url.split("/")[-1].lstrip("icon").split(".")[0]
                icons.append(
                    {"src": icon.url, "sizes": icon_size_name, "type": icon.mimetype}
                )
        else:
            icons = [
                {
                    "src": pwa_icon.url,
                    "sizes": "128x128 144x144 152x152 192x192 256x256 512x512",
                    "type": pwa_icon.mimetype,
                }
            ]
        return icons

    def _get_pwa_manifest(self):
        """Web App manifest"""
        config_param_sudo = request.env["ir.config_parameter"].sudo()
        pwa_name = config_param_sudo.get_param("pwa.manifest.name", "ST PWA")
        pwa_short_name = config_param_sudo.get_param(
            "pwa.manifest.short_name", "ST PWA"
        )
        pwa_icon = (
            request.env["ir.attachment"]
            .sudo()
            .search([("url", "like", "/st_ecommerce_theme/icon.")])
        )
        background_color = config_param_sudo.get_param(
            "pwa.manifest.background_color", "#9B4DCA"
        )
        theme_color = config_param_sudo.get_param("pwa.manifest.theme_color", "#9B4DCA")
        return {
            "name": pwa_name,
            "short_name": pwa_short_name,
            "icons": self._get_pwa_manifest_icons(pwa_icon),
            "start_url": "/",
            "display": "standalone",
            "background_color": background_color,
            "theme_color": theme_color,
        }

    @route('/st_ecommerce_theme/manifest.json', type='http', auth="public")
    def manifest(self):
        """Returns manifest json"""
        return request.make_response(
            json.dumps(self._get_pwa_manifest()),
            headers=[("Content-Type", "application/json;charset=utf-8")],
        )
