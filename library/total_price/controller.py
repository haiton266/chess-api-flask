from flask import Blueprint
from .services import (add_total_data_service, get_all_total_data_service,
                       update_total_data_by_id_service, delete_total_data_by_id_service, get_by_id_service, update_join_by_id_service, update_time)

totals_data = Blueprint("totals_data", __name__)


@totals_data.route("/total_data/update_time/<int:id>", methods=["POST"])
def update_time_id(id):
    return update_time(id)


@totals_data.route("/total_data/add", methods=["POST"])
def add_sensor_data():
    return add_total_data_service()


@totals_data.route("/total_data/all", methods=["GET"])
def get_all_sensors_data():
    return get_all_total_data_service()


@totals_data.route("/total_data/<int:id>/<int:p>", methods=["GET"])
def get_by_id_data(id, p):
    return get_by_id_service(id, p)


@totals_data.route("/total_data/update/<int:id>", methods=['PUT'])
def update_price_by_id(id):
    return update_total_data_by_id_service(id)


@totals_data.route("/total_data/update_join/<int:id>", methods=['PUT'])
def update_join_by_id(id):
    return update_join_by_id_service(id)


@totals_data.route("/total_data/delete/<int:id>", methods=['DELETE'])
def delete_book_by_id(id):
    return delete_total_data_by_id_service(id)
