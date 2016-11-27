Previous: [Advanced Material](gltfTutorial_009d_AdvancedMaterial.md) | [Table of Contents](README.md) | Next: [Textures, Images, Samplers](gltfTutorial_009f_TexturesImagesSamplers.md)

# A simple texture

The materials that have been shown in the previous sections contained different parameters for defining the color of the materials or the overall appearance of the material under the influence of light. One important part for a more realistic appearance of models has been missing so far: Textures. This section will give an example of a glTF asset that contains a simple, single texture. The concepts of `texture`, `image` and `sampler` objects will be explained in more detail in the following section.


The following is a glTF asset that defines a material with a texture: 

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
          "POSITION" : "positionsAccessor",
          "NORMAL" : "normalsAccessor",
          "TEXCOORD_0" : "texCoordsAccessor"
        },
        "indices" : "indicesAccessor",
        "material" : "textureMaterial"
      } ]
    }
  },

  "materials" : {
    "textureMaterial" : {
      "technique" : "textureTechnique"
    }
  },
  "techniques": {
    "textureTechnique": {
      "program": "textureProgram",
      "attributes": {
        "a_position": "positionParameter",
        "a_normal": "normalParameter",
        "a_texcoord0": "texcoord0Parameter"
      },
      "uniforms": {
        "u_modelViewMatrix": "modelViewMatrixParameter",
        "u_normalMatrix": "normalMatrixParameter",
        "u_projectionMatrix": "projectionMatrixParameter",
        "u_ambient": "ambientParameter",
        "u_diffuse": "diffuseParameter",
        "u_specular": "specularParameter",
        "u_shininess": "shininessParameter"
      },
      "parameters": {
        "positionParameter" : {
          "type": 35665,
          "semantic": "POSITION"
        },
        "normalParameter" : {
          "type": 35665,
          "semantic": "NORMAL"
        },
        "texcoord0Parameter" : {
          "type": 35664,
          "semantic": "TEXCOORD_0"
        },
        "modelViewMatrixParameter": {
          "type": 35676,
          "semantic": "MODELVIEW"
        },
        "normalMatrixParameter": {
          "type": 35675,
          "semantic": "MODELVIEWINVERSETRANSPOSE"
        },
        "projectionMatrixParameter": {
          "type": 35676,
          "semantic": "PROJECTION"
        },
        "ambientParameter": {
          "type": 35666,
          "value": [ 0.1, 0.1, 0.1, 1.0 ]
        },
        "diffuseParameter": {
          "type": 35678,
          "value": "exampleTexture"
        },
        "specularParameter": {
          "type": 35666,
          "value": [ 1.0, 1.0, 1.0, 1.0 ]
        },
        "shininessParameter": {
          "type": 5126,
          "value": [ 40.0 ]
        }
      },
      "states": {
        "enable": [
          2929
        ]
      }
    }
  },
  "programs": {
    "textureProgram": {
      "vertexShader": "textureVertexShader",
      "fragmentShader": "textureFragmentShader",
      "attributes": [
        "a_position",
        "a_normal"
      ]
    }
  },
  "shaders": {
    "textureVertexShader": {
      "type": 35633,
      "uri": "texture.vert"
    },
    "textureFragmentShader": {
      "type": 35632,
      "uri": "texture.frag"
    }
  },
  
  
  "textures": {
    "exampleTexture": {
      "target": 3553,
      "internalFormat": 6408,
      "format": 6408,
      "type": 5121,
      "source": "exampleImage",
      "sampler": "exampleSampler"
    }
  },
  "images": {
    "exampleImage": {
      "uri": "testTexture.png"
    }
  },
  "samplers": {
    "exampleSampler": {
       "magFilter": 9729,
       "minFilter": 9987,
       "wrapS": 33648,
       "wrapT": 33648
     }
  },
  

  "buffers" : {
    "buffer0" : {
      "uri" : "data:application/octet-stream;base64,AAABAAIAAQADAAIAAAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAAAAgD8AAAAAAACAPwAAgD8AAAAAAAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AACAPwAAgD8=",
      "byteLength" : 140
    }
  },
  "bufferViews" : {
    "indicesBufferView" : {
      "buffer" : "buffer0",
      "byteOffset" : 0,
      "byteLength" : 12,
      "target" : 34963
    },
    "attributesBufferView" : {
      "buffer" : "buffer0",
      "byteOffset" : 12,
      "byteLength" : 128,
      "target" : 34962
    }
  },
  "accessors" : {
    "indicesAccessor" : {
      "bufferView" : "indicesBufferView",
      "byteOffset" : 0,
      "componentType" : 5123,
      "count" : 6,
      "type" : "SCALAR",
      "max" : [ 3.0 ],
      "min" : [ 0.0 ]
    },
    "positionsAccessor" : {
      "bufferView" : "attributesBufferView",
      "byteOffset" : 0,
      "componentType" : 5126,
      "count" : 4,
      "type" : "VEC3",
      "max" : [ 1.0, 1.0, 0.0 ],
      "min" : [ 0.0, 0.0, 0.0 ]
    },
    "normalsAccessor" : {
      "bufferView" : "attributesBufferView",
      "byteOffset" : 48,
      "componentType" : 5126,
      "count" : 4,
      "type" : "VEC3",
      "max" : [ 0.0, 0.0, 1.0 ],
      "min" : [ 0.0, 0.0, 1.0 ]
    },
    "texCoordsAccessor" : {
      "bufferView" : "attributesBufferView",
      "byteOffset" : 96,
      "componentType" : 5126,
      "count" : 4,
      "type" : "VEC2",
      "max" : [ 1.0, 1.0 ],
      "min" : [ 0.0, 0.0 ]
    }
  },
  
  "asset" : {
    "version" : "1.1"
  }
}
```

The vertex shader source code is stored in `texture.vert`:

```glsl
#ifdef GL_ES
    precision highp float;
