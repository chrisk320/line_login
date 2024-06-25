from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    line_user_id = fields.Char('LINE User ID')

    @api.model
    def get_or_create_line_user(self, line_user_id, display_name, picture_url):
        user = self.search([('line_user_id', '=', line_user_id)], limit=1)
        if not user:
            # Create a new user if not found
            user = self.create({
                'name': display_name,
                'login': f'line_{line_user_id}',
                'line_user_id': line_user_id,
                'image_1920': self.env['ir.attachment'].sudo()._get_binary_content_from_url(picture_url)
            })
        return user
