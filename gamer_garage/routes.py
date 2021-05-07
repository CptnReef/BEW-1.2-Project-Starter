from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from gamer_garage.models import GamerGarage, GameItem, User

from gamer_garage.forms import GameGarageForm, GameItemForm, LoginForm, SignUpForm
from flask_login import login_required, login_user, logout_user, current_user

# Import app and db from events_app package so that we can run app
from gamer_garage import app, db, bcrypt

main = Blueprint("main", __name__)
auth = Blueprint("auth", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GamerGarage.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    gameGarageForm = GameGarageForm()

    if gameGarageForm.validate_on_submit():
        newGameGarage = GamerGarage(
            title=gameGarageForm.title.data,
            address=gameGarageForm.address.data,
            created_by=current_user
        )
        db.session.add(newGameGarage)
        db.session.commit()
        flash('Success')

        return redirect(url_for('main.store_detail', store_id=newGameGarage.id))

    return render_template('new_store.html', gameGarageForm=gameGarageForm, current_user=current_user)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    gameItemForm = GameItemForm()
    if gameItemForm.validate_on_submit():
        newGameItem = GameItem(
            name=gameItemForm.name.data,
            price=gameItemForm.price.data,
            category=gameItemForm.category.data,
            photo_url=gameItemForm.photo_url.data,
            store=gameItemForm.store.data,
            created_by=current_user
        )
        db.session.add(newGameItem)
        db.session.commit()
        flash('Success')

        return redirect(url_for('main.item_detail', item_id=newGameItem.id))
    
    return render_template('new_item.html', gameItemForm=gameItemForm, current_user=current_user)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GamerGarage.query.get(store_id)

    gameGarageForm = GameGarageForm(obj=store)

    if gameGarageForm.validate_on_submit():
        store.title = gameGarageForm.title.data
        store.address = gameGarageForm.address.data
        db.session.commit()
        flash('Success')
        return redirect(url_for('main.store_detail', store_id=store_id))

    store = GamerGarage.query.get(store_id)
    return render_template('store_detail.html', store=store, gameGarageForm=gameGarageForm, current_user=current_user)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GameItem.query.get(item_id)
    gameItemForm = GameItemForm(obj=item)
    
    if gameItemForm.validate_on_submit():
        item.name = gameItemForm.name.data
        item.price = gameItemForm.price.data
        item.category = gameItemForm.category.data
        item.photo_url = gameItemForm.photo_url.data
        item.store = gameItemForm.store.data
        db.session.commit()
        flash('Success')

        return redirect(url_for('main.item_detail', item_id=item_id))

    item = GameItem.query.get(item_id)
    return render_template('item_detail.html', item=item, gameItemForm=gameItemForm, current_user=current_user)

@main.route('/shopping_list')
@login_required
def shopping_list():
    return render_template('game_list.html', current_user=current_user)

@main.route('/game_list', methods=['POST'])
@login_required
def game_list():
    pass
######################################################################################################
######################################################################################################
######################################################################################################

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    print('in signup')
    form = SignUpForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash('Account Created.')
        print('created')
        return redirect(url_for('auth.login'))
    print(form.errors)
    return render_template('signup.html', form=form, current_user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            return redirect(next_page if next_page else url_for('main.homepage'))
    return render_template('login.html', form=form, current_user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.homepage'))