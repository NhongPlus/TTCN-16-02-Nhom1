from odoo import models, fields, api

class BangCongThang(models.Model):
    _name = 'bang_cong_thang'
    _description = 'Bảng công tháng'

    nhan_vien_id = fields.Many2one('nhan_vien', required=True, ondelete='cascade')
    thang = fields.Integer(required=True)
    nam = fields.Integer(required=True)

    so_cong = fields.Float("Số công")
    tong_gio_lam = fields.Float("Tổng giờ làm")
    tong_ot = fields.Float("Tổng OT")

    nghi_co_luong = fields.Float("Nghỉ có lương")
    nghi_khong_luong = fields.Float("Nghỉ không lương")

    diem_danh_ids = fields.One2many('diem_danh', 'bang_cong_thang_id')
