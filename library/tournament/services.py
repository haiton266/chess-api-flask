from flask import request, jsonify
from library.model import Round, Seed, Team
from library.extension import db
from library.library_ma import Total_priceSchema
from library.model import Total_price
import math
# total_schema = Total_priceSchema()

# Round Services


def add_round_service():
    data = request.json
    try:
        new_round = Round(title=data['title'])
        db.session.add(new_round)
        db.session.commit()
        return jsonify({'message': 'Round added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


def get_all_rounds_service():
    rounds = Round.query.all()
    return jsonify([{'id': round.id, 'title': round.title} for round in rounds])


def get_round_by_id_service(id):
    round = Round.query.get(id)
    if round:
        return jsonify({'id': round.id, 'title': round.title})
    else:
        return jsonify({'message': 'Round not found'}), 404


def update_round_by_id_service(id):
    round = Round.query.get(id)
    data = request.json
    if round:
        try:
            round.title = data['title']
            db.session.commit()
            return jsonify({'message': 'Round updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Round not found'}), 404


def delete_round_by_id_service(id):
    round = Round.query.get(id)
    if round:
        try:
            db.session.delete(round)
            db.session.commit()
            return jsonify({'message': 'Round deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Round not found'}), 404

# Seed Services


def add_seed_service():
    data = request.json
    try:
        new_seed = Seed(
            round_id=data['round_id'], matchID=data['matchID'], result=data['result'])
        db.session.add(new_seed)
        db.session.commit()
        return jsonify({'message': 'Seed added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


def get_all_seeds_service():
    seeds = Seed.query.all()
    return jsonify([{'id': seed.id, 'matchID': seed.matchID, 'result': seed.result} for seed in seeds])


def get_seed_by_id_service(id):
    seed = Seed.query.get(id)
    if seed:
        return jsonify({'id': seed.id, 'matchID': seed.matchID, 'result': seed.result})
    else:
        return jsonify({'message': 'Seed not found'}), 404


def update_seed_by_id_service(id):
    seed = Seed.query.get(id)
    data = request.json
    if seed:
        try:
            seed.matchID = data['matchID']
            seed.result = data['result']
            db.session.commit()
            return jsonify({'message': 'Seed updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Seed not found'}), 404


def delete_seed_by_id_service(id):
    seed = Seed.query.get(id)
    if seed:
        try:
            db.session.delete(seed)
            db.session.commit()
            return jsonify({'message': 'Seed deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Seed not found'}), 404

# Team Services


def add_team_service():
    data = request.json
    try:
        new_team = Team(seed_id=data['seed_id'], name=data['name'])
        db.session.add(new_team)
        db.session.commit()
        return jsonify({'message': 'Team added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400


def get_all_teams_service():
    teams = Team.query.all()
    return jsonify([{'id': team.id, 'name': team.name} for team in teams])


def get_team_by_id_service(id):
    team = Team.query.get(id)
    if team:
        return jsonify({'id': team.id, 'name': team.name})
    else:
        return jsonify({'message': 'Team not found'}), 404


def update_team_by_id_service(id):
    team = Team.query.get(id)
    data = request.json
    if team:
        try:
            team.name = data['name']
            db.session.commit()
            return jsonify({'message': 'Team updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Team not found'}), 404


def delete_team_by_id_service(id):
    team = Team.query.get(id)
    if team:
        try:
            db.session.delete(team)
            db.session.commit()
            return jsonify({'message': 'Team deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 400
    else:
        return jsonify({'message': 'Team not found'}), 404
# ---


def get_all_tournament_service():
    rounds_data = Round.query.all()
    result = []

    for round in rounds_data:
        round_info = {
            "title": round.title,
            "seeds": [
                {
                    "id": seed.id,
                    "teams": [{"name": team.name} for team in seed.teams],
                    "result": seed.result,
                    "matchID": seed.matchID
                } for seed in round.seeds
            ]
        }
        result.append(round_info)

    return jsonify(result)


def add_tournament_service():
    data = request.json
    try:
        # Clear all data in Round, Seed, Team
        Team.query.delete()
        Seed.query.delete()
        Round.query.delete()
        db.session.commit()
        # Get data from request
        numberPlayer = data['numberPlayer']
        # Clear space, Iterate string to get name of player by comma
        namePlayer = data['namePlayer'].replace(" ", "").split(",")
        # Add new data
        numberRound = int(math.log2(numberPlayer))
        numberMatch = 2 ** numberRound - 1
        print("numberPlayer", numberPlayer)
        print("numberRound", numberRound)
        print("numberMatch", numberMatch)

        # Create new round
        # Khởi tạo một dictionary để lưu các id của Round
        round_ids = {}

        for i in range(1, numberRound + 1):
            new_round = Round(title="Round " + str(i))
            db.session.add(new_round)
            # Lưu thay đổi để có id cho new_round
            db.session.commit()
            # Lưu id của new_round vào dictionary với key là số thứ tự của vòng
            round_ids[i] = new_round.id

        # Create new seed
        seed_ids = []
        temp = numberPlayer // 2
        for i in range(1, numberRound + 1):
            for j in range(1, temp + 1):
                newMatch = Total_price(chessBoard="R2N2B2Q2K2B2N2R2P2P2P2P2P2P2P2P20000000000000000000000000000000000000000000000000000000000000000P1P1P1P1P1P1P1P1R1N1B1Q1K1B1N1R1",
                                       turn=1, codeGame="1", player1="player1", player2="player2", winner="0", time_player1=0, time_player2=0)
                db.session.add(newMatch)
                db.session.commit()
                match_ids = newMatch.id
                numberOfMatchInDb = Total_price.query.count()
                new_seed = Seed(round_id=round_ids[i], matchID=match_ids,
                                result="happening")  # Cần sửa matchID
                db.session.add(new_seed)
                db.session.commit()
                seed_ids.append(new_seed.id)
            temp = temp // 2
        # Create new team
        for i in range(0, numberPlayer):
            new_team = Team(seed_id=seed_ids[i//2], name=namePlayer[i])
            db.session.add(new_team)
            db.session.commit()
        num = 1
        for i in range(numberPlayer, numberMatch*2):
            new_team = Team(seed_id=seed_ids[i//2], name=f"Winner match {num}")
            num += 1
            db.session.add(new_team)
            db.session.commit()

        return jsonify({'message': 'Tournament added successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
