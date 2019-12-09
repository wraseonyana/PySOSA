import unittest
import pyobs
import rdflib



class MyTestCase(unittest.TestCase):

    def test_add_sensor(self):
        obs = pyobs.ObservationCollection(comment="myCol")
        this_graph = pyobs.get_graph()
        print(this_graph.serialize(format='turtle'))




if __name__ == '__main__':
    unittest.main()
