import math
from library.model import Round, Seed, Team
import time
import chess
import chess.engine
import os

from flask_jwt_extended import create_access_token
from library.extension import db
from library.library_ma import Total_priceSchema
from library.model import Total_price
from library.model import Users
from flask import app, request, jsonify, json
from datetime import timedelta

total_schema = Total_priceSchema()
totals_schema = Total_priceSchema(many=True)
# --------------------
# @app.route('/update_time/<int:id>', methods=['POST'])

def update_time(id):
    game = Total_price.query.get(id)
    if game:
        data = request.json
        current_time = time.time()

        # Kiểm tra lượt đi hiện tại từ dữ liệu đầu vào và so sánh với trạng thái hiện tại của trò chơi
        if 'turn' in data:
            # Giả sử bạn lưu trữ lượt đi hiện tại trong thuộc tính 'turn' của đối tượng game
            current_turn = game.turn

            # Chỉ cập nhật thời gian cho người chơi đang có lượt
            if data['turn'] == current_turn:
                if current_turn == '1':
                    game.time_player1 = current_time if not game.time_player1 else game.time_player1
                elif current_turn == '2':
                    game.time_player2 = current_time if not game.time_player2 else game.time_player2
            else:
                return jsonify({"message": "Not player's turn"}), 400
        else:
            return jsonify({"message": "Turn information is missing"}), 400

        db.session.commit()

        # Trả về thời gian đã cập nhật
        return jsonify({
            "message": "Time updated successfully",
            "time_player1": game.time_player1,
            "time_player2": game.time_player2
        })
    else:
        return jsonify({"message": "Game not found"}), 404


