odoo.define('pos_sale_item_info.pos_so', function (require) {
"use strict";

var screens = require('point_of_sale.screens');
var gui = require('point_of_sale.gui');
var Model = require('web.DataModel');
var Widget = require('web.Widget');
var core = require('web.core');
var PopupWidget = require('point_of_sale.popups');
var PosBaseWidget = require('point_of_sale.BaseWidget');
var ProductListWidget = screens.ProductListWidget;
var QWeb = core.qweb;
var _t = core._t;

var SaleOrderButton = screens.ActionButtonWidget.extend({
    template: 'SaleOrderButton',
    button_click: function(){
        var self = this;
        this.get_orders({
        'title':_t('Product Qty'),
        });
    },
    get_orders : function(options){
        options = options || {};
        var self = this;
        var list = [];
        var order_lines = this.pos.get_order().get_orderlines();
        var flag_negative = false;
        if(this.pos.get_order().get_orderlines().length > 0){
            var product_product = {};
            var product_id = [];
            var self = this;
            var order_lines = this.pos.get_order().get_orderlines();
            for (var line in order_lines){
                    if (order_lines[line].quantity>0)
                    {
                        var product = order_lines[line].product;
                        product_id.push(product);
                    }
                }
            var user = this.pos.cashier
            product_product.from_pos = true;
            product_product.product_id = product_id;
            var productModel = new Model('product.product');
                productModel.call('search_from_ui',[product_product,product_id]).then(function(product_qty){
                    var len = product_qty[0].length;
                    for (var i = 0; i < len; i++) {
                        var name = product_qty[0][i];
                        var qty = product_qty[1][i];
                        list.push({
                            'label': name,
                            'qty': qty,
                            'item':  'Product Qty',
                        });
                    }
                    self.gui.show_popup('pos_so',{
                        'title': options.title || _t('Select User'),
                        list: list,
                    });
                });
        }
    }
    
});

    
screens.define_action_button({
    'name': 'pos_sale_order',
    'widget': SaleOrderButton,
});

var SaleOrderPopupWidget = PopupWidget.extend({
    template: 'SaleOrderPopupWidget',
    events: _.extend({}, PopupWidget.prototype.events,{
        "keyup .order_date" : "date_validate",
    }),
    show: function(options){
        options = options || {};
        var self = this;
        this._super(options);

        this.list    = options.list    || [];
        this.renderElement();
    },
    click_cancel: function(){
        this.gui.close_popup();
    },

});


gui.define_popup({name:'pos_so_ref', widget: SaleOrderButton});
gui.define_popup({name:'pos_so', widget: SaleOrderPopupWidget});


});

