from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta

class DiemDanh(models.Model):
    _name = 'diem_danh'
    _description = 'Bảng Điểm Danh'

    nhan_vien_id = fields.Many2one('nhan_vien', string="Nhân Viên", required=True, ondelete='cascade')
    ngay_lam_viec = fields.Date(related='lich_lam_viec_id.ngay_lam_viec', store=True)
    ngay_trong_tuan = fields.Char(string="Ngày trong tuần", compute='_compute_ngay_trong_tuan', store=True)
    gio_check_in = fields.Datetime(string="Giờ Check-In")
    gio_check_out = fields.Datetime(string="Giờ Check-Out")
    di_muon_phut = fields.Integer("Đi muộn (phút)")
    ve_som_phut = fields.Integer("Về sớm (phút)")
    so_gio_lam_thuc_te = fields.Float("Giờ làm thực tế")
    so_cong = fields.Float("Ngày công", default=1.0)
    bang_cong_thang_id = fields.Many2one('bang_cong_thang', string="Bảng công tháng")

    lich_lam_viec_id = fields.Many2one(
        'lich_lam_viec', string="Lịch Làm Việc",
        domain="[('nhan_vien_id', '=', nhan_vien_id), ('trang_thai', '=', 'da_duyet')]"
    )
    ca_lam_viec_id = fields.Many2one(related='lich_lam_viec_id.ca_lam_viec_id', string="Ca Làm Việc", store=True, readonly=True)
    loai_cong_viec = fields.Selection(related='lich_lam_viec_id.loai_cong_viec', string="Loại công việc", store=True, readonly=True)
    
    trang_thai_diem_danh = fields.Selection(
        [('draft', 'Nháp'),
         ('som', 'Sớm'),
         ('dung_gio', 'Đúng Giờ'),
         ('muon', 'Muộn')],
        string="Trạng Thái Điểm Danh",
        default='draft'
    )
    
    trang_thai_phe_duyet = fields.Selection(
        [('draft', 'Nháp'),
         ('approved', 'Đã Duyệt'),
         ('rejected', 'Bị Từ Chối')],
        string="Trạng Thái Phê Duyệt",
        default='draft'
    )
    
    ghi_chu = fields.Text(string="Ghi chú")

    @api.depends('ngay_lam_viec')
    def _compute_ngay_trong_tuan(self):
        """Tính ngày trong tuần từ ngay_lam_viec"""
        days_vn = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật']
        for rec in self:
            if rec.ngay_lam_viec:
                day_index = rec.ngay_lam_viec.weekday()
                rec.ngay_trong_tuan = days_vn[day_index]
            else:
                rec.ngay_trong_tuan = ''

    @api.model
    def get_start_time(self):
        """
        Lấy giờ bắt đầu ca làm việc từ model ca_lam_viec.
        """
        if self.ca_lam_viec_id and self.ngay_lam_viec:
            gio_bat_dau = self.ca_lam_viec_id.gio_bat_dau
            gio = int(gio_bat_dau)
            phut = int((gio_bat_dau - gio) * 60)
            ngay_gio_bat_dau = f"{self.ngay_lam_viec} {gio:02d}:{phut:02d}:00"
            return datetime.strptime(ngay_gio_bat_dau, "%Y-%m-%d %H:%M:%S")
        return None

    def check_in_out(self):
        """
        - Check-In: Ghi nhận thời gian thực tế và xác định trạng thái (Sớm, Đúng Giờ, Muộn).
        - Check-Out: Ghi nhận thời gian rời đi.
        """
        for rec in self:
            now = fields.Datetime.now()

            if not rec.gio_check_in:
                start_time = rec.get_start_time()
                if start_time:
                    if now < start_time:
                        rec.trang_thai_diem_danh = "som"
                    elif now == start_time:
                        rec.trang_thai_diem_danh = "dung_gio"
                    else:
                        rec.trang_thai_diem_danh = "muon"
                
                rec.gio_check_in = now
            elif not rec.gio_check_out:
                rec.gio_check_out = now
            else:
                raise UserError("Bạn đã hoàn thành điểm danh hôm nay!")

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
