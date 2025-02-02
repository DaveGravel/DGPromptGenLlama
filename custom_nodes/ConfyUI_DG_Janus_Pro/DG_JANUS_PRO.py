"""
@author: Dave Gravel
@title: ComfyUI OrionX3D Nodes
@web: https://www.youtube.com/@EvadLevarg/videos
@facebook: https://www.facebook.com/dave.gravel1
@nickname: k00m, Evados
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
import sys
import os
import re
import torch
import math
import platform
import random
import time
#import json
from datetime import datetime
#import nodes
#import time
#import copy
import numpy as np
import torch.nn.functional as F
#import comfy.diffusers_load
#import comfy.samplers
import comfy.sample
import comfy.sd
import comfy.utils
import comfy.latent_formats
import comfy.model_base
import comfy.model_management
import comfy.model_patcher
import comfy.model_sampling	
from nodes import MAX_RESOLUTION
from PIL import Image
#
import folder_paths
#from folder_paths import base_path
from folder_paths import get_filename_list
from .lib.cache import cleanGPUUsedForce, remove_cache, update_cache
#
#sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
#print(f"OrionX3D lib path: {sys.path}")
#
#import json
#import configparser

from transformers import AutoTokenizer, AutoModelForCausalLM, AutoProcessor

# https://github.com/deepseek-ai/Janus
try:
    from janus.models import MultiModalityCausalLM, VLChatProcessor
    from janus.utils.io import load_pil_images
except ImportError:
    raise ImportError("Install Janus using 'pip install -r requirements-windows.txt'")    

import bitsandbytes

current_dir = os.path.dirname(os.path.abspath(__file__))
current_modeldir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Models")
print(f"OrionX3D Répertoire actuel DG Janus Pro nodes : {current_dir}")

#config = configparser.ConfigParser()
#config.read(os.path.join(current_dir, "dg_llama_managers.cfg"))

if not os.path.exists(current_modeldir):
    os.makedirs(current_modeldir)

print(f"OrionX3D Répertoire actuel pour le model Janus Pro : {current_modeldir}")

folder_paths.add_model_folder_path("dg_janus_model", current_modeldir, is_default=False)
folder_paths.add_model_folder_path("dg_janus", current_dir, is_default=False)

def extract_person_name(filename):
    match = re.search(r'agent_(\w+)_\w+\.agt', filename)
    if match:
        return match.group(1)
    return ""

def extract_version(filename):
    match = re.search(r'agent_\w+_(normal|uncensored)\.agt', filename)
    if match:
        return match.group(1)  # Retourne "normal" ou "uncensored"
    return "unknown"  # Si le format ne correspond pas

def rand_seeder(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

def empty_cache(unique_id=None, extra_pnginfo=None):
    cleanGPUUsedForce()
    remove_cache('*')

def get_filtered_janus_filenames(alias, extensions=None):
    all_files = folder_paths.get_filename_list(alias)
    
    # Filtrer les fichiers contenant "deepseek" (insensible à la casse)
    filtered_files = [file for file in all_files if "janus" in file.lower()]
    
    # Si aucune extension n'est spécifiée, retourner les fichiers filtrés
    if extensions is None:
        return filtered_files

    # Filtrer selon les extensions spécifiées
    return [
        file
        for file in filtered_files
        if os.path.splitext(file)[1] in extensions
    ]

#####################################################################################################################
# DGLoadJanusProModel ###############################################################################################
#####################################################################################################################
class DGLoadJanusProModel:
    def __init__(self):
        self.proc = None
        self.model = None        
        self.model_name = ""
        self.model_check = 0
        self.device_name = "cpu"
        self.model_file = ""
        # I think I need the flash_attention_2 for load other models, but if i'm not wrong the flash_attention_2 don't work on windows for now.
        # Or if it working it is a bit tricky to install because you need to install a precompiled version.
        #self.model_type = "Janus"
        self.offload_device = torch.device('cpu')
        self.clear_extra_mem_gpu = "Yes"
        
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model_file": (get_filtered_janus_filenames("dg_janus_model", extensions=['.bin', '.gguf', '.safetensors']), {"tooltip": "Janus Pro Model 1b 7b."}),
                "reset_model": (["No", "Yes"], {"tooltip": "When you reset the model by selecting 'Yes' Press Queue Prompt to reset the model, remember to set it back to 'No' afterward."}),
                "use_bit_mode": (["4bit","8bit", "nobit"], {"tooltip": "This option don't work with GGUF Model because GGUF model already use an other type of compression."}),
                "device_mode": (["auto", "gpu", "cpu"],),
                #"model_type": (["Janus", "JanusFlow", "Janus-Pro"],),
                "clear_extra_mem_gpu": (["Yes", "No"], {"tooltip": "Try to clean a bit a vram when processing text."}),
            },
        }
    
    RETURN_TYPES = ("ANY",)
    RETURN_NAMES = ("janus_pipe",)
    FUNCTION = "load_model"
    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLoadJanusProModel (Janus Pro - OX3D)" 

    #model_type
    def load_model(self, model_file, use_bit_mode, reset_model, device_mode, clear_extra_mem_gpu):
        self.clear_extra_mem_gpu = clear_extra_mem_gpu
        #self.model_type = model_type
        print(f"OrionX3D Janus Pro Model: {model_file}")
        self.model_name = os.path.basename(model_file)
        print(f"OrionX3D base Janus Pro Model: {self.model_name}")
        amodel_file = os.path.join(current_modeldir, os.path.dirname(model_file))
        print(f"OrionX3D dir Janus Pro Model: {amodel_file}")

        if self.model_file != model_file: 
            self.model_file = model_file
            self.proc = None
            self.model = None         

        if reset_model == "Yes":
            self.proc = None
            self.model = None             

        if self.proc is None and self.model is None:
            load_in_4bit = False
            load_in_8bit = False
            model_check = 0

            # Extraire uniquement l'extension
            print(f"OrionX3D Janus Pro Model New: {self.model_file}")
            file_extension = os.path.splitext(self.model_file)[-1].lower()

            if file_extension == ".gguf":
                print("The Model janus pro is a .gguf file.")
                model_check = 1
            elif file_extension == ".safetensors":
                print("The Model janus pro is a .safetensors file.")
                model_check = 2
            elif file_extension == ".bin":
                print("The Model janus pro is a .bin file.")
                model_check = 3
            else:
                print("The Model janus pro has a different extension.")  
                model_check = 0

            self.model_check = model_check
            
            if use_bit_mode == "4bit":
                load_in_4bit = True
                load_in_8bit = False
            if use_bit_mode == "8bit":
                load_in_4bit = False
                load_in_8bit = True   
            if use_bit_mode == "nobit":
                load_in_4bit = False
                load_in_8bit = False   

            if device_mode == "cpu":
                self.offload_device = torch.device('cpu')
                self.device_name = "cpu"
            elif device_mode == "cuda":
                self.offload_device = torch.device('cuda')
                self.device_name = "cuda"
            elif device_mode == "auto":
                self.offload_device = "auto"
                self.device_name = "auto"                       

            if device_mode == "auto":
                device = "cuda" 
                self.device_name = "cuda"
            else:
                device = self.device_name
        
            try:
                dtype = torch.bfloat16
                torch.zeros(1, dtype=dtype, device=device)
            except RuntimeError:
                dtype = torch.float16
            #
            if self.model_check == 1:
                # Don't look to work with the gguf file for now.
                # Or I don't have find how to load it correctly.
                # I think it can only load with llama.cpp for now.
                # W.I.P
                self.proc = VLChatProcessor.from_pretrained(amodel_file, 
                                                            gguf_file=self.model_name,
                                                            trust_remote_code=True,
                                                            local_files_only=True)                
                self.model = AutoModelForCausalLM.from_pretrained(amodel_file, 
                                                                  gguf_file=self.model_name, 
                                                                  trust_remote_code=True,
                                                                  local_files_only=True,   
                                                                  torch_dtype=dtype,
                                                                  device_map=self.offload_device) 
            else:
                self.proc = VLChatProcessor.from_pretrained(amodel_file, 
                                                            trust_remote_code=True,
                                                            local_files_only=True)                
                #self.model: MultiModalityCausalLM = AutoModelForCausalLM.from_pretrained(amodel_file, 
                self.model = AutoModelForCausalLM.from_pretrained(amodel_file,
                                                                  trust_remote_code=True,
                                                                  local_files_only=True,   
                                                                  torch_dtype=dtype,
                                                                  device_map=self.offload_device,
                                                                  load_in_8bit=load_in_8bit,
                                                                  load_in_4bit=load_in_4bit #,
                                                                  #attn_implementation="flash_attention_2"
                                                                  )  
                   
            #self.model = self.model.to(dtype).to(device).eval()
        return (self,)  
     
#####################################################################################################################
# DGJanusProImageVision #############################################################################################
#####################################################################################################################
class DGJanusProImageVision:
    def __init__(self):
        self.proc = None
        self.model = None        
        self.model_name = ""        
        self.oldseed = -1
        self.useseed = True
        self.seed = -1  
        self.response = ""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "janus_pipe": ("ANY",),
                "image": ("IMAGE",),
                #"use_vision": (["Yes", "No"],),
                "question": ("STRING", {"multiline": True, "default": "Provide a detailed descriptive text prompt for this image." }),
                "use_seeder": (["Yes", "No"],),
                "seeder": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "temperature": ("FLOAT", {"default": 0.1,"min": 0.0,"max": 1.0}),
                "top_p": ("FLOAT", {"default": 0.95,"min": 0.0,"max": 1.0}),
                "max_new_tokens": ("INT", {"default": 512, "min": 1, "max": 4096}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "image_vision"
    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGJanusProImageVision (Janus Pro - OX3D)"

    #use_vision
    def image_vision(self, janus_pipe, image, question, seeder, use_seeder, temperature, top_p, max_new_tokens):
        self.proc = janus_pipe.proc
        self.model = janus_pipe.model        
        self.model_name = janus_pipe.model_name  

        use_vision = "Yes"

        if self.proc is not None and self.model is not None:
            nseed = seeder

            if nseed <= 0:
                nseed = random.randint(1, 100)

            if self.oldseed != nseed:
                self.oldseed = nseed
                random.seed(time.time())   
        
            if use_seeder == "Yes":
                self.useseed = True
                self.seed = self.oldseed

                rand_seeder(nseed - (nseed // 9999999) * 9999999)
            else:
                self.useseed = False         

            # BCHW (Batch, Channel, Height, Width)
            if len(image.shape) == 4:
                if image.shape[0] == 1:
                    image = image.squeeze(0) 
        
            image = (torch.clamp(image, 0, 1) * 255).cpu().numpy().astype(np.uint8)
        
            pil_images = Image.fromarray(image, mode='RGB')

            #conversation = [
            #    {"role": "<|User|>", "content": f"<image_placeholder>\n{question}", "images": [pil_image],},
            #    {"role": "<|Assistant|>", "content": ""},
            #]

            conversation = [
                {"role": "<|User|>", "content": f"<image_placeholder>\n{question}", "images": [pil_images],},
                {"role": "<|Assistant|>", "content": ""},
            ]            

            #pil_images = load_pil_images(conversation)

            prepare_inputs = self.proc(
                conversations=conversation, 
                images=[pil_images], 
                force_batchify=True
            ).to(self.model.device)

            inputs_embeds = self.model.prepare_inputs_embeds(**prepare_inputs)

            outputs = self.model.language_model.generate(
                inputs_embeds=inputs_embeds,
                attention_mask=prepare_inputs.attention_mask,
                pad_token_id=self.proc.tokenizer.eos_token_id,
                bos_token_id=self.proc.tokenizer.bos_token_id,
                eos_token_id=self.proc.tokenizer.eos_token_id,
                max_new_tokens=max_new_tokens,
                do_sample=self.useseed,
                temperature=temperature,
                top_p=top_p,
                use_cache=True,
            )

            self.response = self.proc.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)               

            self.oldseed = seeder

        if janus_pipe.clear_extra_mem_gpu == "Yes":  
            torch.cuda.empty_cache()
            empty_cache()              
 
        return (self.response,)
    
#####################################################################################################################
# DGJanusProImageGenerator ##########################################################################################
#####################################################################################################################
class DGJanusProImageGenerator:
    def __init__(self):        
        self.proc = None
        self.model = None        
        self.model_name = "" 
        self.oldseed = -1
        self.useseed = True
        self.seed = -1  

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "janus_pipe": ("ANY",),
                "prompt": ("STRING", {"multiline": True, "default": "A stunning princess from kabul in red, white traditional clothing, blue eyes, brown hair."}),
                "use_seeder": (["Yes", "No"],),
                "seeder": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "batch_size": ("INT", {"default": 1, "min": 1, "max": 16}),
                "cfg_weight": ("FLOAT", {"default": 5.0, "min": 1.0, "max": 10.0, "step": 0.5}),
                "temperature": ("FLOAT", {"default": 1.0, "min": 0.1, "max": 2.0, "step": 0.1}),
                #"top_p": ("FLOAT", {"default": 0.95, "min": 0.0, "max": 1.0}),
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "generate_images"
    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGJanusProImageGenerator (Janus Pro - OX3D)"

    #, top_p=0.95
    def generate_images(self, janus_pipe, prompt, seeder, use_seeder, batch_size=1, temperature=1.0, cfg_weight=5.0):
        images = None

        self.proc = janus_pipe.proc
        self.model = janus_pipe.model
        self.model_name = janus_pipe.model_name 

        if self.proc is not None and self.model is not None:
            # Gestion du seed
            nseed = seeder if seeder > 0 else random.randint(1, 100)
    
            if self.oldseed != nseed:
                self.oldseed = nseed
                random.seed(time.time())
    
            self.useseed = use_seeder == "Yes"
            if self.useseed:
                self.seed = self.oldseed
                rand_seeder(nseed % 9999999)
    
            image_token_num_per_image = 576
            img_size = 384 
            patch_size = 16 
            parallel_size = batch_size
    
            # Formatage du prompt
            conversation = [{"role": "<|User|>", "content": prompt}, {"role": "<|Assistant|>", "content": ""}]
            sft_format = self.proc.apply_sft_template_for_multi_turn_prompts(conversations=conversation, sft_format=self.proc.sft_format, system_prompt="")
            prompt = sft_format + self.proc.image_start_tag
     
            input_ids = self.proc.tokenizer.encode(prompt)
            input_ids = torch.LongTensor(input_ids)
            
            tokens = torch.zeros((parallel_size*2, len(input_ids)), dtype=torch.int).cuda()
            for i in range(parallel_size*2):
                tokens[i, :] = input_ids
                if i % 2 != 0:
                    tokens[i, 1:-1] = self.proc.pad_id            

            inputs_embeds = self.model.language_model.get_input_embeddings()(tokens)

            generated_tokens = torch.zeros((parallel_size, image_token_num_per_image), dtype=torch.int, device=janus_pipe.device_name)
    
            for i in range(image_token_num_per_image):
                outputs = self.model.language_model.model(inputs_embeds=inputs_embeds, use_cache=True, past_key_values=outputs.past_key_values if i != 0 else None) # type: ignore
                hidden_states = outputs.last_hidden_state

                logits = self.model.gen_head(hidden_states[:, -1, :])
                logit_cond = logits[0::2, :]
                logit_uncond = logits[1::2, :]                
        
                logits = logit_uncond + cfg_weight * (logit_cond-logit_uncond)
                probs = torch.softmax(logits / temperature, dim=-1)

                next_token = torch.multinomial(probs, num_samples=1)
                generated_tokens[:, i] = next_token.squeeze(dim=-1)

                next_token = torch.cat([next_token.unsqueeze(dim=1), next_token.unsqueeze(dim=1)], dim=1).view(-1)
                img_embeds = self.model.prepare_gen_img_embeds(next_token)
                inputs_embeds = img_embeds.unsqueeze(dim=1) 

            # Décodage des images
            dec = self.model.gen_vision_model.decode_code(generated_tokens.to(dtype=torch.int), shape=[parallel_size, 8, img_size // patch_size, img_size // patch_size]).float().cpu().numpy()
    
            if dec.shape[1] != 3:
                dec = np.repeat(dec, 3, axis=1)
    
            dec = np.clip((dec + 1) / 2, 0, 1)
            images = torch.from_numpy(np.transpose(dec, (0, 2, 3, 1))).float()
    
            self.oldseed = seeder

            assert images.ndim == 4 and images.shape[-1] == 3, f"Unexpected shape: {images.shape}"
        
        if janus_pipe.clear_extra_mem_gpu == "Yes":  
            torch.cuda.empty_cache()
            empty_cache()    

        return images,
        
#####################################################################################################################
# Register Class ####################################################################################################
#####################################################################################################################    

NODE_CLASS_MAPPINGS = {
    "DGLoadJanusProModel": DGLoadJanusProModel,
    "DGJanusProImageVision": DGJanusProImageVision,
    "DGJanusProImageGenerator": DGJanusProImageGenerator,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DGLoadJanusProModel //OrionX3D": "DGLoadJanusProModel (💫🅞🅧3🅓)",    
    "DGJanusProImageVision //OrionX3D": "DGJanusProImageVision (💫🅞🅧3🅓)", 
    "DGJanusProImageGenerator //OrionX3D": "DGJanusProImageGenerator (💫🅞🅧3🅓)", 
}