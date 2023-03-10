from flask import Flask, Response, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
import json
from jsonschema import validate, ValidationError
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tic_tac_toe.db'
db = SQLAlchemy(app)
api = Api(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.String(5), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "result": self.result,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time)
        }
    
    @staticmethod
    def json_schema():
        schema = {
            "type": "object",
            "required": ["result"]
        }
        props = schema["properties"] = {}
        props["result"] = {"type": "string", "enum": ["O", "X" "DRAW"]}
        props["start_time"] = {"type": "string"}
        props["end_time"] = {"type": "string"}

        return schema

class GameHistoryCollection(Resource):
    def get(self):
        print("get")
        games = Game.query.all()
        games_json = []
        for game in games:
            games_json.append(game.serialize())
        return Response(json.dumps(games_json), 200)
    
    def post(self):
        try:
            request_dict = json.loads(request.data)
        except:
            return Response(status = 415)
        
        try:
            validate(request_dict, Game.json_schema())
        except ValidationError:
            return Response(status = 415)
        
        game = Game(result = request_dict["result"],
                    start_time = datetime.now(),
                    end_time = datetime.now())

        db.session.add(game)
        db.session.commit()

        return Response(status = 201)

api.add_resource(GameHistoryCollection, "/api/game_history/")

with app.app_context():
    db.create_all()
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
