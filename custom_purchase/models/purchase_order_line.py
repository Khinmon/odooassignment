# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CustomPurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    total_weight_tons = fields.Text(
        string='Total Weight', compute='_compute_line_weight', store=True)

    @api.depends('product_qty')
    def _compute_line_weight(self):
        for line in self:
            line.total_weight_tons = str(line.product_qty) + ' tons'
