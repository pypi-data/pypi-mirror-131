import unittest

from rdflib import Graph, RDFS, RDF

turtle_source = """@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

rdfs:Resource a rdfs:Resource ."""


class JSONLDTestCase(unittest.TestCase):
    def test_jsonld(self):
        """ Make sure that jsonld parsing works """
        g = Graph()
        g.parse(data=turtle_source, format="turtle")
        self.assertEqual(turtle_source, g.serialize(format="turtle").strip())


if __name__ == '__main__':
    unittest.main()
