Previous: [Simple Texture](gltfTutorial_013_SimpleTexture.md) | [Table of Contents](README.md) | Next: [Simple Cameras](gltfTutorial_015_SimpleCameras.md)

# An Advanced Material

The [Simple Texture](gltfTutorial_013_SimpleTexture.md) example in the previous section showed a material for which the "base color" was defined using a texture. But in addition to the base color, there are other properties of a material that may be defined via textures. These properties have already been summarized in the [Materials](gltfTutorial_010_Materials.md) section:

- The *base color*,
- The *metallic* value,
- The *roughness* of the surface,
- The *emissive* properties,
- An *occlusion* texture, and
- A *normal map*.


The effects of these properties cannot properly be demonstrated with trivial textures. Therefore, they will be shown here using one of the official Khronos PBR sample models, namely, the [WaterBottle](https://github.com/KhronosGroup/glTF-Sample-Models/tree/master/2.0/WaterBottle) model. Image 14a shows an overview of the textures that are involved in this model, and the final rendered object:

<p align="center">
<img src="images/materials.png" /><br>
<a name="cameras-png"></a>Image 14a: An example of a material where the surface properties are defined via textures.
</p>

Explaining the implementation of physically based rendering is beyond the scope of this tutorial. The official Khronos [glTF Sample Viewer](https://github.com/KhronosGroup/glTF-Sample-Viewer) contains a reference implementation of a PBR renderer based on WebGL, and provides implementation hints and background information. The following images mainly aim at demonstrating the effects of the different material property textures, under different lighting conditions.

Image 14b shows the effect of the roughness texture: the main part of the bottle has a low roughness, causing it to appear shiny, compared to the cap, which has a rough surface structure.

<p align="center">
<img src="images/advancedMaterial_roughness.png" /><br>
<a name="advancedMaterial_roughness-png"></a>Image 14b: The influence of the roughness texture.
</p>

Image 14c highlights the effect of the metallic texture: the bottle reflects the light from the surrounding environment map.

<p align="center">
<img src="images/advancedMaterial_metallic.png" /><br>
<a name="advancedMaterial_metallic-png"></a>Image 14c: The influence of the metallic texture.
</p>

Image 14d shows the emissive part of the texture: regardless of the dark environment setting, the text, which is contained in the emissive texture, is clearly visible.

<p align="center">
<img src="images/advancedMaterial_emissive.png" /><br>
<a name="advancedMaterial_emissive-png"></a>Image 14d: The emissive part of the texture.
</p>

Image 14e shows the part of the bottle cap for which a normal map is defined: the text appears to be embossed into the cap. This makes it possible to model finer geometric details on the surface, even though the model itself only has a very coarse geometric resolution.

<p align="center">
<img src="images/advancedMaterial_normal.png" /><br>
<a name="advancedMaterial_normal-png"></a>Image 14e: The effect of a normal map.
</p>

Together, these textures and maps allow modeling a wide range of real-world materials. Thanks to the common underlying PBR model - namely, the metallic-roughness model - the objects can be rendered consistently by different renderer implementations.



Previous: [Simple Texture](gltfTutorial_013_SimpleTexture.md) | [Table of Contents](README.md) | Next: [Simple Cameras](gltfTutorial_015_SimpleCameras.md)
