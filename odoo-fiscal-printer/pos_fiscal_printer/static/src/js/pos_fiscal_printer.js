odoo.define("pos_fiscal_printer.pos_fiscal_printer",function (require) {
    var core = require('web.core');
    var screens = require('point_of_sale.screens');
    var Session = require('web.Session');
    var Model = require('web.DataModel');
    var models = require("point_of_sale.models");
    var gui = require('point_of_sale.gui');
    var _t = core._t;
    var dict = []
        var _super_order_line = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
         get_tax_perc: function(){
            return this.get_all_prices().product_taxes;
         },
   	get_all_prices: function(){
		var price_unit = this.get_unit_price() * (1.0 - (this.get_discount() / 100.0));
		var taxtotal = 0;

		var product =  this.get_product();
		var taxes_ids = product.taxes_id;
		var taxes =  this.pos.taxes;
		var taxdetail = {};
		var product_taxes = [];

		_(taxes_ids).each(function(el){
		    product_taxes.push(_.detect(taxes, function(t){
			return t.id === el;
		    }));
		});

		console.log("ioooooooooooooooooooooooo",product_taxes)
		var all_taxes = this.compute_all(product_taxes, price_unit, this.get_quantity(), this.pos.currency.rounding);
		console.log("iooooooooooooooop5555555555>>>>>>>>>>>>",all_taxes)
		_(all_taxes.taxes).each(function(tax) {
		    taxtotal += tax.amount;
		    taxdetail[tax.id] = tax.amount;
		});

		return {
		    "priceWithTax": all_taxes.total_included,
		    "priceWithoutTax": all_taxes.total_excluded,
		    "tax": taxtotal,
		    "taxDetails": taxdetail,
		    "product_taxes":product_taxes,
		};
    	},
        export_for_printing: function(){
             var json = _super_order_line.export_for_printing.apply(this,arguments);
             json.get_tax_perc=  this.get_tax_perc();
             return json
        },
    });
    screens.ReceiptScreenWidget.include({
        print_xml: function() {
            var self = this;
            console.log("self::::::::::::::::",self)
//            .pos.pos_session.id
            var fiscal_pinter_data = {
                'order': this.pos.get_order(),
                'receipt': this.pos.get_order().export_for_printing(),
                'paymentlines': this.pos.get_order().get_paymentlines(),
            }
            console.log("iiiiiiiiiiiiiiiii",this.pos.get_order())
            console.log("RECEIPT :--------------------------",this.pos.get_order().export_for_printing())
            var ip = self.pos.config.proxy_ip ? self.pos.config.proxy_ip : '0.0.0.0:8069'
            self.connection = new Session(undefined,'http://'+ip, { use_cors: true});
            $.blockUI();
            var user_data = new Model('res.users')
            if(self.pos.get_client()){
                user_data.call('get_client_detail',[[self.pos.user.id],{'client_id':self.pos.get_client().id,'session_id':self.pos.pos_session.id}])
//                'session_id':self.pos.pos_session.id
                
                .then(function(result){
                    var printer_config= result[0].printer_config ? result[0].printer_config:false;
                    var printer_port = result[0].printer_port ? result[0].printer_port:false;
                    var printer_model = result[0].printer_model ? result[0].printer_model:false;
                    var partner_afip_code = result[0].partner_afip_code ? result[0].partner_afip_code:false;
                    var partner_code = result[0].partner_code ? result[0].partner_code:false;
                    var afip_responsability_type_id =result[0].afip_responsability_type_id?result[0].afip_responsability_type_id:false;
                    var id_number = result[0].id_number ? result[0].id_number:false;
                    var customer_name = result[0].customer_name ? result[0].customer_name:false;
                    var customer_address = result[0].customer_address ? result[0].customer_address:false;
                    var main_id_number = result[0].main_id_number ? result[0].main_id_number:false;
                    
                    console.log("afip_responsability_type_idafip_responsability_type_id",afip_responsability_type_id)
                    self.connection.rpc('/hw_proxy/fiscal_printer_print_xml_receipt',{receipt:fiscal_pinter_data,
                        printer_config:printer_config,
                        printer_port:printer_port,
                        printer_model:printer_model,
                        partner_afip_code:partner_afip_code,
                        partner_code:partner_code,
                        id_number:id_number,
                        customer_name:customer_name,
                        customer_address:customer_address,
                        main_id_number:main_id_number,
                        afip_responsability_type_id:afip_responsability_type_id
                        }).then(function(res){
                           $.unblockUI();
                           console.log("ioooooooooooooo>>>",res,self.pos.get_order())
                           if(self.pos.get_order() && self.pos.get_order().pos_order_id){
                               if(res.length > 0 ){
                               	console.log('RESSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS   : ',res)
                                   var pos_order_model = new Model('pos.order');
                                   pos_order_model.call("write",[self.pos.get_order().pos_order_id,{'receipt_number':res}]);
                               }
                           }
                        },function(){$.unblockUI();
                    });
                });
            }
            else{
                var ip = self.pos.config.proxy_ip ? self.pos.config.proxy_ip : '0.0.0.0:8069'
                self.connection = new Session(undefined,'http://'+ip, { use_cors: true});
                $.blockUI();
                var printer_config
                var printer_port 
                var printer_model;
                var dataset_model = new Model('res.users').call('read',[self.pos.user.id]).done(function(data){
                    printer_config= data[0].printer_config
                    printer_port = data[0].printer_port
                    printer_model = data[0].printer_model
                    self.connection.rpc('/hw_proxy/fiscal_printer_print_xml_receipt',{receipt:fiscal_pinter_data,
                        printer_config:printer_config,
                        printer_port:printer_port,
                        printer_model:printer_model}).then(function(res){
                            $.unblockUI();
                            if(self.pos.get_order() && self.pos.get_order().pos_order_id){
                                if(res.length > 0 ){
                                    var pos_order_model = new Model('pos.order');
                                    pos_order_model.call("write",[self.pos.get_order().pos_order_id,{'receipt_number':res}]);
                                    console.log("POS ORDER  ::::::::::::: ",res)
                                }
                            }
                         },function(){$.unblockUI();
                     });
                });
            }
            $.unblockUI();
            this.pos.get_order()._printed = true;
        },
    });

    models.PosModel = models.PosModel.extend({
        _save_to_server: function (orders, options) {
            if (!orders || !orders.length) {
                var result = $.Deferred();
                result.resolve([]);
                return result;
            }
            
            options = options || {};

            var self = this;
            var timeout = typeof options.timeout === 'number' ? options.timeout : 7500 * orders.length;

            // Keep the order ids that are about to be sent to the
            // backend. In between create_from_ui and the success callback
            // new orders may have been added to it.
            var order_ids_to_sync = _.pluck(orders, 'id');

            // we try to send the order. shadow prevents a spinner if it takes too long. (unless we are sending an invoice,
            // then we want to notify the user that we are waiting on something )
            var posOrderModel = new Model('pos.order');
//            var account_invoice_model = new Model('account.invoice');
//            
//            account_invoice_model.call('_get_document_type',[[]]).then(function(result3){
//            	console.log("+++++++CALLED+++++++++++++",result3)
//            })
            console.log("ddddddddddddddddddddddddddddddddd",self.config)
            return posOrderModel.call('create_from_ui',
                [_.map(orders, function (order) {
                    order.to_invoice = options.to_invoice || false;
                    return order;
                })],
                undefined,
                {
                    shadow: !options.to_invoice,
                    timeout: timeout
                }
            ).then(function (server_ids) {
                console.log("order_ids_to_syncorder_ids_to_sync",order_ids_to_sync)
                _.each(order_ids_to_sync, function (order_id) {
                    if(self.get_order().uid == order_id){
                        self.get_order().pos_order_id = server_ids;
                    }
                    self.db.remove_order(order_id);
                });
                self.set('failed',false);
                console.log("server_idsserver_idsserver_ids",server_ids)
                return server_ids;
            }).fail(function (error, event){
            	 console.log("fffffffffffffffff")
                if(error.code === 200 ){    // Business Logic Error, not a connection problem
                    //if warning do not need to display traceback!!
                    if (error.data.exception_type == 'warning') {
                       delete error.data.debug;
                    }

                    // Hide error if already shown before ... 
                    if ((!self.get('failed') || options.show_error) && !options.to_invoice) {
                        self.gui.show_popup('error-traceback',{
                            'title': error.data.message,
                           'body':  error.data.debug
                       });
                    }
                    self.set('failed',error)
                }
                // prevent an error popup creation by the rpc failure
                // we want the failure to be silent as we send the orders in the background
                event.preventDefault();
                console.error('Failed to send orders:', orders);
            });
        },
    });
});