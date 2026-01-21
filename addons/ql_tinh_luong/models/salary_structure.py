# -*- coding: utf-8 -*-
from odoo import models, fields

class SalaryStructure(models.Model):
    _name = 'salary.structure'
    _description = 'Cấu trúc lương'

    name = fields.Char("Tên cấu trúc lương", required=True)
    mo_ta = fields.Text("Mô tả")
    
    # Danh sách quy tắc tính lương
    salary_rule_ids = fields.Many2many(
        'salary.rule',
        'salary_structure_rule_rel',
        'structure_id',
        'rule_id',
        string="Quy tắc lương"
    )
    
    # Trạng thái
    active = fields.Boolean("Hoạt động", default=True)
