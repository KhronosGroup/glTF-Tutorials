[目录](README.md) | 下一章: [基本 glTF 结构](gltfTutorial_002_BasicGltfStructure.md)

# 使用 WebGL 的 glTF 介绍

越来越多的应用程序和服务都基于 3D 内容。在线商店提供带有 3D 预览的产品配置器。博物馆对其文物进行 3D 扫描，并允许游客在虚拟画廊中探索他们的收藏品。城市规划师使用 3D 城市模型进行规划和信息可视化。教育工作者创建人体的交互式动画 3D 模型。许多这些应用程序直接在网络浏览器中运行，这是可能的，因为所有现代浏览器都支持通过 WebGL 进行高效渲染。

<p align="center">
<img src="./gltfTutorial_cn/images/applications.png" /><br>
<a name="applications-png"></a>图 1a: 展示 3D 模型的各种网站和应用程序的截图。
</p>

各种应用程序对 3D 内容的需求不断增长。在许多情况下，3D 内容必须通过网络传输，并且必须在客户端高效地渲染。但直到现在，3D 内容创建和在运行时应用程序中高效渲染之间仍存在差距。

## 3D 内容管道

在客户端应用程序中渲染的 3D 内容来自不同的源，并存储在不同的文件格式中。[维基百科上的 3D 图形文件格式列表](https://en.wikipedia.org/wiki/List_of_file_formats#3D_graphics) 显示了一个庞大的数量，有超过 70 种不同的 3D 数据文件格式，服务于不同的目的和应用场景。

例如，原始 3D 数据可以通过 3D 扫描仪获取。这些扫描仪通常提供单个对象的几何数据，这些数据存储在 [OBJ](https://en.wikipedia.org/wiki/Wavefront_.obj_file)、[PLY](https://en.wikipedia.org/wiki/PLY_(file_format)) 或 [STL](https://en.wikipedia.org/wiki/STL_(file_format)) 文件中。这些文件格式不包含关于场景结构或对象应如何渲染的信息。

更复杂的 3D 场景可以使用创作工具创建。这些工具允许编辑场景的结构、灯光设置、相机、动画，以及当然还有场景中出现的对象的 3D 几何体。应用程序以自己的自定义文件格式存储这些信息。例如，[Blender](https://www.blender.org/) 将场景存储在 `.blend` 文件中，[LightWave3D](https://www.lightwave3d.com/) 使用 `.lws` 文件格式，[3ds Max](https://www.autodesk.com/3dsmax) 使用 `.max` 文件格式，而 [Maya](https://www.autodesk.com/maya) 使用 `.ma` 文件。

为了渲染这些 3D 内容，运行时应用程序必须能够读取不同的输入文件格式。必须解析场景结构，3D 几何数据必须转换为图形 API 所需的格式。3D 数据必须传输到图形卡内存，然后可以用图形 API 调用序列描述渲染过程。因此，每个运行时应用程序都必须为其支持的所有文件格式创建导入器、加载器或转换器，如 [图 1b](#contentPipeline-png) 所示。

<p align="center">
<img src="./gltfTutorial/images/contentPipeline.png" /><br>
<a name="contentPipeline-png"></a>图 1b: 当今的 3D 内容管道。
</p>

## glTF: 3D 场景的传输格式

glTF 的目标是为 3D 内容定义一个标准，以适合在运行时应用程序中使用的形式。现有的文件格式不适合这种用例：有些不包含任何场景信息，只有几何数据；其他一些则是为了在创作应用程序之间交换数据而设计的，它们的主要目标是保留关于 3D 场景的尽可能多的信息，这导致文件通常很大、很复杂且难以解析。此外，几何数据可能需要预处理，以便可以用客户端应用程序渲染。

现有的文件格式都不是为通过网络高效传输 3D 场景并尽可能高效地渲染它们而设计的。但 glTF 不是"又一种文件格式"。它是 3D 场景*传输*格式的定义：

- 场景结构用 JSON 描述，它非常紧凑且易于解析。
- 对象的 3D 数据以可以被常见图形 API 直接使用的形式存储，因此没有解码或预处理 3D 数据的开销。

现在，不同的内容创建工具可以提供 glTF 格式的 3D 内容。越来越多的客户端应用程序能够使用和渲染 glTF。[图 1a](#applications-png) 中显示了其中一些应用程序。因此，glTF 可能有助于弥合内容创建和渲染之间的差距，如 [图 1c](#contentPipelineWithGltf-png) 所示。

<p align="center">
<img src="./gltfTutorial/images/contentPipelineWithGltf.png" /><br>
<a name="contentPipelineWithGltf-png"></a>图 1c: 使用 glTF 的 3D 内容管道。
</p>

越来越多的内容创建工具直接提供 glTF 导入和导出功能。例如，Blender 手册记录了[如何使用 glTF 导入和导出 PBR 材质](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html)。或者，其他文件格式可以使用 [glTF Project Explorer](https://github.khronos.org/glTF-Project-Explorer/) 中列出的开源转换工具之一创建 glTF 资产。转换器和导出器的输出可以使用 [Khronos glTF Validator](https://github.khronos.org/glTF-Validator/) 进行验证。

[目录](README.md) | 下一章: [基本 glTF 结构](gltfTutorial_002_BasicGltfStructure.md) 
