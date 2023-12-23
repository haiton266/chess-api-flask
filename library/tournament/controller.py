from flask import Blueprint
from .services import (add_round_service, get_all_rounds_service, get_round_by_id_service,
                       update_round_by_id_service, delete_round_by_id_service,
                       add_seed_service, get_all_seeds_service, get_seed_by_id_service,
                       update_seed_by_id_service, delete_seed_by_id_service,
                       add_team_service, get_all_teams_service, get_team_by_id_service,
                       update_team_by_id_service, delete_team_by_id_service, get_all_tournament_service, add_tournament_service)

tournament = Blueprint("tournament", __name__)


@tournament.route('/api/rounds', methods=['GET'])
def get_tournaments():
    return get_all_tournament_service()


@tournament.route('/tournament/add', methods=['POST'])
def add_tournament():
    return add_tournament_service()
# Round routes


@tournament.route("/round/add", methods=["POST"])
def add_round():
    return add_round_service()


@tournament.route("/round/all", methods=["GET"])
def get_all_rounds():
    return get_all_rounds_service()


@tournament.route("/round/<int:id>", methods=["GET"])
def get_round_by_id(id):
    return get_round_by_id_service(id)


@tournament.route("/round/<int:id>", methods=["PUT"])
def update_round_by_id(id):
    return update_round_by_id_service(id)


@tournament.route("/round/<int:id>", methods=["DELETE"])
def delete_round_by_id(id):
    return delete_round_by_id_service(id)

# Seed routes


@tournament.route("/seed/add", methods=["POST"])
def add_seed():
    return add_seed_service()


@tournament.route("/seed/all", methods=["GET"])
def get_all_seeds():
    return get_all_seeds_service()


@tournament.route("/seed/<int:id>", methods=["GET"])
def get_seed_by_id(id):
    return get_seed_by_id_service(id)


@tournament.route("/seed/<int:id>", methods=["PUT"])
def update_seed_by_id(id):
    return update_seed_by_id_service(id)


@tournament.route("/seed/<int:id>", methods=["DELETE"])
def delete_seed_by_id(id):
    return delete_seed_by_id_service(id)

# Team routes


@tournament.route("/team/add", methods=["POST"])
def add_team():
    return add_team_service()


@tournament.route("/team/all", methods=["GET"])
def get_all_teams():
    return get_all_teams_service()


@tournament.route("/team/<int:id>", methods=["GET"])
def get_team_by_id(id):
    return get_team_by_id_service(id)


@tournament.route("/team/<int:id>", methods=["PUT"])
def update_team_by_id(id):
    return update_team_by_id_service(id)


@tournament.route("/team/<int:id>", methods=["DELETE"])
def delete_team_by_id(id):
    return delete_team_by_id_service(id)
