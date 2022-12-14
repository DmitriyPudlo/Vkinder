from VK import VK
from flask import Flask, jsonify, make_response, abort, request
import time
from db import Connector

app = Flask(__name__)


def prepare_info(candidate_id, response, photos_ids):
    first_name = response['first_name']
    last_name = response['last_name']
    photos_url = [f'https://vk.com/photo{candidate_id}_{photo_id}' for photo_id in photos_ids]
    info = {'first_name': first_name,
            'last_name': last_name,
            'url': f'https://vk.com/id{candidate_id}',
            'photos_url': photos_url}
    return info


def prepare_ids(favor_ids):
    favor_ids = [int(id_) for id_ in favor_ids.split(',')]
    return favor_ids


@app.route('/vkinder/user/search_candidate', methods=['GET'])
def get_candidate():
    user_id = request.args.get('user_id')
    token = request.args.get('token')
    count = request.args.get('count')
    if count:
        count = int(count)
    if not token or not user_id:
        abort(404)
    vk = VK(token)
    to_response = []
    candidates_ids = vk.search_candidate(user_id, count=count)
    for id_candidate in candidates_ids:
        photos_ids = vk.photos_ids(id_candidate)
        response = vk.show_candidate(id_candidate)
        time.sleep(0.5)
        candidates_info = prepare_info(id_candidate, response, photos_ids)
        to_response.append(candidates_info)
    return jsonify(to_response)


@app.route('/vkinder/user/favor', methods=['GET'])
def get_favor():
    user_id = request.args.get('user_id')
    token = request.args.get('token')
    if not token or not user_id:
        abort(404)
    vk = VK(token)
    connect = Connector()
    to_response = []
    candidates_ids = connect.show_candidates(user_id)
    for id_candidate in candidates_ids:
        photos_ids = connect.show_photo(id_candidate)
        response = vk.show_candidate(id_candidate)
        time.sleep(0.5)
        candidates_info = prepare_info(id_candidate, response, photos_ids)
        to_response.append(candidates_info)
    return jsonify(to_response)


@app.route('/vkinder/user/add_favor', methods=['POST'])
def add_favor():
    user_id = request.args.get('user_id')
    favor_ids = request.args.get('favor_ids')
    token = request.args.get('token')
    if not token or not user_id or not favor_ids:
        abort(404)
    favor_ids = prepare_ids(favor_ids)
    vk = VK(token)
    connect = Connector()
    to_response = []
    for favor_id in favor_ids:
        photo_ids = vk.photos_ids(favor_id)
        connect.add_candidate(user_id, favor_id, photo_ids)
        to_response.append([user_id, favor_id, photo_ids])
    return jsonify(to_response)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
