# rdflib-shim
A compatibility adapter for rdflib version 6.0.

## Background
The rdflib 5.x to 6.x transition introduced a couple of breaking changes.  This shim
makes those changes transparent to the outside world.

### 1) Serialize().decode()
In rdflib 5.x, `Graph.serialize` returned a byte array. This was changed to a `str`
in rdflib 6.x, which breaks all the code written in the form:
   `g.serialize(format=...).decode()`

This shim decorates the return string from version 6 so that it has an identity `decode()` method

`rdflib_shim` adds a wrapper on the rdflib Graph.serialize method that _always_ has a decode() function, whether the
output is in bytes or as a string

### 2) rdflib-jsonld
**rdflib-jsonld** was a separate package in the `rdflib 5` ecosystem. While it is no longer necessary in
`rdflib 6`, there is no real harm in still having it present.  The issue, however, is as follows:
* version `0.5.0` had a dependency on a variable (`no_2to3`) in `rdflib`.  This 
variable was remove in `rdflib 6`.
* version `0.6.1` works with _either_ `rdflib 5` or `rdflib 6`
* version `0.6.2` was "tombstoned", which, in this context means that 
`pip install rdflib-jsonld` *and* `pip install rdflib-jsonld~=0.5` are no-ops.  They don't do anything

## Recommendations
* If you don't have anything that needs the new stuff in rdflib 6:
  * rdflib>~=5.0
  * rdflib-jsonld==0.6.1
* If you have to force everything to rdflib 6:
  * rdflib~=6.0
  * rdflib-jsonld==0.6.2

## Usage
```python
from rdflib import Graph, RDF, RDFS
import rdflib_shim

# Make sure the import above works
shimed = rdflib_shim.RDFLIB_SHIM

g = Graph()
g.add( (RDFS.Resource, RDF.type, RDFS.resource))
# serialize() and serialize().decode() works in both 5 and 6
g.serialize(format="turtle")
g.serialize(format="turtle").decode()

```
