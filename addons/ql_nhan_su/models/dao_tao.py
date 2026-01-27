from odoo import models, fields

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class DaoTao(models.Model):
    _name = 'ql.dao.tao'
    _description = 'Đào Tạo'
    name = fields.Char('Tên Đào Tạo', required=True)
    ngay_bat_dau = fields.Date('Ngày bắt đầu', required=True)
    ngay_ket_thuc = fields.Date('Ngày kết thúc', required=True)
    nhan_vien_ids = fields.Many2many('nhan_vien', string='Nhân viên tham gia')
    mo_ta = fields.Text('Mô tả')
    trang_thai = fields.Selection([
        ('du_kien', 'Dự kiến'),
        ('dang_dien_ra', 'Đang diễn ra'),
        ('hoan_thanh', 'Hoàn thành'),
        ('huy', 'Hủy')
    ], string='Trạng thái', default='du_kien')

    @api.constrains('ngay_bat_dau', 'ngay_ket_thuc')
    def _check_ngay_bat_dau_ket_thuc(self):
        for rec in self:
            if rec.ngay_bat_dau and rec.ngay_ket_thuc and rec.ngay_ket_thuc < rec.ngay_bat_dau:
                raise ValidationError('Ngày kết thúc không được nhỏ hơn ngày bắt đầu!')