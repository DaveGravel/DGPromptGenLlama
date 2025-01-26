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
import os
import torch
import nodes
import comfy
import comfy.diffusers_load
import comfy.samplers
import comfy.sample
import comfy.sd
import comfy.utils
import comfy.latent_formats
import comfy.model_base
import comfy.model_management
import comfy.model_patcher
import comfy.model_sampling	
from comfy_extras.nodes_upscale_model import ImageUpscaleWithModel
#
import numpy as np
#
# import hashlib
"""
from transformers import T5EncoderModel, T5Tokenizer

from ltx_video.models.autoencoders.causal_video_autoencoder import (
    CausalVideoAutoencoder,
)
from ltx_video.models.transformers.symmetric_patchifier import SymmetricPatchifier
from ltx_video.models.transformers.transformer3d import Transformer3DModel
from ltx_video.pipelines.pipeline_ltx_video import LTXVideoPipeline
from ltx_video.schedulers.rf import RectifiedFlowScheduler
from ltx_video.utils.conditioning_method import ConditioningMethod
from ltx_video.utils.skip_layer_strategy import SkipLayerStrategy

current_directory = os.path.dirname(os.path.abspath(__file__))
device = "cuda" if torch.cuda.is_available() else "cpu"
"""
#
######################################################################################

def NPToTensorNew(image, batch_size=1):
    out = torch.from_numpy(image)
    out = torch.clamp(out.to(torch.float) / 255., 0.0, 1.0)
    out = out[..., [2, 1, 0]]  # Redéfinissez l'ordre des canaux si nécessaire
    out = out.unsqueeze(0)  # Ajoutez la dimension du batch_size
    out = out.expand(batch_size, -1, -1, -1)  # Étendez le batch_size si nécessaire 
    return out

def to_latent_image(pixels, vae):
    x = pixels.shape[1]
    y = pixels.shape[2]
    if pixels.shape[1] != x or pixels.shape[2] != y:
        pixels = pixels[:, :x, :y, :]
    t = vae.encode(pixels[:, :, :, :3])
    return {"samples": t}

def to_latent_image_Tiled(pixels, vae, tile_size):
    x = pixels.shape[1]
    y = pixels.shape[2]
    if pixels.shape[1] != x or pixels.shape[2] != y:
        pixels = pixels[:, :x, :y, :]
    t = vae.encode_tiled(pixels[:, :, :, :3], tile_x=tile_size, tile_y=tile_size)
    return {"samples": t}

def decode_to_images(latent, vae):
    decoded_image = vae.decode(latent["samples"],)  
    return decoded_image  

def decodeltx(vae, latent_image):
    images = vae.decode(latent_image["samples"])
    if len(images.shape) == 5: #Combine batches
        images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])
    return (images, )

