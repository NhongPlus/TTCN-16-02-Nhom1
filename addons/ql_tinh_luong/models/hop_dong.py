# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HopDong(models.Model):
    _name = 'hop_dong'
    _description = 'Hợp đồng lao động'

    name = fields.Char("Số hợp đồng", required=True)
    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân viên", required=True, ondelete='cascade')
    salary_structure_id = fields.Many2one('salary.structure', string="Cấu trúc lương", required=True)
    basic_salary = fields.Float("Lương cơ bản (VND)", required=True)
    type_id = fields.Many2one('hop_dong.type', string="Loại hợp đồng", required=True)
    date_start = fields.Date("Ngày bắt đầu", required=True, default=lambda self: date.today())
    date_end = fields.Date("Ngày kết thúc")
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('open', 'Hiệu lực'),
        ('close', 'Kết thúc'),
    ], string="Trạng thái", default='draft')
    allowance_ids = fields.One2many('hop_dong.allowance', 'contract_id', string="Phụ cấp")

    mo_ta = fields.Text("Ghi chú")
    is_unlimited_contract = fields.Boolean(string="Hợp đồng vô thời hạn", compute="_compute_is_unlimited_contract")

    @api.depends('type_id')
    def _compute_is_unlimited_contract(self):
        for rec in self:
            rec.is_unlimited_contract = rec.type_id and rec.type_id.code == 'FIXED'

    @api.constrains('date_start', 'date_end', 'type_id')
    def _check_dates(self):
        for rec in self:
            # Nếu loại hợp đồng là vô thời hạn (code = FIXED) thì không được nhập ngày kết thúc
            if rec.type_id and rec.type_id.code == 'FIXED':
                if rec.date_end:
                    raise ValidationError('Hợp đồng vô thời hạn không được nhập ngày kết thúc!')
            else:
                # Các loại hợp đồng khác phải có ngày kết thúc
                if not rec.date_end:
                    raise ValidationError('Hợp đồng có thời hạn phải nhập ngày kết thúc!')
                if rec.date_start and rec.date_end and rec.date_end < rec.date_start:
                    raise ValidationError('Ngày kết thúc không được nhỏ hơn ngày bắt đầu!')

    @api.constrains('basic_salary')
    def _check_basic_salary(self):
        for rec in self:
            if rec.basic_salary == 0:
                raise ValidationError('Lương cơ bản phải khác 0!')

    @api.constrains('allowance_ids')
    def _check_allowance_amount(self):
        for rec in self:
            for allowance in rec.allowance_ids:
                if allowance.amount == 0:
                    raise ValidationError('Số tiền phụ cấp phải khác 0!')

    @api.model
    def create(self, vals):
        # Thêm prefix cho số hợp đồng nếu chưa có
        prefix = 'HD-'
        if 'name' in vals and vals['name'] and not vals['name'].startswith(prefix):
            vals['name'] = prefix + vals['name']
        return super().create(vals)

    def write(self, vals):
        # Đảm bảo prefix khi sửa số hợp đồng
        prefix = 'HD-'
        if 'name' in vals and vals['name'] and not vals['name'].startswith(prefix):
            vals['name'] = prefix + vals['name']
        return super().write(vals)

    def action_open(self):
        for rec in self:
            rec.state = 'open'

    def action_close(self):
        for rec in self:
            rec.state = 'close'
            rec.date_end = date.today()


class HopDongType(models.Model):
    _name = 'hop_dong.type'
    _description = 'Loại hợp đồng'
    
    name = fields.Char("Tên loại hợp đồng", required=True)
    code = fields.Char("Mã loại hợp đồng", required=True)


class HopDongAllowance(models.Model):
    _name = 'hop_dong.allowance'
    _description = 'Phụ cấp hợp đồng'
    
    contract_id = fields.Many2one(
        'hop_dong',
        string="Hợp đồng",
        required=True,
        ondelete='cascade'
    )
    
    name = fields.Char("Tên phụ cấp", required=True)
    amount = fields.Float("Số tiền (VND)", required=True)
    
    type_id = fields.Many2one(
        'salary.rule.category',
        string="Loại phụ cấp"
    )
