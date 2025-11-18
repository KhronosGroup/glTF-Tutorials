上一章: [基本 glTF 结构](gltfTutorial_002_BasicGltfStructure.md) | [目录](README.md) | 下一章: [场景和节点](gltfTutorial_004_ScenesNodes.md)


# 最小的 glTF 文件

以下是一个最小但完整的 glTF 资产，包含一个单独的、索引化的三角形。您可以将它复制并粘贴到一个 `gltf` 文件中，每个基于 glTF 的应用程序都应该能够加载并渲染它。本节将基于此示例解释 glTF 的基本概念。

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
      "mesh" : 0
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

  "buffers" : [
    {
      "uri" : "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAAAAAIA/AAAAAAAAAAAAAAAAAACAPwAAAAA=",
      "byteLength" : 44
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
    }
  ],
  
  "asset" : {
    "version" : "2.0"
  }
}
```

<p align="center">
<img src="../gltfTutorial/images/triangle.png" /><br>
<a name="triangle-png"></a>图 3a: 一个单独的三角形。
</p>


## `scene` 和 `nodes` 结构

[`scenes`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-scene) 数组是存储在 glTF 中的场景描述的入口点。在解析 glTF JSON 文件时，场景结构的遍历将从这里开始。每个场景包含一个名为 `nodes` 的数组，其中包含 [`node`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-node) 对象的索引。这些节点是场景图层次结构的根节点。

此示例由一个单独的场景组成。`scene` 属性表示该场景是加载资产时应显示的默认场景。场景引用了本示例中唯一的节点，即索引为 0 的节点。该节点反过来引用唯一的网格，索引为 0：


```javascript
  "scene": 0,
  "scenes" : [
    {
      "nodes" : [ 0 ]
    }
  ],
  
  "nodes" : [
    {
      "mesh" : 0
    }
  ],
```

关于场景和节点及其属性的更多详细信息将在 [场景和节点](gltfTutorial_004_ScenesNodes.md) 部分给出。


## `meshes`（网格）

[`mesh`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-mesh)（网格）表示出现在场景中的实际几何对象。网格本身通常没有任何属性，只包含一个 [`mesh.primitive`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-mesh-primitive)（网格图元）对象数组，作为更大模型的构建块。每个网格图元都包含网格所包含的几何数据的描述。

该示例由一个单独的网格组成，并有一个单独的 `mesh.primitive` 对象。网格图元有一个 `attributes` 数组。这些是网格几何体顶点的属性，在这种情况下，这只是描述顶点位置的 `POSITION` 属性。网格图元描述了一个*索引化*的几何体，这由 `indices` 属性指示。默认情况下，假定它描述了一组三角形，以便三个连续的索引是一个三角形顶点的索引。

网格图元的实际几何数据由 `attributes` 和 `indices` 给出。这两者都引用 `accessor` 对象，将在下面解释。

```javascript
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
```

关于网格和网格图元的更详细描述可以在 [网格](gltfTutorial_009_Meshes.md) 部分找到。


## `buffer`、`bufferView` 和 `accessor` 概念

`buffer`、`bufferView` 和 `accessor` 对象提供了关于网格图元组成的几何数据的信息。基于特定示例，这里将简要介绍它们。这些概念的更详细描述将在 [缓冲区、缓冲区视图和访问器](gltfTutorial_005_BuffersBufferViewsAccessors.md) 部分给出。

### 缓冲区

[`buffer`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-buffer) 定义了一个没有固有含义的原始、非结构化数据块。它包含一个 `uri`，可以指向包含数据的外部文件，也可以是直接在 JSON 文件中编码二进制数据的 [数据 URI](gltfTutorial_002_BasicGltfStructure.md#数据-uri-中的二进制数据)。

在示例文件中，使用了第二种方法：有一个包含 44 字节的单一缓冲区，这个缓冲区的数据被编码为数据 URI：

```javascript
  "buffers" : [
    {
      "uri" : "data:application/octet-stream;base64,AAABAAIAAAAAAAAAAAAAAAAAAAAAAIA/AAAAAAAAAAAAAAAAAACAPwAAAAA=",
      "byteLength" : 44
    }
  ],
```

这些数据包含三角形的索引和三角形的顶点位置。但是为了实际使用这些数据作为网格图元的几何数据，需要关于这些数据*结构*的额外信息。这个关于结构的信息在 `bufferView` 和 `accessor` 对象中编码。

### 缓冲区视图

[`bufferView`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-bufferview) 描述了整个原始缓冲区数据的一个"块"或"片段"。在给定的示例中，有两个缓冲区视图。它们都引用同一个缓冲区。第一个缓冲区视图引用包含索引数据的缓冲区部分：它有一个 `byteOffset` 为 0，引用整个缓冲区数据，以及一个 `byteLength` 为 6。第二个缓冲区视图引用包含顶点位置的缓冲区部分。它从 `byteOffset` 为 8 的位置开始，并有一个 `byteLength` 为 36；也就是说，它延伸到整个缓冲区的末尾。

```javascript
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
    }
  ],
```


### 访问器

数据结构化的第二步是通过 [`accessor`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-accessor) 对象完成的。它们通过提供关于数据类型和布局的信息来定义如何解释 `bufferView` 的数据。

在这个示例中，有两个访问器对象。

第一个访问器描述了几何数据的索引。它引用索引为 0 的 `bufferView`，这是包含索引原始数据的 `buffer` 部分。此外，它还指定了元素的 `count` 和 `type` 以及它们的 `componentType`。在这种情况下，有 3 个标量元素，它们的组件类型由代表 `unsigned short` 类型的常量给出。

第二个访问器描述了顶点位置。它通过索引为 1 的 `bufferView` 包含对缓冲区数据相关部分的引用，其 `count`、`type` 和 `componentType` 属性表明有三个 3D 向量元素，每个都有 `float` 组件。


```javascript
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
    }
  ],
```

如上所述，`mesh.primitive` 现在可以使用这些访问器的索引引用它们：

```javascript
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
```

当需要渲染这个 `mesh.primitive` 时，渲染器可以解析底层的缓冲区视图和缓冲区，并将缓冲区的所需部分与关于数据类型和布局的信息一起发送到渲染器。关于访问器数据如何被渲染器获取和处理的更详细描述在 [缓冲区、缓冲区视图和访问器](gltfTutorial_005_BuffersBufferViewsAccessors.md) 部分给出。




## `asset` 描述

在 glTF 1.0 中，这个属性仍然是可选的，但在后续的 glTF 版本中，JSON 文件必须包含包含 `version` 编号的 `asset` 属性。这里的示例表明该资产符合 glTF 2.0 版本：

```javascript
  "asset" : {
    "version" : "2.0"
  }
```

`asset` 属性可能包含 [`asset` 规范](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-asset) 中描述的额外元数据。




上一章: [基本 glTF 结构](gltfTutorial_002_BasicGltfStructure.md) | [目录](README.md) | 下一章: [场景和节点](gltfTutorial_004_ScenesNodes.md) 