def decodeltx_tiled(vae, latent_image, tile_size, overlap=64, temporal_size=64, temporal_overlap=8):
    if tile_size < overlap * 4:
        overlap = tile_size // 4
    if temporal_size < temporal_overlap * 2:
        temporal_overlap = temporal_overlap // 2
    temporal_compression = vae.temporal_compression_decode()
    if temporal_compression is not None:
        temporal_size = max(2, temporal_size // temporal_compression)
        temporal_overlap = min(1, temporal_size // 2, temporal_overlap // temporal_compression)
    else:
        temporal_size = None
        temporal_overlap = None

    compression = vae.spacial_compression_decode()
    images = vae.decode_tiled(latent_image["samples"], tile_x=tile_size // compression, tile_y=tile_size // compression, overlap=overlap // compression, tile_t=temporal_size, overlap_t=temporal_overlap)
    if len(images.shape) == 5: #Combine batches
        images = images.reshape(-1, images.shape[-3], images.shape[-2], images.shape[-1])
    return (images, )    

def encodeltx(vae, images):
    # Extraire les images si elles sont dans un tuple
    if isinstance(images, tuple):
        images = images[0]
    
    # Vérifier si c'est bien un tensor
    if not hasattr(images, "shape"):
        raise ValueError(f"Expected a tensor or array-like object, but got {type(images)}")
    
    # Encoder les images
    latents = vae.encode(images)
    print(f"Encoded latents: {latents}")
    
    # Vérifier si la clé "samples" existe et sa structure
    if "samples" not in latents:
        raise KeyError(f"'samples' key not found in latents. Available keys: {latents.keys()}")
    
    print(f"Latents shape: {latents['samples'].shape}")
    
    # Reshape si nécessaire
    if len(latents["samples"].shape) == 4:
        latents["samples"] = latents["samples"].reshape(-1, *latents["samples"].shape[1:])
    
    return latents

def image2nparrayA(image, BGR=False):
    nparray = np.clip(255. * image.cpu().numpy().squeeze(), 0, 255).astype(np.uint8)
    if BGR:
        nparray = nparray[:, :, ::-1]  # Convertir de RGB à BGR si nécessaire
    return nparray

def NPToTensorNew2(image, batch_size=1):
    out = torch.from_numpy(image)
    out = torch.clamp(out.to(torch.float) / 255., 0.0, 1.0)
    # L'ordre des canaux est déjà correct en RGB, donc pas besoin de réarranger
    out = out.unsqueeze(0)  # Ajoutez la dimension du batch_size
    out = out.expand(batch_size, -1, -1, -1)  # Étendez le batch_size si nécessaire 
    return out

def colormatch(image_ref, image_target, method, strength=1.0):
    try:
        from color_matcher import ColorMatcher
    except:
        raise Exception("Can't import color-matcher, did you install requirements.txt? Manual install: pip install color-matcher")
    cm = ColorMatcher()
    image_ref = image_ref.cpu()
    image_target = image_target.cpu()
    batch_size = image_target.size(0)
    out = []
    images_target = image_target.squeeze()
    images_ref = image_ref.squeeze()

    image_ref_np = images_ref.numpy()
    images_target_np = images_target.numpy()

    if image_ref.size(0) > 1 and image_ref.size(0) != batch_size:
        raise ValueError("ColorMatch: Use either single reference image or a matching batch of reference images.")

    for i in range(batch_size):
        image_target_np = images_target_np if batch_size == 1 else images_target[i].numpy()
        image_ref_np_i = image_ref_np if image_ref.size(0) == 1 else images_ref[i].numpy()
        try:
            image_result = cm.transfer(src=image_target_np, ref=image_ref_np_i, method=method)
        except BaseException as e:
            print(f"Error occurred during transfer: {e}")
            break
        # Apply the strength multiplier
        image_result = image_target_np + strength * (image_result - image_target_np)
        out.append(torch.from_numpy(image_result))
            
    out = torch.stack(out, dim=0).to(torch.float32)
    out.clamp_(0, 1)

    #return (out,) 
    return out  

class KSamplersSettingsLTX_ox3d:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": 
                    {"sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                     "scheduler": (comfy.samplers.KSampler.SCHEDULERS,)
                    }
                }

    RETURN_TYPES = (comfy.samplers.KSampler.SAMPLERS, comfy.samplers.KSampler.SCHEDULERS,)
    RETURN_NAMES = ("sampler_name", "scheduler",)
    FUNCTION = "get_samplernames"
    CATEGORY = "OrionX3D/LTX_Samplers (💫🅞🅧3🅓)"                

    def get_samplernames(self, sampler_name, scheduler):
        return (sampler_name, scheduler, )

class KSamplersSettingsAdvLTX_ox3d:
    @classmethod
    def INPUT_TYPES(cls):
        return {"required": 
                    {"sampler_name": (comfy.samplers.KSampler.SAMPLERS,),
                     "scheduler": (comfy.samplers.KSampler.SCHEDULERS,)
                    }
                }

    RETURN_TYPES = (comfy.samplers.KSampler.SAMPLERS, comfy.samplers.KSampler.SCHEDULERS,)
    RETURN_NAMES = ("sampler_name", "scheduler",)
    FUNCTION = "get_samplernames"
    CATEGORY = "OrionX3D/LTX_Samplers (💫🅞🅧3🅓)"                

    def get_samplernames(self, sampler_name, scheduler):
        return (sampler_name, scheduler, )        

class KSamplerLTX_ox3d:
    def __init__(self):
        self.ltx_latent = None
        self.ltx_newlatent = None
        self.result = None
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"ltx_model": ("MODEL",),
                     "vae": ("VAE",),  
                     "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                     "steps": ("INT", {"default": 10, "min": 1, "max": 10000}),
                     "cfg": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 100.0}),
                     "sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"default": "euler_ancestral"}),
                     "positive": ("CONDITIONING", ),
                     "negative": ("CONDITIONING", ),
                     "latent_image": ("LATENT", ),
                     "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                     "refiner_cfg": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 100.0}),
                     "refiner_steps": ("INT", {"default": 10, "min": 1, "max": 10000}),
                     "refiner_count": ("INT", {"default": 0, "min": 0, "max": 10000}),
                     "usetiled": (["Yes", "No"],),                 
                     "tile_size": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 32}),
                     "overlap": ("INT", {"default": 64, "min": 0, "max": 4096, "step": 32}),
                     "temporal_size": ("INT", {"default": 64, "min": 8, "max": 4096, "step": 4, "tooltip": "Only used for video VAEs: Amount of frames to decode at a time."}),
                     "temporal_overlap": ("INT", {"default": 8, "min": 4, "max": 4096, "step": 4, "tooltip": "Only used for video VAEs: Amount of frames to overlap."}),
