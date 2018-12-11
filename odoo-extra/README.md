Odoo OCA addons
===============


Account Closing
===============

[![Build Status](https://travis-ci.org/OCA/account-closing.svg?branch=10.0)](https://travis-ci.org/OCA/account-closing)
[![Coverage Status](https://img.shields.io/coveralls/OCA/account-closing.svg)](https://coveralls.io/r/OCA/account-closing?branch=10.0)

This project aim to deal with modules related to manage account closing.

[//]: # (addons)

Available addons
----------------
addon | version | summary
--- | --- | ---
[account_cutoff_accrual_base](account_cutoff_accrual_base/) | 10.0.0.1.0 | Base module for accrued expenses and revenues
[account_cutoff_base](account_cutoff_base/) | 10.0.1.0.0 | Base module for Account Cut-offs
[account_cutoff_prepaid](account_cutoff_prepaid/) | 10.0.1.0.0 | Prepaid Expense, Prepaid Revenue
[account_invoice_start_end_dates](account_invoice_start_end_dates/) | 10.0.1.0.0 | Adds start/end dates on invoice lines and move lines


Unported addons
---------------
addon | version | summary
--- | --- | ---
[account_cutoff_accrual_picking](account_cutoff_accrual_picking/) | 0.1 (unported) | Accrued Expense & Accrued Revenue from Pickings
[account_multicurrency_revaluation](account_multicurrency_revaluation/) | 8.0.1.0.0 (unported) | Manage revaluation for multicurrency environment
[account_multicurrency_revaluation_report](account_multicurrency_revaluation_report/) | 8.0.1.0.0 (unported) | Module for printing reports that completes the module Multicurrency Revaluation

[//]: # (end addons)

To learn more about this directory, please visit
https://pypi.python.org/pypi/setuptools-odoo



Odoo POS addons
===============

Odoo (OpenERP) POS addons 

List of repositories:
---------------------

* https://github.com/it-projects-llc/misc-addons
* https://github.com/it-projects-llc/pos-addons
* https://github.com/it-projects-llc/mail-addons
* https://github.com/it-projects-llc/rental-addons
* https://github.com/it-projects-llc/access-addons
* https://github.com/it-projects-llc/website-addons
* https://github.com/it-projects-llc/l10n-addons
* https://github.com/it-projects-llc/odoo-telegram
* https://github.com/it-projects-llc/odoo-saas-tools


.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

========================
Sale Order Lot Selection
========================

This Module Allows you to select on sale order the production lot that will be delivered
You can select a lot for every sale order line, and it will be proposed on the delivery

Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/167/10.0

Known issues / Roadmap
======================

* This is functionally incompatible with sale_rental

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/sale-workflow/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback..

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.


Contributors
------------

* Nicola Malcontenti <nicola.malcontenti@agilebg.com>
* Lorenzo Battistini <lorenzo.battistini@agilebg.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.



Sale Workflow
=============
[![Runbot Status](https://runbot.odoo-community.org/runbot/badge/flat/167/10.0.svg)](https://runbot.odoo-community.org/runbot/repo/github-com-oca-sale-workflow-167)
[![Build Status](https://travis-ci.org/OCA/sale-workflow.svg?branch=10.0)](https://travis-ci.org/OCA/sale-workflow)
[![codecov](https://codecov.io/gh/OCA/sale-workflow/branch/10.0/graph/badge.svg)](https://codecov.io/gh/OCA/sale-workflow)

Odoo Sales, Workflow and Organization
======================================

This project aim to deal with modules related to manage sale and their related workflow. You'll find modules that:

 - Allow to group discounts / advances / fees separately
 - Add a condition on sales that is pushed on related invoices
 - Compute shipped rate differently
 - Easy the cancellation of SO
 - ...

[//]: # (addons)

Available addons
----------------
addon | version | summary
--- | --- | ---
[sale_automatic_workflow](sale_automatic_workflow/) | 10.0.1.0.0 | Sale Automatic Workflow
[sale_automatic_workflow_payment_mode](sale_automatic_workflow_payment_mode/) | 10.0.1.0.0 | Sale Automatic Workflow - Payment Mode
[sale_cancel_reason](sale_cancel_reason/) | 10.0.1.0.0 | Sale Cancel Reason
[sale_commercial_partner](sale_commercial_partner/) | 10.0.1.0.0 | Add stored related field 'Commercial Entity' on sale orders
[sale_exception](sale_exception/) | 10.0.2.0.0 | Custom exceptions on sale order
[sale_isolated_quotation](sale_isolated_quotation/) | 10.0.1.0.0 | Sales - Isolated Quotation
[sale_layout_hidden](sale_layout_hidden/) | 10.0.1.0.0 | Sale Layout Hidden Sections
[sale_order_lot_generator](sale_order_lot_generator/) | 10.0.0.0.1 | sale_order_lot_generator
[sale_order_lot_selection](sale_order_lot_selection/) | 10.0.1.0.0 | Sale Order Lot Selection
[sale_order_revision](sale_order_revision/) | 10.0.1.0.0 | Sale order revisions
[sale_owner_stock_sourcing](sale_owner_stock_sourcing/) | 10.0.1.0.0 | Manage stock ownership on sale order lines
[sale_product_set](sale_product_set/) | 10.0.1.0.0 | Sale product set
[sale_product_set_layout](sale_product_set_layout/) | 10.0.1.0.0 | Sale product set layout
[sale_rental](sale_rental/) | 10.0.1.0.0 | Manage Rental of Products
[sale_start_end_dates](sale_start_end_dates/) | 10.0.1.0.0 | Adds start date and end date on sale order lines
[sale_validity](sale_validity/) | 10.0.1.0.0 | Set a default validity delay on quotations


Unported addons
---------------
addon | version | summary
--- | --- | ---
[account_invoice_reorder_lines](account_invoice_reorder_lines/) | 0.1 (unported) | Invoice lines with sequence number
[mail_quotation](mail_quotation/) | 0.1 (unported) | Mail quotation
[partner_prepayment](partner_prepayment/) | 8.0.1.0.0 (unported) | Option on partner to set prepayment policy
[partner_prospect](partner_prospect/) | 8.0.1.0.0 (unported) | Partner Prospect
[pricelist_share_companies](pricelist_share_companies/) | 1.0 (unported) | Share pricelist between compagnies, not product
[product_customer_code_sale](product_customer_code_sale/) | 1.0 (unported) | Product Customer code on sale
[product_special_type](product_special_type/) | 1.0 (unported) | Product Special Types
[product_special_type_invoice](product_special_type_invoice/) | 1.0 (unported) | Product Special Type on Invoice
[product_special_type_sale](product_special_type_sale/) | 1.0 (unported) | Product Special Type on Sale
[sale_condition_text](sale_condition_text/) | 1.3 (unported) | Sale/invoice condition
[sale_delivery_term](sale_delivery_term/) | 0.1 (unported) | Delivery term for sale orders
[sale_dropshipping](sale_dropshipping/) | 1.1.1 (unported) | Sale Dropshipping
[sale_exception_nostock](sale_exception_nostock/) | 8.0.1.2.0 (unported) | Sale stock exception
[sale_fiscal_position_update](sale_fiscal_position_update/) | 1.0 (unported) | Changing the fiscal position of a sale order will auto-update sale order lines
[sale_jit_on_services](sale_jit_on_services/) | 1.0 (unported) | Sale Service Just In Time
[sale_last_price_info](sale_last_price_info/) | 8.0.1.0.0 (unported) | Product Last Price Info - Sale
[sale_multi_picking](sale_multi_picking/) | 0.1 (unported) | Multi Pickings from Sale Orders
[sale_order_add_variants](sale_order_add_variants/) | 8.0.0.1.0 (unported) | Add variants from template into sale order
[sale_order_force_number](sale_order_force_number/) | 0.1 (unported) | Force sale orders numeration
[sale_order_line_description](sale_order_line_description/) | 8.0.1.0.0 (unported) | Sale order line description
[sale_order_price_recalculation](sale_order_price_recalculation/) | 8.0.1.0.0 (unported) | Price recalculation in sales orders
[sale_order_type](sale_order_type/) | 8.0.1.0.1 (unported) | Sale Order Types
[sale_packaging_price](sale_packaging_price/) | 9.0.1.0.0 (unported) | Sale Packaging Price
[sale_partner_order_policy](sale_partner_order_policy/) | 8.0.1.0.0 (unported) | Adds customer create invoice method on partner form
[sale_payment_term_interest](sale_payment_term_interest/) | 8.0.1.0.0 (unported) | Sales Payment Term Interests
[sale_procurement_group_by_line](sale_procurement_group_by_line/) | 8.0.1.0.0 (unported) | Base module for multiple procurement group by Sale order
[sale_quotation_number](sale_quotation_number/) | 8.0.1.1.0 (unported) | Different sequence for sale quotations
[sale_quotation_sourcing](sale_quotation_sourcing/) | 8.0.0.3.1 (unported) | manual sourcing of sale quotations
[sale_quotation_sourcing_stock_route_transit](sale_quotation_sourcing_stock_route_transit/) | 8.0.0.1.0 (unported) | Link module for sale_quotation_sourcing + stock_route_transit
[sale_reason_to_export](sale_reason_to_export/) | 8.0.0.1.0 (unported) | Reason to export in Sales Order
[sale_sourced_by_line](sale_sourced_by_line/) | 8.0.1.1.0 (unported) | Multiple warehouse source locations for Sale order
[sale_sourced_by_line_sale_transport_multi_address](sale_sourced_by_line_sale_transport_multi_address/) | 8.0.1.0.0 (unported) | Make sale_sourced_by_line and sale_transport_multi_addresswork together
[sale_stock_global_delivery_lead_time](sale_stock_global_delivery_lead_time/) | 0.1 (unported) | Sale global delivery lead time

[//]: # (end addons)

Translation Status
------------------
[![Transifex Status](https://www.transifex.com/projects/p/OCA-sale-workflow-10-0/chart/image_png)](https://www.transifex.com/projects/p/OCA-sale-workflow-10-0)
