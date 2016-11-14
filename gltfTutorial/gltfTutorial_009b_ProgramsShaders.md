Previous: [Simple Material](gltfTutorial_009a_SimpleMaterial.md) | [Table of Contents](README.md) | Next: [Materials and Techniques](gltfTutorial_009c_MaterialsTechniques.md)


# Programs and Shaders

The rendering process in OpenGL or WebGL is described with so-called shader programs. These are small programs that are written in [GLSL, the OpenGL shading language](https://www.opengl.org/documentation/glsl/). This section will give a short summary of the concept of shader programs in the context of glTF. For a general introduction or further details, dedicated tutorials should be consulted - for example, at [webglfundamentals.org](http://webglfundamentals.org/webgl/lessons/webgl-shaders-and-glsl.html) or [open.gl](https://open.gl/drawing#Shaders). 
  

### Shaders

A shader program consists of at least two shaders, namely the vertex shader and the fragment shader. In the context of glTF, the vertex- and fragment shader are usually contained in dedicated files, which are referred to by the [`shader`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-shader) objects using a URI:

```javascript
"shaders": {
    "exampleVertexShader": {
        "uri": "exampleShader.vert",
        "type": 35633
    },
    "exampleFragmentShader": {
        "uri": "exampleShader.frag",
        "type": 35632
    }
}
```

The shader source code that is referred to by the URI is stored as a plain text, as described in the section about [GLSL shader data in `shaders`](gltfTutorial_002_BasicGltfStructure.md#glsl-shader-data-in-shaders). This source code can be read into a string, and directly be compiled with WebGL or OpenGL. In addition to the URI, the `shader` object also contains the `type` of the shader, which simply is the respective GL constant: Either `35633` (`GL_VERTEX_SHADER`) for vertex shaders, or `35632` (`GL_FRAGMENT_SHADER`) for fragment shaders.


#### Attributes and uniforms in shaders

The vertex shader may define different *attributes*. The vertex shader is executed for each vertex, and receives the attribute values for the respective vertex in the attribute variables. For example, the following vertex shader defines attributes for the position, normal and texture coordinate of each vertex:

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

The attributes and the uniforms of the vertex- and the fragment shader together define the whole set of input parameters for the rendering process. Later, it will be shown how the actual values for these input parameters are derived from the asset description in the glTF JSON.



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


For the purpose of this tutorial, the main points are that the glTF JSON contains `program` objects that refer to `shader` objects, each `shader` refers to its source code, and this information is all that is required to create the corresponding GL program in the renderer.

In order to actually use this program to render an object, further information is required. Particularly, there must be information about the `attribute` and `uniform` variables that are contained in the shaders. This information is encoded in the `technique` that refers to a `program`, as shown in the next section about [materials and techniques](gltfTutorial_009c_MaterialsTechniques.md).



Previous: [Simple Material](gltfTutorial_009a_SimpleMaterial.md) | [Table of Contents](README.md) | Next: [Materials and Techniques](gltfTutorial_009c_MaterialsTechniques.md)
