from . import models


def post_init_hook(env):
    env["res.partner"]._mig_enhanced_fields()