#                     "auto_reset_cache": ("BOOLEAN", {"default": True, "label_on": "Enable", "label_off": "Disable"}),
                     }
                #,
                #"optional":
                #    {
                #        "optional_scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"tooltip": "optional don't use this option if you like to use OX3DKSamplerLTX node and the refiner mode."}),
                #    }
                }      
                      
    RETURN_TYPES = ("LATENT", "LATENT", "CONDITIONING", "CONDITIONING", "IMAGE", "IMAGE", "VAE", "MODEL", "IMAGE")
    RETURN_NAMES = ("latent_out", "latent_start", "positive_prompt", "negative_prompt", "video_image_out", "last_image_out", "vae_out", "ltx_model_out", "first_image_out")
    FUNCTION = "sample"

    CATEGORY = "OrionX3D/LTX_Samplers (💫🅞🅧3🅓)"
#auto_reset_cache
    def sample(self, ltx_model, vae, seed, steps, cfg, sampler_name, positive, negative, latent_image, denoise, refiner_cfg, refiner_steps, refiner_count, usetiled, tile_size, overlap, temporal_size, temporal_overlap):
        video_images = None
        last_image = None
        self.result = None
        a_scheduler = None

        #self.result = latent_image
        self.ltx_latent = latent_image

        #if auto_reset_cache == True:
        #    self.ltx_newlatent = None
        #    self.ltx_latent = None
        a_scheduler = "ddim_uniform"
        #if self.ltx_newlatent is not None:
        #    self.ltx_latent = self.ltx_newlatent
        #    self.result = self.ltx_newlatent       
        result = nodes.common_ksampler(
            ltx_model, seed, steps, cfg, sampler_name, a_scheduler,
            positive, negative, self.ltx_latent, denoise=denoise
        )
        #if self.ltx_latent is None:
        #    self.ltx_latent = latent_image              
            #new_latent = self.ltx_latent    
            #optional_scheduler
            #if optional_scheduler is not None:
            #    a_scheduler = optional_scheduler
            #else:
        #    a_scheduler = "ddim_uniform"
            # Exécution du sampler initial
        #    self.result = nodes.common_ksampler(
        #        ltx_model, seed, steps, cfg, sampler_name, a_scheduler,
        #        positive, negative, self.ltx_latent, denoise=denoise
        #    )
        #    self.ltx_newlatent = self.result
        self.ltx_latent = result
        #self.ltx_latent = self.result 

        # Boucle pour les étapes de raffinement
        if refiner_count > 0:
            for i in range(refiner_count):
                #if self.ltx_newlatent is not None:
                #    self.result = nodes.common_ksampler(
                #        ltx_model, seed, refiner_steps, refiner_cfg, sampler_name, a_scheduler,
                #        positive, negative, self.ltx_newlatent[0], denoise=denoise
                #    )
                #    self.ltx_latent = self.result
                #else:
                self.result = nodes.common_ksampler(
                    ltx_model, seed, refiner_steps, refiner_cfg, sampler_name, a_scheduler,
                    positive, negative, self.ltx_latent[0], denoise=denoise
                )
                self.ltx_latent = self.result                    
        # Décodage des images vidéo
        if usetiled == "No":
            video_images = decodeltx(vae, self.ltx_latent[0])
        else:
            video_images = decodeltx_tiled(vae, self.ltx_latent[0], tile_size, overlap, temporal_size, temporal_overlap)

        """
        if refiner_count > 0:
            if usetiled == "No":
                video_images = decodeltx(vae, self.ltx_latent[0])
            else:
                video_images = decodeltx_tiled(vae, self.ltx_latent[0], tile_size, overlap, temporal_size, temporal_overlap)
        else:
            # Décodage des images vidéo
            if usetiled == "No":
                video_images = decodeltx(vae, self.ltx_latent[0])
            else:
                video_images = decodeltx_tiled(vae, self.ltx_latent[0], tile_size, overlap, temporal_size, temporal_overlap)
        """

        last_image = video_images[0][-1]

        processed_last_image = last_image.unsqueeze(0)

        first_image = video_images[0][0]
        processed_first_image = first_image.unsqueeze(0)

        # Retourne les données nécessaires
        return (self.ltx_latent[0], latent_image, positive, negative, video_images[0], processed_last_image, vae, ltx_model, processed_first_image)   

