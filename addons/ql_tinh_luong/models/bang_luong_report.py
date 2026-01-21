from odoo import models, fields, api
from datetime import datetime


class BangLuongReport(models.Model):
    _name = 'bang_luong.report'
    _description = 'Báo cáo thống kê lương'
    _auto = False
    _order = 'thang desc, nam desc'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', readonly=True)
    thang = fields.Integer(string='Tháng', readonly=True)
    nam = fields.Integer(string='Năm', readonly=True)
    
    tong_thu_nhap = fields.Float(string='Tổng thu nhập', readonly=True)
    tong_khau_tru = fields.Float(string='Tổng khấu trừ', readonly=True)
    thuc_linh = fields.Float(string='Thực lĩnh', readonly=True)
    
    luong_trung_binh = fields.Float(string='Lương trung bình', readonly=True)
    so_nhan_vien = fields.Integer(string='Số nhân viên', readonly=True)

    def init(self):
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW bang_luong_report AS (
                SELECT
                    bl.id,
                    bl.nhan_vien_id,
                    bl.thang,
                    bl.nam,
                    SUM(bl.tong_thu_nhap) as tong_thu_nhap,
                    SUM(bl.tong_khau_tru) as tong_khau_tru,
                    SUM(bl.thuc_linh) as thuc_linh,
                    AVG(bl.thuc_linh) as luong_trung_binh,
                    COUNT(DISTINCT bl.nhan_vien_id) as so_nhan_vien
                FROM bang_luong bl
                WHERE bl.trang_thai IN ('confirmed', 'paid')
                GROUP BY bl.nhan_vien_id, bl.thang, bl.nam, bl.id
            )
        """)
