上一章: [介绍](gltfTutorial_001_Introduction.md) | [目录](README.md) | 下一章: [最小的 glTF 文件](gltfTutorial_003_MinimalGltfFile.md)

# glTF 的基本结构

glTF 的核心是一个 JSON 文件。这个文件描述了整个 3D 场景的内容。它包含场景结构本身的描述，该结构由定义场景图的节点层次结构给出。场景中出现的 3D 对象使用附加到节点的网格来定义。材质（Materials）定义了对象的外观。动画（Animations）描述了 3D 对象如何随时间变换（例如，旋转或平移），而蒙皮（Skins）定义了对象的几何形状如何基于骨架姿势进行变形。相机（Cameras）描述了渲染器的视图配置。

## JSON 结构

场景对象存储在 JSON 文件中的数组中。可以使用对象在数组中的索引来访问它们：

```javascript
"meshes" : 
[
    { ... }
    { ... }
    ...
],
```

这些索引也用于定义对象之间的*关系*。上面的例子定义了多个网格，一个节点可以使用网格索引引用其中一个网格，表明该网格应该附加到这个节点：

```javascript
"nodes": 
[
    { "mesh": 0, ... },
    { "mesh": 5, ... },
    ...
]
```

下图（改编自 [glTF 概念部分](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#concepts)）概述了 glTF 资产的 JSON 部分的顶级元素：

<p align="center">
<img src="./gltfTutorial/images/gltfJsonStructure.png" /><br>
<a name="gltfJsonStructure-png"></a>图 2a: glTF JSON 结构
</p>

这里快速总结了这些元素，以提供一个概述，并附有 glTF 规范相应部分的链接。在以下章节中将对这些元素之间的关系进行更详细的解释。

- [`scene`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-scene)（场景）是存储在 glTF 中的场景描述的入口点。它引用定义场景图的 `node`（节点）。
- [`node`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-node)（节点）是场景图层次结构中的一个节点。它可以包含变换（例如，旋转或平移），并且可以引用更多（子）节点。此外，它可以引用"附加"到节点的 `mesh`（网格）或 `camera`（相机）实例，或者引用描述网格变形的 `skin`（蒙皮）。
- [`camera`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-camera)（相机）定义了渲染场景的视图配置。
- [`mesh`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-mesh)（网格）描述出现在场景中的几何对象。它引用用于访问实际几何数据的 `accessor`（访问器）对象，以及定义渲染对象时外观的 `material`（材质）。
- [`skin`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-skin)（蒙皮）定义了顶点蒙皮所需的参数，顶点蒙皮允许基于虚拟角色的姿势对网格进行变形。这些参数的值从 `accessor` 获取。
- [`animation`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-animation)（动画）描述了某些节点的变换（例如，旋转或平移）如何随时间变化。
- [`accessor`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-accessor)（访问器）被用作任意数据的抽象源。它被 `mesh`、`skin` 和 `animation` 使用，并提供几何数据、蒙皮参数和时间相关的动画值。它引用 [`bufferView`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-bufferview)（缓冲区视图），它是包含实际原始二进制数据的 [`buffer`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-buffer)（缓冲区）的一部分。
- [`material`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-material)（材质）包含定义对象外观的参数。它通常引用将应用于渲染几何体的 `texture`（纹理）对象。
- [`texture`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-texture)（纹理）由 [`sampler`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-sampler)（采样器）和 [`image`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-image)（图像）定义。`sampler` 定义了 `image` 纹理应该如何放置在对象上。

## 对外部数据的引用

3D 对象的二进制数据，如几何体和纹理，通常不包含在 JSON 文件中。相反，它们存储在专用文件中，JSON 部分只包含指向这些文件的链接。这使得二进制数据可以以非常紧凑的形式存储，并且可以通过网络高效传输。此外，数据可以以可以直接在渲染器中使用的格式存储，而无需解析、解码或预处理数据。

<p align="center">
<img src="./gltfTutorial/images/gltfStructure.png" /><br>
<a name="gltfStructure-png"></a>图 2b: glTF 结构
</p>

如上图所示，有两种类型的对象可能包含这样的外部资源链接，即 `buffers`（缓冲区）和 `images`（图像）。这些对象将在后面更详细地解释。

## 读取和管理外部数据

读取和处理 glTF 资产从解析 JSON 结构开始。结构解析后，[`buffer`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-buffer) 和 [`image`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-image) 对象分别在顶级 `buffers` 和 `images` 数组中可用。这些对象中的每一个都可能引用二进制数据块。为了进一步处理，这些数据被读入内存。通常，数据将存储在一个数组中，以便可以使用与引用它们所属的 `buffer` 或 `image` 对象相同的索引查找它们。

## `buffers` 中的二进制数据

[`buffer`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-buffer) 包含一个指向包含原始二进制缓冲数据的文件的 URI：

```javascript
"buffer01": {
    "byteLength": 12352,
    "type": "arraybuffer",
    "uri": "buffer01.bin"
}
```

这个二进制数据只是从 `buffer` 的 URI 读取的原始内存块，没有固有的含义或结构。[缓冲区、缓冲区视图和访问器](gltfTutorial_005_BuffersBufferViewsAccessors.md) 部分将展示如何用关于数据类型和数据布局的信息扩展这些原始数据。有了这些信息，一部分数据可能会被解释为动画数据，而另一部分可能会被解释为几何数据。以二进制形式存储数据可以使其通过网络传输比 JSON 格式更高效，而且二进制数据可以直接传递给渲染器，无需解码或预处理。

## `images` 中的图像数据

[`image`](https://www.khronos.org/registry/glTF/specs/2.0/glTF-2.0.html#reference-image) 可以引用可以用作渲染对象纹理的外部图像文件：

```javascript
"image01": {
    "uri": "image01.png"
}
```

引用以 URI 的形式给出，通常指向 PNG 或 JPG 文件。这些格式显著减小了文件的大小，以便可以通过网络高效传输。在某些情况下，`image` 对象可能不引用外部文件，而是引用存储在 `buffer` 中的数据。这种间接的细节将在 [纹理、图像和采样器](gltfTutorial_012_TexturesImagesSamplers.md) 部分解释。

## 数据 URI 中的二进制数据

通常，`buffer` 和 `image` 对象中包含的 URI 将指向包含实际数据的文件。作为替代方案，数据可以使用 [数据 URI](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs) 以二进制格式*嵌入*到 JSON 中。

上一章: [介绍](gltfTutorial_001_Introduction.md) | [目录](README.md) | 下一章: [最小的 glTF 文件](gltfTutorial_003_MinimalGltfFile.md)
