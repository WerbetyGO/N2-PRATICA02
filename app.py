from flask import Flask, jsonify
from flask_restful import Api
from models import db
from resources import TutorResource, PetResource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
db.init_app(app)
api = Api(app)

api.add_resource(TutorResource, '/tutor')
api.add_resource(PetResource, '/pet', '/pet/<int:pet_id>')

@app.route('/')
def index():
    return jsonify({'message': 'API de Cadastro de Tutores e Pets'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