def create_board_from_string(board_str):
    # Hàm này cần chuyển đổi chuỗi ký tự thành một bàn cờ mà thư viện chess có thể hiểu
    board = chess.Board()
    board.clear_board()
    for i in range(0, len(board_str), 2):
        piece_str = board_str[i]
        player = board_str[i + 1]
        if piece_str != '0':
            piece = create_piece(piece_str, player)
            square = chess.SQUARES[i // 2]
            board.set_piece_at(square, piece)
    return board


def create_piece(piece_str, player):
    piece_type = {
        'R': chess.ROOK,
        'N': chess.KNIGHT,
        'B': chess.BISHOP,
        'Q': chess.QUEEN,
        'K': chess.KING,
        'P': chess.PAWN
    }.get(piece_str, None)
    color = chess.WHITE if player == '2' else chess.BLACK
    return chess.Piece(piece_type, color) if piece_type is not None else None


def board_to_string(board):
    # Hàm này cần chuyển đổi bàn cờ thành chuỗi ký tự để lưu vào cơ sở dữ liệu
    board_str = ''
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_str = piece.symbol().upper(
            ) if piece.color == chess.WHITE else piece.symbol().upper()
            player = '2' if piece.color == chess.WHITE else '1'
        else:
            piece_str = '0'
            player = '0'
        board_str += piece_str + player
    return board_str

# --------------------


def add_total_data_service():
    data = request.json
    if (('chessBoard' in data) and ('turn' in data) and ('codeGame' in data) and ('player1' in data) and ('player2' in data) and ('winner' in data)):
        chessBoard = data['chessBoard']
        turn = data['turn']
        codeGame = data['codeGame']
        player1 = data['player1']
        player2 = data['player2']
        winner = data['winner']
        time_player1 = time.time()
        time_player2 = time.time()
        try:
            new_total_data = Total_price(
                chessBoard, turn, codeGame, player1, player2, winner, time_player1, time_player2)
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


def get_by_id_service(id, p):
    price = Total_price.query.get(id)
    if price:
        if p == 1:
            time_diff = time.time() - price.time_player1
            price.total_time1 = max(
                price.total_time1 - round(time_diff), 0)
        elif p == 2:
            time_diff = time.time() - price.time_player2
            price.total_time2 = max(
                price.total_time2 - round(time_diff), 0)
        print(price.total_time1)
        # Chuyển đổi price thành JSON
        data = total_schema.jsonify(price)
        return data
    else:
        return jsonify({"message": "Not found price!"}), 404


def update_total_data_by_id_service(id):
    price = Total_price.query.get(id)
    if price:
        data = request.json
        if (data and ('chessBoard' in data) and ('turn' in data) and ('winner' in data)):
            try:
                print(data['player2'])
                if data['winner'] == '0' and data['player2'] == 'AI' and 'player2' in data:
                    board = create_board_from_string(data['chessBoard'])
                    print(os.getcwd())
                    engine_path = "./library/total_price/stockfish/stockfish-windows-x86-64-modern.exe"

                    # Kiểm tra xem đường dẫn tới engine có tồn tại không
                    if os.path.exists(engine_path):
                        engine = chess.engine.SimpleEngine.popen_uci(
                            engine_path)
                        if engine:
                            print("Engine created")
                        else:
                            print("Engine not created")
                    else:
                        print("Engine path does not exist")
                    print(board.is_checkmate())
                    board.turn = chess.WHITE
                    if board.is_checkmate() == False:
                        result = engine.play(
                            board, chess.engine.Limit(time=0.1))
                        board.push(result.move)
                        price.chessBoard = board_to_string(board)
                        # Since AI move, turn is changed
                        price.turn = '2' if data['turn'] == '1' else '1'
                    else:
                        price.winner = 'AI'
                    db.session.commit()
                    engine.quit()
                else:
                    price.chessBoard = data['chessBoard']
                    price.turn = data['turn']
                    price.winner = data['winner']
                    if price.turn == 2:  # thằng 1 đi
                        # Giảm quỹ thời gian
                        price.total_time1 -= (time.time() - price.time_player1)
                    else:
                        price.total_time2 -= (time.time() - price.time_player2)
                    # Cập nhật mốc cho cả 2
                    price.time_player1 = time.time()
                    price.time_player2 = time.time()
                    db.session.commit()
                return jsonify({"message": "Price updated successfully"})
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Cannot update price!", "error": str(e)}), 400
        else:
            return jsonify({"message": "Invalid input data"}), 400
    else:
        return jsonify({"message": "Not found price!"}), 404


# OLD
# def update_total_data_by_id_service(id):
#     price = Total_price.query.get(id)
#     if price:
#         data = request.json
#         if (data and ('chessBoard' in data) and ('turn' in data) and ('winner' in data)):
#             try:
#                 price.chessBoard = data['chessBoard']
#                 price.turn = data['turn']
#                 price.winner = data['winner']
#                 db.session.commit()
#                 return jsonify({"message": "Price updated successfully"})
#             except Exception as e:
#                 db.session.rollback()
#                 return jsonify({"message": "Cannot update price!", "error": str(e)}), 400
#         else:
#             return jsonify({"message": "Invalid input data"}), 400
#     else:
#         return jsonify({"message": "Not found price!"}), 404


def update_join_by_id_service(id):
    price = Total_price.query.get(id)
    if price:
        data = request.json
        if (data and ('codeGame' in data) and ('player2' in data) and (price.codeGame == data['codeGame'])):
            try:
                price.player2 = data['player2']
                price.time_player1 = time.time()
                price.time_player2 = time.time()
                # price.codeGame = data['codeGame']
                db.session.commit()
                return jsonify({"message": "Price updated successfully"})
            except Exception as e:
                db.session.rollback()
                return jsonify({"message": "Cannot update price!", "error": str(e)}), 400
        else:
            return jsonify({"message": "Invalid input data or codeGame mismatch"}), 400
    else:
        return jsonify({"message": "Not found price!"}), 404


def delete_total_data_by_id_service(id):
    price = Total_price.query.get(id)
    if price:
        try:
            # Check if the game in seeds table then update the status
            seed = Seed.query.filter_by(matchID=price.id).first()
            if seed:
                # Tính hiệu của id vừa tìm thấy với id đầu tiên hiện có trong bảng
                id_diff = seed.id - Seed.query.first().id
                # Tính số lượng người chơi
                numOfPlayer = Seed.query.count() + 1
                updateSeedId = seed.id + id_diff // 2 + numOfPlayer // 2
                print("price.winner", price.winner)
                if price.winner == '1':
                    username = Team.query.filter_by(
                        seed_id=seed.id).first().name
                else:
                    # Lấy username của người chơi thắng để cập nhật vào bảng, đối tượng team nằm sau, .second()
                    username = Team.query.filter_by(
                        seed_id=seed.id)[1].name
                seed.result = username + " win"
                print("username", username)
                if id_diff % 2 == 0:
                    updateTeam = Team.query.filter_by(
                        seed_id=updateSeedId).first()
                    updateTeam.name = username
                else:
                    updateTeam = Team.query.filter_by(
                        seed_id=updateSeedId)[1]
                    updateTeam.name = username
                db.session.commit()
            db.session.delete(price)
            db.session.commit()
            return jsonify({"message": "Price deleted successfully"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"message": "Cannot delete price!", "error": str(e)}), 400
    else:
        return jsonify({"message": "Not found price!"}), 404
