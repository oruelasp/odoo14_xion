# -*- coding: utf-8 -*-
from odoo import api, fields, models

from .constants import ACTIVE, FEEDBACK, SCALE, STATE_SELECTION


class XionSprint(models.Model):
    _name = 'xion.sprint'
    _description = 'Sprint'

    partner_id = fields.Many2one('res.partner', string='Cliente')
    sequence = fields.Integer(string='Secuencia', required=True)
    date_start = fields.Date('Fecha inicio')
    date_end = fields.Date('Fecha fin')
    duration = fields.Integer('Duración (en días)')
    state = fields.Selection(STATE_SELECTION, string='Estado')
    product_id = fields.Many2one('product.product', string='Producto')

    def name_get(self):
        res = []
        for record in self:
            if record.partner_id.vat and record.sequence:
                name = '{}-Sp{}'.format(record.partner_id.vat, str(
                    record.sequence).zfill(4))
            else:
                name = '{}-Sp{}'.format(record.partner_id.name, str(
                    record.sequence).zfill(4))
            res.append((record.id, name))
        return res


class XionSession(models.Model):
    _name = 'xion.session'
    _description = 'Sesión'

    sprint_id = fields.Many2one('xion.sprint', string='Sprint')
    sequence = fields.Integer(string='Secuencia')
    datetime_start = fields.Datetime('Fecha-hora inicio')
    datetime_end = fields.Datetime('Fecha-hora fin')
    voltage = fields.Float('Voltaje')
    duration = fields.Integer('Duración (en minutos)')
    feedback_id = fields.Many2one(
        'xion.catalog', string='Feedback',
        domain="[('parent_id.code', '=', '{fb}')]".format(fb=FEEDBACK))

    def name_get(self):
        res = []
        for record in self:
            if record.sequence:
                name = '{}-Se{}'.format(record.sprint_id.display_name,
                                       str(record.sequence).zfill(4))
            else:
                name = '{}-Se{}'.format(record.sprint_id.display_name, 'X')
            res.append((record.id, name))
        return res

    @api.model
    def api_save_session(self, vals_list):
        resultado = {'error': '', 'status': 201}
        try:
            serial = vals_list.get('serial')
            datetime_start = vals_list.get('datetime_start')
            datetime_end = vals_list.get('datetime_end')
            voltage = vals_list.get('voltage')
            duration = vals_list.get('duration')
            partner = self.env['res.partner'].search([('vat', '=', serial)])
            sprint = self.env['xion.sprint'].search(
                [('partner_id', '=', partner.id), ('state', '=', ACTIVE)])

            if sprint:
                parametros = {
                    'sprint_id': sprint.id,
                    'datetime_start': datetime_start,
                    'datetime_end': datetime_end,
                    'voltage': voltage,
                    'duration': duration,
                }
                self.create(parametros)
                resultado['status'] = 201
            else:
                resultado['error'] = 'El paciente no tiene un tratamiento activo'
                resultado['status'] = 404
        except Exception as e:
            resultado['error'] = str(e)
            resultado['status'] = 500
        return resultado


class XionMonitoring(models.Model):
    _name = 'xion.monitoring'
    _description = 'Acto Narrativo'

    sprint_id = fields.Many2one('xion.sprint', string='Tratamiento')
    sequence = fields.Integer(string='Secuencia')
    date = fields.Date('Fecha')
    scale_id = fields.Many2one(
        'xion.catalog',
        string='Scale', domain="[('code', '=', '{scale}')]".format(scale=SCALE)
    )
    observation = fields.Char('Observaciones')

    def name_get(self):
        res = []
        for record in self:
            if record.sequence:
                name = '{}-M{}'.format(record.sprint_id.display_name, str(
                    record.sequence).zfill(4))
            else:
                name = '{}-M{}'.format(record.sprint_id.display_name, 'X')
            res.append((record.id, name))
        return res