class KSamplerAdvLTX_ox3d:
    #upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "bislerp"]
    rescale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]

    def __init__(self):
        self.ltx_latent = None
        self.ltx_newlatent = None 
        self.__imageScaler = ImageUpscaleWithModel()    

    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"ltx_model": ("MODEL",),
                     "vae": ("VAE",),  
                     "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                     "steps": ("INT", {"default": 10, "min": 1, "max": 10000}),
                     "cfg": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 100.0}),
                     "sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"default": "euler"}),
                     "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"default": "normal"}),
                     "positive": ("CONDITIONING", ),
                     "negative": ("CONDITIONING", ),
                     "latent_image": ("LATENT", ),
                     "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                     "refiner_positive": ("CONDITIONING", ),
                     "refiner_negative": ("CONDITIONING", ),                     
                     "refiner_sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"default": "euler"}),
                     "refiner_scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"default": "sgm_uniform"}),                     
                     "refiner_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                     "refiner_cfg": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 100.0}),
                     "refiner_steps": ("INT", {"default": 10, "min": 1, "max": 10000}),
                     "refiner_count": ("INT", {"default": 0, "min": 0, "max": 10000}),
                     "use_refiner_upscale": (["No", "Yes"],), 
                     #"refiner_upscale_method": (cls.upscale_methods,),
                     "refiner_rescale_method": (cls.rescale_methods,),
                     "refiner_scale_by": ("FLOAT", {"default": 1.5, "min": 0.01, "max": 8.0, "step": 0.01}),
                     "refiner_denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                     "refiner_vae": ("VAE",),  
                     "usetiled": (["Yes", "No"],),                 
                     "tile_size": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 32}),
                     "overlap": ("INT", {"default": 64, "min": 0, "max": 4096, "step": 32}),
                     "temporal_size": ("INT", {"default": 64, "min": 8, "max": 4096, "step": 4, "tooltip": "Only used for video VAEs: Amount of frames to decode at a time."}),
                     "temporal_overlap": ("INT", {"default": 8, "min": 4, "max": 4096, "step": 4, "tooltip": "Only used for video VAEs: Amount of frames to overlap."}),
                     #"auto_reset_cache": (["Yes", "No"],),
                     "fix_color_strength": ("FLOAT", {"default": 1.2, "min": 0.0, "max": 10.0, "step": 0.01}),
                     "fix_color_method": (
                     [   
                         'mkl',
                         'hm', 
                         'reinhard', 
                         'mvgd', 
                         'hm-mvgd-hm', 
                         'hm-mkl-hm',
                     ], {
                        "default": 'mkl'
                     }),                     
                     "fix_color": ("BOOLEAN", {"default": True, "label_on": "Enable", "label_off": "Disable"}),
                     "auto_reset_cache": ("BOOLEAN", {"default": True, "label_on": "Enable", "label_off": "Disable"}),
                     },
                     "optional": {
                         "refiner_model": ("MODEL", {"forceInput": True}),
                         "upscale_model": ("UPSCALE_MODEL", {"forceInput": True}),
                    }
                } 
                 
    RETURN_TYPES = ("LATENT", "LATENT", "CONDITIONING", "CONDITIONING", "CONDITIONING", "CONDITIONING", "IMAGE", "IMAGE", "VAE", "MODEL", "IMAGE", "VAE", "MODEL", "IMAGE")
    RETURN_NAMES = ("latent_out", "latent_start", "positive_prompt", "negative_prompt", "ref_positive_prompt", "ref_negative_prompt", "video_image_out", "last_image_out", "vae_out", "ltx_model_out", "first_image_out", "vae_refiner_out", "ref_model_out", "first_pass_img")
    FUNCTION = "sample"

    CATEGORY = "OrionX3D/LTX_Samplers (💫🅞🅧3🅓)"

    def sample(self, ltx_model, vae, refiner_vae, seed, steps, cfg, sampler_name, scheduler, refiner_sampler_name, refiner_scheduler, refiner_scale_by, use_refiner_upscale, positive, negative, refiner_positive, refiner_negative, latent_image, denoise, refiner_denoise, refiner_seed, refiner_cfg, refiner_steps, refiner_count, usetiled, tile_size, overlap, temporal_size, temporal_overlap, auto_reset_cache, refiner_rescale_method, fix_color, fix_color_method, fix_color_strength, refiner_model = None, upscale_model = None):
        video_images = None
        last_image = None
        new_latent = None

        # charger le result maintenant.
        result = latent_image

        # si le cache est a yes cela replace le cache a None ce qui donne un reset
        if auto_reset_cache == True:
            self.ltx_newlatent = None
            self.ltx_latent = None

        # si le cache de la premiere pass n'est pas none cela veut dire qu'il est assigner deja.
        # Alors on utilise le cache pour loader la latent en current latent. 
        if self.ltx_newlatent is not None:
            self.ltx_latent = self.ltx_newlatent
            result = self.ltx_newlatent

        if self.ltx_latent is None:
            self.ltx_latent = latent_image

            # Exécution du sampler initial
            result = nodes.common_ksampler(
                ltx_model, seed, steps, cfg, sampler_name, scheduler,
                positive, negative, self.ltx_latent, denoise=denoise
            )
            self.ltx_newlatent = result

        self.ltx_latent = result  

        # Debugging step to see the type and contents of ltx_latent
        #print(f"self.ltx_latent type: {type(self.ltx_latent)}")
        #print(f"self.ltx_latent content: {self.ltx_latent}")

        # Safe check before accessing the latent data
        if isinstance(self.ltx_latent, (list, tuple)) and len(self.ltx_latent) > 0:
            f_video_images = decodeltx(vae, self.ltx_latent[0])  # Accessing first item safely
        else:
            raise TypeError("self.ltx_latent is not a valid list or tuple or is empty.")
        #f_video_images = decodeltx(vae, self.ltx_latent[0])  # maybe need a better logic here need to test more.
        #elif isinstance(self.ltx_latent, (list, tuple)):
        #    f_video_images = decodeltx(vae, self.ltx_latent)
        #else:
        #    raise TypeError("self.ltx_latent must be a dictionary, list, or tuple.")

        new_image = f_video_images
        
        rmodel = ltx_model
        if refiner_model is not None:
            rmodel = refiner_model
            #self.ltx_upscalelatent
            # Boucle pour les étapes de raffinement
            if refiner_count > 0:
                new_latent = self.ltx_latent
                #         
                #if use_refiner_upscale == "Yes":
                #video_images = decodeltx(vae, new_latent[0])

                if upscale_model is not None and use_refiner_upscale == "Yes":
                    new_image = self.upscale2(upscale_model, f_video_images[0], refiner_scale_by, refiner_rescale_method)

                ref_latent = image2nparrayA(new_image[0]) #encodeltx(refiner_vae, video_images)  
                aref_image = NPToTensorNew2(ref_latent)  
                latentimg = to_latent_image(aref_image, refiner_vae)  
                #
                new_latent = latentimg

                new_latent = self.latentsamples(new_latent)
                #new_latent = self.upscale(new_latent, refiner_upscale_method, 1.0)
                #else:
                #    ref_latent = image2nparrayA(video_images[0]) #encodeltx(refiner_vae, video_images)  
                #    aref_image = NPToTensorNew2(ref_latent)  
                #    latentimg = to_latent_image(aref_image, refiner_vae)  
                    #
                #    new_latent = latentimg
                    #
                #    if use_refiner_upscale == "Yes":
                #        new_latent = self.upscale(new_latent, refiner_upscale_method, refiner_scale_by)
                #    else:
                #        new_latent = self.upscale(new_latent, refiner_upscale_method, 1.0)

                for i in range(refiner_count):
                    result = nodes.common_ksampler(
                        rmodel, refiner_seed, refiner_steps, refiner_cfg, refiner_sampler_name, refiner_scheduler,
                        refiner_positive, refiner_negative, new_latent[0], denoise=refiner_denoise
                    ) 
                    new_latent = result

        if new_latent is None:
            new_latent = self.ltx_latent 

        # Décodage des images vidéo
        if refiner_count > 0:
            if usetiled == "No":
                video_images = decodeltx(refiner_vae, new_latent[0])
            else:
                video_images = decodeltx_tiled(refiner_vae, new_latent[0], tile_size, overlap, temporal_size, temporal_overlap)
        else:
            # Décodage des images vidéo
            if usetiled == "No":
                video_images = decodeltx(vae, new_latent[0])
            else:
                video_images = decodeltx_tiled(vae, new_latent[0], tile_size, overlap, temporal_size, temporal_overlap)

        last_image = video_images[0][-1]
        processed_last_image = last_image.unsqueeze(0)

        first_image = video_images[0][0]
        processed_first_image = first_image.unsqueeze(0)

        f_image = f_video_images[0][0]
        processed_f_image = f_image.unsqueeze(0)

        if refiner_count > 0 and fix_color == True:
           processed_first_image = colormatch(processed_f_image, processed_first_image, fix_color_method, fix_color_strength)
           video_images = colormatch(processed_f_image, video_images[0], fix_color_method, fix_color_strength)
        # Retourne les données nécessaires
        return (new_latent[0], latent_image, positive, negative, refiner_positive, refiner_negative, video_images[0], processed_last_image, vae, ltx_model, processed_first_image, refiner_vae, refiner_model, processed_f_image)  

    def latentsamples(self, samples):
        s = samples.copy()
        s["samples"] = samples["samples"]
        return (s,)

    def upscale(self, samples, upscale_method, scale_by):
        s = samples.copy()
        width = round(samples["samples"].shape[-1] * scale_by)
        height = round(samples["samples"].shape[-2] * scale_by)
        s["samples"] = comfy.utils.common_upscale(samples["samples"], width, height, upscale_method, "disabled")
        return (s,)

    def upscale2(self, upscale_model, image, upscale_by, rescale_method):
        samples = image.movedim(-1,1)

        width = round(samples.shape[3])
        height = round(samples.shape[2])

        target_width = round(samples.shape[3] * upscale_by)
        target_height = round(samples.shape[2] * upscale_by)

        samples = self.__imageScaler.upscale(upscale_model, image)[0].movedim(-1,1)

        upscaled_width = round(samples.shape[3])
        upscaled_height = round(samples.shape[2])

        if upscaled_width > target_width or upscaled_height > target_height:
            samples = comfy.utils.common_upscale(samples, target_width, target_height, rescale_method, "disabled")
            
        samples = samples.movedim(1,-1)
        return (samples,)


