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
#
import folder_paths
#from folder_paths import base_path
from folder_paths import get_filename_list
#
#sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))
#print(f"OrionX3D lib path: {sys.path}")
#
from .lib.data import get_prompt_vehicles, video_styles
from .lib.data import SysTypes, dg_llama_format_prompt
from .lib.data import prompt_translationExp, prompt_correctionsExp, prompt_translation, prompt_corrections, prompt_instructionsExp, prompt_instructions
from .lib.data import generate_prompt_styleMix, generate_prompt_style, get_prompt_styles, clean_prompt_regex, remove_parentheses, empty_cache, get_filtered_filenames, generate_prompt_colors, get_prompt_colors
from .lib.data import get_prompt_nationalities, get_prompt_gods, get_prompt_hairs, get_prompt_humanhybrides, generate_prompt_nationalities, generate_prompt_gods, generate_prompt_hairs, generate_prompt_humanhybrides
from .lib.data import remove_leading_spaces, load_text_from_file, process_prompt_v2, get_random_action, generate_prompt_vehicles, remove_spaces, remove_spaces_lines, create_agent_geraldine_text, create_agent_dave_text
from .lib.data import generate_prompt_colorExt, get_prompt_colorExt, generate_prompt_weapons, get_prompt_weapons, remove_spaces_lines_total, generate_robot_name, insert_line_after_first
from .lib.data import eng_law, cons_law, ox3d_user_name, DG_LlamaTextBuffer, get_filtered_deep_filenames, get_filtered_llama_filenames
from .lib.data import get_prompt_establishment_objects, get_prompt_room_objects, get_prompt_positive_words_sports, get_prompt_words_sports, get_prompt_positive_signs, get_prompt_positive_words, get_prompt_bad_words_medias, get_prompt_bad_words
from .lib.data import get_prompt_dishes, get_prompt_beverages, get_prompt_daytime_moments, get_prompt_earth_elements, get_prompt_realism_styles, get_prompt_produce_list, get_prompt_photo_video_styles, get_prompt_cats, get_prompt_dogs
from .lib.data import get_prompt_birds, get_prompt_dinosaurs, get_prompt_supervillains, get_prompt_superheroes, get_prompt_bubble_keywords, get_prompt_sign_keywords, get_prompt_body_positions, get_prompt_emotion_genres, get_prompt_combat_scenarios
from .lib.data import get_prompt_short_video_scenarios, get_prompt_clothing_brands_and_styles, get_prompt_cameras_and_modes, get_prompt_photographers_and_styles, get_prompt_film_and_series_creators, get_prompt_art_styles, get_prompt_render_systems
from .lib.data import get_prompt_art_genres, get_prompt_gaming_consoles, get_prompt_alien_species, get_prompt_nighttime_styles, get_prompt_daytime_styles, get_prompt_world_religions, get_prompt_biblical_moments, get_prompt_time_periods
from .lib.data import get_prompt_professions, get_prompt_combat_actions, get_prompt_actions_styles, get_prompt_wonders_of_the_world, get_prompt_monsters, get_prompt_celestial_objects, get_prompt_protection_types, get_prompt_shield_types, get_prompt_building_types
from .lib.data import generate_prompt_establishment_objects_media, generate_prompt_room_objects, generate_prompt_positive_words_sports, generate_prompt_words_sports, generate_prompt_positive_signs, generate_prompt_positive_words, generate_prompt_bad_words_medias
from .lib.data import generate_prompt_bad_words, generate_prompt_dishes, generate_prompt_beverages, generate_prompt_daytime_moments, generate_prompt_earth_elements, generate_prompt_realism_styles, generate_prompt_produce_list, generate_prompt_photo_video_styles
from .lib.data import generate_prompt_cats, generate_prompt_dogs, generate_prompt_birds, generate_prompt_dinosaurs, generate_prompt_supervillains, generate_prompt_superheroes, generate_prompt_bubble_keywords, generate_prompt_sign_keywords, generate_prompt_body_positions
from .lib.data import generate_prompt_emotion_genres, generate_prompt_combat_scenarios, generate_prompt_short_video_scenarios, generate_prompt_clothing_brands_and_styles, generate_prompt_cameras_and_modes, generate_prompt_photographers_and_styles, generate_prompt_film_and_series_creators
from .lib.data import generate_prompt_art_styles, generate_prompt_render_systems, generate_prompt_art_genres, generate_prompt_gaming_consoles, generate_prompt_alien_species, generate_prompt_nighttime_styles, generate_prompt_daytime_styles, generate_prompt_world_religions
from .lib.data import generate_prompt_biblical_moments, generate_prompt_time_periods, generate_prompt_professions, generate_prompt_combat_actions, generate_prompt_actions_styles, generate_prompt_wonders_of_the_world, generate_prompt_monsters, generate_prompt_celestial_objects
from .lib.data import generate_prompt_protection_types, generate_prompt_shield_types, generate_prompt_building_types, get_prompt_art_styles2, generate_prompt_art_styles2, extract_think_and_response, format_prompt_gguf, extract_sections_gguf, extract_sections_gguf2, format_prompt_gguf2, format_prompt_gguf3
#
import json
import configparser

from transformers import AutoTokenizer, AutoModelForCausalLM, LlamaForCausalLM, AutoProcessor
import bitsandbytes

#from transformers import ToolCollection, ReactCodeAgent

"""
# Vérifier le système d'exploitation
if platform.system() == "Linux":
    try:
        import flash_attn
        print("OrionX3D llama 3.2 flash_attn importé avec succès.")
    except ImportError:
        print("OrionX3D llama 3.2 flash_attn n'est pas disponible sur ce système.")
else:
    print("OrionX3D llama 3.2 flash_attn n'est pas supporté sur ce système d'exploitation.")   
"""

current_dir = os.path.dirname(os.path.abspath(__file__))
current_modeldir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Models")
print(f"OrionX3D Répertoire actuel llama 3.2 node : {current_dir}")

config = configparser.ConfigParser()
config.read(os.path.join(current_dir, "dg_llama_managers.cfg"))

if not os.path.exists(current_modeldir):
    os.makedirs(current_modeldir)

#model_path = config.get('modelfolder', 'model_path')

#current_modeldir = os.path.join(current_modeldir, model_path)

print(f"OrionX3D Répertoire actuel pour le model llama 3.2 GGUF : {current_modeldir}")

folder_paths.add_model_folder_path("dg_llama3_2", current_modeldir, is_default=False)
folder_paths.add_model_folder_path("dg_llama_agents", current_dir, is_default=False)

str_assistant = ""

str_agent = ""

str_agent_remove = ""

SysType = SysTypes("*")

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

