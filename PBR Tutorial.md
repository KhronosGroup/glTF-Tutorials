# Physically Based Rendering: From Theory to Practice
___

## What is PBR?
Physically-based rendering refers to techniques that attempt to simulate light in order to render photorealistic images. As indicated by the name, these techniques focus on our understanding of physics to model how light interacts with surfaces that have different physical properties. Since these interactions happen on a very fine level, PBR techniques often use statistical models to add realism and complexity to renders.

PBR has been around for several years now, but was initially too computationally expensive to be a viable option for real-time applications. However, with the continuous advancement of computing power, it has increasingly become an industry standard in real-time graphics. In fact, much of the real-time software we see today such as Unreal Engine 4, Unity 5, Frostbite, and many others use physically-based rendering techniques to provide their users with the ability to create highly realistic 3D scenes.

![Marmoset -- PBR](http://www.marmoset.co/wp-content/uploads/header01.jpg)

## How do we model light-object interactions in PBR?
The most central physics law to PBR is the law of conservation of energy. This law states that the total amount of energy within an isolated system remains constant, but how does this relate to rendering? In PBR, radiance is the energy that is conserved, meaning the amount of incoming light at any point in the scene is equal to the sum of the reflected, transmitted, and absorbed light at that point.

Within any environment, it is easy to see several examples of complicated surfaces that seem to interact with light differently. For example, mirrors reflect perfect images, plastics are shiny, and painted walls are matte. All of these complicated interactions can be modeled by considering general mathematical functions called **Bidirectional Scattering Distribution Functions** (**BSDFs**). These functions describe how light scatters upon contact with a surface based on the properties that surface holds. More specifically, they tell the user how much of the incident light is scattered in a specific outgoing direction.

BSDF sounds like a very complicated term for what it actually means, so let’s break it up and explain its parts...  
* **Bidirectional** refers to the notion that at any point on a surface, light comes in and light goes out. This means “bidirectional” describes the binary nature of how light interacts with a point.
* **Scatter** describes that light coming from one direction onto a surface can end up splitting into a range of directions. For example, light can either scatter by being reflected from or transmitted through the surface in certain directions.
* Finally, the details for how light scatters can be described using **distribution functions**, which entail how light is likely to be distributed in certain directions based on the physical properties of the surface. This can be anything from an equal scatter in all directions to a perfect reflection in a single direction.

To help better understand the kinds of BSDFs that occur, we can consider two general types...
* **BRDFs** (Bidirectional Reflectance Distribution Functions) specifically correspond to BSDFs that describe how light is _reflected_ from a surface. This reflected light refers to the colors we see coming directly from a surface. At this point, it is normal to ask something along the lines of the following: If I shine a white light at a banana, why does it appear yellow instead of white? This is because not all light is just reflected from a surface. While surfaces reflect light of certain colors (wavelengths), they absorb or transmit the remaining energy. For bananas, red and green light is reflected while blue light is absorbed.
* **BTDFs** (Bidirectional Transmittance Distribution Functions) specifically correspond to BSDFs that describe how light is _transmitted_ through a surface. This can be seen in examples such as glass and plastics where we can see light that has traveled through the surface.

There exist other types of density functions that account for effects such as subsurface scattering (the effect in which light enters a material and bounces around before exiting again in some other position and direction). However, these models are outside of the scope of tutorial and will not be discussed.

## What are the reflection models?
There are four general surface types with reflection distribution functions (BRDFs) that describe the probability that light scatters in all directions:
* **Diffuse** – surfaces that scatter light equally in all directions (ex: matte paint)
* **Glossy specular** – surfaces that scatter light preferentially in a set of reflected directions and show blurry reflections (ex: plastic)
* **Perfect specular** – surfaces that scatter light in a single outgoing direction such that the angle of incident light is equal to the outgoing light with respect to the surface normal (ex: mirrors)
* **Retro-reflective** – surfaces that scatter light primarily back along the incident direction of the light source (ex: velvet)

![Reflectance Models](https://elementalray.files.wordpress.com/2013/01/dgs.png)
![Retroreflectance](http://www.nextstagepro.com/images/04_retroreflecdiagram.png)

However, it is highly unlikely that a surface in reality will follow only one of these models. Because of this, most materials can be modeled as a complex mix of these.

For each of these types of reflection, the distributions can be isotropic or anisotropic.
* **Isotropic** – The amount of light reflected doesn’t change at a point when rotating the object about its normal (ex: most surfaces).
* **Anisotropic** – The amount of light varies at a point as the object is rotated about its normal. This occurs because the small bumps and grooves on the surface are mostly oriented in the same direction instead of randomly, which results in elongated and blurry reflections (ex: brushed metal).

## What about BTDFs?
The types of reflection distributions also apply to transmission, but conversely discuss how light travels after passing through a surface. The direction light travels after passing through the material is often dependent on the properties of the material itself.

To discuss how this differs from reflection, consider the specific case of perfect specular transmission. For perfect specular transmission, the angle at which the light continues to propagate depends on the **index of refraction** of the medium. This follows **Snell’s Law**…
>$$n_1\theta_1 = n_2\theta_2$$

where $$n$$ is the index of refraction and $$\theta$$ is the angle of the light with respect to the normal. 

This is unlike perfect specular reflection where the incident angle will always be equal to the outgoing angle.

## Are all surfaces the same roughness?
It is very useful to be able to show the roughness or smoothness of a surface without having to directly create the geometry or provide a bump map. Instead, surfaces can be modeled as a collection of small **microfacets** where the more rough a surface is, the more microfacets it has. These microfacets can be thought of as small ridges on the surface of an object, varying the surface normal on a very fine level, which adds a lot of realism to rendered images. The distribution of microfacets on a surface can be described using a statistical model, examples of which include the Oren-Nayar model, the Torrance-Sparrow model, and the Blinn Microfacet Distribution model.

With knowledge of these microfacets, we can simulate some interesting geometric interactions between light and adjacent ridges. Consider the following three scenarios:
1. An adjacent microfacet can block the light reflected from another, causing **masking**.
2. An adjacent microfacet can block incoming light, causing **shadowing**.
3. An adjacent microfacet can reflect light coming from the reflection of another, causing **interreflection**.

Simulating these three phenomena can help augment the realism of roughness on a surface.

## How much light is reflected or transmitted?
It is important for physically based renderers to know how much light is reflected or transmitted on a surface. These amounts are directly related to each other and described by the **Fresnel equations**. The equations are described for two types of media, _dielectrics_ and _conductors_. 
* **Dielectrics**: These are approximated using the following terms...
    >$$r_{\parallel} = \frac{n_tcos\theta_i - n_icos\theta_t}{n_tcos\theta_i + n_icos\theta_t}$$

    >$$r_{\perp} = \frac{n_icos\theta_i - n_tcos\theta_t}{n_icos\theta_i + n_tcos\theta_t}$$

    where $$r_{\parallel}$$ is the Fresnel reflectance for parallel polarized light and $$r_{\perp}$$ is the reflectance for perpendicular polarized light. The subscripts correspond to incident ($$i$$) and transmitted ($$t$$) directions.
For unpolarized light, Fresnel reflectance can be modeled as $$F_r = \frac{1}{2}(r_{\parallel}^2 + r_{\perp}^2)$$.
Due to conservation of energy, Fresnel transmittance can be modeled as $$F_t = 1 - F_r$$.

* **Conductors**: Unlike dielectrics, conductors don’t transmit light. Instead, they absorb some of the incident light, which gets transferred into heat. The amount of absorbed light is described using an **absorption coefficient**, $$k$$, for the conductor.
These are approximated using the following terms...
    >$$r_{\parallel}^2 = \frac{(n^2+k^2)cos\theta_i^2 - 2ncos\theta_i + 1}{(n^2+k^2)cos\theta_i^2 + 2ncos\theta_i + 1}$$

    >$$r_{\perp}^2 = \frac{(n^2+k^2)cos\theta_i^2 - 2ncos\theta_i + cos\theta_i^2}{(n^2+k^2)cos\theta_i^2 + 2ncos\theta_i + cos\theta_i^2}$$

    and Fresnel reflectance is modeled as $$F_r = \frac{1}{2}(r_{\parallel}^2 + r_{\perp}^2)$$.

## What is a material?
Materials are high-level descriptions used to model surfaces specified by mixtures of BRDFs and BTDFs. These BSDFs are specified as parameters that help frame the visual properties of the material. For example, we can describe a matte material by providing a diffuse reflection value to describe how light interacts with the surface and a scalar roughness value to describe its texture. To move from a matte to a plastic, we could simply add a glossy specular reflection value to the matte material to recreate the specular highlights that can be seen on plastics.

Here is a list of some common materials and what their descriptions might entail...
* Glass -- Specular reflection and transmission
* Mirror -- Perfect specular reflection
* Metal -- Fresnel equations for conductors
* Translucent -- Diffuse reflection, glossy specular reflection, and transmission

## Where does glTF come in?
As you may know, glTF is a 3D file format that is increasingly becoming a standard in the CG community. It has the capability to encode everything in a 3D scene including meshes, cameras, lights, joint hierarchies, samples, and materials. This means that glTF can give many software applications, such as game engines and modeling software, the capability of importing and exporting entire scenes by using a single file type. However, with the rise in demand for PBR materials within these applications, it has become clear that there is no consistency in the language used to describe these materials. For example, the parameters used in Unreal Engine are base color, roughness, metallic, and specular while Marmoset uses albedo, microsurface, and reflectivity. This creates a language barrier between artists and developers who use different applications and makes it difficult for them to switch frequently between them. With this in mind, glTF can become the meeting point for all of these applications and unify the language in which the CG community uses to discuss physically-based materials. 

## References
* PBRT
* http://www.cs.cornell.edu/courses/cs6630/2012sp/notes/03brdf.pdf
