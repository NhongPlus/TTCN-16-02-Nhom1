# -*- coding: utf-8 -*-
from odoo import models, fields

class SalaryRule(models.Model):
    _name = 'salary.rule'
    _description = 'Quy tắc tính lương'
    _order = 'sequence,id'

    name = fields.Char("Tên quy tắc", required=True)
    code = fields.Char("Mã quy tắc", required=True, help="VD: BASIC, GROSS, OT, NET")
    
    sequence = fields.Integer("Thứ tự tính", default=10, help="Thứ tự ưu tiên tính")
    
    # Loại quy tắc
    category_id = fields.Many2one(
        'salary.rule.category',
        string="Danh mục",
        help="GROSS, DEDUCTION, NET"
    )
    
    # Công thức tính
    amount_type = fields.Selection([
        ('fixed', 'Cố định'),
        ('percentage', 'Phần trăm'),
        ('python', 'Python Code'),
    ], string="Loại tính", default='fixed', required=True)
    
    amount_fixed = fields.Float("Số tiền cố định", default=0.0)
    amount_percentage = fields.Float("Phần trăm", default=0.0)
    amount_python_compute = fields.Text("Code Python", help="VD: result = employee.basic_salary * 0.1")
    
    # Điều kiện áp dụng
    condition_select = fields.Selection([
        ('none', 'Không'),
        ('python', 'Python Code'),
    ], string="Điều kiện", default='none')
    
    condition_python = fields.Text("Điều kiện Python", help="VD: result = employee.department_id.name == 'IT'")
    
    # Quy tắc phụ thuộc
    parent_rule_id = fields.Many2one(
        'salary.rule',
        string="Quy tắc cha",
        help="Nếu có, quy tắc này phụ thuộc vào quy tắc khác"
    )
    
    mo_ta = fields.Text("Mô tả")
    active = fields.Boolean("Hoạt động", default=True)


class SalaryRuleCategory(models.Model):
    _name = 'salary.rule.category'
    _description = 'Danh mục quy tắc lương'
    
    name = fields.Char("Tên danh mục", required=True)
    code = fields.Char("Mã danh mục", required=True)
    parent_id = fields.Many2one('salary.rule.category', string="Danh mục cha")
