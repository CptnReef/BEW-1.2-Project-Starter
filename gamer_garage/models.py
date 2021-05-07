from sqlalchemy_utils import URLType

from flask_login import UserMixin
from gamer_garage import db
from gamer_garage.utils import FormEnum

class ItemSelection(FormEnum):
    """Categories of game selection."""
    MARIO_BROS_1 = 'Mario Bros.1'
    KILLER_INSTINCT = 'Killer Instinct'
    SOUL_REAVER = 'Soul Reaver'
    SONIC_ADVENTURE = 'Sonic Adventure'
    SPYRO = 'Spyro'
    POKEMON_STADIUM = 'Pokemon Stadium'
    GAUNTLET_LEGEND = 'Gauntlet Legend'
    OTHER = 'Other'

class GamerGarage(db.Model):
    """Gamer Garage model."""
    __tablename__="gamer_garage"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    items = db.relationship('GameItem', back_populates='store')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')

class GameItem(db.Model):
    """Game Item model."""
    __tablename__="game_item"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    category = db.Column(db.Enum(ItemSelection), default=ItemSelection.OTHER)
    photo_url = db.Column(db.String(200), nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey('gamer_garage.id'), nullable=False)
    store = db.relationship('GamerGarage', back_populates='items')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    shopping_lists = db.relationship('User', secondary='user_gameitem_sale')

class User(db.Model, UserMixin):
    """User model."""
    __tablename__="user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    shopping_list_items = db.relationship('GameItem', secondary='user_gameitem_sale')
    
class User_GameItem_Sale(db.Model):
    """User_GameItem_Sale Model"""
    __tablename__="user_gameitem_sale"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    groceryitem_id = db.Column(db.Integer, db.ForeignKey('game_item.id'), primary_key=True)
