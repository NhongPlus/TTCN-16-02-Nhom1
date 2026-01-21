import datetime
import re

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten' #trường của _rec_name là gì?
    _order = 'ma_dinh_danh asc, ngay_sinh desc, ho_ten asc' #có code sắp sếp theo một trường rồi thì code sắp sếp theo hai trường là gì và như thế nào?
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất!')
    ]


    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_ten = fields.Char("Họ và tên", required=True)
    cccd = fields.Char("CCCD")
    ms_bhxh = fields.Char("Mã số BHXH")
    salary = fields.Float("Lương")
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    phong_ban_ids = fields.Many2many(
        comodel_name='phong_ban',
        string='Phòng ban'
    )
    chung_chi_ids = fields.One2many(
        comodel_name='chung_chi', 
        inverse_name="nhan_vien_ids",
        string="Chứng chỉ"
    )
