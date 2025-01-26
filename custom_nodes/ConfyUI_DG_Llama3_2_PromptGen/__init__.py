#!/usr/bin/env python3
"""
@author: Dave Gravel
@title: ComfyUI OrionX3D Nodes
@web: https://www.youtube.com/@EvadLevarg/videos
@facebook: https://www.facebook.com/dave.gravel1
@nickname: k00m
@description: This extension is for experimental purposes only. Although I am a proficient Pascal and C++ programmer, I am relatively new to Python and may have made mistakes in the code.
@description: I have created these nodes primarily for my personal use. Some parts of the code are adapted from existing custom nodes, while others are original and designed entirely by me.
#
# Hello, I’m Dave Gravel. By trade, I’m a C++ programmer specializing in 3D and Physics, 
# along with anything related to this field. I have a basic understanding of almost all 
# programming languages, but the two I’ve used the most and in which I excel are Pascal and C++. 
# I’m familiar with the logic of most other languages, though I haven’t worked with them extensively. 
# As a result, my code may include some repetitive logic and certain methods that could be better 
# implemented, but overall, everything should still work pretty well, hehe.

# A year ago, or maybe a little more, I had created a Llama 3.1 node. However, since it was difficult 
# to get it working due to the size of the Llama 3.1 8B model and because some tools for loading 
# the Llama model at the time conflicted with other tools in ComfyUI, I decided not to make it public.

# When Llama 3.2 was released, I tested the tools again, and the conflicts seem to be resolved now, 
# and Llama works very well. So, I decided to update my node, DGPromptGenLlama, and while building it, 
# I realized that some cool options could be added, like styles and a few other features I’ll discuss below.

# Since everything seems to be working well for me now, I decided to share it with the public. 
# This way, it might be useful for others as well. It’s a great tool if you’re running out of ideas 
# for writing your prompts.

# With this, you’ll be able to create amazing images and videos. Or you can simply use Llama like ChatGPT, 
# as it’s possible to configure and create your own agents for anything, not just for prompts.
#
"""
"""
"""
import os, sys
import importlib
import filecmp
import shutil
import __main__
# temporary D.G
#from .config import ORIONX3D_CONFIG

THIS_DIR=os.path.dirname(os.path.abspath(__file__))

current_dir = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
javascript_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")

target_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))

sys.path.append(target_dir)

print(f"OrionX3D ComfyUI Folder: {target_dir}")

extentions_folder = os.path.join(os.path.dirname(os.path.realpath(__main__.__file__)),
                                 "web" + os.sep + "extensions" + os.sep + "DG_OX3D")
javascript_folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "js")

if not os.path.exists(extentions_folder):
    #print('Making the "web\extensions\DG_OX3D" folder')
    os.mkdir(extentions_folder)

result = filecmp.dircmp(javascript_folder, extentions_folder)

if result.left_only or result.diff_files:
    print('Update to javascripts files detected')
    file_list = list(result.left_only)
    file_list.extend(x for x in result.diff_files if x not in file_list)

    for file in file_list:
        print(f'Copying {file} to extensions folder')
        src_file = os.path.join(javascript_folder, file)
        dst_file = os.path.join(extentions_folder, file)
        if os.path.exists(dst_file):
            os.remove(dst_file)
        #print("disabled")
        shutil.copy(src_file, dst_file)

version_code = [0, 0, 1]
version_str = f"V{version_code[0]}.{version_code[1]}" + (f'.{version_code[2]}' if len(version_code) > 2 else '')
print(f"### Loading: ConfyUI_DG_Llama3_2_PromptGen ({version_str})")

node_list = [
    "DG_LLAMA_PROMPTGEN"
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    import comfy.utils
except ImportError:
    pass
else:
    from .DG_LLAMA_PROMPTGEN import NODE_CLASS_MAPPINGS
    #NODE_DISPLAY_NAME_MAPPINGS = {k:v.TITLE for k,v in NODE_CLASS_MAPPINGS.items()}
    for module_name in node_list:
        imported_module = importlib.import_module(".{}".format(module_name), __name__)

        NODE_DISPLAY_NAME_MAPPINGS = {k:v.TITLE for k,v in NODE_CLASS_MAPPINGS.items()}
        __all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
        #NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
        #NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}