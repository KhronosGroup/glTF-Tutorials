Previous: [Basic glTF structure](gltfTutorial_002_BasicGltfStructure.md) | [Table of Contents](README.md) | Next: [Scenes and nodes](gltfTutorial_004_ScenesNodes.md)


# A minimal glTF file

The following is a minimal but complete glTF asset, containing a single triangle. You can copy and paste it into a `gltf` file, and every glTF-based application should be able to load and render it. This section will explain the basic concepts of glTF based on this example.

```javascript
{
  "scene" : "scene0",
  "scenes" : {
    "scene0" : {
      "nodes" : [ "node0" ]
    }
  },
  "nodes" : {
    "node0" : {
      "meshes" : [ "mesh0" ]
    }
  },
  "meshes" : {
    "mesh0" : {
      "primitives" : [ {
        "attributes" : {
          "POSITION" : "positionsAccessor"
        },
        "indices" : "indicesAccessor"
      } ]
    }
  },

  "buffers" : {
    "buffer0" : {
      "uri" : "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAAAAgD8AAAAA",
      "byteLength" : 42,
    }
  },
  "bufferViews" : {
    "indicesBufferView" : {
      "buffer" : "buffer0",
      "byteOffset" : 0,
      "byteLength" : 6,
      "target" : 34963
    },
    "positionsBufferView" : {
      "buffer" : "buffer0",
      "byteOffset" : 6,
      "byteLength" : 36,
      "target" : 34962
    }
  },
  "accessors" : {
    "indicesAccessor" : {
      "bufferView" : "indicesBufferView",
      "byteOffset" : 0,
      "componentType" : 5123,
      "count" : 3,
      "type" : "SCALAR",
      "max" : [ 2 ],
      "min" : [ 0 ]
    },
    "positionsAccessor" : {
      "bufferView" : "positionsBufferView",
      "byteOffset" : 0,
      "componentType" : 5126,
      "count" : 3,
      "type" : "VEC3",
      "max" : [ 1.0, 1.0, 0.0 ],
      "min" : [ 0.0, 0.0, 0.0 ]
    }
  },
  "asset" : {
    "version" : "1.0"
  }
}
```

<p align="center">
<img src="images/triangle.png" /><br>
<a name="triangle-png"></a>Image 3a: A single triangle
</p>


## The `scene` and `nodes` structure

The [`scene`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-scene) is the entry point for the description of the scene that is stored in the glTF. When parsing a glTF JSON file, the traversal of the scene structure will start here. Each scene contains an array called `nodes`, which contains the IDs of [`node`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-node) objects. These nodes are the root nodes of a scene graph hierarchy.

The example here consists of a single scene, called `"scene0"`. It refers to the only node in this example, which is the node with the ID `"node0"`. This node, in turn, refers to the only mesh, which has the ID `"mesh0"`:


```javascript
  "scenes" : {
    "scene0" : {
      "nodes" : [ "node0" ]
    }
  },
  "nodes" : {
    "node0" : {
      "meshes" : [ "mesh0" ]
    }
  },
```

More details about scenes and nodes and their properties will be given in section about [Scenes and nodes](gltfTutorial_004_ScenesNodes.md).


## The `meshes`

A [`mesh`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-mesh) represents an actual geometric object that appears in the scene. The mesh itself usually does not have any properties, but only contains an array of [`mesh.primitive`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-mesh.primitive) objects, which serve as building blocks for larger models. Each mesh primitive contains a description of the geometry data that the mesh consists of.   

The example consists of a single mesh, which has the ID `"mesh0"`, and has a single `mesh.primitive` object. The mesh primitive has an array of `attributes`. These are the attributes of the vertices of the mesh geometry, and in this case, this is only the `POSITION` attribute, describing the positions of the vertices. The mesh primitive describes an *indexed* geometry, which is indicated by the reference to the `indices`. By default, it is assumed to describe a set of triangles, so that three consecutive indices are the indices of the vertices of one triangle.

The actual geometry data of the mesh primitive is given by the `attributes` and the `indices`. These both refer to `accessor` objects, which will be explained below.

```javascript
  "meshes" : {
    "mesh0" : {
      "primitives" : [ {
        "attributes" : {
          "POSITION" : "positionsAccessor"
        },
        "indices" : "indicesAccessor"
      } ]
    }
  },
```

A more detailed description about meshes and mesh primitives can be found in the [Meshes](gltfTutorial_007_Meshes.md) section.


## The `buffer`, `bufferView` and `accessor` concepts

The `buffer`, `bufferView` and `accessor` objects provide information about the geometry data that the mesh primitives consist of. They are introduced here quickly, based on the specific example. A more detailed description of these concepts will be given in the section about [Buffers, BufferViews and Accessors](gltfTutorial_005_BuffersBufferViewsAccessors.md).