# I can remove it later since both classes are now the same.
# I only need one base class.
# For now, I’m still using both, but I can merge them into one class later.
# In the old version, these two classes were slightly different.
#####################################################################################################################
# AgentGeraldine ####################################################################################################
#####################################################################################################################
# OLD BUT I KEEP IT FOR NOW
class AgentGeraldine:
    def __init__(self, ox3d_user_name, current_dir, tokenizer, max_tokens):
        self.ox3d_user_name = ox3d_user_name
        self.current_dir = current_dir
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.text_buffer = DG_LlamaTextBuffer(ox3d_user_name, self.tokenizer, self.max_tokens)  

    def save_agent_text(self, filename, uncensored=False, agent_str: str = ""):
        filepath = os.path.join(self.current_dir, filename)
        if not os.path.exists(filepath):
            if agent_str == "":
                text = create_agent_geraldine_text(uncensored)
            else:
                text = agent_str 
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"OX3D Agent File saved: {filepath}")
        else:
            pass
            #print(f"OX3D Agent File already exists: {filepath}")

    def load_agent_text(self, filename):
        filepath = os.path.join(self.current_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read().replace("{ox3d_user_name}", self.ox3d_user_name)
        else:
            raise FileNotFoundError(f"OX3D The Agent file {filepath} does not exist.") 
        
#####################################################################################################################
# DGAgentDave #######################################################################################################
#####################################################################################################################
# OLD BUT I KEEP IT FOR NOW
class AgentDave:
    def __init__(self, ox3d_user_name, current_dir, tokenizer, max_tokens):
        self.ox3d_user_name = ox3d_user_name
        self.current_dir = current_dir
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.text_buffer = DG_LlamaTextBuffer(ox3d_user_name, self.tokenizer, self.max_tokens)

    def save_agent_text(self, filename, uncensored=False, agent_str: str = ""):
        filepath = os.path.join(self.current_dir, filename)
        if not os.path.exists(filepath):
            if agent_str == "":
                text = create_agent_geraldine_text(uncensored)
            else:
                text = agent_str 
            with open(filepath, 'w', encoding='utf-8') as file:
                file.write(text)
            print(f"OX3D Agent File saved: {filepath}")
        else:
            pass
            #print(f"OX3D Agent File already exists: {filepath}")

    def load_agent_text(self, filename):
        filepath = os.path.join(self.current_dir, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as file:
                return file.read().replace("{ox3d_user_name}", self.ox3d_user_name)
        else:
            raise FileNotFoundError(f"OX3D The Agent file {filepath} does not exist.")  

#####################################################################################################################
# DGLlamaChatAgent ##################################################################################################
##################################################################################################################### 
class DGLlamaChatAgent:
    def __init__(self, llama3_pipe, agent_name, agent_mode, system_prompt: str):
        if llama3_pipe is None:
            raise ValueError("The pipeline cannot be None.")
        
        if system_prompt is None or system_prompt.strip() == '':
            raise ValueError("The system_prompt must not be empty or contain only whitespace.")
        
        self.llama3_pipe = llama3_pipe
        self.tokenizer = llama3_pipe.tokenizer
        self.model = llama3_pipe.model         
        self.system_prompt = system_prompt
        self.agent_name = agent_name
        self.agent_mode_restriction = agent_mode

        self.chat_history = [{"role": "system", "content": self.system_prompt}]
        
        if self.agent_mode_restriction == "uncensored":
            self.load_history(f"ox3d_llama_{self.agent_name}_chat_uncensored_history.json")
        else:
            self.load_history(f"ox3d_llama_{self.agent_name}_chat_history.json")

    def chat(self, do_rand, user_prompt: str, max_new_tokens: int = 512, temperature: float = 0.8, 
             top_k: int = 50, top_p: float = 0.9, repetition_penalty: float = 1.1) -> str:
        
        maxtokens = max_new_tokens - 1000 

        self.chat_history.append({"role": "user", "content": user_prompt})
        
        formatted_history = self._build_formatted_history()

        input_ids = self.tokenizer(formatted_history, return_tensors="pt").input_ids.to(self.llama3_pipe.device_name)
        input_token_count = input_ids.shape[-1]

        if input_token_count > maxtokens:
            self._trim_history(maxtokens)
            formatted_history = self._build_formatted_history()
            input_ids = self.tokenizer(formatted_history, return_tensors="pt").input_ids.to(self.llama3_pipe.device_name)

        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        if self.model.config.pad_token_id is None:
            self.model.config.pad_token_id = self.model.config.eos_token_id             

        generated_ids = self.model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            do_sample=do_rand,
            num_return_sequences=1
        ) #, eos_token_id=self.tokenizer.eos_token_id

        """
        if self.llama3_pipe.useseed == True:
            generated_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                repetition_penalty=repetition_penalty,
                do_sample=self.llama3_pipe.useseed,
                num_return_sequences=1
            ) #, eos_token_id=self.tokenizer.eos_token_id
        else:
            generated_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                repetition_penalty=repetition_penalty,
                do_sample=self.llama3_pipe.useseed,
                num_return_sequences=1
            ) #, eos_token_id=self.tokenizer.eos_token_id    
        """

        # add_special_tokens=False,
        outputs = self.tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
    
        if outputs.startswith(f"{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}{self.llama3_pipe.codeC}"):
            outputs = outputs[len(f"{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}{self.llama3_pipe.codeC}"):].strip()

        self.chat_history.append({"role": f"{self.llama3_pipe.modeC}", "content": outputs})

        if self.agent_mode_restriction == "uncensored":
            self.save_history(f"ox3d_llama_{self.agent_name}_chat_uncensored_history.json")
        else:
            self.save_history(f"ox3d_llama_{self.agent_name}_chat_history.json")

        self.save_prompt_log(user_prompt, outputs)

        return outputs

    def _update_agent_name(self, agtname):
        self.agent_name = agtname

    def _update_agent_mode(self, agtmode):
        self.agent_mode_restriction = agtmode

    def _build_formatted_history(self) -> str:
        formatted_history = f"{self.llama3_pipe.codeA}"
        for message in self.chat_history:
            formatted_history += f"{self.llama3_pipe.codeB}{message['role']}{self.llama3_pipe.codeC}\n{message['content']}\n{self.llama3_pipe.codeD}"
        formatted_history += f"{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}{self.llama3_pipe.codeC}"
        return formatted_history

    def _trim_history(self, max_tokens: int):
        while True:
            formatted_history = self._build_formatted_history()
            input_ids = self.tokenizer(formatted_history, return_tensors="pt").input_ids.to(self.llama3_pipe.device_name)
            input_token_count = input_ids.shape[-1]

            if input_token_count <= max_tokens:
                break

            if len(self.chat_history) > 1:
                self.chat_history.pop(1)

    def reset_history(self, file_name: str = "chat_history.json", keep_system_prompt: bool = True):
        #if keep_system_prompt:
        self.chat_history = [{"role": "system", "content": self.system_prompt}]
        #else:
        #    self.chat_history = []
        self.save_history(file_name)                

    def print_current_history(self):
        print(json.dumps(self.chat_history, indent=2))  

    def print_current_history_tokens(self):
        formatted_history = self._build_formatted_history()
        input_ids = self.tokenizer(formatted_history, return_tensors="pt").input_ids
        token_count = input_ids.shape[-1]
        print(f"Chat History (tokens count: {token_count}):")
        print(json.dumps(self.chat_history, indent=2))

    def save_history(self, file_name: str):
        file_path = os.path.join(current_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.chat_history, file, ensure_ascii=False, indent=4)

    def load_history(self, file_name: str):
        file_path = os.path.join(current_dir, file_name)
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Skipping load.")
            return 

        with open(file_path, 'r', encoding='utf-8') as file:
            self.chat_history = json.load(file)

        if len(self.chat_history) == 0 or self.chat_history[0]["role"] != "system":
            raise ValueError("Invalid chat history: missing system prompt.") 

    def save_prompt_log(self, user_prompt: str, assistant_response: str):
        logs_dir = os.path.join(current_dir, "prompt_logs")
        os.makedirs(logs_dir, exist_ok=True)

        today_date = datetime.now().strftime("%Y-%m-%d")
        date_dir = os.path.join(logs_dir, today_date)
        os.makedirs(date_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%H-%M-%S")
        log_file_name = f"prompt_{timestamp}.json"
        log_file_path = os.path.join(date_dir, log_file_name)

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "user_prompt": user_prompt,
            "assistant_response": assistant_response,
        }

        with open(log_file_path, "w", encoding="utf-8") as log_file:
            json.dump(log_data, log_file, ensure_ascii=False, indent=4)   

#####################################################################################################################
# DGDeepSeekChatAgent ###############################################################################################
##################################################################################################################### 
class DGDeepSeekChatAgent:
    def __init__(self, deepseek_pipe, agent_name, agent_mode, system_prompt: str):
        if deepseek_pipe is None:
            raise ValueError("The pipeline cannot be None.")
        
        if system_prompt is None or system_prompt.strip() == '':
            raise ValueError("The system_prompt must not be empty or contain only whitespace.")
        
        self.deepseek_pipe = deepseek_pipe
        self.tokenizer = deepseek_pipe.tokenizer
        self.model = deepseek_pipe.model         
        self.system_prompt = system_prompt
        self.agent_name = agent_name
        self.agent_mode_restriction = agent_mode

        self.chat_history = [{"role": "system", "content": self.system_prompt}]
        
        #if self.agent_mode_restriction == "uncensored":
        #    self.load_history(f"ox3d_llama_{self.agent_name}_chat_uncensored_history.json")
        #else:
        #    self.load_history(f"ox3d_llama_{self.agent_name}_chat_history.json")

    def chat(self, user_prompt: str, max_new_tokens: int = 512, temperature: float = 0.8, 
             top_k: int = 50, top_p: float = 0.9, repetition_penalty: float = 1.1) -> str:
        
        self.chat_history.append({"role": "user", "content": user_prompt})
        
        formatted_history = self._build_formatted_history()

        input_ids = self.tokenizer(formatted_history, return_tensors="pt").input_ids.to(self.deepseek_pipe.device_name)
        input_token_count = input_ids.shape[-1]

        if input_token_count > max_new_tokens:
            self._trim_history(max_new_tokens)
            formatted_history = self._build_formatted_history()
            input_ids = self.tokenizer(formatted_history, return_tensors="pt").input_ids.to(self.deepseek_pipe.device_name)

        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        if self.model.config.pad_token_id is None:
            self.model.config.pad_token_id = self.model.config.eos_token_id   


        generated_ids = self.model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            repetition_penalty=repetition_penalty,
            do_sample=True, #self.llama3_pipe.useseed,
            num_return_sequences=1
        ) #, eos_token_id=self.tokenizer.eos_token_id                      
        """
        if self.llama3_pipe.useseed == True:
            generated_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                repetition_penalty=repetition_penalty,
                do_sample=True, #self.llama3_pipe.useseed,
                num_return_sequences=1
            ) #, eos_token_id=self.tokenizer.eos_token_id
        else:
            generated_ids = self.model.generate(
                input_ids,
                max_new_tokens=max_new_tokens,
                top_k=top_k,
                top_p=top_p,
                temperature=temperature,
                repetition_penalty=repetition_penalty,
                do_sample=False, #self.llama3_pipe.useseed,
                num_return_sequences=1
            ) #, eos_token_id=self.tokenizer.eos_token_id            
        """
        #add_special_tokens=False,
        outputs = self.tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
    
        #if outputs.startswith(f"{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}{self.llama3_pipe.codeC}"):
        #    outputs = outputs[len(f"{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}{self.llama3_pipe.codeC}"):].strip()

        #self.chat_history.append({"role": f"{self.llama3_pipe.modeC}", "content": outputs})

        #if self.agent_mode_restriction == "uncensored":
        #    self.save_history(f"ox3d_llama_{self.agent_name}_chat_uncensored_history.json")
        #else:
        #    self.save_history(f"ox3d_llama_{self.agent_name}_chat_history.json")

        self.save_prompt_log(user_prompt, outputs)

        return outputs

    def _update_agent_name(self, agtname):
        self.agent_name = agtname

    def _update_agent_mode(self, agtmode):
        self.agent_mode_restriction = agtmode

    def _build_formatted_history(self) -> str:
        #formatted_history = f"{self.llama3_pipe.codeA}"
        #for message in self.chat_history:
        #    formatted_history += f"{self.llama3_pipe.codeB}{message['role']}{self.llama3_pipe.codeC}\n{message['content']}\n{self.llama3_pipe.codeD}"
        #formatted_history += f"{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}{self.llama3_pipe.codeC}"
        return "" #formatted_history

    def _trim_history(self, max_tokens: int):
        while True:
            formatted_history = self._build_formatted_history()
            input_ids = self.tokenizer(formatted_history, return_tensors="pt").input_ids.to(self.deepseek_pipe.device_name)
            input_token_count = input_ids.shape[-1]

            if input_token_count <= max_tokens:
                break

            if len(self.chat_history) > 1:
                self.chat_history.pop(1)

    def reset_history(self, file_name: str = "chat_history.json", keep_system_prompt: bool = True):
        #if keep_system_prompt:
        self.chat_history = [{"role": "system", "content": self.system_prompt}]
        #else:
        #    self.chat_history = []
        self.save_history(file_name)                

    def print_current_history(self):
        print(json.dumps(self.chat_history, indent=2))  

    def print_current_history_tokens(self):
        formatted_history = self._build_formatted_history()
        input_ids = self.tokenizer(formatted_history, return_tensors="pt").input_ids
        token_count = input_ids.shape[-1]
        print(f"Chat History (tokens count: {token_count}):")
        print(json.dumps(self.chat_history, indent=2))

    def save_history(self, file_name: str):
        file_path = os.path.join(current_dir, file_name)
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(self.chat_history, file, ensure_ascii=False, indent=4)

    def load_history(self, file_name: str):
        file_path = os.path.join(current_dir, file_name)
        if not os.path.exists(file_path):
            print(f"File {file_path} does not exist. Skipping load.")
            return 

        with open(file_path, 'r', encoding='utf-8') as file:
            self.chat_history = json.load(file)

        if len(self.chat_history) == 0 or self.chat_history[0]["role"] != "system":
            raise ValueError("Invalid chat history: missing system prompt.") 

    def save_prompt_log(self, user_prompt: str, assistant_response: str):
        logs_dir = os.path.join(current_dir, "prompt_logs")
        os.makedirs(logs_dir, exist_ok=True)

        today_date = datetime.now().strftime("%Y-%m-%d")
        date_dir = os.path.join(logs_dir, today_date)
        os.makedirs(date_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%H-%M-%S")
        log_file_name = f"prompt_{timestamp}.json"
        log_file_path = os.path.join(date_dir, log_file_name)

        log_data = {
            "timestamp": datetime.now().isoformat(),
            "user_prompt": user_prompt,
            "assistant_response": assistant_response,
        }

        with open(log_file_path, "w", encoding="utf-8") as log_file:
            json.dump(log_data, log_file, ensure_ascii=False, indent=4)  

#####################################################################################################################
# DGLlamaStyles #####################################################################################################
#####################################################################################################################

class DGLlamaStyles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_4": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_4": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_5": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_5": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),  
                "styles_variation_6": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_6": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_7": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_7": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_8": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_8": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_9": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_9": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_10": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_10": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                             
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, style_seed, prompt_mode, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3, styles_variation_4, prompt_styles_4, styles_variation_5, prompt_styles_5, styles_variation_6, prompt_styles_6, styles_variation_7, prompt_styles_7, styles_variation_8, prompt_styles_8, styles_variation_9, prompt_styles_9, styles_variation_10, prompt_styles_10):  
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_styleMix(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_styleMix(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_styleMix(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = "" 
        if prompt_styles_4 != "Other": 
            style4 = generate_prompt_styleMix(prompt_styles_4, media_type=prompt_mode, num_keywords=styles_variation_4)
        else:
            style4 = ""
        if prompt_styles_5 != "Other":     
            style5 = generate_prompt_styleMix(prompt_styles_5, media_type=prompt_mode, num_keywords=styles_variation_5)
        else:
            style5 = ""
        if prompt_styles_6 != "Other":
            style6 = generate_prompt_styleMix(prompt_styles_6, media_type=prompt_mode, num_keywords=styles_variation_6)
        else:
            style6 = ""
        if prompt_styles_7 != "Other":
            style7 = generate_prompt_styleMix(prompt_styles_7, media_type=prompt_mode, num_keywords=styles_variation_7)
        else:
            style7 = "" 
        if prompt_styles_8 != "Other":
            style8 = generate_prompt_styleMix(prompt_styles_8, media_type=prompt_mode, num_keywords=styles_variation_8)
        else:
            style8 = "" 
        if prompt_styles_9 != "Other": 
            style9 = generate_prompt_styleMix(prompt_styles_9, media_type=prompt_mode, num_keywords=styles_variation_9)
        else:
            style9 = ""
        if prompt_styles_10 != "Other":     
            style10 = generate_prompt_styleMix(prompt_styles_10, media_type=prompt_mode, num_keywords=styles_variation_10)
        else:
            style10 = ""            

        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}\n{style4}\n{style5}\n{style6}\n{style7}\n{style8}\n{style9}\n{style10}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,) 

#####################################################################################################################
# DGLlamaStyleColors ################################################################################################
#####################################################################################################################

class DGLlamaStyleColors:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 8, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_colors(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 8, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_colors(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 8, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_colors(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_4": ("INT", {"default": 1, "min": 1, "max": 8, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_4": (get_prompt_colors(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_5": ("INT", {"default": 1, "min": 1, "max": 8, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_5": (get_prompt_colors(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleColors (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3, styles_variation_4, prompt_styles_4, styles_variation_5, prompt_styles_5):    
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_colors(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_colors(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_colors(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = "" 
        if prompt_styles_4 != "Other": 
            style4 = generate_prompt_colors(prompt_styles_4, media_type=prompt_mode, num_keywords=styles_variation_4)
        else:
            style4 = ""
        if prompt_styles_5 != "Other":     
            style5 = generate_prompt_colors(prompt_styles_5, media_type=prompt_mode, num_keywords=styles_variation_5)
        else:
            style5 = ""        
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}\n{style4}\n{style5}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    
    
#####################################################################################################################
# DGLlamaStyleColorExt ##############################################################################################
#####################################################################################################################

class DGLlamaStyleColorExt:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 6, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_colorExt(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 6, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_colorExt(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 6, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_colorExt(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_4": ("INT", {"default": 1, "min": 1, "max": 6, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_4": (get_prompt_colorExt(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_5": ("INT", {"default": 1, "min": 1, "max": 6, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_5": (get_prompt_colorExt(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleColorExt (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3, styles_variation_4, prompt_styles_4, styles_variation_5, prompt_styles_5):    
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_colorExt(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_colorExt(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_colorExt(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = "" 
        if prompt_styles_4 != "Other": 
            style4 = generate_prompt_colorExt(prompt_styles_4, media_type=prompt_mode, num_keywords=styles_variation_4)
        else:
            style4 = ""
        if prompt_styles_5 != "Other":     
            style5 = generate_prompt_colorExt(prompt_styles_5, media_type=prompt_mode, num_keywords=styles_variation_5)
        else:
            style5 = ""        
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}\n{style4}\n{style5}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  
    
#####################################################################################################################
# DGLlamaStyleWeapons ##############################################################################################
#####################################################################################################################

class DGLlamaStyleWeapons:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_weapons(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_weapons(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_weapons(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_4": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_4": (get_prompt_weapons(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_5": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_5": (get_prompt_weapons(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleWeapons (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3, styles_variation_4, prompt_styles_4, styles_variation_5, prompt_styles_5):    
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_weapons(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_weapons(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_weapons(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = "" 
        if prompt_styles_4 != "Other": 
            style4 = generate_prompt_weapons(prompt_styles_4, media_type=prompt_mode, num_keywords=styles_variation_4)
        else:
            style4 = ""
        if prompt_styles_5 != "Other":     
            style5 = generate_prompt_weapons(prompt_styles_5, media_type=prompt_mode, num_keywords=styles_variation_5)
        else:
            style5 = ""        
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}\n{style4}\n{style5}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  
    

#####################################################################################################################
# DGLlamaStyleVehicles ##############################################################################################
#####################################################################################################################

class DGLlamaStyleVehicles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_vehicles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_vehicles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_vehicles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_4": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_4": (get_prompt_vehicles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_5": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_5": (get_prompt_vehicles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleVehicles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3, styles_variation_4, prompt_styles_4, styles_variation_5, prompt_styles_5):    
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_vehicles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_vehicles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_vehicles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = "" 
        if prompt_styles_4 != "Other": 
            style4 = generate_prompt_vehicles(prompt_styles_4, media_type=prompt_mode, num_keywords=styles_variation_4)
        else:
            style4 = ""
        if prompt_styles_5 != "Other":     
            style5 = generate_prompt_vehicles(prompt_styles_5, media_type=prompt_mode, num_keywords=styles_variation_5)
        else:
            style5 = ""        
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}\n{style4}\n{style5}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)     

#####################################################################################################################
# DGLlamaStyleNationalities #########################################################################################
#####################################################################################################################

class DGLlamaStyleNationalities:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_nationalities(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_nationalities(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_nationalities(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleNationalities (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):    
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_nationalities(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_nationalities(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_nationalities(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""        
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    
    
#####################################################################################################################
# DGLlamaStyleGods ##################################################################################################
#####################################################################################################################

class DGLlamaStyleGods:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_gods(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_gods(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_gods(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleGods (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):    
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_gods(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_gods(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_gods(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""         
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)   

#####################################################################################################################
# DGLlamaStyleHairs #################################################################################################
#####################################################################################################################

class DGLlamaStyleHairs:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_hairs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_hairs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_hairs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                              
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleHairs (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):    
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_hairs(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_hairs(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_hairs(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#####################################################################################################################
# DGLlamaStyleHumanHybrid ###########################################################################################
#####################################################################################################################

class DGLlamaStyleHumanHybrid:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_humanhybrides(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_humanhybrides(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_humanhybrides(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleHumanHybrid (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_humanhybrides(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_humanhybrides(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_humanhybrides(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleEstablishmentObjects ##################################################################################
#####################################################################################################################

class DGLlamaStyleEstablishmentObjects:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_establishment_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_establishment_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_establishment_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleEstablishmentObjects (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_establishment_objects_media(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_establishment_objects_media(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_establishment_objects_media(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,) 

#####################################################################################################################
# DGLlamaStyleRoomObjects ###########################################################################################
#####################################################################################################################

class DGLlamaStyleRoomObjects:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_room_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_room_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_room_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleRoomObjects (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_room_objects(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_room_objects(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_room_objects(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#####################################################################################################################
# DGLlamaStylePositiveWordsSports ###################################################################################
#####################################################################################################################

class DGLlamaStylePositiveWordsSports:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_positive_words_sports(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_positive_words_sports(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_positive_words_sports(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStylePositiveWordsSports (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_positive_words_sports(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_positive_words_sports(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_positive_words_sports(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#####################################################################################################################
# DGLlamaStyleWordsSports ###########################################################################################
#####################################################################################################################

class DGLlamaStyleWordsSports:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_words_sports(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_words_sports(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_words_sports(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleWordsSports (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_words_sports(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_words_sports(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_words_sports(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)   

#####################################################################################################################
# DGLlamaStylePositiveSigns #########################################################################################
#####################################################################################################################

class DGLlamaStylePositiveSigns:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_positive_signs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_positive_signs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_positive_signs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStylePositiveSigns (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_positive_signs(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_positive_signs(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_positive_signs(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStylePositiveWords #########################################################################################
#####################################################################################################################

class DGLlamaStylePositiveWords:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_positive_words(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_positive_words(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_positive_words(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStylePositiveWords (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_positive_words(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_positive_words(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_positive_words(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)     


#####################################################################################################################
# DGLlamaStyleBadWordsMedias ########################################################################################
#####################################################################################################################

class DGLlamaStyleBadWordsMedias:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_bad_words_medias(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_bad_words_medias(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_bad_words_medias(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleBadWordsMedias (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_bad_words_medias(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_bad_words_medias(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_bad_words_medias(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleBadWords ##############################################################################################
#####################################################################################################################

class DGLlamaStyleBadWords:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_bad_words(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_bad_words(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_bad_words(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleBadWords (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_bad_words(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_bad_words(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_bad_words(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)   

#####################################################################################################################
# DGLlamaStyleDishes ################################################################################################
#####################################################################################################################

class DGLlamaStyleDishes:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_dishes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_dishes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_dishes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleDishes (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_dishes(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_dishes(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_dishes(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)       

#####################################################################################################################
# DGLlamaStyleBeverages #############################################################################################
#####################################################################################################################

class DGLlamaStyleBeverages:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_beverages(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_beverages(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_beverages(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleBeverages (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_beverages(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_beverages(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_beverages(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleDaytimeMoments ########################################################################################
#####################################################################################################################

class DGLlamaStyleDaytimeMoments:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_daytime_moments(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_daytime_moments(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_daytime_moments(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleDaytimeMoments (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_daytime_moments(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_daytime_moments(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_daytime_moments(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,) 

#####################################################################################################################
# DGLlamaStyleEarthElements #########################################################################################
#####################################################################################################################

class DGLlamaStyleEarthElements:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_earth_elements(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_earth_elements(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_earth_elements(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleEarthElements (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_earth_elements(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_earth_elements(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_earth_elements(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)     

#####################################################################################################################
# DGLlamaStyleRealismStyles #########################################################################################
#####################################################################################################################

class DGLlamaStyleRealismStyles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_realism_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_realism_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_realism_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleRealismStyles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_realism_styles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_realism_styles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_realism_styles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)     

#####################################################################################################################
# DGLlamaStyleProduceList ###########################################################################################
#####################################################################################################################

class DGLlamaStyleProduceList:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_produce_list(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_produce_list(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_produce_list(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleProduceList (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_produce_list(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_produce_list(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_produce_list(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)     

#####################################################################################################################
# DGLlamaStylePhotoVideo ############################################################################################
#####################################################################################################################

class DGLlamaStylePhotoVideo:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_photo_video_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_photo_video_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_photo_video_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStylePhotoVideo (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_photo_video_styles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_photo_video_styles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_photo_video_styles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)         

#####################################################################################################################
# DGLlamaStyleCats ##################################################################################################
#####################################################################################################################

class DGLlamaStyleCats:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_cats(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_cats(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_cats(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleCats (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_cats(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_cats(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_cats(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,) 

#####################################################################################################################
# DGLlamaStyleDogs ##################################################################################################
#####################################################################################################################

class DGLlamaStyleDogs:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_dogs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_dogs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_dogs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleDogs (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_dogs(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_dogs(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_dogs(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#####################################################################################################################
# DGLlamaStyleBirds #################################################################################################
#####################################################################################################################

class DGLlamaStyleBirds:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_birds(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_birds(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_birds(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleBirds (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_birds(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_birds(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_birds(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)   

#####################################################################################################################
# DGLlamaStyleDinosaurs #############################################################################################
#####################################################################################################################

class DGLlamaStyleDinosaurs:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_dinosaurs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_dinosaurs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_dinosaurs(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleDinosaurs (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_dinosaurs(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_dinosaurs(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_dinosaurs(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#####################################################################################################################
# DGLlamaStyleSupervillains #############################################################################################
#####################################################################################################################

class DGLlamaStyleSupervillains:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_supervillains(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_supervillains(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_supervillains(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleSupervillains (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_supervillains(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_supervillains(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_supervillains(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleSuperheroes ###########################################################################################
#####################################################################################################################

class DGLlamaStyleSuperheroes:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_superheroes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_superheroes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_superheroes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleSuperheroes (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_superheroes(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_superheroes(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_superheroes(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleBubbleKeywords ########################################################################################
#####################################################################################################################

class DGLlamaStyleBubbleKeywords:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_bubble_keywords(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_bubble_keywords(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_bubble_keywords(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleBubbleKeywords (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_bubble_keywords(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_bubble_keywords(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_bubble_keywords(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#####################################################################################################################
# DGLlamaStyleSignKeywords ##########################################################################################
#####################################################################################################################

class DGLlamaStyleSignKeywords:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_sign_keywords(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_sign_keywords(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_sign_keywords(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleSignKeywords (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_sign_keywords(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_sign_keywords(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_sign_keywords(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,) 

#####################################################################################################################
# DGLlamaStyleBodyPositions ##########################################################################################
#####################################################################################################################

class DGLlamaStyleBodyPositions:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_body_positions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_body_positions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_body_positions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleBodyPositions (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_body_positions(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_body_positions(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_body_positions(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleEmotionGenres ##########################################################################################
#####################################################################################################################

class DGLlamaStyleEmotionGenres:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_emotion_genres(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_emotion_genres(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_emotion_genres(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleEmotionGenres (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_emotion_genres(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_emotion_genres(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_emotion_genres(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#####################################################################################################################
# DGLlamaStyleCombatScenarios #######################################################################################
#####################################################################################################################

class DGLlamaStyleCombatScenarios:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_combat_scenarios(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_combat_scenarios(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_combat_scenarios(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleCombatScenarios (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_combat_scenarios(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_combat_scenarios(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_combat_scenarios(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleShortVideoScenarios ###################################################################################
#####################################################################################################################

class DGLlamaStyleShortVideoScenarios:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_short_video_scenarios(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_short_video_scenarios(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_short_video_scenarios(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleShortVideoScenarios (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_short_video_scenarios(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_short_video_scenarios(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_short_video_scenarios(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleClothingBrandsAndStyles ###############################################################################
#####################################################################################################################

class DGLlamaStyleClothingBrandsAndStyles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_clothing_brands_and_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_clothing_brands_and_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_clothing_brands_and_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleClothingBrandsAndStyles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_clothing_brands_and_styles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_clothing_brands_and_styles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_clothing_brands_and_styles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,) 

#####################################################################################################################
# DGLlamaStyleCamerasAndModes #######################################################################################
#####################################################################################################################

class DGLlamaStyleCamerasAndModes:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_cameras_and_modes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_cameras_and_modes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_cameras_and_modes(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleCamerasAndModes (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_cameras_and_modes(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_cameras_and_modes(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_cameras_and_modes(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStylePhotographersAndStyles ################################################################################
#####################################################################################################################

class DGLlamaStylePhotographersAndStyles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_photographers_and_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_photographers_and_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_photographers_and_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStylePhotographersAndStyles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_photographers_and_styles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_photographers_and_styles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_photographers_and_styles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleFilmAndSeriesCreators #################################################################################
#####################################################################################################################

class DGLlamaStyleFilmAndSeriesCreators:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_film_and_series_creators(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_film_and_series_creators(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_film_and_series_creators(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleFilmAndSeriesCreators (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_film_and_series_creators(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_film_and_series_creators(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_film_and_series_creators(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#get_prompt_art_styles2, generate_prompt_art_styles2
#####################################################################################################################
# DGLlamaStyleArtStyles #############################################################################################
#####################################################################################################################

class DGLlamaStyleArtStyles2:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_art_styles2(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_art_styles2(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_art_styles2(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleArtStyles2 (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_art_styles2(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_art_styles2(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_art_styles2(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,) 
    
#####################################################################################################################
# DGLlamaStyleArtStyles #############################################################################################
#####################################################################################################################

class DGLlamaStyleArtStyles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_art_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_art_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_art_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleArtStyles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_art_styles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_art_styles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_art_styles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  

#####################################################################################################################
# DGLlamaStyleRenderSystems #########################################################################################
#####################################################################################################################

class DGLlamaStyleRenderSystems:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_render_systems(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_render_systems(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_render_systems(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleRenderSystems (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_render_systems(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_render_systems(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_render_systems(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)    

#####################################################################################################################
# DGLlamaStyleArtGenres #############################################################################################
#####################################################################################################################

class DGLlamaStyleArtGenres:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_art_genres(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_art_genres(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_art_genres(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleArtGenres (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_art_genres(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_art_genres(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_art_genres(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)   

#####################################################################################################################
# DGLlamaStyleGamingConsoles ########################################################################################
#####################################################################################################################

class DGLlamaStyleGamingConsoles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_gaming_consoles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_gaming_consoles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_gaming_consoles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleGamingConsoles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_gaming_consoles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_gaming_consoles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_gaming_consoles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)   

#####################################################################################################################
# DGLlamaStyleAlienSpecies ##########################################################################################
#####################################################################################################################

class DGLlamaStyleAlienSpecies:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_alien_species(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_alien_species(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_alien_species(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleAlienSpecies (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_alien_species(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_alien_species(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_alien_species(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  
    
#####################################################################################################################
# DGLlamaStyleNightTimeStyles #######################################################################################
#####################################################################################################################

class DGLlamaStyleNightTimeStyles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_nighttime_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_nighttime_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_nighttime_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleNightTimeStyles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_nighttime_styles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_nighttime_styles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_nighttime_styles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)  
    
#####################################################################################################################
# DGLlamaStyleDaytimeStyles #########################################################################################
#####################################################################################################################

class DGLlamaStyleDaytimeStyles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_daytime_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_daytime_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_daytime_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleDaytimeStyles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_daytime_styles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_daytime_styles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_daytime_styles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,) 
    
#####################################################################################################################
# DGLlamaStyleWorldReligions ########################################################################################
#####################################################################################################################

class DGLlamaStyleWorldReligions:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_world_religions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_world_religions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_world_religions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleWorldReligions (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_world_religions(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_world_religions(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_world_religions(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleBiblicalMoments #######################################################################################
#####################################################################################################################

class DGLlamaStyleBiblicalMoments:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_biblical_moments(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_biblical_moments(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_biblical_moments(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleBiblicalMoments (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_biblical_moments(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_biblical_moments(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_biblical_moments(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleTimePeriods ###########################################################################################
#####################################################################################################################

class DGLlamaStyleTimePeriods:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_time_periods(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_time_periods(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_time_periods(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleTimePeriods (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_time_periods(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_time_periods(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_time_periods(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleProfessions ###########################################################################################
#####################################################################################################################

class DGLlamaStyleProfessions:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_professions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_professions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_professions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleProfessions (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_professions(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_professions(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_professions(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleCombatActions #########################################################################################
#####################################################################################################################

class DGLlamaStyleCombatActions:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_combat_actions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_combat_actions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_combat_actions(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleCombatActions (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_combat_actions(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_combat_actions(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_combat_actions(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleActionsStyles #########################################################################################
#####################################################################################################################

class DGLlamaStyleActionsStyles:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_actions_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_actions_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_actions_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleActionsStyles (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_actions_styles(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_actions_styles(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_actions_styles(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleWondersOfTheWorld #####################################################################################
#####################################################################################################################

class DGLlamaStyleWondersOfTheWorld:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_wonders_of_the_world(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_wonders_of_the_world(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_wonders_of_the_world(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleWondersOfTheWorld (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_wonders_of_the_world(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_wonders_of_the_world(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_wonders_of_the_world(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleMonsters ##############################################################################################
#####################################################################################################################

class DGLlamaStyleMonsters:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_monsters(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_monsters(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_monsters(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleMonsters (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_monsters(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_monsters(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_monsters(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleCelestialObjects ######################################################################################
#####################################################################################################################

class DGLlamaStyleCelestialObjects:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_celestial_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_celestial_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_celestial_objects(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleCelestialObjects (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_celestial_objects(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_celestial_objects(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_celestial_objects(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleProtectionTypes #######################################################################################
#####################################################################################################################

class DGLlamaStyleProtectionTypes:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_protection_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_protection_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_protection_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleProtectionTypes (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_protection_types(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_protection_types(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_protection_types(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleShieldTypes ###########################################################################################
#####################################################################################################################

class DGLlamaStyleShieldTypes:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_shield_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_shield_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_shield_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleShieldTypes (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value)
        
        if prompt_styles_1 != "Other":
            style1 = generate_prompt_shield_types(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_shield_types(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_shield_types(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)
    
#####################################################################################################################
# DGLlamaStyleBuildingTypes #########################################################################################
#####################################################################################################################

class DGLlamaStyleBuildingTypes:
    def __init__(self):
        self.mixed_style = ""
        self.seed_value = 0

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
                "style_seed": ("INT", {"forceInput": True, "default": 0, "min": 0, "max": 0xffffffffffffffff}),
                "prompt_mode": (["Image", "Video", "Other"], {"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_1": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_1": (get_prompt_building_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "styles_variation_2": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_2": (get_prompt_building_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}), 
                "styles_variation_3": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles_3": (get_prompt_building_types(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),                                                                               
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("style_mix",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGeneratorStyles (💫🅞🅧3🅓)"
    TITLE = "DGLlamaStyleBuildingTypes (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, prompt_mode, style_seed, styles_variation_1, prompt_styles_1, styles_variation_2, prompt_styles_2, styles_variation_3, prompt_styles_3):         
        nseed = style_seed
        if nseed == 0:
            nseed = random.randint(1, 100)

        if self.seed_value != nseed:
            self.seed_value = nseed
            random.seed(self.seed_value) 

        if prompt_styles_1 != "Other":
            style1 = generate_prompt_building_types(prompt_styles_1, media_type=prompt_mode, num_keywords=styles_variation_1)
        else:
            style1 = ""
        if prompt_styles_2 != "Other":
            style2 = generate_prompt_building_types(prompt_styles_2, media_type=prompt_mode, num_keywords=styles_variation_2)
        else:
           style2 = "" 
        if prompt_styles_3 != "Other":
            style3 = generate_prompt_building_types(prompt_styles_3, media_type=prompt_mode, num_keywords=styles_variation_3)
        else:
            style3 = ""       
        if prompt_mode == "Other":
            self.mixed_style = ""
        else:
            self.mixed_style = (f"{style1}\n{style2}\n{style3}")
        # 
        cleaned_string = "\n".join(line for line in self.mixed_style.splitlines() if line.strip())
        return (cleaned_string,)

#####################################################################################################################
# DGLlamaAgent ######################################################################################################
#####################################################################################################################
# I have some work to do here. This was originally supposed to become an agent controller, but the idea has changed over time.
# For now, it is just a text box node used to provide instructions to the agent system.
# I could update it later or possibly remove it entirely. With the latest agent updates in my other node, this one is no longer really necessary.
class DGLlamaAgent:
    acc1 = F"""Include in the prompt details about quality, the type of camera or Kodak, angles, perspective, and distance using professional photography terms.\nIf inspired by a known artist, add their name along with any other details needed to reproduce the image.\nDon't attempt to simulate taking a picture; just provide the prompt in text format."""
    acc2 = F"""# Use case exemple:\nYou are an agent specialized in creating text prompts for generating anime image, photo, video of all genres and styles.\nAs an expert, you are skilled at inventing original text prompt concepts with inspiration from the works of the greatest anime artists.\nYour expertise allows you to craft text prompts that bring to life vibrant shonen battles, heartwarming slice-of-life moments, or breathtaking fantasy worlds.\nYou excel at capturing the essence of any anime style, making you the perfect guide for designing detailed and visually stunning text prompts.\nDo not use words like Title: or Prompt:\nInstead, when you reply the prompt incorporate the content directly into the sentence as a single paragraph without separation"""    
    def __init__(self):
        pass
    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
            "agent": ('STRING', {"multiline": True, "default": f"""{cls.acc2}\n{cls.acc1}""", "tooltip": "The agent text to describe the special Llama agent."}), 
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("agent_msg",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaAgent (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, agent):  

        return (agent) 
    
#####################################################################################################################
# DGLlamaAgentCorrection ############################################################################################
#####################################################################################################################
# OLD METHOD NEED TO CHANGE IT LATER

class DGLlamaAgentCorrection:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.prompts = ""
        self.response = ""
        self.oldseed = -1
        self.useseed = True
        self.seed = -1 
        self.llama3_pipe = None  

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {  
            "correction": ('STRING', {"multiline": True, "default": "Correct any errors in the prompt", "tooltip": "Provide the text you would like to correct"}),
            "use_seeder": (["Yes", "No"],),
            "max_token": ("INT", {"default": 4096, "min": 256, "max": 4096, "step": 32}),
            "top_p": ("FLOAT", {"default": 0.9, "min": 0.0000, "max": 2.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Adjusts the creativity of the AI's responses by controlling how many possible words it considers. Lower values make outputs more predictable; higher values allow for more varied and creative responses."}),
            "top_k": ("INT", {"default": 50, "min": 1, "max": 50, "step": 1, "tooltip": "Limits the AI to choose from the top 'k' most probable words. Lower values make responses more focused; higher values introduce more variety and potential surprises."}),
            "temperature": ("FLOAT", {"default": 0.6000, "min": 0.0000, "max": 5.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Controls the randomness of the output; higher values produce more random results."}),
            "repetition_penalty": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 2.0, "step": 0.1, "round": 0.1, "tooltip": "Penalty for repeated tokens; higher values discourage repetition."}),            
            "use_uncensored_agent": (["No", "Yes"],),
            "always_unpaused": (["Yes", "No"],),
            "pause_generation": ("BOOLEAN", {"default": True, "label_on": "Pause", "label_off": "Unpause"}),
            },
            "optional": {
                "llama3_pipe": ("ANY", {"forceInput": True}), 
                "seeder": ("INT", {"forceInput": True, "default": -1, "min": 0, "max": 0xffffffffffffffff}),            
                "prompt": ('STRING', {"forceInput": True, "multiline": True, "default": "", "tooltip": "Prompt to correct"}),
                "remove_from_prompt": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent_remove, "tooltip": "Use for remove or modify text in the prompt result.\nUse Exemple 1 [Replace:Create a -> A] 'Create a ' is replace by ' A'\nUse Exemple 2 [Replace:Here is -> ] 'Here is ' is replace by ' ' nothing."}),
            }
        }
    
    RETURN_TYPES = ("STRING","ANY",)
    RETURN_NAMES = ("corrected_prompt", "llama3_pipe",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaAgentCorrection (Llama 3.1 & 3.2 - OX3D)"

    def generate_msg(self, correction, use_uncensored_agent, use_seeder, max_token, top_p, top_k, temperature, repetition_penalty, prompt, always_unpaused, pause_generation, seeder=None, remove_from_prompt = None, llama3_pipe = None): 
        self.llama3_pipe = llama3_pipe
        if self.llama3_pipe is not None: 

            if seeder is not None:
                nseed = seeder
            else:
                nseed = 0

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

            self.tokenizer = self.llama3_pipe.tokenizer
            self.model = self.llama3_pipe.model   
            if pause_generation == False or always_unpaused == "Yes":
                if use_uncensored_agent == "Yes":
                    self.prompts = self.code_format_prompt(correction + "\n\n" + "prompt: (" + prompt + ")" + "\n\nNever reply to my request, just give the corrected prompt", prompt_correctionsExp, "")
                else:
                    self.prompts = self.code_format_prompt(correction + "\n\n" + "prompt: (" + prompt + ")" + "\n\nNever reply to my request, just give the corrected prompt", prompt_corrections, "") 

                #print(f"OrionX3D Llama 3.x prompt correction: {self.prompts}")

                if self.tokenizer.pad_token_id is None:
                    self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
                if self.model.config.pad_token_id is None:
                    self.model.config.pad_token_id = self.model.config.eos_token_id 

                input_ids = self.tokenizer(self.prompts, return_tensors="pt").input_ids.to(self.llama3_pipe.device_name)
                generated_ids = self.model.generate(input_ids, max_new_tokens=max_token, top_k=top_k, top_p=top_p, temperature=temperature, repetition_penalty=repetition_penalty, do_sample=True, num_return_sequences=1) #, eos_token_id=self.tokenizer.eos_token_id
                self.response = self.tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
         
                self.response = clean_prompt_regex(self.response)
                
                #"""
                if remove_from_prompt is not None:
                    self.response = process_prompt_v2(self.response, self.llama3_pipe.remove_from_prompt + "\n" + remove_from_prompt)
                else:
                    self.response = process_prompt_v2(self.response, self.llama3_pipe.remove_from_prompt)
                #"""

                self.response = remove_leading_spaces(self.response)
                self.response = remove_parentheses(self.response)

                self.response = self.response.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace('(', '').replace(')', '') 

            if self.llama3_pipe.clear_extra_mem_gpu == "Yes":  
                torch.cuda.empty_cache()
                empty_cache()

        return (self.response, llama3_pipe) 
    
    def code_format_prompt(self, user_query, sprompt_text, aprompt_text):
        if self.llama3_pipe is not None:
            template = f"""{self.llama3_pipe.codeA}{self.llama3_pipe.codeB}{self.llama3_pipe.modeA}{self.llama3_pipe.codeC}\n\n{sprompt_text}{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeB}{self.llama3_pipe.codeC}\n\n{user_query}{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}\n\n{aprompt_text}{self.llama3_pipe.codeC}\n\n"""
        else:
            template = ("")

        return template     

#####################################################################################################################
# DGLlamaAgentTranslate #############################################################################################
#####################################################################################################################
# OLD METHOD NEED TO CHANGE IT LATER

class DGLlamaAgentTranslate:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.prompts = ""
        self.response = ""
        self.oldseed = -1
        self.useseed = True
        self.seed = -1   
        self.llama3_pipe = None

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
            "translate": ('STRING', {"multiline": True, "default": "Translate the prompt into French", "tooltip": "Provide the text you would like to translate and specify how"}),
            "use_seeder": (["Yes", "No"],),
            "max_token": ("INT", {"default": 4096, "min": 256, "max": 4096, "step": 32}),
            "top_p": ("FLOAT", {"default": 0.9, "min": 0.0000, "max": 2.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Adjusts the creativity of the AI's responses by controlling how many possible words it considers. Lower values make outputs more predictable; higher values allow for more varied and creative responses."}),
            "top_k": ("INT", {"default": 50, "min": 1, "max": 50, "step": 1, "tooltip": "Limits the AI to choose from the top 'k' most probable words. Lower values make responses more focused; higher values introduce more variety and potential surprises."}),
            "temperature": ("FLOAT", {"default": 0.6000, "min": 0.0000, "max": 5.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Controls the randomness of the output; higher values produce more random results."}),
            "repetition_penalty": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 2.0, "step": 0.1, "round": 0.1, "tooltip": "Penalty for repeated tokens; higher values discourage repetition."}),            
            "use_uncensored_agent": (["No", "Yes"],),
            "always_unpaused": (["Yes", "No"],),
            "pause_generation": ("BOOLEAN", {"default": True, "label_on": "Pause", "label_off": "Unpause"}),
            },
            "optional": {   
                "llama3_pipe": ("ANY", {"forceInput": True}),  
                "seeder": ("INT", {"forceInput": True, "default": -1, "min": 0, "max": 0xffffffffffffffff}),           
                "prompt": ('STRING', {"forceInput": True, "multiline": True, "default": "", "tooltip": "Prompt to translate"}),
                "remove_from_prompt": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent_remove, "tooltip": "Use for remove or modify text in the prompt result.\nUse Exemple 1 [Replace:Create a -> A] 'Create a ' is replace by ' A'\nUse Exemple 2 [Replace:Here is -> ] 'Here is ' is replace by ' ' nothing."}),
            }
        }
    
    RETURN_TYPES = ("STRING","ANY",)
    RETURN_NAMES = ("translated_prompt", "llama3_pipe",)    

    FUNCTION = "generate_msg"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaAgentTranslate (Llama 3.1 & 3.2 - OX3D)"        

    def generate_msg(self, translate, use_seeder, use_uncensored_agent, max_token, top_p, top_k, temperature, repetition_penalty, prompt, always_unpaused, pause_generation, seeder=None, remove_from_prompt = None, llama3_pipe = None):  
        self.llama3_pipe = llama3_pipe
        if self.llama3_pipe is not None:

            if seeder is not None:
                nseed = seeder
            else:
                nseed = 0

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

            self.tokenizer = self.llama3_pipe.tokenizer
            self.model = self.llama3_pipe.model 
            if pause_generation == False or always_unpaused == "Yes":
                if use_uncensored_agent == "Yes":
                    self.prompts = self.code_format_prompt(translate + "\n\n" + "prompt: (" + prompt + ")" + "\n\nNever reply to my request, just give the translated prompt", prompt_translationExp, "")  
                else:
                    self.prompts = self.code_format_prompt(translate + "\n\n" + "prompt: (" + prompt + ")" + "\n\nNever reply to my request, just give the translated prompt", prompt_translation, "") 
               
                #print(f"OrionX3D Llama 3.x prompt translation: {self.prompts}")

                if self.tokenizer.pad_token_id is None:
                    self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
                if self.model.config.pad_token_id is None:
                    self.model.config.pad_token_id = self.model.config.eos_token_id                  

                input_ids = self.tokenizer(self.prompts, return_tensors="pt").input_ids.to(self.llama3_pipe.device_name)
                generated_ids = self.model.generate(input_ids, max_new_tokens=max_token, top_k=top_k, top_p=top_p, temperature=temperature, repetition_penalty=repetition_penalty, do_sample=True, num_return_sequences=1) #, eos_token_id=self.tokenizer.eos_token_id
                self.response = self.tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
         
                self.response = clean_prompt_regex(self.response)

                #"""
                if remove_from_prompt is not None:
                    self.response = process_prompt_v2(self.response, self.llama3_pipe.remove_from_prompt + "\n" + remove_from_prompt)
                else:
                    self.response = process_prompt_v2(self.response, self.llama3_pipe.remove_from_prompt)
                #"""
                self.response = remove_leading_spaces(self.response)
                self.response = remove_parentheses(self.response)

                self.response = self.response.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace('(', '').replace(')', '') 

            if self.llama3_pipe.clear_extra_mem_gpu == "Yes":  
                torch.cuda.empty_cache()
                empty_cache()

        return (self.response, llama3_pipe)  
    
    def code_format_prompt(self, user_query, sprompt_text, aprompt_text):
        if self.llama3_pipe is not None:
            template = f"""{self.llama3_pipe.codeA}{self.llama3_pipe.codeB}{self.llama3_pipe.modeA}{self.llama3_pipe.codeC}\n\n{sprompt_text}{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeB}{self.llama3_pipe.codeC}\n\n{user_query}{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}\n\n{aprompt_text}{self.llama3_pipe.codeC}\n\n"""
        else:
            template = ("")   

        return template

#####################################################################################################################
# DGLlamaChatUser ###################################################################################################
#####################################################################################################################   
class DGLlamaChatUser:    
    def __init__(self):
        self.tokenizer = None #llama3_pipe.tokenizer
        self.model = None #llama3_pipe.model
        self.prompts = "" #initial_prompt
        self.max_tokens = 4096 
        self.agent = None
        self.agentchat = None
        self.current_normal_text = ""
        self.current_uncensored_text = ""
        self.old_name = ""
        self.response = ""
        self.agent_mode_restriction = "normal"
        self.old_agent_mode = "normal"
        self.oldseed = -1
        self.useseed = True
        self.seed = -1            
        #self.dave_normal_text = ""
        #self.dave_uncensored_text = ""
        #self.geraldine_normal_text = ""
        #self.geraldine_uncensored_text = ""        

    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
            "llama3_pipe": ("ANY",), 
            "use_seeder": (["Yes", "No"],),
            "prompt_mode": (["Other", "Image", "Video", "Chat"], {"tooltip": "Just a quick guidance for the agent."}),
            "llama3_reset": ("BOOLEAN", {"default": False, "label_on": "True", "label_off": "False"}),
            "llama3_agent_clear_history": ("BOOLEAN", {"default": False, "label_on": "True", "label_off": "False"}),
            "llama3_agent_type": (get_filtered_filenames("dg_llama_agents", extensions=['.agt']), {"tooltip": "agent files."}),
            "max_token": ("INT", {"default": 4096, "min": 2048, "max": 4096, "step": 32}),
            "top_p": ("FLOAT", {"default": 0.9, "min": 0.0000, "max": 2.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Adjusts the creativity of the AI's responses by controlling how many possible words it considers. Lower values make outputs more predictable; higher values allow for more varied and creative responses."}),
            "top_k": ("INT", {"default": 50, "min": 1, "max": 50, "step": 1, "tooltip": "Limits the AI to choose from the top 'k' most probable words. Lower values make responses more focused; higher values introduce more variety and potential surprises."}),
            "temperature": ("FLOAT", {"default": 0.6000, "min": 0.0000, "max": 5.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Controls the randomness of the output; higher values produce more random results."}),
            "repetition_penalty": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 2.0, "step": 0.1, "round": 0.1, "tooltip": "Penalty for repeated tokens; higher values discourage repetition."}),                   
            "use_remove_from_manager": (["No", "Yes"],),      
            "use_custom_prompt": (["No", "Yes"], {"tooltip": "This option disable the llama model and use the text subject directly."}),
            "use_external_subject": (["No", "Yes"], {"tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),
            "use_mix_styles": (["No", "Yes"],),
            #"user_name": ("STRING", {"default": "God", "tooltip": "Just a name for interacting with Orion agent."}),
            "subject": ('STRING', {"multiline": True, "default": "", "tooltip": "The user text to direct Llama to generate the prompt."}), 
            "custom_prompt": ('STRING', {"multiline": True, "default": "", "tooltip": "Disable the llama generation and une the custom prompt."}),
            "always_unpaused": (["Yes", "No"],),
            "pause_generation": ("BOOLEAN", {"default": True, "label_on": "Pause", "label_off": "Unpause"}),
            },
            "optional": {            
                "seeder": ("INT", {"forceInput": True, "default": -1, "min": 0, "max": 0xffffffffffffffff}),   
                "mix_styles": ("STRING", {"forceInput": True, "multiline": True}), 
                #"agent": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent, "tooltip": "The agent text to describe the Llama agent."}),
                "external_subject": ("STRING", {"forceInput": True, "multiline": True, "tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),
                "remove_from_prompt": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent_remove, "tooltip": "Use for remove or modify text in the prompt result.\nUse Exemple 1 [Replace:Create a -> A] 'Create a ' is replace by ' A'\nUse Exemple 2 [Replace:Here is -> ] 'Here is ' is replace by ' ' nothing."}), 
            }            
        }   

    RETURN_TYPES = ("STRING","ANY","STRING",)
    RETURN_NAMES = ("prompt","llama3_pipe","mix_styles",)    

    FUNCTION = "generate_prompt"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaChatUser (Llama 3.1 & 3.2 - OX3D)"  
    OUTPUT_NODE = True

    def generate_prompt(self, subject, use_custom_prompt, custom_prompt, max_token, top_p, top_k, temperature, repetition_penalty, use_seeder, prompt_mode, always_unpaused, use_remove_from_manager, llama3_reset, llama3_pipe, llama3_agent_type, llama3_agent_clear_history, pause_generation, use_external_subject, use_mix_styles, seeder=None, mix_styles=None, external_subject=None, remove_from_prompt=None): #agent=None,
        # Currently forcing the size; it likely only works well for the Llama 3B version or larger...
        # Anyway, the Llama 1B is a decent model, but it’s not very good for generating quality prompts or translations. 
        # It requires the 3B version or higher for better performance.
        # I might try to fix this later. The real issue is that I’m using a very large system message, which takes up a lot of space.
        self.max_tokens = max_token #llama3_pipe.max_new_tokens - 1000
        #if self.max_tokens < 0:
        #    self.max_tokens = 4096 - 1000

        reset_agent = llama3_reset

        self.agent_mode_restriction = extract_version(llama3_agent_type)
        pname = extract_person_name(llama3_agent_type)
        
        print(f"Selected Llama agent: {pname}")  

        if pname == "":
            pname = "geraldine"
            #if self.agent is None:
            #    self.agent = AgentGeraldine(ox3d_user_name, current_dir, self.tokenizer, self.max_tokens)
            #    self.agent.save_agent_text(f"agent_{pname}_normal.agt", uncensored=False)
            #    self.agent.save_agent_text(f"agent_{pname}_uncensored.agt", uncensored=True)            

        if self.old_name != pname:
            self.old_name = pname
            reset_agent = True
            if self.agentchat is not None:
                self.agentchat._update_agent_name(pname)          

        if seeder is not None:
            nseed = seeder
        else:
            nseed = 0

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

        if reset_agent == True:
            if self.agentchat is not None:
                #if self.agentchat.agent_mode_restriction == "uncensored":
                #    self.agentchat.reset_history(f"ox3d_llama_{self.agentchat.agent_name}_chat_uncensored_history.json", False)
                #else:
                #    self.agentchat.reset_history(f"ox3d_llama_{self.agentchat.agent_name}_chat_history.json", False)
                
                self.agentchat._update_agent_name(pname)
            #
            self.agentchat = None
            #self.agent = None

        if llama3_agent_clear_history == True:
            if self.agentchat is not None:
                if self.agentchat.agent_mode_restriction == "uncensored":
                    self.agentchat.reset_history(f"ox3d_llama_{self.agentchat.agent_name}_chat_uncensored_history.json", True)
                else: 
                    self.agentchat.reset_history(f"ox3d_llama_{self.agentchat.agent_name}_chat_history.json", True)

        #if self.max_tokens < 512:
        #    self.max_tokens = 512

        if self.old_agent_mode != self.agent_mode_restriction:
           self.old_agent_mode = self.agent_mode_restriction 
           if self.agentchat is not None:
               self.agentchat._update_agent_mode(self.agent_mode_restriction) 
               self.agentchat = None      
        
        if pause_generation == True and always_unpaused == "No":
            print(f"OX3D Llama pause generation - enabled")
        else:
            print(f"OX3D Llama pause generation - disabled")

        file_normal = f"agent_{pname}_normal.agt"
        file_uncensored = f"agent_{pname}_uncensored.agt"

        if self.agent is None:
            self.agent = llama3_pipe.current_agent

        if self.agent is not None:
            try:
                self.current_normal_text = self.agent.load_agent_text(file_normal)
                self.current_uncensored_text = self.agent.load_agent_text(file_uncensored)                     
            except FileNotFoundError as e:
                print(e)
                      
        if self.agentchat is None:
            if self.agent_mode_restriction == "uncensored":
                self.agentchat = DGLlamaChatAgent(llama3_pipe, pname, self.agent_mode_restriction, self.current_uncensored_text)
            else:
                self.agentchat = DGLlamaChatAgent(llama3_pipe, pname, self.agent_mode_restriction, self.current_normal_text)
        
        if use_custom_prompt == "No" and (pause_generation == False or always_unpaused == "Yes"):
            if self.agentchat is not None:
                #prompt_mode
                #chat_str = "\n".join(subject)
                chat_str = subject
                if prompt_mode == "Image":
                    chat_str = "An high quality image prompt about - " + subject
                if prompt_mode == "Video":
                    chat_str = "A high quality video prompt about - " + subject     
                if prompt_mode == "Chat":
                    chat_str = "I'm here for chat - " + subject   
                if prompt_mode == "Other":
                    chat_str = subject

                eval_style = False   

                if mix_styles is not None and external_subject is not None:
                    if mix_styles != "" and external_subject != "":
                        if use_mix_styles == "Yes" and use_external_subject == "Yes":
                            eval_style = True
                            chat_str = f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + external_subject + "\n" + mix_styles
                        if use_mix_styles == "Yes" and use_external_subject == "No":
                            eval_style = True
                            chat_str =  f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + mix_styles
                        if use_mix_styles == "No" and use_external_subject == "Yes":
                            eval_style = True
                            chat_str = f"user {ox3d_user_name}: main topic " + chat_str + "\n" + "mix with " + external_subject

                if mix_styles is not None and external_subject is None:
                    if mix_styles != "":
                        if use_mix_styles == "Yes":
                            eval_style = True
                            chat_str = f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + mix_styles 

                if mix_styles is None and external_subject is not None:
                    if external_subject != "":                    
                        if use_external_subject == "Yes":
                            eval_style = True
                            chat_str = f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + external_subject  

                if eval_style == True:
                    chat_str = chat_str + "\n" + "If styles are similar or mean the same, choose the one that works best for the prompt. Be creative, and try to craft a prompt of 400 tokens maximum or less."                                 
                
                #top_p, top_k, temperature, repetition_penalty
                self.response = self.agentchat.chat(self.useseed, chat_str, max_new_tokens=self.max_tokens, temperature=temperature, top_k=top_k, top_p=top_p, repetition_penalty=repetition_penalty)
                #print(f"Response: \n{res}")   
                #self.agentchat.print_current_history_tokens()

                self.response = clean_prompt_regex(self.response)

                #"""
                if remove_from_prompt is not None:
                    if use_remove_from_manager == "Yes":
                        self.response = process_prompt_v2(self.response, llama3_pipe.remove_from_prompt + "\n" + remove_from_prompt)
                    else:
                        self.response = process_prompt_v2(self.response, remove_from_prompt)
                else:
                    if use_remove_from_manager == "Yes":
                        self.response = process_prompt_v2(self.response, llama3_pipe.remove_from_prompt)
                    else:
                        self.response = process_prompt_v2(self.response, "")
                #"""

                self.response = remove_leading_spaces(self.response)

                self.response = self.response.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace('(', '').replace(')', '')   
        else:
            if use_custom_prompt == "Yes":
                self.response = custom_prompt
            if self.response == "":
                self.response = custom_prompt

        self.old_name = pname
        self.old_agent_mode = self.agent_mode_restriction

        if llama3_pipe.clear_extra_mem_gpu == "Yes":  
            torch.cuda.empty_cache()
            empty_cache() 

        self.oldseed = nseed

        astyle = ""
        if mix_styles is not None:
            astyle = mix_styles            
        
        return(self.response, llama3_pipe, astyle)       
                                 
#####################################################################################################################
# DGLlamaAgentUserEdit ##############################################################################################
#####################################################################################################################
# Very deprecated, I have begin to update it... WIP
class DGLlamaAgentUserEdit:    
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.prompts = ""
        self.old_prompts = ""
        self.response = ""
        self.old_response = ""  
        #self.text_buffer = None   
        self.max_tokens = 4096 
        #self.old_agent = None
        self.new_agent = None
        #self.agent1 = None # AgentGeraldine(ox3d_user_name, current_dir)
        #self.agent2 = None # AgentDave(ox3d_user_name, current_dir)
        #self.dave_normal_text = ""
        #self.dave_uncensored_text = ""
        #self.geraldine_normal_text = ""
        #self.geraldine_uncensored_text = "" 
        self.current_text_buffer = None
        self.agent_mode_restriction = "normal"
        self.default_agent_name = ""
        self.default_old_agent_name = ""
        self.oldseed = -1
        self.useseed = True
        self.seed = -1         
          
    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
            #"user_name": ("STRING", {"default": "God", "tooltip": "Just a name for interacting with Orion agent."}),
            "llama3_pipe": ("ANY",),
            "use_seeder": (["Yes", "No"],),
            #"llama_agent_type": (extract_person_name(get_filtered_filenames("dg_llama_agents", extensions=['.agt'])), {"tooltip": "agent files."}),
            #"llama_agent_type": (["Geraldine", "Dave"],),
            #"llama_reset": (["No", "Yes"],), 
            "prompt_mode": (["Other", "Image", "Video", "Chat"], {"tooltip": "Just a quick guidance for the agent."}),
            "custom_agent_name": ('STRING', {"multiline": False, "default": "Roberto", "tooltip": "Your custom agent name: If you create a new agent, refresh the ComfyUI window after the first generation to see the agent file in the list."}),
            "llama3_reset": ("BOOLEAN", {"default": False, "label_on": "True", "label_off": "False"}),
            "llama3_agent_clear_history": ("BOOLEAN", {"default": False, "label_on": "True", "label_off": "False"}), 
            "llama3_agent_type": (get_filtered_filenames("dg_llama_agents", extensions=['.agt']), {"tooltip": "Agent files: If you change the agent, activate the llama3_reset button to reset the agent."}),
            "max_token": ("INT", {"default": 4096, "min": 2048, "max": 4096, "step": 32}),
            "top_p": ("FLOAT", {"default": 0.9, "min": 0.0000, "max": 2.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Adjusts the creativity of the AI's responses by controlling how many possible words it considers. Lower values make outputs more predictable; higher values allow for more varied and creative responses."}),
            "top_k": ("INT", {"default": 50, "min": 1, "max": 50, "step": 1, "tooltip": "Limits the AI to choose from the top 'k' most probable words. Lower values make responses more focused; higher values introduce more variety and potential surprises."}),
            "temperature": ("FLOAT", {"default": 0.6000, "min": 0.0000, "max": 5.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Controls the randomness of the output; higher values produce more random results."}),
            "repetition_penalty": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 2.0, "step": 0.1, "round": 0.1, "tooltip": "Penalty for repeated tokens; higher values discourage repetition."}),            
            "use_mix_styles": (["No", "Yes"],),
            "use_custom_prompt": (["No", "Yes"], {"tooltip": "This option disable the llama model and use the text subject directly."}),
            "use_external_subject": (["No", "Yes"], {"tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),
            "use_remove_from_manager": (["No", "Yes"],),
            "subject": ('STRING', {"multiline": True, "default": "", "tooltip": "The user text to direct Llama to generate the prompt."}), 
            "custom_prompt": ('STRING', {"multiline": True, "default": "", "tooltip": "Disable the llama generation and une the custom prompt."}),
            #"disable_generation": (["No", "Yes"],),
            #"agent_mode": (["Prompt", "Chat"],),
            "always_unpaused": (["Yes", "No"],),
            "pause_generation": ("BOOLEAN", {"default": True, "label_on": "Pause", "label_off": "Unpause"}),
            },
            "optional": {
                "seeder": ("INT", {"forceInput": True, "default": -1, "min": 0, "max": 0xffffffffffffffff}),
                "mix_styles": ("STRING", {"forceInput": True, "multiline": True}),
                "external_subject": ("STRING", {"forceInput": True, "multiline": True, "tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),  
                "agent": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent, "tooltip": "The agent text to describe your Llama agent, refresh the ComfyUI window after the first generation to see the agent file in the list."}),
                "remove_from_prompt": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent_remove, "tooltip": "Use for remove or modify text in the prompt result.\nUse Exemple 1 [Replace:Create a -> A] 'Create a ' is replace by ' A'\nUse Exemple 2 [Replace:Here is -> ] 'Here is ' is replace by ' ' nothing."}), 
            }
        }
    
    RETURN_TYPES = ("STRING","ANY","STRING",)
    RETURN_NAMES = ("prompt","llama3_pipe","mix_styles",)    

    FUNCTION = "generate_prompt"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaAgentUserEdit (Llama 3.1 & 3.2 - OX3D)"
    #agent_mode, #llama_agent_type, #llama_reset, #disable_generation
    def generate_prompt(self, subject, use_custom_prompt, custom_prompt, prompt_mode, max_token, top_p, top_k, temperature, repetition_penalty, use_seeder, llama3_pipe, custom_agent_name, always_unpaused, llama3_reset, llama3_agent_clear_history, pause_generation, llama3_agent_type, use_remove_from_manager, use_mix_styles, use_external_subject, seeder=None, mix_styles=None, external_subject=None, remove_from_prompt=None, agent = None):
        self.prompts = subject #subject #f"User {ox3d_user_name} Chat: " + subject
        self.tokenizer = llama3_pipe.tokenizer
        self.model = llama3_pipe.model 
        self.max_tokens = max_token
        reset_agent = llama3_reset
        #if llama3_reset == True:
        #    self.old_agent = None
        #    self.new_agent = None 
        #    self.default_agent_name = "" 

        if seeder is not None:
            nseed = seeder
        else:
            nseed = 0 #llama3_pipe.seed

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

        self.agent_mode_restriction = extract_version(llama3_agent_type)
        pname = extract_person_name(llama3_agent_type)

        self.default_agent_name = pname

        #rst = llama3_reset

        if self.default_old_agent_name != self.default_agent_name:
            self.default_old_agent_name = self.default_agent_name
            reset_agent = True

        if reset_agent == True:
            if self.new_agent is not None:
                #if self.new_agent.agent_mode_restriction == "uncensored":
                #    self.new_agent.reset_history(f"ox3d_llama_{self.new_agent.agent_name}_chat_uncensored_history.json", False)
                #else:
                #    self.new_agent.reset_history(f"ox3d_llama_{self.new_agent.agent_name}_chat_history.json", False)
                
                self.new_agent._update_agent_name(pname)
            #
            self.new_agent = None    
            #self.old_agent = None   
            self.default_agent_name = ""        
        #DGLlamaChatAgent
        #AgentGeraldine
        #self.default_agent_name = 
        agent_str = ""
        if agent is not None:
            agent_str = agent        
            if self.default_agent_name == "": 
                #self.old_agent = None
                self.new_agent = None
                if custom_agent_name == "":
                    pname = generate_robot_name()
                else:
                    pname = custom_agent_name
                    agent_str = insert_line_after_first(agent_str, f"Your agent name are {pname}.")
                #    
                self.default_agent_name = pname
        else:
            self.default_agent_name = pname
            agent_str = ""

        file_normal = f"agent_{self.default_agent_name}_normal.agt"
        #self.agent.load_agent_text(file_normal)         

        if llama3_agent_clear_history == True:
            if self.new_agent is not None:
                if self.new_agent.agent_mode_restriction == "uncensored":
                    self.new_agent.reset_history(f"ox3d_llama_{self.new_agent.agent_name}_chat_uncensored_history.json", True)
                else: 
                    self.new_agent.reset_history(f"ox3d_llama_{self.new_agent.agent_name}_chat_history.json", True)        

        #if self.old_agent is None:
        #    self.old_agent = AgentGeraldine(ox3d_user_name, current_dir, self.tokenizer, llama3_pipe.max_new_tokens)
        #    if agent is not None:
        #        self.old_agent.save_agent_text(f"agent_{self.default_agent_name}_normal.agt", False, agent_str)
        #    else:
        if llama3_pipe.current_agent is not None:
            if agent_str == "":
                agent_str = llama3_pipe.current_agent.load_agent_text(file_normal)
            #
            llama3_pipe.current_agent.save_agent_text(f"agent_{self.default_agent_name}_normal.agt", False, agent_str)
        #
        if self.new_agent is None:
            self.new_agent = DGLlamaChatAgent(llama3_pipe, self.default_agent_name, self.agent_mode_restriction, agent_str)

        #self.current_text_buffer = ""

        #geraldine_agent_text = ""
        #dave_agent_text = ""

        #if llama_reset == "Yes":
        #    #self.text_buffer = None  
        #    self.agent1 = None  
        #    self.agent2 = None 
        #    self.current_text_buffer = None

        #if self.agent1 is None:
        #    self.agent1 = AgentGeraldine(ox3d_user_name, current_dir, self.tokenizer, self.max_tokens)
        #    self.agent1.save_agent_text('agent_geraldine_normal.agt', uncensored=False)
        #    self.agent1.save_agent_text('agent_geraldine_uncensored.agt', uncensored=True)

        #if self.agent2 is None:    
        #    self.agent2 = AgentDave(ox3d_user_name, current_dir, self.tokenizer, self.max_tokens)           
        #    self.agent2.save_agent_text('agent_dave_normal.agt', uncensored=False)
        #    self.agent2.save_agent_text('agent_dave_uncensored.agt', uncensored=True)  

        #if llama_agent_type is not None:
        #    self.current_normal_text = ""
        #    self.current_uncensored_text = ""  
        #if self.agent1 is not None:
        #    try:
        #        self.geraldine_normal_text = self.agent1.load_agent_text('agent_geraldine_normal.agt')
        #        self.geraldine_uncensored_text = self.agent1.load_agent_text('agent_geraldine_uncensored.agt')                     
        #    except FileNotFoundError as e:
        #        print(e)   

        #if self.agent2 is not None:
        #    try:           
        #        self.dave_normal_text = self.agent2.load_agent_text('agent_dave_normal.agt')
        #        self.dave_uncensored_text = self.agent2.load_agent_text('agent_dave_uncensored.agt')          
        #    except FileNotFoundError as e:
        #        print(e)     
                
        #print("Geraldine Normal Version:\n", self.geraldine_normal_text)
        #print("\nGeraldine Uncensored Version:\n", self.geraldine_uncensored_text)
        #print("Dave Normal Version:\n", self.dave_normal_text)
        #print("\nDave Uncensored Version:\n", self.dave_uncensored_text)                  

        #if llama3_pipe.use_uncensored_agent == "Yes":
        #    geraldine_agent_text = self.geraldine_uncensored_text
        #    dave_agent_text = self.dave_uncensored_text
        #else:
        #    geraldine_agent_text = self.geraldine_normal_text
        #    dave_agent_text = self.dave_normal_text

        #if llama_agent_type == "Geraldine":
        #    self.current_text_buffer = self.agent1.text_buffer
        #if llama_agent_type == "Dave":
        #    self.current_text_buffer = self.agent2.text_buffer              

        #if llama3_pipe.agent is not None:
        #    agent_str = llama3_pipe.agent
        #if agent is not None:
        #    if llama_agent_type == "Geraldine":
        #        agent_str = f"The user's name is {ox3d_user_name}. follow his directives as you work for him. If {ox3d_user_name} doesn't give you an agent name, your name is Geraldine\n"+agent
        #    if llama_agent_type == "Dave":
        #        agent_str = f"The user's name is {ox3d_user_name}. follow his directives as you work for him. If {ox3d_user_name} doesn't give you an agent name, your name is Dave\n"+agent                
        #else: # some default agent just for fun...
        #    if llama_agent_type == "Geraldine":
        #        agent_str = geraldine_agent_text
        #    if llama_agent_type == "Dave":
        #        agent_str = dave_agent_text

        prompt_only = self.prompts

        #chat_str = subject
        if prompt_mode == "Image":
            prompt_only = "An high quality image prompt about - " + self.prompts
        if prompt_mode == "Video":
            prompt_only = "A high quality video prompt about - " + self.prompts     
        if prompt_mode == "Chat":
            prompt_only = "I'm here for chat - " + self.prompts   
        if prompt_mode == "Other":
            prompt_only = self.prompts        

        #if agent_mode == "chat":
        #    use_mix_styles_new = "No"
        #else:
        use_mix_styles_new = use_mix_styles
        #mix_text = mix_styles
        #if self.old_prompts != ""
        #if use_mix_styles == "Yes" and use_external_subject == "Yes":
        if use_mix_styles_new == "Yes" and use_external_subject == "Yes":
            if mix_styles is not None and external_subject is not None:
                prompt_only = mix_styles + "\n\n" + prompt_only + "\n" + external_subject 
            if mix_styles is not None and external_subject is None:
                prompt_only = mix_styles + "\n\n" + prompt_only  
            if mix_styles is None and external_subject is not None:
                prompt_only = "\n\n" + prompt_only + "\n" + external_subject                                

        if use_mix_styles_new == "Yes" and use_external_subject == "No":    
            if mix_styles is not None:
                prompt_only = mix_styles + "\n\n" + prompt_only

        if use_mix_styles_new == "No" and use_external_subject == "Yes":    
            if use_external_subject is not None:
                prompt_only = "\n\n" + prompt_only + "\n" + external_subject              
            #if mix_styles is not None and external_subject is not None:
            #    prompt_only = mix_styles + "\n\nimportant to add this subject and actors: " + prompt_only + "\n" + external_subject            

        if use_custom_prompt == "No" and (pause_generation == False or always_unpaused == "Yes"):
            #if self.text_buffer is None:
            #    self.text_buffer = DG_LlamaTextBuffer(ox3d_user_name, self.tokenizer, self.max_tokens)            

            #if not self.prompts in self.text_buffer.get_buffer():
            prompt_only = str(remove_spaces_lines_total(prompt_only))
            #print(f"TESTING PROMPT:\n{prompt_only}")

            #if self.current_text_buffer is not None:
            #    buffer_text = self.current_text_buffer  # This will now work since text_buffer is initialized
            #else: 
            #    buffer_text = ""

            full_prompt = prompt_only #llama3_pipe.code_format_prompt2(user_query=prompt_only, sprompt_text=agent_str, aprompt_text="")

            #self.prompts = llama3_pipe.code_format_prompt(prompt_only, agent_str, "")
            self.old_prompts = prompt_only #self.prompts

            #u_prompts = "user: " + self.prompts
            #if self.current_text_buffer is not None:
            #    self.current_text_buffer.add_to_buffer(user_input=prompt_only)

            """
            input_ids = self.tokenizer(buffer_text + "\n" + full_prompt, return_tensors="pt").input_ids.to("cuda")
            #input_ids = self.tokenizer(self.prompts, return_tensors="pt").input_ids.to("cuda")

            if llama3_pipe.useseed == True:
                generated_ids = self.model.generate(input_ids, max_new_tokens=llama3_pipe.max_new_tokens, top_k=llama3_pipe.top_k, top_p=llama3_pipe.top_p, temperature=llama3_pipe.temperature, repetition_penalty=llama3_pipe.repetition_penalty, do_sample=True, eos_token_id=self.tokenizer.eos_token_id)
            else:
                generated_ids = self.model.generate(input_ids, max_new_tokens=llama3_pipe.max_new_tokens, top_k=llama3_pipe.top_k, top_p=llama3_pipe.top_p, temperature=llama3_pipe.temperature, repetition_penalty=llama3_pipe.repetition_penalty, do_sample=False, eos_token_id=self.tokenizer.eos_token_id)
        
            self.response = self.tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
          
            self.response = clean_prompt_regex(self.response)

            if remove_from_prompt is not None:
                if use_remove_from_manager == "Yes":
                    self.response = process_prompt_v2(self.response, llama3_pipe.remove_from_prompt + "\n" + remove_from_prompt)
                else:
                    self.response = process_prompt_v2(self.response, remove_from_prompt)
            else:
                if use_remove_from_manager == "Yes":
                    self.response = process_prompt_v2(self.response, llama3_pipe.remove_from_prompt)
                else:
                    self.response = process_prompt_v2(self.response, "")

            self.response = remove_leading_spaces(self.response)

            self.response = self.response.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace('(', '').replace(')', '')
            """
            #
            #buffer_text + "\n" + 
            if self.new_agent is not None: #top_p, top_k, temperature, repetition_penalty,
                self.response = self.new_agent.chat(self.useseed, full_prompt, max_new_tokens=self.max_tokens, temperature=temperature, top_k=top_k, top_p=top_p, repetition_penalty=repetition_penalty)
            
                self.response = clean_prompt_regex(self.response)
                
                #"""
                if remove_from_prompt is not None:
                    if use_remove_from_manager == "Yes":
                        self.response = process_prompt_v2(self.response, llama3_pipe.remove_from_prompt + "\n" + remove_from_prompt)
                    else:
                        self.response = process_prompt_v2(self.response, remove_from_prompt)
                else:
                    if use_remove_from_manager == "Yes":
                        self.response = process_prompt_v2(self.response, llama3_pipe.remove_from_prompt)
                    else:
                        self.response = process_prompt_v2(self.response, "")
                #"""

                self.response = remove_leading_spaces(self.response)

                self.response = self.response.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace('(', '').replace(')', '')            
            #self.prompts = "user: " + self.prompts
            #self.response = "agent: " + self.response
            #if self.current_text_buffer is not None:
            #    self.current_text_buffer.add_to_buffer(user_input=prompt_only, assistant_response=self.response)

            #print("Contenu actuel du buffer :")
            #print("[BEGIN]===================================================================================")
            #print(self.text_buffer.get_buffer())
            #print(" ")
            #print(f"Buffer size tokens : {self.text_buffer.get_token_count()}") 
            #print("[END]=====================================================================================")      
        else:
            if use_custom_prompt == "Yes":
                self.response = custom_prompt
            if self.response == "":
                self.response = custom_prompt                

        if self.response == "":
            self.response = self.old_response

        self.old_response = self.response
        self.default_old_agent_name = self.default_agent_name

        if llama3_pipe.clear_extra_mem_gpu == "Yes":  
            torch.cuda.empty_cache()
            empty_cache()  

        self.oldseed = nseed  

        astyle = ""
        if mix_styles is not None:
            astyle = mix_styles            

        return (self.response, llama3_pipe, astyle) 
    
"""
# OLD USER DEPRECATED
class DGLlamaUser:    
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.prompts = ""
        self.old_prompts = ""
        self.response = ""
        self.old_response = ""  
        #self.text_buffer = None   
        self.max_tokens = 4096 - 256 
        self.agent1 = None # AgentGeraldine(ox3d_user_name, current_dir)
        self.agent2 = None # AgentDave(ox3d_user_name, current_dir)
        self.dave_normal_text = ""
        self.dave_uncensored_text = ""
        self.geraldine_normal_text = ""
        self.geraldine_uncensored_text = "" 
        self.current_text_buffer = None
          
    @classmethod
    def INPUT_TYPES(cls):
        return { 
            "required": {
            #"user_name": ("STRING", {"default": "God", "tooltip": "Just a name for interacting with Orion agent."}),
            "llama3_pipe": ("ANY",),
            #"llama_agent_type": (extract_person_name(get_filtered_filenames("dg_llama_agents", extensions=['.agt'])), {"tooltip": "agent files."}),
            "llama_agent_type": (["Geraldine", "Dave"],),
            "llama_reset": (["No", "Yes"],),
            "use_mix_styles": (["No", "Yes"],),
            "use_external_subject": (["No", "Yes"], {"tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),
            "use_remove_from_manager": (["No", "Yes"],),
            "subject": ('STRING', {"multiline": True, "default": "", "tooltip": "The user text to direct Llama to generate the prompt."}), 
            "disable_generation": (["No", "Yes"],),
            "agent_mode": (["Prompt", "Chat"],),
            },
            "optional": {
                "mix_styles": ("STRING", {"forceInput": True, "multiline": True}),
                "external_subject": ("STRING", {"forceInput": True, "multiline": True}),  
                "agent": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent, "tooltip": "The agent text to describe the Llama agent."}),
                "remove_from_prompt": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent_remove, "tooltip": "Use for remove or modify text in the prompt result.\nUse Exemple 1 [Replace:Create a -> A] 'Create a ' is replace by ' A'\nUse Exemple 2 [Replace:Here is -> ] 'Here is ' is replace by ' ' nothing."}), 
            }
        }
    
    RETURN_TYPES = ("STRING","ANY",)
    RETURN_NAMES = ("Prompt","llama3_pipe",)    

    FUNCTION = "generate_prompt"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaUser (Llama 3.1 & 3.2 - OX3D)"

    def generate_prompt(self, subject, agent_mode, llama3_pipe, llama_reset, disable_generation, use_remove_from_manager, llama_agent_type, use_mix_styles, use_external_subject, mix_styles=None, external_subject=None, remove_from_prompt=None, agent = None):
        self.prompts = f"User {ox3d_user_name} Chat: " + subject #subject 
        self.tokenizer = llama3_pipe.tokenizer
        self.model = llama3_pipe.model  

        geraldine_agent_text = ""
        dave_agent_text = ""

        if llama_reset == "Yes":
            #self.text_buffer = None  
            self.agent1 = None  
            self.agent2 = None 
            self.current_text_buffer = None

        if self.agent1 is None:
            self.agent1 = AgentGeraldine(ox3d_user_name, current_dir, self.tokenizer, self.max_tokens)
            self.agent1.save_agent_text('agent_geraldine_normal.agt', uncensored=False)
            self.agent1.save_agent_text('agent_geraldine_uncensored.agt', uncensored=True)

        if self.agent2 is None:    
            self.agent2 = AgentDave(ox3d_user_name, current_dir, self.tokenizer, self.max_tokens)           
            self.agent2.save_agent_text('agent_dave_normal.agt', uncensored=False)
            self.agent2.save_agent_text('agent_dave_uncensored.agt', uncensored=True)  

        #if llama_agent_type is not None:
        #    self.current_normal_text = ""
        #    self.current_uncensored_text = ""  
        if self.agent1 is not None:
            try:
                self.geraldine_normal_text = self.agent1.load_agent_text('agent_geraldine_normal.agt')
                self.geraldine_uncensored_text = self.agent1.load_agent_text('agent_geraldine_uncensored.agt')                     
            except FileNotFoundError as e:
                print(e)   

        if self.agent2 is not None:
            try:           
                self.dave_normal_text = self.agent2.load_agent_text('agent_dave_normal.agt')
                self.dave_uncensored_text = self.agent2.load_agent_text('agent_dave_uncensored.agt')          
            except FileNotFoundError as e:
                print(e)     
                
        #print("Geraldine Normal Version:\n", self.geraldine_normal_text)
        #print("\nGeraldine Uncensored Version:\n", self.geraldine_uncensored_text)
        #print("Dave Normal Version:\n", self.dave_normal_text)
        #print("\nDave Uncensored Version:\n", self.dave_uncensored_text)                  

        if llama3_pipe.use_uncensored_agent == "Yes":
            geraldine_agent_text = self.geraldine_uncensored_text
            dave_agent_text = self.dave_uncensored_text
        else:
            geraldine_agent_text = self.geraldine_normal_text
            dave_agent_text = self.dave_normal_text

        if llama_agent_type == "Geraldine":
            self.current_text_buffer = self.agent1.text_buffer
        if llama_agent_type == "Dave":
            self.current_text_buffer = self.agent2.text_buffer              

        agent_str = ""
        #if llama3_pipe.agent is not None:
        #    agent_str = llama3_pipe.agent
        if agent is not None:
            if llama_agent_type == "Geraldine":
                agent_str = f"The user's name is {ox3d_user_name}. follow his directives as you work for him. If {ox3d_user_name} doesn't give you an agent name, your name is Geraldine\n"+agent
            if llama_agent_type == "Dave":
                agent_str = f"The user's name is {ox3d_user_name}. follow his directives as you work for him. If {ox3d_user_name} doesn't give you an agent name, your name is Dave\n"+agent                
        else: # some default agent just for fun...
            if llama_agent_type == "Geraldine":
                agent_str = geraldine_agent_text
            if llama_agent_type == "Dave":
                agent_str = dave_agent_text

        prompt_only = self.prompts

        if agent_mode == "chat":
            use_mix_styles_new = "No"
        else:
            use_mix_styles_new = use_mix_styles
        #mix_text = mix_styles
        #if self.old_prompts != ""
        #if use_mix_styles == "Yes" and use_external_subject == "Yes":
        if use_mix_styles_new == "Yes" and use_external_subject == "Yes":
            if mix_styles is not None and external_subject is not None:
                prompt_only = mix_styles + "\n\n" + prompt_only + "\n" + external_subject 
            if mix_styles is not None and external_subject is None:
                prompt_only = mix_styles + "\n\n" + prompt_only  
            if mix_styles is None and external_subject is not None:
                prompt_only = "\n\n" + prompt_only + "\n" + external_subject                                

        if use_mix_styles_new == "Yes" and use_external_subject == "No":    
            if mix_styles is not None:
                prompt_only = mix_styles + "\n\n" + prompt_only

        if use_mix_styles_new == "No" and use_external_subject == "Yes":    
            if use_external_subject is not None:
                prompt_only = "\n\n" + prompt_only + "\n" + external_subject              
            #if mix_styles is not None and external_subject is not None:
            #    prompt_only = mix_styles + "\n\nimportant to add this subject and actors: " + prompt_only + "\n" + external_subject            

        if disable_generation == "No":
            #if self.text_buffer is None:
            #    self.text_buffer = DG_LlamaTextBuffer(ox3d_user_name, self.tokenizer, self.max_tokens)            

            #if not self.prompts in self.text_buffer.get_buffer():
            prompt_only = str(remove_spaces_lines_total(prompt_only))
            print(f"TESTING PROMPT:\n{prompt_only}")

            if self.current_text_buffer is not None:
                buffer_text = self.current_text_buffer.get_buffer()  # This will now work since text_buffer is initialized
            else: 
                buffer_text = ""

            full_prompt = llama3_pipe.code_format_prompt2(user_query=prompt_only, sprompt_text=agent_str, aprompt_text="")

            #self.prompts = llama3_pipe.code_format_prompt(prompt_only, agent_str, "")
            self.old_prompts = prompt_only#self.prompts

            #u_prompts = "user: " + self.prompts
            if self.current_text_buffer is not None:
                self.current_text_buffer.add_to_buffer(user_input=prompt_only)

            input_ids = self.tokenizer(buffer_text + "\n" + full_prompt, return_tensors="pt").input_ids.to("cuda")
            #input_ids = self.tokenizer(self.prompts, return_tensors="pt").input_ids.to("cuda")

            if llama3_pipe.useseed == True:
                generated_ids = self.model.generate(input_ids, max_new_tokens=llama3_pipe.max_new_tokens, top_k=llama3_pipe.top_k, top_p=llama3_pipe.top_p, temperature=llama3_pipe.temperature, repetition_penalty=llama3_pipe.repetition_penalty, do_sample=True, eos_token_id=self.tokenizer.eos_token_id)
            else:
                generated_ids = self.model.generate(input_ids, max_new_tokens=llama3_pipe.max_new_tokens, top_k=llama3_pipe.top_k, top_p=llama3_pipe.top_p, temperature=llama3_pipe.temperature, repetition_penalty=llama3_pipe.repetition_penalty, do_sample=False, eos_token_id=self.tokenizer.eos_token_id)
        
            self.response = self.tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
          
            self.response = clean_prompt_regex(self.response)

            if remove_from_prompt is not None:
                if use_remove_from_manager == "Yes":
                    self.response = process_prompt_v2(self.response, llama3_pipe.remove_from_prompt + "\n" + remove_from_prompt)
                else:
                    self.response = process_prompt_v2(self.response, remove_from_prompt)
            else:
                if use_remove_from_manager == "Yes":
                    self.response = process_prompt_v2(self.response, llama3_pipe.remove_from_prompt)
                else:
                    self.response = process_prompt_v2(self.response, "")

            self.response = remove_leading_spaces(self.response)

            self.response = self.response.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace('(', '').replace(')', '')

            #self.prompts = "user: " + self.prompts
            #self.response = "agent: " + self.response
            if self.current_text_buffer is not None:
                self.current_text_buffer.add_to_buffer(user_input=prompt_only, assistant_response=self.response)

            #print("Contenu actuel du buffer :")
            #print("[BEGIN]===================================================================================")
            #print(self.text_buffer.get_buffer())
            #print(" ")
            #print(f"Buffer size tokens : {self.text_buffer.get_token_count()}") 
            #print("[END]=====================================================================================")      
        
        if self.response == "":
            self.response = self.old_response

        self.old_response = self.response

        return (self.response, llama3_pipe)    
"""

#####################################################################################################################
# DGLoadDeepSeekModelR1 #############################################################################################
#####################################################################################################################
class DGLoadDeepSeekModelR1:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.model_id = ""
        self.model_name = ""
        self.model_check = 0
        self.offload_device = torch.device('cpu')
        self.device_name = "cpu"
        self.model_file = ""
        self.clear_extra_mem_gpu = "Yes" 

    @classmethod
    def INPUT_TYPES(cls): # pylint: disable = invalid-name, missing-function-docstring
        return { 
            "required": {
                "model_file": (get_filtered_deep_filenames("dg_llama3_2", extensions=['.gguf', '.safetensors']), {"tooltip": "The node is compatible with the model deepseek r1."}), 
                "reset_model": (["No", "Yes"], {"tooltip": "When you reset the model by selecting 'Yes' Press Queue Prompt to reset the model, remember to set it back to 'No' afterward."}),          
                "use_bit_mode": (["4bit","8bit", "nobit"], {"tooltip": "This option don't work with GGUF Model because GGUF model already use an other type of compression."}),
                "device_mode": (["gpu", "cpu"],),
                "clear_extra_mem_gpu": (["Yes", "No"], {"tooltip": "Try to clean a bit a vram when processing text."}),
            }
        }
    
    RETURN_TYPES = ("ANY",)
    RETURN_NAMES = ("deepseek_pipe",)

    FUNCTION = "load_deepseek"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLoadDeepSeekModelR1 (DeepSeek R1 - OX3D)" 

    def load_deepseek(self, model_file, device_mode, reset_model, clear_extra_mem_gpu, use_bit_mode):
        self.clear_extra_mem_gpu = clear_extra_mem_gpu
        print(f"OrionX3D deepseek r1 Model: {model_file}")
        self.model_name = os.path.basename(model_file)

        if reset_model == "Yes":
            self.tokenizer = None
            self.model = None          

        if self.model_file != model_file: 
            self.model_file = model_file
            self.tokenizer = None
            self.model = None         

        self.model_check = 0
        # Check the file extension
        if self.model_file.endswith(".gguf"):
            print("The Model deepseek r1 is a .gguf file.")
            self.model_check = 1
        elif self.model_file.endswith(".safetensors"):
            print("The Model deepseek r1 is a .safetensors file.")
            self.model_check = 2
        else:
            print("The Model deepseek r1 has a different extension.")  
            self.model_check = 0         

        if self.tokenizer is None and self.model is None:
            load_in_4bit = False
            load_in_8bit = False

            if use_bit_mode == "4bit":
                load_in_4bit = True
                load_in_8bit = False
            if use_bit_mode == "8bit":
                load_in_4bit = False
                load_in_8bit = True   
            if use_bit_mode == "nobit":
                load_in_4bit = False
                load_in_8bit = False                
            #
            if device_mode == "cpu":
                self.offload_device = torch.device('cpu')
                self.device_name = "cpu"
            else:
                self.offload_device = torch.device('cuda')
                self.device_name = "cuda"
            #
            if self.model_check == 1:
                self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_modeldir, os.path.dirname(self.model_file)), 
                                                                gguf_file=self.model_name, 
                                                                trust_remote_code=True)                    
                self.model = AutoModelForCausalLM.from_pretrained(os.path.join(current_modeldir, os.path.dirname(self.model_file)), 
                                                                  gguf_file=self.model_name, 
                                                                  low_cpu_mem_usage=True,
                                                                  return_dict=True,
                                                                  torch_dtype=torch.float16, 
                                                                  device_map=self.offload_device,
                                                                  local_files_only=True)  
            elif self.model_check == 2:
                self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_modeldir, os.path.dirname(self.model_file)),  
                                                                trust_remote_code=True)                    
                self.model = AutoModelForCausalLM.from_pretrained(os.path.join(current_modeldir, os.path.dirname(self.model_file)),  
                                                                  torch_dtype=torch.float16,
                                                                  device_map=self.offload_device,
                                                                  load_in_8bit=load_in_8bit,
                                                                  load_in_4bit=load_in_4bit,
                                                                  local_files_only=True)  
            else:
                self.tokenizer = None
                self.model = None   

        return (self,)    
       
#####################################################################################################################
# DGPromptGenSeepSeekR1 #############################################################################################
#####################################################################################################################
class DGPromptGenSeepSeekR1:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.model_id = ""
        self.model_name = ""
        self.think_section = ""
        self.final_response = ""
        self.model_file = ""
        self.oldseed = -1
        self.useseed = True
        self.seed = -1    
        self.temperature = 0.6000
        self.top_p = 0.9000
        self.top_k = 1
        self.repetition_penalty = 1.1   
#        self.offload_device = torch.device('cpu')
        random.seed(time.time())     

    @classmethod
    def INPUT_TYPES(cls): # pylint: disable = invalid-name, missing-function-docstring
        return { 
            "required": {
#                "model_file": (get_filtered_deep_filenames("dg_llama3_2", extensions=['.gguf', '.safetensors']), {"tooltip": "The node is compatible with the model deepseek r1."}),            
                "deepseek_pipe": ("ANY",),
                "prompt_mode": (["Image", "Video", "Chat", "Other"],{"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "use_seeder": (["Yes", "No"],),
                "use_mix_styles": (["No", "Yes"],),
                "use_custom_prompt": (["No", "Yes"], {"tooltip": "This option disable the llama model and use the text subject directly."}),
                "use_external_subject": (["No", "Yes"], {"tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),
                "seeder": ("INT", {"forceInput": True, "default": -1, "min": 0, "max": 0xffffffffffffffff}),
                "max_token": ("INT", {"default": 2048, "min": 256, "max": 4096, "step": 32}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0000, "max": 2.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Adjusts the creativity of the AI's responses by controlling how many possible words it considers. Lower values make outputs more predictable; higher values allow for more varied and creative responses."}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 50, "step": 1, "tooltip": "Limits the AI to choose from the top 'k' most probable words. Lower values make responses more focused; higher values introduce more variety and potential surprises."}),
                "temperature": ("FLOAT", {"default": 0.6000, "min": 0.0000, "max": 5.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Controls the randomness of the output; higher values produce more random results."}),
                "repetition_penalty": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 2.0, "step": 0.1, "round": 0.1, "tooltip": "Penalty for repeated tokens; higher values discourage repetition."}),                
                "subject": ('STRING', {"multiline": True, "default": "", "tooltip": "The user text to direct Llama to generate the prompt."}),
                "custom_prompt": ('STRING', {"multiline": True, "default": "", "tooltip": "Disable the llama generation and une the custom prompt."}),
                #"device_mode": (["gpu", "cpu"],), # device_mode gpu = cuda, because the most compatible video cards are from nvidia and the most used gpu tool egal cuda.
                "always_unpaused": (["Yes", "No"],),
                "pause_generation": ("BOOLEAN", {"default": True, "label_on": "Pause", "label_off": "Unpause"}),                
            },
            "optional": {
                "agent": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent, "tooltip": "The agent text to describe the Llama agent."}),    
                "mix_styles": ("STRING", {"forceInput": True, "multiline": True}),  
                "external_subject": ("STRING", {"forceInput": True, "multiline": True, "tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),            
            }
        }
    
    RETURN_TYPES = ("STRING","STRING","ANY","STRING",)
    RETURN_NAMES = ("prompt","think","deepseek_pipe","mix_styles",)

    FUNCTION = "generate_prompt"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGPromptGenDeepSeekR1 (DeepSeekR1 - OX3D)" 

    # device_mode, model_file,
    def generate_prompt(self, deepseek_pipe, always_unpaused, use_custom_prompt, custom_prompt, pause_generation, subject, prompt_mode, use_mix_styles, use_external_subject, max_token, seeder, use_seeder, top_p, top_k, temperature, repetition_penalty, agent=None, mix_styles=None, external_subject=None):
        
        self.tokenizer = deepseek_pipe.tokenizer
        self.model = deepseek_pipe.model
        self.model_id = deepseek_pipe.model_id
        self.model_name = deepseek_pipe.model_name        
        
        self.temperature = temperature
        self.top_p = top_p
        self.top_k = top_k
        self.repetition_penalty = repetition_penalty     
    
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
        
        """
        print(f"OrionX3D deepseek r1 Model: {model_file}")
        self.model_name = os.path.basename(model_file)

        if self.model_file != model_file: 
            self.model_file = model_file
            self.tokenizer = None
            self.model = None         

        model_check = 0
        # Check the file extension
        if self.model_file.endswith(".gguf"):
            print("The Model deepseek r1 is a .gguf file.")
            model_check = 1
        elif self.model_file.endswith(".safetensors"):
            print("The Model deepseek r1 is a .safetensors file.")
            model_check = 2
        else:
            print("The Model deepseek r1 has a different extension.")  
            model_check = 0         

        if self.tokenizer is None and self.model is None:
            #
            if device_mode == "cpu":
                self.offload_device = torch.device('cpu')
            else:
                self.offload_device = torch.device('cuda')
            #
            if model_check == 1:
                self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_modeldir, os.path.dirname(self.model_file)), 
                                                                gguf_file=self.model_name, 
                                                                trust_remote_code=True)                    
                self.model = AutoModelForCausalLM.from_pretrained(os.path.join(current_modeldir, os.path.dirname(self.model_file)), 
                                                                  gguf_file=self.model_name, 
                                                                  torch_dtype=torch.float16, 
                                                                  device_map=self.offload_device,
                                                                  local_files_only=True)  
            elif model_check == 2:
                self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_modeldir, os.path.dirname(self.model_file)),  
                                                                trust_remote_code=True)                    
                self.model = AutoModelForCausalLM.from_pretrained(os.path.join(current_modeldir, os.path.dirname(self.model_file)),  
                                                                  torch_dtype=torch.float16,
                                                                  device_map=self.offload_device,
                                                                  local_files_only=True)  
            else:
                self.tokenizer = None
                self.model = None    
        """                        
        #    
        if use_custom_prompt == "No" and (pause_generation == False or always_unpaused == "Yes"):  
            if self.tokenizer is not None and self.model is not None:
                tokenizer = self.tokenizer

                text = ""
                auser = ""

                if agent is None:
                    auser = ox3d_user_name
                    system_prompt = f"You are a highly creative expert assistant for helping user {auser} in creating prompt texts for images, photos, and videos."
                else:
                    auser = ""
                    system_prompt = agent

                chat_str = subject
                if prompt_mode == "Image":
                    #if auser != "":
                    chat_str = "An high quality image prompt about - " + subject
                    #else:
                    #    chat_str = "An high quality image prompt about - " + subject
                if prompt_mode == "Video":
                    #if auser != "":
                    chat_str = "A high quality video prompt about - " + subject    
                    #else:
                    #    chat_str = "A high quality video prompt about - " + subject  
                if prompt_mode == "Chat":
                    #if auser != "":
                    chat_str = "I'm here for chat - " + subject 
                    #else:  
                    #    chat_str = "I'm here for chat - " + subject 

                if prompt_mode == "Other":
                    chat_str = subject

                eval_style = False   

                if mix_styles is not None and external_subject is not None:
                    if mix_styles != "" and external_subject != "":
                        if use_mix_styles == "Yes" and use_external_subject == "Yes":
                            eval_style = True
                            chat_str = f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + external_subject + "\n" + mix_styles
                        if use_mix_styles == "Yes" and use_external_subject == "No":
                            eval_style = True
                            chat_str =  f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + mix_styles
                        if use_mix_styles == "No" and use_external_subject == "Yes":
                            eval_style = True
                            chat_str = f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + external_subject

                if mix_styles is not None and external_subject is None:
                    if mix_styles != "":
                        if use_mix_styles == "Yes":
                            eval_style = True
                            chat_str = f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + mix_styles 

                if mix_styles is None and external_subject is not None:
                    if external_subject != "":                    
                        if use_external_subject == "Yes":
                            eval_style = True
                            chat_str = f"user {ox3d_user_name} main topic " + chat_str + "\n" + "mix with " + external_subject  

                if eval_style == True:
                    chat_str = chat_str + "\n" + "If styles are similar or mean the same, choose the one that works best for the prompt. Be creative, and try to craft a prompt of 500 tokens maximum or less." 

                if deepseek_pipe.model_check == 1:  
                    #formatted_prompt = format_prompt_gguf3(system_prompt, subject)
                    #text = formatted_prompt
                    #"""
                    system_msg = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chat_str},
                    ]  
                    text = self.tokenizer.apply_chat_template(
                        system_msg,
                        tokenize=False,
                        add_generation_prompt=True,
                    )      
                    #"""            

                if deepseek_pipe.model_check == 2:
                    system_msg = [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": chat_str},
                    ]  
                    text = self.tokenizer.apply_chat_template(
                        system_msg,
                        tokenize=False,
                        add_generation_prompt=True,
                    )                      

                if not isinstance(text, str):
                    raise TypeError(f"OX3D error apply_chat_template() a renvoyé {type(text)} au lieu de str.")

                input_ids = tokenizer([text], return_tensors="pt").input_ids.to(deepseek_pipe.device_name)

                if self.tokenizer.pad_token_id is None:
                    self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
                if self.model.config.pad_token_id is None:
                    self.model.config.pad_token_id = self.model.config.eos_token_id              

                if use_seeder == "Yes":
                    generated_ids = self.model.generate(input_ids, max_new_tokens=max_token, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, do_sample=True, num_return_sequences=1) #, eos_token_id=self.tokenizer.eos_token_id #     
                else:
                    generated_ids = self.model.generate(input_ids, max_new_tokens=max_token, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, do_sample=False, num_return_sequences=1) #, eos_token_id=self.tokenizer.eos_token_id #        
            
                #add_special_tokens=False,
                #self.response = tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)    
            
                if deepseek_pipe.model_check == 1:
                    self.response = tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], add_special_tokens=True, skip_special_tokens=False, clean_up_tokenization_space=True)
                    #self.think_section = self.response
                    # The gguf version behaving differently.
                    # I personally prefered the original model with the chat template...
                    # I have try to add a better way to deal with the gguf token method, it look to work but surely need a better implementation.

                    self.response = "<think>\n" + self.response
                    self.think_section, self.final_response = extract_sections_gguf2(self.response)

                    #self.think_section, self.final_response = extract_think_and_response(self.response)

                    #self.think_section, self.final_response = extract_think_and_response(self.response)  
                    #self.think_section = self.response

                if deepseek_pipe.model_check == 2:
                    self.response = tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
                    self.think_section, self.final_response = extract_think_and_response(self.response)            
            #extract_think_and_response
            self.oldseed = nseed

            if deepseek_pipe.clear_extra_mem_gpu == "Yes":  
                torch.cuda.empty_cache()
                empty_cache()        
        else:
            if use_custom_prompt == "Yes":
                self.final_response = custom_prompt
            if self.final_response == "":
                self.final_response = custom_prompt            

        astyle = ""
        if mix_styles is not None:
            astyle = mix_styles

        return (self.final_response, self.think_section, deepseek_pipe, astyle)
    
#####################################################################################################################
# DGLoadLlamaModel3_x ###############################################################################################
#####################################################################################################################
class DGLoadLlamaModel3_x:
    def __init__(self):  
        self.tokenizer = None
        self.model = None
        self.model_id = ""
        self.model_name = ""
        self.model_file = ""
        self.current_agent = None
        self.agent1 = None
        self.agent2 = None
        self.codeA = "<|begin_of_text|>"
        self.codeB = "<|start_header_id|>"
        self.codeC = "<|end_header_id|>"
        self.codeD = "<|eot_id|>" 
        self.remove_from_prompt = ""     
        self.offload_device = torch.device('cpu')  
        self.clear_extra_mem_gpu = "Yes"      
        self.device_name = "cpu"          

    @classmethod
    def INPUT_TYPES(cls): # pylint: disable = invalid-name, missing-function-docstring
        return { 
                "required": {
                #get_filtered_filenames    
                "model_file": (get_filtered_llama_filenames("dg_llama3_2", extensions=['.gguf', '.safetensors']), {"tooltip": "The node is compatible with the model llama 3.1 too."}),
                "reset_model": (["No", "Yes"], {"tooltip": "When you reset the model by selecting 'Yes' Press Queue Prompt to reset the model, remember to set it back to 'No' afterward."}),
                "use_bit_mode": (["4bit","8bit", "nobit"], {"tooltip": "This option don't work with GGUF Model because GGUF model already use an other type of compression."}),           
                "device_mode": (["gpu", "cpu"],),
                "clear_extra_mem_gpu": (["Yes", "No"], {"tooltip": "Try to clean a bit a vram when processing text."}), 
            }
        }
    
    RETURN_TYPES = ("ANY",)
    RETURN_NAMES = ("llama3_pipe",)

    FUNCTION = "load_llama3"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLoadLlamaModel3 (Llama 3.1 & 3.2 - OX3D)" 
    
    def load_llama3(self, model_file, device_mode, reset_model, use_bit_mode, clear_extra_mem_gpu):
        print(f"OrionX3D llama Model: {model_file}")
        self.clear_extra_mem_gpu = clear_extra_mem_gpu
        if self.model_file != model_file: 
            self.model_file = model_file
            self.tokenizer = None
            self.model = None 

        config_file = os.path.join(current_dir, "dg_llama_managers.cfg")
        #
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            try:
                # I use this code system because some fine-tuned Llama models no longer use the original system code.
                # With this method, I can change the code through a configuration.
                # It needs an update later to add the possibility of loading multiple configuration files.
                # Currently, it only works with the original model code.
                self.codeA = config.get('prompts', 'codeA')
                self.codeB = config.get('prompts', 'codeB')
                self.codeC = config.get('prompts', 'codeC')
                self.codeD = config.get('prompts', 'codeD')
                self.modeA = config.get('modes', 'modeA')
                self.modeB = config.get('modes', 'modeB')
                self.modeC = config.get('modes', 'modeC')                
                #print(f"OrionX3D llama 3.x Configurations loaded: \n- Prompt codeA: {self.codeA}\n- Prompt codeB: {self.codeB}\n- Prompt codeC: {self.codeC}\n- Prompt codeD: {self.codeD}\n- Mode modeA: {self.modeA}\n- Mode modeB: {self.modeB}\n- Mode modeC: {self.modeC}")
            except configparser.NoSectionError as e:
                print(f"OrionX3D llama 3.x Missing section in configuration file: {e}")
            except configparser.NoOptionError as e:
                print(f"OrionX3D llama 3.x Missing option in configuration file: {e}")
        else:
            print(f"OrionX3D llama 3.x Configuration file '{config_file}' not found. Please ensure it exists or provide default configurations.")  

        filepath = os.path.join(current_dir, "remove_from_prompt.rem")

        remove_from_promptN = load_text_from_file(filepath)

        """
        if remove_from_prompt is None:
            if use_internal_remove == "Yes":
                remove_from_prompt = remove_from_promptN
            else:
                remove_from_prompt = ""
        else:
            if use_internal_remove == "Yes":
                remove_from_prompt = remove_from_promptN + "\n" + remove_from_prompt
            else:
                remove_from_prompt = ""
        """
        remove_from_prompt = remove_from_promptN

        self.remove_from_prompt = remove_from_prompt                      

        if reset_model == "Yes":
            self.tokenizer = None
            self.model = None             

        if self.tokenizer is None and self.model is None:
            load_in_4bit = False
            load_in_8bit = False
            model_check = 0
            # Check the file extension
            if model_file.endswith(".gguf"):
                print("The Model llama 3.x is a .gguf file.")
                model_check = 1
            elif model_file.endswith(".safetensors"):
                print("The Model llama 3.x is a .safetensors file.")
                model_check = 2
            else:
                print("The Model llama 3.x has a different extension.")  
                model_check = 0 

            if use_bit_mode == "4bit":
                load_in_4bit = True
                load_in_8bit = False
            if use_bit_mode == "8bit":
                load_in_4bit = False
                load_in_8bit = True   
            if use_bit_mode == "nobit":
                load_in_4bit = False
                load_in_8bit = False                               

            self.model_name = os.path.basename(model_file)

            if device_mode == "cpu":
                self.offload_device = torch.device('cpu')
                self.device_name = "cpu"
            else:
                self.offload_device = torch.device('cuda')  
                self.device_name = "cuda"          
   
            if model_check == 1:
                self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_modeldir, os.path.dirname(model_file)), 
                                                               gguf_file=self.model_name, 
                                                               trust_remote_code=True)                    
                self.model = AutoModelForCausalLM.from_pretrained(os.path.join(current_modeldir, os.path.dirname(model_file)), 
                                                                  gguf_file=self.model_name, 
                                                                  low_cpu_mem_usage=True,
                                                                  return_dict=True,
                                                                  torch_dtype=torch.float16, 
                                                                  device_map=self.offload_device,
                                                                  local_files_only=True)
            if model_check == 2:
                self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_modeldir, os.path.dirname(model_file)), 
                                                               trust_remote_code=True)    

                self.model = LlamaForCausalLM.from_pretrained(os.path.join(current_modeldir, os.path.dirname(model_file)), 
                                                              torch_dtype=torch.float16,
                                                              device_map=self.offload_device,
                                                              load_in_8bit=load_in_8bit,
                                                              load_in_4bit=load_in_4bit,
                                                              local_files_only=True,
                                                              use_flash_attention_2=False)  
            if model_check == 0:      
                self.model = None   
                self.tokenizer = None 

        if self.tokenizer is not None and self.model is not None:
            # Just use for create the file if it not exist, I can change this later with a better implementation
            #if self.agent1 is None:
            #if self.agent1 is None:
            self.agent1 = AgentGeraldine(ox3d_user_name, current_dir, self.tokenizer, 4096)

            self.agent1.save_agent_text("agent_geraldine_normal.agt", False, create_agent_geraldine_text(False))
            self.agent1.save_agent_text("agent_geraldine_uncensored.agt", True, create_agent_geraldine_text(True))
            self.current_agent = self.agent1 # yes I know it look strange, but it is ok for now...
            # Just use for create the file if it not exist, I can change this later with a better implementation
            #if self.agent2 is None:
            #if self.agent2 is None:
            self.agent2 = AgentDave(ox3d_user_name, current_dir, self.tokenizer, 4096)

            self.agent2.save_agent_text("agent_dave_normal.agt", False, create_agent_dave_text(False))
            self.agent2.save_agent_text("agent_dave_uncensored.agt", True, create_agent_dave_text(True)) 
            #self.current_agent = self.agent2 # yes I know it look strange, but it is ok for now...                             

        return (self,)
                    
#####################################################################################################################
# DGPromptGenLlama3_2 ###############################################################################################
#####################################################################################################################

class DGPromptGenLlama3_2:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.model_id = ""
        self.model_name = ""
        self.oldseed = -1
        self.response = ""
        self.prompts = ""
        self.model_file = ""
        self.agent = ""
        self.internal_agent = ""
        self.max_new_tokens = 4096
#        self.codeA = "<|begin_of_text|>"
#        self.codeB = "<|start_header_id|>"
#        self.codeC = "<|end_header_id|>"
#        self.codeD = "<|eot_id|>"
        self.llama3_pipe = None             
        self.remove_from_prompt = ""
        self.use_uncensored_agent = "Yes"
        self.temperature = 0.6000
        self.top_p = 0.9000
        self.top_k = 1
        self.repetition_penalty = 1.1
        self.useseed = True
        self.seed = -1
        self.full_mix_styles = ""
#        self.agent1 = None
#        self.agent2 = None
#        self.current_agent = None
#        self.clear_extra_mem_gpu = "Yes" 
        #self.offload_device = torch.device('cpu')        
        random.seed(time.time())    

    @classmethod
    def INPUT_TYPES(cls): # pylint: disable = invalid-name, missing-function-docstring
        return { 
            "required": {
                "llama3_pipe": ("ANY",),
#                "model_file": (get_filtered_filenames("dg_llama3_2", extensions=['.gguf', '.safetensors']), {"tooltip": "The node is compatible with the model llama 3.1 too."}),
                "styles_variation": ("INT", {"default": 1, "min": 1, "max": 10, "step": 1, "tooltip": "Adding more or less words about the topic."}),
                "prompt_styles": (get_prompt_styles(), {"default": "Other", "tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
#                "reset_model": (["No", "Yes"], {"tooltip": "When you reset the model by selecting 'Yes' Press Queue Prompt to reset the model, remember to set it back to 'No' afterward."}),
#                "use_bit_mode": (["4bit","8bit", "nobit"], {"tooltip": "This option don't work with GGUF Model because GGUF model already use an other type of compression."}),
                "prompt_mode": (["Image", "Video", "Other"],{"tooltip": "If you use Other it don't apply any styles, it only use the user subject."}),
                "only_english": (["Yes", "No"], {"tooltip": "This option try to force English only but it can depend a lot from the model too."}),
                "use_seeder": (["Yes", "No"],),
                "seeder": ("INT", {"forceInput": True, "default": -1, "min": 0, "max": 0xffffffffffffffff}),
                "use_mix_styles": (["No", "Yes"],),
                "use_custom_prompt": (["No", "Yes"], {"tooltip": "This option disable the llama model and use the text subject directly."}),
                "use_external_subject": (["No", "Yes"], {"tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),
                "max_token": ("INT", {"default": 2048, "min": 256, "max": 4096, "step": 32}),
                "top_p": ("FLOAT", {"default": 0.9, "min": 0.0000, "max": 2.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Adjusts the creativity of the AI's responses by controlling how many possible words it considers. Lower values make outputs more predictable; higher values allow for more varied and creative responses."}),
                "top_k": ("INT", {"default": 50, "min": 1, "max": 50, "step": 1, "tooltip": "Limits the AI to choose from the top 'k' most probable words. Lower values make responses more focused; higher values introduce more variety and potential surprises."}),
                "temperature": ("FLOAT", {"default": 0.6000, "min": 0.0000, "max": 5.0000, "step": 0.0001, "round": 0.0001, "tooltip": "Controls the randomness of the output; higher values produce more random results."}),
                "repetition_penalty": ("FLOAT", {"default": 1.1, "min": 0.0, "max": 2.0, "step": 0.1, "round": 0.1, "tooltip": "Penalty for repeated tokens; higher values discourage repetition."}),
                #"frequency_penalty": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1, "round": 0.1, "tooltip": "Decreases the likelihood of the model repeating the same lines verbatim."}),
                #"presence_penalty": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 2.0, "step": 0.1, "round": 0.1, "tooltip": "Increases the likelihood of the model introducing new topics."}),
#                "device_mode": (["gpu", "cpu"],),
#                "clear_extra_mem_gpu": (["Yes", "No"], {"tooltip": "Try to clean a bit a vram when processing text."}), 
                "subject": ('STRING', {"multiline": True, "default": "", "tooltip": "The user text to direct Llama to generate the prompt."}),                      
                "custom_prompt": ('STRING', {"multiline": True, "default": "", "tooltip": "Disable the llama generation and une the custom prompt."}),
                "use_uncensored_agent": (["No", "Yes"],), 
                "use_internal_agent": (["Yes", "No"],),  
                "use_internal_remove": (["Yes", "No"],),
                "use_assistant": (["No", "Yes"],),
#                "disable_generation": (["No", "Yes"],),
                "always_unpaused": (["Yes", "No"],),
                "pause_generation": ("BOOLEAN", {"default": True, "label_on": "Pause", "label_off": "Unpause"}),                 
            },
            "optional": {
                "mix_styles": ("STRING", {"forceInput": True, "multiline": True}), 
                "agent": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent, "tooltip": "The agent text to describe the Llama agent."}),
                "external_subject": ("STRING", {"forceInput": True, "multiline": True, "tooltip": "This option is use for add an external subject, exemple from florence2 image to text caption."}),     
                "assistant": ('STRING', {"forceInput": True, "multiline": True, "default": str_assistant, "tooltip": "When the assistant is active, it generates responses based on the user's input; it is preferable to turn off the assistant for prompt generation to ensure only the user's input is used without additional responses."}),      
                "remove_from_prompt": ('STRING', {"forceInput": True, "multiline": True, "default": str_agent_remove, "tooltip": "Use for remove or modify text in the prompt result.\nUse Exemple 1 [Replace:Create a -> A] 'Create a ' is replace by ' A'\nUse Exemple 2 [Replace:Here is -> ] 'Here is ' is replace by ' ' nothing."}), 
            }
        }
    
    RETURN_TYPES = ("STRING","ANY","STRING",)
    RETURN_NAMES = ("prompt","llama3_pipe","mix_styles",)

    FUNCTION = "generate_prompt"  

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGPromptGenLlama (Llama 3.1 & 3.2 - OX3D)"  
    #OUTPUT_NODE = True      

    #frequency_penalty, presence_penalty, reset_model, use_bit_mode, device_mode, model_file, clear_extra_mem_gpu, disable_generation,
    def generate_prompt(self, llama3_pipe, always_unpaused, pause_generation, styles_variation, prompt_styles, prompt_mode, only_english, use_seeder, seeder, use_custom_prompt, subject, use_external_subject, max_token, top_p, top_k, temperature, repetition_penalty, custom_prompt, use_internal_remove, use_internal_agent, use_uncensored_agent, use_assistant, use_mix_styles, remove_from_prompt = None, agent = None, assistant = None, external_subject = None, mix_styles= None):
        #print(f"OrionX3D llama Model: {model_file}")
        self.llama3_pipe = llama3_pipe
        self.tokenizer = llama3_pipe.tokenizer
        self.model = llama3_pipe.model
        self.model_id = llama3_pipe.model_id
        self.model_name = llama3_pipe.model_name      
        
        self.clear_extra_mem_gpu = llama3_pipe.clear_extra_mem_gpu

        self.use_uncensored_agent = use_uncensored_agent
        #self.max_tokens = max_token - 256 
        """
        config_file = os.path.join(current_dir, "dg_llama_managers.cfg")
        #
        if os.path.exists(config_file):
            config = configparser.ConfigParser()
            config.read(config_file)
            try:
                # I use this code system because some fine-tuned Llama models no longer use the original system code.
                # With this method, I can change the code through a configuration.
                # It needs an update later to add the possibility of loading multiple configuration files.
                # Currently, it only works with the original model code.
                self.codeA = config.get('prompts', 'codeA')
                self.codeB = config.get('prompts', 'codeB')
                self.codeC = config.get('prompts', 'codeC')
                self.codeD = config.get('prompts', 'codeD')
                self.modeA = config.get('modes', 'modeA')
                self.modeB = config.get('modes', 'modeB')
                self.modeC = config.get('modes', 'modeC')                
                #print(f"OrionX3D llama 3.x Configurations loaded: \n- Prompt codeA: {self.codeA}\n- Prompt codeB: {self.codeB}\n- Prompt codeC: {self.codeC}\n- Prompt codeD: {self.codeD}\n- Mode modeA: {self.modeA}\n- Mode modeB: {self.modeB}\n- Mode modeC: {self.modeC}")
            except configparser.NoSectionError as e:
                print(f"OrionX3D llama 3.x Missing section in configuration file: {e}")
            except configparser.NoOptionError as e:
                print(f"OrionX3D llama 3.x Missing option in configuration file: {e}")
        else:
            print(f"OrionX3D llama 3.x Configuration file '{config_file}' not found. Please ensure it exists or provide default configurations.")
        """
        #
        self.agent = agent

        strA = "Cutting Knowledge Date: December 2023"
        strB = "Today Year: 2025"
        strC = "You are an expert in composing prompts text about video and image, and your agent name are Orion"
        strD = "Be creative and reconstruct a prompt using the information I provide"
        strE = "Do not add length information when you create a video prompt"
        strF = "Try to keep the prompt to a maximum of 256 tokens or less"
        strG = "It is strictly forbidden for the assistant to respond with text unless it is a prompt; it must only provide the final prompt without any additional text, as this could disrupt the system"
        strH = "If the prompt style requests a color, option, sign, poster, text, sprite bubble text, action, or anythings more it is important to use it for create the prompt, same about the styles and subjects and actors"

        if use_uncensored_agent == "Yes":
            self.internal_agent = f"""{strA}\n{strB}\n\n{strC}\n{strD}\n{strE}\n{strF}\n{strG}\n{strH}\n{prompt_instructionsExp}"""
        else:
            self.internal_agent = f"""{strA}\n{strB}\n\n{strC}\n{strD}\n{strE}\n{strF}\n{strG}\n{strH}\n{prompt_instructions}"""

        #self.max_new_tokens = max_token
        # Currently forcing the maximum for using styles and external subjects.
        # This works fine for Llama 3B and larger models.
        # With Llama 1B, it could potentially cause problems.
        # Llama 1B is not very good with prompts and translations; it's better to use the 3B model or larger.
        self.max_new_tokens = max_token

        """
        if self.model_file != model_file: 
            self.model_file = model_file
            self.tokenizer = None
            self.model = None 
        """
        #
        """
        if reset_model == "Yes":
            self.tokenizer = None
            self.model = None 
        """
        #
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
        #
        #if self.tokenizer is None and self.model is None:
            """
            load_in_4bit = False
            load_in_8bit = False
            model_check = 0
            # Check the file extension
            if model_file.endswith(".gguf"):
                print("The Model llama 3.x is a .gguf file.")
                model_check = 1
            elif model_file.endswith(".safetensors"):
                print("The Model llama 3.x is a .safetensors file.")
                model_check = 2
            else:
                print("The Model llama 3.x has a different extension.")  
                model_check = 0 
            """

            """
            if use_bit_mode == "4bit":
                load_in_4bit = True
                load_in_8bit = False
            if use_bit_mode == "8bit":
                load_in_4bit = False
                load_in_8bit = True   
            if use_bit_mode == "nobit":
                load_in_4bit = False
                load_in_8bit = False                               
            """
            
            """
            self.model_name = os.path.basename(model_file)

            if device_mode == "cpu":
                self.offload_device = torch.device('cpu')
            else:
                self.offload_device = torch.device('cuda')            
   
            if model_check == 1:
                self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_modeldir, os.path.dirname(model_file)), 
                                                               gguf_file=self.model_name, 
                                                               trust_remote_code=True)                    
                self.model = AutoModelForCausalLM.from_pretrained(os.path.join(current_modeldir, os.path.dirname(model_file)), 
                                                                  gguf_file=self.model_name, 
                                                                  low_cpu_mem_usage=True,
                                                                  return_dict=True,
                                                                  torch_dtype=torch.float16, 
                                                                  device_map=self.offload_device,
                                                                  local_files_only=True)
            if model_check == 2:
                self.tokenizer = AutoTokenizer.from_pretrained(os.path.join(current_modeldir, os.path.dirname(model_file)), 
                                                               trust_remote_code=True)    

                self.model = LlamaForCausalLM.from_pretrained(os.path.join(current_modeldir, os.path.dirname(model_file)), 
                                                              torch_dtype=torch.float16,
                                                              device_map=self.offload_device,
                                                              load_in_8bit=load_in_8bit,
                                                              load_in_4bit=load_in_4bit,
                                                              local_files_only=True,
                                                              use_flash_attention_2=False)  
            if model_check == 0:      
                self.model = None   
                self.tokenizer = None   
            """
                
        pMode = ""
        pType = ""

        pMode = "Main style:\n"

        if prompt_mode == "Video":
            pMode = pMode + "video very high quality\n\n"
            pType = "video"
        if prompt_mode == "Image":
            pMode = pMode + "image or a photo very high quality\n\n" 
            pType = "image"
        if prompt_mode == "Other":
            pMode = "very high quality" 
            pType = ""

        rmain_style = generate_prompt_style(prompt_styles, media_type=pType, num_keywords=styles_variation)
        #if PromptMode.lower() != "other" and Prompt_styles.lower() != "other":
        if prompt_styles != "Other" and use_mix_styles != "No":
            pMode = "Don't mention the mixed styles that you combined to the user\n" + generate_prompt_style(prompt_styles, media_type=pType, num_keywords=styles_variation) + "\n" + pMode + "\n"
        #else:
        #    pMode = ""

        pLang = ""
        if only_english == "Yes":  
            pLang = eng_law
        if only_english == "No":  
            pLang = ""  

        ptext = ""
        if use_external_subject == "Yes":
            if external_subject is not None:
                ptext = "\n" + external_subject  

        if use_internal_agent == "No":
            self.internal_agent = ""
            if self.agent is not None:
                self.internal_agent = self.agent
        else:
            if self.agent is not None:
                self.internal_agent = self.internal_agent + "\n" + self.agent 

        if mix_styles is not None and use_mix_styles != "No":
            pMode = pMode + "Styles for mix with the main style:\n\n"
            pMode = pMode + mix_styles

        self.full_mix_styles = pMode  
        self.full_mix_styles = remove_spaces_lines_total(self.full_mix_styles) 

        if mix_styles is not None and use_mix_styles != "No": 
            if rmain_style != "":
                rmain_style = rmain_style + "\n" + mix_styles

        if use_mix_styles != "No":
            rf_mix_styles = remove_spaces_lines_total(rmain_style)      
        else:                                                    
            rf_mix_styles = ""

        #if disable_generation == "No":
        if self.tokenizer is not None and self.model is not None:

            """
            # Just use for create the file if it not exist, I can change this later with a better implementation
            #if self.agent1 is None:
            self.agent1 = AgentGeraldine(ox3d_user_name, current_dir, self.tokenizer, self.max_new_tokens)
            self.agent1.save_agent_text("agent_geraldine_normal.agt", False, create_agent_geraldine_text(False))
            self.agent1.save_agent_text("agent_geraldine_uncensored.agt", True, create_agent_geraldine_text(True))
            self.current_agent = self.agent1 # yes I know it look strange, but it is ok for now...
            # Just use for create the file if it not exist, I can change this later with a better implementation
            #if self.agent2 is None:
            self.agent2 = AgentDave(ox3d_user_name, current_dir, self.tokenizer, self.max_new_tokens)
            self.agent2.save_agent_text("agent_dave_normal.agt", False, create_agent_dave_text(False))
            self.agent2.save_agent_text("agent_dave_uncensored.agt", True, create_agent_dave_text(True)) 
            #self.current_agent = self.agent2 # yes I know it look strange, but it is ok for now...         
            """
            #if pause_generation == False or always_unpaused == "Yes":
            if use_custom_prompt == "No" and (pause_generation == False or always_unpaused == "Yes"): 

                """
                if use_assistant == "Yes":          
                    if assistant is not None:                                   
                        #self.prompts = cons_law + self.code_format_prompt(pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang, self.internal_agent, assistant)  
                        self.prompts = self.code_format_prompt(cons_law + pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang, self.internal_agent, assistant)
                    else:
                        #self.prompts = cons_law + self.code_format_prompt(pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang, self.internal_agent, "")  
                        self.prompts = self.code_format_prompt(cons_law + pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang, self.internal_agent, "")
                    #print(f"prompt: {self.prompts}")                      
                else:
                    #self.prompts = cons_law + self.code_format_prompt(pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang, self.internal_agent,"") 
                    self.prompts = self.code_format_prompt(cons_law + pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang, self.internal_agent,"") 
                    #
                    #print(f"prompt: {self.prompts}") 
                """
                system_msg = []

                if use_assistant == "Yes": 
                    if assistant is not None:  
                        system_msg = [
                            {"role": "system", "content": self.internal_agent},
                            {"role": "user", "content": cons_law + pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang},
                            {"role": "assistant", "content": assistant},
                        ]  
                    else:
                        system_msg = [
                            {"role": "system", "content": self.internal_agent},
                            {"role": "user", "content": cons_law + pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang},
                        ]                        
                else:
                    system_msg = [
                        {"role": "system", "content": self.internal_agent},
                        {"role": "user", "content": cons_law + pMode + "\n\nimportant to add this subject and actors: " + subject + "\n" + ptext + pLang},
                    ]  

                input_text = self.tokenizer.apply_chat_template(system_msg, tokenize=False, add_generation_prompt=True)

                if not isinstance(input_text, str):
                    raise TypeError(f"OX3D error apply_chat_template() a renvoyé {type(input_text)} au lieu de str.")
                
                #, padding=True, truncation=True
                #self.prompts 
                input_ids = self.tokenizer(input_text, return_tensors="pt").input_ids.to(llama3_pipe.device_name)
                generated_ids = None

                if self.tokenizer.pad_token_id is None:
                    self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
                if self.model.config.pad_token_id is None:
                    self.model.config.pad_token_id = self.model.config.eos_token_id                

                if use_seeder == "Yes":
                    generated_ids = self.model.generate(input_ids, max_new_tokens=self.max_new_tokens, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, do_sample=True, num_return_sequences=1) #, eos_token_id=self.tokenizer.eos_token_id #frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                else:
                    generated_ids = self.model.generate(input_ids, max_new_tokens=self.max_new_tokens, top_p=top_p, top_k=top_k, temperature=temperature, repetition_penalty=repetition_penalty, do_sample=False, num_return_sequences=1) #, eos_token_id=self.tokenizer.eos_token_id #frequency_penalty=frequency_penalty, presence_penalty=presence_penalty,
                
                #add_special_tokens=False, 
                self.response = self.tokenizer.decode(generated_ids[0][input_ids.shape[-1]:], skip_special_tokens=True, clean_up_tokenization_space=True)
                self.response = self.response.replace('\n', ' ').replace('\r', ' ').replace('"', '').replace('(', '').replace(')', '')  
                #self.response = process_prompt(self.response, remove_from_prompt)                    
            else:
                if self.response == "":
                    self.prompts = custom_prompt
                else:
                    self.prompts = self.response

                self.response = self.prompts
                #print(f"prompt: {self.prompts}") 

            self.oldseed = seeder

            if llama3_pipe.clear_extra_mem_gpu == "Yes":  
                torch.cuda.empty_cache()
                empty_cache()

            if use_custom_prompt == "No" and (pause_generation == False or always_unpaused == "Yes"):

                """  
                filepath = os.path.join(current_dir, "remove_from_prompt.rem")
                remove_from_promptN = load_text_from_file(filepath)

                if remove_from_prompt is None:
                    if use_internal_remove == "Yes":
                        remove_from_prompt = remove_from_promptN
                    else:
                        remove_from_prompt = ""
                else:
                    if use_internal_remove == "Yes":
                        remove_from_prompt = remove_from_promptN + "\n" + remove_from_prompt
                    else:
                        remove_from_prompt = ""

                self.remove_from_prompt = remove_from_prompt
                """

                remove_from_promptN = llama3_pipe.remove_from_prompt

                if remove_from_prompt is None:
                    if use_internal_remove == "Yes":
                        a_remove_from_prompt = remove_from_promptN
                    else:
                        a_remove_from_prompt = ""                
                else:
                    if use_internal_remove == "Yes":
                        a_remove_from_prompt = remove_from_promptN + "\n" + remove_from_prompt
                    else:
                        a_remove_from_prompt = ""

                self.remove_from_prompt = a_remove_from_prompt 

                self.response = clean_prompt_regex(self.response)
                self.response = process_prompt_v2(self.response, self.remove_from_prompt)
                self.response = str(remove_leading_spaces(self.response))
        #else:
        #    if use_custom_prompt == "No": 
        #        self.response = "" 
        #    else:
        #        self.response = custom_prompt 


        return(self.response, llama3_pipe, rf_mix_styles) #self.full_mix_styles
    
    def code_format_prompt(self, user_query, sprompt_text, aprompt_text):
        if self.llama3_pipe is not None:
            template = f"""{self.llama3_pipe.codeA}{self.llama3_pipe.codeB}{self.llama3_pipe.modeA}{self.llama3_pipe.codeC}\n\n{sprompt_text}{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeB}{self.llama3_pipe.codeC}\n\n{user_query}{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}\n\n{aprompt_text}{self.llama3_pipe.codeC}\n\n"""
        else:
            template = ("")

        return template  
    
    def code_format_prompt2(self, user_query=str(""), sprompt_text=str(""), aprompt_text=str("")):
        if self.llama3_pipe is not None:
            template = (
                f"{self.llama3_pipe.codeA}{self.llama3_pipe.codeB}{self.llama3_pipe.modeA}{self.llama3_pipe.codeC}\n\n"
                f"{sprompt_text}"
                f"{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeB}{self.llama3_pipe.codeC}\n\n"
                f"{user_query}"
                f"{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeB}{self.llama3_pipe.codeC}\n\n"
                f"{aprompt_text}{self.llama3_pipe.codeD}{self.llama3_pipe.codeB}{self.llama3_pipe.modeC}\n\n"
            )
        else:
           template = ("")  

        return template

#####################################################################################################################
# DGLlamaSysView ####################################################################################################
#####################################################################################################################   
    
class DGLlamaSysView:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input": (("*",{})),
                "mode": (["raw value", "tensor shape"],),
            },
        }

    @classmethod
    def VALIDATE_INPUTS(cls, input_types):
        return True

    RETURN_TYPES = ()
    RETURN_NAMES = ()
    FUNCTION = "get_sys"
    OUTPUT_NODE = True

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaSysView (Llama 3.1 & 3.2 - OX3D)" 

    def get_sys(self, input, mode):
        if mode == "tensor shape":
            text = []
            #text = str(input)
            def tensorShape(tensor):
                if isinstance(tensor, dict):
                    for k in tensor:
                        tensorShape(tensor[k])
                elif isinstance(tensor, list):
                    for i in range(len(tensor)):
                        tensorShape(tensor[i])
                elif hasattr(tensor, 'shape'):
                    text.append(list(tensor.shape))

            tensorShape(input)
            input = text

        text = str(input)

        return {"ui": {"string": [text,]}, "result": (text,)}
    
#####################################################################################################################
# DGLlamaPromptViewer ###############################################################################################
#####################################################################################################################     
    
class DGLlamaPromptViewer:
  @classmethod
  def INPUT_TYPES(cls): # pylint: disable = invalid-name, missing-function-docstring
    return {
      "required": {
        "source": (SysType, {}),
      },
    }

  RETURN_TYPES = ()
  RETURN_NAMES = ()
  FUNCTION = "fill_viewer"
  OUTPUT_NODE = True

  CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
  TITLE = "DGLlamaPromptViewer (Llama 3.1 & 3.2 - OX3D)"  

  def fill_viewer(self, source=None):
    value = 'None'
    if isinstance(source, str):
      value = source
    elif isinstance(source, (int, float, bool)):
      value = str(source)
    elif source is not None:
      try:
        value = json.dumps(source)
      except Exception:
        try:
          value = str(source)
        except Exception:
          value = 'source exists, but could not be serialized.'
    return {"ui": {"string": [value,]}, "result": (value,)}
  
#####################################################################################################################
# DGLlamaTextPrompt #################################################################################################
#####################################################################################################################   
  
class DGLlamaTextPrompt:
    acc1 = F"""Include in the prompt details about quality, the type of camera or Kodak, angles, perspective, and distance using professional photography terms.\nIf inspired by a known artist, add their name along with any other details needed to reproduce the image.\nDon't attempt to simulate taking a picture; just provide the prompt in text format."""
    acc2 = F"""# You can use this text box for prompt or for agent system:\n# Use case exemple for agent system:\nYou are an agent specialized in creating text prompts for generating anime image, photo, video of all genres and styles.\nAs an expert, you are skilled at inventing original text prompt concepts with inspiration from the works of the greatest anime artists.\nYour expertise allows you to craft text prompts that bring to life vibrant shonen battles, heartwarming slice-of-life moments, or breathtaking fantasy worlds.\nYou excel at capturing the essence of any anime style, making you the perfect guide for designing detailed and visually stunning text prompts.\nDo not use words like Title: or Prompt:\nInstead, when you reply the prompt incorporate the content directly into the sentence as a single paragraph without separation"""
   
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {"default":f"""{cls.acc2}\n{cls.acc1}""", "multiline": True, "dynamicPrompts": True}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("prompt",)
    FUNCTION = "prompt_multiline"

    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaTextPromptAgent (Llama 3.1 & 3.2 - OX3D)" 

    def prompt_multiline(self, prompt):
        import io
        new_text = []
        for line in io.StringIO(prompt):
            if not line.strip().startswith('#'):
                new_text.append(line.replace("\n", ''))
        new_text = "\n".join(new_text)

        return (new_text, )         
    
#####################################################################################################################
# DGLlamaMixStyles ##################################################################################################
#####################################################################################################################  
  
class DGLlamaMixStyles:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "style1": ("STRING", {"default": '', "forceInput": True}),
                "style2": ("STRING", {"default": '', "forceInput": True}),
            }
        }
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("styles",)
    FUNCTION = "mixstyles"
    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaMixStyles (Llama 3.1 & 3.2 - OX3D)" 

    def mixstyles(self, style1, style2):
        mixed_styles = style1 + "\n\n" + style2
        return (mixed_styles, )
    
#####################################################################################################################
# DGLlamaMixStylesMulti #############################################################################################
#####################################################################################################################     
    
class DGLlamaMixStylesMulti:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 1000, "step": 1}),
                "style_1": ("STRING", {"default": '', "forceInput": True}),
                "style_2": ("STRING", {"default": '', "forceInput": True}),
            },
    }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("styles",)
    FUNCTION = "mixstyles"
    CATEGORY = "OrionX3D/PromptGenerator (💫🅞🅧3🅓)"
    TITLE = "DGLlamaMixStylesMulti (Llama 3.1 & 3.2 - OX3D)" 
    DESCRIPTION = """
Mix single Style, or a list of Styles, from  
multiple input Styles.  
You can set how many inputs the node has,  
with the **inputcount** and clicking update.
"""

    def mixstyles(self, inputcount, **kwargs):
        string = kwargs["style_1"]
        for c in range(1, inputcount):
            new_string = kwargs[f"style_{c + 1}"]
            string = string + "\n\n" + new_string
        return (string,)
    
#####################################################################################################################
# Register Class ####################################################################################################
#####################################################################################################################    

NODE_CLASS_MAPPINGS = {
    "DGLoadLlamaModel": DGLoadLlamaModel3_x,
    "DGPromptGenLlama": DGPromptGenLlama3_2,
    "DGLoadDeepSeekModelR1": DGLoadDeepSeekModelR1,
    "DGPromptGenSeepSeekR1": DGPromptGenSeepSeekR1,
    "DGLlamaStyles": DGLlamaStyles,
    "DGLlamaStyleColors": DGLlamaStyleColors,
    "DGLlamaStyleColorExt": DGLlamaStyleColorExt,
    "DGLlamaStyleWeapons": DGLlamaStyleWeapons,
    "DGLlamaStyleVehicles": DGLlamaStyleVehicles,
    "DGLlamaStyleHumanHybrid": DGLlamaStyleHumanHybrid,
    "DGLlamaStyleHairs": DGLlamaStyleHairs,
    "DGLlamaStyleGods": DGLlamaStyleGods,
    "DGLlamaStyleNationalities": DGLlamaStyleNationalities,
    "DGLlamaStyleEstablishmentObjects": DGLlamaStyleEstablishmentObjects,
    "DGLlamaStyleRoomObjects": DGLlamaStyleRoomObjects,
    "DGLlamaStylePositiveWordsSports": DGLlamaStylePositiveWordsSports,
    "DGLlamaStyleWordsSports": DGLlamaStyleWordsSports,
    "DGLlamaStylePositiveSigns": DGLlamaStylePositiveSigns,
    "DGLlamaStylePositiveWords": DGLlamaStylePositiveWords,
    "DGLlamaStyleBadWordsMedias": DGLlamaStyleBadWordsMedias,
    "DGLlamaStyleBadWords": DGLlamaStyleBadWords,
    "DGLlamaStyleDishes": DGLlamaStyleDishes,
    "DGLlamaStyleBeverages": DGLlamaStyleBeverages,
    "DGLlamaStyleDaytimeMoments": DGLlamaStyleDaytimeMoments,
    "DGLlamaStyleEarthElements": DGLlamaStyleEarthElements,
    "DGLlamaStyleRealismStyles": DGLlamaStyleRealismStyles,
    "DGLlamaStyleProduceList": DGLlamaStyleProduceList,
    "DGLlamaStylePhotoVideo": DGLlamaStylePhotoVideo,
    "DGLlamaStyleCats": DGLlamaStyleCats,
    "DGLlamaStyleDogs": DGLlamaStyleDogs,
    "DGLlamaStyleBirds": DGLlamaStyleBirds,
    "DGLlamaStyleDinosaurs": DGLlamaStyleDinosaurs,
    "DGLlamaStyleSupervillains": DGLlamaStyleSupervillains,
    "DGLlamaStyleSuperheroes": DGLlamaStyleSuperheroes,
    "DGLlamaStyleBubbleKeywords": DGLlamaStyleBubbleKeywords,
    "DGLlamaStyleSignKeywords": DGLlamaStyleSignKeywords,
    "DGLlamaStyleBodyPositions": DGLlamaStyleBodyPositions,
    "DGLlamaStyleEmotionGenres": DGLlamaStyleEmotionGenres,
    "DGLlamaStyleCombatScenarios": DGLlamaStyleCombatScenarios,
    "DGLlamaStyleShortVideoScenarios": DGLlamaStyleShortVideoScenarios,
    "DGLlamaStyleClothingBrandsAndStyles": DGLlamaStyleClothingBrandsAndStyles,
    "DGLlamaStyleCamerasAndModes": DGLlamaStyleCamerasAndModes,
    "DGLlamaStylePhotographersAndStyles": DGLlamaStylePhotographersAndStyles,
    "DGLlamaStyleFilmAndSeriesCreators": DGLlamaStyleFilmAndSeriesCreators,
    "DGLlamaStyleArtStyles": DGLlamaStyleArtStyles,
    "DGLlamaStyleArtStyles2": DGLlamaStyleArtStyles2,
    "DGLlamaStyleRenderSystems": DGLlamaStyleRenderSystems,
    "DGLlamaStyleArtGenres": DGLlamaStyleArtGenres,
    "DGLlamaStyleGamingConsoles": DGLlamaStyleGamingConsoles,
    "DGLlamaStyleAlienSpecies": DGLlamaStyleAlienSpecies,
    "DGLlamaStyleNightTimeStyles": DGLlamaStyleNightTimeStyles,
    "DGLlamaStyleDaytimeStyles": DGLlamaStyleDaytimeStyles,
    "DGLlamaStyleWorldReligions": DGLlamaStyleWorldReligions,
    "DGLlamaStyleBiblicalMoments": DGLlamaStyleBiblicalMoments,
    "DGLlamaStyleTimePeriods": DGLlamaStyleTimePeriods,
    "DGLlamaStyleProfessions": DGLlamaStyleProfessions,
    "DGLlamaStyleCombatActions": DGLlamaStyleCombatActions,
    "DGLlamaStyleActionsStyles": DGLlamaStyleActionsStyles,
    "DGLlamaStyleWondersOfTheWorld": DGLlamaStyleWondersOfTheWorld,
    "DGLlamaStyleMonsters": DGLlamaStyleMonsters,
    "DGLlamaStyleCelestialObjects": DGLlamaStyleCelestialObjects,
    "DGLlamaStyleProtectionTypes": DGLlamaStyleProtectionTypes,
    "DGLlamaStyleShieldTypes": DGLlamaStyleShieldTypes,
    "DGLlamaStyleBuildingTypes": DGLlamaStyleBuildingTypes,
    #"DGLlamaUser": DGLlamaUser, # DEPRECATED
    "DGLlamaAgentUserEdit": DGLlamaAgentUserEdit, # DEPRECATED # Temporary enabled for test
    "DGLlamaChatUser": DGLlamaChatUser,
    "DGLlamaAgent": DGLlamaAgent,
    "DGLlamaAgentCorrection": DGLlamaAgentCorrection,
    "DGLlamaAgentTranslate": DGLlamaAgentTranslate,
    "DGLlamaSysView": DGLlamaSysView,
    "DGLlamaPromptViewer": DGLlamaPromptViewer,
    "DGLlamaTextPrompt": DGLlamaTextPrompt,
    "DGLlamaMixStyles": DGLlamaMixStyles,
    "DGLlamaMixStylesMulti": DGLlamaMixStylesMulti,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DGLoadLlamaModel //OrionX3D": "DGLoadLlamaModel (💫🅞🅧3🅓)", 
    "DGPromptGenLlama //OrionX3D": "DGPromptGenLlama (💫🅞🅧3🅓)",  
    "DGLoadDeepSeekModelR1 //OrionX3D": "DGLoadDeepSeekModelR1 (💫🅞🅧3🅓)", 
    "DGPromptGenSeepSeekR1 //OrionX3D": "DGPromptGenSeepSeekR1 (💫🅞🅧3🅓)", 
    "DGLlamaStyles //OrionX3D": "DGLlamaStyles (💫🅞🅧3🅓)", 
    "DGLlamaStyleColors //OrionX3D": "DGLlamaStyleColors (💫🅞🅧3🅓)",
    "DGLlamaStyleColorExt //OrionX3D": "DGLlamaStyleColorExt (💫🅞🅧3🅓)",
    "DGLlamaStyleWeapons //OrionX3D": "DGLlamaStyleWeapons (💫🅞🅧3🅓)",
    "DGLlamaStyleVehicles //OrionX3D": "DGLlamaStyleVehicles (💫🅞🅧3🅓)", 
    "DGLlamaStyleHumanHybrid //OrionX3D": "DGLlamaStyleHumanHybrid (💫🅞🅧3🅓)",
    "DGLlamaStyleHairs //OrionX3D": "DGLlamaStyleHairs (💫🅞🅧3🅓)",
    "DGLlamaStyleGods //OrionX3D": "DGLlamaStyleGods (💫🅞🅧3🅓)",
    "DGLlamaStyleNationalities //OrionX3D": "DGLlamaStyleNationalities (💫🅞🅧3🅓)",
    "DGLlamaStyleEstablishmentObjects //OrionX3D": "DGLlamaStyleEstablishmentObjects (💫🅞🅧3🅓)",
    "DGLlamaStyleRoomObjects //OrionX3D": "DGLlamaStyleRoomObjects (💫🅞🅧3🅓)",
    "DGLlamaStylePositiveWordsSports //OrionX3D": "DGLlamaStylePositiveWordsSports (💫🅞🅧3🅓)",
    "DGLlamaStyleWordsSports //OrionX3D": "DGLlamaStyleWordsSports (💫🅞🅧3🅓)",
    "DGLlamaStylePositiveSigns //OrionX3D": "DGLlamaStylePositiveSigns (💫🅞🅧3🅓)",
    "DGLlamaStylePositiveWords //OrionX3D": "DGLlamaStylePositiveWords (💫🅞🅧3🅓)",
    "DGLlamaStyleBadWordsMedias //OrionX3D": "DGLlamaStyleBadWordsMedias (💫🅞🅧3🅓)",
    "DGLlamaStyleBadWords //OrionX3D": "DGLlamaStyleBadWords (💫🅞🅧3🅓)",
    "DGLlamaStyleDishes //OrionX3D": "DGLlamaStyleDishes (💫🅞🅧3🅓)",
    "DGLlamaStyleBeverages //OrionX3D": "DGLlamaStyleBeverages (💫🅞🅧3🅓)",
    "DGLlamaStyleDayTimeMoments //OrionX3D": "DGLlamaStyleDayTimeMoments (💫🅞🅧3🅓)",
    "DGLlamaStyleEarthElements //OrionX3D": "DGLlamaStyleEarthElements (💫🅞🅧3🅓)",
    "DGLlamaStyleRealismStyles //OrionX3D": "DGLlamaStyleRealismStyles (💫🅞🅧3🅓)",
    "DGLlamaStyleProduceList //OrionX3D": "DGLlamaStyleProduceList (💫🅞🅧3🅓)",
    "DGLlamaStylePhotoVideo //OrionX3D": "DGLlamaStylePhotoVideo (💫🅞🅧3🅓)",
    "DGLlamaStyleCats //OrionX3D": "DGLlamaStyleCats (💫🅞🅧3🅓)",
    "DGLlamaStyleDogs //OrionX3D": "DGLlamaStyleDogs (💫🅞🅧3🅓)",
    "DGLlamaStyleBirds //OrionX3D": "DGLlamaStyleBirds (💫🅞🅧3🅓)",
    "DGLlamaStyleDinosaurs //OrionX3D": "DGLlamaStyleDinosaurs (💫🅞🅧3🅓)",
    "DGLlamaStyleSupervillains //OrionX3D": "DGLlamaStyleSupervillains (💫🅞🅧3🅓)",
    "DGLlamaStyleSuperheroes //OrionX3D": "DGLlamaStyleSuperheroes (💫🅞🅧3🅓)",
    "DGLlamaStyleBubbleKeywords //OrionX3D": "DGLlamaStyleBubbleKeywords (💫🅞🅧3🅓)",
    "DGLlamaStyleSignKeywords //OrionX3D": "DGLlamaStyleSignKeywords (💫🅞🅧3🅓)",
    "DGLlamaStyleBodyPositions //OrionX3D": "DGLlamaStyleBodyPositions (💫🅞🅧3🅓)",
    "DGLlamaStyleEmotionGenres //OrionX3D": "DGLlamaStyleEmotionGenres (💫🅞🅧3🅓)",
    "DGLlamaStyleCombatScenarios //OrionX3D": "DGLlamaStyleCombatScenarios (💫🅞🅧3🅓)",
    "DGLlamaStyleShortVideoScenarios //OrionX3D": "DGLlamaStyleShortVideoScenarios (💫🅞🅧3🅓)",
    "DGLlamaStyleClothingBrandsAndStyles //OrionX3D": "DGLlamaStyleClothingBrandsAndStyles (💫🅞🅧3🅓)",
    "DGLlamaStyleCamerasAndModes //OrionX3D": "DGLlamaStyleCamerasAndModes (💫🅞🅧3🅓)",
    "DGLlamaStylePhotographersAndStyles //OrionX3D": "DGLlamaStylePhotographersAndStyles (💫🅞🅧3🅓)",
    "DGLlamaStyleFilmAndSeriesCreators //OrionX3D": "DGLlamaStyleFilmAndSeriesCreators (💫🅞🅧3🅓)",
    "DGLlamaStyleArtStyles //OrionX3D": "DGLlamaStyleArtStyles (💫🅞🅧3🅓)",
    "DGLlamaStyleArtStyles2 //OrionX3D": "DGLlamaStyleArtStyles2 (💫🅞🅧3🅓)",
    "DGLlamaStyleRenderSystems //OrionX3D": "DGLlamaStyleRenderSystems (💫🅞🅧3🅓)",
    "DGLlamaStyleArtGenres //OrionX3D": "DGLlamaStyleArtGenres (💫🅞🅧3🅓)",
    "DGLlamaStyleGamingConsoles //OrionX3D": "DGLlamaStyleGamingConsoles (💫🅞🅧3🅓)",
    "DGLlamaStyleAlienSpecies //OrionX3D": "DGLlamaStyleAlienSpecies (💫🅞🅧3🅓)",
    "DGLlamaStyleNightTimeStyles //OrionX3D": "DGLlamaStyleNightTimeStyles (💫🅞🅧3🅓)",
    "DGLlamaStyleDaytimeStyles //OrionX3D": "DGLlamaStyleDaytimeStyles (💫🅞🅧3🅓)",
    "DGLlamaStyleWorldReligions //OrionX3D": "DGLlamaStyleWorldReligions (💫🅞🅧3🅓)",
    "DGLlamaStyleBiblicalMoments //OrionX3D": "DGLlamaStyleBiblicalMoments (💫🅞🅧3🅓)",
    "DGLlamaStyleTimePeriods //OrionX3D": "DGLlamaStyleTimePeriods (💫🅞🅧3🅓)",
    "DGLlamaStyleProfessions //OrionX3D": "DGLlamaStyleProfessions (💫🅞🅧3🅓)",
    "DGLlamaStyleCombatActions //OrionX3D": "DGLlamaStyleCombatActions (💫🅞🅧3🅓)",
    "DGLlamaStyleActionsStyles //OrionX3D": "DGLlamaStyleActionsStyles (💫🅞🅧3🅓)",
    "DGLlamaStyleWondersOfTheWorld //OrionX3D": "DGLlamaStyleWondersOfTheWorld (💫🅞🅧3🅓)",
    "DGLlamaStyleMonsters //OrionX3D": "DGLlamaStyleMonsters (💫🅞🅧3🅓)",
    "DGLlamaStyleCelestialObjects //OrionX3D": "DGLlamaStyleCelestialObjects (💫🅞🅧3🅓)",
    "DGLlamaStyleProtectionTypes //OrionX3D": "DGLlamaStyleProtectionTypes (💫🅞🅧3🅓)",
    "DGLlamaStyleShieldTypes //OrionX3D": "DGLlamaStyleShieldTypes (💫🅞🅧3🅓)",
    "DGLlamaStyleBuildingTypes //OrionX3D": "DGLlamaStyleBuildingTypes (💫🅞🅧3🅓)",
    #"DGLlamaUser //OrionX3D": "DGLlamaUser (💫🅞🅧3🅓)", # DEPRECATED
    "DGLlamaAgentUserEdit //OrionX3D": "DGLlamaAgentUserEdit (💫🅞🅧3🅓)", # DEPRECATED # Temporary enabled for test
    "DGLlamaChatUser //OrionX3D": "DGLlamaChatUser (💫🅞🅧3🅓)",
    "DGLlamaAgent //OrionX3D": "DGLlamaAgent (💫🅞🅧3🅓)",
    "DGLlamaAgentCorrection //OrionX3D": "DGLlamaAgentCorrection (💫🅞🅧3🅓)",
    "DGLlamaAgentTranslate //OrionX3D": "DGLlamaAgentTranslate (💫🅞🅧3🅓)",
    "DGLlamaSysView //OrionX3D": "DGLlamaSysView (💫🅞🅧3🅓)",
    "DGLlamaPromptViewer //OrionX3D": "DGLlamaPromptViewer (💫🅞🅧3🅓)",
    "DGLlamaTextPrompt //OrionX3D": "DGLlamaTextPrompt (💫🅞🅧3🅓)",
    "DGLlamaMixStyles //OrionX3D": "DGLlamaMixStyles (💫🅞🅧3🅓)",
    "DGLlamaMixStylesMulti //OrionX3D": "DGLlamaMixStylesMulti (💫🅞🅧3🅓)",    
}