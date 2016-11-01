# Scenes, nodes, cameras and animations

## Scenes

The [`scene`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-scene) is the entry point for the description of the scene that is stored in the glTF. When parsing a glTF JSON file, the traversal of the scene structure will start here.

There may be multiple scenes stored in one glTF file, but in many cases, there will only be a single scene, which then also is the default scene. Each scene contains an array of `nodes`, which are the IDs of the root nodes of the scene graphs. Again, there may be multiple root nodes, forming different hierarchies, but in many cases, the scene will have a single root node.

So the most simple scene description may look as follows:

```javascript
"scene" : "defaultSceneId",
"scenes" : {
    "defaultSceneId": {
        "nodes": [
            "rootNodeId",
        ],
    }
},
"nodes" : {
    "rootNodeId": { ... }
}
```


## Nodes forming the scene graph

Each [`node`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-node) is one element of a hierarchy of nodes, and together they define the structure of the scene as a scene graph.  

![Scene graph](images/sceneGraph.png)

Each of the nodes that are given in the `scene` can be traversed, recursively visiting all its children, to process all elements that are attached to the nodes. The simplified pseudocode for this traversal may look as follows:

```
traverse(node) {
    processCamera(node.camera);
    processMeshes(node.meshes);
    processOtherElements(node); // Skin, joint, skeleton - discussed later
    for each (child in node.children) {
        traverse(child);
    }
}
```

In practice there will some additional information be required for the traversal: The processing of some elements that are attached to nodes will require information about *which* node they are attached to. Additionally, the information about the transforms of the nodes have to be accumulated during the traversal. This will be detailed in the following section.


### Local and global transforms

Each node can have a transform. Such a transform will usually define a translation, rotation or a scaling. This transform will be applied to all elements that are attached to the node itself and to all its child nodes. The hierarchy of nodes thus allows to structure the translations, rotations and scalings that are applied to the scene elements.


#### Local transforms of nodes

There are different possible representations for the local transform of a node. The transform can be given directly by the `matrix` property of the node. This is an array of 16 floating point numbers that describe the matrix in column-major order:

```javascript
"node0": {
    "matrix": [
        1.0,    0.0,    0.0,    0.0,
        0.0,    0.866,  0.5,    0.0,
        0.0,    0.5,    0.866,  0.0,
        3.0,    4.0,    5.0,    1.0
    ]
}    
```

The matrix defined here is

![Matrix](images/matrix.png)

> **Implementation note:**

> The matrix shown above *seems* to be transposed compared to what is written in the JSON. However, matrices in OpenGL are *always* stored in column-major order. All OpenGL functions (and nearly all OpenGL-related matrix utility libraries) are implemented accordingly, and allow creating the appropriate column-major matrix directly from an array.

The transform of a node can also be given using the `transform`, `rotation` and `scale` properties of a node - which is sometimes abbreviated as *TRS*:  

```javascript
"node0": {
    "translation": [ 10.0, 20.0, 30.0 ],
    "rotation": [ 0.7071, 0.0, 0.0, 0.7071 ],
    "scale": [ 2.0, 1.0, 0.5 ]
}
```

