from odoo.addons.onlyoffice_odoo.controllers.controllers import Onlyoffice_Connector


class OnlyOfficeConnector(Onlyoffice_Connector):
    def prepare_editor_values(self, attachment, access_token, can_write):
        return super().prepare_editor_values(attachment, access_token, True)
