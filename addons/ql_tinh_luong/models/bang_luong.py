from odoo import models, fields, api

class BangLuong(models.Model):
    _name = 'bang_luong'
    _description = 'Bảng lương tháng'

    nhan_vien_id = fields.Many2one('nhan_vien', string='Nhân viên', required=True)
    hop_dong_id = fields.Many2one('hop_dong', string='Hợp đồng', compute='_compute_hop_dong', store=True)
    basic_salary = fields.Float(string='Lương cơ bản', compute='_compute_basic_salary', store=True)
    
    thang = fields.Integer(string='Tháng', required=True)
    nam = fields.Integer(string='Năm', required=True)
    
    worked_days = fields.Float(string='Số ngày công', default=26.0)
    overtime_hours = fields.Float(string='Số giờ OT', default=0.0)
    advance = fields.Float(string='Tạm ứng', default=0.0)

    basic = fields.Float(string='Lương cơ bản', compute='_compute_components', store=True)
    gross = fields.Float(string='Lương thực tế', compute='_compute_components', store=True)
    overtime = fields.Float(string='Phụ cấp OT', compute='_compute_components', store=True)
    allowance = fields.Float(string='Phụ cấp khác', compute='_compute_components', store=True)
    insurance = fields.Float(string='Bảo hiểm', compute='_compute_components', store=True)
    
    tong_thu_nhap = fields.Float(string='Tổng thu nhập', compute='_compute_components', store=True)
    tong_khau_tru = fields.Float(string='Tổng khấu trừ', compute='_compute_components', store=True)
    thuc_linh = fields.Float(string='Thực lĩnh', compute='_compute_components', store=True)

    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('confirmed', 'Đã xác nhận'),
        ('paid', 'Đã chi trả'),
    ], string='Trạng thái', default='draft')

    ghi_chu = fields.Text(string='Ghi chú')

    @api.depends('nhan_vien_id')
    def _compute_hop_dong(self):
        for rec in self:
            contract = self.env['hop_dong'].search([
                ('nhan_vien_id', '=', rec.nhan_vien_id.id),
                ('state', '=', 'open')
            ], limit=1)
            rec.hop_dong_id = contract.id if contract else False

    @api.depends('hop_dong_id')
    def _compute_basic_salary(self):
        for rec in self:
            if rec.hop_dong_id:
                rec.basic_salary = rec.hop_dong_id.basic_salary
            else:
                rec.basic_salary = 0.0

    @api.depends('hop_dong_id', 'worked_days', 'overtime_hours', 'advance')
    def _compute_components(self):
        for rec in self:
            if not rec.hop_dong_id:
                rec.basic = 0.0
                rec.gross = 0.0
                rec.overtime = 0.0
                rec.allowance = 0.0
                rec.insurance = 0.0
                rec.tong_thu_nhap = 0.0
                rec.tong_khau_tru = 0.0
                rec.thuc_linh = 0.0
                continue
            
            # Calculate basic salary
            rec.basic = rec.basic_salary
            
            # Calculate gross salary (pro-rata by worked days)
            rec.gross = rec.basic_salary * (rec.worked_days / 26.0) if rec.basic_salary else 0.0
            
            # Calculate overtime (150% of hourly rate)
            if rec.hop_dong_id.salary_structure_id:
                has_ot_rule = any(rule.code == 'OT' for rule in rec.hop_dong_id.salary_structure_id.salary_rule_ids)
                if has_ot_rule and rec.overtime_hours > 0:
                    hourly_rate = rec.basic_salary / (26 * 8) if rec.basic_salary else 0.0
                    rec.overtime = hourly_rate * rec.overtime_hours * 1.5
                else:
                    rec.overtime = 0.0
            else:
                rec.overtime = 0.0
            
            # Calculate allowances from contract
            rec.allowance = sum([a.amount for a in rec.hop_dong_id.allowance_ids]) if rec.hop_dong_id.allowance_ids else 0.0
            
            # Calculate insurance (10% of gross)
            rec.insurance = rec.gross * 0.1
            
            # Calculate totals
            rec.tong_thu_nhap = rec.gross + rec.overtime + rec.allowance
            rec.tong_khau_tru = rec.insurance + rec.advance
            rec.thuc_linh = rec.tong_thu_nhap - rec.tong_khau_tru
