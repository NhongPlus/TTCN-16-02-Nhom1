# -*- coding: utf-8 -*-
from odoo import models, fields
from datetime import date

class HopDong(models.Model):
    _name = 'hop_dong'
    _description = 'Hợp đồng lao động'

    name = fields.Char("Số hợp đồng", required=True)
    
    # Nhân viên
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True,
        ondelete='cascade'
    )
    
    # Cấu trúc lương
    salary_structure_id = fields.Many2one(
        'salary.structure',
        string="Cấu trúc lương",
        required=True
    )
    
    # Lương cơ bản
    basic_salary = fields.Float("Lương cơ bản", required=True)
    
    # Loại hợp đồng
    type_id = fields.Many2one(
        'hop_dong.type',
        string="Loại hợp đồng",
        required=True
    )
    
    # Thời gian
    date_start = fields.Date("Ngày bắt đầu", required=True, default=lambda self: date.today())
    date_end = fields.Date("Ngày kết thúc")
    
    # Trạng thái
    state = fields.Selection([
        ('draft', 'Nháp'),
        ('open', 'Hiệu lực'),
        ('close', 'Kết thúc'),
    ], string="Trạng thái", default='draft')
    
    # Các phụ cấp
    allowance_ids = fields.One2many(
        'hop_dong.allowance',
        'contract_id',
        string="Phụ cấp"
    )
    
    mo_ta = fields.Text("Ghi chú")
    
    def action_open(self):
        """Kích hoạt hợp đồng"""
        self.state = 'open'
    
    def action_close(self):
        """Kết thúc hợp đồng"""
        self.state = 'close'
        self.date_end = date.today()


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
    amount = fields.Float("Số tiền", required=True)
    
    type_id = fields.Many2one(
        'salary.rule.category',
        string="Loại phụ cấp"
    )
