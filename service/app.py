import logging

from flask import Flask, jsonify, render_template, request
from pydantic import BaseModel, ValidationError, field_validator


class Apartment(BaseModel):
    area: int
    num_rooms: int
    total_floors: int
    floor: int

    @field_validator('area', 'num_rooms', 'total_floors', 'floor', mode='after')
    @classmethod
    def is_positive(cls, value: int):
        if value < 1:
            raise ValueError("Must be more than 0")

        return value


app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/numbers', methods=['POST'])
def process_numbers():
    try:
        data = request.json
        apartment = Apartment.model_validate(data)
        logging.debug("numbers are valid")
        return jsonify({"message": "Данные валидны", "data": apartment.model_dump()})
    except ValidationError as e:
        logging.debug("numbers are invalid")
        return e.json(), 422, {'Content-Type': 'application/json'}

if __name__ == '__main__':
    app.run(debug=True)
