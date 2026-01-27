from odoo import models, fields, api
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ho_ten_dem = fields.Char("Họ Tên Đệm", required=True)
    ten = fields.Char("Tên", required=True)
    ho_va_ten = fields.Char("Họ Và Tên", compute="_compute_ho_va_ten", store=True )
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    

    gioi_tinh = fields.Selection([
        ('Nam', 'Nam'),
        ('Nu', 'Nữ'),
        ('Khac', 'Khác'),
    ], string="Giới tính", default='Nam')

    chuc_vu_id = fields.Many2one('chuc_vu', string="Chức vụ")
    phong_ban_id = fields.Many2one('phong_ban', string="Phòng Ban")
    # lich_lam_viec_ids = fields.One2many('lich_lam_viec', 'nhan_vien_id', string="Lịch làm việc")

    @api.depends("ho_ten_dem", "ten")
    def _compute_ho_va_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_va_ten = record.ho_ten_dem + ' ' + record.ten

    @api.depends("hop_dong_id")
    def _compute_hop_dong(self):
        for rec in self:
            hop_dong = self.env["hop_dong"].search([
                ("nhan_vien_id", "=", rec.id)
            ], limit=1, order="ngay_bat_dau desc")

            rec.hop_dong_id = hop_dong.id if hop_dong else False

    @api.onchange("ten", "ho_ten_dem")
    def _default_ma_dinh_danh(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                chu_cai_dau = '' . join([tu[0][0] for tu in record.ho_ten_dem.lower().split()])
                record.ma_dinh_danh = record.ten.lower() + chu_cai_dau
    
    def action_import_csv(self):
        """Mở form để import CSV data"""
        return {
            'name': 'Import Nhân Viên',
            'type': 'ir.actions.act_window',
            'res_model': 'nhan_vien.import.csv',
            'view_mode': 'form',
            'target': 'new',
        }
    
    @api.model
    def import_csv_data(self, csv_text):
        """Import nhân viên từ dữ liệu CSV (tab-separated)"""
        if not csv_text or not csv_text.strip():
            raise ValidationError("Vui lòng nhập dữ liệu!")
        
        lines = csv_text.strip().split('\n')
        if len(lines) < 1:
            raise ValidationError("File CSV không có dữ liệu!")
        
        imported_count = 0
        error_rows = []
        
        for row_idx, line in enumerate(lines, start=1):
            try:
                if not line.strip():
                    continue
                
                parts = [p.strip() for p in line.split('\t')]
                
                if len(parts) < 3:
                    error_rows.append(f"Dòng {row_idx}: Thiếu cột (cần ít nhất: Mã, Họ Đệm, Tên)")
                    continue
                
                ma_dinh_danh = parts[0] or ''
                ho_ten_dem = parts[1] or ''
                ten = parts[2] or ''
                gioi_tinh = parts[4].strip() if len(parts) > 4 and parts[4] else 'Nam'
                email = parts[5].strip() if len(parts) > 5 and parts[5] else ''
                chuc_vu_name = parts[6].strip() if len(parts) > 6 and parts[6] else ''
                phong_ban_name = parts[7].strip() if len(parts) > 7 and parts[7] else ''
                so_dien_thoai = parts[8].strip() if len(parts) > 8 and parts[8] else ''
                
                # Validate
                if not ma_dinh_danh or not ho_ten_dem or not ten:
                    error_rows.append(f"Dòng {row_idx}: Mã định danh, Họ tên đệm hoặc Tên không được để trống")
                    continue
                
                # Kiểm tra trùng lặp
                existing = self.search([('ma_dinh_danh', '=', ma_dinh_danh)])
                if existing:
                    error_rows.append(f"Dòng {row_idx}: Mã '{ma_dinh_danh}' đã tồn tại")
                    continue
                
                # Lấy hoặc tạo chức vụ
                chuc_vu_id = False
                if chuc_vu_name:
                    chuc_vu = self.env['chuc_vu'].search([('name', '=', chuc_vu_name)], limit=1)
                    if chuc_vu:
                        chuc_vu_id = chuc_vu.id
                    else:
                        chuc_vu_id = self.env['chuc_vu'].create({'name': chuc_vu_name}).id
                
                # Lấy hoặc tạo phòng ban
                phong_ban_id = False
                if phong_ban_name:
                    phong_ban = self.env['phong_ban'].search([('name', '=', phong_ban_name)], limit=1)
                    if phong_ban:
                        phong_ban_id = phong_ban.id
                    else:
                        phong_ban_id = self.env['phong_ban'].create({'name': phong_ban_name}).id
                
                # Tạo nhân viên
                self.create({
                    'ma_dinh_danh': ma_dinh_danh,
                    'ho_ten_dem': ho_ten_dem,
                    'ten': ten,
                    'gioi_tinh': 'Nam' if gioi_tinh == 'Nam' else 'Nu' if 'nữ' in gioi_tinh.lower() else 'Khac',
                    'email': email,
                    'so_dien_thoai': so_dien_thoai,
                    'chuc_vu_id': chuc_vu_id,
                    'phong_ban_id': phong_ban_id,
                })
                imported_count += 1
            
            except Exception as e:
                error_rows.append(f"Dòng {row_idx}: {str(e)}")
        
        # Thông báo kết quả
        message = f"✅ Import thành công {imported_count} nhân viên!"
        if error_rows:
            message += f"\n\n❌ Lỗi:\n" + "\n".join(error_rows[:10])
            if len(error_rows) > 10:
                message += f"\n... và {len(error_rows) - 10} lỗi khác"
        
        raise ValidationError(message)
    
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'unique(ma_dinh_danh)', 'Mã Định Danh Phải Là Duy Nhất')
    ]