class KSamplerMoreAdvLTX_ox3d:
    def __init__(self):
        self.ltx_latent = None
    @classmethod
    def INPUT_TYPES(cls):
        return {"required":
                    {"ltx_model": ("MODEL",),
                     "vae": ("VAE",),  
                     "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                     "steps": ("INT", {"default": 10, "min": 1, "max": 10000}),
                     "cfg": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 100.0}),
                     "sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"default": "euler"}),
                     "scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"default": "normal"}),
                     "positive": ("CONDITIONING", ),
                     "negative": ("CONDITIONING", ),
                     "latent_image": ("LATENT", ),
                     "denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                     "refiner_positive": ("CONDITIONING", ),
                     "refiner_negative": ("CONDITIONING", ),         
                     "refiner_denoise": ("FLOAT", {"default": 1.0, "min": 0.0, "max": 1.0, "step": 0.01}),
                     "refiner_seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff}),
                     "refiner_cfg": ("FLOAT", {"default": 5.0, "min": 0.0, "max": 100.0}),
                     "refiner_steps": ("INT", {"default": 10, "min": 1, "max": 10000}),
                     "refiner_count": ("INT", {"default": 0, "min": 0, "max": 10000}),
                     "refiner_sampler_name": (comfy.samplers.KSampler.SAMPLERS, {"default": "euler"}),
                     "refiner_scheduler": (comfy.samplers.KSampler.SCHEDULERS, {"default": "sgm_uniform"}),            
                     "refiner_vae": ("VAE",),  
                     "usetiled": (["Yes", "No"],),                 
                     "tile_size": ("INT", {"default": 512, "min": 64, "max": 4096, "step": 32}),
                     "overlap": ("INT", {"default": 64, "min": 0, "max": 4096, "step": 32}),
                     "temporal_size": ("INT", {"default": 64, "min": 8, "max": 4096, "step": 4, "tooltip": "Only used for video VAEs: Amount of frames to decode at a time."}),
                     "temporal_overlap": ("INT", {"default": 8, "min": 4, "max": 4096, "step": 4, "tooltip": "Only used for video VAEs: Amount of frames to overlap."}),
                     }
                }      
                      
    RETURN_TYPES = ("LATENT", "LATENT", "CONDITIONING", "CONDITIONING", "CONDITIONING", "CONDITIONING", "IMAGE", "IMAGE", "VAE", "MODEL", "IMAGE", "VAE")
    RETURN_NAMES = ("latent_out", "latent_start", "positive_prompt", "negative_prompt", "ref_positive_prompt", "ref_negative_prompt", "video_image_out", "last_image_out", "vae_out", "ltx_model_out", "first_image_out", "vae_refiner_out")
    FUNCTION = "sample"

    CATEGORY = "OrionX3D/LTX_Samplers (💫🅞🅧3🅓)"

    def sample(self, ltx_model, vae, refiner_vae, seed, steps, cfg, sampler_name, scheduler, positive, negative, latent_image, denoise, refiner_positive, refiner_negative, refiner_denoise, refiner_seed, refiner_cfg, refiner_steps, refiner_count, refiner_sampler_name, refiner_scheduler, usetiled, tile_size, overlap, temporal_size, temporal_overlap):
        video_images = None
        last_image = None
        result = None
        self.ltx_latent = latent_image

        # Exécution du sampler initial
        result = nodes.common_ksampler(
            ltx_model, seed, steps, cfg, sampler_name, scheduler,
            positive, negative, self.ltx_latent, denoise=denoise
        )

        self.ltx_latent = result

        # Boucle pour les étapes de raffinement
        if refiner_count > 0:
            for i in range(refiner_count):
                result = nodes.common_ksampler(
                    ltx_model, refiner_seed, refiner_steps, refiner_cfg, refiner_sampler_name, refiner_scheduler,
                    refiner_positive, refiner_negative, self.ltx_latent[0], denoise=refiner_denoise
                )
                self.ltx_latent = result

        if refiner_count > 0:
            if usetiled == "No":
                video_images = decodeltx(refiner_vae, self.ltx_latent[0])
            else:
                video_images = decodeltx_tiled(refiner_vae, self.ltx_latent[0], tile_size, overlap, temporal_size, temporal_overlap)
        else:
            # Décodage des images vidéo
            if usetiled == "No":
                video_images = decodeltx(vae, self.ltx_latent[0])
            else:
                video_images = decodeltx_tiled(vae, self.ltx_latent[0], tile_size, overlap, temporal_size, temporal_overlap)

        last_image = video_images[0][-1]

        processed_last_image = last_image.unsqueeze(0)

        first_image = video_images[0][0]
        processed_first_image = first_image.unsqueeze(0)

        # Retourne les données nécessaires
        return (self.ltx_latent[0], latent_image, positive, negative, refiner_positive, refiner_negative, video_images[0], processed_last_image, vae, ltx_model, processed_first_image, refiner_vae)  


