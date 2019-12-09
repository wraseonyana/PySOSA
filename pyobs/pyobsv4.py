# -*- coding: utf-8 -*-
"""Python module for instantiating and serializing W3C/OGC SSN-EXT Observation Collection.

This module provides utility class objects for maintaining a Observation Collection and the ability to serialize the collections as JSON-LD.

Todo:
    * Add configuration for sensors.
    * Additional Organizational Information

"""

from datetime import datetime

from rdflib import Graph, BNode, Literal, Namespace, RDF, RDFS

# Contexts for SOSA, SSN-EXT, SOSA
#  SOSA https://github.com/opengeospatial/ELFIE/blob/master/docs/json-ld/sosa.jsonld
#  Timeseries ML  https://github.com/opengeospatial/ELFIE/blob/master/docs/json-ld/tsml.jsonld
#  SSN-EXT https://github.com/opengeospatial/SELFIE/blob/master/docs/contexts/ssn-ext.jsonld
#  QUDT https://github.com/opengeospatial/SELFIE/blob/master/docs/contexts/qudt.jsonld
# datetime.datetime.now(pytz.timezone('Europe/Paris')).isoformat()
# UUID str(uuid.uuid4())
# https://github.com/w3c/sdw/blob/gh-pages/proposals/ssn-extensions/rdf/ssn-ext.jsonld 

# For images that are observations IIF 
# https://github.com/zimeon/iiif-ld-demo


context = {
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "ssn-ext-examples": "http://example.org/ssn-ext-examples#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "dcterms": "http://purl.org/dc/terms/",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "time": "http://www.w3.org/2006/time#",
    "ssn-ext": "http://www.w3.org/ns/ssn/ext/",
    "sosa": "http://www.w3.org/ns/sosa/",
    "qudt": "http://qudt.org/1.1/schema/qudt#",
    "prov": "http://www.w3.org/ns/prov#",

    "hasUltimateFeatureOfInterest": {
        "@id": "http://www.w3.org/ns/ssn/ext/hasUltimateFeatureOfInterest",
        "@type": "@id"
    },
    "usedProcedure": {
        "@id": "http://www.w3.org/ns/sosa/usedProcedure",
        "@type": "@id"
    },
    "phenomenonTime": {
        "@id": "http://www.w3.org/ns/sosa/phenomenonTime",
        "@type": "@id"
    },
    "observedProperty": {
        "@id": "http://www.w3.org/ns/sosa/observedProperty",
        "@type": "@id"
    },
    "madeBySensor": {
        "@id": "http://www.w3.org/ns/sosa/madeBySensor",
        "@type": "@id"
    },
    "hasFeatureOfInterest": {
        "@id": "http://www.w3.org/ns/sosa/hasFeatureOfInterest",
        "@type": "@id"
    },
    "hasMember": {
        "@id": "http://www.w3.org/ns/ssn/ext/hasMember",
        "@type": "@id"
    },
    "inXSDDateTime": {
        "@id": "http://www.w3.org/2006/time#inXSDDateTime",
        "@type": "http://www.w3.org/2001/XMLSchema#dateTime"
    },
    "hasBeginning": {
        "@id": "http://www.w3.org/2006/time#hasBeginning",
        "@type": "@id"
    },
    "isSampleOf": {
        "@id": "http://www.w3.org/ns/sosa/isSampleOf",
        "@type": "@id"
    },
    "hasResult": {
        "@id": "http://www.w3.org/ns/sosa/hasResult",
        "@type": "@id"
    },
    "imports": {
        "@id": "http://www.w3.org/2002/07/owl#imports",
        "@type": "@id"
    },
    "comment": {
        "@id": "http://www.w3.org/2000/01/rdf-schema#comment"
    },
    "creator": {
        "@id": "http://purl.org/dc/terms/creator",
        "@type": "@id"
    },
    "created": {
        "@id": "http://purl.org/dc/terms/created",
        "@type": "http://www.w3.org/2001/XMLSchema#date"
    },
    "resultTime": {
        "@id": "http://www.w3.org/ns/sosa/resultTime",
        "@type": "http://www.w3.org/2001/XMLSchema#dateTime"
    },

    "ObservationCollection": "ssn-ext:ObservationCollection",
    "hasMember": "ssn-ext:hasMember",
    "isMemberOf": "ssn-ext:isMemberOf",
    "Observation": "sosa:Observation",
    "Sample": "sosa:Sample",
    "observedProperty": "sosa:observedProperty",
    "hasBeginning": "time:hasBeginning",
    "hasEnd": "time:hasEnd",
    "hasGeometry": "gsp:hasGeometry",
    "isSampleOf": "sosa:isSampleOf",
    "isFeatureOfInterestOf": "sosa:isFeatureOfInterestOf",
    "relatedSample": "sampling:relatedSample",
    "quantityValue": "http://qudt.org/schema/qudt#quantityValue",
    "numericValue": "http://qudt.org/schema/qudt#numericValue",
    "unit": "http://qudt.org/schema/qudt#unit"
}

