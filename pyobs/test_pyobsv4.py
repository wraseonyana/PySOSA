import unittest
import pyobs
import rdflib
from . import pyobsv4


from rdflib import Graph
from rdflib import Namespace
from rdflib import RDF



class MyTestCase(unittest.TestCase):

    def test_add_sensor(self):
        obs = pyobs.ObservationCollection(comment="myCol")
        this_graph = pyobs.get_graph()
        print(this_graph.serialize(format='turtle'))



    def add_sensor_test(self):
        g = Graph()



        p1 = pyobsv4.Platform(comment="Platform1", label="P1")
        s1 = pyobsv4.Sensor("Sensor1","P1","1","1","air speed","guided")
        s2 = pyobsv4.Sensor("Sensor2", "P1", "2", "1", "longitude", "guided")
        s3 = pyobsv4.Sensor("Sensor3", "P1", "3", "1", "altitude", "guided")
        p1.add_sensor(s1)
        p1.add_sensor(s2)
        p1.add_sensor(s3)

        g = pyobs.get_graph()
        print(g.serialize(format='turtle'))

 




if __name__ == '__main__':
    unittest.main()
