from odoo import models, fields, api

class CaLamViec(models.Model):
    _name = 'ca_lam_viec'
    _description = 'Ca làm việc & quy tắc chấm công'

    name = fields.Char("Tên ca", required=True)

    gio_bat_dau = fields.Float("Giờ bắt đầu", required=True)
    gio_ket_thuc = fields.Float("Giờ kết thúc", required=True)
    gio_nghi_trua = fields.Float("Thời gian nghỉ trưa", required=True)
    so_gio_tieu_chuan = fields.Float("Số giờ tiêu chuẩn", compute="_compute_so_gio", store=True)

    cho_phep_di_muon = fields.Integer("Phút cho phép đi muộn", default=0)
    cho_phep_ve_som = fields.Integer("Phút cho phép về sớm", default=0)

    tinh_ot_sau = fields.Float("Tính OT sau (giờ)", default=0.0)

    @api.depends('gio_bat_dau', 'gio_ket_thuc', 'gio_nghi_trua')
    def _compute_so_gio(self):
        for rec in self:
            if rec.gio_ket_thuc >= rec.gio_bat_dau:
                total_hours = rec.gio_ket_thuc - rec.gio_bat_dau
            else:
                total_hours = (24 - rec.gio_bat_dau) + rec.gio_ket_thuc
            rec.so_gio_tieu_chuan = total_hours - rec.gio_nghi_trua
