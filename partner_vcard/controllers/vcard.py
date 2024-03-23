from odoo import http
from odoo.http import request


class VcardController(http.Controller):
    @http.route("/vcard/<string:uuid>", type="http", auth="public", methods=["GET"])
    def get_vcard(self, uuid):
        partner = (
            request.env["res.partner"].sudo().search([("uuid", "=", uuid)], limit=1)
        )
        if not partner:
            return request.not_found()
        return request.make_response(partner.vcard, [("content-type", "text/vcard")])
