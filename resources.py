from flask_restful import Resource, reqparse
from models import db, Tutor, Pet
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

class TutorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Tutor

class PetSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pet

class TutorResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True)
        args = parser.parse_args()

        new_tutor = Tutor(nome=args['nome'])
        db.session.add(new_tutor)
        db.session.commit()

        return {'message': 'Tutor cadastrado com sucesso'}, 201

    def get(self):
        tutors = Tutor.query.all()
        tutor_schema = TutorSchema(many=True)
        return tutor_schema.dump(tutors)

class PetResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True)
        parser.add_argument('tutor_id', type=int, required=True)
        args = parser.parse_args()

        new_pet = Pet(nome=args['nome'], tutor_id=args['tutor_id'])
        db.session.add(new_pet)
        db.session.commit()

        return {'message': 'Pet cadastrado com sucesso'}, 201

    def get(self, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet:
            return {'message': 'Pet não encontrado'}, 404

        pet_schema = PetSchema()
        return pet_schema.dump(pet)

    def put(self, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet:
            return {'message': 'Pet não encontrado'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('nome', type=str, required=True)
        parser.add_argument('tutor_id', type=int, required=True)
        args = parser.parse_args()

        pet.nome = args['nome']
        pet.tutor_id = args['tutor_id']
        db.session.commit()

        return {'message': 'Pet atualizado com sucesso'}

    def delete(self, pet_id):
        pet = Pet.query.get(pet_id)
        if not pet:
            return {'message': 'Pet não encontrado'}, 404

        db.session.delete(pet)
        db.session.commit()

        return {'message': 'Pet excluído com sucesso'}
