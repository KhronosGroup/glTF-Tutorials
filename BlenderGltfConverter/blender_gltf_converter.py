"""
Run from the terminal:
blender -b -P blender_gltf_converter.py -- -mp "path-to-file"

If you're not in the same directory as the blender_gltf_converter.py file, provide full path to it.
The "-b" flag runs Blender in headless mode.
If you wish to see the UI after the script is done processing, skip it.
The "-P" flag allows to pass script to Blender.
"""


import sys
# bpy is the library you need to import to access Blender API
# link to the official documentation: https://docs.blender.org/api/current/index.html
# you can also enable tooltips in Blender: Edit -> Preferences -> Interface -> Python Tooltips
# you can also use Info window to see what API calls are made on each action performed in Blender
import bpy

# custom logic may go here

def runner():
    import argparse
    parser = argparse.ArgumentParser(description='Convert supported file type to gltf format.')
    # arguments go here, e.g. asset path, output path, other custom properties and flags
    parser.add_argument('-mp', '--model_path', help='Path to a model you want to convert.')

    argv = sys.argv
    # -- is a separator between arguments passed to Blender directly and to your script
    if "--" not in argv:
        argv = []
    else:
        # get just the arguments passed to your script
        argv = argv[argv.index("--") + 1:]

    # access passed arguments
    args = parser.parse_args(argv)
    # assignment to a variable is just a convenience, it's not mandatory
    model_path = args.model_path

    # clear default scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # custom logic may go here
    # you might want to e.g. support various file formats, this example works just with .obj files

    bpy.ops.import_scene.obj(filepath=model_path)
    output_path = model_path.replace(".obj", "")

    # the list of all parameters for gltf export can be found here:
    # https://docs.blender.org/api/current/bpy.ops.export_scene.html#bpy.ops.export_scene.gltf
    # parameters that you won't set will use your Blender settings
    bpy.ops.export_scene.gltf(filepath=output_path)


if __name__ == "__main__":
    runner()
