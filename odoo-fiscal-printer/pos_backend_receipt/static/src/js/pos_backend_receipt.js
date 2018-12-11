odoo.define("pos_backend_receipt.pos_backend_receipt",function (require) {
    var core = require('web.core');
    var Model = require('web.DataModel');
    var Session = require('web.Session');
    var form_widgets = require("web.form_widgets");
    var QWeb = core.qweb;
    var _t = core._t;
    form_widgets.WidgetButton.include({
        print: function(printer_ip,receipt, printer_config,printer_port,printer_model,account_invoice=false){
            var self = this;
            if(printer_ip){
                printer_ip = printer_ip ? printer_ip : '0.0.0.0:8069';
                self.connection = new Session(undefined,"http://"+printer_ip, { use_cors: true});
                $.blockUI();
                self.connection.rpc('/hw_proxy/fiscal_printer_print_xml_backend_receipt',{receipt: receipt, 
                    printer_config:printer_config, 
                    printer_port:printer_port,
                    printer_model:printer_model,
                    account_invoice:account_invoice}).then(function(res){
                    $.unblockUI();
                    if(res && _.size(res) > 0 ){
                        var account_invoice_model = new Model('account.invoice');
                        account_invoice_model.call("write",[[res['id']],{'document_number':res['number']}]);
                    }
                },function(){$.unblockUI();});
            }
        },
        print_pos_receipt : function(type){
            var self = this;
            if(self.view && self.view.dataset && self.view.dataset.model){
                var state = $.bbq.getState(true);
                console.log(":::::::::::state:::::::::::::",self)
                $.blockUI();
                var dataset_model = new Model(self.view.dataset.model);
                dataset_model.call("get_printer_data",[state.id,type]).then(function(res){
                    var account_invoice = false;
                    if(self.view.dataset.model == "account.invoice"){
                        account_invoice ={'id': state.id,'model': self.view.dataset.model,
                                          'db':self.session.db,
                        }
                    }
                    $.unblockUI();
                    self.print(res[1],res[0],res[2],res[3],res[4],account_invoice);
                },function(){$.unblockUI();});
            }
        },
        on_click: function() {
        	console.log("==========================")
            var self = this;
            if(this.node && this.node.attrs && (this.node.attrs.type== 'printer' || this.node.attrs.type== 'auto_cancel' || this.node.attrs.type== 'report_x' || this.node.attrs.type== 'report_z') ){
                self.print_pos_receipt(this.node.attrs.type)
                return;
            }else{
                self._super();
            }
        },
    });
});
