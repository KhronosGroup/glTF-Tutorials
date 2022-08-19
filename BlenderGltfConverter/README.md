# blender-gltf-converter

[Blender](https://www.blender.org/) can be used as a command line tool for converting many different input file formats into glTF assets. This repository contains an example script that shows how to use Blender as a glTF conversion tool. 

The purpose of this repository is to show how to create and extend Blender scripts for tasks automation. It does not explain the details of the conversion options, but is intended as a template that can be used as a basis for custom conversion tasks.

# General Blender info

The conversion script is implemented in Python, which can directly be executed by Blender. The library that has to be imported in the Python script in order to access the Blender functionality is called _bpy_. The official documentation can be found at https://docs.blender.org/api/current/index.html .

In order to find the Python functions that correspond to certain Blender functionalities, you can also enable Python tooltips in Blender: _Edit -> Preferences -> Interface -> Display -> Python Tooltips_. When you hover over an element in the Blender UI, in addition to the name and decription, it will show you the Python equivalent of the element. 

You can also use the Info window to see what API calls are made on each action performed in Blender.

# Script usage

The actual conversion script is given in [`blender_gltf_converter.py`](blender_gltf_converter.py). It can be executed with Blender from the command line by calling

`blender -b -P blender_gltf_converter.py -- -mp `*`"path-to-input-file"`*

- The `-b` flag (alternatively: `--background`) runs Blender in headless mode. If you wish to see the UI after the script is done processing, omit it.
- The `-P` flag (uppercase! Alternatively: `--python`) allows you to pass the Python script to Blender. If you are not in the same directory as the `blender_gltf_converter.py` file, provide full path to it.

The full list of Blender command line options can be found at https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html . 

The `--` is used as a separator between the command line arguments that are passed to Blender itself, and the command line arguments that are passed to the script. The script receives only one argument here: 

- The `-mp` (model path) argument, which is followed by the full path of the file that should be converted into a glTF asset.

# Script customization

The example script in this repository is intended as a template for custom scripts. The example only accepts Wavefront OBJ files as the input. The files are imported into blender with `bpy.ops.import_scene.obj`. In order to import other formats (like FBX or X3D files), the corresponding functions from the [import scene operators](https://docs.blender.org/api/current/bpy.ops.import_scene.html) can be used.

The example script imports the input file into a Blender scene. Customization steps may be inserted after the import, for example, to modify the imported model. 

The script then exports the scene as glTF file, using `bpy.ops.export_scene.gltf`. The list of all parameters for the 
glTF export can be found at https://docs.blender.org/api/current/bpy.ops.export_scene.html#bpy.ops.export_scene.gltf.
Parameters that will not be set explicitly, will use `your` Blender settings.