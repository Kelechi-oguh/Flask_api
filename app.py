from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Init app
app = Flask(__name__)
api = Api(app)

basedir =os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init db
db = SQLAlchemy(app)

# Init ma
ma = Marshmallow(app)


# Student Record Database
class Student_Data(db.Model):
    Name = db.Column(db.String(100), unique=True)
    Matric_No = db.Column(db.Unicode, unique=True, primary_key=True)
    Gender = db.Column(db.String(1))
    Programme =db.Column(db.String(50))
    Level = db.Column(db.Integer)

    def __init__(self, Name, Matric_No, Gender, Programme, Level):
        self.Name = Name
        self.Matric_No = Matric_No
        self.Gender = Gender
        self.Programme = Programme
        self.Level = Level
    
# Student Schema
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('Name', 'Matric_No', 'Gender', 'Programme', 'Level')

# Init Student Schema
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

#ENDPOINTS
class Home(Resource):
    def get(self): 
        return jsonify({'Homepage': 'This is the Homepage '})


class Student_Record(Resource):
    # Get all students record
    def get(self):
        all_students = Student_Data.query.all()
        result = students_schema.dump(all_students)
        return jsonify(result)
            
    # Create new student record
    def post(self):
        Name = request.json['Name']
        Matric_No = request.json['Matric_No']
        Gender = request.json['Gender']
        Programme = request.json['Programme']
        Level = request.json['Level']

        new_student = Student_Data(Name, Matric_No, Gender, Programme, Level)

        db.session.add(new_student)
        db.session.commit()
        return student_schema.jsonify(new_student)

class One_student_record(Resource):
    # Get a students record using Matric_No
    def get(self, Matric_No):
        student = Student_Data.query.get(Matric_No)
        return student_schema.jsonify(student)

    # Update student record
    def put(self, Matric_No):
        update_student = Student_Data.query.get(Matric_No)

        Name = request.json['Name']
        Matric_No = request.json['Matric_No']
        Gender = request.json['Gender']
        Programme = request.json['Programme']
        Level = request.json['Level']

        update_student.Name = Name
        update_student.Matric_No = Matric_No
        update_student.Gender = Gender
        update_student.Programme = Programme
        update_student.Level = Level

        db.session.commit()
        return student_schema.jsonify(update_student)

    # Delete Student Record
    def delete(self, Matric_No):
        delete_student = Student_Data.query.get(Matric_No)
    
        db.session.delete(delete_student)
        db.session.commit()

        return "DELETED RECORD: {}".format(Matric_No)
  

api.add_resource(Home, '/')
api.add_resource(Student_Record, '/students')
api.add_resource(One_student_record, '/students/<Matric_No>')

if __name__ == "__main__":
    db.create_all()
    app.run(debug= True)