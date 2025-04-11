Previous: [Simple Material](gltfTutorial_011_SimpleMaterial.md) | [Table of Contents](README.md) | Next: [Simple Texture](gltfTutorial_013_SimpleTexture.md)

# Textures, Images, and Samplers

Textures are an important aspect of giving objects a realistic appearance. They make it possible to define the main color of the objects, as well as other characteristics that are used in the material definition in order to precisely describe what the rendered object should look like.

A glTF asset may define multiple [`texture`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-texture) objects, which can be used as the textures of geometric objects during rendering, and which can be used to encode different material properties. Depending on the graphics API, there may be many features and settings that influence the process of texture mapping. Many of these details are beyond the scope of this tutorial. There are dedicated tutorials that explain the exact meaning of all the texture mapping parameters and settings; for example, on [webglfundamentals.org](https://webglfundamentals.org/webgl/lessons/webgl-3d-textures.html),  [open.gl](https://open.gl/textures), and others. This section will only summarize how the information about textures is encoded in a glTF asset.

There are three top-level arrays for the definition of textures in the glTF JSON. The `textures`, `samplers`, and `images` dictionaries contain  [`texture`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-texture),  [`sampler`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#_texture_sampler), and [`image`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-image) objects, respectively. The following is an excerpt from the [Simple Texture](gltfTutorial_013_SimpleTexture.md) example, which will be presented in the next section:

```javascript
"textures": [
  {
    "source": 0,
    "sampler": 0
  }
],
"images": [
  {
    "uri": "testTexture.png"
  }
],
"samplers": [
  {
     "magFilter": 9729,
     "minFilter": 9987,
     "wrapS": 33648,
     "wrapT": 33648
   }
],
```

The `texture` itself uses indices to refer to one `sampler` and one `image`. The most important element here is the reference to the `image`. It contains a URI that links to the actual image file that will be used for the texture. Information about how to read this image data can be found in the section about [image data in `images`](gltfTutorial_002_BasicGltfStructure.md#image-data-in-images).

The next section will show how such a texture definition may be used inside a material. 

Previous: [Simple Material](gltfTutorial_011_SimpleMaterial.md) | [Table of Contents](README.md) | Next: [Simple Texture](gltfTutorial_013_SimpleTexture.md)