### Buffers

A [`buffer`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-buffer) defines a block of raw, unstructured data with no inherent meaning. It contains an `uri`, which can either point to an external file that contains the data, or it can be a [data URI](gltfTutorial_002_BasicGltfStructure.md#binary-data-in-data-uris) that encodes the binary data directly in the JSON file.

In the example file, the second approach is used: There is a single buffer with the ID `"buffer0"`, containing 42 bytes, and the data of a this buffer is encoded as a data URI:

```javascript
  "buffers" : {
    "buffer0" : {
      "uri" : "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAAAAgD8AAAAA",
      "byteLength" : 42
    }
  },
```

This data contains the indices of the triangle, and the vertex positions of the triangle. But in order to actually use this data as the geometry data of a mesh primitive, additional information about the *structure* of this data is required. This information about the structure is encoded in the `bufferView` and `accessor` objects.

### Buffer views

A [`bufferView`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-bufferView) describes a "chunk" or a "slice" of the whole, raw buffer data. In the given example, there are two buffer views. They both refer to the same buffer, using its ID. The first buffer view is called `"indicesBufferView"`, and refers to the part of the buffer that contains the data of the indices: It has a `byteOffset` of 0 referring to the whole buffer data, and a `byteLength` of 6. The second buffer view is called `"positionsBufferView"`, and refers to the part of the buffer that contains the vertex positions. It starts at a `byteOffset` of 6, and has a `byteLength` of 36, that is, it extends to the end of the whole buffer.

```javascript
  "bufferViews" : {
    "indicesBufferView" : {
      "buffer" : "buffer0",
      "byteOffset" : 0,
      "byteLength" : 6,
      "target" : 34963
    },
    "positionsBufferView" : {
      "buffer" : "buffer0",
      "byteOffset" : 6,
      "byteLength" : 36,
      "target" : 34962
    }
  },
```


### Accessors

The second step of structuring the data is accomplished with  [`accessor`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-accessor) objects. They define how the data of a `bufferView` has to be interpreted, by provide information about the data types and the layout.

In the example, there are two accessor objects.

The first accessor is called `"indicesAccessor"`, and describes the indices of the geometry data. It refers to the `"indicesBufferView"`, which is the part of the `buffer` that contains the raw data for the indices. Additionally, it specifies the `count` and `type` of the elements and their `componentType`. In this case, there are 3 scalar elements, and their component type is given by a constant that stands for the `unsigned short` type.

The second accessor is called `"positionsAccessor"` and describes the vertex positions. It contains a reference to the relevant part of the buffer data, via the `"positionsBufferView"`, and its `count`, `type` and `componentType` properties say that there are 3 elements of 3D vectors, each having `float` components.


```javascript
  "accessors" : {
    "indicesAccessor" : {
      "bufferView" : "indicesBufferView",
      "byteOffset" : 0,
      "componentType" : 5123,
      "count" : 3,
      "type" : "SCALAR",
      "max" : [ 2 ],
      "min" : [ 0 ]
    },
    "positionsAccessor" : {
      "bufferView" : "positionsBufferView",
      "byteOffset" : 0,
      "componentType" : 5126,
      "count" : 3,
      "type" : "VEC3",
      "max" : [ 1.0, 1.0, 0.0 ],
      "min" : [ 0.0, 0.0, 0.0 ]
    }
  },
```

As described above, a `mesh.primitive` may now refer to these accessors, using their IDs:

```javascript
  "meshes" : {
    "mesh0" : {
      "primitives" : [ {
        "attributes" : {
          "POSITION" : "positionsAccessor"
        },
        "indices" : "indicesAccessor"
      } ]
    }
  },
```

When this `mesh.primitive` has to be rendered, the renderer can resolve the underlying buffer views and buffers, and send the required parts of the buffer to the renderer, together with the information about the data types and layout. A more detailed description of how the accessor data is obtained and processed by the renderer is given in the section about [Buffers, BufferViews and Accessors](gltfTutorial_005_BuffersBufferViewsAccessors.md) and the section about [Materials and Techniques](gltfTutorial_009c_MaterialsTechniques.md)




## The `asset` description

In glTF 1.0, this property is still optional, but in subsequent glTF versions, the JSON file is required to contain an `asset` property that contains the `version` number. The example here says that the asset complies to glTF version 1.1:

```javascript
  "asset" : {
    "version" : "1.1"
  }
```

The `asset` property may contain additional metadata that is described in the [`asset` specification](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#reference-asset).




Previous: [Basic glTF structure](gltfTutorial_002_BasicGltfStructure.md.md) | [Table of Contents](README.md) | Next: [Scenes and nodes](gltfTutorial_004_ScenesNodes.md)
