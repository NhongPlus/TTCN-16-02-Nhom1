from odoo import models, fields, api
from datetime import datetime, timedelta


class BangLuongWizard(models.TransientModel):
    _name = 'bang_luong.wizard'
    _description = 'Wizard tạo báo cáo lương'

    thang = fields.Integer(string='Tháng', default=lambda self: datetime.now().month)
    nam = fields.Integer(string='Năm', default=lambda self: datetime.now().year)
    phong_ban_id = fields.Many2one('phong_ban', string='Phòng Ban')
    chuc_vu_id = fields.Many2one('chuc_vu', string='Chức vụ')
    
    def action_generate_report(self):
        """Tạo báo cáo lương cho tháng/năm"""
        domain = [('thang', '=', self.thang), ('nam', '=', self.nam)]
        
        if self.phong_ban_id:
            domain.append(('nhan_vien_id.phong_ban_id', '=', self.phong_ban_id.id))
        
        if self.chuc_vu_id:
            domain.append(('nhan_vien_id.chuc_vu_id', '=', self.chuc_vu_id.id))
        
        payslips = self.env['bang_luong'].search(domain)
        
        return {
            'type': 'ir.actions.act_window',
            'name': f'Báo cáo lương tháng {self.thang}/{self.nam}',
            'res_model': 'bang_luong',
            'view_mode': 'tree,graph,form',
            'domain': domain,
            'context': {'group_by': 'nhan_vien_id'}
        }
