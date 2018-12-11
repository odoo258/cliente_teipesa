# -*- coding: iso-8859-1 -*-
import string
import types
import logging
import unicodedata
from fiscalGeneric import PrinterInterface, PrinterException
import epsonFiscalDriver


class FiscalPrinterError(Exception):
    pass


class FileDriver:
    def __init__(self, filename):
        self.filename = filename
        self.file = open(filename, "w")

    def sendCommand(self, command, parameters):
        self.file.write("Command: %d, Parameters: %s\n" % (command, parameters))
        return ["BLA", "BLA", "BLA", "BLA", "BLA", "BLA", "BLA", "BLA", ]

    def close(self):
        self.file.close()


def formatText(text):
    asciiText = unicodedata.normalize('NFKD', unicode(text)).encode('ASCII', 'ignore')
    asciiText = asciiText.replace("\t", " ").replace("\n", " ").replace("\r", " ")
    return asciiText


class DummyDriver:
    def __init__(self):
        try:
            self.number = int(raw_input("Ingrese el n�mero de la �ltima factura: "))
        except EOFError:
            # iniciar desde 0 (ejecutando sin stdin)
            self.number = 0

    def close(self):
        pass

    def sendCommand(self, commandNumber, parameters, skipStatusErrors):
        ##raise RuntimeError("saraza1")
        ##        if commandNumber in EpsonPrinter.CMD_CLOSE_FISCAL_RECEIPT:
        ##            #raise RuntimeError("saraza")
        ##        else:
        ##            pass
        return ["00", "00", "", "", str(self.number), "", str(self.number)] + [str(self.number)] * 11


