from . import models


def post_init_hook(env):
    for model, fields in (
        ("phone", ("phone", "mobile")),
        ("email", ("email",)),
        ("website", ("website",)),
    ):
        env[f"res.partner.{model}"].create(
            [
                {
                    "partner_id": partner.id,
                    "name": getattr(partner, field),
                    **{"type2": "cell" for _ in range(1) if field == "mobile"},
                }
                for field in fields
                for partner in env["res.partner"]
                .with_context(active_test=False)
                .search([(field, "!=", False)])
            ]
        )
