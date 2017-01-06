Previous: [Meshes](gltfTutorial_009_Meshes.md) | [Table of Contents](README.md) | Next: [Simple Material](gltfTutorial_011_SimpleMaterial.md)

# Materials

## Introduction

The purpose of glTF is to define a transmission format for 3D assets. As shown in the previous sections, this includes information about the scene structure and the geometric objects that appear in the scene. But a glTF asset can also contain information about the *appearance* of the objects; that is, how these objects should be rendered on the screen.

There are several well-known parameters that are commonly used to describe a material in rendering applications and graphics APIs:

* The **diffuse** color: The color of the light that is diffusely reflected by the material. In the simplest form, this can be imagined as the "main" color that the material appears to have. It is often defined by a texture.
* The **specular** color: The color of reflected highlights.
* The **shininess** factor: A value that defines the shininess of the object, influencing the size of the specular highlights.
* The **emissive** color: The color of the light that is emitted by the object
* ...

Many file formats contain this information in some form. For example, [Wavefront OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file) files are combined with `MTL` files that contain exactly these parameters. Renderers can read this information and render the objects accordingly.

However, one of the goals of glTF was to *not* constrain the rendering to one simple, fixed material model. Instead, it should support arbitrary materials models. This is an ambitious goal: there are unlimited degrees of freedom for renderers to implement different material models. To retain this flexibility, the glTF specification of materials can be considered a very generic description of rendering processes.

This flexibility comes at a certain cost. Several elements in the glTF asset have to be combined properly by the renderer to exploit this flexibility. Here is a quick summary of the elements of a glTF asset that are used for defining the appearance of a rendered object:

- A [`material`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-material) can be assigned to a `mesh.primitive`, so that the primitive is rendered with this material. A material can be considered an "instance" of a `technique`.
- A [`technique`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-technique) is the core element describing the appearance of rendered objects in a glTF asset. It is an abstract definition of a rendering process and serves as a "template" for `material` objects.
- A [`program`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-program) is the actual *implementation* of a rendering process for a `technique`. It consists of multiple `shader` objects.
- A [`shader`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-shader) is a basic building block for the implementation of a renderer in WebGL or OpenGL.

The following sections will show how these elements are combined and interpreted to finally render a glTF asset:

- [A Simple Material](gltfTutorial_011_SimpleMaterial.md)
- [Programs and Shaders](gltfTutorial_012_ProgramsShaders.md)
- [Materials and Techniques](gltfTutorial_013_MaterialsTechniques.md)
- [An Advanced Material](gltfTutorial_014_AdvancedMaterial.md)
- [A Simple Texture](gltfTutorial_015_SimpleTexture.md)
- [Textures, Images, and Samplers](gltfTutorial_016_TexturesImagesSamplers.md)

We'll start with a simple material, giving an example of the elements that a material definition consists of, and how these elements are represented in the glTF JSON. Afterwards, these elements will be explained in more detail, showing how they serve as a basis for building advanced materials.


Previous: [Meshes](gltfTutorial_009_Meshes.md) | [Table of Contents](README.md) | Next: [Simple Material](gltfTutorial_011_SimpleMaterial.md)