class EpsonPrinter(PrinterInterface):
    DEBUG = True

    CMD_OPEN_FISCAL_RECEIPT = 0x40
    CMD_OPEN_BILL_TICKET = 0x60
    ##    CMD_PRINT_TEXT_IN_FISCAL = (0x41, 0x61)
    CMD_PRINT_TEXT_IN_FISCAL = 0x41
    CMD_PRINT_LINE_ITEM = (0x42, 0x62)
    ## (0x42, 0x62)
    CMD_PRINT_SUBTOTAL = (0x43, 0x63)
    CMD_ADD_PAYMENT = (0x44, 0x64)
    CMD_CLOSE_FISCAL_RECEIPT = (0x45, 0x65)
    CMD_DAILY_CLOSE = 0x39
    CMD_STATUS_REQUEST = 0x2a

    CMD_OPEN_DRAWER = 0x7b

    CMD_SET_HEADER_TRAILER = 0x5d

    CMD_OPEN_NON_FISCAL_RECEIPT = 0x48
    CMD_PRINT_NON_FISCAL_TEXT = 0x49
    CMD_CLOSE_NON_FISCAL_RECEIPT = 0x4a

    # COMMAND FOR THE PERCEPTION
    CMD_PERCEPTION = 0x66

    #     productMake = []

    CURRENT_DOC_TICKET = 1
    CURRENT_DOC_BILL_TICKET = 2
    CURRENT_DOC_CREDIT_TICKET = 4
    CURRENT_DOC_NON_FISCAL = 3
    TAX = ''
    DocCode = ''
    models = ["tickeadoras", "epsonlx300+", "tm-220-af"]

    #     "tm-220-af"="epsonlx300+"
    def __init__(self, deviceFile=None, speed=9600, host=None, port=None, dummy=False, model=None):
        try:
            if dummy:
                self.driver = DummyDriver()
            elif host:
                self.driver = epsonFiscalDriver.EpsonFiscalDriverProxy(host, port)
            else:
                deviceFile = deviceFile or 0
                self.driver = epsonFiscalDriver.EpsonFiscalDriver(deviceFile, speed)
                # self.driver = FileDriver( "/home/gnarvaja/Desktop/fiscal.txt" )
        except Exception, e:
            raise FiscalPrinterError("Imposible establecer comunicaci�n.", e)
        if not model:
            self.model = "tickeadoras"
        else:
            self.model = model
        self._currentDocument = None
        self._currentDocumentType = None

    def _sendCommand(self, commandNumber, parameters, skipStatusErrors=False):
        print "_sendCommand", commandNumber, parameters
        try:
            logging.getLogger().info("sendCommand: SEND|0x%x|%s|%s" % (commandNumber,
                                                                       skipStatusErrors and "T" or "F",
                                                                       str(parameters)))
            return self.driver.sendCommand(commandNumber, parameters, skipStatusErrors)
        except epsonFiscalDriver.PrinterException, e:
            logging.getLogger().error("epsonFiscalDriver.PrinterException: %s")
            raise PrinterException("Error de la impresora fiscal: " + str(e))
            #             print "Raise Error :   ",str(e)

    def openNonFiscalReceipt(self):
        status = self._sendCommand(self.CMD_OPEN_NON_FISCAL_RECEIPT, [])
        self._currentDocument = self.CURRENT_DOC_NON_FISCAL
        self._currentDocumentType = None
        return status

    def printNonFiscalText(self, text):
        return self._sendCommand(self.CMD_PRINT_NON_FISCAL_TEXT, [formatText(text[:40] or " ")])

    ivaTypeMap = {

        #         PrinterInterface.IVA_TYPE_RESPONSABLE_INSCRIPTO: 'I',
        #         PrinterInterface.IVA_TYPE_RESPONSABLE_NO_INSCRIPTO: 'N',
        #         PrinterInterface.IVA_TYPE_EXENTO: 'E',
        #         PrinterInterface.IVA_TYPE_NO_RESPONSABLE: 'N',
        #         PrinterInterface.IVA_TYPE_CONSUMIDOR_FINAL: 'F',
        #         PrinterInterface.IVA_TYPE_RESPONSABLE_NO_INSCRIPTO_BIENES_DE_USO: 'R',
        #         PrinterInterface.IVA_TYPE_RESPONSABLE_MONOTRIBUTO: 'M',
        #         PrinterInterface.IVA_TYPE_MONOTRIBUTISTA_SOCIAL: 'M',
        #         PrinterInterface.IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL: 'F',
        #         PrinterInterface.IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL_SOCIAL: 'F',
        #         PrinterInterface.IVA_TYPE_NO_CATEGORIZADO: 'F',

        PrinterInterface.IVA_TYPE_RESPONSABLE_INSCRIPTO: 'I',
        PrinterInterface.IVA_TYPE_RESPONSABLE_NO_INSCRIPTO: 'N',
        PrinterInterface.IVA_TYPE_EXENTO: 'E',
        PrinterInterface.IVA_TYPE_NO_RESPONSABLE: 'N',
        PrinterInterface.IVA_TYPE_CONSUMIDOR_FINAL: 'F',
        PrinterInterface.IVA_TYPE_RESPONSABLE_NO_INSCRIPTO_BIENES_DE_USO: 'R',
        PrinterInterface.IVA_TYPE_RESPONSABLE_MONOTRIBUTO: 'M',
        PrinterInterface.IVA_TYPE_MONOTRIBUTISTA_SOCIAL: 'T',
        PrinterInterface.IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL: 'C',
        PrinterInterface.IVA_TYPE_PEQUENIO_CONTRIBUYENTE_EVENTUAL_SOCIAL: 'V',
        PrinterInterface.IVA_TYPE_NO_CATEGORIZADO: 'S',
    }
    ADDRESS_SIZE = 30

    def _setHeaderTrailer(self, line, text):
        self._sendCommand(self.CMD_SET_HEADER_TRAILER, (str(line), text))

    def setHeader(self, header=None):
        "Establecer encabezados"
        if not header:
            header = []
        line = 3
        for text in (header + [chr(0x7f)] * 3)[:3]:  # Agrego chr(0x7f) (DEL) al final para limpiar las
            # l�neas no utilizadas
            self._setHeaderTrailer(line, text)
            line += 1

    def setTrailer(self, trailer=None):
        "Establecer pie"
        if not trailer:
            trailer = []
        line = 11
        for text in (trailer + [chr(0x7f)] * 9)[:9]:
            self._setHeaderTrailer(line, text)
            line += 1

    def DocumentCode(self, Doc):
        if Doc:
            self.DocCode = Doc
            return True

    def getDocumentCode(self):
        return self.DocCode

    def RegisteredTaxNumber(self, RegTaxNumber):
        print "RegTaxNumber  ::::  ", RegTaxNumber
        if RegTaxNumber:
            self.TAX = RegTaxNumber
            print "RegTaxNumbe ::: ", RegTaxNumber
            return True

    def getRegisteredTaxNumber(self):
        return self.TAX

    #    print "REG ::: ",str(self.getRegisteredTaxNumber())

    def openBillCreditTicket(self, type, name, address, doc, docType, ivaType, reference="NC"):
        return self._openBillCreditTicket(type, name, address, doc, docType, ivaType, isCreditNote=True)

    def openBillTicket(self, type, name, address, doc, docType, ivaType):
        return self._openBillCreditTicket(type, name, address, doc, docType, ivaType, isCreditNote=False)

    def _openBillCreditTicket(self, type, name, address, doc, docType, ivaType, isCreditNote,
                              reference=None):
        if not doc or filter(lambda x: x not in string.digits + "-.", doc or "") or not \
                        docType in self.docTypeNames:
            doc, docType = "", ""
        else:
            doc = doc.replace("-", "").replace(".", "")
            docType = self.docTypeNames[docType]
        self._type = type

        if self.model == "epsonlx300+":
            parameters = [isCreditNote and "N" or "F",  # Por ahora no soporto ND, que ser�a "D"
                          "C",
                          type,  # Tipo de FC (A/B/C)
                          "1",  # Copias - Ignorado
                          "P",  # "P" la impresora imprime la lineas(hoja en blanco) o "F" preimpreso
                          "17",  # Tama�o Carac - Ignorado
                          "I",  # Responsabilidad en el modo entrenamiento - Ignorado
                          self.ivaTypeMap.get(ivaType, "F"),  # Iva Comprador
                          formatText(name[:40]),  # Nombre
                          formatText(name[40:80]),  # Segunda parte del nombre - Ignorado
                          formatText(docType) or (isCreditNote and "-" or ""),
                          # Tipo de Doc. - Si es NC obligado pongo algo
                          doc or (isCreditNote and "-" or ""),  # Nro Doc - Si es NC obligado pongo algo
                          "N",  # No imprime leyenda de BIENES DE USO
                          formatText(address[:self.ADDRESS_SIZE] or "-"),  # Domicilio
                          formatText(address[self.ADDRESS_SIZE:self.ADDRESS_SIZE * 2]),  # Domicilio 2da linea
                          formatText(address[self.ADDRESS_SIZE * 2:self.ADDRESS_SIZE * 3]),  # Domicilio 3ra linea
                          (isCreditNote or self.ivaTypeMap.get(ivaType, "F") != "F") and "-" or "",
                          #                 "-",
                          # Remito primera linea - Es obligatorio si el cliente no es consumidor final
                          "",  # Remito segunda linea
                          "C",  # No somos una farmacia
                          ]

        elif type == 'A':
            print "REG ::::  ", self.getRegisteredTaxNumber()
            parameters = [isCreditNote and "M" or "T",  # Ticket NC o Factura
                          "C",  # Tipo de Salida - Ignorado
                          type,  # Tipo de FC (A/B/C)
                          "1",  # Copias - Ignorado
                          "P",  # Tipo de Hoja - Ignorado
                          "17",  # Tama�o Carac - Ignorado
                          "E",  # Responsabilidad en el modo entrenamiento - Ignorado
                          self.ivaTypeMap.get(ivaType, "F"),  # Iva Comprador
                          formatText(name[:40]),  # Nombre
                          formatText(name[40:80]),  # Segunda parte del nombre - Ignorado
                          #                 formatText(docType) or (isCreditNote and "-" or ""),
                          # Tipo de Doc. - Si es NC obligado pongo algo
                          ("%s" % str(self.getDocumentCode())) or "CUIT",
                          # ("%s"%str(self.DocumentCode())) or  doc  or (isCreditNote and "-" or ""),
                          #                doc or (isCreditNote and "-" or ""), # Nro Doc - Si es NC obligado pongo algo
                          #                "N", # No imprime leyenda de BIENES DE USO

                          # "30707468161",

                          # REGISTERED TAX NUMBER
                          ("%s" % str(self.getRegisteredTaxNumber())) or "",
                          "N",

                          formatText(address[:self.ADDRESS_SIZE] or "-"),  # Domicilio
                          formatText(address[self.ADDRESS_SIZE:self.ADDRESS_SIZE * 2]),  # Domicilio 2da linea
                          formatText(address[self.ADDRESS_SIZE * 2:self.ADDRESS_SIZE * 3]),  # Domicilio 3ra linea
                          (isCreditNote or self.ivaTypeMap.get(ivaType, "F") != "F") and "-" or "",
                          #                 "",
                          # Remito primera linea - Es obligatorio si el cliente no es consumidor final
                          "",  # Remito segunda linea
                          "C",  # No somos una farmacia
                          ]

        elif type == 'B':
            parameters = [isCreditNote and "M" or "T",  # Ticket NC o Factura
                          "C",  # Tipo de Salida - Ignorado
                          type,  # Tipo de FC (A/B/C)
                          "1",  # Copias - Ignorado
                          "P",  # Tipo de Hoja - Ignorado
                          "17",  # Tama�o Carac - Ignorado
                          "E",  # Responsabilidad en el modo entrenamiento - Ignorado
                          self.ivaTypeMap.get(ivaType, "F"),
                          # self.ivaTypeMap.get(ivaType, "F"),   # Iva Comprador
                          formatText(name[:40]),  # Nombre
                          formatText(name[40:80]),  # Segunda parte del nombre - Ignorado
                          ("%s" % str(self.getDocumentCode())) or formatText(docType) or (isCreditNote and "-" or ""),
                          # Tipo de Doc. - Si es NC obligado pongo algo
                          ("%s" % str(self.getRegisteredTaxNumber())) or doc or (isCreditNote and "-" or ""),
                          # Nro Doc - Si es NC obligado pongo algo
                          #       ("%s"%str(self.getRegisteredTaxNumber())) or 0,
                          "N",  # No imprime leyenda de BIENES DE USO
                          formatText(address[:self.ADDRESS_SIZE] or "-"),  # Domicilio
                          formatText(address[self.ADDRESS_SIZE:self.ADDRESS_SIZE * 2]),  # Domicilio 2da linea
                          formatText(address[self.ADDRESS_SIZE * 2:self.ADDRESS_SIZE * 3]),  # Domicilio 3ra linea
                          (isCreditNote or self.ivaTypeMap.get(ivaType, "F") != "F") and "-" or "",
                          # Remito primera linea - Es obligatorio si el cliente no es consumidor final
                          "",  # Remito segunda linea
                          "C",  # No somos una farmacia
                          ]

        else:
            parameters = [isCreditNote and "M" or "T",  # Ticket NC o Factura
                          "C",  # Tipo de Salida - Ignorado
                          type,  # Tipo de FC (A/B/C)
                          "1",  # Copias - Ignorado
                          "P",  # Tipo de Hoja - Ignorado
                          "17",  # Tama�o Carac - Ignorado
                          "E",  # Responsabilidad en el modo entrenamiento - Ignorado
                          self.ivaTypeMap.get(ivaType, "F"),  # Iva Comprador
                          formatText(name[:40]),  # Nombre
                          formatText(name[40:80]),  # Segunda parte del nombre - Ignorado
                          formatText(docType) or (isCreditNote and "-" or ""),
                          # Tipo de Doc. - Si es NC obligado pongo algo
                          doc or (isCreditNote and "-" or ""),  # Nro Doc - Si es NC obligado pongo algo
                          #    ("%s"%str(self.getRegisteredTaxNumber())) or 0,
                          "N",  # No imprime leyenda de BIENES DE USO
                          formatText(address[:self.ADDRESS_SIZE] or "-"),  # Domicilio
                          formatText(address[self.ADDRESS_SIZE:self.ADDRESS_SIZE * 2]),  # Domicilio 2da linea
                          formatText(address[self.ADDRESS_SIZE * 2:self.ADDRESS_SIZE * 3]),  # Domicilio 3ra linea
                          (isCreditNote or self.ivaTypeMap.get(ivaType, "F") != "F") and "-" or "",
                          # Remito primera linea - Es obligatorio si el cliente no es consumidor final
                          "",  # Remito segunda linea
                          "C",  # No somos una farmacia
                          ]
        if isCreditNote:
            self._currentDocument = self.CURRENT_DOC_CREDIT_TICKET
        else:
            self._currentDocument = self.CURRENT_DOC_BILL_TICKET
        # guardo el tipo de FC (A/B/C)
        self._currentDocumentType = type
        return self._sendCommand(self.CMD_OPEN_BILL_TICKET, parameters)

    def _getCommandIndex(self):
        if self._currentDocument == self.CURRENT_DOC_TICKET:
            return 0
        elif self._currentDocument in (self.CURRENT_DOC_BILL_TICKET, self.CURRENT_DOC_CREDIT_TICKET):
            return 1
        elif self._currentDocument == self.CURRENT_DOC_NON_FISCAL:
            return 2
        raise "Invalid currentDocument"

    def openTicket(self, defaultLetter='B'):
        if self.model == "epsonlx300+":
            return self.openBillTicket(defaultLetter, "CONSUMIDOR FINAL", "", None, None,
                                       self.IVA_TYPE_CONSUMIDOR_FINAL)
        else:
            self._sendCommand(self.CMD_OPEN_FISCAL_RECEIPT, ["C"])
            self._currentDocument = self.CURRENT_DOC_TICKET

    def openDrawer(self):
        self._sendCommand(self.CMD_OPEN_DRAWER, [])

    def closeDocument(self):
        if self._currentDocument == self.CURRENT_DOC_TICKET:
            reply = self._sendCommand(self.CMD_CLOSE_FISCAL_RECEIPT[self._getCommandIndex()], ["T"])
            return reply[2]
        if self._currentDocument == self.CURRENT_DOC_BILL_TICKET:
            reply = self._sendCommand(self.CMD_CLOSE_FISCAL_RECEIPT[self._getCommandIndex()],
                                      [self.model == "epsonlx300+" and "F" or "T", self._type, "FINAL"])
            del self._type
            return reply[2]
        if self._currentDocument == self.CURRENT_DOC_CREDIT_TICKET:
            reply = self._sendCommand(self.CMD_CLOSE_FISCAL_RECEIPT[self._getCommandIndex()],
                                      [self.model == "epsonlx300+" and "N" or "M", self._type, "FINAL"])
            del self._type
            return reply[2]
        if self._currentDocument in (self.CURRENT_DOC_NON_FISCAL,):
            return self._sendCommand(self.CMD_CLOSE_NON_FISCAL_RECEIPT, ["T"])
        raise NotImplementedError

    def cancelDocument(self):
        if self._currentDocument in (self.CURRENT_DOC_TICKET, self.CURRENT_DOC_BILL_TICKET,
                                     self.CURRENT_DOC_CREDIT_TICKET):
            status = self._sendCommand(self.CMD_ADD_PAYMENT[self._getCommandIndex()], ["Cancelar", "0", 'C'])
            return status
        if self._currentDocument in (self.CURRENT_DOC_NON_FISCAL,):
            self.printNonFiscalText("CANCELADO")
            return self.closeDocument()
        raise NotImplementedError

    def addItem(self, description, quantity, price, iva, discount, discountDescription, negative=False):
        productMake = []
        if type(description) in types.StringTypes:
            description = [description]
        if negative:
            sign = 'R'
        else:
            sign = 'M'
        quantityStr = str(int(quantity * 1000))
        if self.model == "epsonlx300+":
            bultosStr = str(int(quantity))
        else:
            bultosStr = "0" * 5  # No se usa en TM220AF ni TM300AF ni TMU220AF
        if self._currentDocumentType != 'A':
            # enviar con el iva incluido
            priceUnitStr = str(int(round(float(price) * 100, 0)))
        # if len(str(price).split(".")[-1])==2:
        #                 priceUnitStr = str(int(price*100))
        #                 print '1 priceUnitStr  : ',priceUnitStr
        #             elif len(str(price).split(".")[-1])>2:
        #
        #                 priceUnit = round(price,3)
        #                 priceRemain = "0.00"+str(priceUnit)[-1]
        #                 priceQuantity = float(priceRemain) * quantity
        #                 print 'priceQuantity :: -------------------------------------',priceQuantity
        #                 productMake.append(priceQuantity)
        #
        #                 #PRICE UNIT STR
        #                 priceUnitStr=str(int(round(price ,2)*100))
        #                 print '2 priceUnitStr  : ',priceUnitStr
        #             else:
        #                 priceUnitStr = str(int(round(price * 100, 0)))
        #                 print '3 priceUnitStr  : ',priceUnitStr
        else:
            if self.model == "tm-220-af":
                # enviar sin el iva (factura A)
                #                 priceUnitStr =  "%0.4f" % (price / ((100.0 + iva) / 100.0))
                priceUnitStr = str(int(round((price*100),0)))

                    # str(int(round(priceUnit * 100), 0))
                                   # (price * 100))
                # (round(priceUnit * 100, 0))
            else:
                # enviar sin el iva (factura A)
                priceUnitStr = str(int(round((price / ((100 + iva) / 100)) * 100, 0)))
                #             print "priceUnitStr :: ",priceUnitStr

        ivaStr = str(int(iva * 100))
        extraparams = self._currentDocument in (self.CURRENT_DOC_BILL_TICKET,
                                                self.CURRENT_DOC_CREDIT_TICKET) and ["", "", ""] or []
        print "GET COMMAND INDEX :: ", self._getCommandIndex()
        if self._getCommandIndex() == 0:
            for d in description[:-1]:
                self._sendCommand(self.CMD_PRINT_TEXT_IN_FISCAL,
                                  [formatText(d)[:20]])
        reply = self._sendCommand(self.CMD_PRINT_LINE_ITEM[self._getCommandIndex()],
                                  [formatText(description[-1][:20]),
                                   quantityStr, priceUnitStr, ivaStr, sign, bultosStr, "0" * 8] + extraparams)

        # DISCOUNT
        if discount > 0:

            # self._getCommandIndex() = 0 to fire 66 commands
            #       self._getCommandIndex() = 0
            discountdiff = round(discount * 100, 2)
            discountStr = str(int(discountdiff))
            self._sendCommand(self.CMD_PRINT_LINE_ITEM[self._getCommandIndex()],
                              [formatText(discountDescription[:20]), "1000",
                               discountStr, ivaStr, 'R', "0", "0"] + extraparams)
            return reply
        # Surcharge
        elif discount < 0:
            # self._getCommandIndex() = 0 to fire 66 commands
            #	    self._getCommandIndex() = 0
            discount = abs(discount)
            discountdiff = round(discount * 100, 2)
            discountStr = str(int(discountdiff))
            self._sendCommand(self.CMD_PRINT_LINE_ITEM[self._getCommandIndex()],
                              [formatText(discountDescription[:20]), "1000",
                               discountStr, ivaStr, 'M', "0", "0"] + extraparams)
            return reply

            #         if productMake:
            #             #CREATED REMAING PRODUCT
            #             for productPrice in productMake:
            #                 print 'productPrice  -----------------------------------------    ',productPrice
            #                 self._sendCommand(self.CMD_PRINT_LINE_ITEM[1],["Extra", "1000",(str(int(float(productPrice)*100))), '0', 'R', "0", "0"] + extraparams)
            #                 return reply

    # FOR THE TICKET NUMBER
    def TicketNumber(self, description):
        return self._sendCommand(self.CMD_PRINT_TEXT_IN_FISCAL, [(description)[:20]])

    # FOR PERCEPTION
    def AddPerception(self, perceptText, perceptAmount, perceptTax):
        amount = str(int(round((float(perceptAmount) * 100), 2)))
        percent = str(int(float(perceptTax)))
        return (self._sendCommand(self.CMD_PERCEPTION, [str(perceptText), "O", amount, percent]))

    def addPayment(self, description, payment):
        paymentStr = str(int(round(float(payment) * 100, 2)))
        # (int(round(float(payment) * 100,2)))
        status = self._sendCommand(self.CMD_ADD_PAYMENT[self._getCommandIndex()],
                                   [formatText(description)[:20], paymentStr, 'T'])
        return status

    def addAdditional(self, description, amount, iva, negative=False):
        """Agrega un adicional a la FC.
            @param description  Descripci�n
            @param amount       Importe (sin iva en FC A, sino con IVA)
            @param iva          Porcentaje de Iva
            @param negative True->Descuento, False->Recargo"""
        if negative:
            sign = 'R'
        else:
            sign = 'M'
        quantityStr = "1000"
        bultosStr = "0"
        priceUnit = amount
        if self._currentDocumentType != 'A':
            # enviar con el iva incluido
            priceUnitStr = str(int(round(priceUnit * 100, 0)))
        else:
            # enviar sin el iva (factura A)
            priceUnitStr = str(int(round((priceUnit / ((100 + iva) / 100)) * 100, 0)))
        ivaStr = str(int(iva * 100))
        extraparams = self._currentDocument in (self.CURRENT_DOC_BILL_TICKET,
                                                self.CURRENT_DOC_CREDIT_TICKET) and ["", "", ""] or []
        reply = self._sendCommand(self.CMD_PRINT_LINE_ITEM[self._getCommandIndex()],
                                  [formatText(description[:20]),
                                   quantityStr, priceUnitStr, ivaStr, sign, bultosStr, "0"] + extraparams)
        return reply

    def subtotal(self, print_text=True, display=False, text="Subtotal"):
        if self._currentDocument in (self.CURRENT_DOC_TICKET, self.CURRENT_DOC_BILL_TICKET,
                                     self.CURRENT_DOC_CREDIT_TICKET):
            status = self._sendCommand(self.CMD_PRINT_SUBTOTAL[self._getCommandIndex()],
                                       ["P" if print_text else "O", text])
            return status
        raise NotImplementedError

    def dailyClose(self, type):
        reply = self._sendCommand(self.CMD_DAILY_CLOSE, [type, "P"])
        return reply[2:]

    def getLastNumber(self, letter):
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, ["A"], True)
        if len(reply) < 3:
            # La respuesta no es v�lida. Vuelvo a hacer el pedido y si hay alg�n error que se reporte como excepci�n
            reply = self._sendCommand(self.CMD_STATUS_REQUEST, ["A"], False)
        if letter == "A":
            return int(reply[6])
        else:
            return int(reply[4])

    def getLastCreditNoteNumber(self, letter):
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, ["A"], True)
        if len(reply) < 3:
            # La respuesta no es v�lida. Vuelvo a hacer el pedido y si hay alg�n error que se reporte como excepci�n
            reply = self._sendCommand(self.CMD_STATUS_REQUEST, ["A"], False)
        if letter == "A":
            return int(reply[10])
        else:
            return int(reply[11])

    def cancelAnyDocument(self):
        try:
            self._sendCommand(self.CMD_ADD_PAYMENT[0], ["Cancelar", "0", 'C'])
            return True
        except:
            pass
        try:
            self._sendCommand(self.CMD_ADD_PAYMENT[1], ["Cancelar", "0", 'C'])
            return True
        except:
            pass
        try:
            self._sendCommand(self.CMD_CLOSE_NON_FISCAL_RECEIPT, ["T"])
            return True
        except:
            pass
        return False

    def getWarnings(self):
        ret = []
        reply = self._sendCommand(self.CMD_STATUS_REQUEST, ["N"], True)
        printerStatus = reply[0]
        x = int(printerStatus, 16)
        if ((1 << 4) & x) == (1 << 4):
            ret.append("Poco papel para la cinta de auditor�a")
        if ((1 << 5) & x) == (1 << 5):
            ret.append("Poco papel para comprobantes o tickets")
        return ret

    def __del__(self):
        try:
            self.close()
        except:
            pass

    def close(self):
        self.driver.close()
        self.driver = None