# Add Graph obj
obsgraph = Graph()

# Add namespaces
ssnext = Namespace("http://www.w3.org/ns/ssn/ext/")
sosa = Namespace("http://www.w3.org/ns/sosa/")
prov = Namespace("http://www.w3.org/ns/prov#")
qudt = Namespace("http://qudt.org/1.1/schema/qudt#")
owltime = Namespace("ttp://www.w3.org/2006/time#")
owl = Namespace("http://www.w3.org/2002/07/owl#")
rdf = Namespace("http://purl.org/dc/terms/")
rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
ssn = Namespace("http://www.w3.org/ns/ssn/")


def get_graph():
    return obsgraph


class platform(object):
    """
    Creates a Platform object that represents a SOSA Platform
"""
    # Maybe remove list if makes object too big/not needed, or might want a func that returns this list
    sensors = []
    actuators = []
    samplers = []


    def __init__(self, comment, label):
        self.platform_id = BNode()
        self.label = Literal(label)
        self.comment = Literal(comment)
        obsgraph.add((self.platform_id, RDF.type, sosa.Platform))
        obsgraph.add((self.platform_id, RDFS.comment, self.comment))
        obsgraph.add((self.platform_id, RDFS.label, self.label))

    def add_sensor(self, Sensor):
        if(isinstance(self, Sensor)):
            sen_uri = Sensor.get_uri()
            self.sensors.append(sen_uri)
            obsgraph.add((self.platform_id, sosa.hosts, sen_uri))
            Sensor.add_platform_id(self.platform_id)
        else:
            raise Exception('Object is not of type Sensor')



    def add_actuator(self, Actuator):
        if(isinstance(self,Actuator)):
            a_uri = Actuator.get_uri()
            self.actuators.append(a_uri)
            obsgraph.add((self.platform_id, sosa.hosts, a_uri))
            Actuator.add_platform_id(self.platform_id)
        else:
            raise Exception('Object is not of type Actuator')

    def add_sampler(self, Sampler):
        if(isinstance(self, Sampler)):
            s_uri = Sampler.get_uri()
            self.samplers.append(s_uri)
            obsgraph.add((self.platform_id, sosa.hosts, s_uri))
            Sampler.add_platform_id(self.platform_id)
        else:
            raise Exception('Object is not of type Sampler')

    def remove_sensor(self, Sensor):
        sen_uri = Sensor.get_uri()
        self.sensors.remove(sen_uri)
        obsgraph.remove((self.platform_id, sosa.hosts, sen_uri))
        Sensor.add_platform_id(self.platform_id)

    def remove_actuator(self, Actuator):
        a_uri = Actuator.get_uri()
        self.actuators.remove(a_uri)
        obsgraph.remove((self.platform_id, sosa.hosts, a_uri))
        Actuator.add_platform_id(self.platform_id)

    def remove_sampler(self, Sampler):
        s_uri = Sampler.get_uri()
        self.samplers.remove(s_uri)
        obsgraph.remove((self.platform_id, sosa.hosts, s_uri))
        Sampler.add_platform_id(self.platform_id)

