Previous: [Meshes](gltfTutorial_008_Meshes.md) | [Table of Contents](README.md) | Next: [Simple Material](gltfTutorial_009a_SimpleMaterial.md)

# Materials

## Introduction

The purpose of glTF is to define a transmission format for 3D assets. As shown in the previous sections, this includes information about the scene structure and the geometric objects that appear in the secene. But a glTF asset can also contain information about the *appearance* of the objects - that is, how these objects should be rendered on the screen.

There are several well-known parameters that are commonly used to describe a material in rendering applications and graphics APIs:

* The **diffuse** color: The main color of the material, which is often defined by a texture
* The **specular** color: The color of specular highlights
* The **shininess** factor: A value that defines the shininess of the object, influencing the size of the specular highlights
* The **emissive** color: The color of the light that is emitted by the object
* ...

Many file formats contain this information in one or the other form. For example, [Wavefront OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file) files are combined with `MTL` files that contain exactly these parameters. Renderers can read this information and render the objects accordingly.

However, one of the goals of glTF was to *not* constrain the rendering to one simple, fixed material model. Instead, it should support arbitrary materials models. This is an ambitious goal: There are unlimited degrees of freedom for renderers to implement different material models. To retain this flexibility, the glTF specification of materials can be considered as a very generic description of rendering processes. On the lowest level, it encapsulates the actual GLSL shader programs, and thus can cover nearly all imaginable rendering pipelines.

This flexibility comes at a certain cost. Several elements in the glTF asset have to be combined properly by the renderer to exploit this flexibility. The following sections will break down these elements and describe how they are combined and interpreted to finally render a glTF asset. This will start with a basic example of a simple material, giving an overview of the elements that a material definition consists of. Afterwards, these elements will be explained in more detail, showing how they serve as a basis for building advanced materials.

- [A simple material](gltfTutorial_009a_SimpleMaterial.md)
- [Programs and shaders](gltfTutorial_009b_ProgramsShaders.md)
- [Materials and techniques](gltfTutorial_009c_MaterialsTechniques.md)
- [An advanced material](gltfTutorial_009d_AdvancedMaterial.md)



Previous: [Meshes](gltfTutorial_008_Meshes.md) | [Table of Contents](README.md) | Next: [Simple Material](gltfTutorial_009a_SimpleMaterial.md)
