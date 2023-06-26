#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakery_list = []
    for bakery_obj in Bakery.query.all():
        bakery_dict = {
            "name": bakery_obj.name,
        }
        bakery_list.append(bakery_dict)

    response = make_response(
        jsonify(bakery_list),
        200
    )

    return response




@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery_obj = Bakery.query.filter(Bakery.id == id).first()
    if bakery_obj is None:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

    bakery_dict = {
        'id': bakery_obj.id,
        'name': bakery_obj.name,
        'created_at':bakery_obj.created_at
    }

    response = make_response(jsonify(bakery_dict), 200)
    return response



@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = BakedGood.query.all()

    baked_goods_list = []
    for baked_goods_obj in baked_goods:
        baked_goods_dict = {
            "name": baked_goods_obj.name,
            "price": baked_goods_obj.price,
            "bakery": {
                "id": baked_goods_obj.bakery.id,
                "name": baked_goods_obj.bakery.name,
            }
        }
        baked_goods_list.append(baked_goods_dict)

    response = make_response(
        jsonify(baked_goods_list),
        200
    )

    return response


@app.route('/baked_goods/most_expensive/<int:price>')
def most_expensive_baked_good(price):
    baked_goods_obj = BakedGood.query.filter(BakedGood.price == price).order_by(BakedGood.price.desc()).first()
    if baked_goods_obj is None:
        return make_response(jsonify({'error': 'Bakery not found'}), 404)

    bakery_dict = {
        "name": baked_goods_obj.bakery.name,
        "created_at": baked_goods_obj.bakery.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": baked_goods_obj.bakery.updated_at.strftime("%Y-%m-%d %H:%M:%S") if baked_goods_obj.bakery.updated_at else None
    }

    baked_goods_dict = {
        "name": baked_goods_obj.name,
        "price": baked_goods_obj.price,
        "bakery": bakery_dict
    }

    response = make_response(
        jsonify(baked_goods_dict),
        200
    )

    return response

if __name__ == '__main__':
    app.run(port=5551, debug=True)
