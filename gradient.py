from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import math

part_name = 'n'
h1 = 948
h2 = 938
w1 = 2280
w2 = 2280
l = (52+26) * 150
inter = 150
n = int(math.floor(l/inter)) + 1
if h2 - h1 != 0:
    incr = (h2 - h1) / n
else:
    incr = (w2 - w1) / n

for i in range(n):
    s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
    g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
    s.setPrimaryObject(option=STANDALONE)
    s.Line(point1=(0, 0), point2=(w1, 0))
    s.HorizontalConstraint(entity=g[2], addUndoState=False)
    s.Line(point1=(w1, 0), point2=(w1, -(h1 + i * incr)))
    s.VerticalConstraint(entity=g[3], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
    s.Line(point1=(w1, -(h1 + i * incr)), point2=(0, -(h1 + i * incr)))
    s.HorizontalConstraint(entity=g[4], addUndoState=False)
    s.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
    s.Line(point1=(0, -(h1 + i * incr)), point2=(0, 0))
    s.VerticalConstraint(entity=g[5], addUndoState=False)
    p = mdb.models['Model-1'].Part(dimensionality= THREE_D, name= part_name + str(i), type=DEFORMABLE_BODY)
    p.BaseWire(sketch=s)
    del mdb.models['Model-1'].sketches['__profile__']
    mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name=part_name + str(i) + '-1', part=mdb.models['Model-1'].parts[part_name + str(i)])


for j in range(1, n):
    mdb.models['Model-1'].rootAssembly.instances[part_name + str(j) + '-1'].translate(vector=(0, 0.0, inter * j))

mdb.models['Model-1'].rootAssembly.InstanceFromBooleanMerge(domain=GEOMETRY, instances=tuple([mdb.models['Model-1'].rootAssembly.instances['n' + str(i) + '-1'] for i in range(n)]), name='top_cage', originalInstances=DELETE)

