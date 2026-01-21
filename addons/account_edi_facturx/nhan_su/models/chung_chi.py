import datetime
import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ChungChi(models.Model):
    _name = 'chung_chi'
    _description = 'Bảng chứa thông tin chứng chỉ'
    _rec_name = 'ten_chung_chi'
    _order = 'ma_chung_chi asc, ten_chung_chi asc'
    _sql_constraints = [
        ('ma_chung_chi_unique', 'unique(ma_chung_chi)', 'Mã chứng chỉ phải là duy nhất!')
    ]


    ma_chung_chi = fields.Char("Mã chứng chỉ", required=True, store=True)
    ten_chung_chi = fields.Char("Tên chứng chỉ", required=True)
    ghi_chu = fields.Text("ghi_chu")
    nhan_vien_ids = fields.Many2one(
        comodel_name='nhan_vien', 
        string="Nhân viên", 
        store=True
    )