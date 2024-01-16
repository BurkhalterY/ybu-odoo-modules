from odoo import api, fields, models


class TableFootballMatch(models.Model):
    _name = "table.football.match"
    _description = "Table Football Match"
    _inherit = ["mail.thread"]
    _order = "date desc"

    name = fields.Char("Name", compute="_compute_name", store=True)
    date = fields.Datetime("Date", default=fields.Datetime.now, required=True)
    winner_ids = fields.Many2many(
        "res.partner",
        relation="table_football_match_winner",
        string="Winner Team",
        required=True,
    )
    loser_ids = fields.Many2many(
        "res.partner",
        relation="table_football_match_loser",
        string="Loser Team",
        required=True,
    )
    winner_score = fields.Integer("Winner Score", tracking=True)
    loser_score = fields.Integer("Loser Score", tracking=True)
    priority = fields.Selection(
        [("0", "Normal"), ("1", "Important")],
        string="Important Match",
        default="0",
        tracking=True,
    )

    @api.model
    def _get_stylized_score(self, score):
        if score == 10:
            return "🔟"
        if score == 100:
            return "💯"
        return "".join([n + "\ufe0f" for n in str(score)])

    @api.depends("winner_ids.name", "loser_ids.name", "winner_score", "loser_score")
    def _compute_name(self):
        for match in self:
            match.name = (
                "{winner_names} {winner_score}🆚{loser_score} {loser_names}".format(
                    winner_names=", ".join(match.winner_ids.mapped("name")),
                    loser_names=", ".join(match.loser_ids.mapped("name")),
                    winner_score=self._get_stylized_score(match.winner_score),
                    loser_score=self._get_stylized_score(match.loser_score),
                )
            )

    def fix_winner(self):
        for match in self:
            if match.loser_score > match.winner_score:
                match.loser_score, match.winner_score = (
                    match.winner_score,
                    match.loser_score,
                )
                match.loser_ids, match.winner_ids = match.winner_ids, match.loser_ids

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.fix_winner()
        return res

    def write(self, vals):
        res = super().write(vals)
        self.fix_winner()
        return res
