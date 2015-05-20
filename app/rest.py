from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from models import Sensor, Medicion


#sensores = Sensor.query.all()

class SensorAPI(Resource):
#    decorators = [auth.login_required]

    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('id', type=int, location='json')
        self.reqparse.add_argument('ubicacion', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        
        super(SensorAPI, self).__init__()

    def get(self, id):
        sensor = Sensor.query.get(id)
        args = self.reqparse.parse_args()
        for r in args:
        	print r

        return {'sensor': sensor.nombre , 'ubicacion': sensor.ubicacion}

    def put(self, id):
        sensor = [sensor for sensor in sensors if sensor['id'] == id]
        if len(sensor) == 0:
            abort(404)
        sensor = sensor[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                sensor[k] = v
        return {'sensor': marshal(sensor, sensor_fields)}

    def delete(self, id):
        sensor = [sensor for sensor in sensors if sensor['id'] == id]
        if len(sensor) == 0:
            abort(404)
        sensors.remove(sensor[0])
        return {'result': True}


class MedicionAPI(Resource):
#    decorators = [auth.login_required]

    
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('sensor', type=int, location='json')
        self.reqparse.add_argument('valor', type=int, location='json')
        
        super(MedicionAPI, self).__init__()

    def get(self, id):
        sensor = Sensor.query.get(id)
        
        return {'sensor': sensor.nombre , 'ubicacion': sensor.ubicacion}

    def post(self, id):
    	from flask import request
        med = Medicion()
        args = self.reqparse.parse_args()
        for r in request.form:
        	print "asds: " , r
        sensorId = args["sensor"]
        valor = args["valor"]
        print "aqui:  ",  sensorId , valor
        r = med.add(sensorId,valor)

        return {'medicion': r.id}





if __name__ == '__main__':
	from flask import Flask, jsonify, abort, make_response
	app.run(debug=True)
