上一章: [缓冲区、缓冲区视图和访问器](gltfTutorial_005_BuffersBufferViewsAccessors.md) | [目录](README.md) | 下一章: [动画](gltfTutorial_007_Animations.md)


# 简单动画

如 [场景和节点](gltfTutorial_004_ScenesNodes.md) 部分所示，每个节点都可以有一个局部变换。这个变换可以通过节点的 `matrix` 属性给出，或者使用 `translation`、`rotation` 和 `scale`（TRS）属性。

当变换通过 TRS 属性给出时，可以使用 [`animation`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-animation) 来描述节点的 `translation`、`rotation` 或 `scale` 如何随时间变化。

以下是之前展示的[最小 glTF 文件](gltfTutorial_003_MinimalGltfFile.md)，但扩展了一个动画。本节将解释为添加此动画所做的更改和扩展。


```javascript
{
  "scene": 0,
  "scenes" : [
    {
      "nodes" : [ 0 ]
    }
  ],
  
  "nodes" : [
    {
      "mesh" : 0,
      "rotation" : [ 0.0, 0.0, 0.0, 1.0 ]
    }
  ],
  
  "meshes" : [
    {
      "primitives" : [ {
        "attributes" : {
          "POSITION" : 1
        },
        "indices" : 0
      } ]
    }
  ],
  
  "animations": [
    {
      "samplers" : [
        {
          "input" : 2,
          "interpolation" : "LINEAR",
          "output" : 3
        }
      ],
      "channels" : [ {
        "sampler" : 0,
        "target" : {
          "node" : 0,
          "path" : "rotation"
        }
      } ]
    }
  ],

  "buffers" : [
    {
      "uri" : "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAAAAAIA/AAAAAAAAAAAAAAAAAACAPwAAAAA=",
      "byteLength" : 44
    },
    {
      "uri" : "data:application/octet-stream;base64,AAAAAAAAgD4AAAA/AABAPwAAgD8AAAAAAAAAAAAAAAAAAIA/AAAAAAAAAAD0/TQ/9P00PwAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAPT9ND/0/TS/AAAAAAAAAAAAAAAAAACAPw==",
      "byteLength" : 100
    }
  ],
  "bufferViews" : [
    {
      "buffer" : 0,
      "byteOffset" : 0,
      "byteLength" : 6,
      "target" : 34963
    },
    {
      "buffer" : 0,
      "byteOffset" : 8,
      "byteLength" : 36,
      "target" : 34962
    },
    {
      "buffer" : 1,
      "byteOffset" : 0,
      "byteLength" : 100
    }
  ],
  "accessors" : [
    {
      "bufferView" : 0,
      "byteOffset" : 0,
      "componentType" : 5123,
      "count" : 3,
      "type" : "SCALAR",
      "max" : [ 2 ],
      "min" : [ 0 ]
    },
    {
      "bufferView" : 1,
      "byteOffset" : 0,
      "componentType" : 5126,
      "count" : 3,
      "type" : "VEC3",
      "max" : [ 1.0, 1.0, 0.0 ],
      "min" : [ 0.0, 0.0, 0.0 ]
    },
    {
      "bufferView" : 2,
      "byteOffset" : 0,
      "componentType" : 5126,
      "count" : 5,
      "type" : "SCALAR",
      "max" : [ 1.0 ],
      "min" : [ 0.0 ]
    },
    {
      "bufferView" : 2,
      "byteOffset" : 20,
      "componentType" : 5126,
      "count" : 5,
      "type" : "VEC4",
      "max" : [ 0.0, 0.0, 1.0, 1.0 ],
      "min" : [ 0.0, 0.0, 0.0, -0.707 ]
    }
  ],
  
  "asset" : {
    "version" : "2.0"
  }
  
}
```

<p align="center">
<img src="images/animatedTriangle.gif" /><br>
<a name="animatedTriangle-gif"></a>图 6a: 一个单独的、带动画的三角形。
</p>


## 节点的 `rotation` 属性

