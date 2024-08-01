from odoo import models, fields, api 
import random
import requests

class PokemonMaster(models.Model):
    _inherit = 'res.partner'

    pokemon_id = fields.Integer(string="Pokemon ID")
    pokemon_name = fields.Char(string="Pokemon Name")
    pokemon_ability_ids = fields.One2many('pokemon.ability', 'partner_id', string='Pokemon Ability')
    pokemon_game_ids = fields.One2many('pokemon.game', 'partner_id', string='Pokemon Game')
    pokemon_move_ids = fields.One2many('pokemon.move', 'partner_id', string='Pokemon Move')
    pokemon_stat_ids = fields.One2many('pokemon.stat', 'partner_id', string='Pokemon Stat')

    def get_existing_pokemon_id(self):
        existing_pokemon_ids = self.search([]).mapped('pokemon_id')
        return set(existing_pokemon_ids)

    def action_get_pokemon(self):
        for partner in self:
            if partner.is_company:
                
                partner.pokemon_ability_ids.unlink()
                partner.pokemon_game_ids.unlink()
                partner.pokemon_move_ids.unlink()
                partner.pokemon_stat_ids.unlink()

                existing_pokemon_ids = self.get_existing_pokemon_id()

                pokemon_id = random.randint(1, 898)
                while pokemon_id in existing_pokemon_ids:
                    pokemon_id = random.randint(1, 898)

                url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_id}"
                response = requests.get(url)
                if response.status_code == 200:
                    pokemon_data = response.json()
                    partner.write({
                        'pokemon_id': pokemon_id,
                        'pokemon_name': pokemon_data['name'],
                    })

                    for ability in pokemon_data['abilities']:
                        self.env['pokemon.ability'].create({
                            'partner_id': partner.id,
                            'name': ability['ability']['name'],
                            'is_hidden': ability['is_hidden']
                        })

                    for game_index in pokemon_data['game_indices']:
                        self.env['pokemon.game'].create({
                            'partner_id': partner.id,
                            'name': game_index['version']['name']
                        })

                    for move in pokemon_data['moves']:
                        self.env['pokemon.move'].create({
                            'partner_id': partner.id,
                            'name': move['move']['name']
                        })

                    for stat in pokemon_data['stats']:
                        self.env['pokemon.stat'].create({
                            'partner_id': partner.id,
                            'name': stat['stat']['name'],
                            'base_stat': stat['base_stat'],
                            'effort': stat['effort'],
                        })


class PokemonAbility(models.Model):
    _name = 'pokemon.ability'

    partner_id = fields.Many2one('res.partner', string="Company", ondelete="cascade")
    name = fields.Char(string="Ability Name")
    is_hidden = fields.Boolean(string="Is Hidden")

class PokemonGame(models.Model):
    _name = 'pokemon.game'

    partner_id = fields.Many2one('res.partner', string="Company", ondelete="cascade")
    name = fields.Char(string="Game Name")

class PokemonMove(models.Model):
    _name = 'pokemon.move'

    partner_id = fields.Many2one('res.partner', string="Company", ondelete="cascade")
    name = fields.Char(string="Move Name")

class PokemonStat(models.Model):
    _name = 'pokemon.stat'

    partner_id = fields.Many2one('res.partner', string="Company", ondelete="cascade")
    name = fields.Char(string="Stat Name")
    base_stat = fields.Integer(string="Base Stat")
    effort = fields.Integer(string="Effort")



    

