import datetime
import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _rec_name = 'ten_phong_ban'
    _order = 'ma_phong_ban asc, ten_phong_ban asc'
    _sql_constraints = [
        ('ma_phong_ban_unique', 'unique(ma_phong_ban)', 'Mã phòng ban phải là duy nhất!')
    ]


    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    mo_ta = fields.Text("Mô tả")
    nhan_vien_ids = fields.Many2many(
        comodel_name='nhan_vien', 
        string='Nhân viên'
    )