class Actuator(object):
    """
    Creates a System object that represents a SOSA System
    """
    actuations = []

    def __init__(self, comment, label):
        self.actuator_id = BNode()
        self.platform_id = BNode()
        self.label = Literal(label)
        self.comment = Literal(comment)
        self.actuableProperty = ActuableProperty(object)
        self.implementsProcedure = Procedure(object)

        obsgraph.add((self.actuator_id, RDF.type, sosa.System))  # should we use sosa.system or ssn.system?
        obsgraph.add((self.actuator_id, RDFS.comment, self.comment))
        obsgraph.add((self.actuator_id, RDFS.label, self.label))

    def set_actuator_id(self, actuator_id):
        self.actuator_id = actuator_id
        obsgraph.add(self.actuator_id)

    def set_platform_id(self, platform_id):
        self.platform_id = platform_id
        assert isinstance(self.platform_id, self)
        obsgraph.add(self.platform_id)


class Procedure(object):
    """
    Creates a Procedure object that represents a SOSA System
    """

    def __init__(self, comment, label):
        self.procedure_id = BNode()
        self.label = Literal(label)
        self.comment = Literal(comment)
        self.input = Literal("")
        self.output = Literal("")

        obsgraph.add((self.procedure_id, RDF.type, sosa.Procedure))  # should we use sosa.system or ssn.system?
        obsgraph.add((self.procedure_id, RDFS.comment, self.comment))
        obsgraph.add((self.procedure_id, RDFS.label, self.label))

    def set_procedure_id(self, procedure_id):
        self.procedure_id = procedure_id
        obsgraph.add(self.procedure_id, RDF.type, sosa.Procedure)

class Actuation(object):
    """
    Creates an Actuation object that represents a SOSA System
    """

    def __init__(self, comment, label):
        self.label = Literal(label)
        self.comment = Literal(comment)
        self.dateTime = datetime
        self.featureOfInterest = FeatureOfInterest()
        self.simpleResult = Literal('')


class ActuableProperty(object):
    """
    Creates an ActuableProperty object that represents a SOSA System
    """

    def __init__(self, comment, label):
        self.actuable_property_id = BNode()
        self.label = Literal(label)
        self.comment = Literal(comment)
        self.property = Literal('')


class FeatureOfInterest(object):
    """
    Creates a FeatureOfInterest object that represents a SOSA System
    """

    def __init__(self, comment, label):
        self.feature_of_interest_id = BNode()
        self.label = Literal(label)
        self.comment = Literal(comment)


class Sampler(object):
    """
     Feature which is intended to be representative of a FeatureOfInterest on which Observations were made
    """
    samplings = []

    def __init__(self, comment, label):
        self.sampler_id = BNode()
        self.platform_id = BNode()
        self.label = Literal(label)
        self.comment = Literal(comment)
        self.implementsProcedure = Procedure(object)


        obsgraph.add((self.sampler_id, RDF.type, sosa.Sampler))
        obsgraph.add((self.sampler_id_id, RDFS.comment, self.comment))
        obsgraph.add((self.sampler_id, RDFS.label, self.label))

    def set_sampler_id(self, sampler_id):
        self.sampler_id = sampler_id
        obsgraph.add(self.sampler_id, RDF.type, sosa.Sampler)

    def set_platform_id(self, platform_id):
        self.platform_id = platform_id
        obsgraph.add(self.platform_id, RDF.type, sosa.Platform)

    def add_samplings(self, Sampling):
        if (isinstance(self, Sampling)):
            s_uri = Sampling.get_uri()
            self.samplings.append(s_uri)
            obsgraph.add((self.sampler_id, sosa.hosts, s_uri))

        else:
            raise Exception('Object is not of type Sampling')


