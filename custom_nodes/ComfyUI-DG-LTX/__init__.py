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
# temporary D.G
#from .config import ORIONX3D_CONFIG

THIS_DIR=os.path.dirname(os.path.abspath(__file__))

# Récupérer le chemin absolu du répertoire actuel du script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construire le chemin absolu vers le répertoire que vous voulez atteindre
target_dir = os.path.abspath(os.path.join(current_dir, '..', '..'))

# Ajouter le chemin du répertoire à sys.path
sys.path.append(target_dir)

print(f"OrionX3D ComfyUI Folder: {target_dir}")

version_code = [0, 0, 2]
version_str = f"V{version_code[0]}.{version_code[1]}" + (f'.{version_code[2]}' if len(version_code) > 2 else '')
print(f"### Loading: ConfyUI_DG_LTX_PLUS ({version_str})")

node_list = [
    "DG_LTX_PLUS"
]

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

try:
    import comfy.utils
except ImportError:
    pass
else:
    from .DG_LTX_PLUS import NODE_CLASS_MAPPINGS
    #NODE_DISPLAY_NAME_MAPPINGS = {k:v.TITLE for k,v in NODE_CLASS_MAPPINGS.items()}
    for module_name in node_list:
        # dossier ou sont les source py, il y a juste . car il va au folder de base ...
        imported_module = importlib.import_module(".{}".format(module_name), __name__)

        NODE_CLASS_MAPPINGS = {**NODE_CLASS_MAPPINGS, **imported_module.NODE_CLASS_MAPPINGS}
        NODE_DISPLAY_NAME_MAPPINGS = {**NODE_DISPLAY_NAME_MAPPINGS, **imported_module.NODE_DISPLAY_NAME_MAPPINGS}