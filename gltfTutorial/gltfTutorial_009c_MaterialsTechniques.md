Previous: [Programs and Shaders](gltfTutorial_009b_ProgramsShaders.md) | [Table of Contents](README.md) | Next: [Advanced Material](gltfTutorial_009d_AdvancedMaterial.md)


# Materials and Techniques

As a reminder, here is a summary of the elements of a glTF asset that are used for defining the appearance of a rendered object:

- A [`material`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-material) can be assigned to a `mesh.primitive`, so that the primitive is rendered with this material. A material can be considered as an "instance" of a `technique`
- A [`technique`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-technique) is the core element for the description of the appearance of rendered objects in a glTF asset. It is an abstract definition of a rendering process, and serves as a "template" for `material` objects
- A [`program`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-program) is the actual *implementation* of a rendering process for a `technique`. It consists of multiple `shader` objects.
- A [`shader`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-shader) is a basic building block for the implementation of a renderer in WebGL or OpenGL

The previous section explained the basics of [programs and shaders](gltfTutorial_009b_ProgramsShaders.md). This section will focus on the role of the `technique` and `material` objects.

## Techniques

A `technique` is a description of a rendering process. It summarizes a set of parameters that are required for controlling the renderer. These parameters directly correspond to the *attributes* and *uniforms* of the shaders that are used for the implementation of the rendering process.

The technique therefore contains `attributes` and `uniforms` dictionaries. The keys of these dictionaries are the variable names of the attributes and uniforms of the shaders. The values of these dictionaries refer to the [`parameters`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-technique.parameters) dictionary of the technique. These `technique.parameters` define the types of the parameters, and how the values of the parameters are obtained. So for each `attribute` and `uniform` of the shader program, there is a `technique.parameters` entry that defines the type that the variable in the shader program has:

<p align="center">
<img src="images/technique.png" /><br>
<a name="technique-png"></a>Image 9c: The connection between shader source code and technique parameters
</p>

To recall the example from the [simple material](gltfTutorial_009a_SimpleMaterial.md), here is an excerpt of the  JSON part that encodes this information:

```javascript
"techniques": {
  "simpleTechnique": {
    "program": "simpleProgram",
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
"programs": {
  "simpleProgram": {
    ...
    "fragmentShader": "simpleFragmentShader",
    ...
  }
},
"shaders": {
  ...
  "simpleFragmentShader": {
    ...
    "uri": "simple.frag"
  }
},
```


The entry in the `uniforms` dictionary of the `technique` says that one of the shaders has a `uniform` variable with the name `"u_emission"` (in this example, it is contained in the `simple.frag` source code). More information about this variable can be found by looking up the `"emissionParameter"` in the `technique.parameters` dictionary. And for this parameter, the entry says that the parameter has a the `type` `35666`, which stands for `GL_FLOAT_VEC4`, and a default `value`, which is `[0.5, 0.5, 0.5, 1.0]`.  




## Materials

A `material` is is an instance of a `technique`, and specifies a set of input values for the `technique.parameters`. Several materials may be created by instantiating `material` objects with the same `technique`, but different parameter values.  

<p align="center">
<img src="images/materialAndTechnique.png" /><br>
<a name="materialAndTechnique-png"></a>Image 9d: Materials and techniques, and how they affect the appearance of objects
</p>



## Technique parameter values

When an object should be rendered with a certain `technique`, then values have to be provided for all input parameters of the corresponding GL program. The following sections will show how these input parameters are defined using the `technique.parameters`, and how the values for these input parameters may be obtained.


### Technique parameter values in materials

In some cases, the technique parameters can have default values. In other cases, the parameter values can be obtained from the material that refers to the technique. This was already shown in the [simple material](gltfTutorial_009a_SimpleMaterial.md) example.

```javascript
"techniques": {
  "simpleTechnique": {
    ...
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

"materials" : {
  "simpleMaterial" : {
    "technique" : "simpleTechnique",
    "values" : {
      "emissionParameter" : [ 0.9, 0.5, 0.1, 1.0 ]
    }
  },
},

```

When an object should be rendered with the `"simpleMaterial"`, then the value for the `"emissionParameter"` can be looked up in the `values` dictionary. In this case, the value will be `[0.9, 0.5, 0.1, 1.0]`, causing the object to be rendered with an orange color.   

One could now define new materials that refer to the same `technique`, but have different values for the `"emissionParameter"`:

```javascript
"materials" : {
  "simpleMaterial" : {
    "technique" : "simpleTechnique",
    "values" : {
      "emissionParameter" : [ 0.9, 0.5, 0.1, 1.0 ]
    }
  },
  "simpleBlueMaterial" : {
    "technique" : "simpleTechnique",
    "values" : {
      "emissionParameter" : [ 0.0, 0.0, 1.0, 1.0 ]
    }
  },
  "simpleDefaultMaterial" : {
    "technique" : "simpleTechnique"
  }
},

```

In the newly added `"simpleBlueMaterial"`, the value for the `"emissionParameter"` is set to `[0.0, 0.0, 1.0, 1.0]`, so that objects with this material will appear in blue.

The newly added `"simpleDefaultMaterial"` does not contain a value for the `"emissionParameter"`. When an object is rendered with this material, then the default value from the `technique.parameter` definition will be used. This default value is `[0.5, 0.5, 0.5, 1.0]`, causing the object to be rendered in a 50% gray.





### Technique parameter values from semantics

As described above, each technique parameter either describes a `uniform` or an `attribute` of the shader program. And in the simplest case, the values for these parameters may be obtained directly from the material. But there are cases where the value of a parameter cannot be encoded in the material. This is the case when the value for this parameter has a certain *semantic*, and its value can only be derived from the context of where the technique is used.

One example of a `uniform` that has such a semantic is the model-view-matrix: The actual value for the model-view-matrix depends on the `node` to which the rendered object is attached. More precisely, the model-view-matrix is the product of the [global transform](gltfTutorial_004_ScenesNodes.md#global-transforms-of-nodes) of the node and the view matrix of the currently active camera. Similarly, the technique parameters that describe an `attribute` can have semantics which refer to the `attribute` of a `mesh.primitive` that contains the actual input data for the parameter.  

Therefore, the `technique.parameters` may have a `semantic` property that contains a string describing the semantics of the parameter:

```javascript
"exampleTechnique": {
    ...
    "parameters": {
        ...
        "position": {
            "type": 35665,
            "semantic": "POSITION"
        },
        "modelViewMatrix": {
            "type": 35676,
            "semantic": "MODELVIEW"
        },
        ...
    },
}
```

There are many different possible semantics for `uniform` parameters. These are listed in this [table in the glTF specification](https://github.com/KhronosGroup/glTF/tree/master/specification#semantics). Additional `attribute` semantics are listed in the [glTF specification of meshes](https://github.com/KhronosGroup/glTF/tree/master/specification#meshes).

In the example above, the technique says that the `position` parameter has the semantic `POSITION`. This means that when a `meshPrimitive` is rendered with this technique, then this `meshPrimitive` must contain an attribute with this name, as described in the section about [mesh primitive attributes](gltfTutorial_008_Meshes.md#mesh-primitive-attributes).













Previous: [Programs and Shaders](gltfTutorial_009b_ProgramsShaders.md) | [Table of Contents](README.md) | Next: [Advanced Material](gltfTutorial_009d_AdvancedMaterial.md)
