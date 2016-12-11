Previous: [Simple Meshes](gltfTutorial_008_SimpleMeshes.md) | [Table of Contents](README.md) | Next: [Materials](gltfTutorial_010_Materials.md)

# Meshes

The [Simple Meshes](gltfTutorial_008_SimpleMeshes.md) example from the previous section showed a basic example of a [`mesh`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-mesh) with a [`mesh.primitive`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-mesh.primitive) object that contained several attributes. This section will explain the meaning and usage of mesh primitives, how meshes may be attached to nodes of the scene graph, and how they can be rendered with different materials.


## Mesh primitives 

Each `mesh` contains an array of `mesh.primitive` objects. These mesh primitive objects are smaller parts or building blocks of a larger object. Such a mesh primitive summarizes all information about how the respective part of the object will be rendered.


### Mesh primitive attributes

A mesh primitive defines the geometry data of the object, using its `attributes` dictionary. This geometry data is given by references to `accessor` objects that contain the data of vertex attributes. The details of the `accessor`s have been explained in the section about [Buffers, BufferViews and Accessors](gltfTutorial_005_BuffersBufferViewsAccessors.md).

In the given example, there are three entries in the `attributes` dictionary. The entries refer to the `positionsAccessor`, the `normalsAccessor` and the `texCoordsAccessor`:

```javascript
"meshes" : {
  "mesh0" : {
    "primitives" : [ {
      "attributes" : {
        "POSITION" : "positionsAccessor",
        "NORMAL" : "normalsAccessor",
        "TEXCOORD_0" : "texCoordsAccessor"
      },
      "indices" : "indicesAccessor"
    } ]
  }
},
```

Together, the elements of these acessors define all attributes that belong to the individual vertices, as shown in this image:

<p align="center">
<img src="images/meshPrimitiveAttributes.png" /><br>
<a name="meshPrimitiveAttributes-png"></a>Image 9a: Mesh primitive accessors containing the data of vertices
</p>


### Indexed and non-indexed geometry

The geometry data of a `mesh.primitive` may either be *indexed* geometry, or geometry without indices. In the given example, the `mesh.primitive` contains *indexed* geometry. This is indicated by the `indices` property, which refers to the `"indicesAccessor"`. For non-indexed geometry, this property is omitted.


### Mesh primitive mode  

By default, the geometry data is assumed to describe a triangle mesh. For the case of *indexed* geometry, this means that three consecutive elements of the `indices` accessor are assumed to contain the indices of a single triangle. For non-indexed geometry, three elements of the vertex attribute accessors are assumed to contain the attributes of the three vertices of a triangle.

Different other rendering modes are possible: The geometry data may also describe individual points, lines or triangle strips. This is indicated by the `mode` that may be stored in the mesh primitive: Its value is a constant that indicates how the geometry data has to be interpreted. The mode may, for example, be `0` when the geometry consists of points, or `4` when it consists of triangles. See [the `primitive.mode` specification](https://github.com/KhronosGroup/glTF/tree/master/specification#primitivemode) for a list of available modes.

### Mesh primitive material

The mesh primitive may also refer to the `material` that should be used for rendering, using the ID of this material. In the given example, no `material` is defined, causing the objects to be rendered with a default material that just defines the objects to have a uniform 50% gray color. A detailed explanation of materials and the related concepts will be given in the next section about [Materials](gltfTutorial_010_Materials.md).


## Meshes attached to nodes

In the example from the [Simple Meshes](gltfTutorial_008_SimpleMeshes.md) section, there is a single `scene`, and this scene contains two node, and they both nodes refer to the same `mesh` instance, which is called `"mesh0"`:

```javascript
  "scenes" : {
    "scene0" : {
      "nodes" : [ "node0", "node1" ]
    }
  },
  "nodes" : {
    "node0" : {
      "meshes" : [ "mesh0" ]
    },
    "node1" : {
      "meshes" : [ "mesh0" ],
      "translation" : [ 1.0, 0.0, 0.0 ]
    }
  },

  "meshes" : {
    "mesh0" : {
      ...
    }
  },
```

The node `"node1"` has a `translation` property. As shown in the section about [Scenes and Nodes](gltfTutorial_004_ScenesNodes.md), this will be used to compute the local transform matrix of this node. In this case, the matrix will cause a translation of 1.0 along the x-axis. The product of all local transforms of the nodes will yield the [global transform](gltfTutorial_004_ScenesNodes.md#global-transforms-of-nodes). And all elements that are attached to the nodes will be rendered with this global transform.

So in this example, the mesh will be rendered twice, because it is attached to two nodes: Once with the global transform of `"node0"`, which is the identity transform, and once with the global transform of node `"node1"`, which is a translation of 1.0 along the x-axis.



Previous: [Simple Meshes](gltfTutorial_008_SimpleMeshes.md) | [Table of Contents](README.md) | Next: [Materials](gltfTutorial_010_Materials.md)
