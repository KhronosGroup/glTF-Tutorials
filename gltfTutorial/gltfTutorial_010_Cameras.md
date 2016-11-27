Previous: [Advanced Material](gltfTutorial_009f_TexturesImagesSamplers.md) | [Table of Contents](README.md)

# Cameras

The previous sections showed how a basic scene structure with geometric objects is represented in a glTF asset, and how different materials can be applied to these objects. This did not yet include information about the view configuration that should be used for rendering the scene. This view configuration is usually described as a virtual *camera* that is contained in the scene, at a certain position, and pointing in a certain direction. 

This section will show how to define such [`camera`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-camera) objects in a glTF asset. The following is a simple, complete glTF asset. It is similar to the assets that have already been shown: It defines a simple `scene`, containing `node` objects, and a single geometric object that is given as a `mesh`, attached to one of the nodes. But this asset additional contains several `camera` objects, which will be explained in more detail below:


```javascript
{
  "scenes" : {
    "scene0" : {
      "nodes" : [ "meshNode", "perspectiveCameraNode", "orthographicCameraNode" ]
    }
  },
  "nodes" : {
    "meshNode" : {
      "rotation" : [ -0.383, 0.0, 0.0, 0.924 ],
      "meshes" : [ "mesh0" ]
    },
    "perspectiveCameraNode" : {
      "translation" : [ 0.5, 0.5, 3.0 ],
      "camera" : "exampleCameraPerspective"
    },
    "orthographicCameraNode" : {
      "translation" : [ 0.5, 0.5, 3.0 ],
      "camera" : "exampleCameraOrthographic"
    }
  },
  
  "cameras" : {
    "exampleCameraPerspective": {
      "type": "perspective",
      "perspective": {
        "aspectRatio": 1.0,
        "yfov": 0.7,
        "zfar": 100,
        "znear": 0.01
      }
    },
    "exampleCameraOrthographic": {
      "type": "orthographic",
      "orthographic": {
        "xmag": 1.0,
        "ymag": 1.0,
        "zfar": 100,
        "znear": 0.01
      }
    }
  },
  
  "meshes" : {
    "mesh0" : {
      "primitives" : [ {
        "attributes" : {
          "POSITION" : "positionsAccessor",
          "NORMAL" : "normalsAccessor",
          "TEXCOORD_0" : "texCoordsAccessor"
        },
        "indices" : "indicesAccessor"
      } ]
    }
  },

  "buffers" : {
    "buffer0" : {
      "uri" : "data:application/octet-stream;base64,AAABAAIAAQADAAIAAAAAAAAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAAAAgD8AAAAAAACAPwAAgD8AAAAAAAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AAAAAAAAAAAAAIA/AACAPwAAgD8=",
      "byteLength" : 140
    }
  },
  "bufferViews" : {
    "indicesBufferView" : {
      "buffer" : "buffer0",
      "byteOffset" : 0,
      "byteLength" : 12,
      "target" : 34963
    },
    "attributesBufferView" : {
      "buffer" : "buffer0",
      "byteOffset" : 12,
      "byteLength" : 128,
      "target" : 34962
    }
  },
  "accessors" : {
    "indicesAccessor" : {
      "bufferView" : "indicesBufferView",
      "byteOffset" : 0,
      "componentType" : 5123,
      "count" : 6,
      "type" : "SCALAR",
      "max" : [ 2.0 ],
      "min" : [ 0.0 ]
    },
    "positionsAccessor" : {
      "bufferView" : "attributesBufferView",
      "byteOffset" : 0,
      "componentType" : 5126,
      "count" : 4,
      "type" : "VEC3",
      "max" : [ 1.0, 1.0, 0.0 ],
      "min" : [ 0.0, 0.0, 0.0 ]
    },
    "normalsAccessor" : {
      "bufferView" : "attributesBufferView",
      "byteOffset" : 36,
      "componentType" : 5126,
      "count" : 4,
      "type" : "VEC3",
      "max" : [ 0.0, 0.0, 1.0 ],
      "min" : [ 0.0, 0.0, 1.0 ]
    },
    "texCoordsAccessor" : {
      "bufferView" : "attributesBufferView",
      "byteOffset" : 72,
      "componentType" : 5126,
      "count" : 4,
      "type" : "VEC2",
      "max" : [ 1.0, 1.0 ],
      "min" : [ 0.0, 0.0 ]
    }
  },
  "asset" : {
    "version" : "1.1"
  }
}
```

The geometry in this asset is a simple unit square. It is rotated by -45 degrees around the x-axis, to emphasize the effect of the different cameras. The following image shows three options for rendering this asset. The first examples are using the cameras from the asset. The last example shows how the scene looks from an external, user-defined viewpoint:

