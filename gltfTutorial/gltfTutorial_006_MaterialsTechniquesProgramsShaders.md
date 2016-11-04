# Materials, Techniques, Programs, Shaders

## Introduction

As described in the section about [materials in mesh primitives](gltfTutorial_005_MeshesTexturesImagesSamplers.md#mesh-primitive-material), each `meshPrimitive` contains a reference to one `material` that defines how the mesh primitive will be rendered.

There are several well-known parameters that are commonly used to describe a material in rendering applications and graphics APIs:

* The "diffuse" color: The main color of the material, which is often defined by a texture
* The "specular" color: The color of specular highlights
* The "shininess" factor: A value that defines the shininess of the object, influencing the size of the specular highlights
* The "emissive" color: The color of the light that is emitted by the object
* ...

Many file formats contain this information in one or the other form. For example, [Wavefront OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file) files are combined with `MTL` files that contain exactly these parameters. Viewers can read this information and render the objects accordingly.

However, one of the goals of glTF was to **not** constrain the rendering to one simple, fixed material model. It should be possible to encapsulate arbitrary rendered scenes in one glTF asset, *including* the information about how exactly the objects are rendered. This is an ambitious goal: There are unlimited degrees of freedom for renderer implementations. To retain this flexibility, the glTF specification of materials can be considered as a very generic description of rendering processes. On the lowest level, it encapsulates the actual GLSL shader programs, and thus can cover nearly all imaginable rendering pipelines.

This flexibility comes at a certain cost. Several elements in the glTF asset have to be combined properly by the renderer to exploit this flexibility. The following sections will break down these elements and describe how they are combined and interpreted to finally render an asset. The description will be given in a bottom-up fashion: It will start with a short summary of how GLSL shaders are used for rendering, and show how these shaders are encoded in glTF. Then, it will show how these shader programs serve as the basis for describing a generic rendering technique. Finally, it will give describe the process of rendering an object based on a the material definition that was given in the glTF.


## Programs and Shaders

The rendering process in OpenGL or WebGL is described with small shader programs, which are written in [GLSL, the OpenGL shading language](https://www.opengl.org/documentation/glsl/). Such a shader program consists of at least two shaders, namely the vertex shader and the fragment shader. Roughly speaking, the vertex shader defines how the vertices of an object are transformed, preprocessed and projected on the screen, and the fragment shader defines how these projected vertices are used to fill the pixels on the screen to generate the final rendered image. For further details, refer to one of the GLSL tutorials (e.g. at [open.gl](https://open.gl/drawing#Shaders), [webglfundamentals.org](http://webglfundamentals.org/webgl/lessons/webgl-shaders-and-glsl.html) or others)

### Shaders

In the context of glTF, the vertex- and fragment shader are usually contained in dedicated files, which are referred to by the [`shader`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-shader) objects using a URI:

```javascript
"shaders": {
    "exampleVertexShader": {
        "uri": "vertexShader.glsl",
        "type": 35633
    },
    "exampleFragmentShader": {
        "uri": "fragmentShader.glsl",
        "type": 35632
    }
}
```

The shader source code that is referred to by the URI is stored as a plain text, as described in the section about [GLSL shader data in `shaders`](gltfTutorial_002_BasicGltfStructure.md#glsl-shader-data-in-shaders). This source code can be read into a string, and directly be compiled by OpenGL or WebGL. In addition to the URI, the `shader` object also contains the `type` of the shader, which simply is the respective GL constant: Either `35633` (`GL_VERTEX_SHADER`) for vertex shaders, or `35632` (`GL_FRAGMENT_SHADER`) for fragment shaders.


#### Attributes and uniforms in shaders

The vertex shader may define different *attributes*. These attributes describe all properties of a single vertex. Recall this image, already shown in the section about [Mesh primitive attributes](gltfTutorial_005_MeshesTexturesImagesSamplers.md#mesh-primitive-attributes):

<p align="center">
<img src="images/meshPrimitiveAttributes.png" /><br>
<a name="meshPrimitiveAttributes-png"></a>Image 6a: Mesh primitive accessors containing the data of vertices
</p>

The vertex shader is executed for each vertex, and receives the attribute values for the respective vertex in the attribute variables. For example, the following vertex shader defines attributes for the position, normal and texture coordinate of each vertex:

```glsl
attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_texcoord0;

...
uniform vec3 u_lightDirection;
uniform mat4 u_modelViewMatrix;
...

void main(void)
{
    vec4 pos = u_modelViewMatrix * vec4(a_position,1.0);
    ...
    gl_Position = ...;
}
```

Additionally, the vertex- and fragment shaders can define *uniforms*. These are further input parameters for the rendering process which are constant for the current draw call. For example, the vertex shader above defines uniforms for the light direction and the model-view-matrix. The following fragment shader defines additional uniforms for the ambient light color, and for a texture that will be used as the diffuse color of the material:

```glsl
...
uniform vec4 u_ambientLightColor;
uniform sampler2D u_diffuseTexture;
...

void main(void)
{
    ...
    vec4 color = texture2D(u_diffuseTexture, ...);
    color.xyz += u_ambientLightColor.xyz;
    gl_FragColor = color;
}
```

The attributes and the uniforms of the vertex- and the fragment shader together define the whole set of input parameters for the rendering process. Later, it will be shown how the values for these input parameters are provided in the glTF JSON, and how they can be passed to the renderer.



### Programs

The vertex- and the fragment shader are combined into a single [`program`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-program). In the glTF JSON, this program simply refers to the shaders using their IDs, and summarizes all attributes that appear in the vertex shader:

```javascript
"exampleProgram": {
    "vertexShader": "exampleVertexShader",
    "fragmentShader": "exampleFragmentShader",
    "attributes": [
        "a_position",
        "a_normal",
        "a_texcoord0"
    ]
}
```


For the purpose of this tutorial, the main point is that the glTF JSON contains `program`s that refer to `shader`s, and the `shader`s refer to their source code, and that this information is all that is required to create the corresponding GL program. For now, one can assume that after the glTF JSON has been parsed and the GL programs have been created, there exists a dictionary that contains the GL program identifier for each glTF `program` ID.




### Materials and Techniques

The central element for the definition of the rendering process in glTF is a [`technique`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-technique). It contains a description of the inputs for the rendering process, like geometry information, textures and other parameters. These inputs directly correspond to the *attributes* and *uniforms* of the shader programs.

A technique can be considered as a "template" for one [`material`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-material). The material is only a collection of input values for the parameters that are defined by the technique. Several materials may be created by instantiating `material` objects with the same `technique`, but different parameter values.  

<p align="center">
<img src="images/materialAndTechnique.png" /><br>
<a name="materialAndTechnique-png"></a>Image 6b: Materials and techniques, and how they affect the appearance of objects
</p>

When a material does not refer to a technique, then it will be considered as a *default material*, with a certain default technique, as explained in the [Appendix A of the specification](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#appendix-a-default-material).

The following is an example of one technique that may be found in the glTF JSON:

```javascript
"exampleTechnique": {

    "program": "exampleProgram",

    "attributes": {
        "a_position": "position",
        "a_normal": "normal",
        "a_texcoord0": "texcoord0"
    },

    "uniforms": {
        "u_ambientLightColor": "ambientLightColor",
        "u_diffuseTexture": "diffuseTexture",
        "u_lightDirection": "lightDirection",
        "u_modelViewMatrix": "modelViewMatrix",
        ...
    },

    "parameters": {
        "position": {
            "type": 35665,
            "semantic": "POSITION"
        },
        ...
        "ambientLightColor": {  "type": 35666 },
        "diffuseTexture": {  "type": 35678 },
        "lightDirection": {
          "type": 35665,
          "value": [ 1, 1, 1 ]
        },
        "modelViewMatrix": {
            "type": 35676,
            "semantic": "MODELVIEW"
        },
        ...
    },
}
```

The technique refers to a [`program`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-program), which describes the GLSL shader program. The technique also contains `attributes` and `uniforms` dictionaries. The keys of these dictionaries are the variable names of the attributes and uniforms of the shaders of the program. The values of these dictionaries refer to the [`parameters`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-technique.parameters) dictionary of the technique. These `technique.parameters` define the types of the parameters, and how the values of the parameters are obtained. So for each `attribute` and `uniform` of the shader program, there is a `technique.parameters` entry that defines the type that the variable in the shader program has:

<p align="center">
<img src="images/technique.png" /><br>
<a name="technique-png"></a>Image 6c: The connection between shader source code and technique parameters
</p>



#### Technique parameter values

When an object should be rendered with a certain `technique`, then values have to be provided for all input parameters of the corresponding GL program. The following sections will show how these input parameters are defined using the `technique.parameters`, and how the values for these input parameters may be obtained.


##### Technique parameter values in materials

In many cases, the values for the parameters are simply obtained from the material that refers to the technique. For example, consider the parameters in the following technique:

```javascript
"exampleTechnique": {
    ...
    "parameters": {

        "ambientLightColor": {  "type": 35666 },
        "diffuseTexture": {  "type": 35678 },
        ...
    }
}
```

Each parameter only contains information about the `type` of the parameter, given as an GL constant. The values are, for example, `35666` for `GL_FLOAT_VEC4` and `35678` for `GL_SAMPLER_2D`.  


The value for such a parameter is then assumed to be given explicitly in the `material`. For example, for the parameters above, the `material.values` dictionary will contain the corresponding entries:

```javascript
"materials": {
    "exampleMaterial": {
        "technique": "exampleTechnique",
        "values": {
            "ambientLightColor": [ 0, 0, 0, 1 ],
            "diffuseTexture": "exampleTexture",
          ...
        }
    }
},
```

The description of a technique parameter may also contain a default value. For example, the technique parameter for the light direction in this technique:

```javascript
"exampleTechnique": {
    ...
    "parameters": {
        ...
        "lightDirection": {
            "type": 35665,
            "value": [ 1, 1, 1 ]
        },
        ...
    }
}
```

It defines the type to be `35664` for `GL_FLOAT_VEC3`, and contains a default value for the parameter. If the material does not contain a value for this parameter, then the default value will be used.



##### Technique parameter values from semantics

As described above, each technique parameter either describes a `uniform` or an `attribute` of the shader program. And in the simplest case, the values for these parameters may be obtained directly from the material. But there are cases where the value of a parameter cannot be encoded in the material. This is the case when the value for this parameter has a certain *semantic*, and its value can only be derived from the context of where the technique is used.

One example of a `uniform` that has such a semantic is the model-view-matrix: The actual value for the model-view-matrix depends on the `node` to which the rendered object is attached. More precisely, the model-view-matrix is the product of the [global transform](gltfTutorial_004_ScenesNodesCamerasAnimations.md#global-transforms-of-nodes) of the node and the view matrix of the currently active camera. Similarly, the technique parameters that describe an `attribute` can have semantics which refer to the `attribute` of a `meshPrimitive` that contains the actual input data for the parameter.  

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

In the example above, the technique says that the `position` parameter has the semantic `POSITION`. This means that when a `meshPrimitive` is rendered with this technique, then this `meshPrimitive` must contain an attribute with this name, as described in the section about [mesh primitive attributes](gltfTutorial_005_MeshesTexturesImagesSamplers.md#mesh-primitive-attributes).
