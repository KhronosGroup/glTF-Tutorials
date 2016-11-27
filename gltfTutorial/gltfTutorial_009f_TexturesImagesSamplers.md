# Textures, Images, Samplers

A glTF asset may define multiple [`texture`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-texture) objects that can be used as the textures of geometric objects during rendering. The process of texture mapping can be a bit complicated, and many of the details are beyond the scope of this tutorial. There are dedicated tutorials that explain the exact meaning of all the texture mapping parameters and settings (for example, on [webglfundamentals.org](http://webglfundamentals.org/webgl/lessons/webgl-3d-textures.html),  [open.gl](https://open.gl/textures) and others). This section will only summarize how the information about textures is encoded in a glTF asset.

The following is an example of a [`texture`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-texture), a [`sampler`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-sampler) and an [`image`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-image) as they may be found in the glTF JSON:


```javascript
"textures": {
    "exampleTexture": {
        "target": 3553,
        "internalFormat": 6408,
        "format": 6408,
        "type": 5121,
        "sampler": "exampleSampler",
        "source": "exampleImage"
    }
},
"samplers": {
    "exampleSampler": {
        "magFilter": 9729,
        "minFilter": 9987,
        "wrapS": 10497,
        "wrapT": 10497
    }
},
"images": {
    "exampleImage": {
        "uri": "exampleImageFile.png"
    }
},
```

The `texture` itself uses IDs to refer to one `sampler` and one `image`. The most important part here is the reference to the `image`: It contains a URI that links to the actual image file that will be used for the texture. Information about how to read this image data can be found in the section about [Image data in `images`](gltfTutorial_002_BasicGltfStructure.md#image-data-in-images).