示例中的唯一节点现在有一个 `rotation` 属性。这是一个包含描述旋转的[四元数](https://en.wikipedia.org/wiki/Quaternion)的四个浮点值的数组：

```javascript
  "nodes" : [
    {
      "mesh" : 0,
      "rotation" : [ 0.0, 0.0, 0.0, 1.0 ]
    }
  ],
```

给定的值是描述"旋转 0 度"的四元数，因此三角形将以其初始方向显示。


## 动画数据

在 glTF JSON 的顶层数组中添加了三个元素来编码动画数据：

- 一个包含原始动画数据的新 `buffer`；
- 一个引用该缓冲区的新 `bufferView`；
- 两个新的 `accessor` 对象，为动画数据添加结构信息。

### 原始动画数据的 `buffer` 和 `bufferView`

已添加一个新的 `buffer`，其中包含原始动画数据。这个缓冲区也使用[数据 URI](gltfTutorial_002_BasicGltfStructure.md#数据-uri-中的二进制数据)来编码组成动画数据的 100 个字节：

```javascript
  "buffers" : [
    ...
    {
      "uri" : "data:application/octet-stream;base64,AAAAAAAAgD4AAAA/AABAPwAAgD8AAAAAAAAAAAAAAAAAAIA/AAAAAAAAAAD0/TQ/9P00PwAAAAAAAAAAAACAPwAAAAAAAAAAAAAAAPT9ND/0/TS/AAAAAAAAAAAAAAAAAACAPw==",
      "byteLength" : 100
    }
  ],

  "bufferViews" : [
    ...
    {
      "buffer" : 1,
      "byteOffset" : 0,
      "byteLength" : 100
    }
  ],
```

还有一个新的 `bufferView`，它在这里简单地引用包含整个动画缓冲区数据的索引为 1 的新 `buffer`。更多的结构信息通过下面描述的 `accessor` 对象添加。

请注意，也可以将动画数据附加到已经包含三角形几何数据的现有缓冲区中。在这种情况下，新的缓冲区视图将引用索引为 0 的 `buffer`，并使用适当的 `byteOffset` 来引用包含动画数据的缓冲区部分。

在这里显示的示例中，动画数据作为新缓冲区添加，以保持几何数据和动画数据分离。


### 动画数据的 `accessor` 对象

添加了两个新的 `accessor` 对象，描述如何解释动画数据。第一个访问器描述动画关键帧的*时间*。有五个元素（由 `count` 5 表示），每个元素都是一个标量 `float` 值（总共 20 个字节）。第二个访问器表示，在前 20 个字节之后，有五个元素，每个元素都是具有 `float` 组件的 4D 向量。这些是对应于动画五个关键帧的*旋转*，以四元数给出。

```javascript
  "accessors" : [
    ...
    {
      "bufferView" : 2,
      "byteOffset" : 0,
      "componentType" : 5126,
      "count" : 5,
      "type" : "SCALAR",
      "max" : [ 1.0 ],
      "min" : [ 0.0 ]
    },
    {
      "bufferView" : 2,
      "byteOffset" : 20,
      "componentType" : 5126,
      "count" : 5,
      "type" : "VEC4",
      "max" : [ 0.0, 0.0, 1.0, 1.0 ],
      "min" : [ 0.0, 0.0, 0.0, -0.707 ]
    }
  ],

```

使用示例中缓冲区的数据，*时间*访问器和*旋转*访问器提供的实际数据如下表所示：

|*时间*访问器|*旋转*访问器|含义|
|---|---|---|
|0.0| (0.0, 0.0, 0.0, 1.0 )| 在 0.0 秒时，三角形的旋转为 0 度 |
|0.25| (0.0, 0.0, 0.707, 0.707)| 在 0.25 秒时，它围绕 z 轴旋转 90 度
|0.5| (0.0, 0.0, 1.0, 0.0)| 在 0.5 秒时，它围绕 z 轴旋转 180 度 |
|0.75| (0.0, 0.0, 0.707, -0.707)| 在 0.75 秒时，它围绕 z 轴旋转 270 (= -90) 度 |
|1.0| (0.0, 0.0, 0.0, 1.0)| 在 1.0 秒时，它围绕 z 轴旋转 360 (= 0) 度 |

所以这个动画描述了围绕 z 轴的 360 度旋转，持续 1 秒。


## `animation`（动画）

最后，这是添加实际动画的部分。顶层 `animations` 数组包含一个单独的 `animation` 对象。它由两个元素组成：

- `samplers`，描述动画数据的来源；
- `channels`，可以想象为连接动画数据的"源"和"目标"。

在给定的示例中，有一个采样器。每个采样器定义了 `input` 和 `output` 属性。它们都引用访问器对象。在这里，这些是上面描述的*时间*访问器（索引为 2）和*旋转*访问器（索引为 3）。此外，采样器定义了一个 `interpolation` 类型，在本例中为 `"LINEAR"`。

这个例子中也有一个 `channel`。这个通道将唯一的采样器（索引为 0）作为动画数据的来源。动画的目标在 `channel.target` 对象中编码：它包含一个引用其属性应该被动画化的节点的 `id`。实际的节点属性在 `path` 中命名。因此，给定示例中的通道目标表示节点索引为 0 的 `"rotation"` 属性应该被动画化。


```javascript
  "animations": [
    {
      "samplers" : [
        {
          "input" : 2,
          "interpolation" : "LINEAR",
          "output" : 3
        }
      ],
      "channels" : [ {
        "sampler" : 0,
        "target" : {
          "node" : 0,
          "path" : "rotation"
        }
      } ]
    }
  ],
```

结合所有这些信息，给定的动画对象表示以下内容：

> 在动画期间，动画值从*旋转*访问器获取。它们根据当前模拟时间和*时间*访问器提供的关键帧时间进行线性插值。然后将插值后的值写入索引为 0 的节点的 `"rotation"` 属性中。

关于插值和相关计算的更详细描述和实际示例可以在[动画](gltfTutorial_007_Animations.md)部分找到。



上一章: [缓冲区、缓冲区视图和访问器](gltfTutorial_005_BuffersBufferViewsAccessors.md) | [目录](README.md) | 下一章: [动画](gltfTutorial_007_Animations.md)
