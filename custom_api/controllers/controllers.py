# -*- coding: utf-8 -*-
import json
import requests
from odoo import http, api
from odoo.http import request
import odoo
from odoo.http import Response
from werkzeug.exceptions import BadRequest


class CustomApi(http.Controller):

    def authenticate_user(self):
        access_token = request.httprequest.headers.get('Authorization')
        if not access_token:
            raise BadRequest('Access token missing')

        if access_token.startswith('Bearer '):
            access_token = access_token[7:]

        user_id = request.env["res.users.apikeys"]._check_credentials(
            scope='odoo.plugin.outlook', key=access_token)
        if not user_id:
            raise BadRequest('Access token invalid')
        else:
            return user_id

    # Retrieve existing inventory items
    @http.route('/api/inventory-item', type='http', auth='none', methods=['GET'], csrf=False)
    def get_inventory_items(self, id=None, **kwargs):
        self.authenticate_user()
        # Retrieve inventory items
        inventory_items = request.env['product.template'].sudo().search([])
        serialized_items = [{
            'id': item.id,
            'name': item.name,
            'dimension':
                {
                    'length': item.product_length,
                    'height': item.product_height,
                    'width': item.product_width,
                    'volume': item.volume,
                    'weight': item.weight,

                }
        } for item in inventory_items]
        return json.dumps(serialized_items)

    # Create a new inventory item
    @http.route('/api/inventory-item', type='http', auth='none', methods=['POST'], csrf=False)
    def create_inventory_item(self, id=None, **kwargs):
        user_id = self.authenticate_user()

        try:
            # Retrieve raw data from request body
            data = json.loads(request.httprequest.data)

            record = request.env['product.template'].with_env(request.env(user=user_id)).create({
                'name': data.get('name'),
                'product_length': data.get('length'),
                'product_height': data.get('height'),
                'product_width': data.get('width'),
            })
            return Response(json.dumps(record.id, default=str), status=201)

        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=400)

    # Function to update an existing inventory item
    @http.route('/api/inventory-item/<int:id>', type='http', auth='none', methods=['PUT'], csrf=False)
    def update_record(self, id, **kwargs):
        user_id = self.authenticate_user()
        try:
            record = request.env['product.template'].browse(id)
            if not record.exists():
                return Response(json.dumps({'error': 'Record not found'}), status=404)
            data = json.loads(request.httprequest.data)
            record.with_env(request.env(user=user_id)).write({
                'name': data.get('name'),
                'product_length': data.get('length'),
                'product_height': data.get('height'),
                'product_width': data.get('width'),
            })
            return Response(json.dumps(record.id, default=str))
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=400)

    # Function to delete an inventory item
    @http.route('/api/inventory-item/<int:id>', type='http', auth='none', methods=['DELETE'], csrf=False)
    def delete_inventory_item(self, id):
        self.authenticate_user()
        try:
            record = request.env['product.template'].sudo().browse(id)
            if not record.exists():
                return Response(json.dumps({'error': 'Record not found'}), status=404)
            record.unlink()
            return Response(json.dumps({'message': 'Record deleted'}))
        except Exception as e:
            return Response(json.dumps({'error': str(e)}), status=400)
