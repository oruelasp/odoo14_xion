# -*- coding: utf-8 -*-
from datetime import datetime

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

    @api.model
    def api_validar_serial(self, vals_list):
        resultado = {'error': '', 'status': 200}
        try:
            serial = vals_list.get('serial')
            partner = self.search([('vat', '=', serial)])
            fecha_actual = datetime.now().date()
            is_active = False
            if partner:
                fecha_inicio = partner.membership_start
                fecha_fin = partner.membership_stop
                if fecha_inicio and fecha_fin and fecha_inicio <= fecha_actual and fecha_fin >= fecha_actual:
                    is_active = True
                resultado['active'] = is_active
                resultado['date_end'] = fecha_fin.strftime('%Y-%m-%d') if fecha_fin else ''
            else:
                resultado['active'] = is_active
                resultado['error'] = 'serial no existe'
                resultado['status'] = 404
        except Exception as e:
            resultado['error'] = str(e)
            resultado['status'] = 500
        return resultado


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
