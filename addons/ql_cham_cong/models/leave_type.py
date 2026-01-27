from odoo import models, fields

class LeaveType(models.Model):
    _name = 'leave.type'
    _description = 'Loại nghỉ phép'

    name = fields.Char('Tên loại nghỉ phép', required=True)
    code = fields.Char('Mã loại', required=True)
    is_paid = fields.Boolean('Có lương', default=False)
    max_days = fields.Float('Số ngày tối đa/năm', default=0)
    active = fields.Boolean('Kích hoạt', default=True)
