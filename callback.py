from odoo import http
import requests

LINE_CHANNEL_SECRET = '89e81ca6e2083978b01a166ed19437b2'
LINE_CHANNEL_ID = '2005695415'

class LineLoginController(http.Controller):
    @http.route('/line/callback', type='http', auth='public', csrf=False)
    def line_callback(self, **kwargs):
        code = kwargs.get('code')
        state = kwargs.get('state')

        # Exchange the authorization code for an access token
        token_url = 'https://api.line.me/oauth2/v2.1/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'YOUR_REDIRECT_URI',
            'client_id': LINE_CHANNEL_ID,
            'client_secret': LINE_CHANNEL_SECRET
        }

        response = requests.post(token_url, headers=headers, data=data)
        token_data = response.json()
        access_token = token_data['access_token']

        # Use the access token to get user profile information
        profile_url = 'https://api.line.me/v2/profile'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_url, headers=headers)
        profile_data = profile_response.json()

        # Extract user information from profile_data
        user_id = profile_data['userId']
        display_name = profile_data['displayName']
        picture_url = profile_data['pictureUrl']

        # Handle user login or registration in Odoo
        # You need to implement the logic to find or create the Odoo user based on LINE user information

        # Redirect to the appropriate page after login
        return http.redirect_with_hash('/web')


class LineLoginController(http.Controller):
    @http.route('/line/callback', type='http', auth='public', csrf=False)
    def line_callback(self, **kwargs):
        code = kwargs.get('code')
        state = kwargs.get('state')

        # Exchange the authorization code for an access token
        token_url = 'https://api.line.me/oauth2/v2.1/token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': 'YOUR_REDIRECT_URI',
            'client_id': LINE_CHANNEL_ID,
            'client_secret': LINE_CHANNEL_SECRET
        }

        response = requests.post(token_url, headers=headers, data=data)
        token_data = response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            return http.redirect_with_hash('/')

        # Use the access token to get user profile information
        profile_url = 'https://api.line.me/v2/profile'
        headers = {'Authorization': f'Bearer {access_token}'}
        profile_response = requests.get(profile_url, headers=headers)
        profile_data = profile_response.json()

        user_id = profile_data.get('userId')
        display_name = profile_data.get('displayName')
        picture_url = profile_data.get('pictureUrl')

        if not user_id:
            return http.redirect_with_hash('/')

        # Handle user login or registration in Odoo
        user = request.env['res.users'].sudo().get_or_create_line_user(user_id, display_name, picture_url)
        request.env.cr.commit()

        # Log the user in
        request.env['ir.http'].session_info()['uid'] = user.id

        # Redirect to the appropriate page after login
        return http.redirect_with_hash('/web')