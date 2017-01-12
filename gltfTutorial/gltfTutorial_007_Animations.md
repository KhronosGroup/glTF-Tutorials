Previous: [Simple Animation](gltfTutorial_006_SimpleAnimation.md) | [Table of Contents](README.md) | Next: [Simple Meshes](gltfTutorial_008_SimpleMeshes.md)

# Animations

As shown in the [Simple Animation](gltfTutorial_005_SimpleAnimation.md) example, an [`animation`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-animation) can be used to describe how the `translation`, `rotation`, or `scale` properties of nodes change over time.

The following is another example of an `animation`. This time, the animation contains two channels. One animates the translation, and the other animates the rotation of a node:

```javascript
"animation0": {
  "channels": [
    {
      "sampler": "translationSampler",
       "target": {
        "id": "node0",
        "path": "translation"
      }
    },
    {
      "sampler": "rotationSampler",
      "target": {
        "id": "node0",
        "path": "rotation"
      }
    }
  ],
  "samplers": {
    "translationSampler": {
      "input": "TIMEAccessor",
      "interpolation": "LINEAR",
      "output": "translationAccessor"
    },
    "rotationSampler": {
      "input": "TIMEAccessor",
      "interpolation": "LINEAR",
      "output": "rotationAccessor"
    }
  }
}
```


## Animation samplers

The `samplers` dictionary contains [`animation.sampler`](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#reference-animation.sampler) objects that define how the values that are provided by the accessors have to be interpolated between the key frames, as shown in Image 7a.

<p align="center">
<img src="images/animationSamplers.png" /><br>
<a name="animationSamplers-png"></a>Image 7a: Animation samplers.
</p>

In order to compute the value of the translation for the current animation time, the following algorithm can be used:

* Let the current animation time be given as `currentTime`.
* Compute the next smaller and the next larger element of the `TIMEAccessor`:

    `previousTime` = The largest element from the `TIMEAccessor` that is smaller than the `currentTime`

    `nextTime`  = The smallest element from the `TIMEAccessor` that is larger than the `currentTime`

* Obtain the elements from the `translationAccessor` that correspond to these times:

    `previousTranslation` = The element from the `translationAccessor` that corresponds to the `previousTime`

    `nextTranslation` = The element from the `translationAccessor` that corresponds to the `nextTime`

* Compute the interpolation value. This is a value between 0.0 and 1.0 that describes the *relative* position of the `currentTime`, between the `previousTime` and the `nextTime`:

    `interpolationValue = (currentTime - previousTime) / (nextTime - previousTime)`

* Use the interpolation value to compute the translation for the current time:

    `currentTranslation = previousTranslation + interpolationValue * (nextTranslation - previousTranslation)`


### Example:

Imagine the `currentTime` is **1.2**. The next smaller element from the `TIMEAccessor` is **0.8**. The next larger element is **1.6**. So

    previousTime = 0.8
    nextTime     = 1.6

The corresponding values from the `translationAccessor` can be looked up:

    previousTranslation = (14.0, 3.0, -2.0)
    nextTranslation     = (18.0, 1.0,  1.0)

The interpolation value can be computed:

    interpolationValue = (currentTime - previousTime) / (nextTime - previousTime)
                       = (1.2 - 0.8) / (1.6 - 0.8)
                       = 0.4 / 0.8         
                       = 0.5

From the interpolation value, the current translation can be computed:

    currentTranslation = previousTranslation + interpolationValue * (nextTranslation - previousTranslation)
                       = (14.0, 3.0, -2.0) + 0.5 * ( (18.0, 1.0,  1.0) - (14.0, 3.0, -2.0) )
                       = (14.0, 3.0, -2.0) + 0.5 * (4.0, -2.0, 3.0)
                       = (16.0, 2.0, -0.5)

So when the current time is **1.2**, then the `translation` of the node is **(16.0, 2.0, -0.5)**.



## Animation channels

The animations contain an array of [`animation.channel`](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#reference-animation.channel) objects. The channels establish the connection between the input, which is the value that is computed from the sampler, and the output, which is the animated node property. Therefore, each channel refers to one sampler, using the ID of the sampler, and contains an [`animation.channel.target`](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#reference-animation.channel.target). The `target` refers to a node, using the ID of the node, and contains a `path` that defines the property of the node that should be animated. The value from the sampler will be written into this property.

In the example above, there are two channels for the animation. Both refer to the same node. The path of the first channel refers to the `translation` of the node, and the path of the second channel refers to the `rotation` of the node. So all objects (meshes) that are attached to the node will be translated and rotated by the animation, as shown in Image 7b.

<p align="center">
<img src="images/animationChannels.png" /><br>
<a name="animationChannels-png"></a>Image 7b: Animation channels.
</p>


Previous: [Simple Animation](gltfTutorial_006_SimpleAnimation.md) | [Table of Contents](README.md) | Next: [Simple Meshes](gltfTutorial_008_SimpleMeshes.md)
