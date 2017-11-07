Previous: [Simple Morph Target](gltfTutorial_021_SimpleMorphTarget.md) | [Table of Contents](README.md)

# Morph Targets

The example in the previous section contains a mesh that consists of a single triangle with two morph targets:

```javascript
{
  "meshes":[
    {
      "primitives":[
        {
          "attributes":{
            "POSITION":1
          },
          "targets":[
            {
              "POSITION":2
            },
            {
              "POSITION":3
            }
          ],
          "indices":0
        }
      ],
      "weights":[
        1.0,
        0.5
      ]
    }
  ],
```


The actual base geometry of the mesh, namely the triangle geometry, is defined by the `mesh.primitive` attribute called `"POSITIONS"`. Initially, this triangle has the following geometry:

<p align="center">
<img src="images/TODO.png" /><br>
<a name="simpleMorphInitial-png"></a>Image 22a: The initial triangle geometry
</p>

The morph targets of the `mesh.primitive` are dictionaries that map the attribute name `"POSITIONS"` to `accessor` objects that contain the *displacements* for each vertex:

<p align="center">
<img src="images/TODO.png" /><br>
<a name="simpleMorphDisplacements-png"></a>Image 22b: The displacements that are stored in the morph targets
</p>



Previous: [Simple Morph Target](gltfTutorial_021_SimpleMorphTarget.md) | [Table of Contents](README.md)