class Sampling(object):
    """
    Creates an Actuation object that represents a SOSA System
    """

    def __init__(self, comment, label):
        self.sampling_id = BNode()
        self.label = Literal(label)
        self.comment = Literal(comment)
        self.dateTime = datetime
        self.featureOfInterest = FeatureOfInterest()
        self.simpleResult = Literal('')









class ObservationCollection(object):
    """ Create SSN-EXT Observation Collection """

    def __init__(self, comment):
        self.jsonld = {
            "@type": "ssn-ext:ObservationCollection",
            "hasFeatureOfInterest": "http://example.org/Sample_2",
            "madeBySensor": "http://example.org/s4",
            "observedProperty": "http://example.org/op2",
            "phenomenonTime": "_:b13",
            "usedProcedure": "http://example.org/p3",
            "hasMember": ["http://example.org/O5", "http://example.org/O4"]
        }
        self.obscollid = BNode()
        self.comment = Literal(comment)
        obsgraph.add((self.obscollid, RDF.type, ssnext.ObservationCollection))
        obsgraph.add((self.obscollid, RDFS.comment, self.comment))

    def addObservation(self, sensorURI, FeatureURI, result):
        obsid = BNode()
        resultTime = datetime.now(tz=None)
        resultTimeLiteral = Literal(resultTime)
        resultLiteral = Literal(result)
        obsgraph.add((obsid, RDF.type, sosa.Observation))
        obsgraph.add((obsid, sosa.madeBySensor, sensorURI))
        obsgraph.add((self.obscollid, ssnext.hasMember, obsid))
        obsgraph.add((obsid, sosa.resultTime, resultTimeLiteral))
        obsgraph.add((obsid, sosa.hasSimpleResult, resultLiteral))


# str(uuid.uuid4())

class Observation(object):
    def __init__(self, comment, label):
        self.comment = Literal(comment)
        self.observation_id = BNode()
        # Fix Tomorrow
        # obsgraph.add((self.observation_id, sosa.madeBySensor, sensor_id))
        # obsgraph.add((self.platform_id, RDFS.comment, self.comment))
        # obsgraph.add((self.platform_id, RDFS.label, self.label))


class Sensor(object):
    def __init__(self, sensor_description, observable_property_uri):
        self.sensorid = BNode()
        self.sensor_description = Literal(sensor_description)
        obsgraph.add((self.sensorid, RDF.type, sosa.Sensor))
        obsgraph.add((self.sensorid, sosa.Observes, observable_property_uri))
        obsgraph.add((self.sensorid, RDFS.comment, self.sensor_description))

    def add_platform_id(self, platform_id):
        obsgraph.add((self.sensorid, sosa.isHostedBy, platform_id))

    def get_uri(self):
        return self.sensorid

    def add_obs_property(self, observable_property):
        obsgraph.add(self.sensorid, sosa.observes, observable_property)


# Class for managing observableproperties
# Preferably linked to envo, sweet and qudt
class ObservableProperty(object):
    """
    Creates a Observable Property object that represents a SOSA Observable Property

    """

    def __init__(self, property_uri):
        if property_uri:
            self.observable_property_uri = property_uri
        else:
            self.observable_property_uri = BNode()
        obsgraph.add((self.observable_property_uri, rdf.type, sosa.Observable_property))

    def get_uri(self):
        return self.observable_property_uri


class FeatureOfInterest(object):
    """   Creates a Feature of Interest object that represents a SOSA Feature of Interest """

    def __init__(self):
        self.uri = "_B0"
        pass


class UltimateFeatureOfInterest(FeatureOfInterest):
    def __init__(self):
        super(UltimateFeatureOfInterest, self).__init__()
