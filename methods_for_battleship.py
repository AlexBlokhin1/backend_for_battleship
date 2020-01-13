from flask import request, make_response
import uuid

from logging import getLogger
_logger = getLogger(__name__)

PLAYERS = {}
GAME_LOBBIES = {}
opposite_player_move = {}
# make cookies for every user
waiting_pair = {}


true_false_list = [True, False]


def find_players():
    # todo please shortly describe algorithm of this function HERE
    """
    THIS IS FUNCTION FOR FINDING PLAYERS

    STEP 1 - CHECK IF PLAYER HAVE OUR COOKIE
        if player has a cookie he is in waiting pair OR playing.
    STEP 2 - IF HE HAS A COOKIE AND WAITING FOR THE GAME
        player will wait until another player would come.
    STEP 3 - HE IS IN THE GAME AND PLAYING
        they should exchange shot coordinates but i cannot have them.

    PROBLEMS: PLAYERS CAN FIND EACH OTHER BUT CANNOT GIVE COORDINATES OF THE SHOT
    DONT KNOW HOW TO SOLVE THIS.
    """

    request_dict = request.json or {}
    cookie = request.cookies

    print("1REQUEST:  {}".format(request_dict))

    if cookie.get('game_lobby_uuid') in GAME_LOBBIES:
        player_name = request_dict['name']
        game_lobby_uuid = cookie.get('game_lobby_uuid')
        player_uuid = PLAYERS.get(player_name)

        waiting_pair[player_uuid] = request_dict
        GAME_LOBBIES[game_lobby_uuid] = waiting_pair
        game_lobby_pair = GAME_LOBBIES.get(game_lobby_uuid)

        if request_dict['status'] == 'RUN':
            if player_uuid == list(game_lobby_pair.keys())[0]:
                opposite_player = list(game_lobby_pair.values())[1]
            else:
                opposite_player = list(game_lobby_pair.values())[0]

            resp = make_response(opposite_player, 200)
            print("2RESPONSE:  {}".format(opposite_player))
            return resp

        if len(game_lobby_pair) == 2:
            opposite_player = game_lobby_pair.get(player_uuid)
            if opposite_player == list(game_lobby_pair.values())[0]:
                opposite_player = list(game_lobby_pair.values())[1]
            else:
                opposite_player = list(game_lobby_pair.values())[0]

            opposite_player['status'] = 'START'
            last_element = true_false_list.pop()
            if len(request_dict['move_turn']) == 0:
                opposite_player['move_turn'] = last_element
                del last_element
            else:
                opposite_player['move_turn'] = request_dict['move_turn']

            resp = make_response(opposite_player, 200)
            return resp

        else:
            request_dict['status'] = ''
            resp = make_response(request_dict, 200)
            return resp

    else:
        player_uuid = str(uuid.uuid4())
        request_dict['status'] = ''
        lobby_pair_key = str(uuid.uuid4())
        resp = make_response(request_dict, 200)
        resp.set_cookie('game_lobby_uuid', lobby_pair_key, max_age=60 * 60 * 60)

        name = request_dict['name']
        PLAYERS[name] = player_uuid
        waiting_pair[player_uuid] = request_dict
        GAME_LOBBIES[lobby_pair_key] = waiting_pair

        return resp