NODE_CLASS_MAPPINGS = {
    "OX3DKSamplerLTX": KSamplerLTX_ox3d,
    "OX3DKSamplerAdv": KSamplerAdvLTX_ox3d,
    "OX3DKSamplerMoreAdv": KSamplerMoreAdvLTX_ox3d,
    "OX3DKSamplersSettingsLTX": KSamplersSettingsLTX_ox3d,
    "OX3DKSamplersSettingsAdvLTX": KSamplersSettingsAdvLTX_ox3d,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OX3DKSamplerLTX //OrionX3D": "OX3DKSamplerLTX (💫🅞🅧3🅓)",   
    "OX3DKSamplerAdv //OrionX3D": "OX3DKSamplerAdv (💫🅞🅧3🅓)", # renamed for now, currently untested with LTX model 
    "OX3DKSamplerMoreAdv //OrionX3D": "OX3DKSamplerMoreAdv (💫🅞🅧3🅓)", # renamed for now, currently untested with LTX model 
    "OX3DKSamplersSettingsLTX //OrionX3D": "OX3DKSamplersSettingsLTX (💫🅞🅧3🅓)", 
    "OX3DKSamplersSettingsAdvLTX //OrionX3D": "OX3DKSamplersSettingsAdvLTX (💫🅞🅧3🅓)", 
}