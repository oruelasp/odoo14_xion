# -*- coding: utf-8 -*-
from odoo import api, fields, models


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
