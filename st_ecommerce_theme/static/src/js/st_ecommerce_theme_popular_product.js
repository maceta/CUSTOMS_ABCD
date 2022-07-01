/*##############################################################################
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
###############################################################################*/
odoo.define('st_ecommerce_theme.popular_products', function(require) {
    "use strict";

    var sAnimation = require('website.content.snippets.animation');

    sAnimation.registry.popular_products = sAnimation.Class.extend({
        selector: ".popular_products",

        start: function() {
            var self = this;
            if (self.editableMode) {
                self.$target.empty();
            }
            if (!self.editableMode) {
                return $.ajax({
                    url: '/website/slider/popular_products',
                    method: 'GET',
                    data: {
                        limit: self.$target.attr('data-popular-product-days'),
                    },
                    success: function(data) {

                        var loop = false;
                        var autoplay = false;
                        var owl2_item = $(".owl-product-item");
                        if (owl2_item.length > 4){
                            loop = true;
                            autoplay = true
                        }
                        self.$target.empty().append(data);
                        $(".popular_products").owlCarousel({
                            navigation: true,
                            pagination: true,
                            loop: loop,
                            autoplay: autoplay,
                            nav: true,
                            dots: false,
                            margin: 20,
                            responsive: {
                                0: {
                                    items: 1,
                                },
                                600: {
                                    items: 3,
                                },
                                1000: {
                                    items: 4,
                                },
                                1100: {
                                    items: 5,
                                }
                            }
                        });
                    },
                });
            }
        }
    });

    return {
        DataSlider: sAnimation.registry.popular_products,
    };

});