<p align="center">
<img src="images/cameras.png" /><br>
<a name="cameras-png"></a>Image 10a: The effect of rendering the scene with different cameras
</p>


# Perspective and orthographic cameras

The new top-level element of this glTF asset is the `cameras` dictionary, which maps IDs to [`camera`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-camera) objects:

```javascript
"cameras" : {
  "exampleCameraPerspective": {
    "type": "perspective",
    "perspective": {
      "aspectRatio": 1.0,
      "yfov": 0.7,
      "zfar": 100,
      "znear": 0.01
    }
  },
  "exampleCameraOrthographic": {
    "type": "orthographic",
    "orthographic": {
      "xmag": 1.0,
      "ymag": 1.0,
      "zfar": 100,
      "znear": 0.01
    }
  }
},
```

There are two kinds of cameras: *Perspective* cameras, where the viewing volume is a truncated pyramid (often referred to as "viewing frustum"), and *orthographic*  cameras, where the viewing volumne is a rectangular box. The main difference is that rendering with a *perspective* camera causes a proper perspective distortion, whereas rendering with an *orthographic* camera causes a preservation of lengths and angles.

The example contains one camera of each type, with the IDs `"exampleCameraPerspective"` and `"exampleCameraOrthographic"`, respectively. The `type` of the camera is given as a string, which can be `"perspective"` or  `"orthographic"`. Depending on this type, the `camera` object contains a [`camera.perspective`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-camera.perspective) object or a [`camera.orthographic`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-camera.orthographic) object. These objects contain additional parameters that define the actual viewing volume. 

The `camera.perspective` object contains an `aspectRatio` property that defines the aspect ratio of the viewport. Additionally, it contains a property called `yfov`, which stands for *Field Of View in Y-direction*. It defines the "opening angle" of the camera, and is given in radians. 

The `camera.orthographic` object contains `xmag` and `ymag` properties. These the magnification of the camera in x- and y-direction, and basically describe the width and height of the viewing volume.

Both camera types additionally contain `znear` and `zfar` properties, which are the coordinates of the near and far clipping plane.

Explaining the details of cameras, viewing and projections is beyond the scope of this tutorial. The important point is that most graphics APIs offer methods for defining the viewing configuration that are directly based on these parameters. In general, these parameters can be used to compute a *camera matrix*. The camera matrix can be inverted to obtain the *view matrix*, which will later be post-multiplied with the *model matrix* in order to obtain the *model-view matrix*, which is required by the renderer. 


# Camera orientation

A `camera` can be transformed to have a certain orientation and viewing direction in the scene. This accomplished by attaching the camera to a `node`: Each [`node`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-node) may contain the ID of a [`camera`](https://github.com/KhronosGroup/glTF/tree/master/specification#reference-camera) that is attached to it.

In the example, there are two nodes for the cameras. The first node refers to the `"exampleCameraPerspective"`, and the second one refers to the `"exampleCameraOrthographic"`: 

```javascript
"nodes" : {
  ...
  "perspectiveCameraNode" : {
    "translation" : [ 0.5, 0.5, 3.0 ],
    "camera" : "exampleCameraPerspective"
  },
  "orthographicCameraNode" : {
    "translation" : [ 0.5, 0.5, 3.0 ],
    "camera" : "exampleCameraOrthographic"
  }
},
```

As shown in the section about [scenes and nodes](gltfTutorial_004_ScenesNodes.md), these nodes may have properties that define the transform matrix of the node. The [global transform](gltfTutorial_004_ScenesNodes.md#global-transforms-of-nodes) of a node then defines the actual orientation of the camera in the scene.

When the global transform of the camera node is the identity matrix, then the eye point of the camera is at the origin, and the viewing direction is along the negative z-axis. In the given example, the nodes both have a `translation` about `(0.5, 0.5, 3.0)`, which causes the camera to be transformed accordingly: It is translated about 0.5 in x- and y- direction, to look at the center of the unit square, and about 3.0 along the z-axis, to move it a bit away from the object. 


# Camera management

There may be multiple cameras defined in the JSON part of a glTF. However, there is no "default" camera. Instead, the client application has to keep track of the currently active camera. The client application may, for example, offer a dropdown-menu that allows selecting the active camera, and thus, to quickly switch between predefined view configurations. With a bit more implementation effort, the client application can also define an own camera and interaction patterns for the camera control (e.g. zooming with the mouse wheel). However, the logic for the navigation and interaction has to be implemented solely by the client application in this case. The [Image 10a](#cameras-png) above shows the result of such an implementation, where the user may select the active camera from the ones that are defined in the glTF asset, or an "External camera" that may be controlled with the mouse.



Previous: [Advanced Material](gltfTutorial_009f_TexturesImagesSamplers.md) | [Table of Contents](README.md)
