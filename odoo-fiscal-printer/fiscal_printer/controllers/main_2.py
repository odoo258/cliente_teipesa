# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2017 Serpent Consulting Services Pvt. Ltd.
#    Copyright (C) 2017 OpenERP SA (<http://www.serpentcs.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import odoo.addons.hw_proxy.controllers.main as hw_proxy
from odoo import http, _
from odoo.http import controllers_per_module
from odoo.http import content_disposition, dispatch_rpc, request
import odoo
# import thread
# import time
import threading
from Queue import Queue
from threading import Thread, Lock
import logging
import sys

from multiprocessing.pool import ThreadPool

_logger = logging.getLogger(__name__)


class FiscalPrinterPoroxy(http.Controller):
    @http.route('/hw_proxy/fiscal_printer_print_xml_backend_receipt', type='json', auth='none',cors='*')  # For Backed End Model Receipt Print
    def fiscal_printer_print_xml_backend_receipt(self, receipt, printer_config, printer_port, printer_model,account_invoice=False):
        if receipt:
            mp = self.backendReceiptPrintConnection(receipt, printer_config, printer_port, printer_model,account_invoice)
            print 'POS BACKEND RECEIPT : -------------------------------------------------------', mp
            return mp
        else:
            return False

    def backendReceiptPrintConnection(self, receipt, printer_config, printer_port, printer_model,account_invoice):  # For Backed End Model Receipt Print
        if printer_port:
            if printer_model:
                model = printer_model
                if printer_config == 'panama':  # PANAMA CONFIGURATION
                    from panama.pyfiscalprinter_smh250f_panama.epsonFiscal import EpsonPrinter
                    printer = EpsonPrinter(deviceFile=printer_port, model=printer_model, dummy=False)
                    pool = ThreadPool(processes=1)
                    async_result = pool.apply_async(self.PrinterToPrintBackenedReceipt,
                                                    args=(printer, model, receipt, account_invoice))
                    return async_result.get()
                elif printer_config == 'argentina':  # ARGENTINA CONFIGURATION
                    from argentina.epsonfiscal import EpsonPrinter
                    printer = EpsonPrinter(deviceFile=printer_port, model=printer_model, dummy=False)
                    pool = ThreadPool(processes=1)
                    async_result = pool.apply_async(self.PrinterToPrintBackenedReceipt,
                                                    args=(printer, model, receipt, account_invoice))
                    return async_result.get()
                elif printer_config == 'chile':  # CHILE CONFIGURATION
                    from chile.pyfiscalprinter_smh250f_panama.epsonFiscal import EpsonChilePrinter
                    printer = EpsonChilePrinter(deviceFile=printer_port, model=printer_model, dummy=False)
                    pool = ThreadPool(processes=1)
                    async_result = pool.apply_async(self.PrinterToPrintBackenedReceipt,
                                                    args=(printer, model, receipt, account_invoice))
                    return async_result.get()
                else:  # Warning : ERROR IN THE COUNTRY CHOISE
                    _logger.warning('   Error in Print Country choise  ')
                    return False
            else:  # Warning : ERROR IN THE FISCAL MODEL
                _logger.warning(' Wrong Fiscal Model ')
                return False
        else:  # Warning : ERROR IN THE PRINTER PORT
            _logger.warning('  Wrong Printer Port ')
            return False

    def PrinterToPrintBackenedReceipt(self, printer, model, receipt,account_invoice):  # For Backed End Model Receipt Print
        models = ["tickeadoras", "epsonlx300+", "tm-220-af"]  # PRINTER MODELS
        productMake = []
        diffTotal=0
        number = 0
        # ResponsabilityType=''
        if type(receipt) is dict and receipt.get('report') == 'autocancelreceipt':
            printer.cancelAnyDocument()  # TO CANCEL RECEIPT
        elif type(receipt) is dict and receipt.get('report') == 'closingfiscalz':
            printer.dailyClose("Z")  # TO GENERATE REPORT 'Z'
        elif type(receipt) is dict and receipt.get('report') == 'closingfiscalx':
            printer.dailyClose("X")  # TO GENERATE REPORT 'X'
        elif type(receipt) is dict and receipt.get('report') == 'accountinovice':  # ACCOUNT INOVICE
            customer = receipt.get('customer_name') or "No Name"
            company = receipt.get('company')
            companyAddr = receipt.get('address')
            companyState = receipt.get('city')
            zip = receipt.get('zip')
            companyCountry = receipt.get('country')
            InvoiceNumber = receipt.get('number')
            Payment = receipt.get('PaymentTerms')
            InvoiceDate = receipt.get('invoice_date')
            Salesperson = receipt.get('Salesperson')
            Orgprice = receipt.get('Orgprice')
            taxprice = receipt.get('taxprice')
            total = receipt.get('total')
            DocumentName = receipt.get('DocumentName')  # DOCUMENT TYPE FOR INVOICE
            InvoiceType = receipt.get("InvoiceType")
            IsCreditInovice = receipt.get("IsCreditInovice")
            InvoiceType = (InvoiceType.replace(" ", "_")).upper()  # INOVICE DOCUMENT TYPE
            DocumentCode = receipt.get('DocumentCode')
            total_with_tax = receipt.get("amount_total") or 0
            printer.DocumentCode(DocumentCode)
            if DocumentCode == "CUIT":
                RegTaxNumber = receipt.get('RegTaxNumber')  # REGISTERED  TAX NUMBER
                printer.RegisteredTaxNumber(RegTaxNumber)
            InvoiceNumb = receipt.get('InvoiceNumber')  # TICKET NUMBER
            address = str(companyAddr) + ',' + str(companyState) + ',' + str(zip) + ',' + str(companyCountry)  # ADDRESS
            ivaTypeMap = {
                            'IVA_RESPONSABLE_INSCRIPTO': 'I',
                            'RESPONSABLE_NO_INSCRIPTO': 'R',
                            'EXENTO': 'E',
                            'IVA_SUJETO_EXENTO': 'E',
                            'IVA_NO_RESPONSABLE': 'N',
                            'CONSUMIDOR_FINAL': 'F',
                            'RESPONSABLE_NO_INSCRIPTO_BIENES_DE_USO': 'R',
                            'RESPONSABLE_MONOTRIBUTO': 'M',
                            'MONOTRIBUTISTA_SOCIAL': 'M',
                            'PEQUENIO_CONTRIBUYENTE_EVENTUAL': 'C',
                            'PEQUENIO_CONTRIBUYENTE_EVENTUAL_SOCIAL': 'V',
                            'NO_CATEGORIZADO': 'S',
                         }
            PrinterType = ivaTypeMap.get(InvoiceType)
            if receipt.get('receipt_type') == 'B':  # FOR THE INVOICE TYPE 'B' # POS RECEIPT
                FinalPrinterType = PrinterType or "F"
                if model in models:
                    if IsCreditInovice == "invoice":
                        number = printer.getLastNumber("B") + 1
                        printer.openBillTicket("B", customer, address, "0",
                                               DocumentCode,  # printer.DOC_TYPE_SIN_CALIFICADOR,
                                               FinalPrinterType)
                    elif IsCreditInovice == "credit_note":  # TO PRINT CREDIT NOTES
                        number = printer.getLastCreditNoteNumber("B") + 1
                        printer.openBillCreditTicket("B", customer, address, "0",
                                                     DocumentCode,  # printer.DOC_TYPE_SIN_CALIFICADOR,
                                                     FinalPrinterType)
                    else:
                        number = printer.getLastNumber("B") + 1
                        printer.openBillTicket("B", customer, address, "0",
                                               DocumentCode,  # printer.DOC_TYPE_SIN_CALIFICADOR,
                                               FinalPrinterType)
            elif receipt.get('receipt_type') == 'A':  # FOR THE CUSTOMER RECEIPT TYPE 'A'
                number = printer.getLastNumber("A") + 1
                FinalPrinterType = PrinterType or "I"
                if model in model:  # For Backed End Model Receipt Prints:
                    if IsCreditInovice == "invoice":  # TO PRINT RECEIPT TYPE 'A'
                        number = printer.getLastNumber("A") + 1
                        printer.openBillTicket("A", customer, address, "0",printer.DOC_TYPE_CUIT,FinalPrinterType)
                    elif IsCreditInovice == "credit_note":
                        number = printer.getLastCreditNoteNumber("A") + 1
                        printer.openBillCreditTicket("A", customer, address, "0",printer.DOC_TYPE_CUIT,FinalPrinterType)
                    else:
                        number = printer.getLastNumber("A") + 1
                        printer.openBillTicket("A", customer, address, "0",printer.DOC_TYPE_CUIT,FinalPrinterType)
            else:
                number = printer.getLastNumber("B") + 1  # FOR THE TICKET TYEP 'C'
                printer.openTicket()  # OPEN FOR TAX DOCUMENT
            ##########################################################################################################
            if receipt.get('receipt_type') == 'B':
                for data in receipt.get('product'):
                    if type(data) is dict:
                        tax = data.get('tax') or 0
                        product = data.get('product') or 0
                        discount = data.get('discount') or 0
                        price = data.get('price') or 0
                        price = float("%0.2f" % (price))
                        quantity = data.get('quantity') or 0
                        discountDescription = ''
                        try:    # 'B' AND 'C' TYPE RECEIPT

                            if tax:
                                ivaprice = price * ((float(tax) / 100.00) + 1)  # VAT CALCUTLATION
                                ivaprice = float("%0.2f" % (ivaprice))
                                if discount > 0:  # DISCOUNT CALCULATION
                                    discountstr = float("%0.2f"%((discount * float(ivaprice) * quantity) / 100.00))
                                    print 'discountstr : ',discountstr
                                    discountPrice = float(ivaprice * quantity)
                                    totalPrice = float(discountPrice - discountstr)
                                    diffTotal += float(totalPrice)
                                elif discount < 0:  # SURCHARGE CALCULATION
                                    discountstr = float("%0.2f"%(price * (float(abs(discount)) / 100.00) * quantity * ((float(tax) / 100.00) + 1)))
                                    discountPrice = float(ivaprice * quantity)
                                    totalPrice = float(discountPrice - discountstr)
                                    diffTotal += float(totalPrice)
                                elif discount == 0:
                                    discountPrice = float(ivaprice * quantity)
                                    diffTotal += float(discountPrice)
                            else:
                                price = price
                                if discount > 0:
                                    discountstr = float("%0.2f"%((discount * float(price) * quantity) / 100.00))
                                    discountPrice = float(price * quantity)
                                    totalPrice = float(discountPrice - discountstr)
                                    diffTotal += float(totalPrice)
                                elif discount < 0:
                                    discountstr = float("%0.2f"%((abs(discount) * float(price) * quantity) / 100.00))
                                    discountPrice = float(price * quantity)
                                    totalPrice = float(discountPrice + discountstr)
                                    diffTotal += float(totalPrice)
                                elif discount == 0:
                                    discountPrice = float(price * quantity)
                                    diffTotal += float(discountPrice)
                        except Exception as e:
                            _logger.error("Error :  " + str(e))
                try:  # Exceptional price
                    if productMake:
                        sum = 0
                        for ExceptPrice in productMake:
                            if ExceptPrice:
                                ExceptPrice = float("%0.5s" % str(ExceptPrice))
                                sum = sum + float(ExceptPrice)
                        diffTotal += float(sum)
                except:
                    pass
                try:  # PERCEPTION
                    for percept in receipt.get("perception"):
                        if type(percept) is dict:
                            if percept.get("receipttype") == "perception":
                                if receipt.get("receipt_type") == 'B':
                                    diffTotal += float(percept.get("percpt_amount"))
                except:
                    pass

            ##########################################################################################################

