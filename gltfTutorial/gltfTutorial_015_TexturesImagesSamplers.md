Previous: [Simple Texture](gltfTutorial_014_SimpleTexture.md) | [Table of Contents](README.md) | Next: [Cameras](gltfTutorial_016_Cameras.md)

# Textures, Images, Samplers

A glTF asset may define multiple [`texture`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-texture) objects that can be used as the textures of geometric objects during rendering. Depending on the graphics API, there may be many features and settings that influence the process of texture mapping. Many of these details are beyond the scope of this tutorial. There are dedicated tutorials that explain the exact meaning of all the texture mapping parameters and settings, for example, on [webglfundamentals.org](http://webglfundamentals.org/webgl/lessons/webgl-3d-textures.html),  [open.gl](https://open.gl/textures) and others. This section will only summarize how the information about textures is encoded in a glTF asset.

There are three top-level dictionaries for the definition of textures in the glTF JSON. The `textures`, `samplers` and `images` dictionaries map IDs to [`texture`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-texture),  [`sampler`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-sampler) and [`image`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-image) objects, respectively. The following is an excerpt from the [Simple Texture](gltfTutorial_009e_SimpleTexture.md)  example of the previous section that shows these dictionaries:

```javascript
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
```

The `texture` itself uses IDs to refer to one `sampler` and one `image`.


The most important part here is the reference to the `image`: It contains a URI that links to the actual image file that will be used for the texture. Information about how to read this image data can be found in the section about [Image data in `images`](gltfTutorial_002_BasicGltfStructure.md#image-data-in-images).


Previous: [Simple Texture](gltfTutorial_014_SimpleTexture.md) | [Table of Contents](README.md) | Next: [Cameras](gltfTutorial_016_Cameras.md)
