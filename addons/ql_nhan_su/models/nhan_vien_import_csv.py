from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NhanVienImportCSV(models.TransientModel):
    _name = 'nhan_vien.import.csv'
    _description = 'Import Nhân Viên từ CSV'

    csv_data = fields.Text(string="Dữ Liệu CSV (Paste từ Excel)", required=True, 
                           placeholder="Mã\tHọ Đệm\tTên\t...\nlong\tNguyễn Ngọc Bảo\tLong\t...")
    
    def action_import(self):
        """Gọi method import từ model nhan_vien"""
        self.env['nhan_vien'].import_csv_data(self.csv_data)
        return {'type': 'ir.actions.act_window_close'}