#######*****************************************************************************************************
            if receipt.get('receipt_type') == 'B':
                if receipt.get('product')[:-1]:
                    for data in receipt.get('product')[:-1]:
                        if type(data) is dict:
                            tax = data.get('tax') or 0
                            product = data.get('product') or 0
                            discount = data.get('discount') or 0
                            price = data.get('price') or 0
                            price = float("%0.2f" % (price))
                            quantity = data.get('quantity') or 0
                            discountDescription = ''
                            try: # FOR RECEIPT TYPE B/C
                                if tax:
                                    ivaprice = price * ((float(tax) / 100.00) + 1)  # VAT CALCUTLATION
                                    ivaprice = float("%0.2f" % (ivaprice))
                                    if discount > 0:  # DISCOUNT CALCULATION
                                        discountstr = float("%0.2f"%((discount * float(ivaprice) * quantity) / 100.00))
                                        discountDescription = "%s" % discount + "%" + " Discount "
                                        printer.addItem(product, quantity, ivaprice, tax, discountstr, discountDescription)
                                    elif discount < 0:  # SURCHARGE CALCULATION
                                        discountstr = float("%0.2f"%(price * (float(discount) / 100.00) * quantity * ((float(tax) / 100.00) + 1)))
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                        printer.addItem(product, quantity, ivaprice, tax, discountstr, discountDescription)
                                    elif discount == 0:
                                        printer.addItem(product, quantity, ivaprice, tax, discount, discountDescription)
                                else:
                                    price = price
                                    if discount > 0:
                                        discountstr = float("%0.2f"%((discount * float(price) * quantity) / 100.00))
                                        discountDescription = "%s" % discount + "%" + " Discount "
                                        printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                    elif discount < 0:
                                        discountstr = float("%0.2f"%((discount * float(price) * quantity) / 100.00))
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                        printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                    elif discount == 0:
                                        printer.addItem(product, quantity, price, tax, discount, discountDescription)
                            except Exception as e:
                                _logger.error("Error :  " + str(e))
                                printer.cancelAnyDocument()  # TO CANCEL ANY DOCUMENT //    # printer.close()


                if receipt.get('product')[-1:]:
                    for data in receipt.get('product')[-1:]:
                        if type(data) is dict:
                            tax = data.get('tax') or 0
                            product = data.get('product') or 0
                            discount = data.get('discount') or 0
                            price = data.get('price') or 0
                            price = float("%0.2f" % (price))
                            quantity = data.get('quantity') or 0
                            discountDescription = ''
                            if tax:
                                ivaprice = price * ((float(tax) / 100.00) + 1)  # VAT CALCUTLATION
                                ivaprice = float("%0.2f" % (ivaprice))
                                if discount > 0:  # DISCOUNT CALCULATION
                                    discountstr = float("%0.2f" % ((discount * float(ivaprice) * quantity) / 100.00))
                                    # discountDescription = "%s" % discount + "%" + " Discount "
                                    if diffTotal and total_with_tax:
                                        if float(total_with_tax) > float(diffTotal):
                                            outprice = float("%0.2f" % (float(total_with_tax) - float(diffTotal)))
                                            DiscountStr = float(str("%0.2f" % (float(abs(float(abs(discountstr)) - float(abs(outprice)))))))
                                            discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                            printer.addItem(product, quantity, ivaprice, tax, DiscountStr, discountDescription)
                                        else:
                                            outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                            if outprice:
                                                DiscountStr = float(str("%0.2f" % (float(abs(abs(discountstr)) + float(abs(outprice))))))
                                                discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                                printer.addItem(product, quantity, ivaprice, tax, DiscountStr, discountDescription)
                                            else:
                                                discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                                printer.addItem(product, quantity, ivaprice, tax, discountstr, discountDescription)
                                    else:
                                        # discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                        printer.addItem(product, quantity, ivaprice, tax, discountstr, discountDescription)



                                elif discount < 0:  # SURCHARGE CALCULATION
                                    discountstr = float("%0.2f" % (price * (float(discount) / 100.00) * quantity * ((float(tax) / 100.00) + 1)))
                                    # discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                    if diffTotal and total_with_tax:
                                        if float(total_with_tax) > float(diffTotal):
                                            outprice = float("%0.2f" % (float(total_with_tax) - float(diffTotal)))
                                            DiscountStr = float("-" + str("%0.2f" % (float(abs(float(abs(discountstr)) - float(abs(outprice)))))))
                                            discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                            printer.addItem(product, quantity, ivaprice, tax, DiscountStr, discountDescription)
                                        else:
                                            outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                            if outprice:
                                                DiscountStr = float("-" + str("%0.2f" % (float(abs(abs(discountstr)) + float(abs(outprice))))))
                                                discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                                printer.addItem(product, quantity, ivaprice, tax, DiscountStr, discountDescription)
                                            else:
                                                discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                                printer.addItem(product, quantity, ivaprice, tax, discountstr, discountDescription)
                                    else:
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                        printer.addItem(product, quantity, ivaprice, tax, discountstr, discountDescription)

                                elif discount == 0:
                                    if diffTotal and total_with_tax:
                                        if float(total_with_tax) > float(diffTotal):
                                            outprice = float("-" + str("%0.2f" % (float(total_with_tax) - float(diffTotal))))
                                            discountDescription = " Surcharge "
                                            printer.addItem(product, quantity, ivaprice, tax, outprice, discountDescription)
                                        else:
                                            outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                            if outprice:
                                                discountDescription = " Discount "
                                                printer.addItem(product, quantity, ivaprice, tax, outprice, discountDescription)
                                            else:
                                                printer.addItem(product, quantity, ivaprice, tax, discount, discountDescription)
                                    else:
                                        printer.addItem(product, quantity, ivaprice, tax, discount, discountDescription)
                            else:
                                price = price
                                if discount > 0:
                                    discountstr = float("%0.2f" % ((discount * float(price) * quantity) / 100.00))
                                    # discountDescription = "%s" % discount + "%" + " Discount "
                                    # printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                    if diffTotal and total_with_tax:
                                        if float(total_with_tax) > float(diffTotal):
                                            outprice = float("%0.2f" % (float(total_with_tax) - float(diffTotal)))
                                            DiscountStr = float(str("%0.2f" % (float(abs(float(abs(discountstr)) - float(abs(outprice)))))))
                                            discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                            printer.addItem(product, quantity, price, tax, DiscountStr, discountDescription)
                                        else:
                                            outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                            if outprice:
                                                DiscountStr = float(str("%0.2f" % (float(abs(abs(discountstr)) + float(abs(outprice))))))
                                                discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                                printer.addItem(product, quantity, price, tax, DiscountStr, discountDescription)
                                            else:
                                                discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                                printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                    else:
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                        printer.addItem(product, quantity, price, tax, discountstr, discountDescription)

                                elif discount < 0:
                                    discountstr = float("%0.2f" % ((discount * float(price) * quantity) / 100.00))
                                    # discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                    # printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                    if diffTotal and total_with_tax:
                                        if float(total_with_tax) > float(diffTotal):
                                            outprice = float("%0.2f" % (float(total_with_tax) - float(diffTotal)))
                                            DiscountStr = float("-" + str("%0.2f" % (float(abs(float(abs(discountstr)) - float(abs(outprice)))))))
                                            discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                            printer.addItem(product, quantity, price, tax, DiscountStr, discountDescription)
                                        else:
                                            outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                            if outprice:
                                                DiscountStr = float("-" + str("%0.2f" % (float(abs(abs(discountstr)) + float(abs(outprice))))))
                                                discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                                printer.addItem(product, quantity, price, tax, DiscountStr, discountDescription)
                                            else:
                                                discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                                printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                    else:
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                        printer.addItem(product, quantity, price, tax, discountstr, discountDescription)

                                elif discount == 0:
                                    if diffTotal and total_with_tax:
                                        if float(total_with_tax) > float(diffTotal):
                                            outprice = float("-" + str("%0.2f" % (float(total_with_tax) - float(diffTotal))))
                                            discountDescription = " Surcharge "
                                            printer.addItem(product, quantity, price, tax, outprice, discountDescription)
                                        else:
                                            outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                            if outprice:
                                                discountDescription = " Discount "
                                                printer.addItem(product, quantity, price, tax, outprice, discountDescription)
                                    else:
                                        printer.addItem(product, quantity, price, tax, discount, discountDescription)
                                    # printer.addItem(product, quantity, price, tax, discount, discountDescription)