This representation can be imagined as simply performing the transformations, one after the other. The `translation` just contains the translation in x-, y- and z-direction. The `scale` contains the scaling factors along the x-, y- and z-axis. The trickiest part is the `rotation`, which is given as a [quaternion](https://en.wikipedia.org/wiki/Quaternion). The mathematical background of quaternions is beyond the scope of this tutorial. For now, the most important information is that a quaternion is a compact representation of a rotation about an arbitrary angle and around an arbitrary axis.

Each of these properties can be used to create a matrix, and the product of these matrices then is the local transform of the node. It is important to perform the multiplication of these matrices in the right order. The local transform matrix always has to be computed as `M = T * R * S`, where `T` is the matrix for the `translation` part, `R` is the matrix for the `rotation` part, and `S` is the matrix for the `scale` part. So the the pseudocode for the computation is

```
translationMatrix = createTranslationMatrix(node.translation);
rotationMatrix = createRotationMatrix(node.rotation);
scaleMatrix = createScaleMatrix(node.scale);
localTransform = translationMatrix * rotationMatrix * scaleMatrix;
```


> **Implementation note:**

> Most matrix libraries contain functions for directly creating matrices from these properties. The translation matrix is created from an identity matrix where the last column in filled with the `translation` elements. Similarly, the scale matrix is created from an identity matrix where the diagonal elements are replaced with the `scale` values. The computation of the matrix for a given `rotation` quaternion is not so trivial, but usually offered via utility functions:

> The JavaScript [glMatrix](http://glmatrix.net/) library has a [`fromQuat`](http://glmatrix.net/docs/mat4.html#.fromQuat) function that allows creating a 4x4 matrix from a quaternion.

> The Java library [JOML](https://github.com/JOML-CI/JOML) contains different methods, for example, [`rotate()`](https://joml-ci.github.io/JOML/apidocs/org/joml/Matrix4f.html#rotate-org.joml.Quaternionf-), to create a 4x4 matrix from a quaternion.

> The C++ [glm](glm.g-truc.net/) library has a [`mat4_cast`](https://glm.g-truc.net/0.9.7/api/a00177.html#ga14bb2ddf028c91542763eb6f2bba47ef) that converts a quaternion into the corresponding 4x4 matrix.


When any of the three properties is not given, then the identity matrix will be used. Similarly, when a node does neither contain a `matrix` property nor TRS-properties, then its local transform will be the identity matrix.



#### Global transforms of nodes

Regardless of the representation in the JSON file, the local transform of a node can be stored as a 4x4 matrix. The *global* transform of a node is given by the product of all local transforms on the path from the root to the respective node:

                         local transform      global transform
    root                 M                    M
     +- nodeA            A                    M*A
         +- nodeB        B                    M*A*B
         +- nodeC        C                    M*A*C

It is important to point out that these global transforms can *not* be computed only once after the file was loaded. Later, it will be shown how *animations* may modify the local transforms of individual nodes. And these modifications will affect the global transforms of all descendant nodes. Therefore, when the global transform of a node is required, it has to be computed directly from the current local transforms of all nodes. Alternatively, and as a potential performance improvement, an implementation could cache the global transforms, detect changes in the local transforms of ancestor nodes, and update the global transforms only when necessary. The different implementation options for this will depend on the programming language and the requirements for the client application, and thus are beyond the scope of this tutorial.




## Cameras

Each [`node`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-node) may contain the ID of a [`camera`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-camera). The position and orientation of the camera is derived from the global transform of the node.

There are two kinds of cameras: [`orthographic`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-camera.orthographic) cameras and [`perspective`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-camera.perspective) cameras. The parameters that are contained in the different cameras can be used to create the *camera matrix*. Explaining the details of cameras, matrices, viewing and projections is beyond the scope of this tutorial. The WebGL API documentation contains a dedicated section called [WebGL model view projection](https://developer.mozilla.org/en/docs/Web/API/WebGL_API/WebGL_model_view_projection) that contains background information and links to further tutorials.     

> **Implementation note:**

> In many environments, there are utility methods for creating the camera matrix based on the parameters that are contained in the perspective or orthographic camera of glTF.  

> The JavaScript [glMatrix](http://glmatrix.net/) library has an [`ortho`](http://glmatrix.net/docs/mat4.html#.ortho) and a [`perspective`](http://glmatrix.net/docs/mat4.html#.perspective) function for filling the camera matrix with the given parameters.

> The Java library [JOML](https://github.com/JOML-CI/JOML) contains similar [`setOrtho()`](https://joml-ci.github.io/JOML/apidocs/org/joml/Matrix4f.html#setOrtho-float-float-float-float-float-float-) and [`setPerspective()`](https://joml-ci.github.io/JOML/apidocs/org/joml/Matrix4f.html#setPerspective-float-float-float-float-boolean-) methods.

> The [glm](glm.g-truc.net/) library that is commonly used in C++ offers [`ortho`](https://glm.g-truc.net/0.9.7/api/a00174.html#ga65280251de6e38580110a0577a43d8f8) and [`projection`](https://glm.g-truc.net/0.9.7/api/a00174.html#gac3613dcb6c6916465ad5b7ad5a786175) functions as well.

> In the old, fixed-function OpenGL, there have been the [`glOrtho`](https://www.opengl.org/sdk/docs/man2/xhtml/glOrtho.xml) and [`gluPerspective`](https://www.opengl.org/sdk/docs/man2/xhtml/gluPerspective.xml) functions that applied the matrices directly on top of the matrix stack.

What may be important to note is that the camera itself in glTF is assumed to be in a "default" orientation. This is the same configuration that the camera has by default in OpenGL: The eye point of the camera is at the origin, and the viewing direction is along the negative z-axis. All transformations of the camera are only determined by the global transform of the `node` that refers to the camera.

There may be multiple cameras defined in the JSON part of a glTF. However, there is no "default" camera. Instead, the client application has to keep track of the currently active camera. The client application may, for example, offer a dropdown-menu that allows selecting the active camera, and thus, to quickly switch between predefined view configurations. With a bit more implementation effort, the client application can also define an own camera and interaction patterns for the camera control (e.g. zooming with the mouse wheel). However, the logic for the navigation and interaction has to be implemented solely by the client application in this case.



## Animations

As mentioned above, in the section about **Local and global transforms**, each node can contain a local transform. This local transform can either be given as the `node.matrix`, or using the `translation`, `rotation` and `scale` properties of the node. An [`animation`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-animation) may now be used to describe how the `translation`, `rotation` or `scale` of a node changes over time.

The following is an example of an `animation` that animates the translation and rotation of a node:

```javascript
"animation0": {
    "parameters": {
        "TIME": "accessorForTIME",
        "nodeTranslation": "accessorForTranslation",
        "nodeRotation": "accessorForRotation"
    },
    "samplers": {
        "translationSampler": {
            "input": "TIME",
            "interpolation": "LINEAR",
            "output": "nodeTranslation"
        },
        "rotationSampler": {
            "input": "TIME",
            "interpolation": "LINEAR",
            "output": "nodeRotation"
        }
    },
    "channels": [
        {
            "sampler": "translationSampler",
             "target": {
                "id": "animatedNodeId",
                "path": "translation"
            }
        },
        {
            "sampler": "rotationSampler",
            "target": {
                "id": "animatedNodeId",
                "path": "rotation"
            }
        }
    ]
}
```

It can be seen that the animation contains three types of objects: Animation `parameters`, `samplers` and `channels`.

### Animation parameters


The dictionary of animation `parameters` summarizes the input data of the animation. It contains one [`accessor`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-accessor) for each parameter. The details of accessors will be explained in a later the section about [Buffers, BufferViews and Accessors](gltfTutorial_007_BuffersBufferViewsAccessors.md). For now, an accessor can be imagined as an abstract source of arbitrary data: An accessor may provide the time stamps of the key frames of the animation, and the values that the animated properties have at these key frames.

  ![AnimationParameters](images/animationParameters.png)

In the given example, there is one accessor for the `TIME` parameter of the animation. It provides the time, in seconds, of the key frames of the animation. The accessor for the translation provides one 3D vector for each key frame, which describes the translation that the node has at the given time. Similarly, the accessor for the rotation provides the four values that are used to create the quaternion describing the rotation of the node at the given time.


### Animation samplers

The `samplers` dictionary contains [`animation.sampler`](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#reference-animation.sampler) objects that define how the values that are provided by the accessors have to be interpolated between the key frames:

![AnimationSamplers](images/animationSamplers.png)

In order to compute the value of the translation for the current animation time, the following algorithm can be used:

* Let the current animation time be given as `currentTime`
* Compute the next smaller and the next larger element of the `TIME` accessor:

    `previousTime` = The largest element from the `TIME` accessor that is smaller than the `currentTime`

    `nextTime`  = The smallest element from the `TIME` accessor that is larger than the `currentTime`

* Obtain the elements from the `translation` accessor that correspond to these times:

    `previousTranslation` = The element from the `translation` accessor that corresponds to the `previousTime`

    `nextTranslation` = The element from the `translation` accessor that corresponds to the `nextTime`

* Compute the interpolation value. This is a value betwenn 0.0 and 1.0, that describes the *relative* position of the `currentTime`, between the `previousTime` and the `nextTime`:

    `interpolationValue = (currentTime - previousTime) / (nextTime - previousTime)`

* Use the interpolation value to compute the translation for the current time:

    `currentTranslation = previousTranslation + interpolationValue * (nextTranslation - previousTranslation)`


#### Example:

Imagine the `currentTime` is **1.2**. The next smaller element from the `TIME` accessor is **0.8**. The next larger element is **1.6**. So

    previousTime = 0.8
    nextTime     = 1.6

The corresponding values from the `translation` accessor can be looked up:

    previousTranslation = (14.0, 3.0, -2.0)
    nextTranslation     = (18.0, 1.0,  1.0)

The interpolation value can be computed:

    interpolationValue = (currentTime - previousTime) / (nextTime - previousTime)
                       = (1.2 - 0.8) / (1.6 - 0.8)
                       = 0.4 / 0.8         
                       = 0.5

From the interpolation value, the current translation can be computed:

    currentTranslation = previousTranslation + interpolationValue * (nextTranslation - previousTranslation)`
                       = (14.0, 3.0, -2.0) + 0.5 * ( (18.0, 1.0,  1.0) - (14.0, 3.0, -2.0) )
                       = (14.0, 3.0, -2.0) + 0.5 * (4.0, -2.0, 3.0)
                       = (16.0, 2.0, -0.5)

So when the current time is **1.2**, then the `translation` of the node is **(16.0, 2.0, -0.5)**


### Animation channels

Finally, the animations contain an array of of [`animation.channel`](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#reference-animation.channel) objects. The channels establish the connection between the input, which is the value that is computed from the sampler, and the output, which is the animated node property. Therefore, each channel refers to one sampler, using the ID of the sampler, and contains an [`animation.channel.target`](https://github.com/KhronosGroup/glTF/blob/master/specification/README.md#reference-animation.channel.target). The `target` refers to a node, using the ID of the node, and contains a `path` that defines the property of the node that should be animated. The value from the sampler will be written into this property.

In the example above, there are two channels for the animation. Both refer to the same node. The path of the first channel refers to the `translation` of the node, and the path of the second channel refers to the `rotation` of the node. So all objects (meshes) that are attached to the node will be translated and rotated by the animation:

![AnimationChannels](images/animationChannels.png)
