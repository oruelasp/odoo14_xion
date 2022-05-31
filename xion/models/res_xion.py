# -*- coding: utf-8 -*-

from odoo import api, fields, models

from .constants import ACTIVE, FEEDBACK, HDSS, STATE_SELECTION


class XionCatalog(models.Model):
    _name = 'xion.catalog'
    _description = 'Catálogo'

    parent_id = fields.Many2one(
        _name, 'Padre',
        default=lambda self: self._default_parent_id())
    code = fields.Char('Código', size=50, required=True)
    name = fields.Char('Descripción', size=100, required=True)
    alias = fields.Char('Abreviatura', size=30)
    value = fields.Char('Valor')
    value2 = fields.Char('Valor2')
    value3 = fields.Char('Valor3')
    active = fields.Boolean('Activo/Inactivo', default=True)
    sequence = fields.Integer(default=10)
    child_ids = fields.One2many(_name, 'parent_id', 'Items')

    _sql_constraints = [
        ('parent_id_code',
         'UNIQUE(parent_id, code)',
         'Ya existe el código'),
        ('parent_id_name',
         'UNIQUE(parent_id, name)',
         'Ya existe el cátalogo'),
    ]

    def _default_parent_id(self):
        root = self.search([('code', '=', 'root'), ('parent_id', '=', False)],
                           limit=1)
        return self.env.context.get('default_parent_id') or root.id

    def name_get(self):
        res = []
        for record in self:
            if record.parent_id:
                name = '({}) {}: {}'.format(record.parent_id.code, record.parent_id.alias, record.value)
            else:
                name = '({}) {}'.format(record.code, record.name)
            res.append((record.id, name))
        return res

    @api.model
    def get_xion_catalog(self, parent_code, key='code'):
        domain = [('parent_id.code', '=', parent_code)]
        return [(getattr(obj, key), obj.name) for obj in self.search(domain)]


class XionTreatment(models.Model):
    _name = 'xion.treatment'
    _description = 'Tratamiento'

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
                name = '{}-T{}'.format(record.partner_id.vat, str(record.sequence).zfill(4))
            else:
                name = '{}-T{}'.format(record.partner_id.name, str(record.sequence).zfill(4))
            res.append((record.id, name))
        return res


class XionSession(models.Model):
    _name = 'xion.session'
    _description = 'Sesión'

    treatment_id = fields.Many2one('xion.treatment', string='Tratamiento')
    sequence = fields.Integer(string='Secuencia')
    datetime_start = fields.Datetime('Fecha-hora inicio')
    datetime_end = fields.Datetime('Fecha-hora fin')
    voltage = fields.Float('Voltaje')
    duration = fields.Integer('Duración (en minutos)')
    feedback_id = fields.Many2one('xion.catalog', string='Feedback', domain="[('code', '=', {fb})]".format(fb=FEEDBACK))

    def name_get(self):
        res = []
        for record in self:
            if record.sequence:
                name = '{}-S{}'.format(record.treatment_id.display_name, str(record.sequence).zfill(4))
            else:
                name = '{}-S{}'.format(record.treatment_id.display_name, 'X')
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
            treatment = self.env['xion.treatment'].search([('partner_id', '=', partner.id), ('state', '=', ACTIVE)])

            if treatment:
                parametros = {
                    'treatment_id': treatment.id,
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

    treatment_id = fields.Many2one('xion.treatment', string='Tratamiento')
    sequence = fields.Integer(string='Secuencia')
    date = fields.Date('Fecha')
    scale_id = fields.Many2one('xion.catalog', string='HDSS', domain="[('code', '=', {hdss})]".format(hdss=HDSS))
    observation = fields.Char('Observaciones')

    def name_get(self):
        res = []
        for record in self:
            if record.sequence:
                name = '{}-M{}'.format(record.treatment_id.display_name, str(record.sequence).zfill(4))
            else:
                name = '{}-M{}'.format(record.treatment_id.display_name, 'X')
            res.append((record.id, name))
        return res