#######*****************************************************************************************************
            else:
                for data in receipt.get('product'):
                    if type(data) is dict:
                        tax = data.get('tax') or 0
                        product = data.get('product') or 0
                        discount = data.get('discount') or 0
                        price = data.get('price') or 0
                        price = float("%0.2f" % (price))
                        quantity = data.get('quantity') or 0
                        discountDescription = ''
                        if receipt.get('receipt_type') == 'A':  # RECEIPT TYPE 'A'
                            if discount > 0:  # DISCOUNT CALCULATION
                                discountstr = float("%0.2f"%((discount * price * quantity) / 100.00))
                                discountDescription = "%s" % discount + "%" + " Discount "
                                printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                            elif discount < 0:  # SURCHARGE CALCULATION
                                discountstr = float("%0.2f"%(price * (float(discount) / 100.00) * quantity))
                                discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                            elif discount == 0:
                                printer.addItem(product, quantity, price, tax, discount, discountDescription)
                        else:  # 'B' AND 'C' TYPE RECEIPT
                            try:
                                if tax:
                                    ivaprice = price * ((float(tax) / 100.00) + 1)  # VAT CALCUTLATION
                                    ivaprice = float("%0.2f" % (ivaprice))
                                    if discount > 0:  # DISCOUNT CALCULATION
                                        discountstr = float("%0.2f"%((discount * float(ivaprice) * quantity) / 100.00))
                                        discountDescription = "%s" % str(discount) + "%" + " Discount "
                                        printer.addItem(product, quantity, ivaprice, tax, discountstr, discountDescription)
                                    elif discount < 0:  # SURCHARGE CALCULATION
                                        discountstr = float("%0.2f"%(price * (float(discount) / 100.00) * quantity * ((float(tax) / 100.00) + 1)))
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                        printer.addItem(product, quantity, ivaprice, tax, discountstr, discountDescription)
                                    elif discount == 0:
                                        printer.addItem(product, quantity, ivaprice, tax, discount, discountDescription)
                                else:
                                    price = price
                                    if discount > 0:
                                        discountstr = float("%0.2f"%((discount * float(price) * quantity) / 100.00))
                                        discountDescription = "%s" % str(discount) + "%" + " Discount "
                                        printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                    elif discount < 0:
                                        discountstr = float("%0.2f"%((discount * float(price) * quantity) / 100.00))
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                        printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                    elif discount == 0:
                                        printer.addItem(product, quantity, price, tax, discount, discountDescription)
                            except Exception as e:
                                _logger.error("Error :  " + str(e))
                                printer.cancelAnyDocument()  # TO CANCEL ANY DOCUMENT //    # printer.close()

            # try:
            #     if receipt.get('receipt_type') == 'B':
            #         if diffTotal and total_with_tax:
            #             if float(total_with_tax) > float(diffTotal):
            #                  outprice = float("%0.2f"%(float(total_with_tax)-float(diffTotal)))
            #                  printer.addToTotal("Exceptional Price", 1, outprice, 0, 0, '')
            #                  print ' Addition Difference with Total   : ---------',outprice
            #                  print 'Total : ',total_with_tax
            #                  print 'Receipt Total :',diffTotal
            #             else:
            #                  outprice = float("%0.2f"%(float(diffTotal)-float(total_with_tax)))
            #                  if outprice:
            #                     printer.SubToTotal("Exceptional Price",  1, outprice, 0, 0, '')
            #                     print 'Subtraction Difference with total : --------- ',outprice
            #                     print 'Total : ', total_with_tax
            #                     print 'Receipt Total :', diffTotal
            # except:
            #     pass

            try:  # Exceptional price
                if productMake:
                    sum = 0
                    for ExceptPrice in productMake:
                        if ExceptPrice:
                            ExceptPrice = float("%0.5s" % str(ExceptPrice))
                            sum = sum + float(ExceptPrice)
                            print 'Exceptional Prices :   ------------------------------------------- ', ExceptPrice
                    print 'Sum :  --------------- ', sum
                    printer.addItem('Exceptional Price', 1, float(sum), 0, 0, '')
            except:
                pass

            try:  # PERCEPTION
                for percept in receipt.get("perception"):
                    if type(percept) is dict:
                        if percept.get("receipttype") == "perception":
                            if receipt.get("receipt_type") == 'A':
                                printer.AddPerception(percept.get("percpt_text"), percept.get("percpt_amount"),percept.get("percpt_tax"))
                            elif receipt.get("receipt_type") == 'B':
                                printer.AddPerception(percept.get("percpt_text"), percept.get("percpt_amount"),percept.get("percpt_tax"))
                            else:
                                quantity = 1
                                discountstr = 0
                                discountDescription = ''
                                printer.addItem(percept.get("percpt_text"), quantity, percept.get("percpt_amount"),percept.get("percpt_tax"), discountstr, discountDescription)
            except:
                pass

            try:
                printer.closeDocument()  # printer.close()
            except Exception as e:
                _logger.error("Error :  " + str(e))
        else:
            _logger.warning("Unknown receipt type")  # UNKONWN RECEIPT TYPE

        if number:
            if account_invoice:
                number = "0020-" + ((8 - int(len(str(number)))) * "0") + str(number)
                account_invoice.update({'number': str(number)})
                return account_invoice
        else:
            return False

    @http.route('/hw_proxy/fiscal_printer_print_xml_receipt', type='json', auth='none', cors='*')
    def fiscal_printer_print_xml_receipt(self, receipt, printer_config, printer_port, printer_model,partner_afip_code=False, partner_code=False, id_number=False,customer_name=False, customer_address=False, main_id_number=False,afip_responsability_type_id=False):  # For pos front end receipt print
        if receipt:
            mp = self.printconnection(receipt, printer_config, printer_port, printer_model, partner_afip_code,partner_code, id_number, customer_name, customer_address, main_id_number,afip_responsability_type_id)
            print '>>>>>>>>fRontEnfddd>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>5252', mp
            return mp
        else:
            return False

    def printconnection(self, receipt, printer_config, printer_port, printer_model, partner_afip_code, partner_code,id_number, customer_name, customer_address, main_id_number, afip_responsability_type_id):
        if printer_port:
            if printer_model:
                model = printer_model
                if printer_config == 'panama':
                    from panama.pyfiscalprinter_smh250f_panama.epsonFiscal import EpsonPrinter
                    printer = EpsonPrinter(deviceFile=printer_port, model=printer_model, dummy=False)
                    pool = ThreadPool(processes=1)
                    async_result = pool.apply_async(self.PrinterToPrint, args=(printer, model, receipt, partner_afip_code, partner_code, id_number, customer_name,customer_address, main_id_number, afip_responsability_type_id))
                    return async_result.get()
                elif printer_config == 'argentina':
                    from argentina.epsonfiscal import EpsonPrinter
                    printer = EpsonPrinter(deviceFile=printer_port, model=printer_model, dummy=False)
                    pool = ThreadPool(processes=1)
                    async_result = pool.apply_async(self.PrinterToPrint, args=(printer, model, receipt, partner_afip_code, partner_code, id_number, customer_name,customer_address, main_id_number, afip_responsability_type_id))
                    return async_result.get()
                elif printer_config == 'chile':
                    from chile.pyfiscalprinter_smh250f_panama.epsonFiscal import EpsonChilePrinter
                    printer = EpsonChilePrinter(deviceFile=printer_port, model=printer_model, dummy=False)
                    pool = ThreadPool(processes=1)
                    async_result = pool.apply_async(self.PrinterToPrint, args=(printer, model, receipt, partner_afip_code, partner_code, id_number, customer_name,customer_address, main_id_number, afip_responsability_type_id))
                    return async_result.get()
                else:
                    _logger.warning('   Error in Print Country choise  ')
                    return False
            else:
                _logger.warning(' Wrong Fiscal Model ')
                return False
        else:
            _logger.warning('  Wrong Printer Port ')
            return False

    def PrinterToPrint(self, printer, model, receipt, partner_afip_code, partner_code, id_number, customer_name, customer_address, main_id_number, afip_responsability_type_id):
        models = ["tickeadoras", "epsonlx300+", "tm-220-af"]
        perception = []
        postax = []
        productMake = []
        diffTotal = 0
        pos_receipt = 0
        receipt_type = ''
        # ResponsabilityType = ''
        if type(receipt) is dict and receipt.get('report') == 'autocancelreceipt':
            printer.cancelAnyDocument()
        elif type(receipt) is dict and receipt.get('report') == 'closingfiscalz':
            printer.dailyClose("Z")
        elif type(receipt) is dict and receipt.get('report') == 'closingfiscalx':
            printer.dailyClose("X")
        elif type(receipt) is dict and receipt['receipt']['orderlines']:
            partner_afip_code = partner_afip_code or ''
            partner_code = partner_code or 0
            id_number = id_number or 0
            customer_name = customer_name or ''
            customer_address = customer_address
            ResponsabilityType = ''
            if partner_code:
                if model in models:
                    if afip_responsability_type_id:
                        InvoiceType = (afip_responsability_type_id.replace(" ", "_")).upper()
                        ivaTypeMap = {
                                        'IVA_RESPONSABLE_INSCRIPTO': 'I',
                                        'RESPONSABLE_NO_INSCRIPTO': 'R',
                                        'EXENTO': 'E',
                                        'IVA_SUJETO_EXENTO': 'E',
                                        'IVA_NO_RESPONSABLE': 'N',
                                        'CONSUMIDOR_FINAL': 'F',
                                        'RESPONSABLE_NO_INSCRIPTO_BIENES_DE_USO': 'R',
                                        'RESPONSABLE_MONOTRIBUTO': 'M',
                                        'MONOTRIBUTISTA_SOCIAL': 'M',
                                        'PEQUENIO_CONTRIBUYENTE_EVENTUAL': 'C',
                                        'PEQUENIO_CONTRIBUYENTE_EVENTUAL_SOCIAL': 'V',
                                        'NO_CATEGORIZADO': 'S',
                                     }
                        ResponsabilityType = ivaTypeMap.get(InvoiceType)
                        print 'ResponsabilityType : ------------------------------------------------', ResponsabilityType
                        if ResponsabilityType == 'I':  # RECEIPT TYPE 'A'
                            if id_number:
                                printer.RegisteredTaxNumber(id_number)
                            pos_receipt = printer.getLastNumber("A") + 1
                            printer.openBillTicket("A", customer_name, customer_address, "0",printer.DOC_TYPE_CUIT,ResponsabilityType)
                        elif ResponsabilityType == 'F' or 'M' or 'E' or 'N':  # RECEIPT TYPE 'B'
                            receipt_type = ResponsabilityType
                            if id_number:
                                printer.RegisteredTaxNumber(id_number)
                            pos_receipt = printer.getLastNumber("B") + 1
                            printer.openBillTicket("B", customer_name or " ", customer_address or " ", "0",partner_code,ResponsabilityType)
            else:
                pos_receipt = printer.getLastNumber("B") + 1
                printer.openTicket()
            ticketnumer = receipt['receipt']['name']  # REGISTERED  TAX NUMBER
            company = receipt['receipt']['company']['name']
            contact_address = receipt['receipt']['company']['contact_address']
            company_email = receipt['receipt']['company']['website']
            company_email = receipt['receipt']['company']['email']
            company_phone = receipt['receipt']['company']['phone']
            orderNum = receipt['receipt']['name']
            user = receipt['receipt']['cashier']
            datetimez = str(receipt['receipt']['date']['localestring'])
            subtotalmoney = receipt['receipt']['subtotal']
            changeMoney = receipt['receipt']['change']
            paidMoney = receipt['receipt']['total_paid']
            paymentlines_list = receipt['receipt']['paymentlines']
            total_with_tax = receipt['receipt']['total_with_tax']
            total_discount = round(receipt['receipt']['total_discount'], 2)
            taxDetails = receipt['receipt']['tax_details']  ### TAX DETAILS
            # print 'taxDetails :------------------------------------------------',taxDetails
            perceptionTaxs = ['P.IIBB', 'P.GAN', 'P.IVA']
            for taxs in taxDetails:
                postax.append(taxs['tax']['amount'])
                taxname = taxs['tax']['name']
                for perceptTax in perceptionTaxs:
                    if taxname == perceptTax:
                        perception.append({'tax': taxs.get('amount'), 'name': taxs['tax']['name'],'taxamount': taxs['tax']['amount']})
            # test = 0
            # print 'Receipt : -----------------------',receipt['receipt']


            ############################################################
            if receipt_type:
            # if ResponsabilityType == 'F' or 'M' or 'E' or 'N':
                for products in receipt['receipt']['orderlines']:
                    product = products.get('product_name') or 0
                    quantity = products.get('quantity') or 0
                    price_org = products.get('price') or 0
                    print "PRICE :--------------",price_org
                    price_org = float("%0.2f" % (price_org))
                    print "PRICE (FLOAT) :--------------", price_org
                    discount = products.get('discount') or 0
                    discountDescription = ''
                    tax_id = products.get('tax')
                    tax = products['get_tax_perc'][0].get('amount') or 0
                    try:
                          # FOR RECEIPT TYPE B/C
                        if tax:
                            price = price_org * ((float(tax) / 100.00) + 1)
                            price = float("%0.2f" % (price))
                            print 'PIRCE WITH VAT ',str(price)
                        else:
                            price = float("%0.2f" % (price_org))
                            print 'PRICE WITH TAX :---------------------------------------', price
                        if discount > 0:
                            discountstr = float("%0.2f"%((discount * price * quantity) / 100.00))
                            discountPrice = float(price * quantity)
                            print 'DiscountPrice (TAX) : ---- ',discountPrice
                            totalPrice = float(discountPrice - discountstr)
                            diffTotal+=float(totalPrice)
                            print 'TotalPrice (TAX) : ---- ',str(totalPrice)
                            print  'discountstrdiscountstr   :  -------- ',discountstr,type(discountstr)
                            print  'DiscountPrice (TAX) : ------------',discountPrice,type(discountPrice)
                            print 'discountstr', str(discountstr)
                        elif discount < 0:
                            discountstr = float("%0.2f"%(price * (float(abs(discount)) / 100.00) * quantity))
                            discountPrice = float(price * quantity)
                            print 'DiscountPrice (TAX) : ---- ', discountPrice
                            totalPrice = float(discountPrice - discountstr)
                            diffTotal += float(totalPrice)
                            print 'discountPrice  : ---- ', discountPrice
                            print 'discountstr',str(discountstr)
                        elif discount == 0:
                            discountPrice = float(price * quantity)
                            diffTotal +=float(discountPrice)
                            print 'discountPrice  : ---- ', discountPrice
                    except Exception as e:
                        _logger.error("Error :  " + str(e))
                try:
                    if productMake:
                        sum = 0
                        for ExceptPrice in productMake:
                            if ExceptPrice:
                                sum = sum + float(ExceptPrice)
                                print 'Exceptional Prices :   ------------------------------------------- ', ExceptPrice
                        print 'SUM :-------------', str(float(sum))
                except:
                    pass
                try:
                    if perception:
                        for perceptTax in perception:
                            diffTotal+=float(perceptTax.get("tax"))
                except:
                    pass




            ############################################################



