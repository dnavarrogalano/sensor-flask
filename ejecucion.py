__author__ = 'DNG'
from app import models, db




from app import app, db
from app.models import Medicion
from datetime import datetime, timedelta
import random

def generarMediciones(x):
	i = 1
	a = datetime.utcnow() 
	s = db.session()
	v = random.randint(10, 20)
	while i < 199:
		m = models.Medicion()
		i=i+1
		m.sensor = x
		m.timestamp = a + timedelta(seconds=i*30)
		v =random.randint(v-3, v+2)
		if v <= 1:
			v = 1
		m.valor = v
		s.add(m)
	s.commit()

if __name__ == "__main__":
	print 'OK'
	generarMediciones(2)    



