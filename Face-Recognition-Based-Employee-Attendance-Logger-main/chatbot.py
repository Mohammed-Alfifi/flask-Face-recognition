# -*- coding: utf-8 -*-

# chatbot.py

from flask import request, render_template
import json

def setup_routes(app):

    bot_responses = {}

    @app.route('/get')
    def get_bot_response():
        userText = request.args.get('msg')
        bot_response = bot_responses.get(userText, "اعتذر لم استطع فهمك :(")
        return bot_response

    @app.route('/helpBot')
    def helpBot():
        global bot_responses
        with open('static/help.json', encoding='utf-8') as f:
            bot_responses = json.load(f)
        return render_template('chatBot.html', keys=[*bot_responses])