################**************************************************************
            if receipt_type:
                if receipt['receipt']['orderlines'][:-1]:
                    for products in receipt['receipt']['orderlines'][:-1]:
                        ### PRODUCT DETAILS
                        product = products.get('product_name') or 0
                        quantity = products.get('quantity') or 0
                        price_org = products.get('price') or 0
                        print "PRICE :--------------",price_org
                        price_org = float("%0.2f" % (price_org))
                        print "PRICE (FLOAT) :--------------", price_org
                        discount = products.get('discount') or 0
                        discountDescription = ''
                        tax_id = products.get('tax')
                        tax = products['get_tax_perc'][0].get('amount') or 0
                        try:
                                # FOR RECEIPT TYPE B/C
                                if tax:
                                    price = price_org * ((float(tax) / 100.00) + 1)
                                    price = float("%0.2f" % (price))
                                else:
                                    price = float("%0.2f" % (price_org))
                                if discount > 0:
                                    discountstr = float("%0.2f"%((discount * price * quantity) / 100.00))
                                    discountDescription = "%s" % discount + "%" + " Discount "
                                    printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                elif discount < 0:
                                    discountstr = float("%0.2f"%(price * (float(discount) / 100.00) * quantity))
                                    discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                    print 'discountstr',str(discountstr)
                                    printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                                elif discount == 0:
                                    printer.addItem(product, quantity, price, tax, discount, discountDescription)
                        except Exception as e:
                            _logger.error("Error :  " + str(e))
                            printer.cancelAnyDocument()

                if receipt['receipt']['orderlines'][-1:]:
                    for products in receipt['receipt']['orderlines'][-1:]:

                        print 'YOU ARE AT -1 line'
                        product = products.get('product_name') or 0
                        quantity = products.get('quantity') or 0
                        price_org = products.get('price') or 0
                        print "PRICE :--------------", price_org
                        price_org = float("%0.2f" % (price_org))
                        print "PRICE (FLOAT) :--------------", price_org
                        discount = products.get('discount') or 0
                        discountDescription = ''
                        tax_id = products.get('tax')
                        tax = products['get_tax_perc'][0].get('amount') or 0

                        if tax:
                            price = price_org * ((float(tax) / 100.00) + 1)
                            price = float("%0.2f" % (price))
                        else:
                            price = float("%0.2f" % (price_org))
                        if discount > 0:
                                    # discountstr = float("%0.2f" % ((discount * price * quantity) / 100.00))
                                    # discountDescription = "%s" % discount + "%" + " Discount "
                                    # printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                            discountstr = float("%0.2f" % (price * (float(discount) / 100.00) * quantity))
                            if diffTotal and total_with_tax:
                                if float(total_with_tax) > float(diffTotal):
                                    outprice = float("%0.2f" % (float(total_with_tax) - float(diffTotal)))
                                    DiscountStr = float(str("%0.2f" % (float(abs(float(abs(discountstr))-float(abs(outprice)))))))
                                    discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                    printer.addItem(product, quantity, price, tax, DiscountStr, discountDescription)
                                else:
                                    outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                    if outprice:
                                            DiscountStr = float(str("%0.2f" %(float(abs(abs(discountstr))+float(abs(outprice))))))
                                            discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                            printer.addItem(product, quantity, price, tax, DiscountStr, discountDescription)
                                    else:
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                        printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                            else:
                                discountDescription = "%s" % str(abs(discount)) + "%" + " Discount "
                                printer.addItem(product, quantity, price, tax, discountstr, discountDescription)


                        elif discount < 0:
                            discountstr = float("%0.2f" % (price * (float(discount) / 100.00) * quantity))
                            if diffTotal and total_with_tax:
                                if float(total_with_tax) > float(diffTotal):
                                    outprice = float("%0.2f" % (float(total_with_tax) - float(diffTotal)))
                                    DiscountStr = float("-" + str("%0.2f" % (float(abs(float(abs(discountstr))-float(abs(outprice)))))))
                                    discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                    printer.addItem(product, quantity, price, tax, DiscountStr, discountDescription)
                                else:
                                    outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                    if outprice:
                                            DiscountStr = float("-"+str("%0.2f" %(float(abs(abs(discountstr))+float(abs(outprice))))))
                                            discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                            printer.addItem(product, quantity, price, tax, DiscountStr, discountDescription)
                                    else:
                                        discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                        printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                            else:
                                discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                printer.addItem(product, quantity, price, tax, discountstr, discountDescription)

                        elif discount == 0:
                            print 'DISCOUNT IS ZERO '
                            if diffTotal and total_with_tax:
                                print  'RECEIPT TOTAL : ',diffTotal
                                print  'TOTAL : ',total_with_tax
                                if float(total_with_tax) > float(diffTotal):
                                    outprice = float("-"+str("%0.2f" % (float(total_with_tax) - float(diffTotal))))
                                    print 'OUTPRICE :---- ',outprice,type(outprice)

                                    discountDescription = " Surcharge "
                                    printer.addItem(product, quantity, price, tax, outprice, discountDescription)
                                else:
                                    outprice = float("%0.2f" % (float(diffTotal) - float(total_with_tax)))
                                    if outprice:
                                        discountDescription = " Discount "
                                        print 'DISCOUNT : ------ ',outprice,type(outprice)
                                        printer.addItem(product, quantity, price, tax, outprice, discountDescription)
                                    else:
                                        printer.addItem(product, quantity, price, tax, discount, discountDescription)
                            else:
                                discount = 0
                                discountDescription = ''
                                # tax = 0
                                print 'PRODUCT : '+str(product)+ ' QUANTITY: '+str(quantity)
                                printer.addItem(product, quantity, price, tax, discount, discountDescription)

                    # except Exception as e:
                    # _logger.error("Error :  " + str(e))
                    # printer.cancelAnyDocument()

                # try:
                #     if receipt_type:
                #     # if ResponsabilityType == 'F' or 'M' or 'E' or 'N':
                #         if diffTotal and total_with_tax:
                #             if float(total_with_tax) > float(diffTotal):
                #                  outprice = float("%0.2f"%(float(total_with_tax)-float(diffTotal)))
                #                  printer.addToTotal("Exceptional Price", 1, outprice, 0, 0, '')
                #                  print ' Addition Difference with Total   : ---------',outprice
                #             else:
                #                  outprice = float("%0.2f"%(float(diffTotal)-float(total_with_tax)))
                #                  if outprice:
                #                     printer.SubToTotal("Exceptional Price",  1, outprice, 0, 0, '')
                #                     print 'Subtraction Difference with total : --------- ',outprice
                # except:
                #     pass

                # try:
                #     if productMake:
                #         sum = 0
                #         for ExceptPrice in productMake:
                #             if ExceptPrice:
                #                 sum = sum + float(ExceptPrice)
                #                 print 'Exceptional Prices :   ------------------------------------------- ', ExceptPrice
                #         print 'SUM :-------------', str(float(sum))
                #         printer.addItem('Exceptional Price', 1, float(sum), 0, 0, '')
                # except:
                #     pass
                # try:
                #     if perception:
                #         for perceptTax in perception:
                #             # diffTotal.append(perceptTax.get("tax"))
                #             diffTotal+=float(perceptTax.get("tax"))
                #             printer.AddPerception(perceptTax.get("name"), perceptTax.get("tax"),perceptTax.get("taxamount"))
                # except:
                #     pass


