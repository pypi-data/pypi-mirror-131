import unittest

from rdflib import Graph, RDF, RDFS, __version__
import rdflib_shim
# Make sure the import doesn't get removed in a cleanup
shim_in = rdflib_shim.RDFLIB_SHIM

expected = """@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

rdfs:Resource a rdfs:Resource ."""


class SerializeTestCase(unittest.TestCase):
    def test_as_str(self):
        """ Make sure decode works either way """
        g = Graph()
        g.add( (RDFS.Resource, RDF.type, RDFS.Resource))
        self.assertEqual(expected, g.serialize(format="n3").strip())
        self.assertEqual(expected, g.serialize(format="n3").decode().strip())

    def test_fancy_decode(self):
        """ Make sure that parameterized decodes are caught if we are using 6"""
        if __version__.startswith("6."):
            g = Graph()
            g.add( (RDFS.Resource, RDF.type, RDFS.Resource))
            with self.assertRaises(TypeError) as e:
                g.serialize(format="n3").decode("UTF-16")
            self.assertIn("decode() takes 1 positional argument but 2 were given", str(e.exception))


if __name__ == '__main__':
    unittest.main()
