odoo.define('pos_val2text.val2text', function(require) {
    "use strict";
    var val2text = require('vitt_val2words.val2text');
    var screens = require('point_of_sale.screens');
    var models = require('point_of_sale.models');

    var _super_posmodel = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes) {
            this.val2text = new val2text.vitt_val2words();
            return _super_posmodel.initialize.call(this,session,attributes);
        },

        load_server_data: function(session, attributes){
            var self = this;
            for(var i=0; i<self.models.length; i++){
                var model=self.models[i];
                if(model.model === 'res.partner'){
                    model.fields.push('lang');
                }
                if(model.model === 'res.company'){
                    model.fields.push('val2words_default');
                }
            }
            console.log('self.models.push')
            self.models.push(
            {
                model: 'vitt_val2words.config_text',
                fields: ['id','name', 'company_id'],
                loaded: function(self,val2words){
                    self.val2words = val2words;
                    self.company.val2words_id = null;
                    for (var i = 0; i < val2words.length; i++) {
                        if (val2words[i].company_id[0] === self.company.id && val2words[i].id === self.company.val2words_default[0]){
                            self.company.val2words_id = val2words[i].id;
                        }
                    }
                }
            });

            return _super_posmodel.load_server_data.apply(this, session, attributes);

        },

    });


    var _super_order = models.Order.prototype;
    models.Order = models.Order.extend({

        get_total_amount_in_text: function(){
            return this.amount_in_text;
        },
    });

    screens.OrderWidget.include({
        update_summary: function(){
            var order = this.pos.get_order();
            if (!order.get_orderlines().length) {
                return;
            }
            var result = new $.Deferred();
            this._super();
            var total     = order ? order.get_total_with_tax() : 0;
            var taxes     = order ? total - order.get_total_without_tax() : 0;
            if (total || taxes) {
                var currency = (this.pos && this.pos.currency) ? this.pos.currency : {symbol:'$', position: 'after', rounding: 0.01, decimals: 2};
                var context = {};
                this.pos.val2text.vals2text(this.pos.company.val2words_id, total, currency)
                    .then(function(text){
                            result.resolve(text);
                            order.amount_in_text  = text;
                    });

            }
        },
    });

return {
}

});