/**
 * # -*- coding: utf-8 -*-
// ##############################################################################
// # For copyright and license notices, see __manifest__.py file in module root
// # directory
// ##############################################################################
 */

+(function ($) {
    'use strict';

    odoo.define('pos_sequence_ref_number',function (require) {
        var chrome = require('point_of_sale.chrome');
        var core = require('web.core');
        var devices = require('point_of_sale.devices');
        var gui = require('point_of_sale.gui');
        var models = require('point_of_sale.models');
        var screens = require('point_of_sale.screens');
        var popups = require('point_of_sale.popups');
        var Class = require('web.Class');
        var utils = require('web.utils');
        var PosBaseWidget = require('point_of_sale.BaseWidget');
        var PaymentScreenWidget = screens.PaymentScreenWidget;

        var _t = core._t,
            _lt = core._lt;

        var _sequence_next = function(seq, fiscal_seq){
            // var gui = require('point_of_sale.gui');
            var idict = {
                'year': moment().format('YYYY'),
                'month': moment().format('MM'),
                'day': moment().format('DD'),
                'y': moment().format('YY')
            };
            var format = function(s, dict){
                s = s || '';
                $.each(dict, function(k, v){
                    s = s.replace('%(' + k + ')s', v);
                });
                return s;
            };
            function pad(n, width, z) {
                z = z || '0';
                n = n + '';
                if (n.length < width) {
                    n = new Array(width - n.length + 1).join(z) + n;
                }
                return n;
            }
            var num = null;
            var prefix = null;
            var suffix = null;
            var padding = null;
            if (seq) {
                num = seq.number_next_actual;
                prefix = format(seq.prefix, idict);
                suffix = format(seq.suffix, idict);
                seq.number_next_actual += seq.number_increment;
                padding = seq.padding;
            }

            return prefix + pad(num, padding) + suffix;
        };

        var PosModelParent = models.PosModel;
                
        models.PosModel = models.PosModel.extend({
            load_server_data: function(session, attributes){
                var self = this;
                // Load POS sequence object
                self.models.push(
                {
                    model: 'ir.sequence',
                    fields: [],
                    ids:    function(self){
                        if (self.config.sequence_fiscal_id) {
                            return [self.config.sequence_fiscal_id[0]];
                        }
                        else {
                            return [];
                        }
                    },
                    loaded: function(self, sequence){ self.pos_order_sequence = sequence[0]; },
                },
                {
                    model: 'vitt_fiscal_seq.authorization_code',
                    fields: [],
                    ids:    function(self){
                        if (self.config.authorization_code_id) {
                            return [self.config.authorization_code_id[0]];
                        }
                        else {
                            return [];
                        }
                    },
                    loaded: function(self, authorization_code){ self.authorization_codes = authorization_code[0]; },
                },
                {
                    model: 'vitt_fiscal_seq.fiscal_sequence_regime',
                    fields: [],
                    'domain': function (self) {
                        if (self.config.sequence_fiscal_id) {
                            return [['sequence_id', '=', self.config.sequence_fiscal_id[0]]]; 
                        }
                        else {
                            return [['sequence_id', '=', null]];
                        }
                    },
                    loaded: function(self, fiscal_sequence_regime){ self.fiscal_sequence_regimes = fiscal_sequence_regime[0]; },
                },
                {
                    model: 'vitt_fiscal_seq.authorization_code_type',
                    fields: ['name'],
                    ids:    function(self){
                        if (self.config.sequence_fiscal_id) {
                            return [self.authorization_codes.code_type[0]];
                        }
                        else {
                            return [];
                        }
                    },
                    loaded: function(self, authorization_code_type){ self.authorization_code_types = authorization_code_type[0]; },
                }
                );
                return PosModelParent.prototype.load_server_data.apply(this, session, attributes);
            },
            // push_order: function(order) {
            //     if (order !== undefined) {
            //         var seq_next = _sequence_next(this.pos_order_sequence);
            //         order.set({'sequence_ref': seq_next});
            //         order.set({'vitt_min_value': this.pos_order_sequence.vitt_min_value});
            //         order.set({'vitt_max_value': this.pos_order_sequence.vitt_max_value});
            //         order.set({'expiration_date': this.pos_order_sequence.expiration_date});
            //         order.set({'fiscal_sequence_regime_ids': this.pos_order_sequence.fiscal_sequence_regime_ids[1]});
            //         order.set({'sequence_ref_number': this.pos_order_sequence.number_next_actual});
            //         order.set({'authorization_code_id': this.authorization_codes.name});
            //         order.set({'ac_code_type': this.authorization_code_types.name});
            //         order.set({'max_number': this.fiscal_sequence_regimes._to});
            //         order.set({'number_next_actual': this.pos_order_sequence.number_next_actual});
            //     }
            //     return PosModelParent.prototype.push_order.call(this, order);
            // },
        });

        var OrderParent = models.Order;
        models.Order = models.Order.extend({
            export_for_printing: function(attributes){
                var order = OrderParent.prototype.export_for_printing.apply(this, arguments);
                order['max_number'] = this.get('max_number');
                order['min_number'] = this.get('min_number');
                order['vitt_min_value'] = this.get('vitt_min_value');
                order['vitt_max_value'] = this.get('vitt_max_value');
                order['expiration_date'] = this.get('expiration_date');
                order['fiscal_sequence_regime_ids'] = this.get('fiscal_sequence_regime_ids');
                order['sequence_ref_number'] = this.get('sequence_ref_number');
                order['authorization_code_id'] = this.get('authorization_code_id');
                order['authorization_code'] = this.get('authorization_code');
                order['ac_code_type'] = this.get('ac_code_type');
                return order;
            },
            export_as_JSON: function() {
                var order = OrderParent.prototype.export_as_JSON.apply(this, arguments);
                order['max_number'] = this.get('max_number');
                order['min_number'] = this.get('min_number');
                order['vitt_min_value'] = this.get('vitt_min_value');
                order['vitt_max_value'] = this.get('vitt_max_value');
                order['expiration_date'] = this.get('expiration_date');
                order['fiscal_sequence_regime_ids'] = this.get('fiscal_sequence_regime_ids');
                order['sequence_ref'] = this.get('sequence_ref');
                order['sequence_ref_number'] = this.get('sequence_ref_number');
                order['authorization_code_id'] = this.get('authorization_code_id');
                order['authorization_code'] = this.get('authorization_code');
                order['ac_code_type'] = this.get('ac_code_type');
                return order;
            },
            _validate_sequence_next: function(order){
                var max_number =  this.pos.fiscal_sequence_regimes._to
                // var number_next_actual = this.pos.pos_order_sequence.number_next_actual
                var number_next_actual = this.get('sequence_ref_number') - 1;
                if (number_next_actual > max_number) {
                    return false;
                }
                return true;
            },
            _check_sequence_dates: function(order_date){
                var expiration_date = this.pos.pos_order_sequence.expiration_date
                var order_str = moment(order_date).format('L LT')
                var expiration_str = moment(expiration_date).format('L LT')
                var to_convert_str = '';
                var order_date_parts = '';
                var exp_date_parts = '';
                order_date_parts = order_str.substring(0,10).split('/');
                exp_date_parts = expiration_str.substring(0,10).split('/');
                var order_date = new Date(order_date_parts[2],order_date_parts[1]-1,order_date_parts[0]); 
                expiration_date = new Date(exp_date_parts[2],exp_date_parts[1]-1,exp_date_parts[0]); 
                if (order_date > expiration_date) {
                    return false;
                }

                return true;
            },

            _assign_fiscal_data: function(order){
                var seq_next = _sequence_next(this.pos.pos_order_sequence);
                var sequence_ref_number = this.get('sequence_ref_number');
                if (sequence_ref_number == null) {
                    order.set({'sequence_ref': seq_next});
                    order.set({'vitt_min_value': this.pos.pos_order_sequence.vitt_min_value});
                    order.set({'vitt_max_value': this.pos.pos_order_sequence.vitt_max_value});
                    order.set({'expiration_date': moment(this.pos.pos_order_sequence.expiration_date).format('L LT').substring(0,10)});
                    // order.set({'expiration_date': this.pos.pos_order_sequence.expiration_date});
                    order.set({'fiscal_sequence_regime_ids': this.pos.pos_order_sequence.fiscal_sequence_regime_ids[1]});
                    order.set({'sequence_ref_number': this.pos.pos_order_sequence.number_next_actual});
                    order.set({'authorization_code_id': this.pos.authorization_codes.id});
                    order.set({'authorization_code': this.pos.authorization_codes.name});
                    order.set({'ac_code_type': this.pos.authorization_code_types.name});
                    order.set({'min_number': this.pos.fiscal_sequence_regimes._from});
                    order.set({'max_number': this.pos.fiscal_sequence_regimes._to});
                    order.set({'number_next_actual': this.pos.pos_order_sequence.number_next_actual});
                    return order;
                }
                // return PosModelParent.prototype.push_order.call(this, order);
            },
        });

        PaymentScreenWidget.include({
            validate_order: function(force_validation) {
                var order = this.pos.get_order();
                var order_is_paid = order.is_paid();  //update next number when the order is paid

                if (this.pos.pos_order_sequence && order_is_paid === true) {
                    var order_next = order._assign_fiscal_data(order)
                    var seq_next = order._validate_sequence_next(order)
                    if (seq_next == false) {
                        this.gui.show_popup('error',{
                            'title': 'Error',
                            'body':  _t('No Numbers Available, The Sequence has been Completed'),
                        });
                        return false;
                    }
                    var check_date = order._check_sequence_dates(order.creation_date)
                    if (check_date == false) {
                        this.gui.show_popup('error',{
                            'title': 'Error',
                            'body':  _t('No Numbers Available in this date'),
                        });
                        return false;
                    }
                }
                this._super(force_validation);
            }
        });

    });

})(jQuery);
