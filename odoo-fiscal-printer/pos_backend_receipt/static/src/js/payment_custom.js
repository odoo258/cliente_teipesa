odoo.define('pos_backend_receipt.payment_custom',function(require){

    var screens = require('point_of_sale.screens');
    var Model = require('web.DataModel');
    var Session = require('web.Session');
    screens.PaymentScreenWidget.include({
        renderElement: function() {
            var self = this;
            this._super();
            this.$('.to_cancel').click(function(){
                self.print_pos_receipt('auto_cancel');
            });
            this.$('.report_z').click(function(){
                self.print_pos_receipt('report_z');
            });
            this.$('.report_x').click(function(){
                self.print_pos_receipt('report_x');
            });
//            this.$('.report_a').click(function(){
//                self.print_pos_receipt('receiptTypeA');
//                self.validate_order();
//            });
//            this.$('.report_b').click(function(){
//                self.print_pos_receipt('receiptTypeB');
//                self.validate_order();
//            });
//            this.$('.report_c').click(function(){
//                self.print_pos_receipt('receiptTypeC');
//                self.validate_order();
//            });

        },
        print: function(printer_ip,receipt, printer_config,printer_port,printer_model){
            var self = this;
            if(printer_ip){
                printer_ip = printer_ip ? printer_ip : '0.0.0.0:8069';
                self.connection = new Session(undefined,"http://"+printer_ip, { use_cors: true});
                $.blockUI();
                self.connection.rpc('/hw_proxy/fiscal_printer_print_xml_receipt',{receipt: receipt, printer_config:printer_config, printer_port:printer_port,printer_model:printer_model},{timeout: 5000}).then(function(){
                    $.unblockUI();
                },function(){$.unblockUI();});
            }
        },
        print_pos_receipt : function(type){
            var self = this;
                var state = $.bbq.getState(true);
                var dataset_model = new Model('account.invoice');
                dataset_model.call("get_printer_data",[state.id,type]).then(function(res){
                    self.print(res[1],res[0],res[2],res[3],res[4]);
                },function(){$.unblockUI();});
        },
    })

})