#endif

attribute vec3 a_position;
attribute vec3 a_normal;
attribute vec2 a_texcoord0;

uniform mat3 u_normalMatrix;
uniform mat4 u_modelViewMatrix;
uniform mat4 u_projectionMatrix;

varying vec3 v_position;
varying vec3 v_normal;
varying vec2 v_texcoord0;

varying vec3 v_light0Direction;

void main(void) 
{
    vec4 pos = u_modelViewMatrix * vec4(a_position, 1.0);
    v_normal = u_normalMatrix * a_normal;
    v_position = pos.xyz;
    v_light0Direction = mat3(u_modelViewMatrix) * vec3(1.0, 1.0, 1.0);
    v_texcoord0 = a_texcoord0;
    gl_Position = u_projectionMatrix * pos;
}
```


The fragment shader source code is stored in `texture.frag`:

```glsl
#ifdef GL_ES
    precision highp float;
#endif

varying vec3 v_position;
varying vec3 v_normal;
varying vec2 v_texcoord0;

uniform vec4 u_ambient;
uniform sampler2D u_diffuse;
uniform vec4 u_specular;
uniform float u_shininess;

varying vec3 v_light0Direction;

void main(void) 
{
    vec3 normal = normalize(v_normal);
    vec4 color = vec4(0.0, 0.0, 0.0, 0.0);
    vec3 diffuseLight = vec3(0.0, 0.0, 0.0);
    vec3 lightColor = vec3(1.0, 1.0, 1.0);
    vec4 ambient = u_ambient;
    vec4 diffuse = texture2D(u_diffuse, v_texcoord0);
    vec4 specular = u_specular;

    vec3 specularLight = vec3(0.0, 0.0, 0.0);
    {
        float specularIntensity = 0.0;
        float attenuation = 1.0;
        vec3 l = normalize(v_light0Direction);
        vec3 viewDir = -normalize(v_position);
        vec3 h = normalize(l+viewDir);
        specularIntensity = max(0.0, pow(max(dot(normal,h), 0.0) , u_shininess)) * attenuation;
        specularLight += lightColor * specularIntensity;
        diffuseLight += lightColor * max(dot(normal,l), 0.0) * attenuation;
    }
    specular.rgb *= specularLight;
    diffuse.rgb *= diffuseLight;
    color.rgb += ambient.rgb;
    color.rgb += diffuse.rgb;
    color.rgb += specular.rgb;
    color.a = diffuse.a;
    gl_FragColor = color;
}
```

The actual image that the texture consists of is stored as a PNG file called `"testTexture.png"`:

<p align="center">
<img src="images/testTexture.png" /><br>
<a name="testTexture-png"></a>Image 9h: The image for the simple texture example
</p>

Bringing this all together in a renderer will result in the following rendered scene:

<p align="center">
<img src="images/simpleTexture.png" /><br>
<a name="simpleTexture-png"></a>Image 9i: A simple texture on a unit square
</p>






Previous: [Advanced Material](gltfTutorial_009d_AdvancedMaterial.md) | [Table of Contents](README.md) | Next: [Textures, Images, Samplers](gltfTutorial_009f_TexturesImagesSamplers.md)
