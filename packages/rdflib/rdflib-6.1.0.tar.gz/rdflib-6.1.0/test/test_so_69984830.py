import rdflib
from rdflib.plugins import sparql

g = rdflib.Graph()
g.parse("family.ttl")

q = sparql.prepareQuery(
    """SELECT ?child ?sister WHERE {
              ?child fam:hasParent ?parent .
              ?parent fam:hasSister ?sister .
   }""",
   initNs={"fam": "http://example.org/family#"})

sm = rdflib.URIRef("http://example.org/royal#SverreMagnus")

for row in g.query(q, initBindings={'child': sm}):
    print(row)
