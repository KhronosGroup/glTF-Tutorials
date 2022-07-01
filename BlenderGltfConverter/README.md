# blender-gltf-converter

This is an example script on how to use Blender as a glTF conversion tool.  
The purpose of this repo is to show how to create and extend Blender scripts for tasks automation.  

# general Blender info

The library you need to import to access Blender API is called bpy.  
Link to the official documentation: https://docs.blender.org/api/current/index.html  
You can also enable tooltips in Blender: Edit -> Preferences -> Interface -> Python Tooltips. When you hover over an element in Blender UI, in addition to the name and decription, it will show you the Python equivalent of the element.  
You can also use Info window to see what API calls are made on each action performed in Blender.

# script usage

Run from the terminal:  
blender -b -P blender_gltf_converter.py -- -mp "path-to-file"  
If you're not in the same directory as the blender_gltf_converter.py file, provide full path to it.
The "-b" flag runs Blender in headless mode. If you wish to see the UI after the script is done processing, skip it.
The "-P" flag allows to pass script to Blender.

# glTF export options

The list of all parameters for gltf export can be found here:  
https://docs.blender.org/api/current/bpy.ops.export_scene.html#bpy.ops.export_scene.gltf  
Parameters that you won't set will use your Blender settings.
