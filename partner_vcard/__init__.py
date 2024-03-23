from . import controllers, models


def post_init_hook(env):
    from uuid import uuid4

    for partner in env["res.partner"].with_context(active_test=False).search([]):
        partner.uuid = uuid4()