###############***************************************************************
            else:
                for products in receipt['receipt']['orderlines']:
                    ### PRODUCT DETAILS
                    product = products.get('product_name') or 0
                    quantity = products.get('quantity') or 0
                    price_org = products.get('price') or 0
                    print "PRICE :--------------",price_org
                    price_org = float("%0.2f" % (price_org))
                    print "PRICE (FLOAT) :--------------", price_org
                    discount = products.get('discount') or 0
                    discountDescription = ''
                    tax_id = products.get('tax')
                    tax = products['get_tax_perc'][0].get('amount') or 0
                    try:
                        if ResponsabilityType == 'I':  # FOR THE RECEIPT TYPE 'A'
                            if discount > 0:
                                discountstr = float("%0.2f"%((discount * price_org * quantity) / 100.00))
                                print 'discountstr', str(discountstr)
                                discountDescription = "%s" % discount + "%" + " Discount "
                                printer.addItem(product, quantity, price_org, tax, discountstr, discountDescription)
                            elif discount < 0:
                                discountstr = float("%0.2f"%(price_org * (float(discount) / 100.00) * quantity))
                                print 'discountstr', str(discountstr)
                                discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                printer.addItem(product, quantity, price_org, tax, discountstr, discountDescription)
                            elif discount == 0:
                                printer.addItem(product, quantity, price_org, tax, discount, discountDescription)
                        else:  # FOR RECEIPT TYPE B/C
                            if tax:
                                price = price_org * ((float(tax) / 100.00) + 1)
                                price = float("%0.2f" % (price))
                            else:
                                price = float("%0.2f" % (price_org))
                            if discount > 0:
                                discountstr = float("%0.2f"%((discount * price * quantity) / 100.00))
                                discountDescription = "%s" % discount + "%" + " Discount "
                                printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                            elif discount < 0:
                                discountstr = float("%0.2f"%(price * (float(discount) / 100.00) * quantity))
                                discountDescription = "%s" % str(abs(discount)) + "%" + " Surcharge "
                                print 'discountstr',str(discountstr)
                                printer.addItem(product, quantity, price, tax, discountstr, discountDescription)
                            elif discount == 0:
                                printer.addItem(product, quantity, price, tax, discount, discountDescription)
                    except Exception as e:
                        _logger.error("Error :  " + str(e))
                        printer.cancelAnyDocument()

            #Differece can be remove with method but issue with subtraction
            # try:
            #     if receipt_type:
            #     # if ResponsabilityType == 'F' or 'M' or 'E' or 'N':
            #         if diffTotal and total_with_tax:
            #             if float(total_with_tax) > float(diffTotal):
            #                  outprice = float("%0.2f"%(float(total_with_tax)-float(diffTotal)))
            #                  printer.addToTotal("Exceptional Price", 1, outprice, 0, 0, '')
            #                  print ' Addition Difference with Total   : ---------',outprice
            #             else:
            #                  outprice = float("%0.2f"%(float(diffTotal)-float(total_with_tax)))
            #                  if outprice:
            #                     printer.SubToTotal("Exceptional Price",  1, outprice, 0, 0, '')
            #                     print 'Subtraction Difference with total : --------- ',outprice
            # except:
            #     pass

            try:
                if productMake:
                    sum = 0
                    for ExceptPrice in productMake:
                        if ExceptPrice:
                            sum = sum + float(ExceptPrice)
                            print 'Exceptional Prices :   ------------------------------------------- ', ExceptPrice
                    print 'SUM :-------------', str(float(sum))
                    printer.addItem('Exceptional Price', 1, float(sum), 0, 0, '')
            except:
                pass
            try:
                if perception:
                    for perceptTax in perception:
                        # diffTotal.append(perceptTax.get("tax"))
                        diffTotal+=float(perceptTax.get("tax"))
                        printer.AddPerception(perceptTax.get("name"), perceptTax.get("tax"),perceptTax.get("taxamount"))
            except:
                pass
            try:
                if paymentlines_list:
                    for payment in paymentlines_list:
                        paymentAmount = payment.get('amount')
                        paymentJournal = payment.get('journal')
                        printer.addPayment(paymentJournal, paymentAmount)
            except:
                pass
            try:
                printer.closeDocument()
            except:
                pass
            try:
                printer.close()
            except:
                pass
            pos_receipt = "0020-" + ((8 - int(len(str(pos_receipt)))) * "0") + str(pos_receipt)
            print 'POS RECEIPT :-----------------------------------------', pos_receipt
            return str(pos_receipt)