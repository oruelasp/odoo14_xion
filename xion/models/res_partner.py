# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    birthdate_date = fields.Date('Fecha de cumpleaños')
    age = fields.Integer(string='Edad', readonly=True, compute='_compute_age')

    def name_get(self):
        res = []
        for record in self:
            if record.parent_id:
                name = '{} ({})'.format(record.name, record.age)
            else:
                name = '{}'.format(record.name)
            res.append((record.id, name))
        return res

    @api.depends('birthdate_date')
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthdate_date:
                age = relativedelta(fields.Date.today(), record.birthdate_date).years
            record.age = age


class ResPartnerHistoy(models.Model):
    _name = 'res.partner.history'
    _description = 'Histórico de datos contacto'

    partner_id = fields.Many2one('res.partner', 'Contacto')
    weight = fields.Float('Peso')
    height = fields.Float('Altura')
    imc = fields.Float('Índice de masa corporal', compute='_compute_imc')
    age = fields.Integer(related='partner_id.age')

    def name_get(self):
        res = []
        for record in self:
            if record.parent_id:
                name = '{} ({})'.format(record.name, record.age)
            else:
                name = '{}'.format(record.name)
            res.append((record.id, name))
        return res

    @api.depends('weight', 'height')
    def _compute_imc(self):
        for record in self:
            imc = 0
            if record.weight and record.height:
                imc = record.weight / (record.height * record.height)
            record.imc = imc
