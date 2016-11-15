Previous: [Materials](gltfTutorial_009_Materials.md) | [Table of Contents](README.md) | Next: [Programs and Shaders](gltfTutorial_009b_ProgramsShaders.md)

# A simple material

The examples of glTF assets that have been given in the previous sections contained a basic scene structure and
simple geometric objects. But they did not contain information about the appearance of the objects. When no such information is given, viewers are encouraged to render the objects with a "default" material. And as shown in the screenshot of the [minimal glTF file](gltfTutorial_003_MinimalGltfFile.md), this default material causes the object to be rendered with a uniformly gray color. (The technical details of this default material are described in the [Appendix A: Default Material](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#appendix-a-default-material) of the specification).

This section will start with an example of a very simple material. It is similar to the default material, and only allows changing the color of a rendered object. The basic concepts of materials will be summarized here, and explained in more detail in the remaining sections.

The following is a minimal glTF asset with such a simple material:

```javascript
{
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
        "indices" : "indicesAccessor",
        "material" : "simpleMaterial"
      } ]
    }
  },

  "materials" : {
    "simpleMaterial" : {
      "technique" : "simpleTechnique",
      "values" : {
        "emissionParameter" : [ 0.9, 0.5, 0.1, 1.0 ]
      }
    }
  },
  "techniques": {
    "simpleTechnique": {
      "program": "simpleProgram",
      "attributes": {
        "a_position": "positionParameter"
      },
      "uniforms": {
        "u_modelViewMatrix": "modelViewMatrixParameter",
        "u_projectionMatrix": "projectionMatrixParameter",
        "u_emission": "emissionParameter"
      },
      "parameters": {
        "positionParameter" : {
          "type": 35665,
          "semantic": "POSITION"
        },
        "modelViewMatrixParameter": {
          "type": 35676,
          "semantic": "MODELVIEW"
        },
        "projectionMatrixParameter": {
          "type": 35676,
          "semantic": "PROJECTION"
        },
        "emissionParameter": {
          "value": [ 0.5, 0.5, 0.5, 1.0 ],
          "type": 35666
        }
      }
    }
  },
  "programs": {
    "simpleProgram": {
      "attributes": [
        "a_position"
      ],
      "vertexShader": "simpleVertexShader",
      "fragmentShader": "simpleFragmentShader"
    }
  },
  "shaders": {
    "simpleVertexShader": {
      "uri": "simple.vert",
      "type": 35633
    },
    "simpleFragmentShader": {
      "uri": "simple.frag",
      "type": 35632
    }
  },

  "buffers" : {
    "buffer0" : {
      "uri" : "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAAAAgD8AAAAA",
      "byteLength" : 42
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
      "max" : [ 2.0 ],
      "min" : [ 0.0 ]
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
    "version" : "1.1"
  }
}
```      

Note that this time, the file refers to additional, external resources: The `shader` objects contain URIs that refer to the following files, which will also be exlained later, but are shown here for completeness:

The file `simple.vert` contains the source code of the vertex shader:

    #ifdef GL_ES
        precision highp float;
    #endif

    attribute vec3 a_position;

    uniform mat4 u_modelViewMatrix;
    uniform mat4 u_projectionMatrix;

    void main(void)
    {
        gl_Position = u_projectionMatrix * u_modelViewMatrix * vec4(a_position,1.0);
    }

The file `simple.frag` contains the source code of the fragment shader:

    #ifdef GL_ES
        precision highp float;
    #endif

    uniform vec4 u_emission;

    void main(void)
    {
        gl_FragColor = u_emission;
    }

When rendering this asset, it will show the triangle with a new material:

<p align="center">
<img src="images/triangleWithSimpleMaterial.png" /><br>
<a name="triangle-png"></a>Image 9a: A triangle with a simple material
</p>


## New elements for the simple material

Several new top-level dictionaries have been added to the glTF JSON to define this material. The `materials`, `techniques`, `programs` and `shaders` dictionaries map IDs to objects of different types. The following subsections will show how these objects are represented in the glTF JSON, based on the simple example material.

This description is intended to give a first overview of the structure and interdependencies of these elements. More details will be given in the sections about [programs and shaders](gltfTutorial_009b_ProgramsShaders.md) and [materials and techniques](gltfTutorial_009c_MaterialsTechniques.md), leading to an example of [an advanced material](gltfTutorial_009d_AdvancedMaterial.md).


## The `shaders`

The `shaders` dictionary contains [`shader`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-shader) objects. Each shader contains a `type` property, which is a constant indicating whether the shader is a vertex- or a fragment shader, and a `uri` for the shader source code.

In the simple example, there are two shader objects:

- The vertex shader has the IDs `"simpleVertexShader"`. Its type is `35633` (`GL_VERTEX_SHADER`), and its URI refers to the `simple.vert` file that contains the vertex shader source code  

- The fragment shader has the IDs `"simpleFragmentShader"`. Its type is `35632` (`GL_FRAGMENT_SHADER`), and its URI refers to the `simple.frag` file that contains the fragment shader source code  

```javascript
"shaders": {
  "simpleVertexShader": {
    "type": 35633,
    "uri": "simple.vert"
  },
  "simpleFragmentShader": {
    "type": 35632,
    "uri": "simple.frag"
  }
},
```      

The source code of the shaders contains the definitions of variables that govern the rendering process. There are two types of variables: The `attribute` variables represent attributes of the vertices of the rendered geometry. The `uniform` variables are additional variables that are required for rendering. Later, it will be shown how the values of these variables are determined by the `technique` and `material`.   



## The `programs`

There is a single [`program`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-program) in the newly added `programs` dictionary. Such a program refers to two shaders, namely the `vertexShader` and the `fragmentShader`, using the IDs of these shader objects. Additionally, the program contains an array called `"attributes"` that contains a list of the names of all `attribute` variables that appear in the vertex shader. This will later be used to assign values to these attribute variables, after the program has been compiled.      

```javascript
"programs": {
  "simpleProgram": {
    "vertexShader": "simpleVertexShader",
    "fragmentShader": "simpleFragmentShader",
    "attributes": [
      "a_position"
    ]
  }
},
```      


## The `techniques`

The [`technique`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-technique) is the central element for the definition of the appearance of an object in a glTF asset. In the example, there is a single technique, called `"simpleTechnique"`. The technique refers to a `program`, which is the actual implementation of the rendering process. The technique also summarizes the `attributes` and `uniforms` of the shaders that its program consists of. These are given as dictionaries that map the names of the variables, as they appear in the shader source code, to technique parameter names. For example, the given technique says that there are several `uniforms`. One of these uniforms has the name `"u_emission"` in the shader source code. Additional information about this uniform can be found by looking up the `"emissionParameter"` in the `technique.parameters` dictionary.

```javascript
"techniques": {
  "simpleTechnique": {
    "program": "simpleProgram",
    "attributes": {
      "a_position": "positionParameter"
    },
    "uniforms": {
      "u_modelViewMatrix": "modelViewMatrixParameter",
      "u_projectionMatrix": "projectionMatrixParameter",
      "u_emission": "emissionParameter"
    },
    "parameters": {
      ...
      "emissionParameter": {
        "type": 35666,
        "value": [ 0.5, 0.5, 0.5, 1.0 ]
      }
    }
  }
}
```      

These `technique.parameters` are another dictionary, where the type, meaning and default values of the parameters are defined. For example, for the `"emissionParameter"`, the entry says that this parameter has a certain `type`, which is a constant representing the type of the uniform in the shader. Here, this is `35666`, standing for `GL_FLOAT_VEC4`, a 4D vector with floating point elements. There is also a default `value` for this parameter: It is the 4D vector `[0.5, 0.5, 0.5, 1.0]`:

```javascript
"techniques": {
  "simpleTechnique": {
    ...
    "uniforms": {
      ...
      "u_emission": "emissionParameter"
    },
    "parameters": {
      ...
      "emissionParameter": {
        "type": 35666,
        "value": [ 0.5, 0.5, 0.5, 1.0 ]
      },
      ...
    }
  }
}
```      

Since the `u_emission` parameter in the given example defines the color of the light that is emitted by the object, this means that the default color of an object that is rendered with this technique will be a 50% gray. This value may be overridden by the material, as shown below.


## The `materials`

Each [`material`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-material) can be considered as an instance of a `technique`. In the example, the `materials` dictionary contains a single `material`, with the ID `"simpleMaterial"`. This material contains a reference to the `technique`, namely to the `"simpleTechnique"`. Additionally, it contains a `values` property. This is a dictionary that maps the names of `technique.parameters` objects to the values that the respective parameter should have for this material:


```javascript
"materials" : {
  "simpleMaterial" : {
    "technique" : "simpleTechnique",
    "values" : {
      "emissionParameter" : [ 0.9, 0.5, 0.1, 1.0 ]
    }
  }
},
```

In this example, the default value that the `"emissionParameter"` had in the technique will be overridden. So instead of using the default value that was given in the `technique`, the value of the emission parameter will be set to `[0.9, 0.5, 0.1, 1.0]` when this material is used, causing the rendered objects to appear in a dark orange color.


## Assigning a material to an object

After the `shaders`, `programs`, `techniques` and `materials` have been defined, a material may simply be assigned to an object. To do this, a reference to the material is added in the `mesh.primitive`, causing the mesh primitive to be rendered with this material:     

```javascript
"meshes" : {
  "mesh0" : {
    "primitives" : [ {
      ...
      "material" : "simpleMaterial"
    } ]
  }
},
```


## Summary

The example in this section only referred to a very simple technique. The only true variable in this example was the *color* of the objects, which is determined by the `u_emission` uniform variable in the fragment shader. There are additional variables contained in the shaders, like the attribute for the vertex positions and the uniforms for the model-view and the projection matrix. The values for these variables are either obtained from the `mesh.primitive` that the material is assigned to, or from the *context* in which the object is rendered. These concepts will be explained in more detail in the section about [materials and techniques](gltfTutorial_009c_MaterialsTechniques.md).



Previous: [Materials](gltfTutorial_009_Materials.md) | [Table of Contents](README.md) | Next: [Programs and Shaders](gltfTutorial_009b_ProgramsShaders.md)
