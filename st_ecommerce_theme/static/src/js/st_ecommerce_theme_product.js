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
odoo.define('st_ecommerce_theme.product_view', function(require) {
    "use strict";
    var ajax = require('web.ajax');

    /**
     * for display product on list view
     * @param: {Event} event
     */
    $('#list').click(function(event) {
        event.preventDefault();
        $('#grid').removeClass('active');
        $('#list').addClass('active');
        ajax.jsonRpc("/list_view", 'call', {}).then(function() {
            $(document)[0].location.reload();
        });
    });

    /**
     * for display product on grid view
     * @param: {Event} event
     */
    $('#grid').click(function(event) {
        event.preventDefault();
        $('#list').removeClass('active');
        $('#grid').addClass('active');
        ajax.jsonRpc("/grid_view", 'call', {}).then(function() {
            $(document)[0].location.reload();
        });
    });

    $('form.js_product_brands input, form.js_product_brands select').on('change', function(event) {
        if (!event.isDefaultPrevented()) {
            event.preventDefault();
            $(this).closest("form").submit();
        }
    });

});

$(document).ready(function() {

    // add class for list/grid view
    if ($('#products_grid').length > 0) {
        var products_grid_class = $('#products_grid').attr('class');
        $('.productlist-top').addClass(products_grid_class);
    }

});


odoo.define('st_ecommerce_theme.product_page', function(require) {
    "use strict";

    jQuery(document).ready(function() {

        // social-icon on product details page
        $('.fb_product_share').click(function(e) {
            var share_url = window.location.href;
            var popup_url = _.str.sprintf("https://www.facebook.com/sharer/sharer.php?u=%s", encodeURIComponent(share_url));
            window.open(popup_url, 'Share Dialog', 'width=600,height=400');
        });
        $('.tw_product_share').click(function(e) {
            var share_text = "Share product Page";
            var share_url = window.location.href;
            var popup_url = _.str.sprintf("https://twitter.com/intent/tweet?tw_p=tweetbutton&text=%s %s", share_text, share_url);
            window.open(popup_url, 'Share Dialog', 'width=600,height=400');
        });
        $('.li_product_share').click(function(e) {
            var share_text = "Share product Page";
            var share_url = window.location.href;
            var popup_url = _.str.sprintf("http://www.linkedin.com/feed?mini=true&url=%s&title=I am using odoo&summary=%s&source=www.odoo.com", encodeURIComponent(share_url), share_text);
            window.open(popup_url, 'Share Dialog', 'width=600,height=400');
        });

        // display alternatives products on products details page
        var owl = $("#owl-carousel");
        var loop = false;
        var autoplay = false;
        var owl2_item = $(".owl-product-item");
        if (owl2_item.length > 4){
            loop = true;
            autoplay = true
        }

        owl.owlCarousel({

            loop: loop,
            autoplay: autoplay,
            autoplayTimeout: 3000,
            margin: 10,

            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,
                },
                600: {
                    items: 3,
                },
                1000: {
                    items: 5,
                }
            }

        });
    });

});
