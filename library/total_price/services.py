from library.extension import db
from library.library_ma import Total_priceSchema
from library.model import Total_price
from flask import request, jsonify, json

total_schema = Total_priceSchema()
totals_schema = Total_priceSchema(many=True)


def add_total_data_service():
    data = request.json
    if (('chessBoard' in data) and ('turn' in data) and ('codeGame' in data) and ('player1' in data) and ('player2' in data) and ('winner' in data)):
        chessBoard = data['chessBoard']
        turn = data['turn']
        codeGame = data['codeGame']
        player1 = data['player1']
        player2 = data['player2']
        winner = data['winner']
        try:
            new_total_data = Total_price(
                chessBoard, turn, codeGame, player1, player2, winner)
            db.session.add(new_total_data)
            db.session.commit()
            return jsonify({"message": f"Add success! with Id = {new_total_data.id}", "idRoom": new_total_data.id}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot add data", "error": str(e)}), 400
    else:
        return jsonify({"message": "Request error"}), 400


def get_all_total_data_service():
    totals_data = Total_price.query.all()
    if totals_data:
        return totals_schema.jsonify(totals_data)
    else:
        return jsonify({"message": "Not found sensors_data!"})


def get_by_id_service(id):
    price = Total_price.query.get(id)
    if price:
        return total_schema.jsonify(price)
    else:
        return jsonify({"message": "Not found price!"}), 404


def update_total_data_by_id_service(id):
    price = Total_price.query.get(id)
    if price:
        data = request.json
        if (data and ('chessBoard' in data) and ('turn' in data) and ('codeGame' in data) and ('player1' in data) and ('player2' in data) and ('winner' in data)):
            try:
                price.chessBoard = data['chessBoard']
                price.turn = data['turn']
                price.codeGame = data['codeGame']
                price.player1 = data['player1']
                price.player2 = data['player2']
                price.winner = data['winner']
                db.session.commit()
                return jsonify({"message": "Price updated successfully"})
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Cannot update price!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Not found price!"}), 404


def delete_total_data_by_id_service(id):
    price = Total_price.query.get(id)
    if price:
        try:
            db.session.delete(price)
            db.session.commit()
            return jsonify({"message": "Price deleted successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot delete price!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Not found price!"}), 404
