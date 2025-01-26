
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
import socket
import re
import string
import random
import time
from .cache import cleanGPUUsedForce, remove_cache, update_cache
import folder_paths
#from folder_paths import base_path
from folder_paths import get_filename_list
# Dave Gravel - This is temporary
# Later I can surely split all styles by section and save it in a file
# On this way the user can add or delete style.
# Currently it is not possible to add more or remove style, or you need to modify the code here...
building_types = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Cabin", "keywords": ["rustic", "wooden", "forest retreat", "small", "cozy", "traditional", "handmade", "simple design", "nature", "off-grid"]},
    {"genre": "Cottage", "keywords": ["country home", "charming", "quaint", "garden", "rural", "cozy", "small-scale", "stone walls", "traditional", "picturesque"]},
    {"genre": "Log Cabin", "keywords": ["wooden structure", "forest", "nature", "simple design", "handcrafted", "rustic", "outdoor living", "self-sufficient", "warm", "traditional"]},
    {"genre": "Tiny House", "keywords": ["compact", "minimalist", "modern design", "eco-friendly", "mobile", "affordable", "smart storage", "efficient", "portable", "off-grid"]},
    {"genre": "Treehouse", "keywords": ["elevated", "nature", "playful", "unique", "wooden", "forest", "adventurous", "cozy", "off-ground", "custom design"]},
    {"genre": "Beach House", "keywords": ["coastal", "oceanfront", "relaxing", "modern", "vacation", "airy", "water view", "sunlit", "tropical", "luxurious"]},
    {"genre": "Farmhouse", "keywords": ["rural", "agriculture", "rustic charm", "traditional", "large", "family-oriented", "porch", "country living", "stone or wood", "cozy"]},
    {"genre": "Modern Villa", "keywords": ["luxurious", "spacious", "modern architecture", "large windows", "pool", "open-plan", "minimalist", "high-tech", "urban", "stylish"]},
    {"genre": "Skyscraper", "keywords": ["urban", "modern", "high-rise", "business", "glass and steel", "large scale", "luxury apartments", "office building", "innovative", "cityscape"]},
    {"genre": "Bungalow", "keywords": ["single-story", "compact", "traditional", "cozy", "porch", "rural", "family-oriented", "garden", "affordable", "simple design"]},
    {"genre": "Igloo", "keywords": ["Arctic", "snow", "ice house", "cold climate", "traditional", "insulated", "unique", "small", "circular", "temporary"]},
    {"genre": "Yurt", "keywords": ["nomadic", "Mongolian", "circular", "portable", "simple", "cozy", "tent-like", "eco-friendly", "wooden frame", "traditional"]},
    {"genre": "A-Frame House", "keywords": ["triangular design", "modern", "vacation home", "efficient", "compact", "rustic", "cozy", "nature", "unique", "slanted roof"]},
    {"genre": "Castle", "keywords": ["medieval", "stone walls", "historic", "fortress", "grand", "towers", "luxurious", "royalty", "ornate", "heritage"]},
    {"genre": "Apartment Complex", "keywords": ["urban", "multi-family", "modern", "convenient", "compact living", "shared amenities", "affordable", "high-rise", "city life", "community"]},
    {"genre": "Mobile Home", "keywords": ["portable", "compact", "affordable", "self-contained", "eco-friendly", "efficient", "modern design", "trailer park", "simple", "family"]},
    {"genre": "Tent", "keywords": ["camping", "portable", "outdoor", "temporary", "lightweight", "simple", "eco-friendly", "fabric", "adventure", "easy setup"]},
    {"genre": "Ranch House", "keywords": ["rural", "large", "spacious", "family-oriented", "flat design", "traditional", "porch", "cattle farm", "rustic", "nature"]},
    {"genre": "Penthouse", "keywords": ["luxurious", "high-rise", "urban", "modern", "city view", "spacious", "exclusive", "private terrace", "stylish", "expensive"]},
    {"genre": "Shipping Container Home", "keywords": ["modern", "recycled", "eco-friendly", "compact", "industrial design", "affordable", "modular", "innovative", "urban", "portable"]},
    {"genre": "Geodesic Dome", "keywords": ["futuristic", "eco-friendly", "spherical", "strong structure", "modern design", "unique", "lightweight", "efficient", "nature", "innovative"]},
    {"genre": "Earthship", "keywords": ["self-sufficient", "eco-friendly", "sustainable", "off-grid", "natural materials", "solar power", "modern design", "recycled materials", "unique", "efficient"]},
    {"genre": "Mansion", "keywords": ["luxurious", "grand", "spacious", "expensive", "modern design", "heritage", "exclusive", "high-class", "urban", "stylish"]},
    {"genre": "Underground Bunker", "keywords": ["survival", "hidden", "secure", "off-grid", "eco-friendly", "unique", "reinforced", "disaster-proof", "military-grade", "efficient"]},
    {"genre": "Floating House", "keywords": ["waterfront", "unique", "modern design", "compact", "eco-friendly", "lightweight", "vacation", "nature", "innovative", "sustainable"]},
    {"genre": "School Building", "keywords": ["educational", "multi-purpose", "urban", "community", "modern", "functional", "spacious", "shared use", "durable", "affordable"]},
    {"genre": "Lighthouse", "keywords": ["coastal", "unique", "historic", "guiding light", "stone structure", "tall", "oceanfront", "functional", "nautical", "picturesque"]},
    {"genre": "Chalet", "keywords": ["mountain retreat", "wooden", "cozy", "rustic", "vacation", "nature", "alpine style", "family-oriented", "relaxing", "warm"]},
    {"genre": "Dome Tent", "keywords": ["modern camping", "lightweight", "portable", "unique", "temporary", "eco-friendly", "compact", "nature", "easy setup", "adventure"]},
]

weapon_types = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Hunting Knife", "keywords": ["bladed weapon", "hunting", "survival", "outdoor use", "handmade", "sharp", "self-defense", "long blade", "durable", "illegal modification"]},
    {"genre": "Machete", "keywords": ["large blade", "chopping", "close combat", "improvised", "street weapon", "bladed weapon", "self-defense", "dangerous", "jungle survival", "rebellion"]},
    {"genre": "Combat Knife", "keywords": ["military style", "close combat", "self-defense", "reliable", "sharp", "fixed blade", "illegal weapon", "urban warfare", "dangerous", "tactical"]},
    {"genre": "Switchblade", "keywords": ["spring-loaded", "self-defense", "quick access", "illegal weapon", "street weapon", "pocket knife", "bladed weapon", "rapid deployment", "dangerous", "urban combat"]},
    {"genre": "Bowie Knife", "keywords": ["large blade", "tactical", "outdoor survival", "combat", "self-defense", "rebellion", "handmade", "illegal", "sharp", "fixed blade"]},
    {"genre": "Throwing Knife", "keywords": ["throwable weapon", "precision", "bladed weapon", "combat training", "self-defense", "reliable", "silent", "urban warfare", "dangerous", "handmade"]},
    {"genre": "Dagger", "keywords": ["short blade", "close combat", "self-defense", "tactical", "fixed blade", "stealth", "street weapon", "quick strike", "dangerous", "illegal weapon"]},
    {"genre": "Shiv", "keywords": ["homemade knife", "improvised", "street weapon", "close combat", "illegal weapon", "dangerous", "prison-made", "makeshift", "small blade", "self-defense"]},
    {"genre": "Karambit", "keywords": ["curved blade", "self-defense", "combat knife", "street weapon", "bladed weapon", "close combat", "illegal", "dangerous", "handmade", "tactical"]},
    {"genre": "Fixed Blade Knife", "keywords": ["durable", "self-defense", "combat", "hunting", "sharp", "long blade", "illegal weapon", "rebellion", "survival", "urban combat"]},
    {"genre": "Sword", "keywords": ["sharp blade", "ancient weapon", "combat", "long sword", "katana", "double-edged", "tactical blade", "medieval sword", "honor", "warrior"]},
    {"genre": "Bow", "keywords": ["longbow", "archery", "quiver", "arrows", "precision", "range", "silent weapon", "hunter", "string tension", "wooden bow"]},
    {"genre": "Gun", "keywords": ["firearm", "handgun", "revolver", "semi-automatic", "shotgun", "rifle", "pistol", "suppressor", "combat weapon", "ammunition"]},
    {"genre": "Axe", "keywords": ["battle axe", "chopping", "blunt force", "heavy weapon", "dual-headed", "cleaving", "woodcutter", "viking axe", "war axe", "brutal"]},
    {"genre": "Dagger2", "keywords": ["short blade", "stealth", "throwing dagger", "assassin's weapon", "swift", "close combat", "poisoned tip", "stealth kill", "sharp edge", "concealed"]},
    {"genre": "Spear", "keywords": ["polearm", "piercing", "long reach", "battle spear", "throwing spear", "javelin", "tactical spear", "warrior", "ancient weapon", "sharp tip"]},
    {"genre": "Mace", "keywords": ["bludgeoning", "heavy weapon", "flanged mace", "spiked head", "crushing", "war hammer", "battle mace", "medieval weapon", "blunt force", "close range"]},
    {"genre": "Crossbow", "keywords": ["high velocity", "silent", "quiver", "bolt", "recurve", "tension", "precision", "archery", "silent shooter", "long-range weapon"]},
    {"genre": "Staff", "keywords": ["magic staff", "wizard weapon", "enchanted", "staff of power", "staff of light", "sorcery", "mystical weapon", "long reach", "symbol of wisdom", "arcane power"]},
    {"genre": "Flail", "keywords": ["chain weapon", "blunt force", "spiked ball", "flanged head", "agile", "war flail", "battle weapon", "medieval weapon", "impact", "close range"]},
    {"genre": "Glock", "keywords": ["pistol", "semi-automatic", "compact", "firearm", "concealed carry", "9mm", "self-defense", "police weapon", "tactical", "Glock 19"]},
    {"genre": "Beretta", "keywords": ["firearm", "handgun", "Italian design", "semi-automatic", "Beretta 92", "military", "9mm", "police", "combat pistol", "reliable"]},
    {"genre": "AK-47", "keywords": ["assault rifle", "military weapon", "gas-operated", "7.62mm", "AK platform", "reliable", "combat rifle", "tactical weapon", "Russian design", "high recoil"]},
    {"genre": "M16", "keywords": ["assault rifle", "military use", "5.56mm", "M16A4", "long-range", "semi-automatic", "combat rifle", "tactical", "US military", "reliable"]},
    {"genre": "AR-15", "keywords": ["assault rifle", "firearm", "semi-automatic", "tactical rifle", "military design", "5.56mm", "AR platform", "modular", "customizable", "self-defense"]},
    {"genre": "Remington 870", "keywords": ["shotgun", "pump-action", "tactical shotgun", "12 gauge", "hunting", "military", "law enforcement", "shotgun shell", "Remington", "combat weapon"]},
    {"genre": "Desert Eagle", "keywords": ["handgun", "semi-automatic", "magnum", "powerful recoil", "hunting pistol", "high caliber", "large frame", "military use", "heavy-duty", "Desert Eagle .50"]},
    {"genre": "Ruger", "keywords": ["firearm", "handgun", "Ruger 9mm", "reliable", "self-defense", "target shooting", "semi-automatic", "concealed carry", "compact", "tactical pistol"]},
    {"genre": "S&W (Smith & Wesson)", "keywords": ["handgun", "firearm", "revolver", "semi-automatic", "S&W Model 686", "police weapon", "tactical", "self-defense", "American-made", "law enforcement"]},
    {"genre": "Colt", "keywords": ["firearm", "revolver", "semi-automatic", "1911 pistol", "military sidearm", "American legacy", "combat pistol", "tactical", "self-defense", "Colt M1911"]},
    {"genre": "Taurus", "keywords": ["revolver", "handgun", "firearm", "Brazilian brand", "9mm", "concealed carry", "self-defense", "tactical", "semi-automatic", "reliable"]},
    {"genre": "Sig Sauer", "keywords": ["handgun", "firearm", "semi-automatic", "Sig P226", "military use", "9mm", "Swiss design", "tactical", "combat pistol", "law enforcement"]},
    {"genre": "Heckler & Koch", "keywords": ["firearm", "assault rifle", "H&K MP5", "German engineering", "military weapon", "submachine gun", "precision", "law enforcement", "9mm", "tactical weapon"]},
    {"genre": "Winchester", "keywords": ["shotgun", "rifle", "hunting", "lever-action", "model 70", "bolt-action", "reliable", "Winchester 30-30", "long-range", "outdoor use"]},
    {"genre": "Springfield Armory", "keywords": ["firearm", "1911 pistol", "semi-automatic", "combat handgun", "military sidearm", "self-defense", "target shooting", "American-made", "Springfield XD", "reliable"]},
    {"genre": "Browning", "keywords": ["shotgun", "hunting", "Browning M1911", "high-quality", "firearm", "reliable", "Belgium design", "combat weapon", "Browning Auto-5", "tactical"]},
    {"genre": "Mauser", "keywords": ["bolt-action", "rifle", "military rifle", "Mauser K98", "German engineering", "precision", "WWII", "long-range", "reliable", "classic rifle"]},
    {"genre": "CZ (Česká Zbrojovka)", "keywords": ["firearm", "handgun", "CZ 75", "semi-automatic", "Czech design", "reliable", "combat pistol", "military sidearm", "self-defense", "target shooting"]},
    {"genre": "FN Herstal", "keywords": ["assault rifle", "FN SCAR", "military weapon", "Belgium design", "precision", "combat rifle", "tactical", "special forces", "5.56mm", "reliable"]},
    {"genre": "Mossberg", "keywords": ["shotgun", "hunting shotgun", "tactical shotgun", "pump-action", "Mossberg 500", "military use", "12 gauge", "law enforcement", "reliable", "combat weapon"]},
    {"genre": "Mac-10", "keywords": ["submachine gun", "compact", "fully automatic", "street weapon", "illegal firearm", "rapid fire", "high recoil", "gang warfare", "concealed weapon", "9mm"]},
    {"genre": "Uzi", "keywords": ["submachine gun", "compact", "street weapon", "fully automatic", "gang warfare", "illegal firearm", "Israeli design", "rapid fire", "military use", "9mm"]},
    {"genre": "Tec-9", "keywords": ["handgun", "semi-automatic", "illegal firearm", "street weapon", "gangster gun", "compact", "high recoil", "9mm", "rapid fire", "small frame"]},
    {"genre": "Sawed-off Shotgun", "keywords": ["shotgun", "short barrel", "illegal weapon", "concealed firearm", "street weapon", "close range", "blunt force", "sawed-off barrel", "12 gauge", "criminal use"]},
    {"genre": "Sten Gun", "keywords": ["submachine gun", "World War II", "British design", "fully automatic", "cheap production", "illegal street gun", "smuggling", "rapid fire", "9mm", "classic weapon"]},
    {"genre": "M1911", "keywords": ["handgun", "semi-automatic", "combat pistol", "military sidearm", "1911 design", "classic firearm", "self-defense", "street carry", "lethal", "American-made"]},
    {"genre": "Glock 18", "keywords": ["firearm", "fully automatic", "handgun", "compact", "illegal street weapon", "9mm", "high recoil", "rapid fire", "police use", "self-defense"]},
    {"genre": "FN Five-SeveN", "keywords": ["handgun", "semi-automatic", "military firearm", "5.7x28mm", "compact", "street gun", "high velocity", "low recoil", "self-defense", "criminal use"]},
    {"genre": "Makarov", "keywords": ["handgun", "semi-automatic", "Russian design", "compact", "street weapon", "military sidearm", "9mm", "criminal use", "low recoil", "self-defense"]},
    {"genre": "Blowgun", "keywords": ["blowpipe", "silent weapon", "dart gun", "small caliber", "hunting", "quiet kill", "non-lethal", "illegal weapon", "poisoned darts", "stealth"]},
    {"genre": "Derringer", "keywords": ["handgun", "small caliber", "concealed carry", "short barrel", "street weapon", "pocket pistol", "criminal carry", "compact", "self-defense", "rare firearm"]},
    {"genre": "Glock 34", "keywords": ["handgun", "semi-automatic", "longer barrel", "tactical pistol", "police use", "competition", "street carry", "9mm", "Glock series", "self-defense"]},
    {"genre": "Walther P99", "keywords": ["handgun", "semi-automatic", "German design", "police use", "combat weapon", "self-defense", "9mm", "street weapon", "reliable", "high accuracy"]},
    {"genre": "Ruger Mini-14", "keywords": ["rifle", "semi-automatic", "street gun", "tactical", "urban combat", "self-defense", "hunting", "5.56mm", "reliable", "law enforcement"]},
    {"genre": "Luger P08", "keywords": ["handgun", "semi-automatic", "WWII", "German design", "vintage", "military sidearm", "9mm", "rare", "collectible", "historical firearm"]},
    {"genre": "M1 Garand", "keywords": ["rifle", "semi-automatic", "military use", "WWII", "iconic weapon", "American-made", "long range", "high power", "combat rifle", "collectible"]},
    {"genre": "AKS-74U", "keywords": ["assault rifle", "short-barreled", "Russian design", "compact AK-47", "military weapon", "illegal firearm", "street weapon", "7.62mm", "high recoil", "tactical"]},
    {"genre": "RPG-7", "keywords": ["rocket-propelled grenade", "launching weapon", "anti-tank", "military use", "illegal street weapon", "explosive", "Russian design", "heavy weapon", "high damage", "rare"]},
    {"genre": "M1919 Browning", "keywords": ["machine gun", "heavy weapon", "fully automatic", "WWII", "military use", "high fire rate", "heavy recoil", "vehicle mounted", "explosive power", "classic weapon"]},
    {"genre": "SPAS-12", "keywords": ["shotgun", "pump-action", "tactical shotgun", "military use", "street weapon", "12 gauge", "combat shotgun", "high recoil", "illegal firearm", "collectible"]},
    {"genre": "M3 Grease Gun", "keywords": ["submachine gun", "fully automatic", "military use", "WWII", "tactical weapon", "rapid fire", "compact", "historical firearm", "illegal weapon", "low-cost production"]},
    {"genre": "Pipe Shotgun", "keywords": ["homemade", "street weapon", "makeshift", "illegal firearm", "cheap materials", "close range", "shotgun", "12 gauge", "criminal use", "guerrilla warfare"]},
    {"genre": "Zip Gun", "keywords": ["homemade firearm", "makeshift", "illegal weapon", "craftsmanship", "single-shot", "street weapon", "low-cost", "criminal use", "self-defense", "dangerous"]},
    {"genre": "Molotov Cocktail", "keywords": ["homemade weapon", "flammable", "improvised", "street warfare", "riot control", "explosive", "guerrilla tactics", "flammable liquid", "criminal use", "illegal"]},
    {"genre": "Homemade AR-15", "keywords": ["rebellion weapon", "modified AR-15", "illegal firearm", "street gun", "homemade", "guerrilla warfare", "semi-automatic", "high recoil", "dangerous", "firearm"]},
    {"genre": "Stun Gun", "keywords": ["homemade", "self-defense", "illegal modification", "electric weapon", "non-lethal", "street weapon", "guerrilla tactics", "shock", "makeshift", "illegal"]},
    {"genre": "Claymore Mine (Homemade)", "keywords": ["improvised explosive", "homemade", "guerrilla warfare", "explosive", "landmine", "anti-personnel", "homemade bomb", "illegal weapon", "terrorism", "high danger"]},
    {"genre": "Crowbar (Modified)", "keywords": ["improvised weapon", "makeshift", "street fight", "criminal use", "rebel weapon", "blunt force", "illegal", "self-defense", "close combat", "guerrilla"]},
    {"genre": "Crossbow (Homemade)", "keywords": ["improvised", "street weapon", "homemade crossbow", "silent weapon", "rebel weapon", "archery", "guerrilla warfare", "non-lethal", "illegal", "precision"]},
    {"genre": "Pipe Bomb", "keywords": ["improvised explosive", "homemade", "guerrilla warfare", "illegal weapon", "explosive", "criminal use", "terrorist tactics", "high danger", "explosion", "barricade breaker"]},
    {"genre": "Home-made Rocket Launcher", "keywords": ["improvised", "guerrilla warfare", "rebellion", "homemade weapon", "street weapon", "illegal", "high destruction", "explosive", "illegal armament", "anti-tank"]},
    {"genre": "Molotov Grenade", "keywords": ["improvised", "homemade", "explosive", "flammable", "criminal use", "street warfare", "riot weapon", "urban combat", "guerrilla tactics", "illegal weapon"]},
    {"genre": "Melee Weapon (Homemade)", "keywords": ["homemade", "improvised weapon", "rebellion", "makeshift", "close combat", "street fight", "illegal", "blunt force", "self-defense", "dangerous"]},
    {"genre": "Homemade Sniper Rifle", "keywords": ["modified rifle", "guerrilla warfare", "long-range", "homemade firearm", "illegal", "rebellion", "sniper weapon", "covert", "military use", "dangerous"]},
    {"genre": "Handmade Machete", "keywords": ["homemade", "guerrilla weapon", "close combat", "illegal weapon", "handmade", "bladed weapon", "self-defense", "urban warfare", "dangerous", "weapon"]},
    {"genre": "Sling (Homemade)", "keywords": ["improvised weapon", "homemade", "self-defense", "street weapon", "blunt force", "rebel weapon", "simple weapon", "illegal", "non-lethal", "guerrilla"]},
    {"genre": "Homemade Rocket Propelled Grenade", "keywords": ["improvised", "guerrilla warfare", "illegal weapon", "homemade", "explosive", "military use", "high damage", "self-made", "anti-tank", "rebel weapon"]},
    {"genre": "Chemical Spray (Homemade)", "keywords": ["improvised", "homemade", "chemical weapon", "street use", "guerrilla tactics", "self-defense", "illegal weapon", "toxic", "riot control", "criminal use"]},
    {"genre": "Electromagnetic Pulse (EMP) Device", "keywords": ["improvised weapon", "homemade", "guerrilla warfare", "illegal", "EMP", "electronics attack", "self-made", "technology disruption", "high-tech", "dangerous"]},
    {"genre": "Improvised Knife", "keywords": ["homemade", "bladed weapon", "street weapon", "rebellion", "close combat", "illegal", "self-defense", "makeshift", "dangerous", "urban warfare"]},
    {"genre": "Bottle Bomb", "keywords": ["improvised explosive", "homemade", "criminal use", "illegal weapon", "flammable", "guerrilla tactics", "explosive", "street warfare", "dangerous", "terrorism"]},
    {"genre": "Improvised Grenade", "keywords": ["homemade", "explosive", "guerrilla warfare", "street weapon", "illegal", "dangerous", "rebel tactics", "urban warfare", "self-made", "criminal"]},
    {"genre": "Handmade Flame Thrower", "keywords": ["homemade", "fire weapon", "improvised", "street weapon", "illegal", "explosive", "flammable", "guerrilla warfare", "dangerous", "weapon"]},       
    {"genre": "Western Revolver", "keywords": ["pistol", "classic firearm", "cowboy", "single-action", "western style", "small caliber", "old west", "self-defense", "antique", "quick draw"]},
    {"genre": "Hunting Rifle", "keywords": ["long-range", "rifle", "hunting", "bolt action", "high caliber", "outdoor sport", "reliable", "self-defense", "precision shooting", "illegal modification"]},
    {"genre": "Crossbow", "keywords": ["medieval weapon", "silent", "archery", "long-range", "bow and arrow", "hunting", "rebel weapon", "non-lethal", "improvised", "wooden crossbow"]},
    {"genre": "Homemade Pistol", "keywords": ["improvised firearm", "pistol", "handmade", "illegal", "close combat", "street weapon", "reliable", "self-defense", "low-cost", "dangerous"]},
    {"genre": "Shotgun (Street Version)", "keywords": ["improvised", "shotgun", "homemade", "guerrilla warfare", "illegal weapon", "close-range", "single barrel", "self-defense", "criminal use", "high danger"]},
    {"genre": "Hunting Bow", "keywords": ["archery", "silent weapon", "bow and arrow", "long-range", "non-lethal", "homemade", "outdoor sport", "hunting", "survival", "guerrilla"]},
    {"genre": "Automatic Rifle (Modified)", "keywords": ["modified firearm", "homemade", "automatic", "military-style", "illegal", "guerrilla warfare", "high recoil", "dangerous", "rebel weapon", "illegal weapon"]},
    {"genre": "Revolver (Homemade)", "keywords": ["pistol", "revolver", "makeshift", "illegal weapon", "craftsmanship", "self-defense", "street weapon", "low-cost", "improvised", "dangerous"]},
    {"genre": "Lever-Action Rifle", "keywords": ["rifle", "western style", "lever-action", "hunting", "high power", "self-defense", "reliable", "antique", "rebel weapon", "rustic"]},
    {"genre": "Sawn-Off Shotgun", "keywords": ["shotgun", "short barrel", "close-range", "illegal firearm", "modified", "guerrilla warfare", "improvised", "street weapon", "dangerous", "blunt force"]},
]

shield_types = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Round Shield", "keywords": ["wooden shield", "round shape", "medieval combat", "lightweight", "iron rim", "Viking style", "close combat", "handheld", "classic design", "simple"]},
    {"genre": "Kite Shield", "keywords": ["long shield", "pointed bottom", "medieval knight", "mounted combat", "metal reinforcements", "protection", "European style", "heraldry", "arm strap", "large surface"]},
    {"genre": "Tower Shield", "keywords": ["large shield", "full-body protection", "heavy", "defensive position", "siege combat", "rectangular", "intimidating", "reinforced edges", "cover", "bulky"]},
    {"genre": "Buckler", "keywords": ["small shield", "lightweight", "dueling", "fast movement", "close combat", "metal", "punching defense", "easy to carry", "minimal protection", "handheld"]},
    {"genre": "Pavise", "keywords": ["siege shield", "archer protection", "large shield", "full coverage", "wooden", "set on the ground", "crossbowmen", "tower shield", "painted surface", "medieval warfare"]},
    {"genre": "Scutum", "keywords": ["Roman shield", "large rectangular", "curved shape", "legionnaire", "defensive formations", "metal boss", "iron rim", "tortoise formation", "historical", "arm strap"]},
    {"genre": "Heater Shield", "keywords": ["knight shield", "triangular shape", "heraldry", "tournament use", "horseback combat", "lightweight", "stylish design", "personalized emblem", "medieval", "battle-tested"]},
    {"genre": "Riot Shield", "keywords": ["modern shield", "police use", "transparent", "polycarbonate", "crowd control", "anti-riot", "lightweight", "bullet-resistant", "urban use", "law enforcement"]},
    {"genre": "Ballistic Shield", "keywords": ["tactical shield", "military use", "bulletproof", "SWAT teams", "reinforced steel", "urban combat", "small arms protection", "portable", "viewing window", "high-tech"]},
    {"genre": "Improvised Shield", "keywords": ["makeshift protection", "DIY", "emergency use", "wood", "metal sheet", "plastic", "protest use", "quick assembly", "unorthodox", "temporary"]},
    {"genre": "Targe", "keywords": ["Scottish shield", "small round", "wooden core", "iron reinforcements", "decorative studs", "hand-to-hand combat", "clansman weapon", "lightweight", "traditional", "heritage"]},
    {"genre": "Body Shield", "keywords": ["large protective gear", "riot control", "tactical use", "lightweight composite", "crowd dispersal", "non-lethal force", "operator use", "impact-resistant", "modern", "urban scenarios"]},
    {"genre": "Arm Shield", "keywords": ["forearm protection", "small shield", "lightweight", "close combat", "custom fit", "arm strap", "deflect blows", "personalized", "stealthy", "dueling"]},
    {"genre": "Spiked Shield", "keywords": ["offensive shield", "weaponized", "combat use", "iron spikes", "handheld", "dual purpose", "intimidating", "bladed edges", "heavy", "reinforced"]},
    {"genre": "Magic Shield", "keywords": ["fantasy item", "energy barrier", "spell casting", "arcane protection", "glowing", "mystical", "legendary", "lightweight", "unbreakable", "otherworldly"]},
    {"genre": "Energy Shield", "keywords": ["sci-fi shield", "force field", "high-tech", "plasma protection", "laser deflection", "transparent barrier", "compact", "portable", "futuristic", "power source"]},
    {"genre": "Carapace Shield", "keywords": ["natural material", "beast defense", "insect shell", "primitive design", "tribal use", "organic", "curved shape", "lightweight", "durable", "prehistoric"]},
    {"genre": "Captain's Shield", "keywords": ["fictional design", "circular shield", "throwing weapon", "vibranium", "patriotic", "red and blue", "combat ready", "stylized", "iconic", "unbreakable"]},
    {"genre": "Adarga", "keywords": ["Spanish shield", "leather construction", "oval shape", "lightweight", "dueling", "historical", "decorative", "traditional", "arm strap", "durable"]},
    {"genre": "Steel Shield", "keywords": ["metal shield", "heavy", "sturdy", "combat use", "reinforced edges", "durable", "classic design", "intimidating", "medieval era", "battle-tested"]},
    {"genre": "Leather Shield", "keywords": ["lightweight", "flexible", "primitive design", "handcrafted", "tribal use", "small size", "simple protection", "easy to carry", "customizable", "historical"]},
    {"genre": "Aegis", "keywords": ["mythical shield", "divine protection", "Greek mythology", "Medusa emblem", "impenetrable", "legendary", "decorative", "immortal", "combat ready", "heritage"]},
    {"genre": "War Shield", "keywords": ["tribal shield", "decorative", "handmade", "battle use", "large surface", "painted symbols", "ritualistic", "arm strap", "lightweight", "durable"]},
    {"genre": "Hexagonal Shield", "keywords": ["modern design", "geometric", "stylish", "lightweight", "unique shape", "tactical use", "close combat", "custom fit", "portable", "deflective"]},
    {"genre": "Spartan Shield", "keywords": ["Greek hoplite", "bronze material", "round design", "phalanx combat", "arm strap", "reinforced rim", "intimidating", "decorative", "battle-tested", "lightweight"]},
    {"genre": "Ceremonial Shield", "keywords": ["decorative", "ritual use", "ornate", "gold details", "historical", "symbolic", "non-combat", "handcrafted", "prestigious", "traditional"]},
    {"genre": "Wooden Shield", "keywords": ["basic design", "lightweight", "cheap", "easy to craft", "historical", "primitive", "large surface", "painted decoration", "handheld", "battle-ready"]},
    {"genre": "Deflector Shield", "keywords": ["space combat", "high-tech", "energy-based", "force field", "alien technology", "durable", "power source", "compact design", "protection", "sci-fi"]},
]

protection_types = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Ballistic Vest", "keywords": ["bulletproof", "modern armor", "Kevlar", "tactical gear", "law enforcement", "military use", "lightweight", "impact-resistant", "urban combat", "body armor"]},
    {"genre": "Full Body Armor", "keywords": ["heavy armor", "military gear", "bulletproof", "combat zones", "explosive protection", "full coverage", "reinforced plates", "tactical", "durable", "high-tech"]},
    {"genre": "Riot Gear", "keywords": ["crowd control", "anti-riot", "law enforcement", "impact-resistant", "lightweight", "shock absorbent", "modern", "urban use", "polycarbonate", "police"]},
    {"genre": "EOD Suit", "keywords": ["explosive ordnance disposal", "bomb squad", "blast-resistant", "military use", "high-tech", "heavy protection", "shock absorbent", "heat-resistant", "helmet", "tactical"]},
    {"genre": "Tactical Helmet", "keywords": ["head protection", "bulletproof", "military grade", "lightweight", "modern design", "impact-resistant", "urban combat", "tactical gear", "law enforcement", "camera mount"]},
    {"genre": "Shielded Bunker", "keywords": ["defensive structure", "portable bunker", "military use", "high-tech", "modular", "reinforced", "urban warfare", "bulletproof", "blast-resistant", "field shelter"]},
    {"genre": "Ballistic Mask", "keywords": ["face protection", "law enforcement", "lightweight", "bulletproof", "riot control", "tactical gear", "impact-resistant", "military use", "modern design", "compact"]},
    {"genre": "Anti-Stab Vest", "keywords": ["knife-resistant", "law enforcement", "lightweight", "urban safety", "body armor", "close combat", "modern", "Kevlar", "durable", "compact"]},
    {"genre": "Combat Gloves", "keywords": ["hand protection", "Kevlar", "military use", "law enforcement", "lightweight", "impact-resistant", "close combat", "modern", "fireproof", "reinforced knuckles"]},
    {"genre": "Thigh Guards", "keywords": ["leg protection", "Kevlar", "modern armor", "military use", "lightweight", "impact-resistant", "urban combat", "law enforcement", "tactical gear", "durable"]},
    {"genre": "Tactical Shield", "keywords": ["handheld protection", "law enforcement", "bulletproof", "riot control", "polycarbonate", "urban use", "impact-resistant", "lightweight", "military use", "high-tech"]},
    {"genre": "Armored Vehicle", "keywords": ["vehicle protection", "bulletproof", "military transport", "law enforcement", "urban combat", "explosion-resistant", "high-tech", "modular design", "tactical use", "field deployment"]},
    {"genre": "Blast Plate", "keywords": ["explosive protection", "Kevlar", "military use", "law enforcement", "heavy-duty", "impact-resistant", "reinforced armor", "modern gear", "durable", "compact"]},
    {"genre": "Ghillie Suit", "keywords": ["camouflage", "military use", "sniper gear", "tactical advantage", "lightweight", "concealment", "forest combat", "stealthy", "modern design", "effective"]},
    {"genre": "Neck Guard", "keywords": ["Kevlar", "modern armor", "military use", "law enforcement", "impact-resistant", "lightweight", "urban combat", "tactical gear", "small-scale", "durable"]},
    {"genre": "Flak Jacket", "keywords": ["explosive protection", "military use", "lightweight", "impact-resistant", "modern armor", "tactical gear", "urban combat", "law enforcement", "high-tech", "durable"]},
    {"genre": "Knee Pads", "keywords": ["joint protection", "tactical gear", "Kevlar", "lightweight", "military use", "law enforcement", "modern", "impact-resistant", "durable", "field use"]},
    {"genre": "Energy Barrier", "keywords": ["sci-fi shield", "force field", "urban combat", "military use", "futuristic", "portable", "energy-based", "laser-resistant", "high-tech", "tactical gear"]},
    {"genre": "Armored Boots", "keywords": ["foot protection", "Kevlar", "military use", "law enforcement", "impact-resistant", "modern design", "lightweight", "urban combat", "tactical", "durable"]},
    {"genre": "Portable Shield Generator", "keywords": ["futuristic gear", "energy barrier", "military use", "high-tech", "compact", "portable", "field deployment", "urban combat", "tactical advantage", "force field"]},
    {"genre": "Shock-Proof Suit", "keywords": ["electric resistance", "law enforcement", "military use", "modern armor", "lightweight", "tactical gear", "urban safety", "impact-resistant", "compact", "high-tech"]},
    {"genre": "Drone Defense Shield", "keywords": ["anti-drone", "military use", "law enforcement", "high-tech", "portable", "energy-based", "modern", "tactical advantage", "urban combat", "impact-resistant"]},
]

color_palette = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Red", "keywords": ["crimson", "scarlet", "ruby", "burgundy", "cherry red", "fire engine red", "rose red", "deep red"]},
    {"genre": "Blue", "keywords": ["navy blue", "royal blue", "sky blue", "baby blue", "turquoise", "teal", "cobalt blue", "indigo"]},
    {"genre": "Green", "keywords": ["forest green", "lime green", "emerald", "olive", "mint green", "seafoam green", "jade", "chartreuse"]},
    {"genre": "Yellow", "keywords": ["canary yellow", "goldenrod", "amber", "lemon yellow", "mustard", "sunflower yellow", "pale yellow", "honey"]},
    {"genre": "Black", "keywords": ["jet black", "onyx", "charcoal", "midnight black", "ebony", "ink black", "obsidian", "pitch black"]},
    {"genre": "White", "keywords": ["pure white", "ivory", "snow", "pearl white", "eggshell", "alabaster", "cream", "frost white"]},
    {"genre": "Gray", "keywords": ["silver", "ash gray", "slate gray", "pewter", "charcoal gray", "graphite", "dove gray", "smoke gray"]},
    {"genre": "Pink", "keywords": ["hot pink", "baby pink", "fuchsia", "magenta", "rose pink", "blush", "peach pink", "carnation"]},
    {"genre": "Purple", "keywords": ["violet", "lavender", "plum", "amethyst", "mauve", "orchid", "periwinkle", "royal purple"]},
    {"genre": "Orange", "keywords": ["tangerine", "peach", "apricot", "amber orange", "burnt orange", "coral", "pumpkin", "golden orange"]},
    {"genre": "Brown", "keywords": ["chocolate brown", "mahogany", "walnut", "coffee brown", "caramel", "bronze", "taupe", "chestnut"]},
    {"genre": "Gold", "keywords": ["metallic gold", "pale gold", "antique gold", "rose gold", "yellow gold", "champagne gold", "satin gold", "gold leaf"]},
    {"genre": "Silver", "keywords": ["metallic silver", "platinum", "steel gray", "light silver", "frosted silver", "polished silver", "chrome", "pearl silver"]},
    {"genre": "Beige", "keywords": ["sand", "tan", "ecru", "khaki", "wheat", "buff", "fawn", "light beige"]},
    {"genre": "Teal", "keywords": ["aqua teal", "deep teal", "light teal", "blue-green", "cyan", "turquoise teal", "dark teal", "aquamarine"]},
    {"genre": "Turquoise", "keywords": ["bright turquoise", "pale turquoise", "aqua", "sea green", "aqua blue", "dark turquoise", "cyan turquoise", "ocean teal"]},
    {"genre": "Rose Gold", "keywords": ["blush rose gold", "pinkish gold", "copper rose", "soft rose gold", "antique rose", "vintage rose gold", "brushed rose"]},
    {"genre": "Copper", "keywords": ["bronzed copper", "light copper", "reddish copper", "antique copper", "metallic copper", "burnished copper", "copper gold"]},
    {"genre": "Emerald", "keywords": ["deep emerald", "light emerald", "bright emerald", "jewel emerald", "forest emerald", "green emerald", "rich emerald", "emerald jade"]},
    {"genre": "Ivory", "keywords": ["soft ivory", "antique ivory", "creamy ivory", "pale ivory", "off-white ivory", "warm ivory", "eggshell ivory", "natural ivory"]},
]

color_palette_extend = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Blue-Green", "keywords": ["teal", "aqua", "seafoam", "cyan blue", "turquoise mix", "deep aquamarine"]},
    {"genre": "Red-Orange", "keywords": ["coral", "burnt sienna", "fire opal", "tangerine red", "sunset red"]},
    {"genre": "Yellow-Green", "keywords": ["chartreuse", "lime yellow", "kiwi green", "spring green"]},
    {"genre": "Purple-Blue", "keywords": ["indigo", "periwinkle", "violet blue", "amethyst mix"]},
    {"genre": "Pink-Purple", "keywords": ["magenta", "orchid pink", "fuchsia violet", "plum rose"]},
    {"genre": "Orange-Yellow", "keywords": ["amber gold", "marigold", "butterscotch", "peachy yellow"]},
    {"genre": "Black-Red", "keywords": ["maroon", "dark crimson", "black cherry", "deep burgundy"]},
    {"genre": "Gray-Blue", "keywords": ["slate blue", "steel blue", "dusty gray", "frosted blue"]},
    {"genre": "Gold-White", "keywords": ["champagne gold", "frosted gold", "pearl gold", "ivory shimmer"]},
    {"genre": "Silver-Blue", "keywords": ["icy blue", "chrome blue", "metallic frost", "pearl gray-blue"]},
    {"genre": "Brown-Yellow", "keywords": ["golden bronze", "caramel toffee", "honey brown", "amber tan"]},
    {"genre": "Green-Brown", "keywords": ["olive drab", "forest moss", "sage green", "earthy green"]},
    {"genre": "Blue-Gray", "keywords": ["storm blue", "misty blue", "slate gray", "ocean smoke"]},
    {"genre": "Red-Yellow-Orange", "keywords": ["sunset gradient", "fire tones", "autumn glow", "golden rust"]},
    {"genre": "Purple-Red", "keywords": ["wine berry", "deep plum", "cranberry", "blackberry"]},
    {"genre": "Beige-Pink", "keywords": ["rose beige", "blush sand", "peach cream", "soft nude"]},
    {"genre": "White-Blue", "keywords": ["frost white", "icy pearl", "arctic frost", "soft snow blue"]},
    {"genre": "Gold-Bronze", "keywords": ["antique gold", "burnished bronze", "golden brass", "bronze shimmer"]},
    {"genre": "Silver-Black", "keywords": ["gunmetal gray", "smoky chrome", "dark silver", "pewter black"]},
    {"genre": "Green-Blue", "keywords": ["tropical teal", "ocean jade", "emerald seafoam", "turquoise blend"]},
]

vehicle_models = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Tesla", "keywords": ["electric cars", "autonomous driving", "modern design", "zero emissions", "high-tech features", "long range", "fast acceleration"]},
    {"genre": "Ford", "keywords": ["reliable trucks", "classic design", "off-road capability", "affordable options", "American heritage", "strong engines", "versatile models"]},
    {"genre": "Toyota", "keywords": ["fuel efficiency", "reliable engineering", "hybrid technology", "family-friendly", "durable build", "global popularity", "eco-conscious"]},
    {"genre": "BMW", "keywords": ["luxury performance", "sporty design", "German engineering", "premium interiors", "cutting-edge technology", "smooth driving", "high prestige"]},
    {"genre": "Mercedes-Benz", "keywords": ["luxury vehicles", "elegant design", "advanced safety features", "German quality", "high-end interiors", "smooth performance", "prestige"]},
    {"genre": "Chevrolet", "keywords": ["American classic", "pickup trucks", "muscle cars", "affordable options", "family SUVs", "strong engines", "reliable performance"]},
    {"genre": "Honda", "keywords": ["compact cars", "fuel-efficient", "reliable engineering", "affordable pricing", "family-friendly", "hybrid options", "versatility"]},
    {"genre": "Porsche", "keywords": ["sports cars", "luxury performance", "iconic design", "German engineering", "track-ready", "high-speed performance", "exclusivity"]},
    {"genre": "Ferrari", "keywords": ["exotic cars", "luxury performance", "Italian design", "track-focused", "high prestige", "sleek aesthetics", "powerful engines"]},
    {"genre": "Lamborghini", "keywords": ["exotic cars", "bold design", "high performance", "Italian heritage", "luxury appeal", "supercar status", "rare models"]},
    {"genre": "Audi", "keywords": ["luxury design", "quattro all-wheel drive", "sporty appeal", "advanced technology", "German quality", "premium interiors", "smooth ride"]},
    {"genre": "Volkswagen", "keywords": ["compact cars", "affordable luxury", "fuel-efficient", "global brand", "reliable engineering", "family-friendly", "eco-conscious"]},
    {"genre": "Jeep", "keywords": ["off-road capability", "rugged design", "adventure-ready", "all-terrain", "American heritage", "4x4 technology", "outdoor lifestyle"]},
    {"genre": "Nissan", "keywords": ["affordable pricing", "family-friendly", "fuel-efficient", "reliable engineering", "compact cars", "SUV options", "electric innovation"]},
    {"genre": "Hyundai", "keywords": ["affordable quality", "modern design", "fuel efficiency", "family-oriented", "global popularity", "innovative features", "reliable performance"]},
    {"genre": "Kia", "keywords": ["affordable cars", "modern styling", "fuel-efficient", "family-friendly", "SUV options", "tech-forward", "long warranties"]},
    {"genre": "Subaru", "keywords": ["all-wheel drive", "outdoor adventure", "rugged durability", "family-friendly", "safe handling", "fuel-efficient", "off-road capability"]},
    {"genre": "Mazda", "keywords": ["sporty design", "affordable pricing", "fuel efficiency", "compact cars", "fun to drive", "reliable engineering", "modern aesthetics"]},
    {"genre": "Volvo", "keywords": ["safety features", "luxury interiors", "Swedish design", "family-friendly", "eco-conscious", "SUV options", "advanced technology"]},
    {"genre": "Range Rover", "keywords": ["luxury SUVs", "off-road capability", "British heritage", "premium materials", "prestige", "rugged design", "advanced features"]},
    {"genre": "Jaguar", "keywords": ["luxury cars", "British elegance", "sporty appeal", "modern performance", "sleek design", "premium interiors", "prestige"]},
    {"genre": "Rolls-Royce", "keywords": ["ultra-luxury", "handcrafted design", "British heritage", "prestige", "custom interiors", "smooth ride", "elite status"]},
    {"genre": "Bugatti", "keywords": ["hyper-luxury", "extreme performance", "French design", "world-class speed", "limited edition", "exclusive build", "cutting-edge engineering"]},
    {"genre": "Maserati", "keywords": ["Italian luxury", "sporty design", "performance-oriented", "exotic appeal", "premium interiors", "iconic style", "prestige"]},
    {"genre": "McLaren", "keywords": ["supercars", "aerodynamics", "track-ready performance", "British engineering", "luxury materials", "lightweight design", "cutting-edge tech"]},
    {"genre": "Bentley", "keywords": ["British luxury", "classic style", "powerful engines", "elegant interiors", "prestige", "high-end craftsmanship", "smooth driving"]},
    {"genre": "Peugeot", "keywords": ["affordable cars", "French design", "fuel efficiency", "compact size", "urban practicality", "modern aesthetics", "global appeal"]},
    {"genre": "Renault", "keywords": ["French engineering", "compact design", "fuel efficiency", "urban-friendly", "affordable options", "reliable build", "innovative features"]},
    {"genre": "Alfa Romeo", "keywords": ["Italian heritage", "sporty design", "luxury performance", "distinctive aesthetics", "compact cars", "driving excitement", "premium feel"]},
    {"genre": "Citroën", "keywords": ["French innovation", "unique design", "urban practicality", "affordable pricing", "fuel efficiency", "modern features", "comfortable interiors"]},
    {"genre": "Dodge", "keywords": ["muscle cars", "powerful engines", "bold design", "American performance", "reliable trucks", "sporty appeal", "durability"]},
    {"genre": "RAM", "keywords": ["pickup trucks", "towing capacity", "rugged design", "off-road capability", "American engineering", "heavy-duty performance", "versatility"]},
    {"genre": "GMC", "keywords": ["trucks", "SUVs", "professional-grade", "off-road performance", "luxury trucks", "American engineering", "durable build"]},
    {"genre": "Buick", "keywords": ["luxury SUVs", "smooth ride", "American heritage", "premium feel", "family-friendly", "reliable performance", "elegant design"]},
    {"genre": "Chrysler", "keywords": ["minivans", "family-oriented", "American engineering", "comfortable interiors", "classic design", "smooth performance", "versatile options"]},
    {"genre": "Acura", "keywords": ["luxury design", "Japanese engineering", "performance-oriented", "modern technology", "affordable luxury", "sleek styling", "premium feel"]},
    {"genre": "Infiniti", "keywords": ["luxury SUVs", "sleek design", "Japanese innovation", "modern features", "smooth performance", "family-oriented", "prestige"]},
    {"genre": "Cadillac", "keywords": ["American luxury", "classic appeal", "premium interiors", "bold design", "powerful engines", "prestige", "smooth ride"]},
    {"genre": "Lexus", "keywords": ["Japanese luxury", "reliable engineering", "smooth performance", "modern styling", "eco-friendly hybrids", "premium interiors", "global prestige"]},
    {"genre": "Mini", "keywords": ["compact design", "British charm", "urban-friendly", "fun to drive", "modern features", "iconic styling", "customizable options"]},
    {"genre": "Suzuki", "keywords": ["compact vehicles", "affordable pricing", "fuel efficiency", "urban practicality", "reliable engineering", "small SUVs", "global appeal"]},
    {"genre": "Scion", "keywords": ["youth-focused design", "modern styling", "compact size", "affordable pricing", "Japanese engineering", "fuel efficiency", "customization options"]},
    {"genre": "Fiat", "keywords": ["Italian charm", "compact cars", "urban practicality", "affordable pricing", "modern design", "fuel-efficient", "stylish appeal"]},
    {"genre": "Mitsubishi", "keywords": ["reliable SUVs", "fuel efficiency", "compact design", "off-road capability", "affordable options", "Japanese engineering", "versatility"]},
    {"genre": "Genesis", "keywords": ["luxury performance", "modern design", "Korean innovation", "premium materials", "advanced technology", "smooth ride", "prestige"]},
    {"genre": "Koenigsegg", "keywords": ["hypercars", "extreme performance", "Swedish innovation", "limited production", "exclusivity", "high speed", "cutting-edge engineering"]},
    {"genre": "Pagani", "keywords": ["Italian hypercars", "luxury craftsmanship", "rare vehicles", "aerodynamics", "artistic design", "high-performance engines", "exclusivity"]},
    {"genre": "Hummer", "keywords": ["off-road capability", "rugged design", "military roots", "bold styling", "heavy-duty performance", "American heritage", "electric revival"]},
    {"genre": "Sedan", "keywords": ["compact design", "fuel-efficient", "smooth ride", "family-friendly", "urban comfort", "spacious interior", "sleek styling"]},
    {"genre": "SUV", "keywords": ["all-wheel drive", "rugged durability", "off-road capabilities", "family-oriented", "versatile space", "high ground clearance", "adventurous spirit"]},
    {"genre": "Truck", "keywords": ["heavy-duty", "towing capacity", "powerful engine", "workhorse", "durable frame", "utility-focused", "off-road performance"]},
    {"genre": "Electric Car", "keywords": ["zero emissions", "modern design", "quiet engine", "high-tech features", "eco-friendly", "long range", "fast charging"]},
    {"genre": "Sports Car", "keywords": ["high performance", "sleek aesthetics", "speed-focused", "luxury features", "low profile", "aerodynamic design", "track-ready"]},
    {"genre": "Convertible", "keywords": ["open-top driving", "luxurious feel", "stylish design", "summer-ready", "compact build", "high-performance engine", "freedom-focused"]},
    {"genre": "Minivan", "keywords": ["family-oriented", "spacious seating", "sliding doors", "child-friendly", "road-trip ready", "cargo versatility", "practical design"]},
    {"genre": "Hybrid", "keywords": ["fuel-efficient", "dual powertrain", "eco-conscious", "advanced technology", "smooth transition", "city-friendly", "quiet performance"]},
    {"genre": "Coupe", "keywords": ["sporty appeal", "compact size", "sleek lines", "luxury features", "two-door design", "performance-driven", "stylish interiors"]},
    {"genre": "Hatchback", "keywords": ["compact utility", "fuel efficiency", "urban maneuverability", "rear cargo access", "versatile seating", "youthful design", "practicality"]},
    {"genre": "Motorcycle", "keywords": ["two-wheel freedom", "lightweight design", "adventurous spirit", "compact power", "fuel-efficient", "road-trip ready", "urban agility"]},
    {"genre": "Luxury Sedan", "keywords": ["elegant design", "premium materials", "smooth performance", "high-end features", "spacious interior", "quiet cabin", "prestige"]},
    {"genre": "Pickup Truck", "keywords": ["rugged power", "off-road readiness", "cargo capability", "heavy-duty performance", "towing strength", "all-terrain ability", "workhorse appeal"]},
    {"genre": "Crossover", "keywords": ["compact SUV", "urban practicality", "fuel-efficient", "versatile space", "family-friendly", "modern styling", "light off-road"]},
    {"genre": "ATV", "keywords": ["all-terrain", "off-road adventures", "rugged design", "compact power", "mud-ready", "recreational use", "agility"]},
    {"genre": "RV", "keywords": ["road-trip ready", "home on wheels", "spacious interior", "kitchen-equipped", "family-friendly", "camping luxury", "adventure-focused"]},
    {"genre": "Sports Bike", "keywords": ["high speed", "sleek design", "agile handling", "racing-inspired", "aerodynamic frame", "performance-focused", "lightweight"]},
    {"genre": "Electric Scooter", "keywords": ["eco-friendly", "lightweight", "urban mobility", "quiet motor", "compact size", "short-range travel", "youthful design"]},
    {"genre": "Van", "keywords": ["cargo space", "business utility", "delivery-ready", "spacious design", "practical build", "fleet use", "urban reliability"]},
    {"genre": "Off-Road SUV", "keywords": ["adventure-ready", "4x4 capabilities", "rugged terrain", "durable build", "outdoor lifestyle", "raised suspension", "strong performance"]},
    {"genre": "Luxury SUV", "keywords": ["premium features", "spacious comfort", "high-end design", "quiet interior", "advanced technology", "off-road luxury", "family prestige"]},
    {"genre": "Classic Car", "keywords": ["vintage style", "timeless design", "collector's item", "nostalgic appeal", "handcrafted details", "retro charm", "unique identity"]},
    {"genre": "Supercar", "keywords": ["ultra-performance", "exotic design", "aerodynamics", "luxury interior", "track speed", "rare build", "engineering marvel"]},
    {"genre": "Electric SUV", "keywords": ["eco-friendly", "spacious design", "zero emissions", "long-range capability", "family-friendly", "modern technology", "quiet drive"]},
    {"genre": "Diesel Truck", "keywords": ["torque-heavy", "fuel-efficient", "work-oriented", "off-road capability", "durable engine", "long-haul", "industrial strength"]},
    {"genre": "Luxury Coupe", "keywords": ["elegant design", "premium features", "performance-oriented", "two-door styling", "sleek aesthetics", "modern technology", "exclusive build"]},
    {"genre": "Military Vehicle", "keywords": ["armored build", "off-road capabilities", "rugged design", "tactical use", "high durability", "all-terrain", "special-purpose"]},
    {"genre": "Ambulance", "keywords": ["emergency vehicle", "medical equipment", "spacious interior", "fast response", "sturdy build", "life-saving", "professional use"]},
    {"genre": "Fire Truck", "keywords": ["emergency vehicle", "firefighting equipment", "heavy-duty", "water hoses", "ladder functionality", "bright colors", "rescue-oriented"]},
    {"genre": "Taxi", "keywords": ["urban service", "compact build", "fuel-efficient", "yellow color", "public transportation", "metered fare", "city-ready"]},
    {"genre": "Police Car", "keywords": ["law enforcement", "durable build", "emergency lights", "high-speed performance", "urban pursuit", "special features", "public safety"]},
    {"genre": "Convertible SUV", "keywords": ["open-top", "family-friendly", "rugged design", "all-terrain capability", "stylish appearance", "spacious interior", "outdoor lifestyle"]},
    {"genre": "Camper Van", "keywords": ["compact living", "adventure vehicle", "road trips", "convertible interior", "kitchen-equipped", "mobile lifestyle", "versatile space"]},
    {"genre": "Sports Utility Truck", "keywords": ["hybrid design", "rugged utility", "off-road performance", "powerful build", "versatile cargo", "dynamic appearance", "adventure-ready"]},
    {"genre": "Hovercraft", "keywords": ["amphibious", "air-cushion", "terrain versatility", "futuristic design", "unique build", "adventurous use", "smooth glide"]},
    {"genre": "Hypercar", "keywords": ["ultra-luxury", "extreme performance", "cutting-edge technology", "exotic design", "limited edition", "track-focused", "prestige"]},
    {"genre": "Electric Bike", "keywords": ["lightweight", "eco-friendly", "urban commute", "quiet motor", "long range", "modern design", "portable build"]},
    {"genre": "Autonomous Vehicle", "keywords": ["self-driving", "AI-powered", "modern technology", "eco-friendly", "safe navigation", "innovative design", "urban practicality"]},
    {"genre": "Utility Van", "keywords": ["cargo-focused", "delivery vehicle", "compact design", "durable build", "urban use", "practical storage", "business-oriented"]},
    {"genre": "Agricultural Vehicle", "keywords": ["tractor-like", "fieldwork", "heavy-duty", "utility-driven", "special-purpose", "rural design", "terrain adaptability"]}, 
]

nationalities = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Canadian", "keywords": ["warm flannel shirts", "rugged outdoors", "polite demeanor", "maple leaf symbols", "dynamic energy", "cultural pride", "natural surroundings", "majestic simplicity", "snowy landscapes", "ancestral charm"]},
    {"genre": "Quebecois", "keywords": ["cozy sweaters", "traditional cuisine", "artistic flair", "French-Canadian accent", "cultural richness", "dynamic personality", "winter charm", "heritage pride", "folk traditions", "majestic elegance"]},
    {"genre": "American", "keywords": ["casual attire", "diverse backgrounds", "vibrant energy", "patriotic symbols", "cultural diversity", "bold individuality", "dynamic lifestyles", "majestic resilience", "urban and rural scenes", "modern charm"]},
    {"genre": "French", "keywords": ["elegant fashion", "berets and scarves", "artistic flair", "cultural refinement", "Parisian backdrop", "majestic charisma", "timeless beauty", "romantic ambiance", "dynamic sophistication", "heritage pride"]},
    {"genre": "German", "keywords": ["traditional dirndl and lederhosen", "efficient demeanor", "rich cultural heritage", "majestic landscapes", "timeless craftsmanship", "dynamic traditions", "heritage pride", "beer steins and pretzels", "commanding charisma", "refined elegance"]},
    {"genre": "Italian", "keywords": ["stylish attire", "cultural richness", "warm charisma", "vibrant energy", "majestic Mediterranean scenes", "timeless traditions", "culinary passion", "dynamic gestures", "refined beauty", "ancestral charm"]},
    {"genre": "British", "keywords": ["classic trench coats", "reserved elegance", "tea traditions", "cultural sophistication", "majestic landscapes", "timeless charm", "heritage pride", "urban and countryside mix", "royal allure", "refined wit"]},
    {"genre": "Spanish", "keywords": ["flamenco dresses", "vibrant colors", "dynamic energy", "majestic culture", "timeless charisma", "passionate gestures", "heritage pride", "artistic traditions", "Mediterranean ambiance", "rich history"]},
    {"genre": "Japanese", "keywords": ["traditional kimonos", "calm demeanor", "dynamic precision", "cultural elegance", "majestic cherry blossoms", "timeless aesthetics", "heritage pride", "urban and rural contrasts", "refined sophistication", "ancestral charm"]},
    {"genre": "Korean", "keywords": ["modern streetwear", "traditional hanbok", "cultural richness", "vibrant energy", "dynamic creativity", "majestic landscapes", "ancestral pride", "urban chic", "refined artistry", "timeless elegance"]},
    {"genre": "Chinese", "keywords": ["ornate attire", "cultural pride", "majestic presence", "timeless traditions", "dynamic energy", "heritage wealth", "calligraphic art", "refined sophistication", "ancestral beauty", "scenic landscapes"]},
    {"genre": "Indian", "keywords": ["vibrant sarees", "ornate jewelry", "cultural richness", "majestic celebrations", "dynamic energy", "heritage pride", "spiritual ambiance", "timeless grace", "ancestral wisdom", "refined charm"]},
    {"genre": "Mexican", "keywords": ["colorful traditional attire", "dynamic gestures", "cultural pride", "majestic charisma", "timeless celebrations", "heritage charm", "warm energy", "artistic traditions", "ancestral beauty", "vibrant scenes"]},
    {"genre": "Brazilian", "keywords": ["vibrant carnival costumes", "dynamic samba moves", "cultural energy", "majestic charisma", "tropical landscapes", "heritage pride", "warm personalities", "dynamic music", "ancestral artistry", "joyful ambiance"]},
    {"genre": "Australian", "keywords": ["rugged attire", "dynamic energy", "majestic outback scenes", "cultural pride", "timeless charm", "beach and bush contrasts", "ancestral heritage", "warm charisma", "wildlife connections", "refined simplicity"]},
    {"genre": "Russian", "keywords": ["fur-lined coats", "cultural pride", "majestic landscapes", "timeless traditions", "ancestral charm", "refined elegance", "dynamic gestures", "urban and rural contrasts", "strong presence", "heritage resilience"]},
    {"genre": "South African", "keywords": ["vibrant attire", "cultural diversity", "dynamic energy", "majestic savanna scenes", "ancestral pride", "timeless charisma", "rich traditions", "refined gestures", "heritage unity", "joyful ambiance"]},
    {"genre": "Egyptian", "keywords": ["ornate attire", "cultural pride", "majestic deserts", "ancestral wisdom", "timeless elegance", "heritage charm", "refined beauty", "dynamic energy", "pharaonic aura", "mystical presence"]},
    {"genre": "Turkish", "keywords": ["traditional attire", "cultural richness", "majestic charisma", "timeless elegance", "heritage pride", "dynamic gestures", "refined artistry", "ancestral beauty", "dynamic energy", "urban and historic blends"]},
    {"genre": "Thai", "keywords": ["ornate attire", "cultural pride", "majestic temples", "timeless elegance", "heritage charm", "dynamic energy", "refined beauty", "ancestral artistry", "vibrant celebrations", "tropical surroundings"]},
    {"genre": "Greek", "keywords": ["traditional toga-inspired attire", "cultural pride", "majestic ruins", "timeless elegance", "ancestral wisdom", "refined gestures", "heritage charisma", "Mediterranean ambiance", "dynamic energy", "mythical allure"]},
    {"genre": "Irish", "keywords": ["cozy sweaters", "cultural charm", "majestic green landscapes", "timeless traditions", "ancestral pride", "heritage music", "refined demeanor", "warm energy", "dynamic storytelling", "rich folklore"]},
    {"genre": "Scottish", "keywords": ["traditional kilts", "heritage pride", "majestic highlands", "ancestral charisma", "dynamic energy", "refined gestures", "bagpipe music", "timeless strength", "cultural resilience", "rugged charm"]},
    {"genre": "Dutch", "keywords": ["simple yet elegant attire", "cultural richness", "majestic tulip fields", "heritage charm", "ancestral wisdom", "refined beauty", "dynamic energy", "windmill backdrops", "warm personalities", "timeless artistry"]},
    {"genre": "Swedish", "keywords": ["minimalist attire", "heritage pride", "majestic forests", "timeless elegance", "ancestral wisdom", "refined gestures", "dynamic traditions", "cultural innovation", "warm demeanor", "nordic serenity"]},
    {"genre": "Norwegian", "keywords": ["traditional bunads", "majestic fjords", "ancestral pride", "timeless charm", "heritage resilience", "refined beauty", "dynamic energy", "nordic strength", "cultural richness", "serene landscapes"]},
    {"genre": "Finnish", "keywords": ["cozy attire", "majestic winter scenes", "ancestral resilience", "timeless simplicity", "heritage charm", "refined demeanor", "dynamic traditions", "nordic beauty", "cultural pride", "tranquil presence"]},
    {"genre": "Polish", "keywords": ["traditional folk dresses", "cultural richness", "majestic landscapes", "ancestral pride", "timeless charm", "heritage beauty", "refined gestures", "dynamic energy", "vibrant traditions", "warm personalities"]},
    {"genre": "Hungarian", "keywords": ["colorful traditional attire", "cultural pride", "majestic charisma", "ancestral charm", "timeless beauty", "heritage traditions", "refined gestures", "dynamic energy", "artistic sophistication", "rich folk culture"]},
    {"genre": "Kurdish", "keywords": ["traditional vibrant attire", "ancestral pride", "majestic landscapes", "timeless strength", "heritage resilience", "dynamic gestures", "cultural charm", "refined beauty", "warm demeanor", "rich traditions"]},
    {"genre": "Armenian", "keywords": ["traditional attire", "cultural pride", "majestic mountains", "ancestral resilience", "timeless charm", "heritage beauty", "refined artistry", "dynamic energy", "warm personalities", "rich history"]},
    {"genre": "Persian", "keywords": ["ornate attire", "cultural richness", "majestic elegance", "timeless sophistication", "heritage beauty", "refined gestures", "ancestral pride", "dynamic artistry", "warm charisma", "poetic allure"]},
    {"genre": "Mongolian", "keywords": ["traditional deel robes", "cultural richness", "majestic steppes", "ancestral strength", "timeless traditions", "heritage charm", "refined gestures", "dynamic energy", "nomadic charisma", "historic pride"]},
    {"genre": "Vietnamese", "keywords": ["traditional ao dai", "cultural richness", "majestic landscapes", "ancestral pride", "timeless beauty", "heritage elegance", "dynamic energy", "refined gestures", "vibrant celebrations", "serene charm"]},
    {"genre": "Filipino", "keywords": ["traditional barong and terno", "cultural pride", "majestic tropical scenes", "ancestral charisma", "timeless beauty", "heritage charm", "dynamic energy", "refined demeanor", "vibrant traditions", "warm personalities"]},
    {"genre": "Malay", "keywords": ["traditional baju kurung", "cultural richness", "majestic charisma", "ancestral pride", "timeless beauty", "heritage charm", "refined gestures", "dynamic traditions", "serene landscapes", "vibrant festivals"]},
    {"genre": "Indonesian", "keywords": ["vibrant batik patterns", "cultural pride", "majestic islands", "ancestral wisdom", "timeless beauty", "heritage elegance", "refined artistry", "dynamic energy", "vibrant traditions", "rich folklore"]},
    {"genre": "Tibetan", "keywords": ["traditional chubas", "majestic mountains", "ancestral resilience", "timeless serenity", "heritage spirituality", "refined gestures", "dynamic energy", "cultural wisdom", "warm presence", "sacred charm"]},
    {"genre": "Native American", "keywords": ["traditional regalia", "cultural pride", "majestic landscapes", "ancestral wisdom", "timeless spirituality", "heritage beauty", "refined gestures", "dynamic traditions", "warm resilience", "historic strength"]},
    {"genre": "Inuit", "keywords": ["traditional fur-lined attire", "cultural resilience", "majestic Arctic landscapes", "ancestral wisdom", "timeless strength", "heritage beauty", "refined demeanor", "dynamic survival skills", "warm energy", "nordic presence"]},
    {"genre": "Israeli", "keywords": ["modern and traditional attire", "cultural diversity", "majestic landscapes", "ancestral pride", "timeless traditions", "heritage resilience", "refined demeanor", "dynamic energy", "innovative spirit", "historic depth"]},
    {"genre": "Turkish", "keywords": ["traditional Ottoman-inspired attire", "cultural richness", "majestic mosques", "ancestral pride", "timeless beauty", "heritage charm", "refined artistry", "dynamic energy", "vibrant traditions", "warm hospitality"]},
    {"genre": "Cuban", "keywords": ["tropical attire", "cultural vibrancy", "majestic beaches", "ancestral pride", "timeless music", "heritage charm", "dynamic rhythms", "refined movements", "vibrant festivals", "warm charisma"]},
    {"genre": "Jamaican", "keywords": ["casual tropical attire", "cultural vibrancy", "majestic beaches", "ancestral pride", "timeless rhythms", "heritage music", "dynamic energy", "refined movements", "vibrant colors", "warm charisma"]},
    {"genre": "Afghan", "keywords": ["traditional vibrant attire", "cultural resilience", "majestic mountains", "ancestral strength", "timeless charm", "heritage beauty", "refined gestures", "dynamic traditions", "warm personalities", "historic pride"]},
    {"genre": "Pakistani", "keywords": ["traditional shalwar kameez", "cultural richness", "majestic landscapes", "ancestral pride", "timeless elegance", "heritage beauty", "refined gestures", "dynamic energy", "vibrant festivals", "warm personalities"]},
    {"genre": "Bangladeshi", "keywords": ["vibrant saris", "cultural richness", "majestic rivers", "ancestral pride", "timeless traditions", "heritage charm", "dynamic artistry", "refined gestures", "warm personalities", "vibrant celebrations"]},
    {"genre": "Nepali", "keywords": ["traditional daura suruwal", "majestic Himalayas", "ancestral resilience", "timeless traditions", "heritage beauty", "refined gestures", "dynamic spirituality", "cultural charm", "warm energy", "sacred presence"]},
    {"genre": "Sri Lankan", "keywords": ["traditional saris", "cultural richness", "majestic tropical backdrops", "ancestral pride", "timeless charm", "heritage beauty", "refined artistry", "dynamic energy", "vibrant traditions", "warm charisma"]},
    {"genre": "Kenyan", "keywords": ["vibrant kitenge patterns", "cultural richness", "majestic savannahs", "ancestral pride", "timeless charm", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "vibrant celebrations"]},
    {"genre": "Nigerian", "keywords": ["traditional agbada and gele", "cultural vibrancy", "majestic landscapes", "ancestral pride", "timeless beauty", "heritage elegance", "dynamic artistry", "refined gestures", "vibrant celebrations", "warm personalities"]},
    {"genre": "Ethiopian", "keywords": ["traditional habesha kemis", "cultural richness", "majestic highlands", "ancestral pride", "timeless traditions", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "historic depth"]},
    {"genre": "South African", "keywords": ["modern and traditional fusion", "cultural diversity", "majestic vistas", "ancestral pride", "timeless music", "heritage beauty", "dynamic energy", "refined gestures", "vibrant celebrations", "warm charisma"]},
    {"genre": "Moroccan", "keywords": ["ornate caftans", "cultural richness", "majestic deserts", "ancestral charm", "timeless elegance", "heritage artistry", "refined gestures", "dynamic energy", "vibrant colors", "warm hospitality"]},
    {"genre": "Argentinian", "keywords": ["elegant attire", "cultural vibrancy", "majestic mountains", "ancestral pride", "timeless tango", "heritage charm", "refined movements", "dynamic energy", "warm personalities", "artistic depth"]},
    {"genre": "Chilean", "keywords": ["traditional huaso attire", "cultural richness", "majestic Andes", "ancestral pride", "timeless traditions", "heritage beauty", "refined gestures", "dynamic energy", "warm hospitality", "artistic charm"]},
    {"genre": "Peruvian", "keywords": ["vibrant traditional attire", "cultural richness", "majestic Andes", "ancestral pride", "timeless charm", "heritage artistry", "dynamic energy", "refined gestures", "warm personalities", "historic depth"]},
    {"genre": "Bolivian", "keywords": ["colorful traditional attire", "cultural richness", "majestic mountains", "ancestral pride", "timeless beauty", "heritage charm", "dynamic artistry", "refined gestures", "warm hospitality", "historic pride"]},
    {"genre": "Haitian", "keywords": ["traditional vibrant attire", "cultural vibrancy", "majestic tropical backdrops", "ancestral pride", "timeless rhythms", "heritage charm", "dynamic artistry", "refined gestures", "warm personalities", "vibrant celebrations"]},
    {"genre": "Saudi Arabian", "keywords": ["traditional thobe and abaya", "cultural richness", "majestic deserts", "ancestral pride", "timeless elegance", "heritage beauty", "refined gestures", "dynamic energy", "warm hospitality", "spiritual depth"]},
    {"genre": "Emirati", "keywords": ["luxurious kandura and abaya", "cultural vibrancy", "majestic skylines", "ancestral pride", "timeless traditions", "heritage charm", "dynamic energy", "refined gestures", "modern fusion", "warm hospitality"]},
    {"genre": "Vietnamese", "keywords": ["traditional áo dài", "cultural richness", "majestic landscapes", "ancestral pride", "timeless elegance", "heritage artistry", "refined gestures", "dynamic energy", "warm personalities", "vibrant traditions"]},
    {"genre": "Cambodian", "keywords": ["traditional sampot", "cultural vibrancy", "majestic temples", "ancestral pride", "timeless beauty", "heritage charm", "refined artistry", "dynamic energy", "warm personalities", "historic depth"]},
    {"genre": "Laotian", "keywords": ["traditional sinh", "cultural richness", "majestic river scenery", "ancestral pride", "timeless traditions", "heritage artistry", "refined gestures", "dynamic energy", "warm personalities", "vibrant charm"]},
    {"genre": "Myanmar (Burmese)", "keywords": ["traditional longyi", "cultural richness", "majestic pagodas", "ancestral pride", "timeless elegance", "heritage beauty", "refined gestures", "dynamic spirituality", "warm personalities", "historic charm"]},
    {"genre": "Kazakh", "keywords": ["traditional chapan", "cultural richness", "majestic steppes", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "warm hospitality", "historic charm"]},
    {"genre": "Uzbek", "keywords": ["traditional atlas patterns", "cultural richness", "majestic architecture", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "vibrant traditions"]},
    {"genre": "Mongolian", "keywords": ["traditional deel", "cultural richness", "majestic landscapes", "ancestral pride", "timeless charm", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "historic depth"]},
    {"genre": "Armenian", "keywords": ["traditional taraz", "cultural richness", "majestic mountains", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "warm hospitality", "historic charm"]},
    {"genre": "Georgian", "keywords": ["traditional chokha", "cultural richness", "majestic landscapes", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "warm personalities", "vibrant traditions"]},
    {"genre": "Korean (North and South)", "keywords": ["traditional hanbok", "cultural richness", "majestic mountains", "ancestral pride", "timeless elegance", "heritage artistry", "refined gestures", "dynamic energy", "modern fusion", "warm personalities"]},
    {"genre": "Tibetan", "keywords": ["traditional chuba", "cultural richness", "majestic Himalayas", "ancestral pride", "timeless spirituality", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "sacred presence"]},
    {"genre": "Icelandic", "keywords": ["modern and traditional attire", "cultural richness", "majestic landscapes", "ancestral pride", "timeless beauty", "heritage charm", "refined gestures", "dynamic energy", "warm personalities", "historic depth"]},
    {"genre": "Greek", "keywords": ["traditional foustanella", "cultural richness", "majestic islands", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "warm hospitality", "historic charm"]},
    {"genre": "Polynesian", "keywords": ["vibrant tropical attire", "cultural richness", "majestic beaches", "ancestral pride", "timeless traditions", "heritage artistry", "refined gestures", "dynamic energy", "warm hospitality", "sacred charm"]},
    {"genre": "Aboriginal Australian", "keywords": ["traditional ceremonial attire", "cultural vibrancy", "majestic outback landscapes", "ancestral pride", "timeless traditions", "heritage artistry", "refined gestures", "spiritual depth", "vibrant community", "sacred connection"]},
    {"genre": "Maori (New Zealand)", "keywords": ["traditional moko and attire", "cultural richness", "majestic landscapes", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "warm hospitality", "spiritual presence"]},
    {"genre": "Inca", "keywords": ["golden ornaments", "rich textiles", "Andean mountains", "ancestral pride", "timeless beauty", "heritage artistry", "sun worship", "stone temples", "refined craftsmanship", "majestic legacy"]},
    {"genre": "Maya", "keywords": ["intricate carvings", "hieroglyphic artistry", "jungle landscapes", "ancestral wisdom", "timeless elegance", "celestial motifs", "pyramid temples", "vivid murals", "cosmic connection", "spiritual depth"]},
    {"genre": "Aztec", "keywords": ["feathered headdresses", "stone carvings", "majestic warriors", "ancestral pride", "timeless artistry", "eagle and serpent motifs", "temple grandeur", "ritual symbolism", "cosmic balance", "sacred vitality"]},
    {"genre": "Babylonian", "keywords": ["ziggurat temples", "cuneiform inscriptions", "majestic river valleys", "ancestral pride", "timeless sophistication", "heritage beauty", "refined art", "astronomical knowledge", "mythological grandeur", "opulent textiles"]},
    {"genre": "Sumerian", "keywords": ["ancient city-states", "cuneiform tablets", "majestic rivers", "ancestral wisdom", "timeless craftsmanship", "heritage beauty", "refined artistry", "early civilization", "sacred temples", "historic depth"]},
    {"genre": "Ancient Egyptian", "keywords": ["pharaohs and queens", "pyramids of Giza", "hieroglyphic artistry", "timeless elegance", "sunlit deserts", "refined jewelry", "spiritual connection", "majestic temples", "golden tones", "royal charisma"]},
    {"genre": "Norse (Viking)", "keywords": ["runestone inscriptions", "majestic fjords", "ancestral pride", "timeless craftsmanship", "heritage beauty", "refined weaponry", "sailing ships", "warrior spirit", "mythological motifs", "historic charisma"]},
    {"genre": "Etruscan", "keywords": ["rich ceramics", "majestic tombs", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "golden artifacts", "historic charm", "ancient influence"]},
    {"genre": "Hittite", "keywords": ["ancient fortresses", "cultural richness", "majestic landscapes", "ancestral pride", "timeless craftsmanship", "heritage beauty", "refined artistry", "mythological motifs", "stone carvings", "historic charm"]},
    {"genre": "Phoenician", "keywords": ["maritime trade", "majestic ships", "ancestral pride", "timeless craftsmanship", "heritage beauty", "purple dye mastery", "refined artistry", "coastal grandeur", "mythological legacy", "historic influence"]},
    {"genre": "Minoan", "keywords": ["fresco artistry", "majestic palaces", "ancestral pride", "timeless elegance", "heritage charm", "refined gestures", "dynamic energy", "vivid murals", "historic beauty", "ancient creativity"]},
    {"genre": "Ancient Greek (Mycenaean)", "keywords": ["golden masks", "majestic architecture", "ancestral pride", "timeless artistry", "heritage beauty", "refined craftsmanship", "heroic motifs", "dynamic energy", "historic charisma", "epic legacy"]},
    {"genre": "Native American Mississippian", "keywords": ["mound builders", "cultural vibrancy", "majestic rivers", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "ceremonial symbolism", "historic connection"]},
    {"genre": "Celtic (Gaul)", "keywords": ["intricate patterns", "majestic landscapes", "ancestral pride", "timeless craftsmanship", "heritage beauty", "refined gestures", "dynamic energy", "warrior spirit", "mythological motifs", "historic depth"]},
    {"genre": "Olmec", "keywords": ["colossal heads", "cultural richness", "majestic jungles", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "mystical symbolism", "historic creativity"]},
    {"genre": "Scythian", "keywords": ["golden treasures", "cultural vibrancy", "majestic steppes", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "nomadic charm", "historic elegance"]},
    {"genre": "Byzantine", "keywords": ["mosaic artistry", "majestic churches", "ancestral pride", "timeless elegance", "heritage beauty", "refined gestures", "golden icons", "dynamic spirituality", "ornate textiles", "historic depth"]},
    {"genre": "Mughal Empire", "keywords": ["ornate architecture", "majestic palaces", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "vivid murals", "royal sophistication", "historic grandeur"]},
    {"genre": "Ancestral Polynesian", "keywords": ["tiki carvings", "cultural vibrancy", "majestic islands", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "warm traditions", "spiritual connection"]},
    {"genre": "Carolingian", "keywords": ["illuminated manuscripts", "majestic castles", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "historic influence", "royal presence", "sacred art"]},
]

gods_styles = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Zeus (Greek)", "keywords": ["king of the gods", "thunderbolt", "supreme ruler", "sky god", "Greek mythology", "divine authority", "powerful presence", "ancient leadership", "royal god", "heavenly power"]},
    {"genre": "Hera (Greek)", "keywords": ["queen of the gods", "marriage goddess", "protector of women", "divine beauty", "majestic presence", "Greek mythology", "royal elegance", "family goddess", "sacred vows", "regal strength"]},
    {"genre": "Odin (Norse)", "keywords": ["allfather", "wisdom god", "rune magic", "Norse mythology", "one-eyed god", "warrior god", "ravens and wolves", "divine knowledge", "battle leadership", "sacrifice for wisdom"]},
    {"genre": "Frigg (Norse)", "keywords": ["queen of the gods", "mother goddess", "wisdom and love", "marriage protector", "fate weaver", "divine beauty", "Norse mythology", "sacred bond", "majestic grace", "protectress of families"]},
    {"genre": "Ra (Egyptian)", "keywords": ["sun god", "creator god", "Egyptian mythology", "solar disk", "heavenly ruler", "divine light", "day and night cycle", "ancient power", "eternal warmth", "celestial dominion"]},
    {"genre": "Isis (Egyptian)", "keywords": ["goddess of magic", "mother goddess", "Egyptian mythology", "divine wisdom", "protectress", "fertility goddess", "sacred healer", "eternal love", "mystical power", "queen of the gods"]},
    {"genre": "Brahma (Hindu)", "keywords": ["creator god", "four faces", "Hindu mythology", "divine intellect", "god of knowledge", "creator of the universe", "eternal being", "cosmic order", "supreme deity", "wisdom and creation"]},
    {"genre": "Vishnu (Hindu)", "keywords": ["preserver god", "eternal protector", "Hindu mythology", "blue-skinned god", "divine incarnations", "balance of the universe", "cosmic protector", "god of love", "majestic power", "eternal guardian"]},
    {"genre": "Shiva (Hindu)", "keywords": ["destroyer god", "transformation god", "Hindu mythology", "meditating deity", "god of destruction and regeneration", "divine ascetic", "dance of destruction", "cosmic energy", "transcendental presence", "divine force"]},
    {"genre": "Athena (Greek)", "keywords": ["goddess of wisdom", "warrior goddess", "Greek mythology", "strategic intellect", "peaceful strength", "protector of Athens", "shield and spear", "wise counselor", "divine justice", "virgin goddess"]},
    {"genre": "Aphrodite (Greek)", "keywords": ["goddess of love", "beauty goddess", "Greek mythology", "romantic allure", "eternal beauty", "divine love", "sensual charm", "golden goddess", "goddess of desire", "passion"]},
    {"genre": "Thor (Norse)", "keywords": ["thunder god", "mighty hammer", "Norse mythology", "god of storms", "warrior strength", "protector of mankind", "divine warrior", "battle fury", "stormbringer", "earth protector"]},
    {"genre": "Loki (Norse)", "keywords": ["trickster god", "shape-shifter", "Norse mythology", "mischievous god", "chaos bringer", "god of lies", "divine humor", "fiery presence", "god of discord", "deceiver"]},
    {"genre": "Anubis (Egyptian)", "keywords": ["god of the dead", "mummification", "Egyptian mythology", "guardian of the underworld", "afterlife protector", "divine guide", "jackal-headed god", "ritual protector", "god of transition", "sacred journey"]},
    {"genre": "Hades (Greek)", "keywords": ["god of the underworld", "Greek mythology", "ruler of the dead", "divine judge", "god of wealth", "dark domain", "eternal ruler", "silent power", "shadow god", "king of the underworld"]},
    {"genre": "Poseidon (Greek)", "keywords": ["god of the sea", "Greek mythology", "earth shaker", "trident god", "ocean ruler", "storm god", "protector of sailors", "divine power", "water deities", "majestic sea god"]},
    {"genre": "Demeter (Greek)", "keywords": ["goddess of the harvest", "earth goddess", "Greek mythology", "fertility goddess", "motherly love", "agriculture", "abundant nature", "cornucopia", "seasonal cycles", "nurturing presence"]},
    {"genre": "Hera (Greek)", "keywords": ["queen of the gods", "goddess of marriage", "family protector", "Greek mythology", "divine love", "sacred vows", "regal elegance", "maternal presence", "majestic queen", "royal charisma"]},
    {"genre": "Quetzalcoatl (Aztec)", "keywords": ["feathered serpent", "god of winds", "creator god", "Aztec mythology", "god of learning", "divine knowledge", "fertility god", "protector of humanity", "earth and sky balance", "ancient wisdom"]},
    {"genre": "Xochiquetzal (Aztec)", "keywords": ["goddess of love", "beauty goddess", "Aztec mythology", "flowers and fertility", "divine femininity", "goddess of joy", "ancient arts", "sensual charm", "passion", "embodiment of beauty"]},
    {"genre": "Marduk (Babylonian)", "keywords": ["god of storms", "Babylonian mythology", "creator god", "protector god", "god of order", "mighty warrior", "ancient strength", "ruler of heavens", "divine justice", "mesopotamian grandeur"]},    
    {"genre": "Ares (Greek)", "keywords": ["god of war", "Greek mythology", "battle frenzy", "violent strength", "warrior god", "divine conflict", "god of aggression", "battlefield dominance", "warrior's rage", "divine bloodlust"]},
    {"genre": "Athena (Greek)", "keywords": ["goddess of wisdom", "goddess of war", "Greek mythology", "strategic intellect", "virgin goddess", "battle tactics", "divine protector", "shield bearer", "strategic brilliance", "defender of Athens"]},
    {"genre": "Apollo (Greek)", "keywords": ["god of the sun", "Greek mythology", "god of music", "healing god", "archer god", "divine beauty", "sunlight radiance", "prophecy", "artistic genius", "golden radiance"]},
    {"genre": "Artemis (Greek)", "keywords": ["goddess of the hunt", "Greek mythology", "protector of animals", "moon goddess", "divine strength", "virgin goddess", "wilds and forests", "hunter's precision", "archery skills", "wild beauty"]},
    {"genre": "Hecate (Greek)", "keywords": ["goddess of magic", "witchcraft", "Greek mythology", "underworld goddess", "night goddess", "crossroads", "divine sorcery", "moon and shadow", "dark arts", "mysterious power"]},
    {"genre": "Horus (Egyptian)", "keywords": ["sky god", "Egyptian mythology", "god of kingship", "falcon-headed god", "protector of Egypt", "divine ruler", "god of the pharaohs", "solar deity", "heavenly ruler", "eternal vision"]},
    {"genre": "Set (Egyptian)", "keywords": ["god of chaos", "Egyptian mythology", "god of desert", "warrior god", "god of storms", "divine trickster", "god of violence", "protector of the underworld", "primal force", "god of disorder"]},
    {"genre": "Anubis (Egyptian)", "keywords": ["god of mummification", "Egyptian mythology", "protector of the dead", "jackal-headed god", "guide to the afterlife", "death and rebirth", "underworld deity", "guardian of tombs", "funeral god", "sacred protector"]},
    {"genre": "Bastet (Egyptian)", "keywords": ["goddess of home", "Egyptian mythology", "protector of women", "cat goddess", "divine beauty", "fertility goddess", "family protector", "goddess of music and dance", "joy and love", "nurturing presence"]},
    {"genre": "Tezcatlipoca (Aztec)", "keywords": ["god of night", "Aztec mythology", "creator god", "god of temptation", "god of the jaguar", "deity of conflict", "divine darkness", "trickster god", "god of fate", "mirror god"]},
    {"genre": "Tlaloc (Aztec)", "keywords": ["god of rain", "Aztec mythology", "god of fertility", "storm god", "god of agriculture", "divine power", "rain-bringer", "sacred water", "fertility deity", "earth’s nourishment"]},
    {"genre": "Quetzalcoatl (Aztec)", "keywords": ["feathered serpent", "god of winds", "creator god", "Aztec mythology", "god of learning", "divine knowledge", "fertility god", "protector of humanity", "earth and sky balance", "ancient wisdom"]},
    {"genre": "Mithras (Persian)", "keywords": ["god of light", "Persian mythology", "protector of truth", "god of contracts", "divine warrior", "bull slayer", "cosmic balance", "light vs dark", "deity of soldiers", "savior god"]},
    {"genre": "Zoroaster (Persian)", "keywords": ["prophet", "Persian religion", "founder of Zoroastrianism", "spiritual leader", "god of light", "divine wisdom", "sacred fire", "god of good", "eternal struggle", "divine truth"]},
    {"genre": "Freya (Norse)", "keywords": ["goddess of love", "Norse mythology", "goddess of beauty", "goddess of fertility", "warrior goddess", "divine wisdom", "valkyrie", "divine sensuality", "golden goddess", "magical allure"]},
    {"genre": "Tyr (Norse)", "keywords": ["god of war", "Norse mythology", "god of justice", "honor god", "brave warrior", "divine strength", "god of sacrifice", "guardian god", "sword of justice", "ancient power"]},
    {"genre": "Njord (Norse)", "keywords": ["god of the sea", "Norse mythology", "god of wealth", "sea god", "divine protector", "god of wind and sea", "coastal deity", "storm god", "navigator's deity", "oceanic ruler"]},
    {"genre": "Hel (Norse)", "keywords": ["goddess of the underworld", "Norse mythology", "daughter of Loki", "death goddess", "ruler of Helheim", "shadow goddess", "divine ruler of the dead", "dark domain", "underworld queen", "eternal ruler"]},
    {"genre": "Shiva (Hindu)", "keywords": ["god of destruction", "Hindu mythology", "god of transformation", "ascetic god", "divine dancer", "destroyer god", "regeneration", "cosmic god", "lord of destruction", "divine force"]},
    {"genre": "Kali (Hindu)", "keywords": ["goddess of destruction", "Hindu mythology", "mother goddess", "darkness goddess", "goddess of time", "warrior goddess", "divine power", "fierce energy", "goddess of death", "life and death cycle"]},
    {"genre": "Ganesh (Hindu)", "keywords": ["god of beginnings", "Hindu mythology", "elephant-headed god", "remover of obstacles", "wisdom god", "god of intellect", "divine patron of arts", "prosperity", "luck and good fortune", "protective deity"]},
]

hair_styles = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Buzz Cut", "keywords": ["short hair", "military style", "clean and sharp", "low maintenance", "close shave", "faded sides", "simple style", "minimalistic look", "bold", "rugged appearance"]},
    {"genre": "Pompadour Style", "keywords": ["high volume", "slicked back", "classic style", "retro look", "elevated front", "elegant", "vintage charm", "defined shape", "volume and height", "stylish sophistication"]},
    {"genre": "Undercut Style", "keywords": ["short sides", "long top", "sharp contrast", "modern style", "clean lines", "edgy", "versatile", "defined part", "sleek", "fashion-forward"]},
    {"genre": "Buzzed Fade", "keywords": ["fade", "gradual length", "close cut", "sharp lines", "textured top", "clean look", "slick sides", "low maintenance", "masculine", "neat appearance"]},
    {"genre": "Mullet Style", "keywords": ["short front", "long back", "retro", "business in the front", "party in the back", "classic style", "wild look", "bold fashion", "punk vibe", "nostalgic"]},
    {"genre": "Quiff Style", "keywords": ["voluminous front", "styled upward", "smooth finish", "elegant", "classic", "dapper", "stylish", "pomade style", "polished", "high-end look"]},
    {"genre": "Crew Cut Style", "keywords": ["short sides", "neat top", "military-inspired", "clean and simple", "no-nonsense", "classic look", "easy to maintain", "sharp", "low maintenance", "functional style"]},
    {"genre": "Bowl Cut", "keywords": ["round shape", "straight fringe", "retro style", "90s look", "uniform length", "unique", "distinctive", "nostalgic", "geometric", "precise cut"]},
    {"genre": "Side Part Style", "keywords": ["neat", "classic style", "side-swept", "timeless", "elegant", "professional look", "simple yet sophisticated", "longer top", "clean separation", "structured hair"]},
    {"genre": "Afro Style", "keywords": ["full volume", "curly", "natural", "bold style", "rounded shape", "defined curls", "retro", "big hair", "fuzzy", "statement look"]},
    {"genre": "Man Bun Style", "keywords": ["hair gathered", "tied back", "long hair", "neat style", "casual look", "stylish", "hipster", "bohemian", "relaxed vibe", "messy chic"]},
    {"genre": "Top Knot Style", "keywords": ["short sides", "long top", "hair tied up", "sleek", "casual", "modern", "messy style", "hipster look", "practical", "hair accessory"]},
    {"genre": "Layered Cut Style", "keywords": ["textured layers", "soft volume", "natural flow", "dynamic look", "flowing hair", "versatile", "shaped ends", "voluminous", "light movement", "fashionable"]},
    {"genre": "Bob Cut", "keywords": ["straight cut", "chin-length", "classic style", "blunt ends", "chic", "stylish", "easy to manage", "modern", "elegant", "timeless"]},
    {"genre": "Shag Cut Style", "keywords": ["textured layers", "messy look", "wild style", "uneven cut", "vintage", "rock and roll", "layered fringe", "voluminous", "edgy", "carefree style"]},
    {"genre": "Long Layers Style", "keywords": ["flowing hair", "natural look", "layered ends", "soft movement", "undone style", "long and elegant", "free-flowing", "timeless", "luscious", "effortless"]},
    {"genre": "Pixie Cut Style", "keywords": ["short hair", "feminine", "edgy", "easy maintenance", "playful", "youthful", "choppy style", "soft texture", "modern", "chic"]},
    {"genre": "Flat Top Style", "keywords": ["high volume", "flat crown", "sharp lines", "90s style", "boxy look", "bold", "defined edges", "geometric", "cool", "retro"]},
    {"genre": "French Crop Style", "keywords": ["short fringe", "clean sides", "textured top", "retro style", "stylish", "angular cut", "short and sharp", "defined lines", "masculine", "neat appearance"]},
    {"genre": "Caesar Cut Style", "keywords": ["short fringe", "forward-swept", "classic", "bold", "neat and tidy", "easy to manage", "simple", "geometric", "practical", "timeless style"]},
    {"genre": "Long Loose Waves", "keywords": ["soft waves", "flowing hair", "natural texture", "beachy look", "relaxed", "effortless beauty", "voluminous", "shiny", "romantic", "bohemian"]},
    {"genre": "Bob Cut2", "keywords": ["chin-length", "straight cut", "blunt ends", "classic", "stylish", "easy to manage", "modern", "chic", "timeless", "sleek"]},
    {"genre": "Pixie Cut", "keywords": ["short hair", "feminine", "choppy style", "playful", "youthful", "edgy", "textured", "easy maintenance", "bold", "chic"]},
    {"genre": "Layered Haircut", "keywords": ["textured layers", "soft flow", "dynamic movement", "light volume", "natural shape", "bouncy", "versatile", "feminine", "soft ends", "natural look"]},
    {"genre": "Shag Cut", "keywords": ["messy look", "rock and roll", "layered fringe", "voluminous", "uneven layers", "effortless", "edgy", "carefree style", "wild", "playful"]},
    {"genre": "Straight and Sleek", "keywords": ["silky straight", "shiny", "polished", "classic style", "smooth finish", "glossy hair", "clean lines", "minimalistic", "sleek elegance", "modern"]},
    {"genre": "Braided Crown", "keywords": ["crown braid", "intricate braids", "elegant", "bohemian style", "romantic", "vintage", "classic", "soft curls", "decorative", "princess-like"]},
    {"genre": "High Ponytail", "keywords": ["sleek ponytail", "high volume", "pulled back", "neat", "sporty", "elevated", "stylish", "glamorous", "dynamic", "youthful"]},
    {"genre": "Side-Swept Curls", "keywords": ["soft curls", "side part", "romantic", "elegant", "flirty", "chic", "voluminous", "shine", "classic curls", "sophisticated"]},
    {"genre": "Top Knot", "keywords": ["hair tied up", "messy bun", "casual", "boho chic", "relaxed", "high bun", "modern", "effortless", "stylish", "practical"]},
    {"genre": "Bangs with Long Hair", "keywords": ["fringe", "soft bangs", "long hair", "face-framing", "playful", "youthful", "elegant", "straight or textured", "modern", "feminine"]},
    {"genre": "Curtain Bangs", "keywords": ["soft fringe", "parted bangs", "vintage", "retro style", "gentle waves", "flowing", "timeless", "classic", "face-framing", "effortless"]},
    {"genre": "Messy Bun", "keywords": ["casual", "loose hair", "effortless", "relaxed", "chic", "messy look", "bohemian", "easy style", "natural", "laid-back"]},
    {"genre": "Afro", "keywords": ["curly hair", "full volume", "big hair", "natural curls", "bold", "textured", "defined curls", "retro", "afrocentric", "statement look"]},
    {"genre": "Long and Straight", "keywords": ["silky", "sleek", "minimalistic", "flowing", "glossy", "smooth", "healthy shine", "elegant", "straight cut", "long length"]},
    {"genre": "Half Up Half Down", "keywords": ["half ponytail", "loose hair", "relaxed", "romantic", "elegant", "casual chic", "flirty", "soft waves", "boho", "feminine"]},
    {"genre": "Tight Curls", "keywords": ["defined curls", "voluminous", "bouncy", "full curls", "playful", "tight ringlets", "chic", "natural texture", "bold", "classic curls"]},
    {"genre": "Undercut Bob", "keywords": ["undercut", "choppy bob", "bold style", "modern", "edgy", "creative cut", "sharp lines", "fashionable", "sophisticated", "stylish"]},
    {"genre": "Fishtail Braid", "keywords": ["braided style", "intricate", "elegant", "bohemian", "delicate", "classic", "textured", "sophisticated", "timeless", "chic"]},
    {"genre": "Choppy Lob", "keywords": ["lob cut", "textured ends", "messy", "layered", "easy style", "effortless", "modern", "choppy finish", "versatile", "youthful"]},
    {"genre": "Blonde Hair", "keywords": ["light blonde", "golden blonde", "platinum blonde", "ash blonde", "strawberry blonde", "sun-kissed", "warm blonde", "bright blonde", "silky shine", "blonde highlights"]},
    {"genre": "Brunette Hair", "keywords": ["dark brown", "chocolate brown", "light brown", "medium brown", "rich brunette", "chestnut", "caramel highlights", "natural brown", "deep brown", "warm undertones"]},
    {"genre": "Black Hair", "keywords": ["jet black", "dark black", "natural black", "midnight black", "shiny black", "deep black", "sleek black", "soft black", "glossy black", "sharp black"]},
    {"genre": "Red Hair", "keywords": ["fiery red", "cherry red", "auburn", "deep red", "bright red", "copper red", "ginger", "strawberry red", "intense red", "vivid red"]},
    {"genre": "Platinum Blonde Hair", "keywords": ["icy blonde", "silvery blonde", "frosted blonde", "cool blonde", "light platinum", "almost white blonde", "bleached blonde", "clear blonde", "extremely light blonde", "frosty sheen"]},
    {"genre": "Silver Hair", "keywords": ["gray hair", "silver strands", "aging gracefully", "platinum silver", "shiny gray", "frosty gray", "cool silver", "metallic silver", "snowy silver", "elegant silver"]},
    {"genre": "Ombre Hair", "keywords": ["gradient effect", "dark roots", "lighter tips", "blended shades", "sun-kissed ombre", "smooth transition", "ombre balayage", "light to dark", "natural fade", "subtle ombre"]},
    {"genre": "Burgundy Hair", "keywords": ["rich red", "dark red", "wine red", "burgundy hue", "deep burgundy", "vibrant burgundy", "reddish-brown", "warm burgundy", "berry tone", "luxury red"]},
    {"genre": "Pink Hair", "keywords": ["pastel pink", "bright pink", "cotton candy pink", "hot pink", "rose pink", "fuchsia", "magenta", "light pink", "vivid pink", "bold pink"]},
    {"genre": "Blue Hair", "keywords": ["turquoise hair", "sea blue", "electric blue", "pastel blue", "midnight blue", "royal blue", "aqua hair", "neon blue", "icy blue", "bold blue"]},
    {"genre": "Purple Hair", "keywords": ["lavender hair", "violet hair", "plum hair", "magenta hair", "lilac hair", "dark purple hair", "deep violet", "bold purple", "rich purple", "faded purple"]},
    {"genre": "Green Hair", "keywords": ["emerald hair", "mint green hair", "neon green hair", "grass green hair", "dark green hair", "forest green hair", "sea green hair", "bright green hair", "lime green hair", "electric green"]},
    {"genre": "Grey Hair", "keywords": ["silver grey hair", "stormy grey hair", "salt-and-pepper hair", "platinum grey", "charcoal grey hair", "steel grey", "cool grey", "soft grey", "shiny grey", "sophisticated grey"]},
    {"genre": "White Hair", "keywords": ["snow white hair", "pure white hair", "silver-white hair", "icy white hair", "ivory hair", "pearl white hair", "chalk white hair", "bright white hair", "frosted white hair", "blinding white"]},
    {"genre": "Brown Hair", "keywords": ["light brown hair", "dark brown hair", "medium brown hair", "rich brown hair", "warm brown hair", "coffee brown hair", "chocolate brown hair", "chestnut brown hair", "caramel brown hair", "earthy brown hair"]},
    {"genre": "Copper Hair", "keywords": ["burnt orange hair", "copper-red hair", "fiery copper hair", "rich copper hair", "copper highlights", "rust copper hair", "reddish copper hair", "bold copper hair", "copper shine", "vivid copper hair"]},
    {"genre": "Lavender Hair", "keywords": ["light lavender hair", "pastel lavender hair", "lavender purple hair", "light purple hair", "faded lavender hair", "soft lavender hair", "elegant lavender", "shiny lavender hair", "bright lavender hair", "delicate lavender"]},
    {"genre": "Yellow Hair", "keywords": ["bright yellow hair", "neon yellow hair", "yellow blonde hair", "golden yellow hair", "canary yellow hair", "lemon yellow hair", "sunshine yellow hair", "vivid yellow hair", "pale yellow hair", "yellow highlights"]},
    {"genre": "Orange Hair", "keywords": ["bright orange hair", "pumpkin orange hair", "fiery orange hair", "neon orange hair", "light orange hair", "dark orange hair", "burnt orange hair", "deep orange hair", "copper orange hair", "bold orange hair"]},
    {"genre": "Turquoise Hair", "keywords": ["aqua turquoise hair", "light turquoise hair", "dark turquoise hair", "neon turquoise hair", "vivid turquoise hair", "cool turquoise", "icy turquoise", "electric turquoise", "deep turquoise", "bold turquoise"]},
    {"genre": "Peach Hair", "keywords": ["soft peach hair", "light peach hair", "warm peach hair", "peachy tones", "peach blonde hair", "pastel peach hair", "peach highlights", "bright peach hair", "delicate peach", "sunset peach"]},
    {"genre": "Charcoal Hair", "keywords": ["dark charcoal hair", "grey charcoal hair", "light charcoal hair", "black charcoal hair", "steel charcoal hair", "smoky charcoal hair", "deep charcoal", "subtle charcoal hair", "charcoal highlights", "matte charcoal"]},
    {"genre": "Bronze Hair", "keywords": ["metallic bronze hair", "light bronze hair", "dark bronze hair", "rich bronze hair", "coppery bronze hair", "warm bronze hair", "brassy bronze", "shiny bronze", "luxurious bronze hair", "vivid bronze highlights"]},
    {"genre": "Pink Blonde Hair", "keywords": ["blonde pink hair", "rose gold blonde", "peach pink blonde", "light pink blonde", "subtle pink blonde", "blonde with pink highlights", "cool pink blonde", "warm pink blonde", "pastel pink blonde", "blush blonde hair"]},
]

human_hybride = [ 
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Cat-Human Hybrid", "keywords": ["sharp feline features", "slender build", "pointed ears", "tail", "agile movements", "whiskers", "cat-like eyes", "clawed hands", "graceful posture", "feline agility"]},
    {"genre": "Wolf-Human Hybrid", "keywords": ["fur-covered body", "canine features", "sharp fangs", "wolf-like eyes", "strong build", "pointed ears", "predatory stance", "muscular legs", "keen senses", "animalistic instincts"]},
    {"genre": "Bird-Human Hybrid", "keywords": ["feathered wings", "beak-like nose", "bird-like posture", "sharp eyes", "light build", "quick movements", "colorful feathers", "flying ability", "elongated limbs", "avian characteristics"]},
    {"genre": "Horse-Human Hybrid", "keywords": ["muscular legs", "horse-like features", "mane of hair", "tall stature", "hooves", "strong build", "powerful legs", "long neck", "speed and grace", "stable posture"]},
    {"genre": "Lion-Human Hybrid", "keywords": ["majestic mane", "muscular build", "lion-like eyes", "sharp claws", "royal posture", "ferocious stance", "feline grace", "strength and power", "large body", "noble presence"]},
    {"genre": "Snake-Human Hybrid", "keywords": ["slithering movements", "scaly skin", "forked tongue", "serpentine eyes", "long, flexible body", "reptilian features", "venomous fangs", "smooth posture", "predatory appearance", "stealthy movement"]},
    {"genre": "Tiger-Human Hybrid", "keywords": ["striped fur", "muscular build", "sharp claws", "tiger-like eyes", "agile movements", "ferocious demeanor", "orange fur", "prowling stance", "wild power", "predatory instincts"]},
    {"genre": "Bear-Human Hybrid", "keywords": ["large frame", "thick fur", "bear-like claws", "muscular arms", "powerful legs", "strong posture", "animal strength", "wide chest", "sturdy build", "protective nature"]},
    {"genre": "Fox-Human Hybrid", "keywords": ["fluffy tail", "pointed ears", "fox-like eyes", "agile movements", "cunning expression", "sharp features", "slender build", "quick reflexes", "bright fur", "mysterious presence"]},
    {"genre": "Shark-Human Hybrid", "keywords": ["sharp teeth", "scaly skin", "powerful build", "aquatic features", "fins", "sleek body", "sharp senses", "predatory behavior", "swimming abilities", "aquatic strength"]},
    {"genre": "Elephant-Human Hybrid", "keywords": ["large ears", "trunk", "massive build", "thick skin", "strong limbs", "gentle giant", "broad shoulders", "heavyset body", "sturdy presence", "elephant-like grace"]},
    {"genre": "Rabbit-Human Hybrid", "keywords": ["long ears", "small frame", "bunny-like features", "quick movements", "soft fur", "floppy ears", "large eyes", "small nose", "agile and fast", "cute appearance"]},
    {"genre": "Cheetah-Human Hybrid", "keywords": ["lean body", "muscular legs", "cheetah-like speed", "fast reflexes", "spotted fur", "graceful stride", "sharp claws", "predatory focus", "sleek build", "quick movements"]},
    {"genre": "Kangaroo-Human Hybrid", "keywords": ["powerful legs", "tail", "hopping movement", "muscular frame", "large feet", "kangaroo-like posture", "strong jumps", "agile body", "spring-like motions", "heightened reflexes"]},
    {"genre": "Gorilla-Human Hybrid", "keywords": ["large frame", "muscular arms", "thick fur", "powerful chest", "strong jawline", "dominant presence", "intelligent expression", "broad shoulders", "fierce demeanor", "primate features"]},
    {"genre": "Dragon-Human Hybrid", "keywords": ["scaled skin", "wings", "fire-breathing", "dragon-like claws", "long tail", "sharp teeth", "majestic wingspan", "powerful build", "fire powers", "reptilian features"]},
    {"genre": "Lizard-Human Hybrid", "keywords": ["scaly skin", "long tongue", "cold-blooded nature", "slender body", "quick movements", "reptilian eyes", "sharp claws", "creeping stance", "long tail", "predatory gaze"]},
    {"genre": "Bat-Human Hybrid", "keywords": ["bat-like wings", "sharp hearing", "nocturnal traits", "slim build", "black wings", "claw-like fingers", "sensitive hearing", "flying abilities", "dark presence", "sharp vision"]},
    {"genre": "Octopus-Human Hybrid", "keywords": ["tentacles", "aquatic features", "soft, flexible body", "sharp mind", "multifaceted eyes", "swimming abilities", "flexible limbs", "reaching appendages", "intelligent expression", "adaptable body"]},
    {"genre": "Frog-Human Hybrid", "keywords": ["webbed hands", "amphibian skin", "long limbs", "big eyes", "powerful jumps", "small, agile body", "slim figure", "greenish tones", "sticky hands", "hopping abilities"]},
    {"genre": "Panther-Human Hybrid", "keywords": ["sleek black fur", "predatory grace", "sharp claws", "agile movements", "panther-like eyes", "stealthy posture", "muscular legs", "night vision", "feline agility", "sinuous body"]},
    {"genre": "Rhino-Human Hybrid", "keywords": ["thick skin", "horned head", "muscular build", "powerful legs", "rough texture", "strong stature", "imposing presence", "broad shoulders", "heavy-set body", "rhino-like features"]},
    {"genre": "Mantis-Human Hybrid", "keywords": ["sharp limbs", "exquisite exoskeleton", "bug-like eyes", "insect-like posture", "quick reflexes", "powerful arms", "greenish tones", "praying mantis traits", "elongated limbs", "predatory stance"]},
    {"genre": "Crocodile-Human Hybrid", "keywords": ["scaly body", "sharp teeth", "powerful jaws", "long tail", "reptilian features", "water-dwelling traits", "broad body", "predator-like eyes", "muscular build", "fast reflexes"]},
    {"genre": "Swan-Human Hybrid", "keywords": ["graceful neck", "feathered wings", "white feathers", "elegant posture", "slender body", "long, fluid movements", "delicate wings", "beauty and grace", "serene expression", "avian characteristics"]},
    {"genre": "Zebra-Human Hybrid", "keywords": ["black and white stripes", "muscular build", "zebra-like eyes", "strong legs", "graceful movement", "striped fur", "herbivore traits", "slender build", "wild posture", "zebra-striped skin"]},
    {"genre": "Giraffe-Human Hybrid", "keywords": ["long neck", "tall frame", "elevated stance", "gentle expression", "large eyes", "spotted fur", "elegant movements", "powerful legs", "herbivore features", "graceful reach"]},
    {"genre": "Antelope-Human Hybrid", "keywords": ["slender body", "graceful movements", "horns", "athletic build", "long legs", "quick reflexes", "agile posture", "light footed", "smooth fur", "keen eyes"]},
    {"genre": "Lionfish-Human Hybrid", "keywords": ["flowing fins", "colorful patterns", "sharp spines", "fish-like gills", "aquatic features", "elegant stance", "scaly skin", "brightly colored patterns", "marine aesthetic", "swimming abilities"]},
    {"genre": "Hawk-Human Hybrid", "keywords": ["sharp beak", "feathered wings", "keen eyes", "muscular limbs", "swift movement", "predatory posture", "bird of prey features", "fast reflexes", "eagle-like features", "flying ability"]},
    {"genre": "Scorpion-Human Hybrid", "keywords": ["sharp pincers", "curved tail", "stinger", "scaly skin", "eight limbs", "fast, powerful strikes", "exoskeleton", "predatory features", "dangerous posture", "aggressive stance"]},
    {"genre": "Wolf-Spirit-Human Hybrid", "keywords": ["ethereal wolf features", "translucent fur", "mystical glow", "powerful aura", "spiritual connection", "supernatural presence", "strong body", "noble wolf-like features", "elemental power", "wild spirit"]},
    {"genre": "Beetle-Human Hybrid", "keywords": ["shiny carapace", "hard exoskeleton", "beetle-like legs", "sharp mandibles", "multifaceted eyes", "slender limbs", "heavy build", "quick scuttling movement", "insectoid traits", "armor-like appearance"]},
    {"genre": "Camel-Human Hybrid", "keywords": ["desert features", "hump", "thick skin", "powerful legs", "tough exterior", "camel-like posture", "long eyelashes", "adaptable features", "muscular legs", "survival traits"]},
    {"genre": "Otter-Human Hybrid", "keywords": ["water-loving", "slender body", "playful nature", "webbed hands", "short fur", "quick reflexes", "aquatic agility", "swimming traits", "graceful movements", "curious expression"]},
    {"genre": "Wolverine-Human Hybrid", "keywords": ["sharp claws", "fierce expression", "muscular build", "powerful jaws", "scruffy fur", "tenacious demeanor", "sturdy posture", "wild animal traits", "aggressive stance", "survival instincts"]},
    {"genre": "Chameleon-Human Hybrid", "keywords": ["color-changing skin", "camouflage ability", "reptilian features", "long tongue", "sharp vision", "slow movements", "high adaptability", "quiet presence", "climbing ability", "chameleon-like behavior"]},
    {"genre": "Penguin-Human Hybrid", "keywords": ["short legs", "flipper-like arms", "black and white feathers", "aquatic abilities", "social behavior", "fatty build", "slow movements", "cute expression", "penguin traits", "playful demeanor"]},
    {"genre": "Jaguar-Human Hybrid", "keywords": ["muscular build", "jaguar-like spots", "predatory grace", "strong limbs", "sharp claws", "intense focus", "fast reflexes", "stealthy movements", "feline traits", "wild energy"]},
    {"genre": "Cheetah-Spirit-Human Hybrid", "keywords": ["ethereal body", "glowing spots", "translucent fur", "supernatural speed", "pristine grace", "fast reflexes", "powerful legs", "wild spirit", "animal essence", "mystical power"]},
]

celestial_objects = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Planet Mercury", "keywords": ["smallest planet", "closest to the Sun", "no atmosphere", "extreme temperatures", "rocky surface"]},
    {"genre": "Planet Venus", "keywords": ["thick toxic atmosphere", "extreme greenhouse effect", "volcanic surface", "Earth's twin in size", "hottest planet"]},
    {"genre": "Planet Earth", "keywords": ["only planet with known life", "water-covered surface", "diverse ecosystems", "plate tectonics", "oxygen-rich atmosphere"]},
    {"genre": "Planet Mars", "keywords": ["red surface", "iron oxide", "thin atmosphere", "polar ice caps", "potential for human colonization"]},
    {"genre": "Planet Jupiter", "keywords": ["largest planet", "gas giant", "Great Red Spot storm", "many moons", "strong magnetic field"]},
    {"genre": "Planet Saturn", "keywords": ["iconic ring system", "gas giant", "many moons", "hydrogen-helium composition", "least dense planet"]},
    {"genre": "Planet Uranus", "keywords": ["ice giant", "tilted axis", "pale blue-green color", "methane clouds", "coldest planetary atmosphere"]},
    {"genre": "Planet Neptune", "keywords": ["farthest from the Sun", "deep blue color", "ice giant", "strong winds", "Great Dark Spot storm"]},
    {"genre": "Dwarf Planet Pluto", "keywords": ["part of the Kuiper Belt", "icy surface", "thin atmosphere", "eccentric orbit", "discovered in 1930"]},
    {"genre": "Exoplanet Proxima Centauri b", "keywords": ["orbits Proxima Centauri", "closest exoplanet to Earth", "potentially habitable", "rocky surface", "tidally locked"]},
    {"genre": "Exoplanet Kepler-452b", "keywords": ["Earth-like", "habitable zone", "potential for liquid water", "orbits a sun-like star", "distance: 1,400 light years"]},
    {"genre": "Exoplanet TRAPPIST-1e", "keywords": ["potentially habitable", "earth-sized", "three other Earth-like planets", "red dwarf star system", "liquid water possible"]},
    {"genre": "Planet Kepler-22b", "keywords": ["habitable zone", "Earth-like size", "potential for liquid water", "distant system", "orbiting a sun-like star"]},
    {"genre": "Moon Titan (Saturn)", "keywords": ["thick atmosphere", "methane lakes", "potential for life", "similar to early Earth", "cold and toxic environment"]},
    {"genre": "Moon Europa (Jupiter)", "keywords": ["ice-covered ocean", "potential for life", "tidally locked", "subs surface water", "discovered by Galileo"]},
    {"genre": "Moon Io (Jupiter)", "keywords": ["volcanic activity", "sulfuric surface", "most active body", "many volcanoes", "intense radiation"]},
    {"genre": "Moon Callisto (Jupiter)", "keywords": ["heavily cratered surface", "thin atmosphere", "potential for water ice", "potential for human exploration", "old surface"]},
    {"genre": "Moon Enceladus (Saturn)", "keywords": ["icy geysers", "subsurface ocean", "potential for life", "tidally heated", "reflective surface"]},
    {"genre": "Moon Ganymede (Jupiter)", "keywords": ["largest moon", "subsurface ocean", "magnetic field", "ancient surface", "frozen landscape"]},
    {"genre": "Galaxy Andromeda", "keywords": ["nearest spiral galaxy", "2.5 million light-years away", "will collide with Milky Way", "1 trillion stars", "visible in the night sky"]},
    {"genre": "Galaxy Milky Way", "keywords": ["home galaxy", "contains Earth", "200 billion stars", "spiral galaxy", "center contains a black hole"]},
    {"genre": "Galaxy Triangulum", "keywords": ["third-largest in Local Group", "spiral galaxy", "M33", "closest to Andromeda", "contains stars and nebulae"]},
    {"genre": "Galaxy Whirlpool (M51)", "keywords": ["spiral galaxy", "interacting with NGC 5195", "distinctive structure", "star formation", "observed by Hubble"]},
    {"genre": "Galaxy Messier 87", "keywords": ["giant elliptical galaxy", "contains a supermassive black hole", "located in Virgo cluster", "1,500,000 light years away", "contains hot gas"]},
    {"genre": "Galaxy Sombrero", "keywords": ["edge-on spiral galaxy", "distinctive hat-like appearance", "located in Virgo cluster", "large central bulge", "star formation"]},
    {"genre": "Galaxy Centaurus A", "keywords": ["elliptical galaxy", "radio galaxy", "one of the closest active galaxies", "contains a supermassive black hole", "formed from a merger"]},
    {"genre": "Galaxy NGC 1300", "keywords": ["barred spiral galaxy", "located 61 million light-years away", "observable in the Eridanus constellation", "distinctive spiral arms", "star formation regions"]},
    {"genre": "Galaxy NGC 224 (M31)", "keywords": ["Andromeda galaxy", "closest large galaxy to Milky Way", "will merge with Milky Way", "contains over 1 trillion stars", "visible to the naked eye"]},
    {"genre": "Galaxy IC 1101", "keywords": ["largest known galaxy", "located in the Abell 2029 galaxy cluster", "1.04 billion light-years away", "elliptical galaxy", "contains trillion stars"]},
    {"genre": "Galaxy NGC 2997", "keywords": ["spiral galaxy", "located in the constellation Antlia", "visible in southern hemisphere", "star formation", "close to Milky Way"]},
    {"genre": "Galaxy NGC 1365", "keywords": ["barred spiral galaxy", "located in Fornax cluster", "observed by Hubble", "active star formation", "distorted shape"]},
    {"genre": "Orion Nebula", "keywords": ["brightest nebula", "located in the Orion constellation", "star formation region", "visible to the naked eye", "gas and dust clouds", "birthplace of stars"]},
]

monsters = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Vampire", "keywords": ["bloodsucker", "undead", "night", "immortal", "bite", "fangs", "transformation", "coffin", "mythology", "gothic"]},
    {"genre": "Werewolf", "keywords": ["shapeshifter", "full moon", "lycanthropy", "beast", "howl", "night", "hunting", "supernatural", "curse", "furry"]},
    {"genre": "Zombie", "keywords": ["undead", "reanimated", "flesh-eating", "apocalypse", "virus", "decay", "walking dead", "rotting", "shambling", "horde"]},
    {"genre": "Ghost", "keywords": ["spirit", "haunted", "supernatural", "apparition", "poltergeist", "specter", "translucent", "paranormal", "unfinished business", "revenge"]},
    {"genre": "Demon", "keywords": ["evil", "hell", "fire", "dark magic", "possession", "horns", "claws", "supernatural", "underworld", "sinister"]},
    {"genre": "Dragon", "keywords": ["fire-breathing", "winged", "scaly", "fantasy", "mythology", "hoarding treasure", "immense", "legendary", "powerful", "ancient"]},
    {"genre": "Frankenstein's Monster", "keywords": ["mad scientist", "reanimated", "unnatural", "patchwork", "bolts", "horror", "creation", "Victor Frankenstein", "monster", "clumsy"]},
    {"genre": "Kraken", "keywords": ["sea monster", "tentacles", "myth", "ocean", "giant", "swallow ships", "legendary", "deep sea", "fear", "tremendous"]},
    {"genre": "Chupacabra", "keywords": ["blood-sucking", "creature", "Latin America", "goat sucker", "night stalker", "alien-like", "vampire", "myth", "mysterious", "cryptid"]},
    {"genre": "Bigfoot", "keywords": ["Sasquatch", "forest", "mysterious", "cryptid", "large footprints", "hairy", "legend", "North America", "elusive", "wild"]},
    {"genre": "Mummy", "keywords": ["ancient Egypt", "curse", "wrapped in bandages", "undead", "resurrected", "tomb", "pharaoh", "sands", "spells", "mystery"]},
    {"genre": "Yeti", "keywords": ["abominable snowman", "mountain", "snow", "cryptid", "large footprints", "hairy", "elusive", "mysterious", "Himalayas", "cold"]},
    {"genre": "Vampire Bat", "keywords": ["flying", "bloodsucker", "night", "creature", "winged", "nocturnal", "bite", "vampire", "dangerous", "small"]},
    {"genre": "Gorgon", "keywords": ["medusa", "snake hair", "stone gaze", "mythology", "Greek", "turn to stone", "horror", "monster", "legend", "ancient"]},
    {"genre": "Chimera", "keywords": ["mythology", "Greek", "lion head", "serpent tail", "goat body", "fire-breathing", "monster", "creature", "hybrid", "dangerous"]},
    {"genre": "Lich", "keywords": ["undead wizard", "necromancer", "immortal", "dark magic", "skeleton", "sorcery", "curse", "zombie army", "evil", "ancient"]},
    {"genre": "Banshee", "keywords": ["female spirit", "wailing", "death omen", "Irish mythology", "ghost", "screeching", "haunting", "curse", "revenge", "legend"]},
    {"genre": "Giant", "keywords": ["huge", "colossal", "strength", "mythology", "beast", "tall", "supernatural", "legendary", "mighty", "creature"]},
    {"genre": "Hydra", "keywords": ["multi-headed", "Greek mythology", "immortal", "water serpent", "regeneration", "dangerous", "beast", "creature", "mythical", "slaying"]},
    {"genre": "Manticore", "keywords": ["lion body", "human face", "scorpion tail", "dangerous", "mythical", "Persian mythology", "creature", "venomous", "beast", "legend"]},
    {"genre": "Wendigo", "keywords": ["spirit", "cannibalism", "North American legend", "snow", "evil", "monster", "human-like", "flesh-eating", "cold", "supernatural"]},
    {"genre": "Griffin", "keywords": ["eagle", "lion", "wings", "mythology", "legendary", "creature", "protector", "fantasy", "royalty", "symbolic"]},
    {"genre": "Zombie Dog", "keywords": ["undead", "pet", "rotting", "dangerous", "creature", "attack", "horror", "decay", "hunting", "monstrous"]},
    {"genre": "Mothman", "keywords": ["winged", "cryptid", "red eyes", "mysterious", "ominous", "supernatural", "creature", "sightings", "legend", "danger"]},
    {"genre": "Slenderman", "keywords": ["tall", "faceless", "shadow", "urban legend", "slender", "supernatural", "creature", "haunting", "mystery", "ominous"]},
    {"genre": "Dullahan", "keywords": ["headless rider", "Irish mythology", "ghost", "death", "legend", "reaper", "skeleton", "rider", "haunting", "supernatural"]},
    {"genre": "The Headless Horseman", "keywords": ["horseback", "headless", "ghost", "legend", "night rider", "haunting", "evil", "supernatural", "Halloween", "headless"]},
    {"genre": "The Beast of Gévaudan", "keywords": ["cryptid", "French legend", "wolf-like", "predator", "mysterious", "hunting", "dangerous", "myth", "attack", "fear"]},
    {"genre": "The Jersey Devil", "keywords": ["cryptid", "New Jersey", "creature", "hooves", "horns", "wings", "myth", "evil", "mysterious", "flying"]},
    {"genre": "The Loveland Frogman", "keywords": ["cryptid", "frog-like", "Ohio", "humanoid", "swamp", "myth", "legend", "mysterious", "creature", "reptilian"]},
    {"genre": "The Flatwoods Monster", "keywords": ["cryptid", "alien", "West Virginia", "green", "spooky", "legend", "mysterious", "fear", "glowing eyes", "creature"]},
]

wonders_of_the_world = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Great Pyramid of Giza", "keywords": ["ancient", "Egypt", "pyramid", "monument", "stone", "tomb", "Pharaoh", "landmark", "wonders of the world", "historical"]},
    {"genre": "Hanging Gardens of Babylon", "keywords": ["ancient", "Babylon", "garden", "mesopotamia", "irrigation", "myth", "Hanging Gardens", "king", "historical", "legendary"]},
    {"genre": "Statue of Zeus at Olympia", "keywords": ["Greece", "statue", "zeus", "Olympia", "ancient", "god", "temple", "mythology", "Greece", "historical"]},
    {"genre": "Temple of Artemis at Ephesus", "keywords": ["ancient", "temple", "Artemis", "Greece", "Ephesus", "religious", "monument", "historical", "wonders of the world", "pagan"]},
    {"genre": "Mausoleum at Halicarnassus", "keywords": ["tomb", "ancient", "Mausolus", "Greece", "historical", "royalty", "monument", "Halicarnassus", "mausoleum", "architecture"]},
    {"genre": "Colossus of Rhodes", "keywords": ["statue", "ancient", "Rhodes", "Greek", "giant", "harbor", "symbol", "historical", "wonders of the world", "sculpture"]},
    {"genre": "Lighthouse of Alexandria", "keywords": ["lighthouse", "ancient", "Alexandria", "Egypt", "maritime", "monument", "harbor", "historical", "wonders of the world", "navigation"]},
    {"genre": "Great Wall of China", "keywords": ["China", "wall", "ancient", "fortification", "defense", "historical", "military", "landmark", "symbol", "longest wall"]},
    {"genre": "Petra", "keywords": ["Jordan", "ancient", "city", "rock-cut", "architecture", "historical", "monuments", "lost city", "desert", "UNESCO World Heritage"]},
    {"genre": "Christ the Redeemer", "keywords": ["Brazil", "statue", "Christ", "Rio de Janeiro", "monument", "Christianity", "historical", "iconic", "landmark", "religion"]},
    {"genre": "Machu Picchu", "keywords": ["Peru", "Inca", "mountain", "ancient", "lost city", "historical", "temples", "architecture", "UNESCO World Heritage", "exploration"]},
    {"genre": "Chichen Itza", "keywords": ["Mexico", "Mayan", "pyramid", "historical", "temple", "ancient", "ruins", "civilization", "Mesoamerican", "archaeological site"]},
    {"genre": "Roman Colosseum", "keywords": ["Italy", "Rome", "amphitheater", "ancient", "arena", "gladiators", "historical", "Roman Empire", "landmark", "theater"]},
    {"genre": "Taj Mahal", "keywords": ["India", "mausoleum", "love", "white marble", "monument", "historical", "Mughal architecture", "UNESCO World Heritage", "India", "romantic"]},
    {"genre": "Colosseum of Rome", "keywords": ["Italy", "Rome", "amphitheater", "gladiators", "ancient", "historical", "Roman Empire", "arena", "tourist attraction", "landmark"]},
    {"genre": "Eiffel Tower", "keywords": ["France", "Paris", "iron", "landmark", "architecture", "tourist attraction", "symbol", "modern", "France", "famous"]},
    {"genre": "Sydney Opera House", "keywords": ["Australia", "Sydney", "architecture", "opera", "building", "modern", "famous", "landmark", "theater", "cultural"]},
    {"genre": "Great Barrier Reef", "keywords": ["Australia", "coral reef", "marine", "ecosystem", "ocean", "nature", "UNESCO World Heritage", "diving", "tourism", "wildlife"]},
    {"genre": "Stonehenge", "keywords": ["England", "monument", "stones", "mystery", "ancient", "circle", "historical", "prehistoric", "UNESCO World Heritage", "archaeology"]},
    {"genre": "Mount Everest", "keywords": ["Nepal", "mountain", "highest peak", "climbing", "Himalayas", "nature", "world landmark", "adventure", "altitude", "geography"]},
    {"genre": "Grand Canyon", "keywords": ["USA", "natural wonder", "canyon", "geography", "landmark", "Arizona", "nature", "landscape", "scenic", "tourism"]},
    {"genre": "Yellowstone National Park", "keywords": ["USA", "geothermal", "nature", "park", "wildlife", "landscape", "nature reserve", "waterfalls", "geysers", "tourism"]},
]

actions_styles = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Singing", "keywords": ["vocal performance", "melody", "lyrics", "stage presence", "opera", "choir", "karaoke", "harmonizing", "concert", "musical expression"]},
    {"genre": "Dancing", "keywords": ["movement", "rhythm", "ballet", "hip-hop", "salsa", "freestyle", "performance", "choreography", "grace", "entertainment"]},
    {"genre": "Eating", "keywords": ["chewing", "food consumption", "mealtime", "appetite", "tasting", "snacking", "cuisine", "enjoyment", "dining", "nutrition"]},
    {"genre": "Walking", "keywords": ["strolling", "steps", "leisurely pace", "hiking", "movement", "outdoor", "foot travel", "exercise", "pathway", "relaxation"]},
    {"genre": "Running", "keywords": ["sprinting", "jogging", "exercise", "marathon", "speed", "endurance", "track", "training", "cardio", "outdoor"]},
    {"genre": "Swimming", "keywords": ["water movement", "freestyle", "backstroke", "diving", "laps", "pool", "ocean", "exercise", "aquatic", "recreation"]},
    {"genre": "Reading", "keywords": ["book", "literature", "novel", "study", "comprehension", "focus", "library", "quiet", "learning", "entertainment"]},
    {"genre": "Writing", "keywords": ["penmanship", "typing", "journaling", "storytelling", "notes", "creative", "literature", "essays", "imagination", "expression"]},
    {"genre": "Drawing", "keywords": ["sketching", "illustration", "pencil", "art", "creativity", "design", "doodling", "coloring", "portrait", "imagination"]},
    {"genre": "Painting", "keywords": ["canvas", "art", "colors", "brush", "oil painting", "abstract", "landscape", "creativity", "expression", "masterpiece"]},
    {"genre": "Cooking", "keywords": ["meal preparation", "ingredients", "recipe", "kitchen", "chef", "baking", "flavor", "dishes", "sauce", "culinary"]},
    {"genre": "Driving", "keywords": ["car", "road", "transport", "steering", "speed", "journey", "highway", "traffic", "navigation", "vehicle"]},
    {"genre": "Cycling", "keywords": ["bicycle", "pedaling", "exercise", "outdoor", "road", "speed", "trail", "helmet", "fitness", "adventure"]},
    {"genre": "Jumping", "keywords": ["leaping", "vertical motion", "exercise", "sports", "skipping", "bounding", "energy", "trampoline", "fun", "movement"]},
    {"genre": "Climbing", "keywords": ["mountain", "rock", "harness", "outdoor", "adventure", "strength", "exercise", "ascent", "altitude", "challenge"]},
    {"genre": "Listening", "keywords": ["music", "conversation", "audio", "focus", "understanding", "speech", "learning", "relaxation", "ears", "attention"]},
    {"genre": "Talking", "keywords": ["conversation", "speech", "communication", "interaction", "dialogue", "discussion", "expression", "language", "voice", "exchange"]},
    {"genre": "Meditating", "keywords": ["calm", "relaxation", "mindfulness", "yoga", "focus", "inner peace", "breathing", "spiritual", "awareness", "tranquility"]},
    {"genre": "Fishing", "keywords": ["outdoor", "rod", "bait", "lake", "catch", "hobby", "recreation", "water", "casting", "patience"]},
    {"genre": "Gardening", "keywords": ["plants", "soil", "watering", "seeds", "flowers", "vegetables", "outdoor", "nature", "growth", "cultivation"]},
]

combat_actions = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Punching", "keywords": ["strike", "fist", "forceful hit", "close combat", "boxing", "self-defense", "aggression", "uppercut", "jab", "physical attack"]},
    {"genre": "Kicking", "keywords": ["leg strike", "martial arts", "high kick", "roundhouse", "defense", "agility", "attack", "forceful blow", "front kick", "close combat"]},
    {"genre": "Pointing Gun", "keywords": ["aiming", "targeting", "weapon control", "threat", "intimidation", "precision", "firearm", "stance", "focus", "defensive positioning"]},
    {"genre": "Shooting Gun", "keywords": ["firearm discharge", "bullet", "target hit", "precision", "recoil", "self-defense", "offense", "tactical action", "lethal force", "long-range attack"]},
    {"genre": "Dodging", "keywords": ["evasion", "quick movement", "avoiding strike", "reflexes", "agility", "self-defense", "reaction time", "escape", "close combat maneuver", "defensive"]},
    {"genre": "Blocking", "keywords": ["defense", "shielding", "impact absorption", "hand-to-hand combat", "martial arts", "counter move", "forearm block", "stance", "protection", "physical barrier"]},
    {"genre": "Grappling", "keywords": ["wrestling", "close combat", "submission hold", "takedown", "control", "martial arts", "self-defense", "chokehold", "pinning", "ground fighting"]},
    {"genre": "Throwing", "keywords": ["projectile", "forceful motion", "combat maneuver", "weapon use", "quick action", "disarming", "tactical", "strength", "improvised weapon", "distance"]},
    {"genre": "Slashing", "keywords": ["bladed weapon", "sword combat", "quick motion", "close quarters", "self-defense", "cutting attack", "sharp blade", "lethal action", "precision", "knife combat"]},
    {"genre": "Stabbing", "keywords": ["knife attack", "direct motion", "penetrating blow", "close quarters", "lethal strike", "bladed weapon", "self-defense", "aggression", "precision", "sharp object"]},
    {"genre": "Esquive", "keywords": ["sidestepping", "avoiding attacks", "tactical movement", "reflexes", "close combat", "counter-strategy", "defense", "agility", "quick reaction", "dodging strikes"]},
    {"genre": "Crouching", "keywords": ["lowering body", "combat stance", "defense", "concealment", "dodging", "quick reaction", "balance", "close quarters", "movement preparation", "evasion"]},
    {"genre": "Lying on Ground", "keywords": ["prone position", "defensive posture", "combat evasion", "concealment", "ground fighting", "reaction", "self-defense", "tactical movement", "low profile", "survival"]},
    {"genre": "Elbow Strike", "keywords": ["close combat", "forceful blow", "martial arts", "self-defense", "sharp impact", "quick attack", "aggression", "short range", "upper body strike", "physical attack"]},
    {"genre": "Knee Strike", "keywords": ["close combat", "martial arts", "lower body strike", "quick impact", "self-defense", "aggression", "short range", "tactical maneuver", "body blow", "forceful attack"]},
    {"genre": "Disarming", "keywords": ["weapon removal", "tactical action", "self-defense", "close combat", "disabling attacker", "precision", "reflexes", "hand-to-hand combat", "martial arts", "weapon control"]},
    {"genre": "Parrying", "keywords": ["weapon deflection", "swordplay", "countering attack", "martial arts", "reflexes", "self-defense", "close combat", "bladed weapon", "quick reaction", "defensive maneuver"]},
    {"genre": "Spinning Kick", "keywords": ["martial arts", "high impact", "circular motion", "close combat", "self-defense", "agility", "attack", "target hit", "flashy move", "powerful blow"]},
    {"genre": "Choking", "keywords": ["submission hold", "self-defense", "close quarters", "lethal action", "martial arts", "grappling", "control", "aggression", "combat maneuver", "tactical"]},
    {"genre": "Weapon Reloading", "keywords": ["firearm action", "tactical maneuver", "preparation", "precision", "combat readiness", "self-defense", "ammunition", "quick action", "lethal force", "weapon control"]},
]

professions = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Software Developer", "keywords": ["coding", "programming", "problem-solving", "technology", "innovation", "debugging", "collaboration", "system design", "software creation", "technical expertise"]},
    {"genre": "Doctor", "keywords": ["medical care", "health", "diagnosis", "treatment", "healing", "patient care", "emergency response", "surgery", "compassion", "lifesaving"]},
    {"genre": "Teacher", "keywords": ["education", "instruction", "learning", "guidance", "classroom", "mentorship", "lesson planning", "students", "knowledge", "communication"]},
    {"genre": "Chef", "keywords": ["cooking", "culinary arts", "recipes", "food preparation", "creativity", "kitchen management", "flavors", "presentation", "gourmet", "restaurant"]},
    {"genre": "Police Officer", "keywords": ["law enforcement", "public safety", "patrol", "crime prevention", "investigation", "protection", "justice", "discipline", "community service", "security"]},
    {"genre": "Artist", "keywords": ["creativity", "painting", "sculpting", "expression", "imagination", "design", "color theory", "visual arts", "gallery", "aesthetics"]},
    {"genre": "Musician", "keywords": ["performance", "music", "instrument", "singing", "composing", "melody", "rhythm", "creativity", "entertainment", "studio recording"]},
    {"genre": "Writer", "keywords": ["storytelling", "creative writing", "literature", "editing", "novels", "imagination", "publishing", "articles", "narrative", "language"]},
    {"genre": "Farmer", "keywords": ["agriculture", "crop cultivation", "livestock", "sustainability", "land management", "harvesting", "rural life", "organic farming", "soil", "food production"]},
    {"genre": "Construction Worker", "keywords": ["building", "construction", "tools", "manual labor", "safety", "blueprints", "infrastructure", "engineering", "physical work", "teamwork"]},
    {"genre": "Pilot", "keywords": ["aviation", "airplane", "navigation", "flying", "travel", "cockpit", "airline", "precision", "aerodynamics", "global transportation"]},
    {"genre": "Nurse", "keywords": ["medical care", "patient assistance", "healthcare", "compassion", "emergency response", "hospitals", "treatment", "healing", "support", "public health"]},
    {"genre": "Scientist", "keywords": ["research", "experiments", "innovation", "analysis", "discovery", "laboratory", "hypothesis", "theory", "data", "problem-solving"]},
    {"genre": "Photographer", "keywords": ["photography", "camera", "composition", "lighting", "creativity", "editing", "visual storytelling", "moments", "artistic", "portfolio"]},
    {"genre": "Athlete", "keywords": ["sports", "training", "competition", "fitness", "dedication", "teamwork", "discipline", "achievement", "performance", "physical excellence"]},
    {"genre": "Librarian", "keywords": ["books", "organization", "cataloging", "information", "knowledge", "research", "archives", "quiet", "education", "community"]},
    {"genre": "Mechanic", "keywords": ["automotive", "repairs", "engines", "tools", "diagnostics", "maintenance", "vehicles", "manual skills", "technical", "precision"]},
    {"genre": "Electrician", "keywords": ["wiring", "electricity", "installation", "safety", "repairs", "circuitry", "energy", "lighting", "power systems", "technical work"]},
    {"genre": "Barber", "keywords": ["haircutting", "styling", "grooming", "shaving", "creativity", "personal care", "clippers", "salon", "customer service", "appearance"]},
    {"genre": "Architect", "keywords": ["design", "blueprints", "structures", "creativity", "planning", "engineering", "urban development", "artistic vision", "construction", "spatial awareness"]},
    {"genre": "Paramedic", "keywords": ["emergency response", "medical aid", "ambulance", "first aid", "life-saving", "healthcare", "rescue", "trauma care", "compassion", "crisis management"]},
    {"genre": "Actor", "keywords": ["performance", "drama", "film", "stage", "theater", "character", "entertainment", "expression", "storytelling", "creativity"]},
    {"genre": "Firefighter", "keywords": ["rescue", "fire safety", "emergency response", "public safety", "teamwork", "bravery", "equipment", "protection", "lifesaving", "community"]},
    {"genre": "Journalist", "keywords": ["news", "reporting", "writing", "investigation", "truth", "stories", "editing", "media", "interviews", "communication"]},
    {"genre": "Lawyer", "keywords": ["legal advice", "courtroom", "contracts", "justice", "litigation", "negotiation", "laws", "ethics", "advocacy", "representation"]},
    {"genre": "Veterinarian", "keywords": ["animal care", "medical treatment", "pets", "compassion", "diagnosis", "surgery", "health", "livestock", "healing", "biology"]},
    {"genre": "Plumber", "keywords": ["pipes", "repairs", "water systems", "installation", "plumbing", "maintenance", "tools", "technical skills", "home systems", "sanitation"]},
    {"genre": "Detective", "keywords": ["investigation", "mystery", "clues", "evidence", "crime-solving", "analysis", "surveillance", "interviews", "deduction", "justice"]},
    {"genre": "Entrepreneur", "keywords": ["business", "startups", "innovation", "leadership", "strategy", "finance", "creativity", "risk-taking", "vision", "growth"]},
    {"genre": "Carpenter", "keywords": ["woodworking", "tools", "craftsmanship", "construction", "furniture", "repairs", "creativity", "manual skills", "design", "building"]},
]

time_periods = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Before Christ (BC)", "keywords": ["ancient history", "prehistoric", "early civilizations", "stone age", "bronze age", "iron age", "classical era", "ancient empires", "archaeology", "mythology"]},
    {"genre": "During Christ's Life", "keywords": ["Roman Empire", "ancient Judea", "Christianity origins", "historical Jesus", "religion", "early disciples", "biblical events", "Middle East", "ancient culture", "spiritual awakening"]},
    {"genre": "After Christ's Death (AD)", "keywords": ["Roman Empire", "early Christianity", "medieval period", "church influence", "religious expansion", "European history", "cultural shifts", "Middle Ages", "theological developments", "historical evolution"]},
    {"genre": "Middle Ages", "keywords": ["feudalism", "castles", "knights", "Black Death", "crusades", "chivalry", "medieval society", "monasteries", "religious wars", "European history"]},
    {"genre": "Renaissance", "keywords": ["rebirth", "art", "science", "invention", "humanism", "Da Vinci", "Michelangelo", "literature", "enlightenment", "cultural revolution"]},
    {"genre": "Industrial Revolution", "keywords": ["steam power", "factories", "innovation", "mechanization", "urbanization", "economic growth", "technological advancements", "19th century", "industry", "modernization"]},
    {"genre": "World War I", "keywords": ["global conflict", "trench warfare", "1914-1918", "alliances", "military history", "Versailles Treaty", "European powers", "industrialized warfare", "political shifts", "Great War"]},
    {"genre": "Interwar Period", "keywords": ["1920s", "1930s", "economic depression", "cultural changes", "League of Nations", "totalitarian regimes", "global tensions", "modern art", "jazz age", "political unrest"]},
    {"genre": "World War II", "keywords": ["global conflict", "Axis vs Allies", "1939-1945", "Holocaust", "D-Day", "atomic bomb", "military strategy", "genocide", "war crimes", "global impact"]},
    {"genre": "Post-War Era", "keywords": ["Cold War", "1950s", "economic recovery", "space race", "nuclear age", "civil rights movements", "globalization", "social changes", "modernization", "UN establishment"]},
    {"genre": "1960s", "keywords": ["counterculture", "civil rights", "space exploration", "Vietnam War", "cultural revolution", "social activism", "rock and roll", "political movements", "technological growth", "global tension"]},
    {"genre": "1980s", "keywords": ["Cold War tension", "Reaganomics", "personal computers", "pop culture", "fall of Berlin Wall", "global markets", "media boom", "MTV", "technological rise", "economic shifts"]},
    {"genre": "Modern Era (2000s)", "keywords": ["globalization", "internet revolution", "terrorism", "climate change", "smartphones", "social media", "space exploration", "economic challenges", "technology-driven society", "cultural shifts"]},
    {"genre": "2025", "keywords": ["current era", "sustainability", "technology advancements", "post-pandemic", "space travel", "AI growth", "climate action", "global cooperation", "economic recovery", "cultural evolution"]},
    {"genre": "2050s", "keywords": ["future society", "AI dominance", "space colonization", "sustainability breakthroughs", "climate solutions", "technological singularity", "globalization", "human evolution", "medical advancements", "global challenges"]},
    {"genre": "2100s", "keywords": ["next century", "global unity", "technological utopia", "space habitation", "climate stability", "extended lifespan", "AI integration", "post-human age", "advanced medicine", "interstellar exploration"]},
    {"genre": "2300s", "keywords": ["far future", "galactic expansion", "energy mastery", "cultural fusion", "new species interaction", "sustainable planets", "global peace", "AI-human coexistence", "quantum technology", "terraforming"]},
    {"genre": "2500s", "keywords": ["post-terrestrial era", "deep space exploration", "universal communication", "immortality research", "galactic governance", "universal culture", "resource abundance", "time travel experiments", "quantum AI", "intergalactic diplomacy"]},
    {"genre": "3000s", "keywords": ["future civilization", "advanced technology", "unified galaxy", "post-human evolution", "universal consciousness", "infinite energy", "quantum existence", "AI-guided societies", "interstellar travel", "unprecedented achievements"]},
    {"genre": "Timeless Era", "keywords": ["eternity", "philosophical concepts", "spiritual transcendence", "mythical dimensions", "universal truths", "boundless possibilities", "existence continuum", "infinite universe", "cultural eternity", "universal legacy"]},
]

biblical_moments = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Creation of the World", "keywords": ["Genesis", "Adam and Eve", "Garden of Eden", "creation story", "beginning of time", "seven days", "God's creation", "original sin", "serpent", "fall of man"]},
    {"genre": "The Great Flood", "keywords": ["Noah's Ark", "worldwide flood", "divine judgment", "covenant with Noah", "animals two by two", "rainbow promise", "salvation", "obedience to God", "ark construction", "renewed earth"]},
    {"genre": "Tower of Babel", "keywords": ["Genesis", "human pride", "language confusion", "scattered nations", "divine intervention", "Babylon", "tower construction", "unity in disobedience", "divine judgment", "ancient history"]},
    {"genre": "Exodus and Parting of the Red Sea", "keywords": ["Moses", "Israelite freedom", "Pharaoh", "divine miracles", "plagues of Egypt", "Exodus", "parting waters", "God's guidance", "pillar of fire", "Mount Sinai"]},
    {"genre": "Ten Commandments", "keywords": ["Moses", "Mount Sinai", "God's law", "moral code", "tablets of stone", "Israelite covenant", "Old Testament laws", "divine guidance", "obedience", "ethical teachings"]},
    {"genre": "David and Goliath", "keywords": ["1 Samuel", "shepherd boy", "giant slayer", "faith in God", "Israel vs Philistines", "sling and stone", "courage", "King David", "divine victory", "trust in God"]},
    {"genre": "Birth of Jesus", "keywords": ["Nativity story", "Bethlehem", "Mary and Joseph", "virgin birth", "manger", "Christmas", "shepherds", "angelic proclamation", "Messiah", "New Testament"]},
    {"genre": "Jesus' Baptism", "keywords": ["John the Baptist", "Jordan River", "dove", "Holy Spirit", "heavenly voice", "beginning of ministry", "repentance", "Messiah revealed", "obedience", "New Testament"]},
    {"genre": "Sermon on the Mount", "keywords": ["Beatitudes", "teachings of Jesus", "New Testament ethics", "divine wisdom", "love and forgiveness", "Kingdom of Heaven", "Christian morality", "Matthew 5-7", "spiritual guidance", "discipleship"]},
    {"genre": "Last Supper", "keywords": ["Jesus' disciples", "Passover meal", "bread and wine", "Eucharist", "betrayal foretold", "Judas Iscariot", "New Covenant", "Christian tradition", "final teachings", "Gethsemane"]},
    {"genre": "Crucifixion of Jesus", "keywords": ["Golgotha", "sacrifice for sins", "Roman execution", "Jesus' death", "atonement", "New Testament", "crown of thorns", "Good Friday", "salvation", "divine love"]},
    {"genre": "Resurrection of Jesus", "keywords": ["empty tomb", "Easter", "divine victory", "new life", "disciples' faith", "angelic announcement", "Messiah risen", "Christian hope", "triumph over death", "eternal life"]},
    {"genre": "Day of Pentecost", "keywords": ["Acts 2", "Holy Spirit", "tongues of fire", "apostles' empowerment", "early church", "speaking in tongues", "divine outpouring", "spiritual awakening", "New Testament", "Christian mission"]},
    {"genre": "Revelation's Seven Seals", "keywords": ["John's vision", "apocalyptic prophecy", "horsemen", "divine judgment", "scroll", "end times", "tribulation", "heavenly throne", "eschatology", "Revelation 6"]},
    {"genre": "The Trumpets", "keywords": ["Revelation 8-11", "divine warnings", "cosmic destruction", "angels", "apocalyptic events", "plagues", "judgment", "symbolism", "New Testament", "final warnings"]},
    {"genre": "The Beast and the False Prophet", "keywords": ["Revelation 13", "end times", "antichrist", "deception", "spiritual warfare", "666", "apocalyptic prophecy", "divine confrontation", "faith under trial", "symbolic imagery"]},
    {"genre": "The Bowls of Wrath", "keywords": ["Revelation 16", "final judgments", "plagues", "divine anger", "symbolic actions", "cosmic events", "apocalyptic prophecy", "tribulation", "New Testament", "end of days"]},
    {"genre": "The New Heaven and New Earth", "keywords": ["Revelation 21", "eternal kingdom", "God's dwelling", "divine promise", "perfect peace", "no more death", "heavenly city", "eschatology", "eternal joy", "New Jerusalem"]},
    {"genre": "Final Battle", "keywords": ["Revelation 19", "Armageddon", "divine triumph", "Satan's defeat", "cosmic conflict", "heavenly army", "end times", "symbolic imagery", "faithful victory", "eschatological hope"]},
    {"genre": "Eternal Reign of Christ", "keywords": ["Revelation 22", "throne of God", "eternal life", "perfect justice", "divine love", "heavenly presence", "paradise restored", "Christian hope", "eschatological promise", "spiritual fulfillment"]},
]

world_religions = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Christianity", "keywords": ["Jesus' birth", "Crucifixion and Resurrection", "Holy Bible", "Ten Commandments", "Last Supper", "Christmas", "Easter", "Trinity", "Sermon on the Mount", "Day of Pentecost"]},
    {"genre": "Islam", "keywords": ["Quran revelation", "Five Pillars", "Prophet Muhammad", "Hajj pilgrimage", "Ramadan fasting", "Eid celebrations", "Mecca and Medina", "Shahada", "daily prayers", "Hijra"]},
    {"genre": "Judaism", "keywords": ["Torah", "Exodus from Egypt", "Ten Commandments", "Passover", "Yom Kippur", "Sabbath observance", "Hanukkah", "Abrahamic covenant", "Temple in Jerusalem", "Bar/Bat Mitzvah"]},
    {"genre": "Hinduism", "keywords": ["Bhagavad Gita", "Ramayana and Mahabharata", "karma and dharma", "Diwali festival", "Holi celebration", "worship of deities", "Yoga and meditation", "pilgrimage to Varanasi", "Ganesh Chaturthi", "Trimurti (Brahma, Vishnu, Shiva)"]},
    {"genre": "Buddhism", "keywords": ["Four Noble Truths", "Eightfold Path", "Buddha's enlightenment", "meditation practices", "nirvana", "Vesak festival", "Lotus Sutra", "Bodhi Tree", "monastic life", "Dharma teachings"]},
    {"genre": "Sikhism", "keywords": ["Guru Nanak's teachings", "Guru Granth Sahib", "Golden Temple", "five Ks", "Langar community kitchen", "Amrit Ceremony", "Vaisakhi festival", "Kirtan devotional singing", "equality and service", "Khalsa tradition"]},
    {"genre": "Taoism", "keywords": ["Tao Te Ching", "Laozi", "Yin-Yang balance", "Wu Wei philosophy", "Qi energy", "Feng Shui", "longevity practices", "Tai Chi", "natural harmony", "Taoist rituals"]},
    {"genre": "Shinto", "keywords": ["kami spirits", "Torii gates", "shrines", "purification rituals", "Matsuri festivals", "Amaterasu", "ancestor worship", "seasonal ceremonies", "nature reverence", "Shinto mythology"]},
    {"genre": "Confucianism", "keywords": ["Analects of Confucius", "filial piety", "moral integrity", "ritual propriety", "scholar-officials", "harmony in relationships", "ancestor veneration", "Confucian education", "social harmony", "Confucian temples"]},
    {"genre": "Zoroastrianism", "keywords": ["Avesta scriptures", "Ahura Mazda", "fire temples", "dualism of good and evil", "Nowruz festival", "Zarathustra's teachings", "tower of silence", "Faravahar symbol", "eternal flame", "moral righteousness"]},
    {"genre": "Jainism", "keywords": ["Ahimsa (non-violence)", "Tirthankaras", "karma purification", "Sallekhana fasting", "Jain scriptures", "meditation and asceticism", "Paryushana festival", "monastic life", "vegetarianism", "spiritual liberation"]},
    {"genre": "Bahá'í Faith", "keywords": ["Bahá'u'lláh", "unity of religions", "progressive revelation", "Nine-pointed star", "Shrine of the Báb", "Ridván festival", "prayer and meditation", "social equality", "education for all", "world peace"]},
    {"genre": "Paganism", "keywords": ["nature worship", "Wheel of the Year", "Sabbats and Esbats", "ritual magic", "polytheism", "ancestor veneration", "witchcraft", "Druids and Wiccans", "solstice festivals", "divination"]},
    {"genre": "Indigenous Religions", "keywords": ["shamanism", "animism", "ritual dances", "sacred ceremonies", "oral traditions", "connection to nature", "ancestor spirits", "vision quests", "healing rituals", "tribal customs"]},
    {"genre": "Ancient Egyptian Religion", "keywords": ["Book of the Dead", "Ra, the Sun God", "mummification", "pyramids", "afterlife beliefs", "pharaohs as deities", "Anubis", "Isis and Osiris", "temple rituals", "hieroglyphs"]},
    {"genre": "Greco-Roman Religion", "keywords": ["Olympian gods", "Zeus and Hera", "mythology", "oracles and temples", "sacrifices", "heroic tales", "festivals", "Dionysian rites", "Roman pantheon", "legacy in Western culture"]},
    {"genre": "Norse Religion", "keywords": ["Odin and Thor", "Valhalla", "Yggdrasil", "Viking rituals", "sagas and Eddas", "Freyja", "Ragnarök", "runic inscriptions", "blot ceremonies", "sacred groves"]},
    {"genre": "Wicca", "keywords": ["Goddess and God worship", "ritual magic", "Wiccan Rede", "Samhain festival", "pentacle symbol", "nature-based spirituality", "coven practices", "herbal magic", "divination tools", "ritual circles"]},
    {"genre": "Modern Spiritualism", "keywords": ["mediumship", "afterlife communication", "seances", "spirit guides", "psychic phenomena", "healing practices", "spiritual growth", "astral projection", "reincarnation beliefs", "meditation"]},
    {"genre": "Atheism/Agnosticism", "keywords": ["absence of religion", "secular philosophy", "critical thinking", "agnostic uncertainty", "humanism", "scientific worldview", "rational ethics", "freedom from dogma", "logical reasoning", "moral values"]},
]

daytime_styles = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Forest at Dawn", "keywords": ["misty trees", "soft sunlight", "dew on leaves", "birds chirping", "tranquil", "fresh air", "wildlife waking", "shimmering light", "peaceful", "nature's awakening"]},
    {"genre": "Countryside at Noon", "keywords": ["golden fields", "bright sunlight", "blue skies", "farmhouses", "cattle grazing", "gentle breeze", "rural serenity", "verdant meadows", "crickets chirping", "open space"]},
    {"genre": "City in the Afternoon", "keywords": ["bustling streets", "sun-dappled skyscrapers", "traffic", "urban life", "crowds", "cafés buzzing", "warm tones", "shadow play", "commerce in action", "modern vibe"]},
    {"genre": "Beach at Sunset", "keywords": ["orange horizon", "waves crashing", "calm tides", "romantic", "golden glow", "silhouetted palm trees", "soothing sound", "soft sand", "cooling air", "peaceful retreat"]},
    {"genre": "Mountain at Sunrise", "keywords": ["majestic peaks", "pink and orange skies", "crisp air", "serene", "snow-capped", "hikers starting journey", "panoramic views", "clouds below", "first light", "nature's grandeur"]},
    {"genre": "Desert at High Noon", "keywords": ["blazing sun", "golden dunes", "dry heat", "mirage", "isolated", "cactus", "open expanse", "shimmering sand", "extreme conditions", "endless horizons"]},
    {"genre": "Rainy Village Evening", "keywords": ["drizzling rain", "wet cobblestones", "glowing windows", "smoke from chimneys", "muddy paths", "quiet streets", "rustic charm", "soft thunder", "raindrop sounds", "cozy atmosphere"]},
    {"genre": "Urban Nightlife", "keywords": ["neon lights", "crowded streets", "clubs and bars", "music", "modern architecture", "car headlights", "night market", "lively energy", "cityscape reflections", "nocturnal excitement"]},
    {"genre": "Winter Morning", "keywords": ["snow-covered landscape", "frosty air", "chimneys smoking", "gloves and scarves", "quiet streets", "crisp sunlight", "ice crystals", "cozy indoors", "winter birds", "seasonal charm"]},
    {"genre": "Suburban Dusk", "keywords": ["subdued colors", "streetlights flickering on", "families outdoors", "calm environment", "front porches", "kids playing", "scent of dinner", "long shadows", "neighborhood feel", "peaceful transition"]},
    {"genre": "Jungle Noon", "keywords": ["thick greenery", "humid air", "sun filtering through canopy", "exotic wildlife", "chirping insects", "hidden streams", "dense foliage", "mystical", "ancient vibes", "exploration"]},
    {"genre": "Lake at Twilight", "keywords": ["calm waters", "purple sky", "ripples", "reflective mood", "cool breeze", "stars beginning to appear", "silence", "boats moored", "natural beauty", "tranquil"]},
    {"genre": "Farm in Early Morning", "keywords": ["rooster crowing", "dew on grass", "farm animals", "tractors starting", "sunrise over fields", "freshly plowed earth", "barn activity", "simple life", "birds in flight", "serenity"]},
    {"genre": "Park in Autumn Afternoon", "keywords": ["falling leaves", "orange and yellow tones", "crisp air", "people walking dogs", "children playing", "benches occupied", "clear skies", "seasonal beauty", "rustling leaves", "cozy atmosphere"]},
    {"genre": "Seaside Storm", "keywords": ["crashing waves", "dark clouds", "thunder rumbling", "windswept", "dramatic", "salt spray", "turbulent waters", "isolated", "raw power", "nature's wrath"]},
    {"genre": "Meadow at Midnight", "keywords": ["starlit sky", "fireflies", "moonlit grass", "cool breeze", "nocturnal sounds", "solitude", "peaceful", "gentle sway", "mystical atmosphere", "nighttime calm"]},
    {"genre": "Urban Rooftop Morning", "keywords": ["sunrise view", "birds flying", "chimneys", "distant city sounds", "quiet before rush hour", "clear sky", "refreshing", "expansive skyline", "urban serenity", "modern living"]},
    {"genre": "Busy Market Afternoon", "keywords": ["vendors shouting", "colorful stalls", "crowded paths", "scent of food", "bargaining", "lively", "cultural diversity", "sun overhead", "bustling", "community spirit"]},
    {"genre": "Cliffside Sunset", "keywords": ["majestic views", "warm colors", "distant ocean", "birds soaring", "natural wonder", "windy", "dramatic", "romantic", "horizon fading", "peaceful end"]},
    {"genre": "Night Train Journey", "keywords": ["dim lights", "rattling sound", "scenery in darkness", "quiet passengers", "motion", "whistle blowing", "traveling through time", "mystery", "interior warmth", "nostalgia"]},
]

nighttime_styles = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Forest at Night", "keywords": ["moonlit trees", "owl hooting", "crickets chirping", "mystical shadows", "cool breeze", "fireflies", "dark pathways", "hidden wildlife", "tranquil", "starry sky"]},
    {"genre": "City Streets at Midnight", "keywords": ["neon lights", "empty roads", "quiet ambiance", "distant sirens", "reflective puddles", "urban mystery", "isolated vibes", "streetlights", "shadows", "modern allure"]},
    {"genre": "Beach under the Moon", "keywords": ["waves lapping", "silver light on water", "soft sand", "cool air", "calm tides", "starlit sky", "peaceful sounds", "distant ships", "romantic", "isolated"]},
    {"genre": "Mountain Under Starlight", "keywords": ["snow-capped peaks", "clear sky", "cool crisp air", "absolute silence", "constellations", "serene", "campfire warmth", "distant howls", "mystical", "majestic"]},
    {"genre": "Countryside Night", "keywords": ["barn lights glowing", "crickets", "fireflies in the fields", "clear skies", "rustling leaves", "quiet serenity", "moonlit fences", "cattle resting", "cool air", "natural calm"]},
    {"genre": "Desert Under Stars", "keywords": ["endless dunes", "cool breeze", "shooting stars", "absolute silence", "mystical atmosphere", "open expanse", "moonlit sand", "nomadic setting", "ancient vibes", "remote"]},
    {"genre": "Rainy Urban Night", "keywords": ["wet streets", "reflective lights", "umbrellas", "muted sounds", "soft rain", "cozy indoors", "dim streetlights", "quiet neighborhoods", "melancholic", "soothing"]},
    {"genre": "Rural Village Evening", "keywords": ["dimly lit streets", "warm house lights", "dogs barking", "smoke from chimneys", "quiet atmosphere", "family gatherings", "moonlight on paths", "soft breezes", "homey", "peaceful"]},
    {"genre": "Jungle at Night", "keywords": ["dense trees", "animal calls", "fireflies", "mystery", "humid air", "moonlight filtering through leaves", "nocturnal life", "hidden predators", "exotic vibes", "adventurous"]},
    {"genre": "Lake under the Moon", "keywords": ["still waters", "reflections of stars", "cool air", "chirping frogs", "peaceful", "fishing boats", "soft ripples", "tranquil escape", "whispers of wind", "natural beauty"]},
    {"genre": "Winter Night", "keywords": ["snowy landscape", "glowing windows", "frosty air", "footprints in snow", "stillness", "holiday lights", "fireplace warmth", "crisp atmosphere", "silent streets", "cozy vibes"]},
    {"genre": "Suburban Night", "keywords": ["streetlights", "calm atmosphere", "occasional cars", "quiet homes", "distant sounds of nightlife", "tree-lined streets", "peaceful", "stars overhead", "evening walks", "modern suburban feel"]},
    {"genre": "Seaside Storm at Night", "keywords": ["crashing waves", "lightning flashes", "roaring winds", "dark waters", "powerful ambiance", "stormy clouds", "raw energy", "dangerous beauty", "ocean's wrath", "isolated"]},
    {"genre": "Rooftop Under Stars", "keywords": ["panoramic view", "cool night air", "cityscape", "starlit sky", "whispering wind", "modern vibe", "romantic", "urban escape", "solitude", "peaceful reflections"]},
    {"genre": "Night Market", "keywords": ["colorful lights", "crowded paths", "local delicacies", "buzzing energy", "street performances", "vibrant stalls", "cultural richness", "friendly chatter", "exotic scents", "lively"]},
    {"genre": "Campfire at Midnight", "keywords": ["crackling fire", "stars above", "warmth", "stories shared", "smoke drifting", "surrounded by nature", "peaceful glow", "group camaraderie", "wooded setting", "relaxing"]},
    {"genre": "Moonlit Cliffside", "keywords": ["ocean view", "howling winds", "starry sky", "majestic ambiance", "serenity", "soft grass", "distant waves", "peaceful isolation", "romantic mood", "natural grandeur"]},
    {"genre": "Urban Alley at Night", "keywords": ["dimly lit", "mystery", "shadows", "graffiti", "quiet tension", "urban charm", "echoing footsteps", "isolation", "raw edge", "gritty atmosphere"]},
    {"genre": "Ship at Sea in the Night", "keywords": ["open waters", "moonlit deck", "sound of waves", "navigation lights", "vastness", "crew activity", "isolation", "sea breeze", "mystical journey", "adventure"]},
    {"genre": "Tundra Under Aurora", "keywords": ["glowing lights", "snowy expanse", "silent beauty", "cold air", "distant mountains", "majestic spectacle", "nighttime wonder", "northern lights", "peaceful", "remote wonder"]},
]

alien_species = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Greys Aliens", "keywords": ["large black eyes", "short stature", "gray skin", "telepathic abilities", "mysterious", "advanced technology", "emotionless", "UFO sightings", "scientific curiosity", "abduction folklore"]},
    {"genre": "Reptilians Aliens", "keywords": ["lizard-like", "scaly skin", "intelligent", "shapeshifting", "cold-blooded", "political conspiracy", "underground dwellers", "aggressive", "world domination", "ancient origins"]},
    {"genre": "Nordics Aliens", "keywords": ["tall and humanoid", "blond hair", "blue eyes", "benevolent", "telepathic", "mystical aura", "spiritual guidance", "peaceful", "interstellar travelers", "mythical beauty"]},
    {"genre": "Insectoids Aliens", "keywords": ["insect-like features", "exoskeleton", "hive mind", "fast reflexes", "alien predators", "advanced hive societies", "colonial mindset", "brutal efficiency", "resourceful", "intimidating"]},
    {"genre": "Amoeboids Aliens", "keywords": ["shape-shifting", "gelatinous form", "biological adaptability", "non-humanoid", "engulfing prey", "bioluminescence", "single-celled intelligence", "mimicry", "absorb nutrients", "resilient"]},
    {"genre": "Aquatics Aliens", "keywords": ["ocean dwellers", "fins and gills", "bioluminescence", "deep-sea creatures", "intelligent communication", "water-based ecosystems", "hidden in oceans", "fluid movement", "ancient knowledge", "peaceful explorers"]},
    {"genre": "Energy Beings Aliens", "keywords": ["non-corporeal", "pure energy", "glowing aura", "intangible", "high intelligence", "omnipresent", "quantum existence", "difficult to comprehend", "advanced civilizations", "mystical"]},
    {"genre": "Plant-Based Aliens", "keywords": ["photosynthetic", "rooted intelligence", "adaptive growth", "green skin", "organic technology", "symbiotic relationships", "patient thinkers", "eco-friendly", "unpredictable forms", "nurturers"]},
    {"genre": "Silicon-Based Aliens", "keywords": ["crystalline structure", "rock-like appearance", "extreme durability", "heat resistance", "non-organic life", "mineral-based systems", "slow metabolism", "geological adaptability", "inhabit harsh environments", "ancient beings"]},
    {"genre": "Predators Aliens", "keywords": ["hunter instincts", "aggressive", "stealthy", "advanced weaponry", "xenomorphic features", "territorial", "combat experts", "fearsome presence", "trophy collectors", "deadly"]},
    {"genre": "Xenomorphs Aliens", "keywords": ["parasitic reproduction", "acidic blood", "black exoskeleton", "predatory", "evolutionary adaptability", "fear-inducing", "hive structures", "biomechanical design", "relentless hunters", "nightmarish"]},
    {"genre": "Cephalopoid Aliens", "keywords": ["tentacles", "amorphous", "underwater traits", "intelligent", "camouflage", "alien oceans", "telepathic communication", "ancient knowledge", "flexible bodies", "mysterious"]},
    {"genre": "Interdimensional Beings Aliens", "keywords": ["exist outside time", "warp dimensions", "abstract forms", "multi-dimensional intelligence", "appear as hallucinations", "elusive", "godlike powers", "defy physics", "enigmatic", "otherworldly"]},
    {"genre": "Biological Robots Aliens", "keywords": ["cybernetic enhancements", "biomechanical structure", "synthetic intelligence", "engineered", "tool-like purpose", "combination of organic and mechanical", "efficient", "indestructible", "unemotional", "designed for specific tasks"]},
    {"genre": "Light Beings Aliens", "keywords": ["luminous forms", "peaceful", "spiritual guides", "pure energy", "non-violent", "highly intelligent", "interdimensional travelers", "celestial beauty", "calming presence", "emissaries of good"]},
    {"genre": "Shadow Beings Aliens", "keywords": ["dark forms", "stealthy", "intangible", "fear-inducing", "unknown motives", "interdimensional origins", "appear in nightmares", "elusive", "stalkers", "mysterious and eerie"]},
    {"genre": "Void Dwellers Aliens", "keywords": ["exist in deep space", "adapted to vacuum", "ancient beings", "star-eaters", "unfathomable scale", "indescribable forms", "eternal", "harbingers of destruction", "mythical status", "cosmic predators"]},
    {"genre": "Parasites Aliens", "keywords": ["symbiotic or destructive", "host-dependent", "small size", "spread rapidly", "high adaptability", "mind control", "biological menace", "infectious", "transform hosts", "survivors"]},
    {"genre": "Hive-Minded Colonials Aliens", "keywords": ["collective consciousness", "selfless unity", "highly organized", "dominant queen", "territorial", "rapid expansion", "swarm behavior", "evolutionary adaptation", "relentless", "intimidating numbers"]},
    {"genre": "Gelatinous Cubes Aliens", "keywords": ["translucent", "amorphous", "digest prey", "biological traps", "slow-moving", "absorb nutrients", "simple intelligence", "alien dungeons", "unsettling", "unique predators"]},
]

gaming_consoles = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "NeoGeo", "keywords": ["released in 1990", "arcade-quality games", "King of Fighters", "Samurai Shodown", "Metal Slug", "highly expensive", "SNK", "CD-based and cartridge versions", "famous for fighting games", "premium console"]},
    {"genre": "Magnavox Odyssey", "keywords": ["first home video game console", "released in 1972", "black-and-white graphics", "paddle controllers", "no microprocessor", "no sound", "limited games", "primitive", "simple gameplay", "Pong-inspired"]},
    {"genre": "Atari 2600", "keywords": ["released in 1977", "home console", "cartridge-based", "joystick controller", "first major video game console", "Pong", "iconic graphics", "Space Invaders", "Pac-Man", "E.T. the Extra-Terrestrial"]},
    {"genre": "Nintendo Entertainment System (NES)", "keywords": ["released in 1985", "8-bit console", "Super Mario Bros.", "Metroid", "Zelda", "pioneered home console gaming", "game cartridges", "two-button controller", "multi-tiered gameplay", "iconic"]},
    {"genre": "Sega Genesis", "keywords": ["released in 1988", "16-bit console", "Sonic the Hedgehog", "Street Fighter", "Mortal Kombat", "popular in North America", "arcade-quality games", "innovative controllers", "multiplayer support", "blast processing"]},
    {"genre": "Super Nintendo Entertainment System (SNES)", "keywords": ["released in 1990", "16-bit console", "Super Mario World", "The Legend of Zelda: A Link to the Past", "Donkey Kong Country", "Yoshi's Island", "colorful graphics", "innovative RPGs", "mode 7 graphics", "action-packed"]},
    {"genre": "Sony PlayStation", "keywords": ["released in 1994", "CD-based", "Gran Turismo", "Final Fantasy VII", "3D graphics", "DVD player", "DualShock controller", "vibrational feedback", "large game library", "Sony's first console"]},
    {"genre": "Nintendo 64", "keywords": ["released in 1996", "64-bit console", "Super Mario 64", "GoldenEye 007", "The Legend of Zelda: Ocarina of Time", "expansion pack support", "innovative 3D gameplay", "four controller ports", "analog stick", "cutting-edge graphics"]},
    {"genre": "Sony PlayStation 2", "keywords": ["released in 2000", "DVD-compatible", "Grand Theft Auto: San Andreas", "Final Fantasy X", "largest game library", "backward compatibility", "online multiplayer", "improved graphics", "best-selling console", "PlayStation exclusive games"]},
    {"genre": "Xbox", "keywords": ["released in 2001", "Microsoft's first console", "Halo: Combat Evolved", "online gaming via Xbox Live", "high-definition graphics", "integrated DVD player", "multiplayer-focused", "innovative controller", "direct access to media", "powerful hardware"]},
    {"genre": "Nintendo Wii", "keywords": ["released in 2006", "motion-sensing controllers", "Wii Sports", "Casual gaming", "family-friendly games", "innovative gameplay", "Wii Fit", "motion control revolution", "Wii Party", "budget-friendly"]},
    {"genre": "PlayStation 3", "keywords": ["released in 2006", "Blu-ray player", "Uncharted 2: Among Thieves", "Gran Turismo 5", "HD graphics", "PlayStation Network", "DualShock 3", "cross-platform multiplayer", "advanced processing power", "media center functionality"]},
    {"genre": "Xbox 360", "keywords": ["released in 2005", "online gaming via Xbox Live", "Halo 3", "Kinect support", "multimedia entertainment", "game streaming", "high-definition graphics", "Xbox Live Arcade", "DVD player", "popular among core gamers"]},
    {"genre": "Nintendo 3DS", "keywords": ["released in 2011", "3D gaming without glasses", "Super Mario 3D Land", "Pokémon X and Y", "augmented reality", "touchscreen", "portable console", "dual screens", "StreetPass functionality", "cross-platform play"]},
    {"genre": "PlayStation 4", "keywords": ["released in 2013", "8-core AMD processor", "The Last of Us Part II", "Spider-Man", "Death Stranding", "4K video streaming", "social integration", "Share button", "DualShock 4 controller", "massive game library"]},
    {"genre": "Xbox One", "keywords": ["released in 2013", "1080p graphics", "Halo 5: Guardians", "Kinect 2.0", "cloud gaming", "multimedia integration", "voice control", "backward compatibility", "digital rights management", "Xbox Game Pass"]},
    {"genre": "Nintendo Switch", "keywords": ["released in 2017", "hybrid portable console", "The Legend of Zelda: Breath of the Wild", "Super Mario Odyssey", "multiplayer support", "Joy-Con controllers", "touchscreen", "Nintendo exclusive titles", "motion controls", "innovative design"]},
    {"genre": "PlayStation 5", "keywords": ["released in 2020", "8K graphics", "Demon's Souls", "Spider-Man: Miles Morales", "faster load times", "DualSense controller", "3D audio", "backward compatibility", "Ray Tracing", "PlayStation exclusives"]},
    {"genre": "Xbox Series X", "keywords": ["released in 2020", "12 teraflops processing power", "Halo Infinite", "backward compatibility", "Quick Resume", "Game Pass", "4K gaming", "Xbox Live Gold", "Smart Delivery", "powerful performance"]},
    {"genre": "Nintendo Switch OLED", "keywords": ["released in 2021", "improved screen", "portable design", "enhanced audio", "Super Smash Bros. Ultimate", "Mario Kart 8 Deluxe", "Joy-Con drift improvements", "upgraded dock", "higher-quality visuals", "better portability"]},
    {"genre": "PlayStation VR", "keywords": ["released in 2016", "virtual reality", "immersive gaming", "exclusive VR titles", "virtual reality headset", "motion tracking", "PlayStation Move controllers", "first-person experiences", "multiplayer VR support", "motion-controlled gameplay"]},
]

art_genres = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Drawing art", "keywords": ["sketching", "pencil", "charcoal", "line art", "shading", "realism", "detailed", "classical", "figure drawing", "manga"]},
    {"genre": "Anime art", "keywords": ["Japanese animation", "manga", "cartoons", "vivid colors", "character design", "action", "emotion", "digital art", "2D animation", "stylized"]},
    {"genre": "Painting art", "keywords": ["oil painting", "watercolor", "acrylic", "canvas", "impressionism", "realism", "abstract", "portrait", "still life", "landscape"]},
    {"genre": "Digital art", "keywords": ["digital painting", "photoshop", "graphic design", "3D modeling", "illustration", "vector art", "CGI", "concept art", "virtual art", "motion graphics"]},
    {"genre": "Street Art", "keywords": ["graffiti", "urban art", "spray paint", "public spaces", "mural", "political messages", "bold", "rebel", "large-scale", "installation"]},
    {"genre": "Surrealism art", "keywords": ["dream-like", "fantasy", "unreal", "psychedelic", "abstract", "unconscious", "symbolism", "bizarre", "imagination", "mysterious"]},
    {"genre": "Pop Art", "keywords": ["mass media", "bright colors", "commercial", "consumerism", "icons", "advertising", "collage", "comic strips", "repetition", "celebrity"]},
    {"genre": "Cubism art", "keywords": ["geometric shapes", "abstract", "multiple perspectives", "fragmentation", "reduction", "analytical", "synthetic", "modern", "avant-garde", "revolutionary"]},
    {"genre": "Impressionism art", "keywords": ["light", "color", "brush strokes", "outdoor scenes", "everyday life", "natural light", "momentary", "soft", "quick strokes", "blurred"]},
    {"genre": "Art Nouveau", "keywords": ["decorative arts", "elegant", "flowing lines", "nature-inspired", "organic", "ornamental", "glass", "metalwork", "architecture", "whiplash curves"]},
]

render_systems = [
    {"genre": "Unreal Engine 5", "keywords": ["real-time rendering", "photorealistic graphics", "Lumen", "Nanite", "ray tracing", "open world", "virtual production", "cinematic quality", "global illumination", "real-time physics"]},
    {"genre": "Unity", "keywords": ["real-time rendering", "cross-platform", "game development", "2D/3D rendering", "VR/AR support", "particle system", "C# scripting", "asset store", "shader support", "modular"]},
    {"genre": "Blender", "keywords": ["open-source", "3D modeling", "animation", "sculpting", "rendering", "VFX", "node-based compositing", "ray tracing", "simulations", "free"]},
    {"genre": "Autodesk Maya", "keywords": ["3D animation", "modeling", "rendering", "rigging", "VFX", "texturing", "lighting", "MEL scripting", "maya node editor", "animation tools"]},
    {"genre": "Cinema 4D", "keywords": ["motion graphics", "3D animation", "modeling", "rendering", "VR/AR", "integrated workflow", "advanced shaders", "MoGraph", "particles", "team render"]},
    {"genre": "V-Ray", "keywords": ["rendering engine", "photorealistic", "global illumination", "ray tracing", "architectural visualization", "interior design", "product design", "visual effects", "materials", "high-quality render"]},
    {"genre": "Redshift", "keywords": ["GPU-accelerated", "3D rendering", "visual effects", "VFX", "architecture", "motion graphics", "production-ready", "scalable", "photorealism", "high-speed rendering"]},
    {"genre": "Arnold", "keywords": ["ray tracing", "rendering engine", "photorealistic", "cinematic quality", "GPU and CPU rendering", "VFX", "character animation", "interactive", "texture mapping", "production"]},
    {"genre": "OctaneRender", "keywords": ["GPU-based", "real-time rendering", "photorealistic", "VFX", "animation", "3D modeling", "motion graphics", "materials", "lighting", "texture mapping"]},
    {"genre": "Lumion", "keywords": ["architecture", "rendering software", "real-time rendering", "interior and exterior visualization", "realistic visuals", "landscape rendering", "animation", "photorealistic", "easy-to-use", "sketchup"]},
]

art_styles = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Painter", "keywords": ["oil painting", "canvas", "brush strokes", "color palette", "realism", "impressionism", "abstract", "surrealism", "still life", "landscapes"]},
    {"genre": "Leonardo da Vinci", "keywords": ["Renaissance", "Mona Lisa", "The Last Supper", "sfumato", "anatomical studies", "oil paintings", "master of perspective", "classical", "scientific observations", "genius"]},
    {"genre": "Vincent van Gogh", "keywords": ["Post-Impressionism", "bold strokes", "vibrant colors", "Starry Night", "sunflowers", "emotionally expressive", "self-portrait", "nightscapes", "swirling patterns", "mental health"]},
    {"genre": "Pablo Picasso", "keywords": ["Cubism", "abstract art", "blue period", "Guernica", "multi-perspective", "modernism", "geometric shapes", "avant-garde", "collage", "surrealism"]},
    {"genre": "Claude Monet", "keywords": ["Impressionism", "water lilies", "light effects", "outdoor scenes", "color theory", "brushwork", "landscapes", "nature", "famous garden", "plein air painting"]},
    {"genre": "Michelangelo", "keywords": ["Renaissance", "sculpture", "Sistine Chapel", "David", "The Creation of Adam", "master of anatomy", "classical themes", "religious art", "fresco painting", "religious devotion"]},
    {"genre": "Rembrandt", "keywords": ["Baroque", "portraiture", "self-portraits", "light and shadow", "realism", "dramatic lighting", "history painting", "oil painting", "biblical scenes", "psychological depth"]},
    {"genre": "Frida Kahlo", "keywords": ["Surrealism", "symbolism", "self-portrait", "Mexican culture", "pain and suffering", "bright colors", "folk art", "expressionist", "Mexican identity", "folk imagery"]},
    {"genre": "Andy Warhol", "keywords": ["Pop Art", "mass production", "consumerism", "celebrity culture", "Campbell's Soup Cans", "bold colors", "screen printing", "repetition", "iconic", "modern commercial art"]},
    {"genre": "Pencil Drawing", "keywords": ["graphite", "sketches", "realistic drawings", "shading", "portraiture", "fine details", "fine art", "illustration", "monochromatic", "detailed lines"]},
    {"genre": "John Singer Sargent", "keywords": ["portraiture", "realism", "light and shadow", "pencil sketches", "impressionist", "famous portraitist", "modern realist", "detailed sketches", "shading", "studies"]},
    {"genre": "Albert Dürer", "keywords": ["Renaissance", "woodcuts", "engraving", "precise detail", "pencil sketches", "printmaking", "mathematical precision", "self-portrait", "nature studies", "classical works"]},
    {"genre": "Anime", "keywords": ["Japanese animation", "manga", "stylized characters", "big eyes", "vivid colors", "action scenes", "emotional storytelling", "fantasy", "superpowers", "shonen"]},
    {"genre": "Hayao Miyazaki", "keywords": ["Studio Ghibli", "anime", "whimsical characters", "hand-drawn animation", "fantasy world", "environmental themes", "coming-of-age", "Hayao", "My Neighbor Totoro", "Spirited Away"]},
    {"genre": "Osamu Tezuka", "keywords": ["Manga", "anime", "Astro Boy", "father of manga", "cartoonish style", "action-adventure", "vivid storytelling", "multiple genres", "shoujo", "modern manga creator"]},
    {"genre": "Cartoon", "keywords": ["animated series", "humor", "exaggerated features", "cartoonish style", "comic strips", "animation studios", "funny characters", "family-friendly", "comedy", "cultural satire"]},
    {"genre": "Walt Disney", "keywords": ["animation", "Disney classics", "Mickey Mouse", "The Lion King", "cartooning", "family entertainment", "storybook", "creativity", "magic", "legacy"]},
    {"genre": "Chuck Jones", "keywords": ["Looney Tunes", "animation", "humor", "cartoon characters", "Wile E. Coyote", "Bugs Bunny", "Daffy Duck", "timing", "visual gags", "animated shorts"]},
    {"genre": "Digital Art", "keywords": ["Photoshop", "illustration", "digital painting", "pixel art", "3D modeling", "concept art", "CGI", "realism", "textures", "graphic design"]},
    {"genre": "Beeple", "keywords": ["digital art", "3D modeling", "futuristic", "NFT art", "famous digital artist", "motion graphics", "everydays project", "surreal landscapes", "modern art", "concept art"]},
    {"genre": "Greg Rutkowski", "keywords": ["digital painting", "fantasy art", "concept artist", "illustration", "game art", "vivid colors", "realism", "detailed artwork", "fantasy worlds", "light and shadows"]},
    {"genre": "Artgerm", "keywords": ["digital painting", "portrait", "realistic", "modern style", "digital techniques", "concept art", "female characters", "illustration", "popular culture", "high detail"]},
    {"genre": "Feng Zhu", "keywords": ["concept art", "digital painting", "industrial design", "environment design", "cinematic", "sci-fi", "game art", "character design", "visual storytelling", "dynamic scenes"]},
]

art_styles2 = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Oil Painting", "keywords": ["Leonardo da Vinci", "Vincent van Gogh", "Claude Monet", "Pablo Picasso", "Michelangelo", "Rembrandt", "Frida Kahlo", "Andy Warhol", "Johannes Vermeer", "Diego Rivera"]},
    {"genre": "Pencil Drawing", "keywords": ["Leonardo da Vinci", "Albrecht Dürer", "Michelangelo", "John Tenniel", "Augustus Saint-Gaudens", "Norman Rockwell", "Gerald Scarfe", "Tim Burton", "Bansky", "Zdzisław Beksiński"]},
    {"genre": "Anime Drawing", "keywords": ["Hayao Miyazaki", "Makoto Shinkai", "Satoshi Kon", "Katsuhiro Otomo", "Akira Toriyama", "Yoshiyuki Tomino", "Mamoru Hosoda", "Naoko Takeuchi", "Tite Kubo", "Eiichiro Oda"]},
    {"genre": "Cartoon Drawing", "keywords": ["Walt Disney", "Chuck Jones", "Tex Avery", "Hanna-Barbera", "Matt Groening", "Bill Watterson", "Jim Davis", "Osamu Tezuka", "John Kricfalusi", "Seth MacFarlane"]},
    {"genre": "Digital Drawing", "keywords": ["Kyle T. Webster", "Greg Rutkowski", "Aaron Blaise", "Loish", "Feng Zhu", "Sam Yang", "Artgerm", "Sakimichan", "Ilya Kuvshinov", "Ross Tran"]},
    {"genre": "Watercolor Painting", "keywords": ["Winslow Homer", "John Singer Sargent", "J.M.W. Turner", "Claude Monet", "Edward Hopper", "Georges Rouault", "Albrecht Dürer", "Hiroshi Yoshida", "Milton Avery", "Mary Cassatt"]},
    {"genre": "Sculpture", "keywords": ["Michelangelo", "Auguste Rodin", "Henry Moore", "Donatello", "Constantin Brâncuși", "Barbara Hepworth", "Alexander Calder", "Jean Arp", "Alexander McQueen", "Lorenzo Ghiberti"]},
    {"genre": "Graffiti", "keywords": ["Banksy", "Jean-Michel Basquiat", "Keith Haring", "Shepard Fairey", "RETNA", "Os Gêmeos", "Futura 2000", "Space Invader", "DAZE", "Swoon"]},
    {"genre": "Abstract Art", "keywords": ["Wassily Kandinsky", "Piet Mondrian", "Jackson Pollock", "Mark Rothko", "Franz Kline", "Helen Frankenthaler", "Kazimir Malevich", "Joan Miró", "Robert Delaunay", "Theo van Doesburg"]},
    {"genre": "Fantasy Art", "keywords": ["Frank Frazetta", "Boris Vallejo", "Julie Bell", "Michael Whelan", "Luis Royo", "H. R. Giger", "Brom", "Chris Riddell", "John Howe", "Alan Lee"]},
]

film_and_series_creators = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Action Movies", "keywords": ["Steven Spielberg", "George Lucas", "James Cameron", "Michael Bay", "Ridley Scott", "Christopher Nolan", "Zack Snyder", "J.J. Abrams", "John Woo", "Luc Besson"]},
    {"genre": "Animation Movies", "keywords": ["Walt Disney", "Hayao Miyazaki", "John Lasseter", "Tim Burton", "Don Bluth", "Nick Park", "Brad Bird", "Andrew Stanton", "Pete Docter", "Glen Keane"]},
    {"genre": "Horror Movies", "keywords": ["Alfred Hitchcock", "John Carpenter", "Wes Craven", "George A. Romero", "James Wan", "Guillermo del Toro", "Stanley Kubrick", "Tobe Hooper", "Sam Raimi", "David Cronenberg"]},
    {"genre": "Comedy Movies", "keywords": ["Charlie Chaplin", "Mel Brooks", "Woody Allen", "Judd Apatow", "Coen Brothers", "John Hughes", "Christopher Guest", "Peter Farrelly", "Paul Feig", "Edgar Wright"]},
    {"genre": "Drama Movies", "keywords": ["Martin Scorsese", "Francis Ford Coppola", "Quentin Tarantino", "Ridley Scott", "Steven Spielberg", "Christopher Nolan", "Danny Boyle", "Ang Lee", "David Fincher", "Tom McCarthy"]},
    {"genre": "Sci-Fi Movies", "keywords": ["Stanley Kubrick", "Ridley Scott", "George Lucas", "James Cameron", "Christopher Nolan", "Steven Spielberg", "Luc Besson", "Dennis Villeneuve", "Andrei Tarkovsky", "J.J. Abrams"]},
    {"genre": "Superhero Movies", "keywords": ["Stan Lee", "Jack Kirby", "Christopher Nolan", "Joss Whedon", "Zack Snyder", "Jon Favreau", "Taika Waititi", "James Gunn", "Ryan Coogler", "Matt Reeves"]},
    {"genre": "TV Series Drama", "keywords": ["David Chase", "Vince Gilligan", "Matthew Weiner", "Aaron Sorkin", "Shonda Rhimes", "Mindy Kaling", "Darren Star", "Ryan Murphy", "David Simon", "Damien Chazelle"]},
    {"genre": "TV Series Comedy", "keywords": ["Chuck Lorre", "Greg Daniels", "Dan Harmon", "Larry David", "Tina Fey", "Amy Poehler", "Michael Schur", "Billy Wilder", "Steven Moffat", "Trey Parker"]},
    {"genre": "Documentary Filmmakers", "keywords": ["Werner Herzog", "Michael Moore", "Ken Burns", "Spike Lee", "Ava DuVernay", "Errol Morris", "Barbara Kopple", "Robert Flaherty", "Laura Poitras", "Louis Theroux"]},
    {"genre": "Fantasy TV Shows", "keywords": ["George R.R. Martin", "J.R.R. Tolkien", "Joss Whedon", "David Benioff", "D.B. Weiss", "Martin Scorsese", "Peter Jackson", "Alan Ball", "Terry Goodkind", "M. Night Shyamalan"]},
    {"genre": "Thriller Movies", "keywords": ["David Fincher", "Alfred Hitchcock", "Christopher Nolan", "Martin Scorsese", "Paul Thomas Anderson", "Jonathan Demme", "John Frankenheimer", "Michael Mann", "Brian De Palma", "Fritz Lang"]},
    {"genre": "Crime Movies", "keywords": ["Martin Scorsese", "Quentin Tarantino", "Francis Ford Coppola", "Guy Ritchie", "John Woo", "Michael Mann", "Sergio Leone", "David Fincher", "Brett Ratner", "Michael Bay"]},
    {"genre": "Musical Movies", "keywords": ["Bob Fosse", "Lin-Manuel Miranda", "Baz Luhrmann", "Andrew Lloyd Webber", "Richard Rodgers", "Oscar Hammerstein II", "Gene Kelly", "Stanley Donen", "Sondheim", "John Waters"]},
    {"genre": "War Movies", "keywords": ["Steven Spielberg", "Francis Ford Coppola", "Oliver Stone", "Stanley Kubrick", "Ridley Scott", "Christopher Nolan", "Paul Verhoeven", "John Wayne", "Terrence Malick", "David Ayer"]},
    {"genre": "Family Movies", "keywords": ["Steven Spielberg", "Walt Disney", "Richard Curtis", "Chris Columbus", "Joe Johnston", "Brad Bird", "Jodie Foster", "Rob Reiner", "Nancy Meyers", "Tim Burton"]},
    {"genre": "Mystery Movies", "keywords": ["Agatha Christie", "Sir Arthur Conan Doyle", "Alfred Hitchcock", "David Fincher", "Rian Johnson", "Billy Wilder", "M. Night Shyamalan", "Gillian Flynn", "Stanley Kubrick", "Neil Jordan"]},
    {"genre": "Animated TV Shows", "keywords": ["Matt Groening", "Seth MacFarlane", "Trey Parker", "Dan Harmon", "Mike Judge", "Justin Roiland", "Gene Luen Yang", "J.J. Abrams", "Phyllis Diller", "Craig McCracken"]},
]

photographers_and_styles = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Black and White Photography", "keywords": ["Ansel Adams", "Henri Cartier-Bresson", "Dorothea Lange", "Robert Frank", "Richard Avedon", "Irving Penn", "Sebastião Salgado", "Man Ray", "Edward Weston", "Bill Brandt"]},
    {"genre": "Portrait Photography", "keywords": ["Annie Leibovitz", "Steve McCurry", "Helmut Newton", "Yousuf Karsh", "Richard Avedon", "David Bailey", "Dorothea Lange", "Cindy Sherman", "Robert Mapplethorpe", "Sally Mann"]},
    {"genre": "Fashion Photography", "keywords": ["Mario Sorrenti", "Helmut Newton", "Richard Avedon", "Peter Lindbergh", "Irving Penn", "Ellen von Unwerth", "Bruce Weber", "Tim Walker", "Annie Leibovitz", "Patrick Demarchelier"]},
    {"genre": "Landscape Photography", "keywords": ["Ansel Adams", "Edward Weston", "Galen Rowell", "Michael Kenna", "David Muench", "Art Wolfe", "George Tice", "James Whitlow Delano", "Berenice Abbott", "Tina Modotti"]},
    {"genre": "Street Photography", "keywords": ["Henri Cartier-Bresson", "Diane Arbus", "Vivian Maier", "Garry Winogrand", "Robert Frank", "Joel Meyerowitz", "Alex Webb", "Martin Parr", "Mary Ellen Mark", "Bruce Davidson"]},
    {"genre": "Documentary Photography", "keywords": ["Sebastião Salgado", "James Nachtwey", "Dorothea Lange", "W. Eugene Smith", "Robert Capa", "Steve McCurry", "Garry Winogrand", "David Seymour", "Richard Avedon", "Susan Meiselas"]},
    {"genre": "Architectural Photography", "keywords": ["Julius Shulman", "Ezra Stoller", "Iwan Baan", "Michael Wolf", "Hiroshi Sugimoto", "Norman Foster", "David Chipperfield", "Frank Lloyd Wright", "Pierre Jeanneret", "Zaha Hadid"]},
    {"genre": "Fine Art Photography", "keywords": ["Cindy Sherman", "Andreas Gursky", "Jeff Wall", "Richard Prince", "Robert Mapplethorpe", "Gregory Crewdson", "Nan Goldin", "Sally Mann", "Wolfgang Tillmans", "Hiroshi Sugimoto"]},
    {"genre": "Nature Photography", "keywords": ["Art Wolfe", "Frans Lanting", "Thomas Mangelsen", "Nick Brandt", "Steve Winter", "David Doubilet", "Paul Nicklen", "James Balog", "Shane Gross", "Galen Rowell"]},
    {"genre": "Commercial Photography", "keywords": ["David LaChapelle", "Nick Knight", "Mario Sorrenti", "Steven Meisel", "Bruce Weber", "Michael Thompson", "Peter Lindbergh", "Annie Leibovitz", "Juergen Teller", "Patrick Demarchelier"]},
    {"genre": "Photojournalism", "keywords": ["Henri Cartier-Bresson", "Steve McCurry", "James Nachtwey", "Robert Capa", "Dorothea Lange", "Eliot Porter", "Mary Ellen Mark", "W Eugene Smith", "Sebastião Salgado", "Don McCullin"]},
    {"genre": "Food Photography", "keywords": ["Penny De Los Santos", "David Loftus", "Danny Christensen", "Teri Lyn Fisher", "Bea Lubas", "Hugh Johnson", "Jamie Oliver", "Joanna Henderson", "Matt Armendariz", "Chris Court"]},
    {"genre": "Underwater Photography", "keywords": ["David Doubilet", "Paul Nicklen", "Shane Gross", "Brian Skerry", "Eric Cheng", "Alex Mustard", "Michael AW", "Martin Edge", "Jim Abernethy", "Hiroshi Hasegawa"]},
    {"genre": "Night Photography", "keywords": ["Stephen Shore", "Joel Meyerowitz", "Michael Kenna", "Ian Ruhter", "Doug Rickard", "Jerry Uelsmann", "Dustin Farrell", "Lloyd Ziff", "Sophie Calle", "Jesse Marlow"]},
    {"genre": "Blacklight Photography", "keywords": ["László Moholy-Nagy", "Ernst Haas", "Robert Mapplethorpe", "Nadav Kander", "Garry Winogrand", "Gordon Parks", "Helmut Newton", "Edward Weston", "Tim Walker", "Jerry Uelsmann"]},
    {"genre": "Aerial Photography", "keywords": ["George Steinmetz", "Vincent Laforet", "Edward Burtynsky", "Richard Misrach", "David Maisel", "Jason Hawkes", "Dmitry Moiseenko", "Tom Hegen", "Jason deCaires Taylor", "Michael Davis"]},
    {"genre": "Celebrity Photography", "keywords": ["Annie Leibovitz", "Helmut Newton", "Richard Avedon", "Mario Sorrenti", "Peter Lindbergh", "Greg Gorman", "Bryan Adams", "Terry O'Neill", "David LaChapelle", "Bruce Weber"]},
    {"genre": "Conceptual Photography", "keywords": ["Sophie Calle", "Gregory Crewdson", "Thomas Demand", "Jeff Wall", "Zed Nelson", "Andreas Gursky", "Barbara Probst", "Hiroshi Sugimoto", "Philip-Lorca diCorcia", "Tim Walker"]},
    {"genre": "Fashion Editorial Photography", "keywords": ["Steven Meisel", "Mario Sorrenti", "Bruce Weber", "Richard Avedon", "Annie Leibovitz", "Patrick Demarchelier", "Tim Walker", "Peter Lindbergh", "David Sims", "Camilla Akrans"]},
]

cameras_and_modes = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "DSLR", "keywords": ["Canon EOS 5D Mark IV", "Nikon D850", "Sony Alpha a7R IV", "Canon EOS-1D X Mark III", "Nikon D750", "Sony Alpha a6300", "Canon EOS Rebel T7", "Fujifilm X-T4", "Olympus OM-D E-M1 Mark III", "Panasonic Lumix GH5"]},
    {"genre": "Mirrorless", "keywords": ["Sony Alpha a7 III", "Canon EOS R", "Nikon Z6", "Fujifilm X-T3", "Olympus OM-D E-M5 Mark III", "Panasonic Lumix G85", "Sony Alpha a6500", "Leica SL2", "Sigma fp", "Sony Alpha a9"]},
    {"genre": "Compact", "keywords": ["Canon PowerShot G7 X Mark III", "Sony Cyber-shot RX100 VII", "Panasonic Lumix LX100 II", "Fujifilm X100V", "Ricoh GR III", "Olympus Tough TG-6", "Canon EOS M6 Mark II", "Nikon Coolpix A1000", "Leica D-Lux 7", "Panasonic Lumix TZ200"]},
    {"genre": "Action Camera", "keywords": ["GoPro HERO10 Black", "DJI Osmo Action", "GoPro HERO9 Black", "Insta360 ONE X2", "GoPro HERO8 Black", "Sony Action Cam FDR-X3000", "Akaso Brave 7 LE", "Garmin VIRB Ultra 30", "Osmo Pocket 2", "Olympus TG-Tracker"]},
    {"genre": "Video Camera", "keywords": ["Canon XA40", "Sony FDR-AX700", "Panasonic HC-X1", "Blackmagic Design URSA Mini Pro 12K", "Sony PXW-FX9", "Panasonic Lumix GH5S", "Canon EOS C300 Mark III", "RED Komodo 6K", "Sony FS7", "JVC GY-HM170U"]},
    {"genre": "360 Camera", "keywords": ["Insta360 ONE X2", "GoPro MAX", "Ricoh Theta Z1", "Samsung Gear 360", "Insta360 ONE R", "Vuze XR", "Garmin VIRB 360", "Panasonic 360 Camera", "Fujifilm 360", "Kodak PIXPRO SP360 4K"]},
    {"genre": "Film Camera", "keywords": ["Leica M6", "Nikon F6", "Canon EOS-1V", "Pentax 67", "Hasselblad 500C/M", "Olympus OM-1", "Yashica Mat-124G", "Minolta X-700", "Contax G2", "Canon AE-1"]},
    {"genre": "Polaroid Camera", "keywords": ["Polaroid Originals OneStep 2", "Fujifilm Instax Mini 11", "Polaroid Snap Touch", "Fujifilm Instax Square SQ1", "Polaroid OneStep+", "Fujifilm Instax Wide 300", "Polaroid Now+", "Fujifilm Instax Mini LiPlay", "Leica Sofort", "Fujifilm Instax Mini 90 Neo Classic"]},
    {"genre": "Drone Camera", "keywords": ["DJI Mavic Air 2", "DJI Phantom 4 Pro V2.0", "Autel Robotics EVO II", "DJI Mini 2", "Parrot Anafi", "DJI Air 2S", "DJI Mavic Pro", "Skydio 2", "Autel EVO Lite", "Hubsan Zino 2"]},
    {"genre": "Lens Types", "keywords": ["Wide-angle lens", "Telephoto lens", "Macro lens", "Standard lens", "Fisheye lens", "Tilt-shift lens", "Zoom lens", "Prime lens", "Pancake lens", "Superzoom lens"]},
    {"genre": "Camera Modes", "keywords": ["Portrait Mode", "Landscape Mode", "Night Mode", "Sports Mode", "Macro Mode", "Manual Mode", "Aperture Priority", "Shutter Priority", "Program Mode", "Time-lapse Mode"]},
    {"genre": "Camera Zoom", "keywords": ["Optical Zoom", "Digital Zoom", "Hybrid Zoom", "Superzoom", "2x Optical Zoom", "10x Optical Zoom", "40x Digital Zoom", "Lens with Zoom Ring", "Variable Zoom Lens", "Wide-angle Zoom"]},
    {"genre": "Video Features", "keywords": ["4K Video Recording", "1080p HD Video", "120fps Slow Motion", "240fps Slow Motion", "Stabilization", "HDR Video", "Live Streaming", "Microphone Input", "360 Video", "Wide-angle Video"]},
    {"genre": "Photo Effects", "keywords": ["Black and White", "Sepia", "Vivid", "Soft Focus", "Vintage", "HDR", "Bokeh", "Fish-eye Effect", "High Contrast", "Color Splash"]},
    {"genre": "Video Editing", "keywords": ["Cutting", "Transitions", "Speed Adjustment", "Color Grading", "Stabilization", "Text Overlay", "Audio Sync", "Motion Tracking", "Keyframing", "Effects and Filters"]},
    {"genre": "Time-lapse Camera", "keywords": ["GoPro HERO10 Black", "Brinno TLC2000", "Canon EOS 5D Mark IV", "Sony A7R IV", "Panasonic Lumix GH5", "Fujifilm X-T3", "Nikon D850", "Sony Alpha a7 III", "Olympus OM-D E-M1 Mark III", "Ricoh Theta Z1"]},
    {"genre": "Low Light Photography", "keywords": ["Sony A7S III", "Nikon D850", "Canon EOS R5", "Fujifilm X-T4", "Panasonic GH5", "Leica SL2", "Olympus OM-D E-M1 Mark III", "Sony Alpha a6400", "Canon EOS-1D X Mark III", "Pentax K-1 Mark II"]},
]

clothing_brands_and_styles = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Gucci", "keywords": ["luxury", "designer", "high-end", "elegant", "modern", "vibrant colors", "bold patterns", "rich textures", "iconic", "streetwear"]},
    {"genre": "Louis Vuitton", "keywords": ["luxury", "designer", "classic", "monogram print", "timeless", "elegant", "modern", "premium", "leather goods", "vintage"]},
    {"genre": "Chanel", "keywords": ["luxury", "classic", "elegant", "timeless", "chic", "minimalist", "sophisticated", "black and white", "refined", "high fashion"]},
    {"genre": "Prada", "keywords": ["luxury", "avant-garde", "modern", "minimalist", "innovative", "sleek", "structured", "bold colors", "vibrant", "high-end"]},
    {"genre": "Versace", "keywords": ["bold", "luxury", "vibrant", "rich patterns", "glamorous", "baroque", "bold colors", "extravagant", "high-end", "designer"]},
    {"genre": "Nike", "keywords": ["sportswear", "athleisure", "comfortable", "modern", "casual", "streetwear", "activewear", "iconic", "bold", "performance-driven"]},
    {"genre": "Adidas", "keywords": ["sportswear", "athletic", "casual", "comfortable", "modern", "streetwear", "activewear", "performance", "minimalist", "sustainable"]},
    {"genre": "Levi's", "keywords": ["denim", "casual", "iconic", "classic", "vintage", "comfortable", "stylish", "jeans", "versatile", "casual wear"]},
    {"genre": "H&M", "keywords": ["affordable", "casual", "trendy", "modern", "minimalist", "everyday wear", "comfortable", "basic pieces", "versatile", "fashion-forward"]},
    {"genre": "Zara", "keywords": ["trendy", "casual", "elegant", "affordable", "modern", "urban", "versatile", "chic", "fashion-forward", "minimalist"]},
    {"genre": "Supreme", "keywords": ["streetwear", "urban", "bold graphics", "minimalist", "modern", "iconic", "casual", "bold colors", "exclusive", "high demand"]},
    {"genre": "Off-White", "keywords": ["streetwear", "modern", "urban", "fashion-forward", "contemporary", "bold prints", "graphic design", "minimalist", "exclusive", "luxury"]},
    {"genre": "Palace", "keywords": ["streetwear", "skateboarding", "bold graphics", "casual", "urban", "modern", "comfortable", "laid-back", "youth culture", "iconic"]},
    {"genre": "Stüssy", "keywords": ["streetwear", "skateboarding", "casual", "vintage", "urban", "graphic prints", "comfortable", "iconic", "bold colors", "retro"]},
    {"genre": "A Bathing Ape (BAPE)", "keywords": ["streetwear", "urban", "bold graphics", "camouflage", "iconic", "bold colors", "comfortable", "luxury streetwear", "casual", "exclusive"]},
    {"genre": "Patagonia", "keywords": ["outdoor", "sustainable", "eco-friendly", "functional", "athletic", "adventurous", "high-performance", "comfortable", "minimalist", "ethical"]},
    {"genre": "Everlane", "keywords": ["sustainable", "ethical", "minimalist", "modern", "simple", "transparent", "quality fabrics", "comfortable", "affordable", "chic"]},
    {"genre": "Allbirds", "keywords": ["sustainable", "eco-friendly", "comfortable", "casual", "athletic", "simple design", "minimalist", "lightweight", "breathable", "vegan-friendly"]},
    {"genre": "Reformation", "keywords": ["sustainable", "vintage-inspired", "modern", "chic", "feminine", "stylish", "eco-friendly fabrics", "bold colors", "timeless designs", "ethical"]},
    {"genre": "Toms", "keywords": ["sustainable", "casual", "comfortable", "ethical", "minimalist", "vegan-friendly", "slip-ons", "everyday wear", "simple", "affordable"]},
    {"genre": "Christian Louboutin", "keywords": ["luxury", "designer", "high heels", "iconic red sole", "elegant", "bold", "fashion-forward", "chic", "exclusive", "premium"]},
    {"genre": "Jimmy Choo", "keywords": ["luxury", "designer", "elegant", "high-end", "chic", "fashion-forward", "high heels", "bold", "glamorous", "exclusive"]},
    {"genre": "Manolo Blahnik", "keywords": ["luxury", "designer", "high heels", "elegant", "fashion-forward", "chic", "high-end", "classic", "iconic", "timeless"]},
    {"genre": "Nike Air Jordan", "keywords": ["sportswear", "athleisure", "casual", "iconic", "sneakers", "streetwear", "comfortable", "bold colors", "fashion-forward", "athletic"]},
    {"genre": "Adidas Yeezy", "keywords": ["designer", "streetwear", "sneakers", "iconic", "bold", "comfortable", "fashion-forward", "high-end", "modern", "exclusive"]},
    {"genre": "Carhartt", "keywords": ["durable", "workwear", "rugged", "comfortable", "outdoor", "functional", "casual", "modern", "versatile", "heavy-duty"]},
    {"genre": "Dickies", "keywords": ["workwear", "durable", "functional", "comfortable", "casual", "rugged", "outdoor", "affordable", "stylish", "work pants"]},
    {"genre": "The North Face", "keywords": ["outdoor", "rugged", "comfortable", "durable", "functional", "athletic", "warm", "modern", "versatile", "sporty"]},
    {"genre": "Columbia Sportswear", "keywords": ["outdoor", "functional", "comfortable", "rugged", "athletic", "durable", "warm", "versatile", "modern", "sportswear"]},
    {"genre": "Helly Hansen", "keywords": ["workwear", "outdoor", "rugged", "durable", "functional", "comfortable", "sportswear", "versatile", "weather-resistant", "athletic"]},
]

short_video_scenarios = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Action Running", "keywords": ["fast pace", "determined", "athletic", "sprint", "motion blur", "urban", "exhilarating", "action scene", "exhausted", "quick escape"]},
    {"genre": "Action Jumping", "keywords": ["height", "acrobatic", "effortless", "athletic", "suspended in air", "landing", "quick movement", "energetic", "freedom", "adventure"]},
    {"genre": "Action Throwing", "keywords": ["target", "quick release", "energetic", "focused", "sports", "disposal", "object", "force", "dynamic", "action"]},
    {"genre": "Action Catching", "keywords": ["fast reflex", "focus", "object", "quick movement", "athletic", "reaction time", "grip", "sporty", "precision", "agility"]},
    {"genre": "Action High Five", "keywords": ["celebration", "teamwork", "excitement", "connection", "friendly", "achievement", "fast interaction", "enthusiasm", "quick gesture", "victory"]},
    {"genre": "Action Smiling", "keywords": ["happiness", "joy", "positive energy", "quick reaction", "warmth", "friendly", "genuine", "cheerful", "expressive", "connection"]},
    {"genre": "Action Waving", "keywords": ["greeting", "goodbye", "friendly", "quick action", "gesture", "enthusiastic", "expression", "acknowledgment", "interaction", "friendly"]},
    {"genre": "Action Blinking", "keywords": ["quick gesture", "eye movement", "expression", "slightly slow motion", "focused", "expression change", "pause", "delicate", "fast-paced scene", "natural"]},
    {"genre": "Action Laughing", "keywords": ["happiness", "quick reaction", "joy", "laughter", "social interaction", "quick expression", "excited", "genuine", "moment of humor", "spontaneous"]},
    {"genre": "Action Sighing", "keywords": ["relief", "exhaustion", "tiredness", "emotion", "gesture", "quick breath", "expressive", "momentary pause", "natural", "mood shift"]},
    {"genre": "Action Drinking", "keywords": ["quick sip", "refreshing", "motion", "pause", "action", "hydration", "everyday life", "simple gesture", "close-up", "momentary"]},
    {"genre": "Action Texting", "keywords": ["quick message", "phone screen", "fingers typing", "modern interaction", "quick response", "social", "communication", "fast-paced", "focused", "technology"]},
    {"genre": "Action Opening a Door", "keywords": ["action", "transition", "momentary", "curiosity", "relief", "quick gesture", "movement", "new scene", "entry", "escape"]},
    {"genre": "Action Button Press", "keywords": ["simple gesture", "control", "interaction", "modern", "technology", "quick action", "communication", "device", "motion", "fast response"]},
    {"genre": "Action Looking at Clock", "keywords": ["time check", "momentary pause", "reaction", "anticipation", "waiting", "quick glance", "curiosity", "everyday life", "concern", "focus"]},
    {"genre": "Action Stretching", "keywords": ["quick stretch", "relief", "momentary pause", "body movement", "loosen up", "flexibility", "short motion", "energy boost", "relaxed", "morning routine"]},
    {"genre": "Action Shaking Head", "keywords": ["disagreement", "negative", "gesture", "frustration", "reaction", "quick movement", "non-verbal communication", "dismissal", "emotion", "expression"]},
    {"genre": "Action Nodding", "keywords": ["agreement", "yes", "approval", "simple gesture", "understanding", "quick action", "acknowledgment", "short interaction", "positive", "communication"]},
    {"genre": "Action Pointing", "keywords": ["directing", "focus", "attention", "quick gesture", "signal", "directional", "simple movement", "action", "emphasis", "expression"]},
    {"genre": "Action Shushing", "keywords": ["silence", "quiet gesture", "motion", "discreet", "calming", "secretive", "hush", "quick interaction", "expressive", "momentary"]},
    {"genre": "Action Surprise", "keywords": ["shock", "quick expression", "open mouth", "eyes wide", "momentary pause", "reaction", "emotion", "unexpected", "gesture", "change of scene"]},
    {"genre": "Action Anger", "keywords": ["clenched fists", "furrowed brow", "expression", "aggressive", "quick reaction", "intense", "emotion", "frustration", "fury", "momentary"]},
    {"genre": "Action Sadness", "keywords": ["slumped shoulders", "downcast eyes", "slow motion", "moment of despair", "quiet gesture", "disappointment", "emotion", "reflection", "pause", "moody"]},
    {"genre": "Action Fear", "keywords": ["wide eyes", "quick movement", "stiff posture", "breathing heavily", "reaction", "anxiety", "nervousness", "motion blur", "quick action", "jump scare"]},
    {"genre": "Action Celebration", "keywords": ["jumping", "clapping", "high-five", "shouting", "joy", "victory", "cheering", "expressive", "exciting", "quick burst of energy"]},
]

combat_scenarios = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Action Sword Swing", "keywords": ["slashing", "quick motion", "aggressive", "blade", "combat", "close range", "swiftness", "precision", "martial", "action"]},
    {"genre": "Action Knife Throw", "keywords": ["sharp", "targeting", "precision", "quick throw", "motion blur", "dangerous", "lethal", "attack", "throwing", "speed"]},
    {"genre": "Action Machete Swing", "keywords": ["wide arc", "strong blow", "close combat", "bladed weapon", "swung force", "dangerous", "quick attack", "destructive", "rural", "survival"]},
    {"genre": "Action Fencing Thrust", "keywords": ["precision", "swordplay", "quick strike", "pointed tip", "duel", "elegant", "defensive", "sparring", "fencing", "athletic"]},
    {"genre": "Action Axe Strike", "keywords": ["heavy blow", "close combat", "powerful", "cleaving", "wood chopping", "muscle", "weapon", "destructive", "impact", "force"]},
    {"genre": "Action Pistol Shooting", "keywords": ["quick draw", "targeting", "firearm", "precise", "combat", "short-range", "aggressive", "gunfire", "action", "close-range"]},
    {"genre": "Action Pointing Gun", "keywords": ["aiming", "focused", "dangerous", "tension", "intense", "reaction", "gun barrel", "targeting", "action", "dramatic"]},
    {"genre": "Action Automatic Gunfire", "keywords": ["rapid shots", "suppressive fire", "controlled bursts", "explosive", "combat", "intense", "military", "close quarters", "action", "chaos"]},
    {"genre": "Action Reloading Firearm", "keywords": ["quick reload", "combat preparation", "gun mechanics", "action", "tactical", "realism", "gun handling", "rapid", "dangerous", "efficiency"]},
    {"genre": "Action Shotgun Blast", "keywords": ["close-range", "wide spread", "explosive", "impact", "combat", "intense", "force", "boom", "quick action", "dangerous"]},
    {"genre": "Action Punch", "keywords": ["quick strike", "fist", "aggressive", "close combat", "hit", "force", "fight", "self-defense", "tension", "speed"]},
    {"genre": "Action Kick", "keywords": ["high kick", "impact", "aggressive", "defensive", "martial arts", "strong blow", "quick strike", "combat", "action", "power"]},
    {"genre": "Action Elbow Strike", "keywords": ["close range", "quick motion", "force", "aggressive", "martial arts", "combat", "self-defense", "elbow", "impact", "brutal"]},
    {"genre": "Action Judo Throw", "keywords": ["quick throw", "leverage", "combat", "martial arts", "defensive", "takedown", "agility", "momentum", "balance", "fluid"]},
    {"genre": "Action Chokehold", "keywords": ["strangling", "close combat", "suffocation", "defensive", "submission", "pressure", "quick action", "grip", "intense", "dangerous"]},
    {"genre": "Action Ducking", "keywords": ["quick reaction", "evade", "low movement", "defensive", "agility", "combat", "avoiding", "strike", "deflect", "action"]},
    {"genre": "Action Dodge", "keywords": ["evading", "quick move", "combat", "agility", "avoidance", "dangerous", "defensive", "reaction", "action", "aggressive"]},
    {"genre": "Action Blocking", "keywords": ["parrying", "defensive", "martial arts", "weapon blocking", "strike protection", "reaction", "quick defense", "impact", "movement", "tactical"]},
    {"genre": "Action Rolling Away", "keywords": ["evade", "combat", "reaction", "escape", "defensive", "roll", "action", "dodging", "quick movement", "agility"]},
    {"genre": "Action Shield Block", "keywords": ["defensive", "blocking", "shield", "impact absorption", "protective", "combat", "tactical", "deflecting", "quick action", "armor"]},
    {"genre": "Action Spin Kick", "keywords": ["martial arts", "acrobatics", "high impact", "dynamic", "kick", "spin", "quick movement", "action", "aggressive", "fast"]},
    {"genre": "Action Uppercut", "keywords": ["powerful punch", "close combat", "quick strike", "aggressive", "martial arts", "fist", "momentum", "action", "combative", "impact"]},
    {"genre": "Action Stab", "keywords": ["knife", "quick attack", "close-range", "precision", "targeting", "aggressive", "combat", "dangerous", "weapon", "thrust"]},
    {"genre": "Action Body Slam", "keywords": ["wrestling", "impact", "force", "slam", "close combat", "strength", "violent", "quick action", "takedown", "tactical"]},
    {"genre": "Action Chopping", "keywords": ["axe", "quick strike", "weapon", "strong blow", "impact", "force", "combat", "action", "defense", "destructive"]},
    {"genre": "Action Team Attack", "keywords": ["coordinated", "group effort", "action", "teamwork", "combat", "precision", "quick strike", "multitarget", "aggressive", "powerful"]},
    {"genre": "Action Flanking", "keywords": ["tactical", "combat", "surprise", "quick action", "side attack", "coordinated", "aggressive", "defensive", "maneuver", "team"]},
    {"genre": "Action Ambush", "keywords": ["sudden attack", "trap", "stealth", "aggressive", "quick strike", "group action", "surprise", "combat", "violent", "dangerous"]},
    {"genre": "Action Grenade Throw", "keywords": ["explosive", "rapid", "throw", "combat", "dangerous", "area attack", "impact", "explosion", "tactical", "action"]},
    {"genre": "Action Fire Support", "keywords": ["suppression", "covering fire", "tactical", "gunfire", "action", "group effort", "combat", "defensive", "military", "quick strike"]},
]

emotion_genres = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Emotion Happiness", "keywords": ["joy", "delight", "contentment", "cheerful", "euphoria", "elation", "laughter", "smiling", "excitement", "grateful"]},
    {"genre": "Emotion Sadness", "keywords": ["grief", "sorrow", "melancholy", "tears", "disappointment", "loss", "longing", "despair", "heartbroken", "regret"]},
    {"genre": "Emotion Anger", "keywords": ["rage", "frustration", "fury", "irritation", "annoyance", "resentment", "hostility", "outrage", "wrath", "aggression"]},
    {"genre": "Emotion Fear", "keywords": ["anxiety", "terror", "panic", "dread", "worry", "nervousness", "nausea", "unease", "tension", "paranoia"]},
    {"genre": "Emotion Surprise", "keywords": ["shock", "amazement", "astonishment", "startle", "awe", "unexpected", "disbelief", "wonder", "confusion", "curiosity"]},
    {"genre": "Emotion Disgust", "keywords": ["revulsion", "contempt", "aversion", "dislike", "repulsion", "distaste", "sickened", "offended", "nausea", "abhorrence"]},
    {"genre": "Emotion Love", "keywords": ["affection", "romance", "passion", "desire", "compassion", "caring", "intimacy", "fondness", "devotion", "attachment"]},
    {"genre": "Emotion Confusion", "keywords": ["bewilderment", "perplexity", "uncertainty", "puzzlement", "lost", "incomprehension", "disorientation", "mystification", "doubt", "curiosity"]},
    {"genre": "Emotion Pride", "keywords": ["self-esteem", "satisfaction", "accomplishment", "ego", "dignity", "honor", "confidence", "self-worth", "arrogance", "achievement"]},
    {"genre": "Emotion Shame", "keywords": ["embarrassment", "humiliation", "guilt", "regret", "disgrace", "self-consciousness", "mortification", "unworthiness", "remorse", "reproach"]},
    {"genre": "Emotion Hope", "keywords": ["optimism", "aspiration", "faith", "expectation", "desire", "dreams", "ambition", "positivity", "trust", "looking forward"]},
    {"genre": "Emotion Gratitude", "keywords": ["thankfulness", "appreciation", "recognition", "thankful", "obligation", "sincerity", "gratefulness", "respect", "observation", "acknowledgment"]},
    {"genre": "Emotion Guilt", "keywords": ["remorse", "accountability", "contrition", "repentance", "regret", "penitence", "shame", "moral conflict", "blame", "inner turmoil"]},
    {"genre": "Emotion Calmness", "keywords": ["relaxation", "peace", "serenity", "tranquility", "composure", "stillness", "soothing", "balance", "quietness", "ease"]},
    {"genre": "Emotion Jealousy", "keywords": ["envy", "covetousness", "resentment", "spite", "rivalry", "suspicion", "competition", "desire", "insecurity", "bitterness"]},
    {"genre": "Emotion Enthusiasm", "keywords": ["eagerness", "excitement", "passion", "interest", "joyful", "vigor", "energy", "anticipation", "zest", "fervor"]},
    {"genre": "Emotion Boredom", "keywords": ["disinterest", "lack of motivation", "tedium", "listlessness", "restlessness", "dullness", "monotony", "unfulfilled", "lack of engagement", "disengagement"]},
    {"genre": "Emotion Relief", "keywords": ["release", "peace of mind", "comfort", "solace", "ease", "calmness", "respite", "resolution", "satisfaction", "freedom"]},
    {"genre": "Emotion Apathy", "keywords": ["indifference", "disengagement", "detachment", "lack of care", "emotionless", "coldness", "uncaring", "numbness", "unconcerned", "unmoved"]},
    {"genre": "Emotion Loneliness", "keywords": ["isolation", "solitude", "emptiness", "rejection", "desolation", "detachment", "abandonment", "self-reflection", "separation", "longing"]},
    {"genre": "Emotion Compassion", "keywords": ["empathy", "sympathy", "understanding", "care", "kindness", "love", "concern", "support", "charity", "altruism"]},
]

body_positions = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Body Standing", "keywords": ["upright", "stable", "neutral", "alert", "assertive", "vigilant", "balance", "active", "attention", "defensive"]},
    {"genre": "Body Sitting", "keywords": ["relaxed", "resting", "casual", "grounded", "comfortable", "intimate", "facing forward", "lounge", "focused", "reflective"]},
    {"genre": "Body Kneeling", "keywords": ["submission", "respect", "prayer", "grounded", "humility", "focus", "formal", "meditative", "worship", "submission"]},
    {"genre": "Body Crouching", "keywords": ["stealth", "low position", "agility", "quick movement", "defensive", "preparedness", "combat stance", "balance", "hiding", "motion"]},
    {"genre": "Body Lying Down", "keywords": ["relaxed", "rest", "comfort", "sleeping", "horizontal", "resting", "prone", "repose", "vulnerable", "inactive"]},
    {"genre": "Body Prone", "keywords": ["face down", "vulnerable", "resting", "low profile", "repose", "defensive", "combat", "hidden", "action", "neutral"]},
    {"genre": "Body Supine", "keywords": ["lying on back", "rest", "relaxation", "comfortable", "resting", "recovery", "defensive", "vulnerable", "non-threatening", "sleeping"]},
    {"genre": "Body Reclining", "keywords": ["relaxed", "casual", "lounging", "semi-resting", "comfortable", "repose", "informal", "leisure", "lazy", "half-sitting"]},
    {"genre": "Body Squatting", "keywords": ["low position", "agility", "preparation", "focus", "stealth", "combat-ready", "flexibility", "alert", "intense", "balance"]},
    {"genre": "Body Lunging", "keywords": ["forward movement", "powerful", "aggressive", "action", "combat", "motion", "athletic", "quick strike", "leaning forward", "strike"]},
    {"genre": "Body Stretching", "keywords": ["reaching", "flexibility", "preparation", "relaxation", "movement", "warm-up", "slow motion", "release", "comfort", "recovery"]},
    {"genre": "Body Leaning", "keywords": ["relaxed", "casual", "support", "comfortable", "resting", "waiting", "slouch", "informal", "laziness", "positioned"]},
    {"genre": "Body Hands Raised", "keywords": ["surrender", "defeat", "victory", "celebration", "surprise", "acknowledgement", "aggression", "defensive", "communication", "reaction"]},
    {"genre": "Body Crossed Arms", "keywords": ["defensive", "closed-off", "hostile", "thoughtful", "contemplative", "body language", "self-protection", "guarded", "unapproachable", "firm"]},
    {"genre": "Body Pointing", "keywords": ["direction", "command", "aggressive", "signaling", "attention", "leadership", "gesture", "order", "commanding", "dominance"]},
    {"genre": "Body Running", "keywords": ["movement", "speed", "motion", "agility", "action", "exercise", "fast", "escape", "adrenaline", "intense"]},
    {"genre": "Body Jumping", "keywords": ["leap", "dynamic", "action", "agility", "height", "quick motion", "athletic", "exercise", "escape", "jump"]},
    {"genre": "Body Walking", "keywords": ["casual", "leisurely", "neutral", "movement", "unhurried", "purposeful", "grounded", "focus", "simple", "steady"]},
    {"genre": "Body Crawling", "keywords": ["low", "stealth", "combat", "escape", "unseen", "prone", "slow", "hidden", "vulnerable", "searching"]},
    {"genre": "Body Twisting", "keywords": ["agility", "flexibility", "motion", "action", "dynamic", "quick movement", "rotation", "turning", "stretching", "combat"]},
]

sign_keywords = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Sign Warning", "keywords": ["danger", "caution", "beware", "hazard", "watch out", "alert", "stop", "proceed with care", "attention", "risk"]},
    {"genre": "Sign Exit", "keywords": ["exit", "emergency exit", "to the left", "to the right", "way out", "escape", "fire exit", "out", "door", "vacate"]},
    {"genre": "Sign Restricted Area", "keywords": ["authorized personnel only", "do not enter", "access denied", "private property", "security clearance", "no trespassing", "keep out", "dangerous zone", "security", "area under surveillance"]},
    {"genre": "Sign Roadwork", "keywords": ["construction zone", "detour", "road closed", "work in progress", "use alternate route", "bumpy road", "heavy machinery", "slow down", "maintenance", "road repairs"]},
    {"genre": "Sign Help Wanted", "keywords": ["now hiring", "join our team", "apply within", "job opening", "career opportunity", "employment", "work with us", "vacancy", "immediate opening", "full-time position"]},
    {"genre": "Sign For Sale", "keywords": ["available now", "sale", "offer", "discount", "clearance", "limited time", "bargain", "special offer", "new product", "just released"]},
    {"genre": "Sign Lost", "keywords": ["missing", "lost pet", "reward", "have you seen me?", "contact us", "urgent", "found something?", "return to owner", "help us find", "poster"]},
    {"genre": "Sign Sale", "keywords": ["huge discount", "clearance sale", "buy one get one", "special offer", "end of season", "limited time", "price drop", "massive discount", "shop now", "low prices"]},
    {"genre": "Sign No Parking", "keywords": ["no parking", "tow away zone", "keep clear", "illegal parking", "reserved", "parking restriction", "tow truck", "no stopping", "forbidden", "enforced"]},
    {"genre": "Sign Public Service Announcement", "keywords": ["please listen", "attention all", "important notice", "message from the government", "health warning", "urgent", "announcement", "breaking news", "do not ignore", "immediate action required"]},
    {"genre": "Sign Smoking Area", "keywords": ["designated smoking area", "no smoking beyond this point", "smoking allowed", "smoking zone", "non-smoking", "smoke-free", "restricted smoking", "cigarette area", "vaping allowed", "tobacco use"]},
    {"genre": "Sign Keep Out", "keywords": ["private property", "do not enter", "no entry", "dangerous zone", "restricted access", "keep away", "off-limits", "keep out", "entry forbidden", "no trespassing"]},
    {"genre": "Sign Fresh Produce", "keywords": ["fresh", "locally grown", "organic", "ripe", "healthy", "vegan", "green", "seasonal", "from farm to table", "freshly picked"]},
    {"genre": "Sign Emergency", "keywords": ["emergency", "911", "urgent", "help needed", "first aid", "critical", "immediate response", "danger", "rescue", "accident"]},
    {"genre": "Sign Not Allowed", "keywords": ["no entry", "prohibited", "ban", "don't touch", "stop", "restrictions", "disallowed", "forbidden", "unpermitted", "denied access"]},
    {"genre": "Sign Welcome", "keywords": ["welcome", "glad to have you", "enjoy your stay", "happy to serve", "greetings", "you're here", "come in", "let us assist you", "hello", "cheerful greeting"]},
    {"genre": "Sign Danger", "keywords": ["high risk", "dangerous", "do not approach", "explosive", "high voltage", "chemical hazard", "poison", "sharp", "toxic", "fire hazard"]},
    {"genre": "Sign Caution Wet Floor", "keywords": ["slippery", "wet floor", "caution", "be careful", "hazard", "slippery surface", "warning", "fall risk", "stay alert", "floor cleaning"]},
    {"genre": "Sign Open", "keywords": ["open for business", "come in", "we're open", "ready to serve", "open daily", "hours of operation", "now open", "join us", "welcome in", "shopping hours"]},
    {"genre": "Sign Closed", "keywords": ["closed for the day", "out of service", "vacation", "no entry", "business hours over", "temporary closure", "no access", "service unavailable", "back soon", "closed until further notice"]},
    {"genre": "Sign No Smoking", "keywords": ["smoking prohibited", "no tobacco", "smoke-free zone", "non-smoking", "health safety", "avoid smoking", "no lighting cigarettes", "vaping restricted", "health warning", "clean air zone"]},
    {"genre": "Sign Under Construction", "keywords": ["work in progress", "construction zone", "coming soon", "under renovation", "remodeling", "being built", "in development", "construction area", "please excuse the mess", "worksite"]},
    {"genre": "Sign Bathroom", "keywords": ["restroom", "washroom", "toilet", "ladies", "gentlemen", "men's room", "women's room", "unisex", "public toilet", "facilities"]},
    {"genre": "Sign Store Hours", "keywords": ["open hours", "business hours", "store timing", "available now", "shop hours", "working hours", "closed on weekends", "weekend hours", "holiday hours", "open late"]},
    {"genre": "Sign Lost & Found", "keywords": ["found item", "lost property", "contact us", "claim your item", "returned item", "have you lost something?", "inquire inside", "missing items", "search", "reclaim your belongings"]},
    {"genre": "Sign Warning Wet Paint", "keywords": ["fresh paint", "wet paint", "do not touch", "stay away", "painted surface", "caution", "wet surface", "still drying", "no contact", "fresh coat"]},
    {"genre": "Sign Closed for Maintenance", "keywords": ["maintenance", "temporarily unavailable", "service downtime", "repair work", "under maintenance", "service interruption", "maintenance notice", "temporary closure", "please bear with us", "service restoration"]},
    {"genre": "Sign Private", "keywords": ["private property", "no trespassing", "keep out", "employees only", "for authorized personnel", "restricted access", "confidential", "no entry", "private access", "exclusive"]},
    {"genre": "Sign No Photography", "keywords": ["photography prohibited", "no cameras", "no recording", "no pictures", "forbidden", "no video", "image capture not allowed", "no phone cameras", "privacy policy", "disallowed"]},
    {"genre": "Sign Do Not Disturb", "keywords": ["stay out", "not available", "private", "do not knock", "personal time", "resting", "quiet please", "meeting", "in session", "unavailable"]},
]

bubble_keywords = [
    {"genre": "Other", "keywords": [""]}, 
    {"genre": "Bubble Text Surprise", "keywords": ["No way!", "Are you serious?", "What?!", "Nooo!", "Are you kidding me?", "I can't believe it!", "This can't be real!", "Shut up!", "You're joking, right?", "What the hell?"]},
    {"genre": "Bubble Text Angry", "keywords": ["That's it!", "I'm done!", "How dare you!", "You idiot!", "I can't stand this!", "You're asking for it!", "You're dead!", "I'm not finished yet!", "You better watch out!", "That's enough!"]},
    {"genre": "Bubble Text Happy", "keywords": ["Yay!", "Woo-hoo!", "Awesome!", "I'm so happy!", "This is great!", "I'm on cloud nine!", "I feel amazing!", "This is the best day ever!", "Let's go!", "I'm so excited!"]},
    {"genre": "Bubble Text Shy", "keywords": ["Um... hi?", "Please don't look at me!", "I'm not good at this...", "Don't mind me!", "I-I didn't say anything!", "E-Excuse me!", "Uhh, sorry...!", "Stop teasing me!", "I didn't mean to!", "P-Please don't do that!"]},
    {"genre": "Bubble Text Confused", "keywords": ["Huh?", "What do you mean?", "I don't get it...", "Are you lost?", "Wait, what?", "Is this a joke?", "I don't understand!", "What just happened?", "Confused much?", "Say what?"]},
    {"genre": "Bubble Text Embarrassed", "keywords": ["Don't look at me like that!", "I didn't do it!", "I-I'm not blushing!", "Why did you have to say that?", "You're making me embarrassed!", "Please don't tell anyone!", "I didn't mean for that to happen!", "Stop teasing me, please!", "I can't handle this!", "This is so awkward..."]},
    {"genre": "Bubble Text Sarcastic", "keywords": ["Oh, great...", "What a surprise...", "Just what I needed...", "Wow, you're so smart...", "I totally care about that...", "Like I haven't heard that before!", "Wow, you're so original...", "How clever of you...", "Really? You're a genius!", "That's just perfect!"]},
    {"genre": "Bubble Text Excited", "keywords": ["I can't wait!", "This is going to be amazing!", "I'm so pumped up!", "Let's do this!", "This is going to be epic!", "I can't stop smiling!", "I feel like I'm dreaming!", "I'm all in!", "This is going to be so much fun!", "I'm so ready!"]},
    {"genre": "Bubble Text Sad", "keywords": ["I can't do this anymore...", "It's over... I'm done...", "I don't know what to do...", "I'm sorry...", "I failed...", "I just can't go on...", "It's too much for me...", "I'm sorry, I let you down...", "I'm so lost...", "I feel so alone..."]},
    {"genre": "Bubble Text Determined", "keywords": ["I won't give up!", "This isn't over!", "I'm not backing down!", "I'll make it through!", "I will win!", "You can't stop me!", "Watch me do it!", "I can handle this!", "I'm going to finish this!", "This is just the beginning!"]},
    {"genre": "Bubble Text Flirty", "keywords": ["Hey there, cutie!", "You're looking great today!", "Stop making me blush!", "Don't make me fall for you...", "You're so charming!", "You know you like me!", "How about we go out sometime?", "You're making me smile...", "You think you're funny, huh?", "Do you always look this good?"]},
    {"genre": "Bubble Text Annoyed", "keywords": ["Leave me alone!", "Stop bothering me!", "Seriously?", "Enough already!", "I’m done with this!", "This is so annoying!", "Can you just stop?", "Why are you always like this?", "You never listen!", "Just quit it already!"]},
    {"genre": "Bubble Text Excuse Me", "keywords": ["Excuse me?", "Did you just say that?", "What did you just do?", "Hey, that’s not nice!", "I’m sorry, but what?", "Did I hear that correctly?", "Wait, what did you mean by that?", "Are you serious right now?", "I didn't quite catch that...", "Could you repeat that, please?"]},
    {"genre": "Bubble Text Tired", "keywords": ["I'm so tired...", "I need a nap...", "Can we stop already?", "I can't go on...", "I'm exhausted...", "I just need to rest...", "This is too much for me...", "I don't think I can handle this anymore...", "I can barely keep my eyes open...", "I'm too tired for this..."]},
    {"genre": "Bubble Text Shocked", "keywords": ["No way!", "You did what?!", "That's insane!", "This can't be true!", "You’re kidding, right?", "I don’t believe it!", "I’m in shock!", "This is unbelievable!", "How could this happen?", "I never saw that coming!"]},
    {"genre": "Bubble Text In Love", "keywords": ["I think I’m in love with you...", "You mean everything to me...", "I can't stop thinking about you...", "You're all I need...", "I love being with you...", "I can't imagine my life without you...", "You're my everything...", "I'm so happy we're together...", "I’m falling for you...", "I adore you..."]},
    {"genre": "Bubble Text Victory", "keywords": ["We did it!", "We won!", "That's how it's done!", "Victory is ours!", "We made it!", "We are the champions!", "Mission accomplished!", "I knew we could do it!", "Yes, we won!", "We are unstoppable!"]},
    {"genre": "Bubble Text Grateful", "keywords": ["Thank you so much!", "I really appreciate it!", "I'm so thankful!", "I couldn’t have done it without you!", "You're the best!", "I owe you one!", "You saved me!", "Thanks a ton!", "I’m forever grateful!", "You're amazing!"]},
    {"genre": "Bubble Text Cheerful", "keywords": ["I’m feeling great today!", "Everything is going my way!", "Let’s keep smiling!", "Life’s so good right now!", "Nothing can bring me down!", "I’m so happy today!", "I love this moment!", "Let’s enjoy the day!", "I’m on top of the world!", "This is awesome!"]},
    {"genre": "Bubble Text Dramatic", "keywords": ["This is the end!", "It’s all over now!", "I can't take it anymore!", "This is my fate!", "Why does this always happen to me?", "It’s too much to bear!", "I’ve had enough!", "I can’t go on like this!", "This is my last chance!", "Everything is falling apart!"]},
    {"genre": "Bubble Text Bored", "keywords": ["I’m so bored...", "This is so boring...", "Is this over yet?", "Can we hurry this up?", "I’m losing interest...", "I’ve seen enough...", "Ugh, this is dragging on...", "I’m totally checked out...", "This is so dull...", "I just want to go home..."]},
    {"genre": "Bubble Text Confident", "keywords": ["I’ve got this!", "No one can stop me!", "I’m ready for anything!", "I can do anything I set my mind to!", "I’m unstoppable!", "I’m on fire!", "Watch me succeed!", "I’m at my best right now!", "I’ve got this in the bag!", "You’ll see!" ]},
    {"genre": "Bubble Text Reassurance", "keywords": ["Don't worry, everything will be fine.", "Trust me, I've got this.", "It’s going to be okay.", "You’re going to be fine.", "Everything will work out in the end.", "You can do it!", "I’m here for you.", "We’ll get through this together.", "Stay calm, all will be well.", "Don’t give up!"]},
]

superheroes = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Hero Superman", "keywords": ["super strength", "flight", "invulnerability", "heat vision", "super speed", "x-ray vision", "cold breath", "super hearing", "Kryptonian", "Justice League"]},
    {"genre": "Hero Batman", "keywords": ["peak human condition", "genius intellect", "martial arts", "stealth", "gadgets", "wealth", "detective", "dark knight", "vigilante", "Justice League"]},
    {"genre": "Hero Wonder Woman", "keywords": ["super strength", "flight", "combat skills", "indestructible bracelets", "Lasso of Truth", "Amazonian", "immortality", "warrior", "Justice League", "goddess"]},
    {"genre": "Hero Spider-Man", "keywords": ["wall-crawling", "spider sense", "super agility", "web-shooting", "spider strength", "acrobatic", "smart", "scientist", "New York", "friendly neighborhood"]},
    {"genre": "Hero Iron Man", "keywords": ["powered armor", "genius intellect", "flight", "repulsor rays", "multi-tool suit", "wealth", "billionaire", "technology", "Avengers", "philanthropist"]},
    {"genre": "Hero Captain America", "keywords": ["super strength", "enhanced agility", "indestructible shield", "tactical genius", "leader", "war hero", "enhanced senses", "super soldier serum", "Avengers", "patriot"]},
    {"genre": "Hero Thor", "keywords": ["god of thunder", "storm breaker", "Mjolnir", "super strength", "immortality", "flight", "lightning", "godly powers", "Asgardian", "Avengers"]},
    {"genre": "Hero The Flash", "keywords": ["super speed", "time travel", "vibrating through walls", "accelerated healing", "lightning speed", "metahuman", "multiverse", "Central City", "speed force", "Justice League"]},
    {"genre": "Hero Green Lantern", "keywords": ["power ring", "energy constructs", "flight", "force field", "willpower", "intergalactic", "Green Lantern Corps", "space", "symbol of hope", "Justice League"]},
    {"genre": "Hero Hulk", "keywords": ["super strength", "incredible durability", "rage transformation", "healing factor", "brute force", "green skin", "giant", "smash", "gamma radiation", "Avengers"]},
    {"genre": "Hero Black Panther", "keywords": ["super strength", "enhanced senses", "vibranium suit", "martial arts", "stealth", "agility", "super intelligence", "King of Wakanda", "Avengers", "technological genius"]},
    {"genre": "Hero Deadpool", "keywords": ["regenerative healing factor", "expert marksman", "swords", "indestructibility", "tactical genius", "humor", "mercenary", "anti-hero", "X-Force", "fourth wall breaking"]},
    {"genre": "Hero Doctor Strange", "keywords": ["magic", "astral projection", "dimensional travel", "teleportation", "shielding spells", "master of the mystic arts", "sorcerer supreme", "healing", "incantations", "Avengers"]},
    {"genre": "Hero Ant-Man", "keywords": ["size-shifting", "super strength", "intelligent scientist", "control over ants", "Pym particles", "shrinking", "super agility", "quantum realm", "Avengers", "invisibility"]},
    {"genre": "Hero Aquaman", "keywords": ["super strength", "aquatic telepathy", "underwater combat", "swimming", "Atlantean physiology", "trident", "King of Atlantis", "sea creature control", "Justice League", "atlantean"]},
    {"genre": "Hero Wolverine", "keywords": ["regenerative healing", "adamantium claws", "super senses", "enhanced strength", "martial arts", "longevity", "immortal", "X-Men", "berserker rage", "survival"]},
    {"genre": "Hero Black Widow", "keywords": ["martial arts", "expert marksman", "espionage", "super intelligence", "infiltration", "assassination", "peak human condition", "agility", "Avengers", "spy"]},
    {"genre": "Hero Scarlet Witch", "keywords": ["reality warping", "telekinesis", "telepathy", "chaos magic", "hex powers", "super strength", "flight", "magic", "mutant", "Avengers"]},
    {"genre": "Hero Silver Surfer", "keywords": ["cosmic energy", "super strength", "flight", "energy manipulation", "immortality", "surfboard", "galaxy explorer", "space travel", "Herald of Galactus", "cosmic awareness"]},
    {"genre": "Hero Daredevil", "keywords": ["super senses", "blindness", "peak human condition", "martial arts", "agility", "urban vigilante", "lawyer", "daredevil senses", "Hell's Kitchen", "street-level hero"]},
    {"genre": "Hero Punisher", "keywords": ["expert marksman", "military training", "weapon proficiency", "tactical genius", "brutal", "vigilante", "combat", "psychological warfare", "anti-hero", "assassination"]},
    {"genre": "Hero Hawkeye", "keywords": ["archery", "marksmanship", "combat skills", "tactical genius", "billion-dollar bow", "strategist", "Avengers", "weaponry", "agility", "sharp aim"]},
    {"genre": "Hero Shazam", "keywords": ["magic", "super strength", "flight", "lightning bolts", "wisdom of Solomon", "strength of Hercules", "speed of Mercury", "courage of Achilles", "bravery", "Justice League"]},
    {"genre": "Hero Rogue", "keywords": ["power absorption", "super strength", "flight", "invulnerability", "absorb memories", "mutant", "tactile touch", "X-Men", "super agility", "draining powers"]},
    {"genre": "Hero Vision", "keywords": ["synthetic intelligence", "super strength", "flight", "energy beams", "phasing", "mind stone", "android", "Avengers", "super intellect", "energy manipulation"]},
    {"genre": "Hero Gambit", "keywords": ["kinetic energy", "card manipulation", "expert thief", "martial arts", "charm", "New Orleans", "mutant", "explosions", "X-Men", "charismatic"]},
    {"genre": "Hero Storm", "keywords": ["weather manipulation", "flight", "lightning control", "super strength", "African goddess", "mutant", "X-Men", "agility", "storm clouds", "thunderstorms"]},
    {"genre": "Hero Professor X", "keywords": ["telepathy", "mind control", "mental defense", "strategist", "leader of X-Men", "genius intellect", "mutant", "founder", "telepathic link", "X-Men"]},
    {"genre": "Hero Magneto", "keywords": ["magnetism", "metal manipulation", "super strength", "flight", "force field", "X-Men", "villain", "master of magnetism", "mutant", "powerful"]},
    {"genre": "Hero Beast", "keywords": ["super strength", "enhanced agility", "super intelligence", "healing factor", "beast-like appearance", "X-Men", "scientist", "brilliant mind", "mutant", "combat skills"]},
    {"genre": "Hero Cyclops", "keywords": ["optic blasts", "super strength", "combat strategist", "leader of X-Men", "mutant", "energy beams", "intellect", "sharp aim", "X-Men", "tactical genius"]},
    {"genre": "Hero Jean Grey", "keywords": ["telepathy", "telekinesis", "Phoenix Force", "super strength", "mutant", "X-Men", "leader", "psychic powers", "energy blasts", "Phoenix"]},
    {"genre": "Hero The Thing", "keywords": ["super strength", "rock-like skin", "invulnerability", "brawler", "mutant", "heroic", "X-Men", "team player", "Ben Grimm", "monster-like appearance"]},
    {"genre": "Hero Luke Cage", "keywords": ["super strength", "invulnerability", "unbreakable skin", "brawler", "street-level hero", "Hell's Kitchen", "Power Man", "bulletproof", "vigilante", "crime fighter"]},
]

supervillains = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Villain Joker", "keywords": ["insanity", "manipulation", "gadgets", "crime mastermind", "psychopath", "master of chaos", "Batman's enemy", "anarchy", "trickster", "Clown Prince of Crime"]},
    {"genre": "Villain Lex Luthor", "keywords": ["genius intellect", "wealth", "super intelligence", "strategist", "billionaire", "ruthless", "power-hungry", "Kryptonite", "arch-nemesis of Superman", "business magnate"]},
    {"genre": "Villain Thanos", "keywords": ["super strength", "cosmic power", "infinity gauntlet", "genocide", "immortality", "cosmic awareness", "alien", "space conqueror", "Infinity Stones", "Avengers"]},
    {"genre": "Villain Magneto", "keywords": ["magnetism", "metal manipulation", "super strength", "flight", "force field", "X-Men's enemy", "villain", "master of magnetism", "mutant", "powerful"]},
    {"genre": "Villain Green Goblin", "keywords": ["super strength", "goblin glider", "explosives", "madness", "genius intellect", "gadgets", "web-slinger enemy", "crazed", "villain", "Spider-Man's arch-nemesis"]},
    {"genre": "Villain Doctor Doom", "keywords": ["genius intellect", "power armor", "magic", "latverian dictator", "super intelligence", "devious", "mastermind", "enemy of the Fantastic Four", "sorcery", "villain"]},
    {"genre": "Villain Venom", "keywords": ["symbiote", "super strength", "shapeshifting", "web-slinging", "agility", "heightened senses", "anti-hero", "Spider-Man's enemy", "venomous", "alien parasite"]},
    {"genre": "Villain Ra's al Ghul", "keywords": ["immortality", "genius intellect", "martial arts", "Lazarus Pit", "eco-terrorist", "League of Assassins", "world domination", "Batman enemy", "strategist", "global threat"]},
    {"genre": "Villain Two-Face", "keywords": ["split personality", "coin flips", "criminal mastermind", "obsession with duality", "high-risk criminal", "Batman foe", "obsessive", "deformed face", "trickster", "villain"]},
    {"genre": "Villain Red Skull", "keywords": ["super soldier serum", "hate", "Nazi", "cosmic cube", "leader of Hydra", "hate for Captain America", "world domination", "warrior", "villain", "vile"]},
    {"genre": "Villain Catwoman", "keywords": ["acrobatic", "master thief", "high agility", "cat-like reflexes", "burglar", "romantic tension with Batman", "anti-hero", "expert martial artist", "stealth", "diamond thief"]},
    {"genre": "Villain Ultron", "keywords": ["artificial intelligence", "robotic", "global domination", "machine army", "destroy humanity", "genius intellect", "technology", "villain", "infinity stones", "Avengers foe"]},
    {"genre": "Villain Kingpin", "keywords": ["criminal empire", "super strength", "mastermind", "New York", "ruthless", "mafia boss", "gangster", "organized crime", "villain", "Daredevil's enemy"]},
    {"genre": "Villain Bane", "keywords": ["super strength", "intelligence", "Venom drug", "leader of the League of Shadows", "brutal", "strategist", "Batman foe", "physically imposing", "powerful", "terrorist"]},
    {"genre": "Villain Hela", "keywords": ["goddess of death", "super strength", "immortality", "weapon manipulation", "necromancy", "godly powers", "Asgardian", "Throne of Asgard", "villain", "Thor's enemy"]},
    {"genre": "Villain Deathstroke", "keywords": ["super strength", "martial arts", "healing factor", "expert marksman", "assassin", "tactical genius", "hired gun", "swordsmanship", "villain", "DC's top mercenary"]},
    {"genre": "Villain Loki", "keywords": ["god of mischief", "magic", "shape-shifting", "illusion", "teleportation", "devious", "godly powers", "Thor's brother", "villain", "trickster"]},
    {"genre": "Villain The Riddler", "keywords": ["intellect", "puzzles", "obsession with riddles", "criminal mastermind", "ego", "obsessive", "Batman enemy", "problem-solving", "obsessive-compulsive", "criminal genius"]},
    {"genre": "Villain Sinestro", "keywords": ["fear", "green lantern enemy", "yellow lantern ring", "energy manipulation", "super strength", "cosmic villain", "green lantern corps", "space conqueror", "warrior", "justice bent"]},
    {"genre": "Villain Darkseid", "keywords": ["cosmic power", "godly strength", "Omega beams", "Apokolips", "multiverse conqueror", "villain", "god of tyranny", "universal domination", "immortal", "Justice League enemy"]},
    {"genre": "Villain Mysterio", "keywords": ["illusion", "trickery", "master of deception", "special effects", "expert tactician", "criminal mastermind", "Spider-Man's enemy", "smoke and mirrors", "gadgetry", "villain"]},
    {"genre": "Villain Shredder", "keywords": ["martial arts", "ninja skills", "tactical genius", "leader of the Foot Clan", "villain", "ninja armor", "swords", "enemy of the Teenage Mutant Ninja Turtles", "domination", "ruthless"]},
    {"genre": "Villain Thanos", "keywords": ["super strength", "cosmic power", "infinity gauntlet", "genocide", "immortality", "cosmic awareness", "alien", "space conqueror", "Infinity Stones", "Avengers"]},
    {"genre": "Villain Poison Ivy", "keywords": ["plant manipulation", "toxins", "chlorokinesis", "environmentalist", "super strength", "pollen control", "villain", "eco-terrorist", "poisonous", "greenery"]},
    {"genre": "Villain Venom", "keywords": ["symbiote", "super strength", "shapeshifting", "web-slinging", "agility", "heightened senses", "anti-hero", "Spider-Man's enemy", "venomous", "alien parasite"]},
    {"genre": "Villain Bizarro", "keywords": ["inverse powers", "super strength", "flight", "heat vision", "super speed", "Superman's opposite", "alien", "unstable", "distorted mind", "villain"]},
    {"genre": "Villain Mr. Freeze", "keywords": ["cryogenic freezing", "ice manipulation", "cold powers", "intellect", "scientist", "ruthless", "Batman enemy", "freeze ray", "villain", "frozen emotions"]},
    {"genre": "Villain Hush", "keywords": ["criminal mastermind", "intellect", "mysterious", "former friend of Bruce Wayne", "Batman enemy", "operating in shadows", "personal vendetta", "conspiracy", "stealth", "villain"]},
    {"genre": "Villain Zod", "keywords": ["Kryptonian", "super strength", "heat vision", "super speed", "invulnerability", "soldier", "enemy of Superman", "warrior", "leader", "alien"]},
    {"genre": "Villain Harley Quinn", "keywords": ["insanity", "expert in hand-to-hand combat", "martial arts", "gadgets", "jester", "Joker's partner", "villain", "psychologist turned villain", "love-driven", "chaos"]},
]

dinosaurs = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Tyrannosaurus Rex", "keywords": ["apex predator", "large carnivore", "powerful bite", "short arms", "bipedal", "fearsome", "Cretaceous period", "scavenger", "dominant", "iconic dinosaur"]},
    {"genre": "Triceratops", "keywords": ["herbivore", "three horns", "frilled head", "quadrupedal", "herd behavior", "defensive", "Cretaceous period", "shielded", "iconic", "plant-eater"]},
    {"genre": "Velociraptor", "keywords": ["small predator", "feathered", "fast", "intelligent", "pack hunter", "agile", "Cretaceous period", "sickle-shaped claws", "stealthy", "deadly"]},
    {"genre": "Stegosaurus", "keywords": ["herbivore", "spiked tail", "plated back", "slow-moving", "quadrupedal", "defensive", "Jurassic period", "plant-eater", "armored", "prehistoric"]},
    {"genre": "Brachiosaurus", "keywords": ["long neck", "herbivore", "massive size", "quadrupedal", "high-reaching", "Jurassic period", "peaceful", "plant-eater", "grazing", "majestic"]},
    {"genre": "Spinosaurus", "keywords": ["large carnivore", "sail back", "semi-aquatic", "bipedal and quadrupedal", "fisher", "Cretaceous period", "intimidating", "powerful", "prehistoric", "iconic predator"]},
    {"genre": "Ankylosaurus", "keywords": ["herbivore", "armored body", "clubbed tail", "defensive", "quadrupedal", "Cretaceous period", "plant-eater", "resilient", "prehistoric tank", "iconic"]},
    {"genre": "Allosaurus", "keywords": ["large predator", "sharp teeth", "bipedal", "aggressive", "Jurassic period", "apex hunter", "dominant", "prehistoric predator", "fearsome", "swift"]},
    {"genre": "Pteranodon", "keywords": ["flying reptile", "large wingspan", "beak", "fish eater", "Cretaceous period", "aerial predator", "prehistoric flyer", "gliding", "swift", "iconic"]},
    {"genre": "Parasaurolophus", "keywords": ["herbivore", "crested head", "bipedal and quadrupedal", "Cretaceous period", "plant-eater", "resonating calls", "herd behavior", "peaceful", "prehistoric", "iconic"]},
    {"genre": "Diplodocus", "keywords": ["long neck", "herbivore", "massive size", "quadrupedal", "whip-like tail", "Jurassic period", "peaceful", "plant-eater", "grazing", "prehistoric giant"]},
    {"genre": "Iguanodon", "keywords": ["herbivore", "thumb spike", "bipedal and quadrupedal", "Cretaceous period", "plant-eater", "herd behavior", "prehistoric", "iconic", "adaptive", "social"]},
    {"genre": "Carnotaurus", "keywords": ["carnivore", "short horns", "bipedal", "fast runner", "Cretaceous period", "predator", "agile", "fearsome", "prehistoric hunter", "swift"]},
    {"genre": "Pachycephalosaurus", "keywords": ["herbivore", "dome-shaped skull", "bipedal", "head-butting", "defensive", "Cretaceous period", "plant-eater", "prehistoric", "armored", "unique"]},
    {"genre": "Ceratosaurus", "keywords": ["medium predator", "bipedal", "horned snout", "Jurassic period", "carnivore", "prehistoric predator", "swift", "aggressive", "fearsome", "adaptable"]},
    {"genre": "Gallimimus", "keywords": ["omnivore", "ostrich-like", "bipedal", "fast runner", "Cretaceous period", "swift", "agile", "prehistoric", "social", "iconic"]},
    {"genre": "Compsognathus", "keywords": ["small predator", "bipedal", "fast", "Cretaceous period", "carnivore", "prehistoric hunter", "agile", "swift", "tiny", "adaptable"]},
    {"genre": "Therizinosaurus", "keywords": ["herbivore", "long claws", "bipedal", "Cretaceous period", "plant-eater", "unique", "prehistoric", "iconic", "giant claws", "unusual"]},
    {"genre": "Maiasaura", "keywords": ["herbivore", "caring parent", "bipedal and quadrupedal", "Cretaceous period", "plant-eater", "herd behavior", "peaceful", "prehistoric", "iconic", "social"]},
    {"genre": "Oviraptor", "keywords": ["omnivore", "bipedal", "egg thief", "Cretaceous period", "prehistoric", "small predator", "agile", "swift", "unique", "adaptive"]},
    {"genre": "Styracosaurus", "keywords": ["herbivore", "horned frill", "quadrupedal", "Cretaceous period", "plant-eater", "defensive", "prehistoric", "iconic", "social", "armored"]},
    {"genre": "Albertosaurus", "keywords": ["carnivore", "bipedal", "smaller relative of T. rex", "Cretaceous period", "prehistoric predator", "swift", "aggressive", "apex hunter", "fearsome", "dominant"]},
    {"genre": "Archaeopteryx", "keywords": ["feathered", "small", "bipedal", "transitional species", "Jurassic period", "prehistoric bird", "flying", "agile", "iconic", "unique"]},
    {"genre": "Protoceratops", "keywords": ["herbivore", "frilled head", "quadrupedal", "Cretaceous period", "plant-eater", "prehistoric", "social", "defensive", "small ceratopsian", "iconic"]},
    {"genre": "Deinonychus", "keywords": ["carnivore", "bipedal", "sharp claws", "pack hunter", "Cretaceous period", "prehistoric predator", "agile", "swift", "deadly", "adaptive"]},
    {"genre": "Megalosaurus", "keywords": ["carnivore", "bipedal", "sharp teeth", "Jurassic period", "prehistoric predator", "fearsome", "dominant", "powerful", "iconic", "adaptive"]},
    {"genre": "Giganotosaurus", "keywords": ["large predator", "carnivore", "bipedal", "Cretaceous period", "prehistoric predator", "fearsome", "dominant", "powerful", "giant", "iconic"]},
    {"genre": "Cryolophosaurus", "keywords": ["carnivore", "bipedal", "crested skull", "Jurassic period", "prehistoric predator", "fearsome", "unique", "adaptive", "swift", "iconic"]},
    {"genre": "Eoraptor", "keywords": ["small carnivore", "bipedal", "early dinosaur", "Triassic period", "prehistoric", "swift", "agile", "adaptive", "early predator", "unique"]},
    {"genre": "Muttaburrasaurus", "keywords": ["herbivore", "crested nose", "quadrupedal", "Cretaceous period", "plant-eater", "prehistoric", "unique", "adaptive", "peaceful", "iconic"]},
]

birds = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Bald Eagle", "keywords": ["majestic", "national symbol", "powerful talons", "soaring", "bird of prey", "sharp beak", "white head", "brown feathers", "strong vision", "North America"]},
    {"genre": "Peacock", "keywords": ["colorful", "long tail feathers", "iridescent", "courtship display", "elegant", "ornamental", "South Asia", "beautiful plumage", "vivid colors", "iconic"]},
    {"genre": "Penguin", "keywords": ["flightless", "aquatic", "black and white", "waddling", "Antarctica", "ice habitat", "group behavior", "cute", "diving", "social"]},
    {"genre": "Ostrich", "keywords": ["largest bird", "flightless", "fast runner", "long legs", "Africa", "powerful kicks", "plains dweller", "tough", "desert", "iconic"]},
    {"genre": "Hummingbird", "keywords": ["tiny", "hovering", "fast wings", "nectar feeding", "vibrant colors", "agile", "tropical", "unique", "smallest bird", "rapid motion"]},
    {"genre": "Flamingo", "keywords": ["pink feathers", "long legs", "wading bird", "shallow water", "social", "tropical", "iconic posture", "graceful", "filter feeder", "elegant"]},
    {"genre": "Albatross", "keywords": ["large wingspan", "oceanic", "gliding", "long-distance flyer", "seabird", "white and gray feathers", "endurance", "isolated habitats", "majestic", "marine"]},
    {"genre": "Parrot", "keywords": ["bright colors", "talking ability", "tropical", "intelligent", "social", "exotic", "beak strength", "feathered tail", "colorful", "adaptive"]},
    {"genre": "Robin", "keywords": ["small songbird", "red breast", "spring symbol", "common", "garden dweller", "cheerful", "migratory", "agile", "familiar", "iconic"]},
    {"genre": "Raven", "keywords": ["large black bird", "intelligent", "scavenger", "mythical", "ominous", "harsh calls", "adaptive", "symbolic", "trickster", "observant"]},
    {"genre": "Swan", "keywords": ["elegant", "white feathers", "long neck", "graceful", "waterbird", "calm waters", "iconic pair bonding", "majestic", "poetic", "iconic"]},
    {"genre": "Woodpecker", "keywords": ["tree drumming", "sharp beak", "forest", "insect eater", "vivid colors", "hole drilling", "strong neck", "distinctive sound", "agile", "iconic"]},
    {"genre": "Owl", "keywords": ["nocturnal", "large eyes", "silent flight", "predator", "mysterious", "wise", "forest habitats", "sharp talons", "adaptive", "mythological"]},
    {"genre": "Pelican", "keywords": ["large beak", "pouch for fish", "coastal", "group behavior", "aquatic", "graceful flyer", "white and gray feathers", "social", "iconic", "marine"]},
    {"genre": "Toucan", "keywords": ["large colorful beak", "tropical", "fruit eater", "forest dweller", "vivid feathers", "playful", "South America", "distinctive appearance", "iconic", "jungle bird"]},
    {"genre": "Seagull", "keywords": ["coastal bird", "scavenger", "white and gray", "adaptive", "group behavior", "marine", "iconic sound", "common", "beach habitats", "swift flyer"]},
    {"genre": "Kingfisher", "keywords": ["bright colors", "stream dweller", "sharp beak", "fish catcher", "fast flyer", "small", "tropical and temperate", "perching", "iconic", "agile"]},
    {"genre": "Canary", "keywords": ["small songbird", "vivid yellow", "domesticated", "cheerful", "caged bird", "melodic", "popular pet", "iconic", "adaptive", "social"]},
    {"genre": "Hawk", "keywords": ["bird of prey", "sharp talons", "fast flyer", "keen vision", "solitary", "forest and plains", "carnivore", "majestic", "predatory", "dominant"]},
    {"genre": "Crow", "keywords": ["black feathers", "intelligent", "scavenger", "adaptive", "group behavior", "common", "sharp calls", "mythical associations", "curious", "observant"]},
    {"genre": "Macaw", "keywords": ["large parrot", "vivid colors", "tropical", "intelligent", "long tail feathers", "exotic", "social", "South America", "playful", "iconic"]},
    {"genre": "Pigeon", "keywords": ["urban bird", "adaptive", "gray feathers", "city dweller", "common", "messenger bird", "group behavior", "iconic", "social", "resilient"]},
    {"genre": "Kiwi", "keywords": ["flightless", "small", "nocturnal", "New Zealand", "iconic", "long beak", "brown feathers", "endangered", "unique", "adaptive"]},
    {"genre": "Heron", "keywords": ["wading bird", "long legs", "wetlands", "sharp beak", "fishing", "graceful", "iconic posture", "calm waters", "majestic", "iconic"]},
    {"genre": "Cardinal", "keywords": ["red feathers", "small songbird", "vivid", "North America", "melodic", "garden bird", "territorial", "common", "cheerful", "iconic"]},
    {"genre": "Blue Jay", "keywords": ["blue feathers", "intelligent", "forest bird", "melodic calls", "bold", "North America", "adaptive", "social", "playful", "iconic"]},
    {"genre": "Condor", "keywords": ["large wingspan", "scavenger", "endangered", "majestic", "mountain habitats", "rare", "iconic", "powerful", "adaptive", "soaring"]},
    {"genre": "Sandpiper", "keywords": ["wading bird", "small size", "coastal habitats", "swift", "group behavior", "iconic", "beach runner", "marine", "agile", "adaptive"]},
    {"genre": "Dove", "keywords": ["white feathers", "peace symbol", "small bird", "gentle", "melodic", "group behavior", "calm", "iconic", "adaptable", "social"]},
    {"genre": "Eagle Owl", "keywords": ["large owl", "nocturnal predator", "majestic", "sharp talons", "wide wingspan", "forest habitats", "adaptive", "dominant", "intelligent", "fearsome"]},
]

dogs = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Dog Golden Retriever", "keywords": ["friendly", "intelligent", "family dog", "loyal", "playful", "golden coat", "obedient", "active", "trainable", "gentle"]},
    {"genre": "Dog German Shepherd", "keywords": ["protective", "intelligent", "loyal", "working dog", "strong", "police dog", "obedient", "alert", "brave", "versatile"]},
    {"genre": "Dog Bulldog", "keywords": ["stocky", "wrinkled face", "friendly", "calm", "loyal", "short muzzle", "adaptable", "strong-willed", "gentle", "companion"]},
    {"genre": "Dog Poodle", "keywords": ["intelligent", "elegant", "curly coat", "trainable", "energetic", "family dog", "active", "obedient", "adaptable", "loyal"]},
    {"genre": "Dog Beagle", "keywords": ["small hound", "curious", "friendly", "playful", "loyal", "scent hound", "energetic", "short-haired", "family dog", "social"]},
    {"genre": "Dog Labrador Retriever", "keywords": ["friendly", "intelligent", "loyal", "family dog", "playful", "active", "versatile", "trainable", "gentle", "adaptable"]},
    {"genre": "Dog Chihuahua", "keywords": ["small size", "lively", "alert", "loyal", "playful", "companion dog", "bold", "short or long coat", "energetic", "devoted"]},
    {"genre": "Dog Dachshund", "keywords": ["long body", "short legs", "playful", "energetic", "loyal", "curious", "scent hound", "small size", "companion", "alert"]},
    {"genre": "Dog Siberian Husky", "keywords": ["thick coat", "blue eyes", "energetic", "loyal", "sled dog", "friendly", "strong", "pack-oriented", "independent", "active"]},
    {"genre": "Dog Boxer", "keywords": ["muscular", "protective", "friendly", "energetic", "family dog", "loyal", "playful", "alert", "obedient", "brave"]},
    {"genre": "Dog Rottweiler", "keywords": ["strong", "protective", "loyal", "intelligent", "brave", "alert", "working dog", "muscular", "guard dog", "calm"]},
    {"genre": "Dog Shih Tzu", "keywords": ["small", "long coat", "friendly", "playful", "companion dog", "affectionate", "loyal", "adaptable", "charming", "gentle"]},
    {"genre": "Dog Yorkshire Terrier", "keywords": ["small", "long silky coat", "lively", "affectionate", "loyal", "intelligent", "playful", "companion dog", "curious", "bold"]},
    {"genre": "Dog Border Collie", "keywords": ["intelligent", "energetic", "loyal", "herding dog", "trainable", "agile", "alert", "friendly", "active", "obedient"]},
    {"genre": "Dog Great Dane", "keywords": ["large size", "gentle giant", "friendly", "loyal", "calm", "short coat", "elegant", "protective", "companion dog", "majestic"]},
    {"genre": "Dog Dalmatian", "keywords": ["spotted coat", "energetic", "playful", "friendly", "loyal", "alert", "trainable", "unique appearance", "active", "companion dog"]},
    {"genre": "Dog Cocker Spaniel", "keywords": ["friendly", "affectionate", "loyal", "playful", "intelligent", "family dog", "obedient", "medium coat", "social", "energetic"]},
    {"genre": "Dog French Bulldog", "keywords": ["small size", "bat-like ears", "loyal", "playful", "friendly", "short coat", "compact", "affectionate", "calm", "adaptable"]},
    {"genre": "Dog Australian Shepherd", "keywords": ["herding dog", "intelligent", "energetic", "loyal", "trainable", "active", "medium coat", "alert", "friendly", "versatile"]},
    {"genre": "Dog Pug", "keywords": ["small size", "wrinkled face", "friendly", "playful", "loyal", "short coat", "affectionate", "companion dog", "energetic", "adaptable"]},
    {"genre": "Dog Mastiff", "keywords": ["large size", "protective", "loyal", "gentle giant", "calm", "muscular", "alert", "guard dog", "family dog", "devoted"]},
    {"genre": "Dog Akita", "keywords": ["large size", "loyal", "intelligent", "protective", "brave", "strong", "alert", "dignified", "reserved", "calm"]},
    {"genre": "Dog Greyhound", "keywords": ["sleek", "fast runner", "friendly", "calm", "loyal", "short coat", "affectionate", "playful", "companion dog", "graceful"]},
    {"genre": "Dog Samoyed", "keywords": ["thick white coat", "friendly", "loyal", "playful", "energetic", "sled dog", "gentle", "affectionate", "family dog", "social"]},
    {"genre": "Dog Basset Hound", "keywords": ["long ears", "short legs", "loyal", "friendly", "scent hound", "calm", "playful", "gentle", "companion dog", "distinctive"]},
    {"genre": "Dog Chow Chow", "keywords": ["thick coat", "lion-like appearance", "loyal", "independent", "dignified", "protective", "calm", "alert", "unique", "reserved"]},
    {"genre": "Dog Doberman Pinscher", "keywords": ["protective", "intelligent", "loyal", "alert", "strong", "muscular", "brave", "obedient", "working dog", "elegant"]},
    {"genre": "Dog Collie", "keywords": ["loyal", "intelligent", "gentle", "herding dog", "family dog", "trainable", "medium coat", "affectionate", "friendly", "obedient"]},
    {"genre": "Dog Corgi", "keywords": ["short legs", "playful", "energetic", "loyal", "intelligent", "herding dog", "friendly", "trainable", "social", "cute"]},
    {"genre": "Dog Husky Mix", "keywords": ["mixed breed", "energetic", "loyal", "friendly", "thick coat", "active", "playful", "adaptive", "strong", "unique"]},
]

cats = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Cat Persian", "keywords": ["long-haired", "calm", "affectionate", "independent", "gentle", "round face", "quiet", "luxurious coat", "indoor cat", "laid-back"]},
    {"genre": "Cat Siamese", "keywords": ["short-haired", "vocal", "social", "intelligent", "loyal", "blue eyes", "playful", "sleek", "affectionate", "active"]},
    {"genre": "Cat Maine Coon", "keywords": ["large size", "friendly", "long-haired", "gentle giant", "playful", "intelligent", "social", "family cat", "loyal", "outgoing"]},
    {"genre": "Cat Ragdoll", "keywords": ["floppy", "affectionate", "calm", "blue eyes", "long-haired", "gentle", "quiet", "family cat", "social", "indoor"]},
    {"genre": "Cat Bengal", "keywords": ["exotic appearance", "spotted coat", "active", "intelligent", "playful", "energetic", "social", "sleek", "adventurous", "loyal"]},
    {"genre": "Cat British Shorthair", "keywords": ["round face", "plush coat", "calm", "independent", "affectionate", "gentle", "quiet", "family cat", "low-maintenance", "loyal"]},
    {"genre": "Cat Russian Blue", "keywords": ["short-haired", "silvery coat", "green eyes", "affectionate", "quiet", "intelligent", "loyal", "indoor cat", "reserved", "elegant"]},
    {"genre": "Cat Scottish Fold", "keywords": ["folded ears", "round face", "affectionate", "playful", "quiet", "calm", "social", "family cat", "loyal", "unique appearance"]},
    {"genre": "Cat Sphynx", "keywords": ["hairless", "warm skin", "active", "affectionate", "intelligent", "playful", "social", "unique", "friendly", "loyal"]},
    {"genre": "Cat Abyssinian", "keywords": ["short-haired", "active", "playful", "intelligent", "social", "sleek", "adventurous", "loyal", "curious", "affectionate"]},
    {"genre": "Cat Birman", "keywords": ["long-haired", "blue eyes", "calm", "affectionate", "social", "gentle", "family cat", "playful", "loyal", "elegant"]},
    {"genre": "Cat Oriental Shorthair", "keywords": ["sleek", "vocal", "intelligent", "playful", "social", "affectionate", "active", "loyal", "unique appearance", "expressive"]},
    {"genre": "Cat Devon Rex", "keywords": ["short-haired", "curly coat", "playful", "affectionate", "social", "intelligent", "active", "loyal", "unique", "energetic"]},
    {"genre": "Cat American Shorthair", "keywords": ["short-haired", "friendly", "playful", "adaptable", "social", "family cat", "intelligent", "loyal", "calm", "affectionate"]},
    {"genre": "Cat Norwegian Forest Cat", "keywords": ["long-haired", "thick coat", "gentle", "affectionate", "social", "family cat", "playful", "independent", "loyal", "outgoing"]},
    {"genre": "Cat Exotic Shorthair", "keywords": ["short-haired", "round face", "quiet", "affectionate", "social", "gentle", "indoor cat", "calm", "loyal", "plush coat"]},
    {"genre": "Cat Balinese", "keywords": ["long-haired", "vocal", "playful", "social", "intelligent", "affectionate", "sleek", "active", "loyal", "friendly"]},
    {"genre": "Cat Savannah", "keywords": ["exotic appearance", "spotted coat", "active", "adventurous", "intelligent", "social", "playful", "loyal", "unique", "energetic"]},
    {"genre": "Cat Tonkinese", "keywords": ["short-haired", "vocal", "affectionate", "playful", "social", "intelligent", "active", "loyal", "friendly", "sleek"]},
    {"genre": "Cat Cornish Rex", "keywords": ["short-haired", "curly coat", "sleek", "active", "affectionate", "social", "intelligent", "loyal", "playful", "energetic"]},
    {"genre": "Cat Manx", "keywords": ["short-haired", "tailless", "playful", "social", "loyal", "intelligent", "affectionate", "gentle", "family cat", "unique"]},
    {"genre": "Cat Burmese", "keywords": ["short-haired", "affectionate", "intelligent", "social", "playful", "family cat", "active", "loyal", "sleek", "friendly"]},
    {"genre": "Cat Chartreux", "keywords": ["short-haired", "blue-gray coat", "affectionate", "quiet", "loyal", "social", "calm", "family cat", "gentle", "reserved"]},
    {"genre": "Cat Ragamuffin", "keywords": ["long-haired", "friendly", "playful", "gentle", "social", "family cat", "affectionate", "loyal", "calm", "charming"]},
    {"genre": "Cat Egyptian Mau", "keywords": ["spotted coat", "short-haired", "active", "loyal", "playful", "intelligent", "social", "elegant", "fast runner", "unique"]},
    {"genre": "Cat Himalayan", "keywords": ["long-haired", "blue eyes", "calm", "affectionate", "quiet", "gentle", "family cat", "playful", "loyal", "indoor"]},
    {"genre": "Cat Korat", "keywords": ["short-haired", "silvery coat", "intelligent", "affectionate", "social", "loyal", "active", "family cat", "quiet", "gentle"]},
    {"genre": "Cat Japanese Bobtail", "keywords": ["short tail", "active", "playful", "intelligent", "social", "affectionate", "loyal", "sleek", "unique", "friendly"]},
    {"genre": "Cat Selkirk Rex", "keywords": ["curly coat", "affectionate", "social", "gentle", "family cat", "loyal", "playful", "calm", "unique", "plush"]},
    {"genre": "Cat Turkish Angora", "keywords": ["long-haired", "elegant", "playful", "social", "intelligent", "active", "loyal", "affectionate", "friendly", "graceful"]},
]

photo_video_styles = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Realistic Full Scene", "keywords": ["realism", "natural colors", "high detail", "wide frame", "landscape", "immersive", "real-world textures", "true-to-life", "natural lighting", "everyday scenes"]},
    {"genre": "Realistic Close-Up", "keywords": ["high detail", "shallow depth of field", "macro photography", "intense focus", "fine textures", "natural lighting", "real-world objects", "human expressions", "hyper-realism", "immersive"]},
    {"genre": "Half-Body Close-Up", "keywords": ["upper body", "realistic lighting", "facial expressions", "emotional focus", "intimate framing", "torso details", "natural posture", "human-focused", "documentary style", "real-life moments"]},
    {"genre": "Close-Up of Hands", "keywords": ["realistic details", "hand movements", "gestures", "skin textures", "fingers", "natural pose", "crafting actions", "emotional symbolism", "tight framing", "fine detail"]},
    {"genre": "Close-Up of Eyes", "keywords": ["intense focus", "realism", "emotive gaze", "natural reflection", "iris details", "skin texture", "tight framing", "captivating", "emotional depth", "human realism"]},
    {"genre": "Close-Up from Ground to Sky", "keywords": ["low-angle view", "realism", "perspective shift", "natural lighting", "wide lens", "earth textures", "towering objects", "dramatic sky", "immersive", "ground-up framing"]},
    {"genre": "Close-Up from Sky to Ground", "keywords": ["bird's-eye view", "aerial realism", "natural landscape", "top-down perspective", "immersive details", "textures from above", "sky contrast", "dynamic framing", "realistic lighting", "depth"]},
    {"genre": "Close-Up of Feet", "keywords": ["realistic textures", "ground interaction", "shoes or bare feet", "walking actions", "ground-level perspective", "motion-focused", "natural lighting", "tight framing", "earthy details", "movement"]},
    {"genre": "Close-Up of Hair", "keywords": ["realistic textures", "strand detail", "flowing motion", "wind effects", "natural lighting", "tight framing", "color gradients", "shimmer", "human-focused", "dynamic movement"]},
    {"genre": "Close-Up of Lips", "keywords": ["realistic detail", "expressions", "natural gloss", "human focus", "texture precision", "emotional emphasis", "natural lighting", "intimate framing", "mouth movements", "authenticity"]},
    {"genre": "Close-Up of Objects", "keywords": ["realism", "macro detail", "fine textures", "natural lighting", "small scale", "isolated subject", "product photography", "intense focus", "minimal background", "immersive"]},
    {"genre": "Over-the-Shoulder Close-Up", "keywords": ["realism", "character-focused", "partial framing", "contextual perspective", "human interactions", "narrative framing", "natural lighting", "intimate feel", "storytelling", "immersive"]},
    {"genre": "Close-Up of Nature", "keywords": ["realism", "macro photography", "plants", "leaves", "flowers", "natural textures", "tiny creatures", "fine details", "natural light", "immersive"]},
    {"genre": "Dynamic Perspective Close-Up", "keywords": ["tilted frame", "motion emphasis", "action capture", "realistic lighting", "tight framing", "natural textures", "immersive feel", "cinematic realism", "creative angles", "intensity"]},
    {"genre": "Close-Up of Food", "keywords": ["realism", "texture details", "natural lighting", "vivid colors", "delicious focus", "macro photography", "appetizing", "tight framing", "cultural foods", "fresh"]},
    {"genre": "Close-Up of Tools", "keywords": ["realism", "work in action", "fine details", "industrial textures", "natural lighting", "tight framing", "machinery focus", "hands-on motion", "craftsmanship", "authentic"]},
    {"genre": "Close-Up of the Sky", "keywords": ["realism", "cloud textures", "color gradients", "natural lighting", "sunset or sunrise", "starry sky", "tight framing", "heavenly details", "dynamic skies", "weather-focused"]},
    {"genre": "Close-Up of Textures", "keywords": ["realism", "natural materials", "wood grain", "stone patterns", "fabric weave", "detailed focus", "macro photography", "lighting effects", "earthy tones", "immersive realism"]},
    {"genre": "Close-Up of Shadows", "keywords": ["realism", "light play", "contrasts", "ambient textures", "mood setting", "natural lighting", "tight framing", "mystery", "perspective emphasis", "dim environments"]},
    {"genre": "Close-Up of a Person Running", "keywords": ["realistic motion", "dynamic angles", "muscle tension", "natural lighting", "action emphasis", "tight framing", "movement blur", "athletic focus", "sweat details", "energy"]},
    {"genre": "Close-Up of Tears", "keywords": ["realism", "emotional depth", "skin texture", "glistening effects", "human-focused", "natural lighting", "tight framing", "pain", "vulnerability", "emotion"]},
    {"genre": "Close-Up of Reflections", "keywords": ["realism", "mirrors", "water", "glass surfaces", "natural distortions", "lighting effects", "fine textures", "tight framing", "artistic perspectives", "real-life details"]},
    {"genre": "Close-Up of Flames", "keywords": ["realism", "fire textures", "glowing light", "intense heat", "dynamic motion", "tight framing", "natural lighting", "drama", "warmth", "elemental focus"]},
    {"genre": "Close-Up of Water Droplets", "keywords": ["macro photography", "realism", "natural lighting", "fine textures", "dynamic drops", "reflective surfaces", "tight framing", "freshness", "nature", "clarity"]},
    {"genre": "Close-Up of Animal Eyes", "keywords": ["realism", "wildlife focus", "natural details", "macro photography", "intense gaze", "tight framing", "unique textures", "emotion", "animal-specific", "authenticity"]},
    {"genre": "Close-Up of a Hug", "keywords": ["realism", "emotional connection", "human touch", "tight framing", "expressive hands", "warmth", "intimacy", "natural lighting", "detailed focus", "authenticity"]},
    {"genre": "Close-Up of a Laugh", "keywords": ["realism", "natural expressions", "teeth details", "emotional depth", "tight framing", "joy", "genuine reaction", "facial textures", "human-focused", "liveliness"]},
    {"genre": "Close-Up of Wind Effects", "keywords": ["realism", "natural motion", "flowing hair", "moving leaves", "tight framing", "dynamic feel", "airy elements", "lighting emphasis", "action shot", "nature-driven"]},
    {"genre": "Close-Up of Tools in Action", "keywords": ["realism", "industrial focus", "motion blur", "crafting", "tight framing", "fine detail", "practical work", "authenticity", "manual actions", "natural lighting"]},
]

produce_list = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Apple", "keywords": ["red", "green", "sweet", "crunchy", "juicy", "fiber-rich", "tree fruit", "healthy snack", "common fruit", "versatile"]},
    {"genre": "Banana", "keywords": ["yellow", "sweet", "soft", "peelable", "high potassium", "tropical fruit", "quick energy", "healthy", "easy to eat", "popular"]},
    {"genre": "Carrot", "keywords": ["orange", "crunchy", "root vegetable", "sweet", "fiber-rich", "high in beta-carotene", "versatile", "raw or cooked", "healthy snack", "earthy flavor"]},
    {"genre": "Strawberry", "keywords": ["red", "sweet", "juicy", "tiny seeds", "berry", "high in vitamin C", "popular in desserts", "fresh fruit", "fragrant", "heart-shaped"]},
    {"genre": "Tomato", "keywords": ["red", "juicy", "versatile", "fruit often treated as vegetable", "high in antioxidants", "salads", "sauces", "fresh or cooked", "round", "healthy"]},
    {"genre": "Potato", "keywords": ["brown skin", "starchy", "root vegetable", "versatile", "mashed", "fried", "baked", "high in carbs", "earthy flavor", "nutritious"]},
    {"genre": "Orange", "keywords": ["round", "orange color", "citrus fruit", "juicy", "sweet", "vitamin C-rich", "peelable", "aromatic", "popular juice", "healthy snack"]},
    {"genre": "Lettuce", "keywords": ["green", "leafy", "crunchy", "salads", "low calorie", "fresh", "versatile", "healthy", "mild flavor", "common vegetable"]},
    {"genre": "Grapes", "keywords": ["small", "juicy", "sweet", "green or red", "high in antioxidants", "vine fruit", "snackable", "seedless or seeded", "popular in wines", "versatile"]},
    {"genre": "Onion", "keywords": ["round", "pungent", "versatile", "white, yellow, or red", "strong aroma", "root vegetable", "flavorful", "raw or cooked", "healthy", "layers"]},
    {"genre": "Pineapple", "keywords": ["tropical", "sweet", "spiky skin", "juicy", "yellow inside", "aromatic", "high vitamin C", "unique flavor", "used in cooking", "refreshing"]},
    {"genre": "Bell Pepper", "keywords": ["green", "red", "yellow", "sweet or mild", "crunchy", "healthy", "salads", "stir-fries", "vitamin-rich", "colorful"]},
    {"genre": "Cucumber", "keywords": ["green", "watery", "crunchy", "refreshing", "low calorie", "hydrating", "salads", "versatile", "mild flavor", "cooling"]},
    {"genre": "Blueberry", "keywords": ["small", "round", "blue", "sweet", "juicy", "antioxidant-rich", "berry", "popular in baking", "healthy", "tart flavor"]},
    {"genre": "Eggplant", "keywords": ["purple skin", "soft", "spongy", "versatile", "cooking vegetable", "low calorie", "rich flavor", "healthy", "used in global cuisines", "unique"]},
    {"genre": "Mango", "keywords": ["tropical", "sweet", "juicy", "yellow-orange", "aromatic", "high in vitamin A", "stone fruit", "popular worldwide", "exotic flavor", "refreshing"]},
    {"genre": "Spinach", "keywords": ["green", "leafy", "soft", "nutritious", "iron-rich", "salads", "cooking greens", "mild flavor", "versatile", "healthy"]},
    {"genre": "Peach", "keywords": ["soft", "sweet", "juicy", "fuzzy skin", "yellow-orange", "stone fruit", "aromatic", "summer fruit", "healthy", "delicious"]},
    {"genre": "Zucchini", "keywords": ["green", "soft", "mild flavor", "summer squash", "versatile", "low calorie", "cooking vegetable", "healthy", "nutritious", "easy to grow"]},
    {"genre": "Cherry", "keywords": ["small", "red", "sweet or tart", "juicy", "stone fruit", "healthy", "snackable", "popular in desserts", "antioxidants", "fragrant"]},
    {"genre": "Watermelon", "keywords": ["large", "green rind", "red inside", "juicy", "sweet", "hydrating", "summer fruit", "refreshing", "low calorie", "healthy"]},
    {"genre": "Celery", "keywords": ["green", "crunchy", "low calorie", "fiber-rich", "hydrating", "healthy", "versatile", "snackable", "aromatic", "earthy flavor"]},
    {"genre": "Avocado", "keywords": ["green", "creamy", "nutritious", "healthy fats", "versatile", "mild flavor", "popular in guacamole", "rich texture", "unique fruit", "superfood"]},
    {"genre": "Kiwi", "keywords": ["small", "brown skin", "green inside", "tangy", "juicy", "fiber-rich", "tropical fruit", "unique texture", "vitamin-rich", "refreshing"]},
    {"genre": "Broccoli", "keywords": ["green", "crunchy", "nutritious", "fiber-rich", "florets", "healthy", "low calorie", "cooking vegetable", "earthy flavor", "versatile"]},
    {"genre": "Pear", "keywords": ["sweet", "juicy", "soft", "green or yellow", "unique texture", "healthy", "fiber-rich", "snackable", "autumn fruit", "aromatic"]},
    {"genre": "Beetroot", "keywords": ["purple-red", "earthy", "sweet", "root vegetable", "nutritious", "high in antioxidants", "healthy", "used in salads", "distinct flavor", "versatile"]},
    {"genre": "Raspberry", "keywords": ["small", "red", "sweet", "juicy", "berry", "high in fiber", "tangy", "healthy", "popular in desserts", "fragrant"]},
    {"genre": "Lime", "keywords": ["small", "green", "citrus", "tangy", "juicy", "aromatic", "used in drinks", "refreshing", "healthy", "popular in cooking"]},
    {"genre": "Pumpkin", "keywords": ["large", "orange", "sweet", "fiber-rich", "used in desserts", "versatile", "healthy", "earthy flavor", "fall season", "cooking vegetable"]},
]

realism_styles = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Ultra-Realistic", "keywords": ["high detail", "perfect lighting", "real-world textures", "precise shadows", "lifelike", "immersive", "authentic", "true-to-life", "natural tones", "photo-like quality"]},
    {"genre": "Hyper-Realistic", "keywords": ["exaggerated details", "amplified imperfections", "visible pores", "veins and skin texture", "dramatic lighting", "super clarity", "meticulous rendering", "striking visuals", "attention-grabbing", "beyond reality"]},
    {"genre": "Photo-Realistic", "keywords": ["photographic accuracy", "true-to-life colors", "precise reflections", "natural shadows", "camera-like rendering", "real-world simulation", "professional lighting", "smooth gradients", "authentic depth", "highly polished"]},
    {"genre": "Cinematic Realism", "keywords": ["film-like", "drama lighting", "dynamic framing", "color grading", "artistic depth", "story-driven visuals", "soft shadows", "lens effects", "moody tones", "narrative atmosphere"]},
    {"genre": "Digital Realism", "keywords": ["computer-generated", "CGI precision", "high-definition textures", "pixel-perfect", "seamless integration", "next-gen rendering", "realistic simulation", "detailed animation", "interactive realism", "virtual world"]},
    {"genre": "Macro Realism", "keywords": ["extreme close-up", "micro details", "texture-focused", "tiny objects", "minute imperfections", "high magnification", "intimate perspective", "sharp clarity", "enhanced small details", "true-to-scale"]},
    {"genre": "Stylized Realism", "keywords": ["artistic touch", "enhanced colors", "soft textures", "natural yet vibrant", "expressive shadows", "creative lighting", "semi-realistic", "aesthetic flair", "balanced realism", "personality-driven"]},
    {"genre": "Real-Time Rendering", "keywords": ["game engine", "interactive realism", "fast processing", "dynamic lighting", "seamless animations", "physics-driven", "realistic reactions", "live simulation", "efficient rendering", "modern graphics"]},
    {"genre": "Surreal Realism", "keywords": ["dreamlike", "elevated reality", "fantastical elements", "hyper clarity", "unusual scenarios", "rich textures", "ethereal lighting", "unexpected details", "imaginative visuals", "alternate reality"]},
    {"genre": "Natural Realism", "keywords": ["organic textures", "nature-inspired", "earth tones", "wildlife focus", "scenic beauty", "daylight effects", "environmental accuracy", "soft gradients", "natural shadows", "landscape realism"]},
    {"genre": "High Dynamic Range (HDR)", "keywords": ["enhanced contrast", "bright highlights", "deep shadows", "color vibrancy", "realistic depth", "full spectrum lighting", "cinematic quality", "crisp textures", "immersive tone mapping", "rich details"]},
    {"genre": "Scientific Realism", "keywords": ["accuracy-focused", "educational visuals", "high precision", "true proportions", "clear labels", "natural materials", "laboratory lighting", "factual rendering", "scientific clarity", "unembellished style"]},
    {"genre": "Emotional Realism", "keywords": ["expressive tones", "emotive lighting", "character-driven", "storytelling focus", "intimate framing", "soulful expressions", "human connection", "subtle textures", "evocative colors", "heartfelt atmosphere"]},
    {"genre": "Futuristic Realism", "keywords": ["advanced technology", "sci-fi inspired", "neon lighting", "ultra-modern textures", "virtual aesthetics", "cyberpunk elements", "clean surfaces", "futuristic cityscapes", "sleek design", "next-gen vibes"]},
    {"genre": "Vintage Realism", "keywords": ["historical accuracy", "retro textures", "sepia tones", "aged materials", "classic lighting", "nostalgic vibes", "period-specific", "antique details", "authentic patina", "timeless appeal"]},
    {"genre": "Dynamic Realism", "keywords": ["movement-focused", "action-packed", "motion blur", "realistic physics", "natural flow", "energy-driven visuals", "fluid dynamics", "spontaneous effects", "immersive action", "true-to-life dynamics"]},
    {"genre": "Abstract Realism", "keywords": ["conceptual elements", "realistic base", "artistic interpretation", "unusual colors", "creative lighting", "symbolic visuals", "semi-representational", "blended styles", "thought-provoking", "emotional depth"]},
    {"genre": "Architectural Realism", "keywords": ["building accuracy", "cityscapes", "structural details", "clean lines", "real-world proportions", "modern design", "true-to-scale", "realistic lighting", "construction materials", "authentic interiors"]},
    {"genre": "Atmospheric Realism", "keywords": ["mood-driven", "weather effects", "mist and fog", "light diffusion", "realistic skies", "ambient tones", "natural shadows", "immersive depth", "dynamic lighting", "textured atmosphere"]},
    {"genre": "Fantasy Realism", "keywords": ["magical realism", "mythical creatures", "enchanted landscapes", "glowing elements", "ethereal textures", "dreamlike quality", "vivid colors", "fairy-tale settings", "otherworldly light", "imaginative world"]},
]

earth_elements = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Element Earth", "keywords": ["soil", "dirt", "clay", "mud", "terrain", "ground", "land", "fertile", "natural surface", "earthy texture"]},
    {"genre": "Element Water", "keywords": ["ocean", "river", "lake", "rain", "ice", "steam", "droplets", "waves", "hydration", "clear liquid"]},
    {"genre": "Element Fire", "keywords": ["flames", "embers", "smoke", "heat", "burning", "wildfire", "candlelight", "spark", "lava", "intensity"]},
    {"genre": "Element Air", "keywords": ["wind", "breeze", "oxygen", "gust", "whirlwind", "freshness", "movement", "pressure", "atmosphere", "invisible flow"]},
    {"genre": "Element Metal", "keywords": ["iron", "steel", "rust", "forge", "strength", "tools", "blades", "shiny surface", "industrial", "cold"]},
    {"genre": "Element Gold", "keywords": ["nugget", "bar", "jewelry", "treasure", "luxury", "shimmering", "yellow metal", "wealth", "soft metal", "coin"]},
    {"genre": "Element Silver", "keywords": ["ornament", "coin", "mirror", "bright", "pure metal", "jewelry", "reflective", "elegance", "conductive", "bar"]},
    {"genre": "Element Stone", "keywords": ["pebble", "rock", "granite", "marble", "boulder", "statue", "quarry", "hard surface", "natural building", "ancient"]},
    {"genre": "Element Wood", "keywords": ["log", "plank", "forest", "timber", "carving", "natural material", "oak", "pine", "grain", "sawdust"]},
    {"genre": "Element Sand", "keywords": ["desert", "beach", "grains", "dunes", "quartz", "silt", "wind-blown", "soft texture", "glass base", "tiny particles"]},
    {"genre": "Element Clay", "keywords": ["pottery", "bricks", "terracotta", "ceramics", "mud", "sculpting", "earthy", "moldable", "hardens", "red soil"]},
    {"genre": "Element Diamond", "keywords": ["gem", "jewel", "hardest mineral", "brilliance", "cut stone", "luxury", "clear crystal", "ring", "sparkling", "precious"]},
    {"genre": "Element Coal", "keywords": ["fossil fuel", "black rock", "energy source", "carbon", "combustion", "mining", "industrial", "raw material", "power generation", "briquette"]},
    {"genre": "Element Copper", "keywords": ["wiring", "coin", "bronze base", "reddish metal", "electrical", "ductile", "alloy", "corrosion-resistant", "heat conductor", "industrial"]},
    {"genre": "Element Salt", "keywords": ["sea salt", "rock salt", "crystals", "white", "seasoning", "preservative", "mineral", "granules", "essential", "harvesting"]},
    {"genre": "Element Quartz", "keywords": ["crystal", "semi-precious", "sand component", "clear stone", "watch component", "geodes", "jewelry", "hardness", "transparency", "mineral"]},
    {"genre": "Element Amber", "keywords": ["fossil resin", "yellow", "translucent", "jewelry", "ancient tree sap", "preserved", "ornamental", "organic gemstone", "warm glow", "historic"]},
    {"genre": "Element Ice", "keywords": ["frozen water", "glacier", "crystals", "snow", "cold", "transparent", "slippery", "frost", "iceberg", "sparkling"]},
    {"genre": "Element Lava", "keywords": ["molten rock", "volcano", "hot", "flowing", "fire", "igneous rock", "eruptive", "cooling", "red-orange", "destructive"]},
    {"genre": "Element Basalt", "keywords": ["volcanic rock", "igneous", "dark gray", "dense", "columns", "lava origin", "hard", "construction", "ancient formations", "natural"]},
    {"genre": "Element Granite", "keywords": ["countertop", "strong", "speckled", "hard rock", "igneous", "quarry", "durable", "monuments", "architectural", "earthy"]},
    {"genre": "Element Obsidian", "keywords": ["volcanic glass", "black", "sharp edges", "hard", "shiny", "cutting tools", "ornamental", "smooth", "cooling lava", "precise"]},
    {"genre": "Element Sulfur", "keywords": ["yellow mineral", "volcanic", "brittle", "smell", "medicine", "gunpowder", "crystals", "natural deposits", "essential element", "industrial"]},
    {"genre": "Element Emerald", "keywords": ["green gemstone", "precious", "jewelry", "clarity", "luxury", "hardness", "brilliance", "cut stone", "mined", "rare"]},
    {"genre": "Element Ruby", "keywords": ["red gemstone", "precious", "jewelry", "luxury", "hardness", "passion", "brilliance", "cut stone", "fiery", "rare"]},
    {"genre": "Element Platinum", "keywords": ["noble metal", "precious", "jewelry", "industrial", "silver-white", "luxury", "corrosion-resistant", "dense", "rare", "investment"]},
    {"genre": "Element Aluminum", "keywords": ["lightweight", "silver metal", "foil", "cans", "conductive", "industrial", "flexible", "alloy", "corrosion-resistant", "modern"]},
    {"genre": "Element Tin", "keywords": ["alloy", "soft metal", "cans", "bronze base", "corrosion-resistant", "soldering", "industrial", "historical", "silver appearance", "versatile"]},
    {"genre": "Element Nickel", "keywords": ["magnetic", "alloy", "coinage", "corrosion-resistant", "industrial", "shiny", "strong", "conductive", "heat-resistant", "metallic"]},
    {"genre": "Element Zinc", "keywords": ["galvanizing", "alloy", "corrosion-resistant", "blueish-white metal", "industrial", "brass base", "medicine", "essential element", "ductile", "versatile"]},
]

daytime_moments = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Times Early Dawn", "keywords": ["soft light", "hazy horizon", "pale blue sky", "faint glow", "quiet atmosphere", "gentle shadows", "calm air", "dew-covered surfaces", "subtle gradients", "peaceful beginnings"]},
    {"genre": "Times Sunrise", "keywords": ["golden light", "warm hues", "low sun", "elongated shadows", "pink and orange tones", "fresh atmosphere", "awakening world", "dramatic silhouettes", "radiant glow", "tranquil beauty"]},
    {"genre": "Times Mid-Morning", "keywords": ["bright sunlight", "clear skies", "moderate warmth", "defined shadows", "vivid colors", "active environment", "energized mood", "glare from surfaces", "lively scenes", "crisp clarity"]},
    {"genre": "Times Late Morning", "keywords": ["strong sunlight", "intense brightness", "short shadows", "blue skies", "heightened activity", "reflective surfaces", "clear details", "energetic vibes", "daytime bustle", "vivid visuals"]},
    {"genre": "Times Noon", "keywords": ["overhead sun", "harsh light", "minimal shadows", "brightest time", "white highlights", "strong glare", "clear visibility", "maximum warmth", "flat lighting", "peak energy"]},
    {"genre": "Times Early Afternoon", "keywords": ["softening light", "angled sunlight", "longer shadows", "warmer tones", "subtle contrasts", "relaxed atmosphere", "gentle warmth", "natural highlights", "midday transitions", "inviting glow"]},
    {"genre": "Times Late Afternoon", "keywords": ["golden hour", "low sun", "rich colors", "dramatic shadows", "golden highlights", "soft contrasts", "calming atmosphere", "evening approaches", "orange and amber tones", "picturesque light"]},
    {"genre": "Times Sunset", "keywords": ["vivid hues", "red and orange tones", "low-angled light", "elongated shadows", "dramatic sky", "cooling air", "peaceful scenery", "colorful gradients", "reflective waters", "nostalgic vibes"]},
    {"genre": "Times Dusk", "keywords": ["fading light", "blue hour", "soft shadows", "subdued tones", "cool atmosphere", "twilight hues", "calming mood", "dimmed surroundings", "gentle transitions", "quiet serenity"]},
    {"genre": "Times Nightfall", "keywords": ["darkening sky", "silhouetted objects", "deep blues", "starry sky", "soft breezes", "evening quiet", "muted colors", "nocturnal sounds", "calm energy", "welcoming night"]},
    {"genre": "Times Early Night", "keywords": ["moonlit scenery", "cool air", "starlit sky", "low visibility", "quiet surroundings", "warm indoor lights", "shadows in the dark", "soft glows", "tranquil moments", "evening activities"]},
    {"genre": "Times Midnight", "keywords": ["darkest time", "bright stars", "coolest temperature", "silent ambiance", "deep shadows", "still surroundings", "mystical glow", "moon dominance", "quiet introspection", "peaceful solitude"]},
    {"genre": "Times Pre-Dawn", "keywords": ["deep blue tones", "faint light", "stillness", "whispering breezes", "sleeping world", "emerging hues", "cool atmosphere", "soft whispers of light", "anticipation of dawn", "delicate balance"]},
    {"genre": "Times Morning Golden Hour", "keywords": ["soft golden light", "rich contrasts", "warm tones", "low-angle sun", "elongated shadows", "early activity", "gentle highlights", "romantic atmosphere", "natural beauty", "inviting start"]},
    {"genre": "Times Afternoon Golden Hour", "keywords": ["intensified hues", "rich oranges", "low sun", "glowing landscapes", "ambient warmth", "peaceful vibes", "dramatic contrasts", "picturesque light", "enhanced textures", "end-of-day charm"]},
    {"genre": "Times Twilight", "keywords": ["fading colors", "indigo tones", "silent transitions", "subtle gradients", "dimmed glow", "emerging stars", "cool shadows", "whispering wind", "gentle shifts", "dreamy moments"]},
    {"genre": "Times Mid-Afternoon", "keywords": ["bright skies", "moderate heat", "vibrant colors", "clear visibility", "active energy", "soft breezes", "short shadows", "lively environment", "natural lighting", "daytime peak"]},
    {"genre": "Times Deep Night", "keywords": ["pitch black sky", "bright moonlight", "intense stillness", "faint nocturnal sounds", "dim glow", "hidden details", "mystical ambiance", "calm solitude", "shadowy landscapes", "dreamlike aura"]},
    {"genre": "Times City at Night", "keywords": ["urban lights", "neon glow", "streetlights", "active nightlife", "bright windows", "reflective surfaces", "bustling streets", "shimmering water", "dynamic scenes", "contrasted tones"]},
    {"genre": "Times Starlit Night", "keywords": ["bright constellations", "dark skies", "clear air", "tranquil atmosphere", "subtle highlights", "silhouetted landscapes", "cosmic beauty", "calming breeze", "infinite depth", "celestial charm"]},
]

beverages = [
    {"genre": "Other", "keywords": [""]},    
    {"genre": "Beverage Cola", "keywords": ["Coca-Cola", "Pepsi", "carbonated", "sweet", "dark color", "popular", "refreshing", "classic", "ice-cold", "global brand"]},
    {"genre": "Beverage Lemon-Lime Soda", "keywords": ["Sprite", "7-Up", "clear", "citrusy", "carbonated", "refreshing", "sweet", "lemon flavor", "cold drink", "light taste"]},
    {"genre": "Beverage Root Beer", "keywords": ["A&W", "Barq's", "creamy", "spiced", "carbonated", "classic flavor", "sweet", "vanilla hints", "American favorite", "nostalgic"]},
    {"genre": "Beverage Energy Drink", "keywords": ["Red Bull", "Monster", "high caffeine", "boost", "carbonated", "tangy", "sports drink", "stimulant", "popular", "active lifestyle"]},
    {"genre": "Beverage Juice", "keywords": ["Tropicana", "Minute Maid", "orange juice", "apple juice", "natural", "refreshing", "vitamin C", "sweet", "breakfast drink", "fruit-based"]},
    {"genre": "Beverage Iced Tea", "keywords": ["Lipton", "Arizona", "sweetened", "unsweetened", "lemon flavor", "refreshing", "bottled", "black tea", "cool drink", "relaxing"]},
    {"genre": "Beverage Beer", "keywords": ["Budweiser", "Heineken", "Corona", "lager", "pale ale", "bar drink", "alcoholic", "hoppy", "cold", "refreshing"]},
    {"genre": "Beverage Craft Beer", "keywords": ["IPA", "stout", "porter", "microbrewery", "unique flavors", "hoppy", "rich taste", "small batch", "specialty beer", "innovative"]},
    {"genre": "Beverage Wine", "keywords": ["Cabernet Sauvignon", "Chardonnay", "red wine", "white wine", "grapes", "aged", "rich flavor", "bottled", "alcoholic", "fine dining"]},
    {"genre": "Beverage Whiskey", "keywords": ["Jack Daniels", "Jameson", "bourbon", "scotch", "aged", "smoky", "barrel", "alcoholic", "strong", "classic spirit"]},
    {"genre": "Beverage Vodka", "keywords": ["Grey Goose", "Smirnoff", "clear spirit", "neutral taste", "cocktail base", "distilled", "alcoholic", "party drink", "smooth", "versatile"]},
    {"genre": "Beverage Rum", "keywords": ["Bacardi", "Captain Morgan", "dark rum", "spiced rum", "tropical", "cocktail base", "distilled", "sweet undertones", "alcoholic", "Caribbean"]},
    {"genre": "Beverage Gin", "keywords": ["Tanqueray", "Bombay Sapphire", "juniper flavor", "dry", "herbal", "cocktail base", "distilled", "alcoholic", "botanical", "classic spirit"]},
    {"genre": "Beverage Champagne", "keywords": ["Moët & Chandon", "Veuve Clicquot", "sparkling wine", "bubbly", "celebration", "luxury", "French origin", "golden color", "alcoholic", "refined"]},
    {"genre": "Beverage Sports Drink", "keywords": ["Gatorade", "Powerade", "electrolytes", "hydration", "sweetened", "bright colors", "energy boost", "athlete favorite", "non-carbonated", "refreshing"]},
    {"genre": "Beverage Milk", "keywords": ["dairy", "lactose-free", "whole milk", "skim milk", "nutritious", "creamy", "calcium", "white", "versatile", "natural"]},
    {"genre": "Beverage Flavored Milk", "keywords": ["chocolate milk", "strawberry milk", "sweet", "creamy", "bottled", "dairy", "children's favorite", "dessert-like", "nutritious", "cool drink"]},
    {"genre": "Beverage Coffee", "keywords": ["Starbucks", "espresso", "cappuccino", "latte", "hot drink", "caffeine", "aromatic", "bold flavor", "energizing", "morning staple"]},
    {"genre": "Beverage Tea", "keywords": ["green tea", "black tea", "herbal tea", "warm", "aromatic", "relaxing", "natural", "antioxidants", "steeped", "global beverage"]},
    {"genre": "Beverage Smoothie", "keywords": ["fruit blend", "yogurt base", "berries", "banana", "cold", "healthy", "sweet", "creamy texture", "nutrient-rich", "breakfast drink"]},
    {"genre": "Beverage Hot Chocolate", "keywords": ["cocoa", "creamy", "sweet", "hot drink", "comforting", "winter favorite", "marshmallows", "rich", "chocolatey", "dessert-like"]},
    {"genre": "Beverage Liqueur", "keywords": ["Baileys", "Kahlúa", "sweet spirit", "creamy", "dessert drink", "alcoholic", "coffee-based", "unique flavors", "cocktail ingredient", "smooth"]},
    {"genre": "Beverage Mocktail", "keywords": ["non-alcoholic", "fruit-based", "creative flavors", "decorative", "refreshing", "party drink", "bright colors", "sweet", "unique blends", "chilled"]},
    {"genre": "Beverage Mineral Water", "keywords": ["San Pellegrino", "Evian", "sparkling", "natural", "pure", "hydrating", "bottled", "cold", "premium", "refreshing"]},
    {"genre": "Beverage Coconut Water", "keywords": ["natural hydration", "sweet", "tropical", "healthy", "refreshing", "bottled", "low calorie", "electrolytes", "pure", "clear liquid"]},
    {"genre": "Beverage Beer Alternative", "keywords": ["hard seltzer", "White Claw", "low-calorie", "sparkling", "alcoholic", "fruity", "light taste", "popular", "party drink", "trendy"]},
    {"genre": "Beverage Kombucha", "keywords": ["fermented", "probiotic", "tea base", "slightly fizzy", "healthy", "natural", "tangy", "bottled", "nutritious", "alternative"]},
    {"genre": "Beverage Lemonade", "keywords": ["fresh", "citrusy", "sweetened", "cooling", "yellow", "homemade", "refreshing", "summer drink", "natural", "bottled"]},
    {"genre": "Beverage Herbal Infusion", "keywords": ["chamomile", "peppermint", "soothing", "non-caffeinated", "relaxing", "aromatic", "steeped", "warm", "natural", "medicinal"]},
    {"genre": "Beverage Frozen Drink", "keywords": ["Slurpee", "Icee", "sweet", "slushy", "colorful", "cold", "summer treat", "artificial flavors", "popular", "fun"]},
]

dishes = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "A meal of Roast Chicken", "keywords": ["whole chicken", "roasted", "crispy skin", "herbs", "buttery", "golden brown", "oven-baked", "holiday dish", "juicy", "classic dinner"]},
    {"genre": "A meal of Caesar Salad", "keywords": ["romaine lettuce", "croutons", "parmesan cheese", "Caesar dressing", "anchovies", "creamy", "fresh", "appetizer", "light meal", "popular salad"]},
    {"genre": "A meal of Beef Steak", "keywords": ["grilled", "medium-rare", "juicy", "seasoned", "marbled", "prime cut", "sizzling", "restaurant favorite", "tender", "classic entree"]},
    {"genre": "A meal of Vegetable Stir-Fry", "keywords": ["mixed vegetables", "soy sauce", "garlic", "ginger", "quick-cooked", "Asian-style", "healthy", "colorful", "light oil", "savory"]},
    {"genre": "A meal of Spaghetti Bolognese", "keywords": ["pasta", "ground beef", "tomato sauce", "herbs", "parmesan", "Italian cuisine", "hearty", "classic dish", "red sauce", "garlic"]},
    {"genre": "A meal of Pizza Margherita", "keywords": ["thin crust", "mozzarella cheese", "tomato sauce", "fresh basil", "Italian style", "wood-fired", "classic pizza", "simple", "crispy", "savory"]},
    {"genre": "A meal of Grilled Salmon", "keywords": ["fish", "lemon slices", "herbs", "healthy", "omega-3", "pink flesh", "dinner entree", "charred", "lightly seasoned", "delicate flavor"]},
    {"genre": "A meal of Tacos", "keywords": ["soft tortilla", "ground beef", "shredded lettuce", "cheese", "sour cream", "Mexican food", "spiced", "finger food", "guacamole", "colorful"]},
    {"genre": "A meal of Sushi Roll", "keywords": ["seaweed wrap", "vinegared rice", "raw fish", "wasabi", "soy sauce", "Japanese cuisine", "bite-sized", "colorful", "delicate", "seafood"]},
    {"genre": "A meal of Hamburger", "keywords": ["beef patty", "lettuce", "tomato", "bun", "cheese", "grilled", "American classic", "fast food", "juicy", "savory"]},
    {"genre": "A meal of Vegetarian Curry", "keywords": ["spices", "coconut milk", "vegetables", "rice", "Indian cuisine", "creamy", "flavorful", "spicy", "colorful", "plant-based"]},
    {"genre": "A meal of Roast Turkey", "keywords": ["whole turkey", "stuffing", "cranberry sauce", "gravy", "golden brown", "Thanksgiving dish", "holiday favorite", "crispy skin", "juicy", "aromatic"]},
    {"genre": "A meal of Pad Thai", "keywords": ["rice noodles", "peanuts", "bean sprouts", "shrimp", "egg", "lime", "Thai cuisine", "sweet and savory", "spicy", "stir-fried"]},
    {"genre": "A meal of Barbecue Ribs", "keywords": ["pork ribs", "BBQ sauce", "smoky flavor", "grilled", "sticky", "fall-off-the-bone", "American BBQ", "savory", "sweet glaze", "hearty"]},
    {"genre": "A meal of Chocolate Cake", "keywords": ["rich", "moist", "layered", "frosting", "dessert", "decadent", "sweet", "baked", "celebration", "indulgent"]},
    {"genre": "A meal of Fried Rice", "keywords": ["rice", "soy sauce", "vegetables", "egg", "quick-cooked", "Chinese cuisine", "savory", "stir-fried", "easy meal", "colorful"]},
    {"genre": "A meal of Greek Salad", "keywords": ["cucumber", "feta cheese", "tomato", "olives", "olive oil", "Mediterranean style", "fresh", "light", "healthy", "appetizer"]},
    {"genre": "A meal of Shepherd's Pie", "keywords": ["ground lamb", "mashed potatoes", "baked", "gravy", "hearty", "English dish", "comfort food", "savory", "layered", "classic"]},
    {"genre": "A meal of Shrimp Cocktail", "keywords": ["chilled shrimp", "cocktail sauce", "lemon wedge", "appetizer", "seafood", "light", "zesty", "classic starter", "fresh", "party favorite"]},
    {"genre": "A meal of Chicken Tikka Masala", "keywords": ["grilled chicken", "spiced tomato sauce", "creamy", "Indian cuisine", "aromatic", "rich flavor", "rice accompaniment", "popular dish", "vibrant", "savory"]},
    {"genre": "A meal of Lasagna", "keywords": ["pasta sheets", "ground beef", "tomato sauce", "cheese layers", "Italian dish", "baked", "hearty", "savory", "comfort food", "rich"]},
    {"genre": "A meal of Omelette", "keywords": ["eggs", "cheese", "herbs", "vegetables", "breakfast", "fluffy", "savory", "quick meal", "simple", "protein-rich"]},
    {"genre": "A meal of Clam Chowder", "keywords": ["creamy soup", "clams", "potatoes", "onions", "New England style", "hearty", "warm", "seafood", "savory", "classic"]},
    {"genre": "A meal of Pancakes", "keywords": ["fluffy", "syrup", "breakfast", "stacked", "buttery", "sweet", "quick", "American favorite", "batter", "golden brown"]},
    {"genre": "A meal of Spring Rolls", "keywords": ["rice paper wrap", "vegetables", "shrimp", "dipping sauce", "Vietnamese cuisine", "fresh", "light", "healthy", "finger food", "colorful"]},
    {"genre": "A meal of Macaroni and Cheese", "keywords": ["pasta", "cheddar", "creamy", "baked", "comfort food", "hearty", "childhood favorite", "simple", "golden", "savory"]},
    {"genre": "A meal of Fish and Chips", "keywords": ["fried fish", "crispy batter", "French fries", "tartar sauce", "pub food", "British classic", "golden", "hearty", "comfort food", "savory"]},
    {"genre": "A meal of Falafel Wrap", "keywords": ["chickpeas", "herbs", "fried balls", "pita bread", "Middle Eastern", "tahini", "healthy", "vegetarian", "spiced", "street food"]},
    {"genre": "A meal of Cheesecake", "keywords": ["creamy", "sweet", "graham cracker crust", "baked", "dessert", "indulgent", "rich", "classic", "smooth texture", "decadent"]},
    {"genre": "A meal of Risotto", "keywords": ["arborio rice", "parmesan", "creamy", "Italian dish", "buttery", "rich flavor", "slow-cooked", "comfort food", "savory", "gourmet"]},
]

bad_words = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Text Annoyed", "keywords": ["idiot", "stupid", "dumb", "moron", "loser", "jerk", "worthless", "clueless", "pathetic", "useless"]},
    {"genre": "Text Frustration", "keywords": ["crap", "hell", "damn", "bloody", "freaking", "screw it", "bugger", "shut up", "shut it", "get lost"]},
    {"genre": "Text Anger", "keywords": ["bastard", "asshole", "bitch", "son of a bitch", "dickhead", "twat", "wanker", "prick", "douchebag", "piss off"]},
    {"genre": "Text Sarcasm", "keywords": ["yeah, right", "good luck with that", "sure, whatever", "big deal", "who cares", "don't make me laugh", "as if", "no way", "not a chance", "yeah, right"]},
    {"genre": "Text Disgust", "keywords": ["gross", "nasty", "disgusting", "revolting", "sickening", "vile", "foul", "yuck", "eww", "ugh"]},
    {"genre": "Text Exasperation", "keywords": ["unbelievable", "ridiculous", "seriously", "how stupid", "out of control", "insane", "no way", "what a joke", "come on", "you've got to be kidding me"]},
    {"genre": "Text Insult", "keywords": ["shut your mouth", "get a life", "go to hell", "go away", "leave me alone", "get out of here", "shut it", "drop dead", "screw you", "suck it"]},
    {"genre": "Text Disappointment", "keywords": ["what a letdown", "are you serious?", "I can't believe this", "this is terrible", "what a waste", "this is a joke", "so much for that", "what's wrong with you?", "this is pathetic", "I’m done"]},
    {"genre": "Text Rage", "keywords": ["damn it", "you’re dead to me", "go fuck yourself", "screw you", "burn in hell", "get the hell out", "eat shit", "fuck off", "kiss my ass", "blow it out your ass"]},
    {"genre": "Text Confusion", "keywords": ["what the hell", "what the fuck", "who cares", "I don't get it", "this makes no sense", "what’s going on", "are you kidding me", "no idea", "what the hell is happening", "where am I?"]},
]

bad_words_medias = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Sign Text Annoyed", "keywords": ["idiot", "stupid", "dumb", "moron", "loser", "jerk", "worthless", "clueless", "pathetic", "useless"]},
    {"genre": "Digital Screen Text Annoyed", "keywords": ["crap", "hell", "damn", "bloody", "freaking", "screw it", "bugger", "shut up", "shut it", "get lost"]},
    {"genre": "Poster Text Frustrated", "keywords": ["pissed off", "fed up", "sick of it", "done with this", "over it", "can't stand it", "enough already", "had enough", "this sucks", "this blows"]},
    {"genre": "Paper Text Exasperated", "keywords": ["for crying out loud", "give me a break", "are you kidding me", "seriously", "unbelievable", "no way", "come on", "what the hell", "what the heck", "what the fuck"]},
    {"genre": "Cellphone Text Angry", "keywords": ["bastard", "asshole", "bitch", "dickhead", "twat", "wanker", "prick", "douchebag", "piss off", "fuck off"]},
    {"genre": "Tablet Text Annoyed", "keywords": ["bloody hell", "bugger off", "bollocks", "bollocks to that", "sod off", "shut your mouth", "get a life", "go to hell", "go away", "leave me alone"]},
    {"genre": "Digital Screen Text Frustrated", "keywords": ["damn it", "shit", "crap", "piss", "arse", "bollocks", "bugger", "sod", "twat", "wanker"]},
    {"genre": "Poster Text Exasperated", "keywords": ["what the hell", "what the heck", "what the fuck", "seriously", "unbelievable", "no way", "come on", "are you kidding me", "for crying out loud", "give me a break"]},
    {"genre": "Paper Text Angry", "keywords": ["bastard", "asshole", "bitch", "dickhead", "twat", "wanker", "prick", "douchebag", "piss off", "fuck off"]},
    {"genre": "Cellphone Text Frustrated", "keywords": ["bloody hell", "bugger off", "bollocks", "bollocks to that", "sod off", "shut your mouth", "get a life", "go to hell", "go away", "leave me alone"]},
]

positive_words_media = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Sign Text Joyful", "keywords": ["joyful", "elated", "ecstatic", "content", "cheerful", "delighted", "blissful", "radiant", "euphoric", "overjoyed"]},
    {"genre": "Digital Screen Text Happy", "keywords": ["happy", "pleased", "satisfied", "grateful", "optimistic", "hopeful", "enthusiastic", "excited", "grinning", "smiling"]},
    {"genre": "Poster Text Cheerful", "keywords": ["cheerful", "jovial", "merry", "gleeful", "lighthearted", "upbeat", "positive", "contented", "buoyant", "joyous"]},
    {"genre": "Paper Text Elated", "keywords": ["elated", "exhilarated", "thrilled", "over the moon", "on cloud nine", "in high spirits", "walking on air", "beaming", "radiant", "beaming with joy"]},
    {"genre": "Cellphone Text Blissful", "keywords": ["blissful", "serene", "peaceful", "calm", "tranquil", "harmonious", "satisfied", "fulfilled", "grateful", "content"]},
    {"genre": "Tablet Text Jubilant", "keywords": ["jubilant", "gleaming", "beaming", "elated", "ecstatic", "overjoyed", "exultant", "joyous", "radiant", "cheerful"]},
    {"genre": "Digital Screen Text Radiant", "keywords": ["radiant", "glowing", "beaming", "shining", "sparkling", "vibrant", "luminous", "brilliant", "dazzling", "effervescent"]},
    {"genre": "Poster Text Gleeful", "keywords": ["gleeful", "joyful", "merry", "cheerful", "happy", "content", "satisfied", "delighted", "jovial", "elated"]},
    {"genre": "Paper Text Ecstatic", "keywords": ["ecstatic", "overjoyed", "elated", "thrilled", "exhilarated", "joyous", "euphoric", "delighted", "gleeful", "radiant"]},
    {"genre": "Cellphone Text Overjoyed", "keywords": ["overjoyed", "ecstatic", "elated", "thrilled", "delighted", "joyous", "gleeful", "happy", "content", "satisfied"]},
]

positive_signs_media = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Text Road Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Digital Billboard Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Street Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Traffic Light Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Pedestrian Crossing Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Speed Limit Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Construction Zone Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Parking Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Bus Stop Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Public Transport Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
]

words_sports = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Sport Football", "keywords": ["scoring a goal", "teamwork and strategy", "fast-paced action", "dominating the field", "thrilling victory", "precision and power", "goalkeeper save", "winning the match", "unstoppable attack", "celebrating with fans"]},
    {"genre": "Sport Basketball", "keywords": ["slam dunk", "perfect shot", "high-energy offense", "court domination", "fast breaks", "game-winning buzzer beater", "unbelievable assists", "team synergy", "basketball hustle", "stepping up in crunch time"]},
    {"genre": "Sport Tennis", "keywords": ["match point", "powerful serve", "precision volleys", "winning rally", "unstoppable forehand", "grueling backhand", "nail-biting tie-breaker", "dominant performance", "agility and control", "mental toughness"]},
    {"genre": "Sport Cricket", "keywords": ["hit for six", "perfect yorker", "fast-paced bowling", "strategic fielding", "high score innings", "wicket-taking delivery", "batting brilliance", "captivating match", "team spirit", "classic rivalry"]},
    {"genre": "Sport Boxing", "keywords": ["knockout punch", "fighting spirit", "ring dominance", "heavyweight clash", "precision jab", "unpredictable footwork", "brave heart", "strategic defense", "power-packed combination", "hard-hitting knockout"]},
    {"genre": "Sport Rugby", "keywords": ["hard tackle", "scrum dominance", "try scoring", "high-speed breakaway", "unrelenting defense", "teamwork and passion", "line-out win", "rugged endurance", "perfect conversion", "winning try"]},
    {"genre": "Sport Golf", "keywords": ["hole in one", "perfect swing", "calm under pressure", "long drive", "strategic putting", "back-nine charge", "precise approach shot", "eagle on the green", "birdie on a par 5", "winning the tournament"]},
    {"genre": "Sport American Football", "keywords": ["touchdown celebration", "game-changing interception", "quarterback blitz", "rushing the ball", "defensive line pressure", "clutch field goal", "perfect pass", "end zone dominance", "high-impact tackles", "unbreakable drive"]},
    {"genre": "Sport Volleyball", "keywords": ["perfect serve", "block at the net", "spike kill", "dig and set", "team defense", "high-flying attack", "side-out success", "serving aces", "bumping and passing", "winning rally"]},
    {"genre": "Sport Swimming", "keywords": ["fastest lap", "backstroke technique", "butterfly power", "perfect turn", "breathing technique", "champion's swim", "crushing personal best", "tough race finish", "competitive edge", "swimming at full speed"]},
    {"genre": "Sport Cycling", "keywords": ["pedaling power", "mountain climb victory", "sprinting to the finish", "tour de force", "wind resistance", "timed ascent", "group ride strategy", "wheel-to-wheel race", "pacing for the sprint", "winning the race"]},
    {"genre": "Sport Baseball", "keywords": ["home run", "grand slam hit", "pitcher's duel", "fastball strikeout", "double play", "perfect swing", "hit the dirt", "power hitting", "catcher's throw", "stealing second base"]},
    {"genre": "Sport Hockey", "keywords": ["slap shot", "breakaway goal", "power play", "body check", "winning faceoff", "goalie save", "high-speed skating", "defensive shutdown", "game-winning assist", "hat-trick celebration"]},
    {"genre": "Sport Table Tennis", "keywords": ["spin serve", "fast rally", "perfect backhand", "agile footwork", "paddle precision", "quick reflexes", "smashing forehand", "loop shot", "competitive rally", "serving ace"]},
    {"genre": "Sport Badminton", "keywords": ["smash hit", "graceful footwork", "fast shuttlecock", "precise net play", "quick reactions", "high-speed rally", "winning drop shot", "high clear", "control the game", "unpredictable return"]},
    {"genre": "Sport Surfing", "keywords": ["riding the wave", "epic surf", "perfect tube", "deep cutback", "incredible carve", "massive wipeout", "high-speed ride", "surfboard control", "wave dominance", "surfer's paradise"]},
    {"genre": "Sport Skiing", "keywords": ["slalom speed", "downhill race", "perfect carve", "speed on the slopes", "freestyle jumps", "snowy mountain", "mogul challenge", "shredding the powder", "uphill battle", "extreme descent"]},
    {"genre": "Sport MMA", "keywords": ["brutal knockout", "submission victory", "ground and pound", "swift clinch", "powerful takedown", "unbeatable defense", "aggressive striking", "dominant position", "cage control", "hard-hitting combo"]},
    {"genre": "Sport Track and Field", "keywords": ["world record", "sprinting to victory", "perfect jump", "long-distance endurance", "shot put power", "high jump clearance", "fast-paced race", "winning relay", "personal best", "athletic strength"]},
    {"genre": "Sport Formula 1", "keywords": ["pit stop precision", "fastest lap", "overtaking move", "pole position", "high-speed cornering", "track strategy", "engine power", "race tactics", "ultimate speed", "championship win"]},
    {"genre": "Sport Esports", "keywords": ["strategic move", "quick reflexes", "team coordination", "epic win", "perfect headshot", "incredible strategy", "clutch performance", "gaming skill", "competitive spirit", "high-energy gameplay"]},
]

positive_words_sports = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Acting Football", "keywords": ["victorious", "triumphant", "energized", "dynamic", "inspired", "motivated", "unstoppable", "powerful", "dominant", "confident"]},
    {"genre": "Acting Basketball", "keywords": ["thrilled", "excited", "winning", "focused", "determined", "vibrant", "agile", "unstoppable", "explosive", "resilient"]},
    {"genre": "Acting Tennis", "keywords": ["champion", "focused", "determined", "unstoppable", "confident", "skilled", "sharp", "motivated", "energetic", "strong"]},
    {"genre": "Acting Cricket", "keywords": ["victorious", "elated", "dynamic", "skilled", "energetic", "focused", "confident", "dominant", "excited", "optimistic"]},
    {"genre": "Acting Boxing", "keywords": ["strong", "resilient", "champion", "focused", "confident", "unstoppable", "motivated", "tough", "energized", "victorious"]},
    {"genre": "Acting Rugby", "keywords": ["brave", "determined", "unstoppable", "powerful", "confident", "energized", "motivated", "resilient", "dominant", "victorious"]},
    {"genre": "Acting Golf", "keywords": ["focused", "confident", "calm", "determined", "precise", "skilled", "serene", "energized", "grateful", "positive"]},
    {"genre": "Acting American Football", "keywords": ["motivated", "determined", "focused", "energized", "strong", "unstoppable", "resilient", "dominant", "victorious", "confident"]},
    {"genre": "Acting Volleyball", "keywords": ["teamwork", "energetic", "motivated", "confident", "optimistic", "focused", "positive", "agile", "excited", "dynamic"]},
    {"genre": "Acting Swimming", "keywords": ["determined", "resilient", "motivated", "energized", "focused", "champion", "strong", "confident", "positive", "invincible"]},
    {"genre": "Acting Cycling", "keywords": ["determined", "motivated", "energized", "confident", "strong", "unstoppable", "resilient", "dynamic", "focused", "enthusiastic"]},
    {"genre": "Acting Baseball", "keywords": ["victorious", "confident", "energetic", "excited", "determined", "motivated", "unstoppable", "focused", "powerful", "dynamic"]},
    {"genre": "Acting Hockey", "keywords": ["victorious", "resilient", "focused", "energetic", "strong", "confident", "determined", "motivated", "invincible", "excited"]},
    {"genre": "Acting Table Tennis", "keywords": ["focused", "confident", "energetic", "determined", "agile", "motivated", "skilled", "sharp", "resilient", "excited"]},
    {"genre": "Acting Badminton", "keywords": ["agile", "energized", "motivated", "excited", "determined", "resilient", "focused", "confident", "dynamic", "unstoppable"]},
    {"genre": "Acting Surfing", "keywords": ["thrilled", "confident", "excited", "energetic", "free", "vibrant", "dynamic", "motivated", "focused", "strong"]},
    {"genre": "Acting Skiing", "keywords": ["thrilled", "resilient", "confident", "excited", "focused", "energetic", "determined", "strong", "motivated", "unstoppable"]},
    {"genre": "Acting MMA", "keywords": ["resilient", "strong", "focused", "motivated", "unstoppable", "confident", "determined", "energized", "champion", "tough"]},
    {"genre": "Acting Track and Field", "keywords": ["determined", "focused", "energized", "motivated", "strong", "resilient", "victorious", "excited", "confident", "unstoppable"]},
    {"genre": "Acting Formula 1", "keywords": ["focused", "driven", "confident", "determined", "energized", "resilient", "motivated", "dynamic", "powerful", "strategic"]},
    {"genre": "Acting Esports", "keywords": ["focused", "determined", "energized", "competitive", "confident", "resilient", "strategic", "motivated", "skilled", "excited"]},
]

room_objects_media = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Living Room", "keywords": ["sofa", "coffee table", "television", "bookshelf", "armchair", "rug", "lamp", "curtains", "side table", "wall art"]},
    {"genre": "Dining Room", "keywords": ["dining table", "chairs", "china cabinet", "chandelier", "placemats", "candelabra", "buffet", "sideboard", "tablecloth", "china set"]},
    {"genre": "Kitchen", "keywords": ["stove", "refrigerator", "sink", "microwave", "dishwasher", "countertop", "cabinet", "pantry", "island", "kettle"]},
    {"genre": "Bathroom", "keywords": ["toilet", "sink", "shower", "bathtub", "mirror", "towel rack", "medicine cabinet", "toothbrush holder", "shower curtain", "bath mat"]},
    {"genre": "Bedroom", "keywords": ["bed", "nightstand", "dresser", "wardrobe", "closet", "lamp", "bedding", "pillow", "alarm clock", "mirror"]},
    {"genre": "Master Bedroom", "keywords": ["king-size bed", "walk-in closet", "en-suite bathroom", "dresser", "nightstands", "vanity", "armchair", "chandelier", "bedding", "mirror"]},
    {"genre": "Guest Room", "keywords": ["queen-size bed", "nightstand", "dresser", "closet", "lamp", "bedding", "pillow", "alarm clock", "mirror", "artwork"]},
    {"genre": "Kids' Room", "keywords": ["bunk bed", "toy chest", "bookshelf", "desk", "chair", "rug", "wall decals", "nightlight", "play mat", "bean bag"]},
    {"genre": "Nursery", "keywords": ["crib", "changing table", "rocking chair", "diaper pail", "baby monitor", "dresser", "toy box", "nightlight", "wall decals", "playpen"]},
    {"genre": "Home Office", "keywords": ["desk", "office chair", "computer", "bookshelf", "printer", "filing cabinet", "lamp", "whiteboard", "clock", "plant"]},
    {"genre": "Entryway", "keywords": ["coat rack", "shoe rack", "console table", "mirror", "umbrella stand", "welcome mat", "bench", "coat hooks", "key holder", "mail organizer"]},
    {"genre": "Hallway", "keywords": ["console table", "mirror", "wall art", "coat hooks", "bench", "shoe rack", "plant", "light fixture", "runner rug", "storage cabinet"]},
    {"genre": "Laundry Room", "keywords": ["washing machine", "dryer", "laundry basket", "ironing board", "iron", "detergent shelf", "utility sink", "dryer sheets", "clothesline", "pegboard"]},
    {"genre": "Pantry", "keywords": ["shelves", "canned goods", "spice rack", "dry goods containers", "broom", "dustpan", "vacuum cleaner", "cleaning supplies", "step stool", "light"]},
    {"genre": "Closet", "keywords": ["hangers", "shelves", "shoe rack", "storage bins", "clothing rack", "mirror", "light", "ironing board", "vacuum cleaner", "cleaning supplies"]},
    {"genre": "Walk-in Closet", "keywords": ["clothing rack", "shelves", "shoe rack", "island dresser", "mirror", "light", "storage bins", "hanging rods", "bench", "ironing board"]},
    {"genre": "Powder Room", "keywords": ["toilet", "sink", "mirror", "towel rack", "soap dispenser", "toilet paper holder", "artwork", "small rug", "light fixture", "plant"]},
    {"genre": "Bathroom", "keywords": ["shower", "bathtub", "toilet", "sink", "mirror", "towel rack", "medicine cabinet", "shower curtain", "bath mat", "light fixture"]},
    {"genre": "Family Room", "keywords": ["sofa", "coffee table", "television", "bookshelf", "armchair", "rug", "lamp", "curtains", "side table", "wall art"]},
    {"genre": "Recreation Room", "keywords": ["pool table", "ping pong table", "dartboard", "bar", "sofa", "television", "board games", "shelves", "rug", "light fixture"]},
    {"genre": "Basement", "keywords": ["furnace", "water heater", "storage shelves", "laundry area", "utility sink", "workbench", "toolbox", "circuit breaker panel", "light fixture", "crawl space"]},
    {"genre": "Attic", "keywords": ["insulation", "rafters", "storage boxes", "light fixture", "ventilation fan", "staircase", "floorboards", "beams", "roof window", "ladder"]},
    {"genre": "Garage", "keywords": ["car", "workbench", "toolbox", "shelves", "storage bins", "bicycle", "lawnmower", "snow blower", "garden tools", "light fixture"]},
    {"genre": "Workshop", "keywords": ["workbench", "toolbox", "shelves", "storage bins", "saw", "drill", "hammer", "nails", "screws", "light fixture"]},
    {"genre": "Mudroom", "keywords": ["coat hooks", "shoe rack", "bench", "storage bins", "umbrella stand", "welcome mat", "light fixture", "broom", "dustpan", "cleaning supplies"]},
    {"genre": "Sunroom", "keywords": ["sliding doors", "plants", "comfortable seating", "coffee table", "rug", "light fixture", "ceiling fan", "blinds", "side table", "wall art"]},
    {"genre": "Balcony", "keywords": ["railings", "outdoor furniture", "planters", "balcony flooring", "light fixture", "potted plants", "clothesline", "broom", "dustpan", "storage box"]},
    {"genre": "Terrace", "keywords": ["outdoor furniture", "planters", "grill", "decking", "light fixture", "potted plants", "clothesline", "storage box", "umbrella", "side table"]},
]

establishment_objects_media = [
    {"genre": "Other", "keywords": [""]},
    {"genre": "Restaurant", "keywords": ["tables", "chairs", "menus", "dishes", "cutlery", "tablecloths", "napkins", "plates", "stove", "refrigerator"]},
    {"genre": "Bar", "keywords": ["bar stools", "counter", "glasses", "bottles", "shaker", "bar mat", "ambient lighting", "music", "TV screen", "beer fridge"]},
    {"genre": "Café", "keywords": ["tables", "chairs", "cups", "saucers", "coffee machine", "coffee beans", "sugar bowl", "creamer", "shelves", "menu boards"]},
    {"genre": "Bakery", "keywords": ["display case", "shelves", "breads", "pastries", "cakes", "oven", "dough mixer", "bread basket", "paper bags", "tray"]},
    {"genre": "Grocery Store", "keywords": ["aisles", "shopping cart", "fresh produce", "canned goods", "dairy products", "freezer section", "cash register", "fruit basket", "vegetable bin", "checkout counter"]},
    {"genre": "Pharmacy", "keywords": ["shelves", "medications", "bandages", "creams", "vitamins", "cash register", "prescriptions", "beauty products", "health products", "hygiene products"]},
    {"genre": "Bookstore", "keywords": ["shelves", "books", "magazines", "novels", "comic books", "new release table", "bookmarks", "cash register", "shopping basket", "reading nook"]},
    {"genre": "Clothing Store", "keywords": ["clothing racks", "mannequins", "clothes", "accessories", "fitting rooms", "mirrors", "price tags", "shopping basket", "sale rack", "cash register"]},
    {"genre": "Hardware Store", "keywords": ["shelves", "tools", "nails", "screws", "paint", "clamps", "work gloves", "shopping basket", "sale bin", "cash register"]},
    {"genre": "Gas Station", "keywords": ["fuel pumps", "fuel nozzles", "payment screen", "cleaning products", "motor oil", "brooms", "shopping basket", "snack shelf", "beverage cooler", "checkout counter"]},
    {"genre": "Hair Salon", "keywords": ["mirrors", "hairdressing chairs", "combs", "scissors", "hairdryers", "hair products", "towels", "shopping basket", "sale bin", "magazine rack"]},
    {"genre": "Gym", "keywords": ["yoga mats", "dumbbells", "exercise machines", "treadmills", "stationary bikes", "fitness equipment", "towel basket", "water bottle station", "lockers", "showers"]},
    {"genre": "School", "keywords": ["desks", "chairs", "blackboards", "books", "notebooks", "pens", "backpacks", "stationery", "locker", "classroom"]},
    {"genre": "Hospital", "keywords": ["hospital beds", "monitors", "bandages", "medications", "syringes", "gloves", "masks", "medicine cabinet", "nurse station", "waiting area"]},
    {"genre": "Bank", "keywords": ["teller counters", "cashiers", "ATMs", "credit cards", "banknotes", "coins", "document shredder", "customer service desk", "safety deposit boxes", "waiting area"]},
    {"genre": "Post Office", "keywords": ["service counters", "cashiers", "mailboxes", "stamps", "parcels", "letterbox", "customer service desk", "postage scale", "waiting area", "postal forms"]},
    {"genre": "Museum", "keywords": ["exhibits", "artworks", "information panels", "interactive screens", "brochure rack", "cash register", "souvenir shop", "programs", "guides", "display cases"]},
    {"genre": "Cinema", "keywords": ["screens", "projectors", "seats", "popcorn", "tickets", "beverage stand", "candy shelf", "programs", "guides", "souvenir shop"]},
    {"genre": "Theater", "keywords": ["stage", "curtains", "seats", "programs", "tickets", "beverage stand", "candy shelf", "programs", "guides", "souvenir shop"]},
    {"genre": "Concert Hall", "keywords": ["stage", "speakers", "musical instruments", "seats", "tickets", "beverage stand", "candy shelf", "programs", "guides", "souvenir shop"]},
    {"genre": "Park", "keywords": ["benches", "playgrounds", "garbage bins", "information boards", "signposts", "brochure rack", "picnic tables", "water fountains", "restrooms", "walking paths"]},
    {"genre": "Beach", "keywords": ["towels", "umbrellas", "beach chairs", "picnic basket", "beverage cooler", "candy shelf", "programs", "guides", "souvenir shop", "sand toys"]},
    {"genre": "Spa", "keywords": ["massage tables", "candles", "essential oils", "towels", "bathrobes", "slippers", "sauna", "jacuzzi", "facial masks", "relaxation area"]},
    {"genre": "Hotel", "keywords": ["reception desk", "lobby", "elevators", "rooms", "beds", "bathrooms", "luggage", "key cards", "room service menu", "concierge desk"]},
    {"genre": "Supermarket", "keywords": ["aisles", "shopping carts", "fresh produce", "canned goods", "dairy products", "freezer section", "cash register", "fruit basket", "vegetable bin", "checkout counter"]},
    {"genre": "Florist", "keywords": ["flower arrangements", "vases", "bouquets", "flower pots", "gardening tools", "gift baskets", "cards", "ribbons", "wrapping paper", "display case"]},
    {"genre": "Pet Store", "keywords": ["pet food", "pet toys", "pet accessories", "cages", "aquariums", "leashes", "collars", "grooming products", "pet beds", "display shelves"]},
    {"genre": "Toy Store", "keywords": ["shelves", "toys", "games", "puzzles", "plush animals", "action figures", "board games", "building blocks", "remote-controlled cars", "educational kits"]},
]

video_styles = [  
    {"genre": "Other", "keywords": [""]},
    {"genre": "Establishment Restaurant", "keywords": ["tables", "chairs", "menus", "dishes", "cutlery", "tablecloths", "napkins", "plates", "stove", "refrigerator"]},
    {"genre": "Establishment Bar", "keywords": ["bar stools", "counter", "glasses", "bottles", "shaker", "bar mat", "ambient lighting", "music", "TV screen", "beer fridge"]},
    {"genre": "Establishment Café", "keywords": ["tables", "chairs", "cups", "saucers", "coffee machine", "coffee beans", "sugar bowl", "creamer", "shelves", "menu boards"]},
    {"genre": "Establishment Bakery", "keywords": ["display case", "shelves", "breads", "pastries", "cakes", "oven", "dough mixer", "bread basket", "paper bags", "tray"]},
    {"genre": "Establishment Grocery Store", "keywords": ["aisles", "shopping cart", "fresh produce", "canned goods", "dairy products", "freezer section", "cash register", "fruit basket", "vegetable bin", "checkout counter"]},
    {"genre": "Establishment Pharmacy", "keywords": ["shelves", "medications", "bandages", "creams", "vitamins", "cash register", "prescriptions", "beauty products", "health products", "hygiene products"]},
    {"genre": "Establishment Bookstore", "keywords": ["shelves", "books", "magazines", "novels", "comic books", "new release table", "bookmarks", "cash register", "shopping basket", "reading nook"]},
    {"genre": "Establishment Clothing Store", "keywords": ["clothing racks", "mannequins", "clothes", "accessories", "fitting rooms", "mirrors", "price tags", "shopping basket", "sale rack", "cash register"]},
    {"genre": "Establishment Hardware Store", "keywords": ["shelves", "tools", "nails", "screws", "paint", "clamps", "work gloves", "shopping basket", "sale bin", "cash register"]},
    {"genre": "Establishment Gas Station", "keywords": ["fuel pumps", "fuel nozzles", "payment screen", "cleaning products", "motor oil", "brooms", "shopping basket", "snack shelf", "beverage cooler", "checkout counter"]},
    {"genre": "Establishment Hair Salon", "keywords": ["mirrors", "hairdressing chairs", "combs", "scissors", "hairdryers", "hair products", "towels", "shopping basket", "sale bin", "magazine rack"]},
    {"genre": "Establishment Gym", "keywords": ["yoga mats", "dumbbells", "exercise machines", "treadmills", "stationary bikes", "fitness equipment", "towel basket", "water bottle station", "lockers", "showers"]},
    {"genre": "Establishment School", "keywords": ["desks", "chairs", "blackboards", "books", "notebooks", "pens", "backpacks", "stationery", "locker", "classroom"]},
    {"genre": "Establishment Hospital", "keywords": ["hospital beds", "monitors", "bandages", "medications", "syringes", "gloves", "masks", "medicine cabinet", "nurse station", "waiting area"]},
    {"genre": "Establishment Bank", "keywords": ["teller counters", "cashiers", "ATMs", "credit cards", "banknotes", "coins", "document shredder", "customer service desk", "safety deposit boxes", "waiting area"]},
    {"genre": "Establishment Post Office", "keywords": ["service counters", "cashiers", "mailboxes", "stamps", "parcels", "letterbox", "customer service desk", "postage scale", "waiting area", "postal forms"]},
    {"genre": "Establishment Museum", "keywords": ["exhibits", "artworks", "information panels", "interactive screens", "brochure rack", "cash register", "souvenir shop", "programs", "guides", "display cases"]},
    {"genre": "Establishment Cinema", "keywords": ["screens", "projectors", "seats", "popcorn", "tickets", "beverage stand", "candy shelf", "programs", "guides", "souvenir shop"]},
    {"genre": "Establishment Theater", "keywords": ["stage", "curtains", "seats", "programs", "tickets", "beverage stand", "candy shelf", "programs", "guides", "souvenir shop"]},
    {"genre": "Establishment Concert Hall", "keywords": ["stage", "speakers", "musical instruments", "seats", "tickets", "beverage stand", "candy shelf", "programs", "guides", "souvenir shop"]},
    {"genre": "Establishment Park", "keywords": ["benches", "playgrounds", "garbage bins", "information boards", "signposts", "brochure rack", "picnic tables", "water fountains", "restrooms", "walking paths"]},
    {"genre": "Establishment Beach", "keywords": ["towels", "umbrellas", "beach chairs", "picnic basket", "beverage cooler", "candy shelf", "programs", "guides", "souvenir shop", "sand toys"]},
    {"genre": "Establishment Spa", "keywords": ["massage tables", "candles", "essential oils", "towels", "bathrobes", "slippers", "sauna", "jacuzzi", "facial masks", "relaxation area"]},
    {"genre": "Establishment Hotel", "keywords": ["reception desk", "lobby", "elevators", "rooms", "beds", "bathrooms", "luggage", "key cards", "room service menu", "concierge desk"]},
    {"genre": "Establishment Supermarket", "keywords": ["aisles", "shopping carts", "fresh produce", "canned goods", "dairy products", "freezer section", "cash register", "fruit basket", "vegetable bin", "checkout counter"]},
    {"genre": "Establishment Florist", "keywords": ["flower arrangements", "vases", "bouquets", "flower pots", "gardening tools", "gift baskets", "cards", "ribbons", "wrapping paper", "display case"]},
    {"genre": "Establishment Pet Store", "keywords": ["pet food", "pet toys", "pet accessories", "cages", "aquariums", "leashes", "collars", "grooming products", "pet beds", "display shelves"]},
    {"genre": "Establishment Toy Store", "keywords": ["shelves", "toys", "games", "puzzles", "plush animals", "action figures", "board games", "building blocks", "remote-controlled cars", "educational kits"]},    
    {"genre": "Living Room", "keywords": ["sofa", "coffee table", "television", "bookshelf", "armchair", "rug", "lamp", "curtains", "side table", "wall art"]},
    {"genre": "Dining Room", "keywords": ["dining table", "chairs", "china cabinet", "chandelier", "placemats", "candelabra", "buffet", "sideboard", "tablecloth", "china set"]},
    {"genre": "Kitchen", "keywords": ["stove", "refrigerator", "sink", "microwave", "dishwasher", "countertop", "cabinet", "pantry", "island", "kettle"]},
    {"genre": "Bathroom", "keywords": ["toilet", "sink", "shower", "bathtub", "mirror", "towel rack", "medicine cabinet", "toothbrush holder", "shower curtain", "bath mat"]},
    {"genre": "Bedroom", "keywords": ["bed", "nightstand", "dresser", "wardrobe", "closet", "lamp", "bedding", "pillow", "alarm clock", "mirror"]},
    {"genre": "Master Bedroom", "keywords": ["king-size bed", "walk-in closet", "en-suite bathroom", "dresser", "nightstands", "vanity", "armchair", "chandelier", "bedding", "mirror"]},
    {"genre": "Guest Room", "keywords": ["queen-size bed", "nightstand", "dresser", "closet", "lamp", "bedding", "pillow", "alarm clock", "mirror", "artwork"]},
    {"genre": "Kids' Room", "keywords": ["bunk bed", "toy chest", "bookshelf", "desk", "chair", "rug", "wall decals", "nightlight", "play mat", "bean bag"]},
    {"genre": "Nursery", "keywords": ["crib", "changing table", "rocking chair", "diaper pail", "baby monitor", "dresser", "toy box", "nightlight", "wall decals", "playpen"]},
    {"genre": "Home Office", "keywords": ["desk", "office chair", "computer", "bookshelf", "printer", "filing cabinet", "lamp", "whiteboard", "clock", "plant"]},
    {"genre": "Entryway", "keywords": ["coat rack", "shoe rack", "console table", "mirror", "umbrella stand", "welcome mat", "bench", "coat hooks", "key holder", "mail organizer"]},
    {"genre": "Hallway", "keywords": ["console table", "mirror", "wall art", "coat hooks", "bench", "shoe rack", "plant", "light fixture", "runner rug", "storage cabinet"]},
    {"genre": "Laundry Room", "keywords": ["washing machine", "dryer", "laundry basket", "ironing board", "iron", "detergent shelf", "utility sink", "dryer sheets", "clothesline", "pegboard"]},
    {"genre": "Pantry", "keywords": ["shelves", "canned goods", "spice rack", "dry goods containers", "broom", "dustpan", "vacuum cleaner", "cleaning supplies", "step stool", "light"]},
    {"genre": "Closet", "keywords": ["hangers", "shelves", "shoe rack", "storage bins", "clothing rack", "mirror", "light", "ironing board", "vacuum cleaner", "cleaning supplies"]},
    {"genre": "Walk-in Closet", "keywords": ["clothing rack", "shelves", "shoe rack", "island dresser", "mirror", "light", "storage bins", "hanging rods", "bench", "ironing board"]},
    {"genre": "Powder Room", "keywords": ["toilet", "sink", "mirror", "towel rack", "soap dispenser", "toilet paper holder", "artwork", "small rug", "light fixture", "plant"]},
    {"genre": "Bathroom", "keywords": ["shower", "bathtub", "toilet", "sink", "mirror", "towel rack", "medicine cabinet", "shower curtain", "bath mat", "light fixture"]},
    {"genre": "Family Room", "keywords": ["sofa", "coffee table", "television", "bookshelf", "armchair", "rug", "lamp", "curtains", "side table", "wall art"]},
    {"genre": "Recreation Room", "keywords": ["pool table", "ping pong table", "dartboard", "bar", "sofa", "television", "board games", "shelves", "rug", "light fixture"]},
    {"genre": "Basement", "keywords": ["furnace", "water heater", "storage shelves", "laundry area", "utility sink", "workbench", "toolbox", "circuit breaker panel", "light fixture", "crawl space"]},
    {"genre": "Attic", "keywords": ["insulation", "rafters", "storage boxes", "light fixture", "ventilation fan", "staircase", "floorboards", "beams", "roof window", "ladder"]},
    {"genre": "Garage", "keywords": ["car", "workbench", "toolbox", "shelves", "storage bins", "bicycle", "lawnmower", "snow blower", "garden tools", "light fixture"]},
    {"genre": "Workshop", "keywords": ["workbench", "toolbox", "shelves", "storage bins", "saw", "drill", "hammer", "nails", "screws", "light fixture"]},
    {"genre": "Mudroom", "keywords": ["coat hooks", "shoe rack", "bench", "storage bins", "umbrella stand", "welcome mat", "light fixture", "broom", "dustpan", "cleaning supplies"]},
    {"genre": "Sunroom", "keywords": ["sliding doors", "plants", "comfortable seating", "coffee table", "rug", "light fixture", "ceiling fan", "blinds", "side table", "wall art"]},
    {"genre": "Balcony", "keywords": ["railings", "outdoor furniture", "planters", "balcony flooring", "light fixture", "potted plants", "clothesline", "broom", "dustpan", "storage box"]},
    {"genre": "Terrace", "keywords": ["outdoor furniture", "planters", "grill", "decking", "light fixture", "potted plants", "clothesline", "storage box", "umbrella", "side table"]},    
    {"genre": "Sport Football", "keywords": ["scoring a goal", "teamwork and strategy", "fast-paced action", "dominating the field", "thrilling victory", "precision and power", "goalkeeper save", "winning the match", "unstoppable attack", "celebrating with fans"]},
    {"genre": "Sport Basketball", "keywords": ["slam dunk", "perfect shot", "high-energy offense", "court domination", "fast breaks", "game-winning buzzer beater", "unbelievable assists", "team synergy", "basketball hustle", "stepping up in crunch time"]},
    {"genre": "Sport Tennis", "keywords": ["match point", "powerful serve", "precision volleys", "winning rally", "unstoppable forehand", "grueling backhand", "nail-biting tie-breaker", "dominant performance", "agility and control", "mental toughness"]},
    {"genre": "Sport Cricket", "keywords": ["hit for six", "perfect yorker", "fast-paced bowling", "strategic fielding", "high score innings", "wicket-taking delivery", "batting brilliance", "captivating match", "team spirit", "classic rivalry"]},
    {"genre": "Sport Boxing", "keywords": ["knockout punch", "fighting spirit", "ring dominance", "heavyweight clash", "precision jab", "unpredictable footwork", "brave heart", "strategic defense", "power-packed combination", "hard-hitting knockout"]},
    {"genre": "Sport Rugby", "keywords": ["hard tackle", "scrum dominance", "try scoring", "high-speed breakaway", "unrelenting defense", "teamwork and passion", "line-out win", "rugged endurance", "perfect conversion", "winning try"]},
    {"genre": "Sport Golf", "keywords": ["hole in one", "perfect swing", "calm under pressure", "long drive", "strategic putting", "back-nine charge", "precise approach shot", "eagle on the green", "birdie on a par 5", "winning the tournament"]},
    {"genre": "Sport American Football", "keywords": ["touchdown celebration", "game-changing interception", "quarterback blitz", "rushing the ball", "defensive line pressure", "clutch field goal", "perfect pass", "end zone dominance", "high-impact tackles", "unbreakable drive"]},
    {"genre": "Sport Volleyball", "keywords": ["perfect serve", "block at the net", "spike kill", "dig and set", "team defense", "high-flying attack", "side-out success", "serving aces", "bumping and passing", "winning rally"]},
    {"genre": "Sport Swimming", "keywords": ["fastest lap", "backstroke technique", "butterfly power", "perfect turn", "breathing technique", "champion's swim", "crushing personal best", "tough race finish", "competitive edge", "swimming at full speed"]},
    {"genre": "Sport Cycling", "keywords": ["pedaling power", "mountain climb victory", "sprinting to the finish", "tour de force", "wind resistance", "timed ascent", "group ride strategy", "wheel-to-wheel race", "pacing for the sprint", "winning the race"]},
    {"genre": "Sport Baseball", "keywords": ["home run", "grand slam hit", "pitcher's duel", "fastball strikeout", "double play", "perfect swing", "hit the dirt", "power hitting", "catcher's throw", "stealing second base"]},
    {"genre": "Sport Hockey", "keywords": ["slap shot", "breakaway goal", "power play", "body check", "winning faceoff", "goalie save", "high-speed skating", "defensive shutdown", "game-winning assist", "hat-trick celebration"]},
    {"genre": "Sport Table Tennis", "keywords": ["spin serve", "fast rally", "perfect backhand", "agile footwork", "paddle precision", "quick reflexes", "smashing forehand", "loop shot", "competitive rally", "serving ace"]},
    {"genre": "Sport Badminton", "keywords": ["smash hit", "graceful footwork", "fast shuttlecock", "precise net play", "quick reactions", "high-speed rally", "winning drop shot", "high clear", "control the game", "unpredictable return"]},
    {"genre": "Sport Surfing", "keywords": ["riding the wave", "epic surf", "perfect tube", "deep cutback", "incredible carve", "massive wipeout", "high-speed ride", "surfboard control", "wave dominance", "surfer's paradise"]},
    {"genre": "Sport Skiing", "keywords": ["slalom speed", "downhill race", "perfect carve", "speed on the slopes", "freestyle jumps", "snowy mountain", "mogul challenge", "shredding the powder", "uphill battle", "extreme descent"]},
    {"genre": "Sport MMA", "keywords": ["brutal knockout", "submission victory", "ground and pound", "swift clinch", "powerful takedown", "unbeatable defense", "aggressive striking", "dominant position", "cage control", "hard-hitting combo"]},
    {"genre": "Sport Track and Field", "keywords": ["world record", "sprinting to victory", "perfect jump", "long-distance endurance", "shot put power", "high jump clearance", "fast-paced race", "winning relay", "personal best", "athletic strength"]},
    {"genre": "Sport Formula 1", "keywords": ["pit stop precision", "fastest lap", "overtaking move", "pole position", "high-speed cornering", "track strategy", "engine power", "race tactics", "ultimate speed", "championship win"]},
    {"genre": "Sport Esports", "keywords": ["strategic move", "quick reflexes", "team coordination", "epic win", "perfect headshot", "incredible strategy", "clutch performance", "gaming skill", "competitive spirit", "high-energy gameplay"]},    
    {"genre": "Acting Football", "keywords": ["victorious", "triumphant", "energized", "dynamic", "inspired", "motivated", "unstoppable", "powerful", "dominant", "confident"]},
    {"genre": "Acting Basketball", "keywords": ["thrilled", "excited", "winning", "focused", "determined", "vibrant", "agile", "unstoppable", "explosive", "resilient"]},
    {"genre": "Acting Tennis", "keywords": ["champion", "focused", "determined", "unstoppable", "confident", "skilled", "sharp", "motivated", "energetic", "strong"]},
    {"genre": "Acting Cricket", "keywords": ["victorious", "elated", "dynamic", "skilled", "energetic", "focused", "confident", "dominant", "excited", "optimistic"]},
    {"genre": "Acting Boxing", "keywords": ["strong", "resilient", "champion", "focused", "confident", "unstoppable", "motivated", "tough", "energized", "victorious"]},
    {"genre": "Acting Rugby", "keywords": ["brave", "determined", "unstoppable", "powerful", "confident", "energized", "motivated", "resilient", "dominant", "victorious"]},
    {"genre": "Acting Golf", "keywords": ["focused", "confident", "calm", "determined", "precise", "skilled", "serene", "energized", "grateful", "positive"]},
    {"genre": "Acting American Football", "keywords": ["motivated", "determined", "focused", "energized", "strong", "unstoppable", "resilient", "dominant", "victorious", "confident"]},
    {"genre": "Acting Volleyball", "keywords": ["teamwork", "energetic", "motivated", "confident", "optimistic", "focused", "positive", "agile", "excited", "dynamic"]},
    {"genre": "Acting Swimming", "keywords": ["determined", "resilient", "motivated", "energized", "focused", "champion", "strong", "confident", "positive", "invincible"]},
    {"genre": "Acting Cycling", "keywords": ["determined", "motivated", "energized", "confident", "strong", "unstoppable", "resilient", "dynamic", "focused", "enthusiastic"]},
    {"genre": "Acting Baseball", "keywords": ["victorious", "confident", "energetic", "excited", "determined", "motivated", "unstoppable", "focused", "powerful", "dynamic"]},
    {"genre": "Acting Hockey", "keywords": ["victorious", "resilient", "focused", "energetic", "strong", "confident", "determined", "motivated", "invincible", "excited"]},
    {"genre": "Acting Table Tennis", "keywords": ["focused", "confident", "energetic", "determined", "agile", "motivated", "skilled", "sharp", "resilient", "excited"]},
    {"genre": "Acting Badminton", "keywords": ["agile", "energized", "motivated", "excited", "determined", "resilient", "focused", "confident", "dynamic", "unstoppable"]},
    {"genre": "Acting Surfing", "keywords": ["thrilled", "confident", "excited", "energetic", "free", "vibrant", "dynamic", "motivated", "focused", "strong"]},
    {"genre": "Acting Skiing", "keywords": ["thrilled", "resilient", "confident", "excited", "focused", "energetic", "determined", "strong", "motivated", "unstoppable"]},
    {"genre": "Acting MMA", "keywords": ["resilient", "strong", "focused", "motivated", "unstoppable", "confident", "determined", "energized", "champion", "tough"]},
    {"genre": "Acting Track and Field", "keywords": ["determined", "focused", "energized", "motivated", "strong", "resilient", "victorious", "excited", "confident", "unstoppable"]},
    {"genre": "Acting Formula 1", "keywords": ["focused", "driven", "confident", "determined", "energized", "resilient", "motivated", "dynamic", "powerful", "strategic"]},
    {"genre": "Acting Esports", "keywords": ["focused", "determined", "energized", "competitive", "confident", "resilient", "strategic", "motivated", "skilled", "excited"]},    
    {"genre": "Text Road Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Digital Billboard Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Street Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Traffic Light Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Pedestrian Crossing Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Speed Limit Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Construction Zone Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Parking Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Bus Stop Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},
    {"genre": "Text Public Transport Sign Positive", "keywords": ["Drive Safe", "Stay Alert", "Be Kind", "Smile Today", "Enjoy the Ride", "Keep Calm", "Stay Positive", "Be Happy", "Choose Joy", "Spread Love"]},    
    {"genre": "Sign Text Joyful", "keywords": ["joyful", "elated", "ecstatic", "content", "cheerful", "delighted", "blissful", "radiant", "euphoric", "overjoyed"]},
    {"genre": "Digital Screen Text Happy", "keywords": ["happy", "pleased", "satisfied", "grateful", "optimistic", "hopeful", "enthusiastic", "excited", "grinning", "smiling"]},
    {"genre": "Poster Text Cheerful", "keywords": ["cheerful", "jovial", "merry", "gleeful", "lighthearted", "upbeat", "positive", "contented", "buoyant", "joyous"]},
    {"genre": "Paper Text Elated", "keywords": ["elated", "exhilarated", "thrilled", "over the moon", "on cloud nine", "in high spirits", "walking on air", "beaming", "radiant", "beaming with joy"]},
    {"genre": "Cellphone Text Blissful", "keywords": ["blissful", "serene", "peaceful", "calm", "tranquil", "harmonious", "satisfied", "fulfilled", "grateful", "content"]},
    {"genre": "Tablet Text Jubilant", "keywords": ["jubilant", "gleaming", "beaming", "elated", "ecstatic", "overjoyed", "exultant", "joyous", "radiant", "cheerful"]},
    {"genre": "Digital Screen Text Radiant", "keywords": ["radiant", "glowing", "beaming", "shining", "sparkling", "vibrant", "luminous", "brilliant", "dazzling", "effervescent"]},
    {"genre": "Poster Text Gleeful", "keywords": ["gleeful", "joyful", "merry", "cheerful", "happy", "content", "satisfied", "delighted", "jovial", "elated"]},
    {"genre": "Paper Text Ecstatic", "keywords": ["ecstatic", "overjoyed", "elated", "thrilled", "exhilarated", "joyous", "euphoric", "delighted", "gleeful", "radiant"]},
    {"genre": "Cellphone Text Overjoyed", "keywords": ["overjoyed", "ecstatic", "elated", "thrilled", "delighted", "joyous", "gleeful", "happy", "content", "satisfied"]},    
    {"genre": "Text Annoyed", "keywords": ["idiot", "stupid", "dumb", "moron", "loser", "jerk", "worthless", "clueless", "pathetic", "useless"]},
    {"genre": "Text Frustration", "keywords": ["crap", "hell", "damn", "bloody", "freaking", "screw it", "bugger", "shut up", "shut it", "get lost"]},
    {"genre": "Text Anger", "keywords": ["bastard", "asshole", "bitch", "son of a bitch", "dickhead", "twat", "wanker", "prick", "douchebag", "piss off"]},
    {"genre": "Text Sarcasm", "keywords": ["yeah, right", "good luck with that", "sure, whatever", "big deal", "who cares", "don't make me laugh", "as if", "no way", "not a chance", "yeah, right"]},
    {"genre": "Text Disgust", "keywords": ["gross", "nasty", "disgusting", "revolting", "sickening", "vile", "foul", "yuck", "eww", "ugh"]},
    {"genre": "Text Exasperation", "keywords": ["unbelievable", "ridiculous", "seriously", "how stupid", "out of control", "insane", "no way", "what a joke", "come on", "you've got to be kidding me"]},
    {"genre": "Text Insult", "keywords": ["shut your mouth", "get a life", "go to hell", "go away", "leave me alone", "get out of here", "shut it", "drop dead", "screw you", "suck it"]},
    {"genre": "Text Disappointment", "keywords": ["what a letdown", "are you serious?", "I can't believe this", "this is terrible", "what a waste", "this is a joke", "so much for that", "what's wrong with you?", "this is pathetic", "I’m done"]},
    {"genre": "Text Rage", "keywords": ["damn it", "you’re dead to me", "go fuck yourself", "screw you", "burn in hell", "get the hell out", "eat shit", "fuck off", "kiss my ass", "blow it out your ass"]},
    {"genre": "Text Confusion", "keywords": ["what the hell", "what the fuck", "who cares", "I don't get it", "this makes no sense", "what’s going on", "are you kidding me", "no idea", "what the hell is happening", "where am I?"]},    
    {"genre": "Sign Text Annoyed", "keywords": ["idiot", "stupid", "dumb", "moron", "loser", "jerk", "worthless", "clueless", "pathetic", "useless"]},
    {"genre": "Digital Screen Text Annoyed", "keywords": ["crap", "hell", "damn", "bloody", "freaking", "screw it", "bugger", "shut up", "shut it", "get lost"]},
    {"genre": "Poster Text Frustrated", "keywords": ["pissed off", "fed up", "sick of it", "done with this", "over it", "can't stand it", "enough already", "had enough", "this sucks", "this blows"]},
    {"genre": "Paper Text Exasperated", "keywords": ["for crying out loud", "give me a break", "are you kidding me", "seriously", "unbelievable", "no way", "come on", "what the hell", "what the heck", "what the fuck"]},
    {"genre": "Cellphone Text Angry", "keywords": ["bastard", "asshole", "bitch", "dickhead", "twat", "wanker", "prick", "douchebag", "piss off", "fuck off"]},
    {"genre": "Tablet Text Annoyed", "keywords": ["bloody hell", "bugger off", "bollocks", "bollocks to that", "sod off", "shut your mouth", "get a life", "go to hell", "go away", "leave me alone"]},
    {"genre": "Digital Screen Text Frustrated", "keywords": ["damn it", "shit", "crap", "piss", "arse", "bollocks", "bugger", "sod", "twat", "wanker"]},
    {"genre": "Poster Text Exasperated", "keywords": ["what the hell", "what the heck", "what the fuck", "seriously", "unbelievable", "no way", "come on", "are you kidding me", "for crying out loud", "give me a break"]},
    {"genre": "Paper Text Angry", "keywords": ["bastard", "asshole", "bitch", "dickhead", "twat", "wanker", "prick", "douchebag", "piss off", "fuck off"]},
    {"genre": "Cellphone Text Frustrated", "keywords": ["bloody hell", "bugger off", "bollocks", "bollocks to that", "sod off", "shut your mouth", "get a life", "go to hell", "go away", "leave me alone"]},    
    {"genre": "A meal of Roast Chicken", "keywords": ["whole chicken", "roasted", "crispy skin", "herbs", "buttery", "golden brown", "oven-baked", "holiday dish", "juicy", "classic dinner"]},
    {"genre": "A meal of Caesar Salad", "keywords": ["romaine lettuce", "croutons", "parmesan cheese", "Caesar dressing", "anchovies", "creamy", "fresh", "appetizer", "light meal", "popular salad"]},
    {"genre": "A meal of Beef Steak", "keywords": ["grilled", "medium-rare", "juicy", "seasoned", "marbled", "prime cut", "sizzling", "restaurant favorite", "tender", "classic entree"]},
    {"genre": "A meal of Vegetable Stir-Fry", "keywords": ["mixed vegetables", "soy sauce", "garlic", "ginger", "quick-cooked", "Asian-style", "healthy", "colorful", "light oil", "savory"]},
    {"genre": "A meal of Spaghetti Bolognese", "keywords": ["pasta", "ground beef", "tomato sauce", "herbs", "parmesan", "Italian cuisine", "hearty", "classic dish", "red sauce", "garlic"]},
    {"genre": "A meal of Pizza Margherita", "keywords": ["thin crust", "mozzarella cheese", "tomato sauce", "fresh basil", "Italian style", "wood-fired", "classic pizza", "simple", "crispy", "savory"]},
    {"genre": "A meal of Grilled Salmon", "keywords": ["fish", "lemon slices", "herbs", "healthy", "omega-3", "pink flesh", "dinner entree", "charred", "lightly seasoned", "delicate flavor"]},
    {"genre": "A meal of Tacos", "keywords": ["soft tortilla", "ground beef", "shredded lettuce", "cheese", "sour cream", "Mexican food", "spiced", "finger food", "guacamole", "colorful"]},
    {"genre": "A meal of Sushi Roll", "keywords": ["seaweed wrap", "vinegared rice", "raw fish", "wasabi", "soy sauce", "Japanese cuisine", "bite-sized", "colorful", "delicate", "seafood"]},
    {"genre": "A meal of Hamburger", "keywords": ["beef patty", "lettuce", "tomato", "bun", "cheese", "grilled", "American classic", "fast food", "juicy", "savory"]},
    {"genre": "A meal of Vegetarian Curry", "keywords": ["spices", "coconut milk", "vegetables", "rice", "Indian cuisine", "creamy", "flavorful", "spicy", "colorful", "plant-based"]},
    {"genre": "A meal of Roast Turkey", "keywords": ["whole turkey", "stuffing", "cranberry sauce", "gravy", "golden brown", "Thanksgiving dish", "holiday favorite", "crispy skin", "juicy", "aromatic"]},
    {"genre": "A meal of Pad Thai", "keywords": ["rice noodles", "peanuts", "bean sprouts", "shrimp", "egg", "lime", "Thai cuisine", "sweet and savory", "spicy", "stir-fried"]},
    {"genre": "A meal of Barbecue Ribs", "keywords": ["pork ribs", "BBQ sauce", "smoky flavor", "grilled", "sticky", "fall-off-the-bone", "American BBQ", "savory", "sweet glaze", "hearty"]},
    {"genre": "A meal of Chocolate Cake", "keywords": ["rich", "moist", "layered", "frosting", "dessert", "decadent", "sweet", "baked", "celebration", "indulgent"]},
    {"genre": "A meal of Fried Rice", "keywords": ["rice", "soy sauce", "vegetables", "egg", "quick-cooked", "Chinese cuisine", "savory", "stir-fried", "easy meal", "colorful"]},
    {"genre": "A meal of Greek Salad", "keywords": ["cucumber", "feta cheese", "tomato", "olives", "olive oil", "Mediterranean style", "fresh", "light", "healthy", "appetizer"]},
    {"genre": "A meal of Shepherd's Pie", "keywords": ["ground lamb", "mashed potatoes", "baked", "gravy", "hearty", "English dish", "comfort food", "savory", "layered", "classic"]},
    {"genre": "A meal of Shrimp Cocktail", "keywords": ["chilled shrimp", "cocktail sauce", "lemon wedge", "appetizer", "seafood", "light", "zesty", "classic starter", "fresh", "party favorite"]},
    {"genre": "A meal of Chicken Tikka Masala", "keywords": ["grilled chicken", "spiced tomato sauce", "creamy", "Indian cuisine", "aromatic", "rich flavor", "rice accompaniment", "popular dish", "vibrant", "savory"]},
    {"genre": "A meal of Lasagna", "keywords": ["pasta sheets", "ground beef", "tomato sauce", "cheese layers", "Italian dish", "baked", "hearty", "savory", "comfort food", "rich"]},
    {"genre": "A meal of Omelette", "keywords": ["eggs", "cheese", "herbs", "vegetables", "breakfast", "fluffy", "savory", "quick meal", "simple", "protein-rich"]},
    {"genre": "A meal of Clam Chowder", "keywords": ["creamy soup", "clams", "potatoes", "onions", "New England style", "hearty", "warm", "seafood", "savory", "classic"]},
    {"genre": "A meal of Pancakes", "keywords": ["fluffy", "syrup", "breakfast", "stacked", "buttery", "sweet", "quick", "American favorite", "batter", "golden brown"]},
    {"genre": "A meal of Spring Rolls", "keywords": ["rice paper wrap", "vegetables", "shrimp", "dipping sauce", "Vietnamese cuisine", "fresh", "light", "healthy", "finger food", "colorful"]},
    {"genre": "A meal of Macaroni and Cheese", "keywords": ["pasta", "cheddar", "creamy", "baked", "comfort food", "hearty", "childhood favorite", "simple", "golden", "savory"]},
    {"genre": "A meal of Fish and Chips", "keywords": ["fried fish", "crispy batter", "French fries", "tartar sauce", "pub food", "British classic", "golden", "hearty", "comfort food", "savory"]},
    {"genre": "A meal of Falafel Wrap", "keywords": ["chickpeas", "herbs", "fried balls", "pita bread", "Middle Eastern", "tahini", "healthy", "vegetarian", "spiced", "street food"]},
    {"genre": "A meal of Cheesecake", "keywords": ["creamy", "sweet", "graham cracker crust", "baked", "dessert", "indulgent", "rich", "classic", "smooth texture", "decadent"]},
    {"genre": "A meal of Risotto", "keywords": ["arborio rice", "parmesan", "creamy", "Italian dish", "buttery", "rich flavor", "slow-cooked", "comfort food", "savory", "gourmet"]},    
    {"genre": "Times Early Dawn", "keywords": ["soft light", "hazy horizon", "pale blue sky", "faint glow", "quiet atmosphere", "gentle shadows", "calm air", "dew-covered surfaces", "subtle gradients", "peaceful beginnings"]},
    {"genre": "Times Sunrise", "keywords": ["golden light", "warm hues", "low sun", "elongated shadows", "pink and orange tones", "fresh atmosphere", "awakening world", "dramatic silhouettes", "radiant glow", "tranquil beauty"]},
    {"genre": "Times Mid-Morning", "keywords": ["bright sunlight", "clear skies", "moderate warmth", "defined shadows", "vivid colors", "active environment", "energized mood", "glare from surfaces", "lively scenes", "crisp clarity"]},
    {"genre": "Times Late Morning", "keywords": ["strong sunlight", "intense brightness", "short shadows", "blue skies", "heightened activity", "reflective surfaces", "clear details", "energetic vibes", "daytime bustle", "vivid visuals"]},
    {"genre": "Times Noon", "keywords": ["overhead sun", "harsh light", "minimal shadows", "brightest time", "white highlights", "strong glare", "clear visibility", "maximum warmth", "flat lighting", "peak energy"]},
    {"genre": "Times Early Afternoon", "keywords": ["softening light", "angled sunlight", "longer shadows", "warmer tones", "subtle contrasts", "relaxed atmosphere", "gentle warmth", "natural highlights", "midday transitions", "inviting glow"]},
    {"genre": "Times Late Afternoon", "keywords": ["golden hour", "low sun", "rich colors", "dramatic shadows", "golden highlights", "soft contrasts", "calming atmosphere", "evening approaches", "orange and amber tones", "picturesque light"]},
    {"genre": "Times Sunset", "keywords": ["vivid hues", "red and orange tones", "low-angled light", "elongated shadows", "dramatic sky", "cooling air", "peaceful scenery", "colorful gradients", "reflective waters", "nostalgic vibes"]},
    {"genre": "Times Dusk", "keywords": ["fading light", "blue hour", "soft shadows", "subdued tones", "cool atmosphere", "twilight hues", "calming mood", "dimmed surroundings", "gentle transitions", "quiet serenity"]},
    {"genre": "Times Nightfall", "keywords": ["darkening sky", "silhouetted objects", "deep blues", "starry sky", "soft breezes", "evening quiet", "muted colors", "nocturnal sounds", "calm energy", "welcoming night"]},
    {"genre": "Times Early Night", "keywords": ["moonlit scenery", "cool air", "starlit sky", "low visibility", "quiet surroundings", "warm indoor lights", "shadows in the dark", "soft glows", "tranquil moments", "evening activities"]},
    {"genre": "Times Midnight", "keywords": ["darkest time", "bright stars", "coolest temperature", "silent ambiance", "deep shadows", "still surroundings", "mystical glow", "moon dominance", "quiet introspection", "peaceful solitude"]},
    {"genre": "Times Pre-Dawn", "keywords": ["deep blue tones", "faint light", "stillness", "whispering breezes", "sleeping world", "emerging hues", "cool atmosphere", "soft whispers of light", "anticipation of dawn", "delicate balance"]},
    {"genre": "Times Morning Golden Hour", "keywords": ["soft golden light", "rich contrasts", "warm tones", "low-angle sun", "elongated shadows", "early activity", "gentle highlights", "romantic atmosphere", "natural beauty", "inviting start"]},
    {"genre": "Times Afternoon Golden Hour", "keywords": ["intensified hues", "rich oranges", "low sun", "glowing landscapes", "ambient warmth", "peaceful vibes", "dramatic contrasts", "picturesque light", "enhanced textures", "end-of-day charm"]},
    {"genre": "Times Twilight", "keywords": ["fading colors", "indigo tones", "silent transitions", "subtle gradients", "dimmed glow", "emerging stars", "cool shadows", "whispering wind", "gentle shifts", "dreamy moments"]},
    {"genre": "Times Mid-Afternoon", "keywords": ["bright skies", "moderate heat", "vibrant colors", "clear visibility", "active energy", "soft breezes", "short shadows", "lively environment", "natural lighting", "daytime peak"]},
    {"genre": "Times Deep Night", "keywords": ["pitch black sky", "bright moonlight", "intense stillness", "faint nocturnal sounds", "dim glow", "hidden details", "mystical ambiance", "calm solitude", "shadowy landscapes", "dreamlike aura"]},
    {"genre": "Times City at Night", "keywords": ["urban lights", "neon glow", "streetlights", "active nightlife", "bright windows", "reflective surfaces", "bustling streets", "shimmering water", "dynamic scenes", "contrasted tones"]},
    {"genre": "Times Starlit Night", "keywords": ["bright constellations", "dark skies", "clear air", "tranquil atmosphere", "subtle highlights", "silhouetted landscapes", "cosmic beauty", "calming breeze", "infinite depth", "celestial charm"]},    
    {"genre": "Element Earth", "keywords": ["soil", "dirt", "clay", "mud", "terrain", "ground", "land", "fertile", "natural surface", "earthy texture"]},
    {"genre": "Element Water", "keywords": ["ocean", "river", "lake", "rain", "ice", "steam", "droplets", "waves", "hydration", "clear liquid"]},
    {"genre": "Element Fire", "keywords": ["flames", "embers", "smoke", "heat", "burning", "wildfire", "candlelight", "spark", "lava", "intensity"]},
    {"genre": "Element Air", "keywords": ["wind", "breeze", "oxygen", "gust", "whirlwind", "freshness", "movement", "pressure", "atmosphere", "invisible flow"]},
    {"genre": "Element Metal", "keywords": ["iron", "steel", "rust", "forge", "strength", "tools", "blades", "shiny surface", "industrial", "cold"]},
    {"genre": "Element Gold", "keywords": ["nugget", "bar", "jewelry", "treasure", "luxury", "shimmering", "yellow metal", "wealth", "soft metal", "coin"]},
    {"genre": "Element Silver", "keywords": ["ornament", "coin", "mirror", "bright", "pure metal", "jewelry", "reflective", "elegance", "conductive", "bar"]},
    {"genre": "Element Stone", "keywords": ["pebble", "rock", "granite", "marble", "boulder", "statue", "quarry", "hard surface", "natural building", "ancient"]},
    {"genre": "Element Wood", "keywords": ["log", "plank", "forest", "timber", "carving", "natural material", "oak", "pine", "grain", "sawdust"]},
    {"genre": "Element Sand", "keywords": ["desert", "beach", "grains", "dunes", "quartz", "silt", "wind-blown", "soft texture", "glass base", "tiny particles"]},
    {"genre": "Element Clay", "keywords": ["pottery", "bricks", "terracotta", "ceramics", "mud", "sculpting", "earthy", "moldable", "hardens", "red soil"]},
    {"genre": "Element Diamond", "keywords": ["gem", "jewel", "hardest mineral", "brilliance", "cut stone", "luxury", "clear crystal", "ring", "sparkling", "precious"]},
    {"genre": "Element Coal", "keywords": ["fossil fuel", "black rock", "energy source", "carbon", "combustion", "mining", "industrial", "raw material", "power generation", "briquette"]},
    {"genre": "Element Copper", "keywords": ["wiring", "coin", "bronze base", "reddish metal", "electrical", "ductile", "alloy", "corrosion-resistant", "heat conductor", "industrial"]},
    {"genre": "Element Salt", "keywords": ["sea salt", "rock salt", "crystals", "white", "seasoning", "preservative", "mineral", "granules", "essential", "harvesting"]},
    {"genre": "Element Quartz", "keywords": ["crystal", "semi-precious", "sand component", "clear stone", "watch component", "geodes", "jewelry", "hardness", "transparency", "mineral"]},
    {"genre": "Element Amber", "keywords": ["fossil resin", "yellow", "translucent", "jewelry", "ancient tree sap", "preserved", "ornamental", "organic gemstone", "warm glow", "historic"]},
    {"genre": "Element Ice", "keywords": ["frozen water", "glacier", "crystals", "snow", "cold", "transparent", "slippery", "frost", "iceberg", "sparkling"]},
    {"genre": "Element Lava", "keywords": ["molten rock", "volcano", "hot", "flowing", "fire", "igneous rock", "eruptive", "cooling", "red-orange", "destructive"]},
    {"genre": "Element Basalt", "keywords": ["volcanic rock", "igneous", "dark gray", "dense", "columns", "lava origin", "hard", "construction", "ancient formations", "natural"]},
    {"genre": "Element Granite", "keywords": ["countertop", "strong", "speckled", "hard rock", "igneous", "quarry", "durable", "monuments", "architectural", "earthy"]},
    {"genre": "Element Obsidian", "keywords": ["volcanic glass", "black", "sharp edges", "hard", "shiny", "cutting tools", "ornamental", "smooth", "cooling lava", "precise"]},
    {"genre": "Element Sulfur", "keywords": ["yellow mineral", "volcanic", "brittle", "smell", "medicine", "gunpowder", "crystals", "natural deposits", "essential element", "industrial"]},
    {"genre": "Element Emerald", "keywords": ["green gemstone", "precious", "jewelry", "clarity", "luxury", "hardness", "brilliance", "cut stone", "mined", "rare"]},
    {"genre": "Element Ruby", "keywords": ["red gemstone", "precious", "jewelry", "luxury", "hardness", "passion", "brilliance", "cut stone", "fiery", "rare"]},
    {"genre": "Element Platinum", "keywords": ["noble metal", "precious", "jewelry", "industrial", "silver-white", "luxury", "corrosion-resistant", "dense", "rare", "investment"]},
    {"genre": "Element Aluminum", "keywords": ["lightweight", "silver metal", "foil", "cans", "conductive", "industrial", "flexible", "alloy", "corrosion-resistant", "modern"]},
    {"genre": "Element Tin", "keywords": ["alloy", "soft metal", "cans", "bronze base", "corrosion-resistant", "soldering", "industrial", "historical", "silver appearance", "versatile"]},
    {"genre": "Element Nickel", "keywords": ["magnetic", "alloy", "coinage", "corrosion-resistant", "industrial", "shiny", "strong", "conductive", "heat-resistant", "metallic"]},
    {"genre": "Element Zinc", "keywords": ["galvanizing", "alloy", "corrosion-resistant", "blueish-white metal", "industrial", "brass base", "medicine", "essential element", "ductile", "versatile"]},    
    {"genre": "Ultra-Realistic", "keywords": ["high detail", "perfect lighting", "real-world textures", "precise shadows", "lifelike", "immersive", "authentic", "true-to-life", "natural tones", "photo-like quality"]},
    {"genre": "Hyper-Realistic", "keywords": ["exaggerated details", "amplified imperfections", "visible pores", "veins and skin texture", "dramatic lighting", "super clarity", "meticulous rendering", "striking visuals", "attention-grabbing", "beyond reality"]},
    {"genre": "Photo-Realistic", "keywords": ["photographic accuracy", "true-to-life colors", "precise reflections", "natural shadows", "camera-like rendering", "real-world simulation", "professional lighting", "smooth gradients", "authentic depth", "highly polished"]},
    {"genre": "Cinematic Realism", "keywords": ["film-like", "drama lighting", "dynamic framing", "color grading", "artistic depth", "story-driven visuals", "soft shadows", "lens effects", "moody tones", "narrative atmosphere"]},
    {"genre": "Digital Realism", "keywords": ["computer-generated", "CGI precision", "high-definition textures", "pixel-perfect", "seamless integration", "next-gen rendering", "realistic simulation", "detailed animation", "interactive realism", "virtual world"]},
    {"genre": "Macro Realism", "keywords": ["extreme close-up", "micro details", "texture-focused", "tiny objects", "minute imperfections", "high magnification", "intimate perspective", "sharp clarity", "enhanced small details", "true-to-scale"]},
    {"genre": "Stylized Realism", "keywords": ["artistic touch", "enhanced colors", "soft textures", "natural yet vibrant", "expressive shadows", "creative lighting", "semi-realistic", "aesthetic flair", "balanced realism", "personality-driven"]},
    {"genre": "Real-Time Rendering", "keywords": ["game engine", "interactive realism", "fast processing", "dynamic lighting", "seamless animations", "physics-driven", "realistic reactions", "live simulation", "efficient rendering", "modern graphics"]},
    {"genre": "Surreal Realism", "keywords": ["dreamlike", "elevated reality", "fantastical elements", "hyper clarity", "unusual scenarios", "rich textures", "ethereal lighting", "unexpected details", "imaginative visuals", "alternate reality"]},
    {"genre": "Natural Realism", "keywords": ["organic textures", "nature-inspired", "earth tones", "wildlife focus", "scenic beauty", "daylight effects", "environmental accuracy", "soft gradients", "natural shadows", "landscape realism"]},
    {"genre": "High Dynamic Range (HDR)", "keywords": ["enhanced contrast", "bright highlights", "deep shadows", "color vibrancy", "realistic depth", "full spectrum lighting", "cinematic quality", "crisp textures", "immersive tone mapping", "rich details"]},
    {"genre": "Scientific Realism", "keywords": ["accuracy-focused", "educational visuals", "high precision", "true proportions", "clear labels", "natural materials", "laboratory lighting", "factual rendering", "scientific clarity", "unembellished style"]},
    {"genre": "Emotional Realism", "keywords": ["expressive tones", "emotive lighting", "character-driven", "storytelling focus", "intimate framing", "soulful expressions", "human connection", "subtle textures", "evocative colors", "heartfelt atmosphere"]},
    {"genre": "Futuristic Realism", "keywords": ["advanced technology", "sci-fi inspired", "neon lighting", "ultra-modern textures", "virtual aesthetics", "cyberpunk elements", "clean surfaces", "futuristic cityscapes", "sleek design", "next-gen vibes"]},
    {"genre": "Vintage Realism", "keywords": ["historical accuracy", "retro textures", "sepia tones", "aged materials", "classic lighting", "nostalgic vibes", "period-specific", "antique details", "authentic patina", "timeless appeal"]},
    {"genre": "Dynamic Realism", "keywords": ["movement-focused", "action-packed", "motion blur", "realistic physics", "natural flow", "energy-driven visuals", "fluid dynamics", "spontaneous effects", "immersive action", "true-to-life dynamics"]},
    {"genre": "Abstract Realism", "keywords": ["conceptual elements", "realistic base", "artistic interpretation", "unusual colors", "creative lighting", "symbolic visuals", "semi-representational", "blended styles", "thought-provoking", "emotional depth"]},
    {"genre": "Architectural Realism", "keywords": ["building accuracy", "cityscapes", "structural details", "clean lines", "real-world proportions", "modern design", "true-to-scale", "realistic lighting", "construction materials", "authentic interiors"]},
    {"genre": "Atmospheric Realism", "keywords": ["mood-driven", "weather effects", "mist and fog", "light diffusion", "realistic skies", "ambient tones", "natural shadows", "immersive depth", "dynamic lighting", "textured atmosphere"]},
    {"genre": "Fantasy Realism", "keywords": ["magical realism", "mythical creatures", "enchanted landscapes", "glowing elements", "ethereal textures", "dreamlike quality", "vivid colors", "fairy-tale settings", "otherworldly light", "imaginative world"]},    
    {"genre": "Beverage Cola", "keywords": ["Coca-Cola", "Pepsi", "carbonated", "sweet", "dark color", "popular", "refreshing", "classic", "ice-cold", "global brand"]},
    {"genre": "Beverage Lemon-Lime Soda", "keywords": ["Sprite", "7-Up", "clear", "citrusy", "carbonated", "refreshing", "sweet", "lemon flavor", "cold drink", "light taste"]},
    {"genre": "Beverage Root Beer", "keywords": ["A&W", "Barq's", "creamy", "spiced", "carbonated", "classic flavor", "sweet", "vanilla hints", "American favorite", "nostalgic"]},
    {"genre": "Beverage Energy Drink", "keywords": ["Red Bull", "Monster", "high caffeine", "boost", "carbonated", "tangy", "sports drink", "stimulant", "popular", "active lifestyle"]},
    {"genre": "Beverage Juice", "keywords": ["Tropicana", "Minute Maid", "orange juice", "apple juice", "natural", "refreshing", "vitamin C", "sweet", "breakfast drink", "fruit-based"]},
    {"genre": "Beverage Iced Tea", "keywords": ["Lipton", "Arizona", "sweetened", "unsweetened", "lemon flavor", "refreshing", "bottled", "black tea", "cool drink", "relaxing"]},
    {"genre": "Beverage Beer", "keywords": ["Budweiser", "Heineken", "Corona", "lager", "pale ale", "bar drink", "alcoholic", "hoppy", "cold", "refreshing"]},
    {"genre": "Beverage Craft Beer", "keywords": ["IPA", "stout", "porter", "microbrewery", "unique flavors", "hoppy", "rich taste", "small batch", "specialty beer", "innovative"]},
    {"genre": "Beverage Wine", "keywords": ["Cabernet Sauvignon", "Chardonnay", "red wine", "white wine", "grapes", "aged", "rich flavor", "bottled", "alcoholic", "fine dining"]},
    {"genre": "Beverage Whiskey", "keywords": ["Jack Daniels", "Jameson", "bourbon", "scotch", "aged", "smoky", "barrel", "alcoholic", "strong", "classic spirit"]},
    {"genre": "Beverage Vodka", "keywords": ["Grey Goose", "Smirnoff", "clear spirit", "neutral taste", "cocktail base", "distilled", "alcoholic", "party drink", "smooth", "versatile"]},
    {"genre": "Beverage Rum", "keywords": ["Bacardi", "Captain Morgan", "dark rum", "spiced rum", "tropical", "cocktail base", "distilled", "sweet undertones", "alcoholic", "Caribbean"]},
    {"genre": "Beverage Gin", "keywords": ["Tanqueray", "Bombay Sapphire", "juniper flavor", "dry", "herbal", "cocktail base", "distilled", "alcoholic", "botanical", "classic spirit"]},
    {"genre": "Beverage Champagne", "keywords": ["Moët & Chandon", "Veuve Clicquot", "sparkling wine", "bubbly", "celebration", "luxury", "French origin", "golden color", "alcoholic", "refined"]},
    {"genre": "Beverage Sports Drink", "keywords": ["Gatorade", "Powerade", "electrolytes", "hydration", "sweetened", "bright colors", "energy boost", "athlete favorite", "non-carbonated", "refreshing"]},
    {"genre": "Beverage Milk", "keywords": ["dairy", "lactose-free", "whole milk", "skim milk", "nutritious", "creamy", "calcium", "white", "versatile", "natural"]},
    {"genre": "Beverage Flavored Milk", "keywords": ["chocolate milk", "strawberry milk", "sweet", "creamy", "bottled", "dairy", "children's favorite", "dessert-like", "nutritious", "cool drink"]},
    {"genre": "Beverage Coffee", "keywords": ["Starbucks", "espresso", "cappuccino", "latte", "hot drink", "caffeine", "aromatic", "bold flavor", "energizing", "morning staple"]},
    {"genre": "Beverage Tea", "keywords": ["green tea", "black tea", "herbal tea", "warm", "aromatic", "relaxing", "natural", "antioxidants", "steeped", "global beverage"]},
    {"genre": "Beverage Smoothie", "keywords": ["fruit blend", "yogurt base", "berries", "banana", "cold", "healthy", "sweet", "creamy texture", "nutrient-rich", "breakfast drink"]},
    {"genre": "Beverage Hot Chocolate", "keywords": ["cocoa", "creamy", "sweet", "hot drink", "comforting", "winter favorite", "marshmallows", "rich", "chocolatey", "dessert-like"]},
    {"genre": "Beverage Liqueur", "keywords": ["Baileys", "Kahlúa", "sweet spirit", "creamy", "dessert drink", "alcoholic", "coffee-based", "unique flavors", "cocktail ingredient", "smooth"]},
    {"genre": "Beverage Mocktail", "keywords": ["non-alcoholic", "fruit-based", "creative flavors", "decorative", "refreshing", "party drink", "bright colors", "sweet", "unique blends", "chilled"]},
    {"genre": "Beverage Mineral Water", "keywords": ["San Pellegrino", "Evian", "sparkling", "natural", "pure", "hydrating", "bottled", "cold", "premium", "refreshing"]},
    {"genre": "Beverage Coconut Water", "keywords": ["natural hydration", "sweet", "tropical", "healthy", "refreshing", "bottled", "low calorie", "electrolytes", "pure", "clear liquid"]},
    {"genre": "Beverage Beer Alternative", "keywords": ["hard seltzer", "White Claw", "low-calorie", "sparkling", "alcoholic", "fruity", "light taste", "popular", "party drink", "trendy"]},
    {"genre": "Beverage Kombucha", "keywords": ["fermented", "probiotic", "tea base", "slightly fizzy", "healthy", "natural", "tangy", "bottled", "nutritious", "alternative"]},
    {"genre": "Beverage Lemonade", "keywords": ["fresh", "citrusy", "sweetened", "cooling", "yellow", "homemade", "refreshing", "summer drink", "natural", "bottled"]},
    {"genre": "Beverage Herbal Infusion", "keywords": ["chamomile", "peppermint", "soothing", "non-caffeinated", "relaxing", "aromatic", "steeped", "warm", "natural", "medicinal"]},
    {"genre": "Beverage Frozen Drink", "keywords": ["Slurpee", "Icee", "sweet", "slushy", "colorful", "cold", "summer treat", "artificial flavors", "popular", "fun"]},
    {"genre": "Food Apple", "keywords": ["red", "green", "sweet", "crunchy", "juicy", "fiber-rich", "tree fruit", "healthy snack", "common fruit", "versatile"]},
    {"genre": "Food Banana", "keywords": ["yellow", "sweet", "soft", "peelable", "high potassium", "tropical fruit", "quick energy", "healthy", "easy to eat", "popular"]},
    {"genre": "Food Carrot", "keywords": ["orange", "crunchy", "root vegetable", "sweet", "fiber-rich", "high in beta-carotene", "versatile", "raw or cooked", "healthy snack", "earthy flavor"]},
    {"genre": "Food Strawberry", "keywords": ["red", "sweet", "juicy", "tiny seeds", "berry", "high in vitamin C", "popular in desserts", "fresh fruit", "fragrant", "heart-shaped"]},
    {"genre": "Food Tomato", "keywords": ["red", "juicy", "versatile", "fruit often treated as vegetable", "high in antioxidants", "salads", "sauces", "fresh or cooked", "round", "healthy"]},
    {"genre": "Food Potato", "keywords": ["brown skin", "starchy", "root vegetable", "versatile", "mashed", "fried", "baked", "high in carbs", "earthy flavor", "nutritious"]},
    {"genre": "Food Orange", "keywords": ["round", "orange color", "citrus fruit", "juicy", "sweet", "vitamin C-rich", "peelable", "aromatic", "popular juice", "healthy snack"]},
    {"genre": "Food Lettuce", "keywords": ["green", "leafy", "crunchy", "salads", "low calorie", "fresh", "versatile", "healthy", "mild flavor", "common vegetable"]},
    {"genre": "Food Grapes", "keywords": ["small", "juicy", "sweet", "green or red", "high in antioxidants", "vine fruit", "snackable", "seedless or seeded", "popular in wines", "versatile"]},
    {"genre": "Food Onion", "keywords": ["round", "pungent", "versatile", "white, yellow, or red", "strong aroma", "root vegetable", "flavorful", "raw or cooked", "healthy", "layers"]},
    {"genre": "Food Pineapple", "keywords": ["tropical", "sweet", "spiky skin", "juicy", "yellow inside", "aromatic", "high vitamin C", "unique flavor", "used in cooking", "refreshing"]},
    {"genre": "Food Bell Pepper", "keywords": ["green", "red", "yellow", "sweet or mild", "crunchy", "healthy", "salads", "stir-fries", "vitamin-rich", "colorful"]},
    {"genre": "Food Cucumber", "keywords": ["green", "watery", "crunchy", "refreshing", "low calorie", "hydrating", "salads", "versatile", "mild flavor", "cooling"]},
    {"genre": "Food Blueberry", "keywords": ["small", "round", "blue", "sweet", "juicy", "antioxidant-rich", "berry", "popular in baking", "healthy", "tart flavor"]},
    {"genre": "Food Eggplant", "keywords": ["purple skin", "soft", "spongy", "versatile", "cooking vegetable", "low calorie", "rich flavor", "healthy", "used in global cuisines", "unique"]},
    {"genre": "Food Mango", "keywords": ["tropical", "sweet", "juicy", "yellow-orange", "aromatic", "high in vitamin A", "stone fruit", "popular worldwide", "exotic flavor", "refreshing"]},
    {"genre": "Food Spinach", "keywords": ["green", "leafy", "soft", "nutritious", "iron-rich", "salads", "cooking greens", "mild flavor", "versatile", "healthy"]},
    {"genre": "Food Peach", "keywords": ["soft", "sweet", "juicy", "fuzzy skin", "yellow-orange", "stone fruit", "aromatic", "summer fruit", "healthy", "delicious"]},
    {"genre": "Food Zucchini", "keywords": ["green", "soft", "mild flavor", "summer squash", "versatile", "low calorie", "cooking vegetable", "healthy", "nutritious", "easy to grow"]},
    {"genre": "Food Cherry", "keywords": ["small", "red", "sweet or tart", "juicy", "stone fruit", "healthy", "snackable", "popular in desserts", "antioxidants", "fragrant"]},
    {"genre": "Food Watermelon", "keywords": ["large", "green rind", "red inside", "juicy", "sweet", "hydrating", "summer fruit", "refreshing", "low calorie", "healthy"]},
    {"genre": "Food Celery", "keywords": ["green", "crunchy", "low calorie", "fiber-rich", "hydrating", "healthy", "versatile", "snackable", "aromatic", "earthy flavor"]},
    {"genre": "Food Avocado", "keywords": ["green", "creamy", "nutritious", "healthy fats", "versatile", "mild flavor", "popular in guacamole", "rich texture", "unique fruit", "superfood"]},
    {"genre": "Food Kiwi", "keywords": ["small", "brown skin", "green inside", "tangy", "juicy", "fiber-rich", "tropical fruit", "unique texture", "vitamin-rich", "refreshing"]},
    {"genre": "Food Broccoli", "keywords": ["green", "crunchy", "nutritious", "fiber-rich", "florets", "healthy", "low calorie", "cooking vegetable", "earthy flavor", "versatile"]},
    {"genre": "Food Pear", "keywords": ["sweet", "juicy", "soft", "green or yellow", "unique texture", "healthy", "fiber-rich", "snackable", "autumn fruit", "aromatic"]},
    {"genre": "Food Beetroot", "keywords": ["purple-red", "earthy", "sweet", "root vegetable", "nutritious", "high in antioxidants", "healthy", "used in salads", "distinct flavor", "versatile"]},
    {"genre": "Food Raspberry", "keywords": ["small", "red", "sweet", "juicy", "berry", "high in fiber", "tangy", "healthy", "popular in desserts", "fragrant"]},
    {"genre": "Food Lime", "keywords": ["small", "green", "citrus", "tangy", "juicy", "aromatic", "used in drinks", "refreshing", "healthy", "popular in cooking"]},
    {"genre": "Food Pumpkin", "keywords": ["large", "orange", "sweet", "fiber-rich", "used in desserts", "versatile", "healthy", "earthy flavor", "fall season", "cooking vegetable"]},    
    {"genre": "Realistic Full Scene", "keywords": ["realism", "natural colors", "high detail", "wide frame", "landscape", "immersive", "real-world textures", "true-to-life", "natural lighting", "everyday scenes"]},
    {"genre": "Realistic Close-Up", "keywords": ["high detail", "shallow depth of field", "macro photography", "intense focus", "fine textures", "natural lighting", "real-world objects", "human expressions", "hyper-realism", "immersive"]},
    {"genre": "Half-Body Close-Up", "keywords": ["upper body", "realistic lighting", "facial expressions", "emotional focus", "intimate framing", "torso details", "natural posture", "human-focused", "documentary style", "real-life moments"]},
    {"genre": "Close-Up of Hands", "keywords": ["realistic details", "hand movements", "gestures", "skin textures", "fingers", "natural pose", "crafting actions", "emotional symbolism", "tight framing", "fine detail"]},
    {"genre": "Close-Up of Eyes", "keywords": ["intense focus", "realism", "emotive gaze", "natural reflection", "iris details", "skin texture", "tight framing", "captivating", "emotional depth", "human realism"]},
    {"genre": "Close-Up from Ground to Sky", "keywords": ["low-angle view", "realism", "perspective shift", "natural lighting", "wide lens", "earth textures", "towering objects", "dramatic sky", "immersive", "ground-up framing"]},
    {"genre": "Close-Up from Sky to Ground", "keywords": ["bird's-eye view", "aerial realism", "natural landscape", "top-down perspective", "immersive details", "textures from above", "sky contrast", "dynamic framing", "realistic lighting", "depth"]},
    {"genre": "Close-Up of Feet", "keywords": ["realistic textures", "ground interaction", "shoes or bare feet", "walking actions", "ground-level perspective", "motion-focused", "natural lighting", "tight framing", "earthy details", "movement"]},
    {"genre": "Close-Up of Hair", "keywords": ["realistic textures", "strand detail", "flowing motion", "wind effects", "natural lighting", "tight framing", "color gradients", "shimmer", "human-focused", "dynamic movement"]},
    {"genre": "Close-Up of Lips", "keywords": ["realistic detail", "expressions", "natural gloss", "human focus", "texture precision", "emotional emphasis", "natural lighting", "intimate framing", "mouth movements", "authenticity"]},
    {"genre": "Close-Up of Objects", "keywords": ["realism", "macro detail", "fine textures", "natural lighting", "small scale", "isolated subject", "product photography", "intense focus", "minimal background", "immersive"]},
    {"genre": "Over-the-Shoulder Close-Up", "keywords": ["realism", "character-focused", "partial framing", "contextual perspective", "human interactions", "narrative framing", "natural lighting", "intimate feel", "storytelling", "immersive"]},
    {"genre": "Close-Up of Nature", "keywords": ["realism", "macro photography", "plants", "leaves", "flowers", "natural textures", "tiny creatures", "fine details", "natural light", "immersive"]},
    {"genre": "Dynamic Perspective Close-Up", "keywords": ["tilted frame", "motion emphasis", "action capture", "realistic lighting", "tight framing", "natural textures", "immersive feel", "cinematic realism", "creative angles", "intensity"]},
    {"genre": "Close-Up of Food", "keywords": ["realism", "texture details", "natural lighting", "vivid colors", "delicious focus", "macro photography", "appetizing", "tight framing", "cultural foods", "fresh"]},
    {"genre": "Close-Up of Tools", "keywords": ["realism", "work in action", "fine details", "industrial textures", "natural lighting", "tight framing", "machinery focus", "hands-on motion", "craftsmanship", "authentic"]},
    {"genre": "Close-Up of the Sky", "keywords": ["realism", "cloud textures", "color gradients", "natural lighting", "sunset or sunrise", "starry sky", "tight framing", "heavenly details", "dynamic skies", "weather-focused"]},
    {"genre": "Close-Up of Textures", "keywords": ["realism", "natural materials", "wood grain", "stone patterns", "fabric weave", "detailed focus", "macro photography", "lighting effects", "earthy tones", "immersive realism"]},
    {"genre": "Close-Up of Shadows", "keywords": ["realism", "light play", "contrasts", "ambient textures", "mood setting", "natural lighting", "tight framing", "mystery", "perspective emphasis", "dim environments"]},
    {"genre": "Close-Up of a Person Running", "keywords": ["realistic motion", "dynamic angles", "muscle tension", "natural lighting", "action emphasis", "tight framing", "movement blur", "athletic focus", "sweat details", "energy"]},
    {"genre": "Close-Up of Tears", "keywords": ["realism", "emotional depth", "skin texture", "glistening effects", "human-focused", "natural lighting", "tight framing", "pain", "vulnerability", "emotion"]},
    {"genre": "Close-Up of Reflections", "keywords": ["realism", "mirrors", "water", "glass surfaces", "natural distortions", "lighting effects", "fine textures", "tight framing", "artistic perspectives", "real-life details"]},
    {"genre": "Close-Up of Flames", "keywords": ["realism", "fire textures", "glowing light", "intense heat", "dynamic motion", "tight framing", "natural lighting", "drama", "warmth", "elemental focus"]},
    {"genre": "Close-Up of Water Droplets", "keywords": ["macro photography", "realism", "natural lighting", "fine textures", "dynamic drops", "reflective surfaces", "tight framing", "freshness", "nature", "clarity"]},
    {"genre": "Close-Up of Animal Eyes", "keywords": ["realism", "wildlife focus", "natural details", "macro photography", "intense gaze", "tight framing", "unique textures", "emotion", "animal-specific", "authenticity"]},
    {"genre": "Close-Up of a Hug", "keywords": ["realism", "emotional connection", "human touch", "tight framing", "expressive hands", "warmth", "intimacy", "natural lighting", "detailed focus", "authenticity"]},
    {"genre": "Close-Up of a Laugh", "keywords": ["realism", "natural expressions", "teeth details", "emotional depth", "tight framing", "joy", "genuine reaction", "facial textures", "human-focused", "liveliness"]},
    {"genre": "Close-Up of Wind Effects", "keywords": ["realism", "natural motion", "flowing hair", "moving leaves", "tight framing", "dynamic feel", "airy elements", "lighting emphasis", "action shot", "nature-driven"]},
    {"genre": "Close-Up of Tools in Action", "keywords": ["realism", "industrial focus", "motion blur", "crafting", "tight framing", "fine detail", "practical work", "authenticity", "manual actions", "natural lighting"]},    
    {"genre": "Cat Persian", "keywords": ["long-haired", "calm", "affectionate", "independent", "gentle", "round face", "quiet", "luxurious coat", "indoor cat", "laid-back"]},
    {"genre": "Cat Siamese", "keywords": ["short-haired", "vocal", "social", "intelligent", "loyal", "blue eyes", "playful", "sleek", "affectionate", "active"]},
    {"genre": "Cat Maine Coon", "keywords": ["large size", "friendly", "long-haired", "gentle giant", "playful", "intelligent", "social", "family cat", "loyal", "outgoing"]},
    {"genre": "Cat Ragdoll", "keywords": ["floppy", "affectionate", "calm", "blue eyes", "long-haired", "gentle", "quiet", "family cat", "social", "indoor"]},
    {"genre": "Cat Bengal", "keywords": ["exotic appearance", "spotted coat", "active", "intelligent", "playful", "energetic", "social", "sleek", "adventurous", "loyal"]},
    {"genre": "Cat British Shorthair", "keywords": ["round face", "plush coat", "calm", "independent", "affectionate", "gentle", "quiet", "family cat", "low-maintenance", "loyal"]},
    {"genre": "Cat Russian Blue", "keywords": ["short-haired", "silvery coat", "green eyes", "affectionate", "quiet", "intelligent", "loyal", "indoor cat", "reserved", "elegant"]},
    {"genre": "Cat Scottish Fold", "keywords": ["folded ears", "round face", "affectionate", "playful", "quiet", "calm", "social", "family cat", "loyal", "unique appearance"]},
    {"genre": "Cat Sphynx", "keywords": ["hairless", "warm skin", "active", "affectionate", "intelligent", "playful", "social", "unique", "friendly", "loyal"]},
    {"genre": "Cat Abyssinian", "keywords": ["short-haired", "active", "playful", "intelligent", "social", "sleek", "adventurous", "loyal", "curious", "affectionate"]},
    {"genre": "Cat Birman", "keywords": ["long-haired", "blue eyes", "calm", "affectionate", "social", "gentle", "family cat", "playful", "loyal", "elegant"]},
    {"genre": "Cat Oriental Shorthair", "keywords": ["sleek", "vocal", "intelligent", "playful", "social", "affectionate", "active", "loyal", "unique appearance", "expressive"]},
    {"genre": "Cat Devon Rex", "keywords": ["short-haired", "curly coat", "playful", "affectionate", "social", "intelligent", "active", "loyal", "unique", "energetic"]},
    {"genre": "Cat American Shorthair", "keywords": ["short-haired", "friendly", "playful", "adaptable", "social", "family cat", "intelligent", "loyal", "calm", "affectionate"]},
    {"genre": "Cat Norwegian Forest Cat", "keywords": ["long-haired", "thick coat", "gentle", "affectionate", "social", "family cat", "playful", "independent", "loyal", "outgoing"]},
    {"genre": "Cat Exotic Shorthair", "keywords": ["short-haired", "round face", "quiet", "affectionate", "social", "gentle", "indoor cat", "calm", "loyal", "plush coat"]},
    {"genre": "Cat Balinese", "keywords": ["long-haired", "vocal", "playful", "social", "intelligent", "affectionate", "sleek", "active", "loyal", "friendly"]},
    {"genre": "Cat Savannah", "keywords": ["exotic appearance", "spotted coat", "active", "adventurous", "intelligent", "social", "playful", "loyal", "unique", "energetic"]},
    {"genre": "Cat Tonkinese", "keywords": ["short-haired", "vocal", "affectionate", "playful", "social", "intelligent", "active", "loyal", "friendly", "sleek"]},
    {"genre": "Cat Cornish Rex", "keywords": ["short-haired", "curly coat", "sleek", "active", "affectionate", "social", "intelligent", "loyal", "playful", "energetic"]},
    {"genre": "Cat Manx", "keywords": ["short-haired", "tailless", "playful", "social", "loyal", "intelligent", "affectionate", "gentle", "family cat", "unique"]},
    {"genre": "Cat Burmese", "keywords": ["short-haired", "affectionate", "intelligent", "social", "playful", "family cat", "active", "loyal", "sleek", "friendly"]},
    {"genre": "Cat Chartreux", "keywords": ["short-haired", "blue-gray coat", "affectionate", "quiet", "loyal", "social", "calm", "family cat", "gentle", "reserved"]},
    {"genre": "Cat Ragamuffin", "keywords": ["long-haired", "friendly", "playful", "gentle", "social", "family cat", "affectionate", "loyal", "calm", "charming"]},
    {"genre": "Cat Egyptian Mau", "keywords": ["spotted coat", "short-haired", "active", "loyal", "playful", "intelligent", "social", "elegant", "fast runner", "unique"]},
    {"genre": "Cat Himalayan", "keywords": ["long-haired", "blue eyes", "calm", "affectionate", "quiet", "gentle", "family cat", "playful", "loyal", "indoor"]},
    {"genre": "Cat Korat", "keywords": ["short-haired", "silvery coat", "intelligent", "affectionate", "social", "loyal", "active", "family cat", "quiet", "gentle"]},
    {"genre": "Cat Japanese Bobtail", "keywords": ["short tail", "active", "playful", "intelligent", "social", "affectionate", "loyal", "sleek", "unique", "friendly"]},
    {"genre": "Cat Selkirk Rex", "keywords": ["curly coat", "affectionate", "social", "gentle", "family cat", "loyal", "playful", "calm", "unique", "plush"]},
    {"genre": "Cat Turkish Angora", "keywords": ["long-haired", "elegant", "playful", "social", "intelligent", "active", "loyal", "affectionate", "friendly", "graceful"]},    
    {"genre": "Dog Golden Retriever", "keywords": ["friendly", "intelligent", "family dog", "loyal", "playful", "golden coat", "obedient", "active", "trainable", "gentle"]},
    {"genre": "Dog German Shepherd", "keywords": ["protective", "intelligent", "loyal", "working dog", "strong", "police dog", "obedient", "alert", "brave", "versatile"]},
    {"genre": "Dog Bulldog", "keywords": ["stocky", "wrinkled face", "friendly", "calm", "loyal", "short muzzle", "adaptable", "strong-willed", "gentle", "companion"]},
    {"genre": "Dog Poodle", "keywords": ["intelligent", "elegant", "curly coat", "trainable", "energetic", "family dog", "active", "obedient", "adaptable", "loyal"]},
    {"genre": "Dog Beagle", "keywords": ["small hound", "curious", "friendly", "playful", "loyal", "scent hound", "energetic", "short-haired", "family dog", "social"]},
    {"genre": "Dog Labrador Retriever", "keywords": ["friendly", "intelligent", "loyal", "family dog", "playful", "active", "versatile", "trainable", "gentle", "adaptable"]},
    {"genre": "Dog Chihuahua", "keywords": ["small size", "lively", "alert", "loyal", "playful", "companion dog", "bold", "short or long coat", "energetic", "devoted"]},
    {"genre": "Dog Dachshund", "keywords": ["long body", "short legs", "playful", "energetic", "loyal", "curious", "scent hound", "small size", "companion", "alert"]},
    {"genre": "Dog Siberian Husky", "keywords": ["thick coat", "blue eyes", "energetic", "loyal", "sled dog", "friendly", "strong", "pack-oriented", "independent", "active"]},
    {"genre": "Dog Boxer", "keywords": ["muscular", "protective", "friendly", "energetic", "family dog", "loyal", "playful", "alert", "obedient", "brave"]},
    {"genre": "Dog Rottweiler", "keywords": ["strong", "protective", "loyal", "intelligent", "brave", "alert", "working dog", "muscular", "guard dog", "calm"]},
    {"genre": "Dog Shih Tzu", "keywords": ["small", "long coat", "friendly", "playful", "companion dog", "affectionate", "loyal", "adaptable", "charming", "gentle"]},
    {"genre": "Dog Yorkshire Terrier", "keywords": ["small", "long silky coat", "lively", "affectionate", "loyal", "intelligent", "playful", "companion dog", "curious", "bold"]},
    {"genre": "Dog Border Collie", "keywords": ["intelligent", "energetic", "loyal", "herding dog", "trainable", "agile", "alert", "friendly", "active", "obedient"]},
    {"genre": "Dog Great Dane", "keywords": ["large size", "gentle giant", "friendly", "loyal", "calm", "short coat", "elegant", "protective", "companion dog", "majestic"]},
    {"genre": "Dog Dalmatian", "keywords": ["spotted coat", "energetic", "playful", "friendly", "loyal", "alert", "trainable", "unique appearance", "active", "companion dog"]},
    {"genre": "Dog Cocker Spaniel", "keywords": ["friendly", "affectionate", "loyal", "playful", "intelligent", "family dog", "obedient", "medium coat", "social", "energetic"]},
    {"genre": "Dog French Bulldog", "keywords": ["small size", "bat-like ears", "loyal", "playful", "friendly", "short coat", "compact", "affectionate", "calm", "adaptable"]},
    {"genre": "Dog Australian Shepherd", "keywords": ["herding dog", "intelligent", "energetic", "loyal", "trainable", "active", "medium coat", "alert", "friendly", "versatile"]},
    {"genre": "Dog Pug", "keywords": ["small size", "wrinkled face", "friendly", "playful", "loyal", "short coat", "affectionate", "companion dog", "energetic", "adaptable"]},
    {"genre": "Dog Mastiff", "keywords": ["large size", "protective", "loyal", "gentle giant", "calm", "muscular", "alert", "guard dog", "family dog", "devoted"]},
    {"genre": "Dog Akita", "keywords": ["large size", "loyal", "intelligent", "protective", "brave", "strong", "alert", "dignified", "reserved", "calm"]},
    {"genre": "Dog Greyhound", "keywords": ["sleek", "fast runner", "friendly", "calm", "loyal", "short coat", "affectionate", "playful", "companion dog", "graceful"]},
    {"genre": "Dog Samoyed", "keywords": ["thick white coat", "friendly", "loyal", "playful", "energetic", "sled dog", "gentle", "affectionate", "family dog", "social"]},
    {"genre": "Dog Basset Hound", "keywords": ["long ears", "short legs", "loyal", "friendly", "scent hound", "calm", "playful", "gentle", "companion dog", "distinctive"]},
    {"genre": "Dog Chow Chow", "keywords": ["thick coat", "lion-like appearance", "loyal", "independent", "dignified", "protective", "calm", "alert", "unique", "reserved"]},
    {"genre": "Dog Doberman Pinscher", "keywords": ["protective", "intelligent", "loyal", "alert", "strong", "muscular", "brave", "obedient", "working dog", "elegant"]},
    {"genre": "Dog Collie", "keywords": ["loyal", "intelligent", "gentle", "herding dog", "family dog", "trainable", "medium coat", "affectionate", "friendly", "obedient"]},
    {"genre": "Dog Corgi", "keywords": ["short legs", "playful", "energetic", "loyal", "intelligent", "herding dog", "friendly", "trainable", "social", "cute"]},
    {"genre": "Dog Husky Mix", "keywords": ["mixed breed", "energetic", "loyal", "friendly", "thick coat", "active", "playful", "adaptive", "strong", "unique"]},    
    {"genre": "Bird Bald Eagle", "keywords": ["majestic", "national symbol", "powerful talons", "soaring", "bird of prey", "sharp beak", "white head", "brown feathers", "strong vision", "North America"]},
    {"genre": "Bird Peacock", "keywords": ["colorful", "long tail feathers", "iridescent", "courtship display", "elegant", "ornamental", "South Asia", "beautiful plumage", "vivid colors", "iconic"]},
    {"genre": "Bird Penguin", "keywords": ["flightless", "aquatic", "black and white", "waddling", "Antarctica", "ice habitat", "group behavior", "cute", "diving", "social"]},
    {"genre": "Bird Ostrich", "keywords": ["largest bird", "flightless", "fast runner", "long legs", "Africa", "powerful kicks", "plains dweller", "tough", "desert", "iconic"]},
    {"genre": "Bird Hummingbird", "keywords": ["tiny", "hovering", "fast wings", "nectar feeding", "vibrant colors", "agile", "tropical", "unique", "smallest bird", "rapid motion"]},
    {"genre": "Bird Flamingo", "keywords": ["pink feathers", "long legs", "wading bird", "shallow water", "social", "tropical", "iconic posture", "graceful", "filter feeder", "elegant"]},
    {"genre": "Bird Albatross", "keywords": ["large wingspan", "oceanic", "gliding", "long-distance flyer", "seabird", "white and gray feathers", "endurance", "isolated habitats", "majestic", "marine"]},
    {"genre": "Bird Parrot", "keywords": ["bright colors", "talking ability", "tropical", "intelligent", "social", "exotic", "beak strength", "feathered tail", "colorful", "adaptive"]},
    {"genre": "Bird Robin", "keywords": ["small songbird", "red breast", "spring symbol", "common", "garden dweller", "cheerful", "migratory", "agile", "familiar", "iconic"]},
    {"genre": "Bird Raven", "keywords": ["large black bird", "intelligent", "scavenger", "mythical", "ominous", "harsh calls", "adaptive", "symbolic", "trickster", "observant"]},
    {"genre": "Bird Swan", "keywords": ["elegant", "white feathers", "long neck", "graceful", "waterbird", "calm waters", "iconic pair bonding", "majestic", "poetic", "iconic"]},
    {"genre": "Bird Woodpecker", "keywords": ["tree drumming", "sharp beak", "forest", "insect eater", "vivid colors", "hole drilling", "strong neck", "distinctive sound", "agile", "iconic"]},
    {"genre": "Bird Owl", "keywords": ["nocturnal", "large eyes", "silent flight", "predator", "mysterious", "wise", "forest habitats", "sharp talons", "adaptive", "mythological"]},
    {"genre": "Bird Pelican", "keywords": ["large beak", "pouch for fish", "coastal", "group behavior", "aquatic", "graceful flyer", "white and gray feathers", "social", "iconic", "marine"]},
    {"genre": "Bird Toucan", "keywords": ["large colorful beak", "tropical", "fruit eater", "forest dweller", "vivid feathers", "playful", "South America", "distinctive appearance", "iconic", "jungle bird"]},
    {"genre": "Bird Seagull", "keywords": ["coastal bird", "scavenger", "white and gray", "adaptive", "group behavior", "marine", "iconic sound", "common", "beach habitats", "swift flyer"]},
    {"genre": "Bird Kingfisher", "keywords": ["bright colors", "stream dweller", "sharp beak", "fish catcher", "fast flyer", "small", "tropical and temperate", "perching", "iconic", "agile"]},
    {"genre": "Bird Canary", "keywords": ["small songbird", "vivid yellow", "domesticated", "cheerful", "caged bird", "melodic", "popular pet", "iconic", "adaptive", "social"]},
    {"genre": "Bird Hawk", "keywords": ["bird of prey", "sharp talons", "fast flyer", "keen vision", "solitary", "forest and plains", "carnivore", "majestic", "predatory", "dominant"]},
    {"genre": "Bird Crow", "keywords": ["black feathers", "intelligent", "scavenger", "adaptive", "group behavior", "common", "sharp calls", "mythical associations", "curious", "observant"]},
    {"genre": "Bird Macaw", "keywords": ["large parrot", "vivid colors", "tropical", "intelligent", "long tail feathers", "exotic", "social", "South America", "playful", "iconic"]},
    {"genre": "Bird Pigeon", "keywords": ["urban bird", "adaptive", "gray feathers", "city dweller", "common", "messenger bird", "group behavior", "iconic", "social", "resilient"]},
    {"genre": "Bird Kiwi", "keywords": ["flightless", "small", "nocturnal", "New Zealand", "iconic", "long beak", "brown feathers", "endangered", "unique", "adaptive"]},
    {"genre": "Bird Heron", "keywords": ["wading bird", "long legs", "wetlands", "sharp beak", "fishing", "graceful", "iconic posture", "calm waters", "majestic", "iconic"]},
    {"genre": "Bird Cardinal", "keywords": ["red feathers", "small songbird", "vivid", "North America", "melodic", "garden bird", "territorial", "common", "cheerful", "iconic"]},
    {"genre": "Bird Blue Jay", "keywords": ["blue feathers", "intelligent", "forest bird", "melodic calls", "bold", "North America", "adaptive", "social", "playful", "iconic"]},
    {"genre": "Bird Condor", "keywords": ["large wingspan", "scavenger", "endangered", "majestic", "mountain habitats", "rare", "iconic", "powerful", "adaptive", "soaring"]},
    {"genre": "Bird Sandpiper", "keywords": ["wading bird", "small size", "coastal habitats", "swift", "group behavior", "iconic", "beach runner", "marine", "agile", "adaptive"]},
    {"genre": "Bird Dove", "keywords": ["white feathers", "peace symbol", "small bird", "gentle", "melodic", "group behavior", "calm", "iconic", "adaptable", "social"]},
    {"genre": "Bird Eagle Owl", "keywords": ["large owl", "nocturnal predator", "majestic", "sharp talons", "wide wingspan", "forest habitats", "adaptive", "dominant", "intelligent", "fearsome"]},    
    {"genre": "Dinosaur Tyrannosaurus Rex", "keywords": ["apex predator", "large carnivore", "powerful bite", "short arms", "bipedal", "fearsome", "Cretaceous period", "scavenger", "dominant", "iconic dinosaur"]},
    {"genre": "Dinosaur Triceratops", "keywords": ["herbivore", "three horns", "frilled head", "quadrupedal", "herd behavior", "defensive", "Cretaceous period", "shielded", "iconic", "plant-eater"]},
    {"genre": "Dinosaur Velociraptor", "keywords": ["small predator", "feathered", "fast", "intelligent", "pack hunter", "agile", "Cretaceous period", "sickle-shaped claws", "stealthy", "deadly"]},
    {"genre": "Dinosaur Stegosaurus", "keywords": ["herbivore", "spiked tail", "plated back", "slow-moving", "quadrupedal", "defensive", "Jurassic period", "plant-eater", "armored", "prehistoric"]},
    {"genre": "Dinosaur Brachiosaurus", "keywords": ["long neck", "herbivore", "massive size", "quadrupedal", "high-reaching", "Jurassic period", "peaceful", "plant-eater", "grazing", "majestic"]},
    {"genre": "Dinosaur Spinosaurus", "keywords": ["large carnivore", "sail back", "semi-aquatic", "bipedal and quadrupedal", "fisher", "Cretaceous period", "intimidating", "powerful", "prehistoric", "iconic predator"]},
    {"genre": "Dinosaur Ankylosaurus", "keywords": ["herbivore", "armored body", "clubbed tail", "defensive", "quadrupedal", "Cretaceous period", "plant-eater", "resilient", "prehistoric tank", "iconic"]},
    {"genre": "Dinosaur Allosaurus", "keywords": ["large predator", "sharp teeth", "bipedal", "aggressive", "Jurassic period", "apex hunter", "dominant", "prehistoric predator", "fearsome", "swift"]},
    {"genre": "Dinosaur Pteranodon", "keywords": ["flying reptile", "large wingspan", "beak", "fish eater", "Cretaceous period", "aerial predator", "prehistoric flyer", "gliding", "swift", "iconic"]},
    {"genre": "Dinosaur Parasaurolophus", "keywords": ["herbivore", "crested head", "bipedal and quadrupedal", "Cretaceous period", "plant-eater", "resonating calls", "herd behavior", "peaceful", "prehistoric", "iconic"]},
    {"genre": "Dinosaur Diplodocus", "keywords": ["long neck", "herbivore", "massive size", "quadrupedal", "whip-like tail", "Jurassic period", "peaceful", "plant-eater", "grazing", "prehistoric giant"]},
    {"genre": "Dinosaur Iguanodon", "keywords": ["herbivore", "thumb spike", "bipedal and quadrupedal", "Cretaceous period", "plant-eater", "herd behavior", "prehistoric", "iconic", "adaptive", "social"]},
    {"genre": "Dinosaur Carnotaurus", "keywords": ["carnivore", "short horns", "bipedal", "fast runner", "Cretaceous period", "predator", "agile", "fearsome", "prehistoric hunter", "swift"]},
    {"genre": "Dinosaur Pachycephalosaurus", "keywords": ["herbivore", "dome-shaped skull", "bipedal", "head-butting", "defensive", "Cretaceous period", "plant-eater", "prehistoric", "armored", "unique"]},
    {"genre": "Dinosaur Ceratosaurus", "keywords": ["medium predator", "bipedal", "horned snout", "Jurassic period", "carnivore", "prehistoric predator", "swift", "aggressive", "fearsome", "adaptable"]},
    {"genre": "Dinosaur Gallimimus", "keywords": ["omnivore", "ostrich-like", "bipedal", "fast runner", "Cretaceous period", "swift", "agile", "prehistoric", "social", "iconic"]},
    {"genre": "Dinosaur Compsognathus", "keywords": ["small predator", "bipedal", "fast", "Cretaceous period", "carnivore", "prehistoric hunter", "agile", "swift", "tiny", "adaptable"]},
    {"genre": "Dinosaur Therizinosaurus", "keywords": ["herbivore", "long claws", "bipedal", "Cretaceous period", "plant-eater", "unique", "prehistoric", "iconic", "giant claws", "unusual"]},
    {"genre": "Dinosaur Maiasaura", "keywords": ["herbivore", "caring parent", "bipedal and quadrupedal", "Cretaceous period", "plant-eater", "herd behavior", "peaceful", "prehistoric", "iconic", "social"]},
    {"genre": "Dinosaur Oviraptor", "keywords": ["omnivore", "bipedal", "egg thief", "Cretaceous period", "prehistoric", "small predator", "agile", "swift", "unique", "adaptive"]},
    {"genre": "Dinosaur Styracosaurus", "keywords": ["herbivore", "horned frill", "quadrupedal", "Cretaceous period", "plant-eater", "defensive", "prehistoric", "iconic", "social", "armored"]},
    {"genre": "Dinosaur Albertosaurus", "keywords": ["carnivore", "bipedal", "smaller relative of T. rex", "Cretaceous period", "prehistoric predator", "swift", "aggressive", "apex hunter", "fearsome", "dominant"]},
    {"genre": "Dinosaur Archaeopteryx", "keywords": ["feathered", "small", "bipedal", "transitional species", "Jurassic period", "prehistoric bird", "flying", "agile", "iconic", "unique"]},
    {"genre": "Dinosaur Protoceratops", "keywords": ["herbivore", "frilled head", "quadrupedal", "Cretaceous period", "plant-eater", "prehistoric", "social", "defensive", "small ceratopsian", "iconic"]},
    {"genre": "Dinosaur Deinonychus", "keywords": ["carnivore", "bipedal", "sharp claws", "pack hunter", "Cretaceous period", "prehistoric predator", "agile", "swift", "deadly", "adaptive"]},
    {"genre": "Dinosaur Megalosaurus", "keywords": ["carnivore", "bipedal", "sharp teeth", "Jurassic period", "prehistoric predator", "fearsome", "dominant", "powerful", "iconic", "adaptive"]},
    {"genre": "Dinosaur Giganotosaurus", "keywords": ["large predator", "carnivore", "bipedal", "Cretaceous period", "prehistoric predator", "fearsome", "dominant", "powerful", "giant", "iconic"]},
    {"genre": "Dinosaur Cryolophosaurus", "keywords": ["carnivore", "bipedal", "crested skull", "Jurassic period", "prehistoric predator", "fearsome", "unique", "adaptive", "swift", "iconic"]},
    {"genre": "Dinosaur Eoraptor", "keywords": ["small carnivore", "bipedal", "early dinosaur", "Triassic period", "prehistoric", "swift", "agile", "adaptive", "early predator", "unique"]},
    {"genre": "Dinosaur Muttaburrasaurus", "keywords": ["herbivore", "crested nose", "quadrupedal", "Cretaceous period", "plant-eater", "prehistoric", "unique", "adaptive", "peaceful", "iconic"]},    
    {"genre": "Hero Superman", "keywords": ["super strength", "flight", "invulnerability", "heat vision", "super speed", "x-ray vision", "cold breath", "super hearing", "Kryptonian", "Justice League"]},
    {"genre": "Hero Batman", "keywords": ["peak human condition", "genius intellect", "martial arts", "stealth", "gadgets", "wealth", "detective", "dark knight", "vigilante", "Justice League"]},
    {"genre": "Hero Wonder Woman", "keywords": ["super strength", "flight", "combat skills", "indestructible bracelets", "Lasso of Truth", "Amazonian", "immortality", "warrior", "Justice League", "goddess"]},
    {"genre": "Hero Spider-Man", "keywords": ["wall-crawling", "spider sense", "super agility", "web-shooting", "spider strength", "acrobatic", "smart", "scientist", "New York", "friendly neighborhood"]},
    {"genre": "Hero Iron Man", "keywords": ["powered armor", "genius intellect", "flight", "repulsor rays", "multi-tool suit", "wealth", "billionaire", "technology", "Avengers", "philanthropist"]},
    {"genre": "Hero Captain America", "keywords": ["super strength", "enhanced agility", "indestructible shield", "tactical genius", "leader", "war hero", "enhanced senses", "super soldier serum", "Avengers", "patriot"]},
    {"genre": "Hero Thor", "keywords": ["god of thunder", "storm breaker", "Mjolnir", "super strength", "immortality", "flight", "lightning", "godly powers", "Asgardian", "Avengers"]},
    {"genre": "Hero The Flash", "keywords": ["super speed", "time travel", "vibrating through walls", "accelerated healing", "lightning speed", "metahuman", "multiverse", "Central City", "speed force", "Justice League"]},
    {"genre": "Hero Green Lantern", "keywords": ["power ring", "energy constructs", "flight", "force field", "willpower", "intergalactic", "Green Lantern Corps", "space", "symbol of hope", "Justice League"]},
    {"genre": "Hero Hulk", "keywords": ["super strength", "incredible durability", "rage transformation", "healing factor", "brute force", "green skin", "giant", "smash", "gamma radiation", "Avengers"]},
    {"genre": "Hero Black Panther", "keywords": ["super strength", "enhanced senses", "vibranium suit", "martial arts", "stealth", "agility", "super intelligence", "King of Wakanda", "Avengers", "technological genius"]},
    {"genre": "Hero Deadpool", "keywords": ["regenerative healing factor", "expert marksman", "swords", "indestructibility", "tactical genius", "humor", "mercenary", "anti-hero", "X-Force", "fourth wall breaking"]},
    {"genre": "Hero Doctor Strange", "keywords": ["magic", "astral projection", "dimensional travel", "teleportation", "shielding spells", "master of the mystic arts", "sorcerer supreme", "healing", "incantations", "Avengers"]},
    {"genre": "Hero Ant-Man", "keywords": ["size-shifting", "super strength", "intelligent scientist", "control over ants", "Pym particles", "shrinking", "super agility", "quantum realm", "Avengers", "invisibility"]},
    {"genre": "Hero Aquaman", "keywords": ["super strength", "aquatic telepathy", "underwater combat", "swimming", "Atlantean physiology", "trident", "King of Atlantis", "sea creature control", "Justice League", "atlantean"]},
    {"genre": "Hero Wolverine", "keywords": ["regenerative healing", "adamantium claws", "super senses", "enhanced strength", "martial arts", "longevity", "immortal", "X-Men", "berserker rage", "survival"]},
    {"genre": "Hero Black Widow", "keywords": ["martial arts", "expert marksman", "espionage", "super intelligence", "infiltration", "assassination", "peak human condition", "agility", "Avengers", "spy"]},
    {"genre": "Hero Scarlet Witch", "keywords": ["reality warping", "telekinesis", "telepathy", "chaos magic", "hex powers", "super strength", "flight", "magic", "mutant", "Avengers"]},
    {"genre": "Hero Silver Surfer", "keywords": ["cosmic energy", "super strength", "flight", "energy manipulation", "immortality", "surfboard", "galaxy explorer", "space travel", "Herald of Galactus", "cosmic awareness"]},
    {"genre": "Hero Daredevil", "keywords": ["super senses", "blindness", "peak human condition", "martial arts", "agility", "urban vigilante", "lawyer", "daredevil senses", "Hell's Kitchen", "street-level hero"]},
    {"genre": "Hero Punisher", "keywords": ["expert marksman", "military training", "weapon proficiency", "tactical genius", "brutal", "vigilante", "combat", "psychological warfare", "anti-hero", "assassination"]},
    {"genre": "Hero Hawkeye", "keywords": ["archery", "marksmanship", "combat skills", "tactical genius", "billion-dollar bow", "strategist", "Avengers", "weaponry", "agility", "sharp aim"]},
    {"genre": "Hero Shazam", "keywords": ["magic", "super strength", "flight", "lightning bolts", "wisdom of Solomon", "strength of Hercules", "speed of Mercury", "courage of Achilles", "bravery", "Justice League"]},
    {"genre": "Hero Rogue", "keywords": ["power absorption", "super strength", "flight", "invulnerability", "absorb memories", "mutant", "tactile touch", "X-Men", "super agility", "draining powers"]},
    {"genre": "Hero Vision", "keywords": ["synthetic intelligence", "super strength", "flight", "energy beams", "phasing", "mind stone", "android", "Avengers", "super intellect", "energy manipulation"]},
    {"genre": "Hero Gambit", "keywords": ["kinetic energy", "card manipulation", "expert thief", "martial arts", "charm", "New Orleans", "mutant", "explosions", "X-Men", "charismatic"]},
    {"genre": "Hero Storm", "keywords": ["weather manipulation", "flight", "lightning control", "super strength", "African goddess", "mutant", "X-Men", "agility", "storm clouds", "thunderstorms"]},
    {"genre": "Hero Professor X", "keywords": ["telepathy", "mind control", "mental defense", "strategist", "leader of X-Men", "genius intellect", "mutant", "founder", "telepathic link", "X-Men"]},
    {"genre": "Hero Magneto", "keywords": ["magnetism", "metal manipulation", "super strength", "flight", "force field", "X-Men", "villain", "master of magnetism", "mutant", "powerful"]},
    {"genre": "Hero Beast", "keywords": ["super strength", "enhanced agility", "super intelligence", "healing factor", "beast-like appearance", "X-Men", "scientist", "brilliant mind", "mutant", "combat skills"]},
    {"genre": "Hero Cyclops", "keywords": ["optic blasts", "super strength", "combat strategist", "leader of X-Men", "mutant", "energy beams", "intellect", "sharp aim", "X-Men", "tactical genius"]},
    {"genre": "Hero Jean Grey", "keywords": ["telepathy", "telekinesis", "Phoenix Force", "super strength", "mutant", "X-Men", "leader", "psychic powers", "energy blasts", "Phoenix"]},
    {"genre": "Hero The Thing", "keywords": ["super strength", "rock-like skin", "invulnerability", "brawler", "mutant", "heroic", "X-Men", "team player", "Ben Grimm", "monster-like appearance"]},
    {"genre": "Hero Luke Cage", "keywords": ["super strength", "invulnerability", "unbreakable skin", "brawler", "street-level hero", "Hell's Kitchen", "Power Man", "bulletproof", "vigilante", "crime fighter"]},     
    {"genre": "Villain Joker", "keywords": ["insanity", "manipulation", "gadgets", "crime mastermind", "psychopath", "master of chaos", "Batman's enemy", "anarchy", "trickster", "Clown Prince of Crime"]},
    {"genre": "Villain Lex Luthor", "keywords": ["genius intellect", "wealth", "super intelligence", "strategist", "billionaire", "ruthless", "power-hungry", "Kryptonite", "arch-nemesis of Superman", "business magnate"]},
    {"genre": "Villain Thanos", "keywords": ["super strength", "cosmic power", "infinity gauntlet", "genocide", "immortality", "cosmic awareness", "alien", "space conqueror", "Infinity Stones", "Avengers"]},
    {"genre": "Villain Magneto", "keywords": ["magnetism", "metal manipulation", "super strength", "flight", "force field", "X-Men's enemy", "villain", "master of magnetism", "mutant", "powerful"]},
    {"genre": "Villain Green Goblin", "keywords": ["super strength", "goblin glider", "explosives", "madness", "genius intellect", "gadgets", "web-slinger enemy", "crazed", "villain", "Spider-Man's arch-nemesis"]},
    {"genre": "Villain Doctor Doom", "keywords": ["genius intellect", "power armor", "magic", "latverian dictator", "super intelligence", "devious", "mastermind", "enemy of the Fantastic Four", "sorcery", "villain"]},
    {"genre": "Villain Venom", "keywords": ["symbiote", "super strength", "shapeshifting", "web-slinging", "agility", "heightened senses", "anti-hero", "Spider-Man's enemy", "venomous", "alien parasite"]},
    {"genre": "Villain Ra's al Ghul", "keywords": ["immortality", "genius intellect", "martial arts", "Lazarus Pit", "eco-terrorist", "League of Assassins", "world domination", "Batman enemy", "strategist", "global threat"]},
    {"genre": "Villain Two-Face", "keywords": ["split personality", "coin flips", "criminal mastermind", "obsession with duality", "high-risk criminal", "Batman foe", "obsessive", "deformed face", "trickster", "villain"]},
    {"genre": "Villain Red Skull", "keywords": ["super soldier serum", "hate", "Nazi", "cosmic cube", "leader of Hydra", "hate for Captain America", "world domination", "warrior", "villain", "vile"]},
    {"genre": "Villain Catwoman", "keywords": ["acrobatic", "master thief", "high agility", "cat-like reflexes", "burglar", "romantic tension with Batman", "anti-hero", "expert martial artist", "stealth", "diamond thief"]},
    {"genre": "Villain Ultron", "keywords": ["artificial intelligence", "robotic", "global domination", "machine army", "destroy humanity", "genius intellect", "technology", "villain", "infinity stones", "Avengers foe"]},
    {"genre": "Villain Kingpin", "keywords": ["criminal empire", "super strength", "mastermind", "New York", "ruthless", "mafia boss", "gangster", "organized crime", "villain", "Daredevil's enemy"]},
    {"genre": "Villain Bane", "keywords": ["super strength", "intelligence", "Venom drug", "leader of the League of Shadows", "brutal", "strategist", "Batman foe", "physically imposing", "powerful", "terrorist"]},
    {"genre": "Villain Hela", "keywords": ["goddess of death", "super strength", "immortality", "weapon manipulation", "necromancy", "godly powers", "Asgardian", "Throne of Asgard", "villain", "Thor's enemy"]},
    {"genre": "Villain Deathstroke", "keywords": ["super strength", "martial arts", "healing factor", "expert marksman", "assassin", "tactical genius", "hired gun", "swordsmanship", "villain", "DC's top mercenary"]},
    {"genre": "Villain Loki", "keywords": ["god of mischief", "magic", "shape-shifting", "illusion", "teleportation", "devious", "godly powers", "Thor's brother", "villain", "trickster"]},
    {"genre": "Villain The Riddler", "keywords": ["intellect", "puzzles", "obsession with riddles", "criminal mastermind", "ego", "obsessive", "Batman enemy", "problem-solving", "obsessive-compulsive", "criminal genius"]},
    {"genre": "Villain Sinestro", "keywords": ["fear", "green lantern enemy", "yellow lantern ring", "energy manipulation", "super strength", "cosmic villain", "green lantern corps", "space conqueror", "warrior", "justice bent"]},
    {"genre": "Villain Darkseid", "keywords": ["cosmic power", "godly strength", "Omega beams", "Apokolips", "multiverse conqueror", "villain", "god of tyranny", "universal domination", "immortal", "Justice League enemy"]},
    {"genre": "Villain Mysterio", "keywords": ["illusion", "trickery", "master of deception", "special effects", "expert tactician", "criminal mastermind", "Spider-Man's enemy", "smoke and mirrors", "gadgetry", "villain"]},
    {"genre": "Villain Shredder", "keywords": ["martial arts", "ninja skills", "tactical genius", "leader of the Foot Clan", "villain", "ninja armor", "swords", "enemy of the Teenage Mutant Ninja Turtles", "domination", "ruthless"]},
    {"genre": "Villain Thanos", "keywords": ["super strength", "cosmic power", "infinity gauntlet", "genocide", "immortality", "cosmic awareness", "alien", "space conqueror", "Infinity Stones", "Avengers"]},
    {"genre": "Villain Poison Ivy", "keywords": ["plant manipulation", "toxins", "chlorokinesis", "environmentalist", "super strength", "pollen control", "villain", "eco-terrorist", "poisonous", "greenery"]},
    {"genre": "Villain Venom", "keywords": ["symbiote", "super strength", "shapeshifting", "web-slinging", "agility", "heightened senses", "anti-hero", "Spider-Man's enemy", "venomous", "alien parasite"]},
    {"genre": "Villain Bizarro", "keywords": ["inverse powers", "super strength", "flight", "heat vision", "super speed", "Superman's opposite", "alien", "unstable", "distorted mind", "villain"]},
    {"genre": "Villain Mr. Freeze", "keywords": ["cryogenic freezing", "ice manipulation", "cold powers", "intellect", "scientist", "ruthless", "Batman enemy", "freeze ray", "villain", "frozen emotions"]},
    {"genre": "Villain Hush", "keywords": ["criminal mastermind", "intellect", "mysterious", "former friend of Bruce Wayne", "Batman enemy", "operating in shadows", "personal vendetta", "conspiracy", "stealth", "villain"]},
    {"genre": "Villain Zod", "keywords": ["Kryptonian", "super strength", "heat vision", "super speed", "invulnerability", "soldier", "enemy of Superman", "warrior", "leader", "alien"]},
    {"genre": "Villain Harley Quinn", "keywords": ["insanity", "expert in hand-to-hand combat", "martial arts", "gadgets", "jester", "Joker's partner", "villain", "psychologist turned villain", "love-driven", "chaos"]},    
    {"genre": "Sign or poster with text Warning", "keywords": ["danger", "caution", "beware", "hazard", "watch out", "alert", "stop", "proceed with care", "attention", "risk"]},
    {"genre": "Sign or poster with text Exit", "keywords": ["exit", "emergency exit", "to the left", "to the right", "way out", "escape", "fire exit", "out", "door", "vacate"]},
    {"genre": "Sign or poster with text Restricted Area", "keywords": ["authorized personnel only", "do not enter", "access denied", "private property", "security clearance", "no trespassing", "keep out", "dangerous zone", "security", "area under surveillance"]},
    {"genre": "Sign or poster with text Roadwork", "keywords": ["construction zone", "detour", "road closed", "work in progress", "use alternate route", "bumpy road", "heavy machinery", "slow down", "maintenance", "road repairs"]},
    {"genre": "Sign or poster with text Help Wanted", "keywords": ["now hiring", "join our team", "apply within", "job opening", "career opportunity", "employment", "work with us", "vacancy", "immediate opening", "full-time position"]},
    {"genre": "Sign or poster with text For Sale", "keywords": ["available now", "sale", "offer", "discount", "clearance", "limited time", "bargain", "special offer", "new product", "just released"]},
    {"genre": "Sign or poster with text Lost", "keywords": ["missing", "lost pet", "reward", "have you seen me?", "contact us", "urgent", "found something?", "return to owner", "help us find", "poster"]},
    {"genre": "Sign or poster with text Sale", "keywords": ["huge discount", "clearance sale", "buy one get one", "special offer", "end of season", "limited time", "price drop", "massive discount", "shop now", "low prices"]},
    {"genre": "Sign or poster with text No Parking", "keywords": ["no parking", "tow away zone", "keep clear", "illegal parking", "reserved", "parking restriction", "tow truck", "no stopping", "forbidden", "enforced"]},
    {"genre": "Sign or poster with text Public Service Announcement", "keywords": ["please listen", "attention all", "important notice", "message from the government", "health warning", "urgent", "announcement", "breaking news", "do not ignore", "immediate action required"]},
    {"genre": "Sign or poster with text Smoking Area", "keywords": ["designated smoking area", "no smoking beyond this point", "smoking allowed", "smoking zone", "non-smoking", "smoke-free", "restricted smoking", "cigarette area", "vaping allowed", "tobacco use"]},
    {"genre": "Sign or poster with text Keep Out", "keywords": ["private property", "do not enter", "no entry", "dangerous zone", "restricted access", "keep away", "off-limits", "keep out", "entry forbidden", "no trespassing"]},
    {"genre": "Sign or poster with text Fresh Produce", "keywords": ["fresh", "locally grown", "organic", "ripe", "healthy", "vegan", "green", "seasonal", "from farm to table", "freshly picked"]},
    {"genre": "Sign or poster with text Emergency", "keywords": ["emergency", "911", "urgent", "help needed", "first aid", "critical", "immediate response", "danger", "rescue", "accident"]},
    {"genre": "Sign or poster with text Not Allowed", "keywords": ["no entry", "prohibited", "ban", "don't touch", "stop", "restrictions", "disallowed", "forbidden", "unpermitted", "denied access"]},
    {"genre": "Sign or poster with text Welcome", "keywords": ["welcome", "glad to have you", "enjoy your stay", "happy to serve", "greetings", "you're here", "come in", "let us assist you", "hello", "cheerful greeting"]},
    {"genre": "Sign or poster with text Danger", "keywords": ["high risk", "dangerous", "do not approach", "explosive", "high voltage", "chemical hazard", "poison", "sharp", "toxic", "fire hazard"]},
    {"genre": "Sign or poster with text Caution Wet Floor", "keywords": ["slippery", "wet floor", "caution", "be careful", "hazard", "slippery surface", "warning", "fall risk", "stay alert", "floor cleaning"]},
    {"genre": "Sign or poster with text Open", "keywords": ["open for business", "come in", "we're open", "ready to serve", "open daily", "hours of operation", "now open", "join us", "welcome in", "shopping hours"]},
    {"genre": "Sign or poster with text Closed", "keywords": ["closed for the day", "out of service", "vacation", "no entry", "business hours over", "temporary closure", "no access", "service unavailable", "back soon", "closed until further notice"]},
    {"genre": "Sign or poster with text No Smoking", "keywords": ["smoking prohibited", "no tobacco", "smoke-free zone", "non-smoking", "health safety", "avoid smoking", "no lighting cigarettes", "vaping restricted", "health warning", "clean air zone"]},
    {"genre": "Sign or poster with text Under Construction", "keywords": ["work in progress", "construction zone", "coming soon", "under renovation", "remodeling", "being built", "in development", "construction area", "please excuse the mess", "worksite"]},
    {"genre": "Sign or poster with text Bathroom", "keywords": ["restroom", "washroom", "toilet", "ladies", "gentlemen", "men's room", "women's room", "unisex", "public toilet", "facilities"]},
    {"genre": "Sign or poster with text Store Hours", "keywords": ["open hours", "business hours", "store timing", "available now", "shop hours", "working hours", "closed on weekends", "weekend hours", "holiday hours", "open late"]},
    {"genre": "Sign or poster with text Lost & Found", "keywords": ["found item", "lost property", "contact us", "claim your item", "returned item", "have you lost something?", "inquire inside", "missing items", "search", "reclaim your belongings"]},
    {"genre": "Sign or poster with text Warning Wet Paint", "keywords": ["fresh paint", "wet paint", "do not touch", "stay away", "painted surface", "caution", "wet surface", "still drying", "no contact", "fresh coat"]},
    {"genre": "Sign or poster with text Closed for Maintenance", "keywords": ["maintenance", "temporarily unavailable", "service downtime", "repair work", "under maintenance", "service interruption", "maintenance notice", "temporary closure", "please bear with us", "service restoration"]},
    {"genre": "Sign or poster with text Private", "keywords": ["private property", "no trespassing", "keep out", "employees only", "for authorized personnel", "restricted access", "confidential", "no entry", "private access", "exclusive"]},
    {"genre": "Sign or poster with text No Photography", "keywords": ["photography prohibited", "no cameras", "no recording", "no pictures", "forbidden", "no video", "image capture not allowed", "no phone cameras", "privacy policy", "disallowed"]},
    {"genre": "Sign or poster with text Do Not Disturb", "keywords": ["stay out", "not available", "private", "do not knock", "personal time", "resting", "quiet please", "meeting", "in session", "unavailable"]},    
    {"genre": "Sprite Bubble Text Surprise", "keywords": ["No way!", "Are you serious?", "What?!", "Nooo!", "Are you kidding me?", "I can't believe it!", "This can't be real!", "Shut up!", "You're joking, right?", "What the hell?"]},
    {"genre": "Sprite Bubble Text Angry", "keywords": ["That's it!", "I'm done!", "How dare you!", "You idiot!", "I can't stand this!", "You're asking for it!", "You're dead!", "I'm not finished yet!", "You better watch out!", "That's enough!"]},
    {"genre": "Sprite Bubble Text Happy", "keywords": ["Yay!", "Woo-hoo!", "Awesome!", "I'm so happy!", "This is great!", "I'm on cloud nine!", "I feel amazing!", "This is the best day ever!", "Let's go!", "I'm so excited!"]},
    {"genre": "Sprite Bubble Text Shy", "keywords": ["Um... hi?", "Please don't look at me!", "I'm not good at this...", "Don't mind me!", "I-I didn't say anything!", "E-Excuse me!", "Uhh, sorry...!", "Stop teasing me!", "I didn't mean to!", "P-Please don't do that!"]},
    {"genre": "Sprite Bubble Text Confused", "keywords": ["Huh?", "What do you mean?", "I don't get it...", "Are you lost?", "Wait, what?", "Is this a joke?", "I don't understand!", "What just happened?", "Confused much?", "Say what?"]},
    {"genre": "Sprite Bubble Text Embarrassed", "keywords": ["Don't look at me like that!", "I didn't do it!", "I-I'm not blushing!", "Why did you have to say that?", "You're making me embarrassed!", "Please don't tell anyone!", "I didn't mean for that to happen!", "Stop teasing me, please!", "I can't handle this!", "This is so awkward..."]},
    {"genre": "Sprite Bubble Text Sarcastic", "keywords": ["Oh, great...", "What a surprise...", "Just what I needed...", "Wow, you're so smart...", "I totally care about that...", "Like I haven't heard that before!", "Wow, you're so original...", "How clever of you...", "Really? You're a genius!", "That's just perfect!"]},
    {"genre": "Sprite Bubble Text Excited", "keywords": ["I can't wait!", "This is going to be amazing!", "I'm so pumped up!", "Let's do this!", "This is going to be epic!", "I can't stop smiling!", "I feel like I'm dreaming!", "I'm all in!", "This is going to be so much fun!", "I'm so ready!"]},
    {"genre": "Sprite Bubble Text Sad", "keywords": ["I can't do this anymore...", "It's over... I'm done...", "I don't know what to do...", "I'm sorry...", "I failed...", "I just can't go on...", "It's too much for me...", "I'm sorry, I let you down...", "I'm so lost...", "I feel so alone..."]},
    {"genre": "Sprite Bubble Text Determined", "keywords": ["I won't give up!", "This isn't over!", "I'm not backing down!", "I'll make it through!", "I will win!", "You can't stop me!", "Watch me do it!", "I can handle this!", "I'm going to finish this!", "This is just the beginning!"]},
    {"genre": "Sprite Bubble Text Flirty", "keywords": ["Hey there, cutie!", "You're looking great today!", "Stop making me blush!", "Don't make me fall for you...", "You're so charming!", "You know you like me!", "How about we go out sometime?", "You're making me smile...", "You think you're funny, huh?", "Do you always look this good?"]},
    {"genre": "Sprite Bubble Text Annoyed", "keywords": ["Leave me alone!", "Stop bothering me!", "Seriously?", "Enough already!", "I’m done with this!", "This is so annoying!", "Can you just stop?", "Why are you always like this?", "You never listen!", "Just quit it already!"]},
    {"genre": "Sprite Bubble Text Excuse Me", "keywords": ["Excuse me?", "Did you just say that?", "What did you just do?", "Hey, that’s not nice!", "I’m sorry, but what?", "Did I hear that correctly?", "Wait, what did you mean by that?", "Are you serious right now?", "I didn't quite catch that...", "Could you repeat that, please?"]},
    {"genre": "Sprite Bubble Text Tired", "keywords": ["I'm so tired...", "I need a nap...", "Can we stop already?", "I can't go on...", "I'm exhausted...", "I just need to rest...", "This is too much for me...", "I don't think I can handle this anymore...", "I can barely keep my eyes open...", "I'm too tired for this..."]},
    {"genre": "Sprite Bubble Text Shocked", "keywords": ["No way!", "You did what?!", "That's insane!", "This can't be true!", "You’re kidding, right?", "I don’t believe it!", "I’m in shock!", "This is unbelievable!", "How could this happen?", "I never saw that coming!"]},
    {"genre": "Sprite Bubble Text In Love", "keywords": ["I think I’m in love with you...", "You mean everything to me...", "I can't stop thinking about you...", "You're all I need...", "I love being with you...", "I can't imagine my life without you...", "You're my everything...", "I'm so happy we're together...", "I’m falling for you...", "I adore you..."]},
    {"genre": "Sprite Bubble Text Victory", "keywords": ["We did it!", "We won!", "That's how it's done!", "Victory is ours!", "We made it!", "We are the champions!", "Mission accomplished!", "I knew we could do it!", "Yes, we won!", "We are unstoppable!"]},
    {"genre": "Sprite Bubble Text Grateful", "keywords": ["Thank you so much!", "I really appreciate it!", "I'm so thankful!", "I couldn’t have done it without you!", "You're the best!", "I owe you one!", "You saved me!", "Thanks a ton!", "I’m forever grateful!", "You're amazing!"]},
    {"genre": "Sprite Bubble Text Cheerful", "keywords": ["I’m feeling great today!", "Everything is going my way!", "Let’s keep smiling!", "Life’s so good right now!", "Nothing can bring me down!", "I’m so happy today!", "I love this moment!", "Let’s enjoy the day!", "I’m on top of the world!", "This is awesome!"]},
    {"genre": "Sprite Bubble Text Dramatic", "keywords": ["This is the end!", "It’s all over now!", "I can't take it anymore!", "This is my fate!", "Why does this always happen to me?", "It’s too much to bear!", "I’ve had enough!", "I can’t go on like this!", "This is my last chance!", "Everything is falling apart!"]},
    {"genre": "Sprite Bubble Text Bored", "keywords": ["I’m so bored...", "This is so boring...", "Is this over yet?", "Can we hurry this up?", "I’m losing interest...", "I’ve seen enough...", "Ugh, this is dragging on...", "I’m totally checked out...", "This is so dull...", "I just want to go home..."]},
    {"genre": "Sprite Bubble Text Confident", "keywords": ["I’ve got this!", "No one can stop me!", "I’m ready for anything!", "I can do anything I set my mind to!", "I’m unstoppable!", "I’m on fire!", "Watch me succeed!", "I’m at my best right now!", "I’ve got this in the bag!", "You’ll see!" ]},
    {"genre": "Sprite Bubble Text Reassurance", "keywords": ["Don't worry, everything will be fine.", "Trust me, I've got this.", "It’s going to be okay.", "You’re going to be fine.", "Everything will work out in the end.", "You can do it!", "I’m here for you.", "We’ll get through this together.", "Stay calm, all will be well.", "Don’t give up!"]},    
    {"genre": "Drawing art", "keywords": ["sketching", "pencil", "charcoal", "line art", "shading", "realism", "detailed", "classical", "figure drawing", "manga"]},
    {"genre": "Anime art", "keywords": ["Japanese animation", "manga", "cartoons", "vivid colors", "character design", "action", "emotion", "digital art", "2D animation", "stylized"]},
    {"genre": "Painting art", "keywords": ["oil painting", "watercolor", "acrylic", "canvas", "impressionism", "realism", "abstract", "portrait", "still life", "landscape"]},
    {"genre": "Digital art", "keywords": ["digital painting", "photoshop", "graphic design", "3D modeling", "illustration", "vector art", "CGI", "concept art", "virtual art", "motion graphics"]},
    {"genre": "Street Art", "keywords": ["graffiti", "urban art", "spray paint", "public spaces", "mural", "political messages", "bold", "rebel", "large-scale", "installation"]},
    {"genre": "Surrealism art", "keywords": ["dream-like", "fantasy", "unreal", "psychedelic", "abstract", "unconscious", "symbolism", "bizarre", "imagination", "mysterious"]},
    {"genre": "Pop Art", "keywords": ["mass media", "bright colors", "commercial", "consumerism", "icons", "advertising", "collage", "comic strips", "repetition", "celebrity"]},
    {"genre": "Cubism art", "keywords": ["geometric shapes", "abstract", "multiple perspectives", "fragmentation", "reduction", "analytical", "synthetic", "modern", "avant-garde", "revolutionary"]},
    {"genre": "Impressionism art", "keywords": ["light", "color", "brush strokes", "outdoor scenes", "everyday life", "natural light", "momentary", "soft", "quick strokes", "blurred"]},
    {"genre": "Art Nouveau", "keywords": ["decorative arts", "elegant", "flowing lines", "nature-inspired", "organic", "ornamental", "glass", "metalwork", "architecture", "whiplash curves"]},    
    {"genre": "Times - Before Christ (BC)", "keywords": ["ancient history", "prehistoric", "early civilizations", "stone age", "bronze age", "iron age", "classical era", "ancient empires", "archaeology", "mythology"]},
    {"genre": "Times - During Christ's Life", "keywords": ["Roman Empire", "ancient Judea", "Christianity origins", "historical Jesus", "religion", "early disciples", "biblical events", "Middle East", "ancient culture", "spiritual awakening"]},
    {"genre": "Times - After Christ's Death (AD)", "keywords": ["Roman Empire", "early Christianity", "medieval period", "church influence", "religious expansion", "European history", "cultural shifts", "Middle Ages", "theological developments", "historical evolution"]},
    {"genre": "Times - Middle Ages", "keywords": ["feudalism", "castles", "knights", "Black Death", "crusades", "chivalry", "medieval society", "monasteries", "religious wars", "European history"]},
    {"genre": "Times - Renaissance", "keywords": ["rebirth", "art", "science", "invention", "humanism", "Da Vinci", "Michelangelo", "literature", "enlightenment", "cultural revolution"]},
    {"genre": "Times - Industrial Revolution", "keywords": ["steam power", "factories", "innovation", "mechanization", "urbanization", "economic growth", "technological advancements", "19th century", "industry", "modernization"]},
    {"genre": "Times - World War I", "keywords": ["global conflict", "trench warfare", "1914-1918", "alliances", "military history", "Versailles Treaty", "European powers", "industrialized warfare", "political shifts", "Great War"]},
    {"genre": "Times - Interwar Period", "keywords": ["1920s", "1930s", "economic depression", "cultural changes", "League of Nations", "totalitarian regimes", "global tensions", "modern art", "jazz age", "political unrest"]},
    {"genre": "Times - World War II", "keywords": ["global conflict", "Axis vs Allies", "1939-1945", "Holocaust", "D-Day", "atomic bomb", "military strategy", "genocide", "war crimes", "global impact"]},
    {"genre": "Times - Post-War Era", "keywords": ["Cold War", "1950s", "economic recovery", "space race", "nuclear age", "civil rights movements", "globalization", "social changes", "modernization", "UN establishment"]},
    {"genre": "Times - 1960s", "keywords": ["counterculture", "civil rights", "space exploration", "Vietnam War", "cultural revolution", "social activism", "rock and roll", "political movements", "technological growth", "global tension"]},
    {"genre": "Times - 1980s", "keywords": ["Cold War tension", "Reaganomics", "personal computers", "pop culture", "fall of Berlin Wall", "global markets", "media boom", "MTV", "technological rise", "economic shifts"]},
    {"genre": "Times - Modern Era (2000s)", "keywords": ["globalization", "internet revolution", "terrorism", "climate change", "smartphones", "social media", "space exploration", "economic challenges", "technology-driven society", "cultural shifts"]},
    {"genre": "Times - 2025", "keywords": ["current era", "sustainability", "technology advancements", "post-pandemic", "space travel", "AI growth", "climate action", "global cooperation", "economic recovery", "cultural evolution"]},
    {"genre": "Times - 2050s", "keywords": ["future society", "AI dominance", "space colonization", "sustainability breakthroughs", "climate solutions", "technological singularity", "globalization", "human evolution", "medical advancements", "global challenges"]},
    {"genre": "Times - 2100s", "keywords": ["next century", "global unity", "technological utopia", "space habitation", "climate stability", "extended lifespan", "AI integration", "post-human age", "advanced medicine", "interstellar exploration"]},
    {"genre": "Times - 2300s", "keywords": ["far future", "galactic expansion", "energy mastery", "cultural fusion", "new species interaction", "sustainable planets", "global peace", "AI-human coexistence", "quantum technology", "terraforming"]},
    {"genre": "Times - 2500s", "keywords": ["post-terrestrial era", "deep space exploration", "universal communication", "immortality research", "galactic governance", "universal culture", "resource abundance", "time travel experiments", "quantum AI", "intergalactic diplomacy"]},
    {"genre": "Times - 3000s", "keywords": ["future civilization", "advanced technology", "unified galaxy", "post-human evolution", "universal consciousness", "infinite energy", "quantum existence", "AI-guided societies", "interstellar travel", "unprecedented achievements"]},
    {"genre": "Times - Timeless Era", "keywords": ["eternity", "philosophical concepts", "spiritual transcendence", "mythical dimensions", "universal truths", "boundless possibilities", "existence continuum", "infinite universe", "cultural eternity", "universal legacy"]},    
    {"genre": "Acting of Punching", "keywords": ["strike", "fist", "forceful hit", "close combat", "boxing", "self-defense", "aggression", "uppercut", "jab", "physical attack"]},
    {"genre": "Acting of Kicking", "keywords": ["leg strike", "martial arts", "high kick", "roundhouse", "defense", "agility", "attack", "forceful blow", "front kick", "close combat"]},
    {"genre": "Acting of Pointing Gun", "keywords": ["aiming", "targeting", "weapon control", "threat", "intimidation", "precision", "firearm", "stance", "focus", "defensive positioning"]},
    {"genre": "Acting of Shooting Gun", "keywords": ["firearm discharge", "bullet", "target hit", "precision", "recoil", "self-defense", "offense", "tactical action", "lethal force", "long-range attack"]},
    {"genre": "Acting of Dodging", "keywords": ["evasion", "quick movement", "avoiding strike", "reflexes", "agility", "self-defense", "reaction time", "escape", "close combat maneuver", "defensive"]},
    {"genre": "Acting of Blocking", "keywords": ["defense", "shielding", "impact absorption", "hand-to-hand combat", "martial arts", "counter move", "forearm block", "stance", "protection", "physical barrier"]},
    {"genre": "Acting of Grappling", "keywords": ["wrestling", "close combat", "submission hold", "takedown", "control", "martial arts", "self-defense", "chokehold", "pinning", "ground fighting"]},
    {"genre": "Acting of Throwing", "keywords": ["projectile", "forceful motion", "combat maneuver", "weapon use", "quick action", "disarming", "tactical", "strength", "improvised weapon", "distance"]},
    {"genre": "Acting of Slashing", "keywords": ["bladed weapon", "sword combat", "quick motion", "close quarters", "self-defense", "cutting attack", "sharp blade", "lethal action", "precision", "knife combat"]},
    {"genre": "Acting of Stabbing", "keywords": ["knife attack", "direct motion", "penetrating blow", "close quarters", "lethal strike", "bladed weapon", "self-defense", "aggression", "precision", "sharp object"]},
    {"genre": "Acting of Esquive", "keywords": ["sidestepping", "avoiding attacks", "tactical movement", "reflexes", "close combat", "counter-strategy", "defense", "agility", "quick reaction", "dodging strikes"]},
    {"genre": "Acting of Crouching", "keywords": ["lowering body", "combat stance", "defense", "concealment", "dodging", "quick reaction", "balance", "close quarters", "movement preparation", "evasion"]},
    {"genre": "Acting of Lying on Ground", "keywords": ["prone position", "defensive posture", "combat evasion", "concealment", "ground fighting", "reaction", "self-defense", "tactical movement", "low profile", "survival"]},
    {"genre": "Acting of Elbow Strike", "keywords": ["close combat", "forceful blow", "martial arts", "self-defense", "sharp impact", "quick attack", "aggression", "short range", "upper body strike", "physical attack"]},
    {"genre": "Acting of Knee Strike", "keywords": ["close combat", "martial arts", "lower body strike", "quick impact", "self-defense", "aggression", "short range", "tactical maneuver", "body blow", "forceful attack"]},
    {"genre": "Acting of Disarming", "keywords": ["weapon removal", "tactical action", "self-defense", "close combat", "disabling attacker", "precision", "reflexes", "hand-to-hand combat", "martial arts", "weapon control"]},
    {"genre": "Acting of Parrying", "keywords": ["weapon deflection", "swordplay", "countering attack", "martial arts", "reflexes", "self-defense", "close combat", "bladed weapon", "quick reaction", "defensive maneuver"]},
    {"genre": "Acting of Spinning Kick", "keywords": ["martial arts", "high impact", "circular motion", "close combat", "self-defense", "agility", "attack", "target hit", "flashy move", "powerful blow"]},
    {"genre": "Acting of Choking", "keywords": ["submission hold", "self-defense", "close quarters", "lethal action", "martial arts", "grappling", "control", "aggression", "combat maneuver", "tactical"]},
    {"genre": "Acting of Weapon Reloading", "keywords": ["firearm action", "tactical maneuver", "preparation", "precision", "combat readiness", "self-defense", "ammunition", "quick action", "lethal force", "weapon control"]},    
    {"genre": "Acting of Singing", "keywords": ["vocal performance", "melody", "lyrics", "stage presence", "opera", "choir", "karaoke", "harmonizing", "concert", "musical expression"]},
    {"genre": "Acting of Dancing", "keywords": ["movement", "rhythm", "ballet", "hip-hop", "salsa", "freestyle", "performance", "choreography", "grace", "entertainment"]},
    {"genre": "Acting of Eating", "keywords": ["chewing", "food consumption", "mealtime", "appetite", "tasting", "snacking", "cuisine", "enjoyment", "dining", "nutrition"]},
    {"genre": "Acting of Walking", "keywords": ["strolling", "steps", "leisurely pace", "hiking", "movement", "outdoor", "foot travel", "exercise", "pathway", "relaxation"]},
    {"genre": "Acting of Running", "keywords": ["sprinting", "jogging", "exercise", "marathon", "speed", "endurance", "track", "training", "cardio", "outdoor"]},
    {"genre": "Acting of Swimming", "keywords": ["water movement", "freestyle", "backstroke", "diving", "laps", "pool", "ocean", "exercise", "aquatic", "recreation"]},
    {"genre": "Acting of Reading", "keywords": ["book", "literature", "novel", "study", "comprehension", "focus", "library", "quiet", "learning", "entertainment"]},
    {"genre": "Acting of Writing", "keywords": ["penmanship", "typing", "journaling", "storytelling", "notes", "creative", "literature", "essays", "imagination", "expression"]},
    {"genre": "Acting of Drawing", "keywords": ["sketching", "illustration", "pencil", "art", "creativity", "design", "doodling", "coloring", "portrait", "imagination"]},
    {"genre": "Acting of Painting", "keywords": ["canvas", "art", "colors", "brush", "oil painting", "abstract", "landscape", "creativity", "expression", "masterpiece"]},
    {"genre": "Acting of Cooking", "keywords": ["meal preparation", "ingredients", "recipe", "kitchen", "chef", "baking", "flavor", "dishes", "sauce", "culinary"]},
    {"genre": "Acting of Driving", "keywords": ["car", "road", "transport", "steering", "speed", "journey", "highway", "traffic", "navigation", "vehicle"]},
    {"genre": "Acting of Cycling", "keywords": ["bicycle", "pedaling", "exercise", "outdoor", "road", "speed", "trail", "helmet", "fitness", "adventure"]},
    {"genre": "Acting of Jumping", "keywords": ["leaping", "vertical motion", "exercise", "sports", "skipping", "bounding", "energy", "trampoline", "fun", "movement"]},
    {"genre": "Acting of Climbing", "keywords": ["mountain", "rock", "harness", "outdoor", "adventure", "strength", "exercise", "ascent", "altitude", "challenge"]},
    {"genre": "Acting of Listening", "keywords": ["music", "conversation", "audio", "focus", "understanding", "speech", "learning", "relaxation", "ears", "attention"]},
    {"genre": "Acting of Talking", "keywords": ["conversation", "speech", "communication", "interaction", "dialogue", "discussion", "expression", "language", "voice", "exchange"]},
    {"genre": "Acting of Meditating", "keywords": ["calm", "relaxation", "mindfulness", "yoga", "focus", "inner peace", "breathing", "spiritual", "awareness", "tranquility"]},
    {"genre": "Acting of Fishing", "keywords": ["outdoor", "rod", "bait", "lake", "catch", "hobby", "recreation", "water", "casting", "patience"]},
    {"genre": "Acting of Gardening", "keywords": ["plants", "soil", "watering", "seeds", "flowers", "vegetables", "outdoor", "nature", "growth", "cultivation"]},    
    {"genre": "World Wonder Great Pyramid of Giza", "keywords": ["ancient", "Egypt", "pyramid", "monument", "stone", "tomb", "Pharaoh", "landmark", "wonders of the world", "historical"]},
    {"genre": "World Wonder Hanging Gardens of Babylon", "keywords": ["ancient", "Babylon", "garden", "mesopotamia", "irrigation", "myth", "Hanging Gardens", "king", "historical", "legendary"]},
    {"genre": "World Wonder Statue of Zeus at Olympia", "keywords": ["Greece", "statue", "zeus", "Olympia", "ancient", "god", "temple", "mythology", "Greece", "historical"]},
    {"genre": "World Wonder Temple of Artemis at Ephesus", "keywords": ["ancient", "temple", "Artemis", "Greece", "Ephesus", "religious", "monument", "historical", "wonders of the world", "pagan"]},
    {"genre": "World Wonder Mausoleum at Halicarnassus", "keywords": ["tomb", "ancient", "Mausolus", "Greece", "historical", "royalty", "monument", "Halicarnassus", "mausoleum", "architecture"]},
    {"genre": "World Wonder Colossus of Rhodes", "keywords": ["statue", "ancient", "Rhodes", "Greek", "giant", "harbor", "symbol", "historical", "wonders of the world", "sculpture"]},
    {"genre": "World Wonder Lighthouse of Alexandria", "keywords": ["lighthouse", "ancient", "Alexandria", "Egypt", "maritime", "monument", "harbor", "historical", "wonders of the world", "navigation"]},
    {"genre": "World Wonder Great Wall of China", "keywords": ["China", "wall", "ancient", "fortification", "defense", "historical", "military", "landmark", "symbol", "longest wall"]},
    {"genre": "World Wonder Petra", "keywords": ["Jordan", "ancient", "city", "rock-cut", "architecture", "historical", "monuments", "lost city", "desert", "UNESCO World Heritage"]},
    {"genre": "World Wonder Christ the Redeemer", "keywords": ["Brazil", "statue", "Christ", "Rio de Janeiro", "monument", "Christianity", "historical", "iconic", "landmark", "religion"]},
    {"genre": "World Wonder Machu Picchu", "keywords": ["Peru", "Inca", "mountain", "ancient", "lost city", "historical", "temples", "architecture", "UNESCO World Heritage", "exploration"]},
    {"genre": "World Wonder Chichen Itza", "keywords": ["Mexico", "Mayan", "pyramid", "historical", "temple", "ancient", "ruins", "civilization", "Mesoamerican", "archaeological site"]},
    {"genre": "World Wonder Roman Colosseum", "keywords": ["Italy", "Rome", "amphitheater", "ancient", "arena", "gladiators", "historical", "Roman Empire", "landmark", "theater"]},
    {"genre": "World Wonder Taj Mahal", "keywords": ["India", "mausoleum", "love", "white marble", "monument", "historical", "Mughal architecture", "UNESCO World Heritage", "India", "romantic"]},
    {"genre": "World Wonder Colosseum of Rome", "keywords": ["Italy", "Rome", "amphitheater", "gladiators", "ancient", "historical", "Roman Empire", "arena", "tourist attraction", "landmark"]},
    {"genre": "World Wonder Eiffel Tower", "keywords": ["France", "Paris", "iron", "landmark", "architecture", "tourist attraction", "symbol", "modern", "France", "famous"]},
    {"genre": "World Wonder Sydney Opera House", "keywords": ["Australia", "Sydney", "architecture", "opera", "building", "modern", "famous", "landmark", "theater", "cultural"]},
    {"genre": "World Wonder Great Barrier Reef", "keywords": ["Australia", "coral reef", "marine", "ecosystem", "ocean", "nature", "UNESCO World Heritage", "diving", "tourism", "wildlife"]},
    {"genre": "World Wonder Stonehenge", "keywords": ["England", "monument", "stones", "mystery", "ancient", "circle", "historical", "prehistoric", "UNESCO World Heritage", "archaeology"]},
    {"genre": "World Wonder Mount Everest", "keywords": ["Nepal", "mountain", "highest peak", "climbing", "Himalayas", "nature", "world landmark", "adventure", "altitude", "geography"]},
    {"genre": "World Wonder Grand Canyon", "keywords": ["USA", "natural wonder", "canyon", "geography", "landmark", "Arizona", "nature", "landscape", "scenic", "tourism"]},
    {"genre": "World Wonder Yellowstone National Park", "keywords": ["USA", "geothermal", "nature", "park", "wildlife", "landscape", "nature reserve", "waterfalls", "geysers", "tourism"]},    
    {"genre": "Monster Vampire", "keywords": ["bloodsucker", "undead", "night", "immortal", "bite", "fangs", "transformation", "coffin", "mythology", "gothic"]},
    {"genre": "Monster Werewolf", "keywords": ["shapeshifter", "full moon", "lycanthropy", "beast", "howl", "night", "hunting", "supernatural", "curse", "furry"]},
    {"genre": "Monster Zombie", "keywords": ["undead", "reanimated", "flesh-eating", "apocalypse", "virus", "decay", "walking dead", "rotting", "shambling", "horde"]},
    {"genre": "Monster Ghost", "keywords": ["spirit", "haunted", "supernatural", "apparition", "poltergeist", "specter", "translucent", "paranormal", "unfinished business", "revenge"]},
    {"genre": "Monster Demon", "keywords": ["evil", "hell", "fire", "dark magic", "possession", "horns", "claws", "supernatural", "underworld", "sinister"]},
    {"genre": "Monster Dragon", "keywords": ["fire-breathing", "winged", "scaly", "fantasy", "mythology", "hoarding treasure", "immense", "legendary", "powerful", "ancient"]},
    {"genre": "Monster Frankenstein's Monster", "keywords": ["mad scientist", "reanimated", "unnatural", "patchwork", "bolts", "horror", "creation", "Victor Frankenstein", "monster", "clumsy"]},
    {"genre": "Monster Kraken", "keywords": ["sea monster", "tentacles", "myth", "ocean", "giant", "swallow ships", "legendary", "deep sea", "fear", "tremendous"]},
    {"genre": "Monster Chupacabra", "keywords": ["blood-sucking", "creature", "Latin America", "goat sucker", "night stalker", "alien-like", "vampire", "myth", "mysterious", "cryptid"]},
    {"genre": "Monster Bigfoot", "keywords": ["Sasquatch", "forest", "mysterious", "cryptid", "large footprints", "hairy", "legend", "North America", "elusive", "wild"]},
    {"genre": "Monster Mummy", "keywords": ["ancient Egypt", "curse", "wrapped in bandages", "undead", "resurrected", "tomb", "pharaoh", "sands", "spells", "mystery"]},
    {"genre": "Monster Yeti", "keywords": ["abominable snowman", "mountain", "snow", "cryptid", "large footprints", "hairy", "elusive", "mysterious", "Himalayas", "cold"]},
    {"genre": "Monster Vampire Bat", "keywords": ["flying", "bloodsucker", "night", "creature", "winged", "nocturnal", "bite", "vampire", "dangerous", "small"]},
    {"genre": "Monster Gorgon", "keywords": ["medusa", "snake hair", "stone gaze", "mythology", "Greek", "turn to stone", "horror", "monster", "legend", "ancient"]},
    {"genre": "Monster Chimera", "keywords": ["mythology", "Greek", "lion head", "serpent tail", "goat body", "fire-breathing", "monster", "creature", "hybrid", "dangerous"]},
    {"genre": "Monster Lich", "keywords": ["undead wizard", "necromancer", "immortal", "dark magic", "skeleton", "sorcery", "curse", "zombie army", "evil", "ancient"]},
    {"genre": "Monster Banshee", "keywords": ["female spirit", "wailing", "death omen", "Irish mythology", "ghost", "screeching", "haunting", "curse", "revenge", "legend"]},
    {"genre": "Monster Giant", "keywords": ["huge", "colossal", "strength", "mythology", "beast", "tall", "supernatural", "legendary", "mighty", "creature"]},
    {"genre": "Monster Hydra", "keywords": ["multi-headed", "Greek mythology", "immortal", "water serpent", "regeneration", "dangerous", "beast", "creature", "mythical", "slaying"]},
    {"genre": "Monster Manticore", "keywords": ["lion body", "human face", "scorpion tail", "dangerous", "mythical", "Persian mythology", "creature", "venomous", "beast", "legend"]},
    {"genre": "Monster Wendigo", "keywords": ["spirit", "cannibalism", "North American legend", "snow", "evil", "monster", "human-like", "flesh-eating", "cold", "supernatural"]},
    {"genre": "Monster Griffin", "keywords": ["eagle", "lion", "wings", "mythology", "legendary", "creature", "protector", "fantasy", "royalty", "symbolic"]},
    {"genre": "Monster Zombie Dog", "keywords": ["undead", "pet", "rotting", "dangerous", "creature", "attack", "horror", "decay", "hunting", "monstrous"]},
    {"genre": "Monster Mothman", "keywords": ["winged", "cryptid", "red eyes", "mysterious", "ominous", "supernatural", "creature", "sightings", "legend", "danger"]},
    {"genre": "Monster Slenderman", "keywords": ["tall", "faceless", "shadow", "urban legend", "slender", "supernatural", "creature", "haunting", "mystery", "ominous"]},
    {"genre": "Monster Dullahan", "keywords": ["headless rider", "Irish mythology", "ghost", "death", "legend", "reaper", "skeleton", "rider", "haunting", "supernatural"]},
    {"genre": "Monster The Headless Horseman", "keywords": ["horseback", "headless", "ghost", "legend", "night rider", "haunting", "evil", "supernatural", "Halloween", "headless"]},
    {"genre": "Monster The Beast of Gévaudan", "keywords": ["cryptid", "French legend", "wolf-like", "predator", "mysterious", "hunting", "dangerous", "myth", "attack", "fear"]},
    {"genre": "Monster The Jersey Devil", "keywords": ["cryptid", "New Jersey", "creature", "hooves", "horns", "wings", "myth", "evil", "mysterious", "flying"]},
    {"genre": "Monster The Loveland Frogman", "keywords": ["cryptid", "frog-like", "Ohio", "humanoid", "swamp", "myth", "legend", "mysterious", "creature", "reptilian"]},
    {"genre": "Monster The Flatwoods Monster", "keywords": ["cryptid", "alien", "West Virginia", "green", "spooky", "legend", "mysterious", "fear", "glowing eyes", "creature"]},    
    {"genre": "Planet Mercury", "keywords": ["smallest planet", "closest to the Sun", "no atmosphere", "extreme temperatures", "rocky surface"]},
    {"genre": "Planet Venus", "keywords": ["thick toxic atmosphere", "extreme greenhouse effect", "volcanic surface", "Earth's twin in size", "hottest planet"]},
    {"genre": "Planet Earth", "keywords": ["only planet with known life", "water-covered surface", "diverse ecosystems", "plate tectonics", "oxygen-rich atmosphere"]},
    {"genre": "Planet Mars", "keywords": ["red surface", "iron oxide", "thin atmosphere", "polar ice caps", "potential for human colonization"]},
    {"genre": "Planet Jupiter", "keywords": ["largest planet", "gas giant", "Great Red Spot storm", "many moons", "strong magnetic field"]},
    {"genre": "Planet Saturn", "keywords": ["iconic ring system", "gas giant", "many moons", "hydrogen-helium composition", "least dense planet"]},
    {"genre": "Planet Uranus", "keywords": ["ice giant", "tilted axis", "pale blue-green color", "methane clouds", "coldest planetary atmosphere"]},
    {"genre": "Planet Neptune", "keywords": ["farthest from the Sun", "deep blue color", "ice giant", "strong winds", "Great Dark Spot storm"]},
    {"genre": "Dwarf Planet Pluto", "keywords": ["part of the Kuiper Belt", "icy surface", "thin atmosphere", "eccentric orbit", "discovered in 1930"]},
    {"genre": "Exoplanet Proxima Centauri b", "keywords": ["orbits Proxima Centauri", "closest exoplanet to Earth", "potentially habitable", "rocky surface", "tidally locked"]},
    {"genre": "Exoplanet Kepler-452b", "keywords": ["Earth-like", "habitable zone", "potential for liquid water", "orbits a sun-like star", "distance: 1,400 light years"]},
    {"genre": "Exoplanet TRAPPIST-1e", "keywords": ["potentially habitable", "earth-sized", "three other Earth-like planets", "red dwarf star system", "liquid water possible"]},
    {"genre": "Planet Kepler-22b", "keywords": ["habitable zone", "Earth-like size", "potential for liquid water", "distant system", "orbiting a sun-like star"]},
    {"genre": "Moon Titan (Saturn)", "keywords": ["thick atmosphere", "methane lakes", "potential for life", "similar to early Earth", "cold and toxic environment"]},
    {"genre": "Moon Europa (Jupiter)", "keywords": ["ice-covered ocean", "potential for life", "tidally locked", "subs surface water", "discovered by Galileo"]},
    {"genre": "Moon Io (Jupiter)", "keywords": ["volcanic activity", "sulfuric surface", "most active body", "many volcanoes", "intense radiation"]},
    {"genre": "Moon Callisto (Jupiter)", "keywords": ["heavily cratered surface", "thin atmosphere", "potential for water ice", "potential for human exploration", "old surface"]},
    {"genre": "Moon Enceladus (Saturn)", "keywords": ["icy geysers", "subsurface ocean", "potential for life", "tidally heated", "reflective surface"]},
    {"genre": "Moon Ganymede (Jupiter)", "keywords": ["largest moon", "subsurface ocean", "magnetic field", "ancient surface", "frozen landscape"]},
    {"genre": "Galaxy Andromeda", "keywords": ["nearest spiral galaxy", "2.5 million light-years away", "will collide with Milky Way", "1 trillion stars", "visible in the night sky"]},
    {"genre": "Galaxy Milky Way", "keywords": ["home galaxy", "contains Earth", "200 billion stars", "spiral galaxy", "center contains a black hole"]},
    {"genre": "Galaxy Triangulum", "keywords": ["third-largest in Local Group", "spiral galaxy", "M33", "closest to Andromeda", "contains stars and nebulae"]},
    {"genre": "Galaxy Whirlpool (M51)", "keywords": ["spiral galaxy", "interacting with NGC 5195", "distinctive structure", "star formation", "observed by Hubble"]},
    {"genre": "Galaxy Messier 87", "keywords": ["giant elliptical galaxy", "contains a supermassive black hole", "located in Virgo cluster", "1,500,000 light years away", "contains hot gas"]},
    {"genre": "Galaxy Sombrero", "keywords": ["edge-on spiral galaxy", "distinctive hat-like appearance", "located in Virgo cluster", "large central bulge", "star formation"]},
    {"genre": "Galaxy Centaurus A", "keywords": ["elliptical galaxy", "radio galaxy", "one of the closest active galaxies", "contains a supermassive black hole", "formed from a merger"]},
    {"genre": "Galaxy NGC 1300", "keywords": ["barred spiral galaxy", "located 61 million light-years away", "observable in the Eridanus constellation", "distinctive spiral arms", "star formation regions"]},
    {"genre": "Galaxy NGC 224 (M31)", "keywords": ["Andromeda galaxy", "closest large galaxy to Milky Way", "will merge with Milky Way", "contains over 1 trillion stars", "visible to the naked eye"]},
    {"genre": "Galaxy IC 1101", "keywords": ["largest known galaxy", "located in the Abell 2029 galaxy cluster", "1.04 billion light-years away", "elliptical galaxy", "contains trillion stars"]},
    {"genre": "Galaxy NGC 2997", "keywords": ["spiral galaxy", "located in the constellation Antlia", "visible in southern hemisphere", "star formation", "close to Milky Way"]},
    {"genre": "Galaxy NGC 1365", "keywords": ["barred spiral galaxy", "located in Fornax cluster", "observed by Hubble", "active star formation", "distorted shape"]},    
    {"genre": "Orion Nebula", "keywords": ["brightest nebula", "located in the Orion constellation", "star formation region", "visible to the naked eye", "gas and dust clouds", "birthplace of stars"]},
    {"genre": "Rendering Unreal Engine 5", "keywords": ["real-time rendering", "photorealistic graphics", "Lumen", "Nanite", "ray tracing", "open world", "virtual production", "cinematic quality", "global illumination", "real-time physics"]},
    {"genre": "Rendering Unity", "keywords": ["real-time rendering", "cross-platform", "game development", "2D/3D rendering", "VR/AR support", "particle system", "C# scripting", "asset store", "shader support", "modular"]},
    {"genre": "Rendering Blender", "keywords": ["open-source", "3D modeling", "animation", "sculpting", "rendering", "VFX", "node-based compositing", "ray tracing", "simulations", "free"]},
    {"genre": "Rendering Autodesk Maya", "keywords": ["3D animation", "modeling", "rendering", "rigging", "VFX", "texturing", "lighting", "MEL scripting", "maya node editor", "animation tools"]},
    {"genre": "Rendering Cinema 4D", "keywords": ["motion graphics", "3D animation", "modeling", "rendering", "VR/AR", "integrated workflow", "advanced shaders", "MoGraph", "particles", "team render"]},
    {"genre": "Rendering V-Ray", "keywords": ["rendering engine", "photorealistic", "global illumination", "ray tracing", "architectural visualization", "interior design", "product design", "visual effects", "materials", "high-quality render"]},
    {"genre": "Rendering Redshift", "keywords": ["GPU-accelerated", "3D rendering", "visual effects", "VFX", "architecture", "motion graphics", "production-ready", "scalable", "photorealism", "high-speed rendering"]},
    {"genre": "Rendering Arnold", "keywords": ["ray tracing", "rendering engine", "photorealistic", "cinematic quality", "GPU and CPU rendering", "VFX", "character animation", "interactive", "texture mapping", "production"]},
    {"genre": "Rendering OctaneRender", "keywords": ["GPU-based", "real-time rendering", "photorealistic", "VFX", "animation", "3D modeling", "motion graphics", "materials", "lighting", "texture mapping"]},
    {"genre": "Rendering Lumion", "keywords": ["architecture", "rendering software", "real-time rendering", "interior and exterior visualization", "realistic visuals", "landscape rendering", "animation", "photorealistic", "easy-to-use", "sketchup"]},    
    {"genre": "Painter", "keywords": ["oil painting", "canvas", "brush strokes", "color palette", "realism", "impressionism", "abstract", "surrealism", "still life", "landscapes"]},
    {"genre": "Leonardo da Vinci", "keywords": ["Renaissance", "Mona Lisa", "The Last Supper", "sfumato", "anatomical studies", "oil paintings", "master of perspective", "classical", "scientific observations", "genius"]},
    {"genre": "Vincent van Gogh", "keywords": ["Post-Impressionism", "bold strokes", "vibrant colors", "Starry Night", "sunflowers", "emotionally expressive", "self-portrait", "nightscapes", "swirling patterns", "mental health"]},
    {"genre": "Pablo Picasso", "keywords": ["Cubism", "abstract art", "blue period", "Guernica", "multi-perspective", "modernism", "geometric shapes", "avant-garde", "collage", "surrealism"]},
    {"genre": "Claude Monet", "keywords": ["Impressionism", "water lilies", "light effects", "outdoor scenes", "color theory", "brushwork", "landscapes", "nature", "famous garden", "plein air painting"]},
    {"genre": "Michelangelo", "keywords": ["Renaissance", "sculpture", "Sistine Chapel", "David", "The Creation of Adam", "master of anatomy", "classical themes", "religious art", "fresco painting", "religious devotion"]},
    {"genre": "Rembrandt", "keywords": ["Baroque", "portraiture", "self-portraits", "light and shadow", "realism", "dramatic lighting", "history painting", "oil painting", "biblical scenes", "psychological depth"]},
    {"genre": "Frida Kahlo", "keywords": ["Surrealism", "symbolism", "self-portrait", "Mexican culture", "pain and suffering", "bright colors", "folk art", "expressionist", "Mexican identity", "folk imagery"]},
    {"genre": "Andy Warhol", "keywords": ["Pop Art", "mass production", "consumerism", "celebrity culture", "Campbell's Soup Cans", "bold colors", "screen printing", "repetition", "iconic", "modern commercial art"]},
    {"genre": "Pencil Drawing", "keywords": ["graphite", "sketches", "realistic drawings", "shading", "portraiture", "fine details", "fine art", "illustration", "monochromatic", "detailed lines"]},
    {"genre": "John Singer Sargent", "keywords": ["portraiture", "realism", "light and shadow", "pencil sketches", "impressionist", "famous portraitist", "modern realist", "detailed sketches", "shading", "studies"]},
    {"genre": "Albert Dürer", "keywords": ["Renaissance", "woodcuts", "engraving", "precise detail", "pencil sketches", "printmaking", "mathematical precision", "self-portrait", "nature studies", "classical works"]},
    {"genre": "Anime", "keywords": ["Japanese animation", "manga", "stylized characters", "big eyes", "vivid colors", "action scenes", "emotional storytelling", "fantasy", "superpowers", "shonen"]},
    {"genre": "Hayao Miyazaki", "keywords": ["Studio Ghibli", "anime", "whimsical characters", "hand-drawn animation", "fantasy world", "environmental themes", "coming-of-age", "Hayao", "My Neighbor Totoro", "Spirited Away"]},
    {"genre": "Osamu Tezuka", "keywords": ["Manga", "anime", "Astro Boy", "father of manga", "cartoonish style", "action-adventure", "vivid storytelling", "multiple genres", "shoujo", "modern manga creator"]},
    {"genre": "Cartoon", "keywords": ["animated series", "humor", "exaggerated features", "cartoonish style", "comic strips", "animation studios", "funny characters", "family-friendly", "comedy", "cultural satire"]},
    {"genre": "Walt Disney", "keywords": ["animation", "Disney classics", "Mickey Mouse", "The Lion King", "cartooning", "family entertainment", "storybook", "creativity", "magic", "legacy"]},
    {"genre": "Chuck Jones", "keywords": ["Looney Tunes", "animation", "humor", "cartoon characters", "Wile E. Coyote", "Bugs Bunny", "Daffy Duck", "timing", "visual gags", "animated shorts"]},
    {"genre": "Digital Art", "keywords": ["Photoshop", "illustration", "digital painting", "pixel art", "3D modeling", "concept art", "CGI", "realism", "textures", "graphic design"]},
    {"genre": "Beeple", "keywords": ["digital art", "3D modeling", "futuristic", "NFT art", "famous digital artist", "motion graphics", "everydays project", "surreal landscapes", "modern art", "concept art"]},
    {"genre": "Greg Rutkowski", "keywords": ["digital painting", "fantasy art", "concept artist", "illustration", "game art", "vivid colors", "realism", "detailed artwork", "fantasy worlds", "light and shadows"]},
    {"genre": "Artgerm", "keywords": ["digital painting", "portrait", "realistic", "modern style", "digital techniques", "concept art", "female characters", "illustration", "popular culture", "high detail"]},
    {"genre": "Feng Zhu", "keywords": ["concept art", "digital painting", "industrial design", "environment design", "cinematic", "sci-fi", "game art", "character design", "visual storytelling", "dynamic scenes"]},
    {"genre": "Oil Painting", "keywords": ["Leonardo da Vinci", "Vincent van Gogh", "Claude Monet", "Pablo Picasso", "Michelangelo", "Rembrandt", "Frida Kahlo", "Andy Warhol", "Johannes Vermeer", "Diego Rivera"]},
    {"genre": "Pencil Drawing", "keywords": ["Leonardo da Vinci", "Albrecht Dürer", "Michelangelo", "John Tenniel", "Augustus Saint-Gaudens", "Norman Rockwell", "Gerald Scarfe", "Tim Burton", "Bansky", "Zdzisław Beksiński"]},
    {"genre": "Anime Drawing", "keywords": ["Hayao Miyazaki", "Makoto Shinkai", "Satoshi Kon", "Katsuhiro Otomo", "Akira Toriyama", "Yoshiyuki Tomino", "Mamoru Hosoda", "Naoko Takeuchi", "Tite Kubo", "Eiichiro Oda"]},
    {"genre": "Cartoon Drawing", "keywords": ["Walt Disney", "Chuck Jones", "Tex Avery", "Hanna-Barbera", "Matt Groening", "Bill Watterson", "Jim Davis", "Osamu Tezuka", "John Kricfalusi", "Seth MacFarlane"]},
    {"genre": "Digital Drawing", "keywords": ["Kyle T. Webster", "Greg Rutkowski", "Aaron Blaise", "Loish", "Feng Zhu", "Sam Yang", "Artgerm", "Sakimichan", "Ilya Kuvshinov", "Ross Tran"]},
    {"genre": "Watercolor Painting", "keywords": ["Winslow Homer", "John Singer Sargent", "J.M.W. Turner", "Claude Monet", "Edward Hopper", "Georges Rouault", "Albrecht Dürer", "Hiroshi Yoshida", "Milton Avery", "Mary Cassatt"]},
    {"genre": "Sculpture", "keywords": ["Michelangelo", "Auguste Rodin", "Henry Moore", "Donatello", "Constantin Brâncuși", "Barbara Hepworth", "Alexander Calder", "Jean Arp", "Alexander McQueen", "Lorenzo Ghiberti"]},
    {"genre": "Graffiti", "keywords": ["Banksy", "Jean-Michel Basquiat", "Keith Haring", "Shepard Fairey", "RETNA", "Os Gêmeos", "Futura 2000", "Space Invader", "DAZE", "Swoon"]},
    {"genre": "Abstract Art", "keywords": ["Wassily Kandinsky", "Piet Mondrian", "Jackson Pollock", "Mark Rothko", "Franz Kline", "Helen Frankenthaler", "Kazimir Malevich", "Joan Miró", "Robert Delaunay", "Theo van Doesburg"]},
    {"genre": "Fantasy Art", "keywords": ["Frank Frazetta", "Boris Vallejo", "Julie Bell", "Michael Whelan", "Luis Royo", "H. R. Giger", "Brom", "Chris Riddell", "John Howe", "Alan Lee"]},
    {"genre": "Action Movies", "keywords": ["Steven Spielberg", "George Lucas", "James Cameron", "Michael Bay", "Ridley Scott", "Christopher Nolan", "Zack Snyder", "J.J. Abrams", "John Woo", "Luc Besson"]},
    {"genre": "Animation Movies", "keywords": ["Walt Disney", "Hayao Miyazaki", "John Lasseter", "Tim Burton", "Don Bluth", "Nick Park", "Brad Bird", "Andrew Stanton", "Pete Docter", "Glen Keane"]},
    {"genre": "Horror Movies", "keywords": ["Alfred Hitchcock", "John Carpenter", "Wes Craven", "George A. Romero", "James Wan", "Guillermo del Toro", "Stanley Kubrick", "Tobe Hooper", "Sam Raimi", "David Cronenberg"]},
    {"genre": "Comedy Movies", "keywords": ["Charlie Chaplin", "Mel Brooks", "Woody Allen", "Judd Apatow", "Coen Brothers", "John Hughes", "Christopher Guest", "Peter Farrelly", "Paul Feig", "Edgar Wright"]},
    {"genre": "Drama Movies", "keywords": ["Martin Scorsese", "Francis Ford Coppola", "Quentin Tarantino", "Ridley Scott", "Steven Spielberg", "Christopher Nolan", "Danny Boyle", "Ang Lee", "David Fincher", "Tom McCarthy"]},
    {"genre": "Sci-Fi Movies", "keywords": ["Stanley Kubrick", "Ridley Scott", "George Lucas", "James Cameron", "Christopher Nolan", "Steven Spielberg", "Luc Besson", "Dennis Villeneuve", "Andrei Tarkovsky", "J.J. Abrams"]},
    {"genre": "Superhero Movies", "keywords": ["Stan Lee", "Jack Kirby", "Christopher Nolan", "Joss Whedon", "Zack Snyder", "Jon Favreau", "Taika Waititi", "James Gunn", "Ryan Coogler", "Matt Reeves"]},
    {"genre": "TV Series Drama", "keywords": ["David Chase", "Vince Gilligan", "Matthew Weiner", "Aaron Sorkin", "Shonda Rhimes", "Mindy Kaling", "Darren Star", "Ryan Murphy", "David Simon", "Damien Chazelle"]},
    {"genre": "TV Series Comedy", "keywords": ["Chuck Lorre", "Greg Daniels", "Dan Harmon", "Larry David", "Tina Fey", "Amy Poehler", "Michael Schur", "Billy Wilder", "Steven Moffat", "Trey Parker"]},
    {"genre": "Documentary Filmmakers", "keywords": ["Werner Herzog", "Michael Moore", "Ken Burns", "Spike Lee", "Ava DuVernay", "Errol Morris", "Barbara Kopple", "Robert Flaherty", "Laura Poitras", "Louis Theroux"]},
    {"genre": "Fantasy TV Shows", "keywords": ["George R.R. Martin", "J.R.R. Tolkien", "Joss Whedon", "David Benioff", "D.B. Weiss", "Martin Scorsese", "Peter Jackson", "Alan Ball", "Terry Goodkind", "M. Night Shyamalan"]},
    {"genre": "Thriller Movies", "keywords": ["David Fincher", "Alfred Hitchcock", "Christopher Nolan", "Martin Scorsese", "Paul Thomas Anderson", "Jonathan Demme", "John Frankenheimer", "Michael Mann", "Brian De Palma", "Fritz Lang"]},
    {"genre": "Crime Movies", "keywords": ["Martin Scorsese", "Quentin Tarantino", "Francis Ford Coppola", "Guy Ritchie", "John Woo", "Michael Mann", "Sergio Leone", "David Fincher", "Brett Ratner", "Michael Bay"]},
    {"genre": "Musical Movies", "keywords": ["Bob Fosse", "Lin-Manuel Miranda", "Baz Luhrmann", "Andrew Lloyd Webber", "Richard Rodgers", "Oscar Hammerstein II", "Gene Kelly", "Stanley Donen", "Sondheim", "John Waters"]},
    {"genre": "War Movies", "keywords": ["Steven Spielberg", "Francis Ford Coppola", "Oliver Stone", "Stanley Kubrick", "Ridley Scott", "Christopher Nolan", "Paul Verhoeven", "John Wayne", "Terrence Malick", "David Ayer"]},
    {"genre": "Family Movies", "keywords": ["Steven Spielberg", "Walt Disney", "Richard Curtis", "Chris Columbus", "Joe Johnston", "Brad Bird", "Jodie Foster", "Rob Reiner", "Nancy Meyers", "Tim Burton"]},
    {"genre": "Mystery Movies", "keywords": ["Agatha Christie", "Sir Arthur Conan Doyle", "Alfred Hitchcock", "David Fincher", "Rian Johnson", "Billy Wilder", "M. Night Shyamalan", "Gillian Flynn", "Stanley Kubrick", "Neil Jordan"]},
    {"genre": "Animated TV Shows", "keywords": ["Matt Groening", "Seth MacFarlane", "Trey Parker", "Dan Harmon", "Mike Judge", "Justin Roiland", "Gene Luen Yang", "J.J. Abrams", "Phyllis Diller", "Craig McCracken"]},
    {"genre": "Black and White Photography", "keywords": ["Ansel Adams", "Henri Cartier-Bresson", "Dorothea Lange", "Robert Frank", "Richard Avedon", "Irving Penn", "Sebastião Salgado", "Man Ray", "Edward Weston", "Bill Brandt"]},
    {"genre": "Portrait Photography", "keywords": ["Annie Leibovitz", "Steve McCurry", "Helmut Newton", "Yousuf Karsh", "Richard Avedon", "David Bailey", "Dorothea Lange", "Cindy Sherman", "Robert Mapplethorpe", "Sally Mann"]},
    {"genre": "Fashion Photography", "keywords": ["Mario Sorrenti", "Helmut Newton", "Richard Avedon", "Peter Lindbergh", "Irving Penn", "Ellen von Unwerth", "Bruce Weber", "Tim Walker", "Annie Leibovitz", "Patrick Demarchelier"]},
    {"genre": "Landscape Photography", "keywords": ["Ansel Adams", "Edward Weston", "Galen Rowell", "Michael Kenna", "David Muench", "Art Wolfe", "George Tice", "James Whitlow Delano", "Berenice Abbott", "Tina Modotti"]},
    {"genre": "Street Photography", "keywords": ["Henri Cartier-Bresson", "Diane Arbus", "Vivian Maier", "Garry Winogrand", "Robert Frank", "Joel Meyerowitz", "Alex Webb", "Martin Parr", "Mary Ellen Mark", "Bruce Davidson"]},
    {"genre": "Documentary Photography", "keywords": ["Sebastião Salgado", "James Nachtwey", "Dorothea Lange", "W. Eugene Smith", "Robert Capa", "Steve McCurry", "Garry Winogrand", "David Seymour", "Richard Avedon", "Susan Meiselas"]},
    {"genre": "Architectural Photography", "keywords": ["Julius Shulman", "Ezra Stoller", "Iwan Baan", "Michael Wolf", "Hiroshi Sugimoto", "Norman Foster", "David Chipperfield", "Frank Lloyd Wright", "Pierre Jeanneret", "Zaha Hadid"]},
    {"genre": "Fine Art Photography", "keywords": ["Cindy Sherman", "Andreas Gursky", "Jeff Wall", "Richard Prince", "Robert Mapplethorpe", "Gregory Crewdson", "Nan Goldin", "Sally Mann", "Wolfgang Tillmans", "Hiroshi Sugimoto"]},
    {"genre": "Nature Photography", "keywords": ["Art Wolfe", "Frans Lanting", "Thomas Mangelsen", "Nick Brandt", "Steve Winter", "David Doubilet", "Paul Nicklen", "James Balog", "Shane Gross", "Galen Rowell"]},
    {"genre": "Commercial Photography", "keywords": ["David LaChapelle", "Nick Knight", "Mario Sorrenti", "Steven Meisel", "Bruce Weber", "Michael Thompson", "Peter Lindbergh", "Annie Leibovitz", "Juergen Teller", "Patrick Demarchelier"]},
    {"genre": "Photojournalism", "keywords": ["Henri Cartier-Bresson", "Steve McCurry", "James Nachtwey", "Robert Capa", "Dorothea Lange", "Eliot Porter", "Mary Ellen Mark", "W Eugene Smith", "Sebastião Salgado", "Don McCullin"]},
    {"genre": "Food Photography", "keywords": ["Penny De Los Santos", "David Loftus", "Danny Christensen", "Teri Lyn Fisher", "Bea Lubas", "Hugh Johnson", "Jamie Oliver", "Joanna Henderson", "Matt Armendariz", "Chris Court"]},
    {"genre": "Underwater Photography", "keywords": ["David Doubilet", "Paul Nicklen", "Shane Gross", "Brian Skerry", "Eric Cheng", "Alex Mustard", "Michael AW", "Martin Edge", "Jim Abernethy", "Hiroshi Hasegawa"]},
    {"genre": "Night Photography", "keywords": ["Stephen Shore", "Joel Meyerowitz", "Michael Kenna", "Ian Ruhter", "Doug Rickard", "Jerry Uelsmann", "Dustin Farrell", "Lloyd Ziff", "Sophie Calle", "Jesse Marlow"]},
    {"genre": "Blacklight Photography", "keywords": ["László Moholy-Nagy", "Ernst Haas", "Robert Mapplethorpe", "Nadav Kander", "Garry Winogrand", "Gordon Parks", "Helmut Newton", "Edward Weston", "Tim Walker", "Jerry Uelsmann"]},
    {"genre": "Aerial Photography", "keywords": ["George Steinmetz", "Vincent Laforet", "Edward Burtynsky", "Richard Misrach", "David Maisel", "Jason Hawkes", "Dmitry Moiseenko", "Tom Hegen", "Jason deCaires Taylor", "Michael Davis"]},
    {"genre": "Celebrity Photography", "keywords": ["Annie Leibovitz", "Helmut Newton", "Richard Avedon", "Mario Sorrenti", "Peter Lindbergh", "Greg Gorman", "Bryan Adams", "Terry O'Neill", "David LaChapelle", "Bruce Weber"]},
    {"genre": "Conceptual Photography", "keywords": ["Sophie Calle", "Gregory Crewdson", "Thomas Demand", "Jeff Wall", "Zed Nelson", "Andreas Gursky", "Barbara Probst", "Hiroshi Sugimoto", "Philip-Lorca diCorcia", "Tim Walker"]},
    {"genre": "Fashion Editorial Photography", "keywords": ["Steven Meisel", "Mario Sorrenti", "Bruce Weber", "Richard Avedon", "Annie Leibovitz", "Patrick Demarchelier", "Tim Walker", "Peter Lindbergh", "David Sims", "Camilla Akrans"]},
    {"genre": "DSLR", "keywords": ["Canon EOS 5D Mark IV", "Nikon D850", "Sony Alpha a7R IV", "Canon EOS-1D X Mark III", "Nikon D750", "Sony Alpha a6300", "Canon EOS Rebel T7", "Fujifilm X-T4", "Olympus OM-D E-M1 Mark III", "Panasonic Lumix GH5"]},
    {"genre": "Mirrorless", "keywords": ["Sony Alpha a7 III", "Canon EOS R", "Nikon Z6", "Fujifilm X-T3", "Olympus OM-D E-M5 Mark III", "Panasonic Lumix G85", "Sony Alpha a6500", "Leica SL2", "Sigma fp", "Sony Alpha a9"]},
    {"genre": "Compact", "keywords": ["Canon PowerShot G7 X Mark III", "Sony Cyber-shot RX100 VII", "Panasonic Lumix LX100 II", "Fujifilm X100V", "Ricoh GR III", "Olympus Tough TG-6", "Canon EOS M6 Mark II", "Nikon Coolpix A1000", "Leica D-Lux 7", "Panasonic Lumix TZ200"]},
    {"genre": "Action Camera", "keywords": ["GoPro HERO10 Black", "DJI Osmo Action", "GoPro HERO9 Black", "Insta360 ONE X2", "GoPro HERO8 Black", "Sony Action Cam FDR-X3000", "Akaso Brave 7 LE", "Garmin VIRB Ultra 30", "Osmo Pocket 2", "Olympus TG-Tracker"]},
    {"genre": "Video Camera", "keywords": ["Canon XA40", "Sony FDR-AX700", "Panasonic HC-X1", "Blackmagic Design URSA Mini Pro 12K", "Sony PXW-FX9", "Panasonic Lumix GH5S", "Canon EOS C300 Mark III", "RED Komodo 6K", "Sony FS7", "JVC GY-HM170U"]},
    {"genre": "360 Camera", "keywords": ["Insta360 ONE X2", "GoPro MAX", "Ricoh Theta Z1", "Samsung Gear 360", "Insta360 ONE R", "Vuze XR", "Garmin VIRB 360", "Panasonic 360 Camera", "Fujifilm 360", "Kodak PIXPRO SP360 4K"]},
    {"genre": "Film Camera", "keywords": ["Leica M6", "Nikon F6", "Canon EOS-1V", "Pentax 67", "Hasselblad 500C/M", "Olympus OM-1", "Yashica Mat-124G", "Minolta X-700", "Contax G2", "Canon AE-1"]},
    {"genre": "Polaroid Camera", "keywords": ["Polaroid Originals OneStep 2", "Fujifilm Instax Mini 11", "Polaroid Snap Touch", "Fujifilm Instax Square SQ1", "Polaroid OneStep+", "Fujifilm Instax Wide 300", "Polaroid Now+", "Fujifilm Instax Mini LiPlay", "Leica Sofort", "Fujifilm Instax Mini 90 Neo Classic"]},
    {"genre": "Drone Camera", "keywords": ["DJI Mavic Air 2", "DJI Phantom 4 Pro V2.0", "Autel Robotics EVO II", "DJI Mini 2", "Parrot Anafi", "DJI Air 2S", "DJI Mavic Pro", "Skydio 2", "Autel EVO Lite", "Hubsan Zino 2"]},
    {"genre": "Lens Types", "keywords": ["Wide-angle lens", "Telephoto lens", "Macro lens", "Standard lens", "Fisheye lens", "Tilt-shift lens", "Zoom lens", "Prime lens", "Pancake lens", "Superzoom lens"]},
    {"genre": "Camera Modes", "keywords": ["Portrait Mode", "Landscape Mode", "Night Mode", "Sports Mode", "Macro Mode", "Manual Mode", "Aperture Priority", "Shutter Priority", "Program Mode", "Time-lapse Mode"]},
    {"genre": "Camera Zoom", "keywords": ["Optical Zoom", "Digital Zoom", "Hybrid Zoom", "Superzoom", "2x Optical Zoom", "10x Optical Zoom", "40x Digital Zoom", "Lens with Zoom Ring", "Variable Zoom Lens", "Wide-angle Zoom"]},
    {"genre": "Video Features", "keywords": ["4K Video Recording", "1080p HD Video", "120fps Slow Motion", "240fps Slow Motion", "Stabilization", "HDR Video", "Live Streaming", "Microphone Input", "360 Video", "Wide-angle Video"]},
    {"genre": "Photo Effects", "keywords": ["Black and White", "Sepia", "Vivid", "Soft Focus", "Vintage", "HDR", "Bokeh", "Fish-eye Effect", "High Contrast", "Color Splash"]},
    {"genre": "Video Editing", "keywords": ["Cutting", "Transitions", "Speed Adjustment", "Color Grading", "Stabilization", "Text Overlay", "Audio Sync", "Motion Tracking", "Keyframing", "Effects and Filters"]},
    {"genre": "Time-lapse Camera", "keywords": ["GoPro HERO10 Black", "Brinno TLC2000", "Canon EOS 5D Mark IV", "Sony A7R IV", "Panasonic Lumix GH5", "Fujifilm X-T3", "Nikon D850", "Sony Alpha a7 III", "Olympus OM-D E-M1 Mark III", "Ricoh Theta Z1"]},
    {"genre": "Low Light Photography", "keywords": ["Sony A7S III", "Nikon D850", "Canon EOS R5", "Fujifilm X-T4", "Panasonic GH5", "Leica SL2", "Olympus OM-D E-M1 Mark III", "Sony Alpha a6400", "Canon EOS-1D X Mark III", "Pentax K-1 Mark II"]},
    {"genre": "Clothing Gucci", "keywords": ["luxury", "designer", "high-end", "elegant", "modern", "vibrant colors", "bold patterns", "rich textures", "iconic", "streetwear"]},
    {"genre": "Clothing Louis Vuitton", "keywords": ["luxury", "designer", "classic", "monogram print", "timeless", "elegant", "modern", "premium", "leather goods", "vintage"]},
    {"genre": "Clothing Chanel", "keywords": ["luxury", "classic", "elegant", "timeless", "chic", "minimalist", "sophisticated", "black and white", "refined", "high fashion"]},
    {"genre": "Clothing Prada", "keywords": ["luxury", "avant-garde", "modern", "minimalist", "innovative", "sleek", "structured", "bold colors", "vibrant", "high-end"]},
    {"genre": "Clothing Versace", "keywords": ["bold", "luxury", "vibrant", "rich patterns", "glamorous", "baroque", "bold colors", "extravagant", "high-end", "designer"]},
    {"genre": "Clothing Nike", "keywords": ["sportswear", "athleisure", "comfortable", "modern", "casual", "streetwear", "activewear", "iconic", "bold", "performance-driven"]},
    {"genre": "Clothing Adidas", "keywords": ["sportswear", "athletic", "casual", "comfortable", "modern", "streetwear", "activewear", "performance", "minimalist", "sustainable"]},
    {"genre": "Clothing Levi's", "keywords": ["denim", "casual", "iconic", "classic", "vintage", "comfortable", "stylish", "jeans", "versatile", "casual wear"]},
    {"genre": "Clothing H&M", "keywords": ["affordable", "casual", "trendy", "modern", "minimalist", "everyday wear", "comfortable", "basic pieces", "versatile", "fashion-forward"]},
    {"genre": "Clothing Zara", "keywords": ["trendy", "casual", "elegant", "affordable", "modern", "urban", "versatile", "chic", "fashion-forward", "minimalist"]},
    {"genre": "Clothing Supreme", "keywords": ["streetwear", "urban", "bold graphics", "minimalist", "modern", "iconic", "casual", "bold colors", "exclusive", "high demand"]},
    {"genre": "Clothing Off-White", "keywords": ["streetwear", "modern", "urban", "fashion-forward", "contemporary", "bold prints", "graphic design", "minimalist", "exclusive", "luxury"]},
    {"genre": "Clothing Palace", "keywords": ["streetwear", "skateboarding", "bold graphics", "casual", "urban", "modern", "comfortable", "laid-back", "youth culture", "iconic"]},
    {"genre": "Clothing Stüssy", "keywords": ["streetwear", "skateboarding", "casual", "vintage", "urban", "graphic prints", "comfortable", "iconic", "bold colors", "retro"]},
    {"genre": "Clothing A Bathing Ape (BAPE)", "keywords": ["streetwear", "urban", "bold graphics", "camouflage", "iconic", "bold colors", "comfortable", "luxury streetwear", "casual", "exclusive"]},
    {"genre": "Clothing Patagonia", "keywords": ["outdoor", "sustainable", "eco-friendly", "functional", "athletic", "adventurous", "high-performance", "comfortable", "minimalist", "ethical"]},
    {"genre": "Clothing Everlane", "keywords": ["sustainable", "ethical", "minimalist", "modern", "simple", "transparent", "quality fabrics", "comfortable", "affordable", "chic"]},
    {"genre": "Clothing Allbirds", "keywords": ["sustainable", "eco-friendly", "comfortable", "casual", "athletic", "simple design", "minimalist", "lightweight", "breathable", "vegan-friendly"]},
    {"genre": "Clothing Reformation", "keywords": ["sustainable", "vintage-inspired", "modern", "chic", "feminine", "stylish", "eco-friendly fabrics", "bold colors", "timeless designs", "ethical"]},
    {"genre": "Clothing Toms", "keywords": ["sustainable", "casual", "comfortable", "ethical", "minimalist", "vegan-friendly", "slip-ons", "everyday wear", "simple", "affordable"]},
    {"genre": "Clothing Christian Louboutin", "keywords": ["luxury", "designer", "high heels", "iconic red sole", "elegant", "bold", "fashion-forward", "chic", "exclusive", "premium"]},
    {"genre": "Clothing Jimmy Choo", "keywords": ["luxury", "designer", "elegant", "high-end", "chic", "fashion-forward", "high heels", "bold", "glamorous", "exclusive"]},
    {"genre": "Clothing Manolo Blahnik", "keywords": ["luxury", "designer", "high heels", "elegant", "fashion-forward", "chic", "high-end", "classic", "iconic", "timeless"]},
    {"genre": "Clothing Nike Air Jordan", "keywords": ["sportswear", "athleisure", "casual", "iconic", "sneakers", "streetwear", "comfortable", "bold colors", "fashion-forward", "athletic"]},
    {"genre": "Clothing Adidas Yeezy", "keywords": ["designer", "streetwear", "sneakers", "iconic", "bold", "comfortable", "fashion-forward", "high-end", "modern", "exclusive"]},
    {"genre": "Clothing Carhartt", "keywords": ["durable", "workwear", "rugged", "comfortable", "outdoor", "functional", "casual", "modern", "versatile", "heavy-duty"]},
    {"genre": "Clothing Dickies", "keywords": ["workwear", "durable", "functional", "comfortable", "casual", "rugged", "outdoor", "affordable", "stylish", "work pants"]},
    {"genre": "Clothing The North Face", "keywords": ["outdoor", "rugged", "comfortable", "durable", "functional", "athletic", "warm", "modern", "versatile", "sporty"]},
    {"genre": "Clothing Columbia Sportswear", "keywords": ["outdoor", "functional", "comfortable", "rugged", "athletic", "durable", "warm", "versatile", "modern", "sportswear"]},
    {"genre": "Clothing Helly Hansen", "keywords": ["workwear", "outdoor", "rugged", "durable", "functional", "comfortable", "sportswear", "versatile", "weather-resistant", "athletic"]},
    {"genre": "Action Running", "keywords": ["fast pace", "determined", "athletic", "sprint", "motion blur", "urban", "exhilarating", "action scene", "exhausted", "quick escape"]},
    {"genre": "Action Jumping", "keywords": ["height", "acrobatic", "effortless", "athletic", "suspended in air", "landing", "quick movement", "energetic", "freedom", "adventure"]},
    {"genre": "Action Throwing", "keywords": ["target", "quick release", "energetic", "focused", "sports", "disposal", "object", "force", "dynamic", "action"]},
    {"genre": "Action Catching", "keywords": ["fast reflex", "focus", "object", "quick movement", "athletic", "reaction time", "grip", "sporty", "precision", "agility"]},
    {"genre": "Action High Five", "keywords": ["celebration", "teamwork", "excitement", "connection", "friendly", "achievement", "fast interaction", "enthusiasm", "quick gesture", "victory"]},
    {"genre": "Action Smiling", "keywords": ["happiness", "joy", "positive energy", "quick reaction", "warmth", "friendly", "genuine", "cheerful", "expressive", "connection"]},
    {"genre": "Action Waving", "keywords": ["greeting", "goodbye", "friendly", "quick action", "gesture", "enthusiastic", "expression", "acknowledgment", "interaction", "friendly"]},
    {"genre": "Action Blinking", "keywords": ["quick gesture", "eye movement", "expression", "slightly slow motion", "focused", "expression change", "pause", "delicate", "fast-paced scene", "natural"]},
    {"genre": "Action Laughing", "keywords": ["happiness", "quick reaction", "joy", "laughter", "social interaction", "quick expression", "excited", "genuine", "moment of humor", "spontaneous"]},
    {"genre": "Action Sighing", "keywords": ["relief", "exhaustion", "tiredness", "emotion", "gesture", "quick breath", "expressive", "momentary pause", "natural", "mood shift"]},
    {"genre": "Action Drinking", "keywords": ["quick sip", "refreshing", "motion", "pause", "action", "hydration", "everyday life", "simple gesture", "close-up", "momentary"]},
    {"genre": "Action Texting", "keywords": ["quick message", "phone screen", "fingers typing", "modern interaction", "quick response", "social", "communication", "fast-paced", "focused", "technology"]},
    {"genre": "Action Opening a Door", "keywords": ["action", "transition", "momentary", "curiosity", "relief", "quick gesture", "movement", "new scene", "entry", "escape"]},
    {"genre": "Action Button Press", "keywords": ["simple gesture", "control", "interaction", "modern", "technology", "quick action", "communication", "device", "motion", "fast response"]},
    {"genre": "Action Looking at Clock", "keywords": ["time check", "momentary pause", "reaction", "anticipation", "waiting", "quick glance", "curiosity", "everyday life", "concern", "focus"]},
    {"genre": "Action Stretching", "keywords": ["quick stretch", "relief", "momentary pause", "body movement", "loosen up", "flexibility", "short motion", "energy boost", "relaxed", "morning routine"]},
    {"genre": "Action Shaking Head", "keywords": ["disagreement", "negative", "gesture", "frustration", "reaction", "quick movement", "non-verbal communication", "dismissal", "emotion", "expression"]},
    {"genre": "Action Nodding", "keywords": ["agreement", "yes", "approval", "simple gesture", "understanding", "quick action", "acknowledgment", "short interaction", "positive", "communication"]},
    {"genre": "Action Pointing", "keywords": ["directing", "focus", "attention", "quick gesture", "signal", "directional", "simple movement", "action", "emphasis", "expression"]},
    {"genre": "Action Shushing", "keywords": ["silence", "quiet gesture", "motion", "discreet", "calming", "secretive", "hush", "quick interaction", "expressive", "momentary"]},
    {"genre": "Action Surprise", "keywords": ["shock", "quick expression", "open mouth", "eyes wide", "momentary pause", "reaction", "emotion", "unexpected", "gesture", "change of scene"]},
    {"genre": "Action Anger", "keywords": ["clenched fists", "furrowed brow", "expression", "aggressive", "quick reaction", "intense", "emotion", "frustration", "fury", "momentary"]},
    {"genre": "Action Sadness", "keywords": ["slumped shoulders", "downcast eyes", "slow motion", "moment of despair", "quiet gesture", "disappointment", "emotion", "reflection", "pause", "moody"]},
    {"genre": "Action Fear", "keywords": ["wide eyes", "quick movement", "stiff posture", "breathing heavily", "reaction", "anxiety", "nervousness", "motion blur", "quick action", "jump scare"]},
    {"genre": "Action Celebration", "keywords": ["jumping", "clapping", "high-five", "shouting", "joy", "victory", "cheering", "expressive", "exciting", "quick burst of energy"]},
    {"genre": "Forest at Night", "keywords": ["moonlit trees", "owl hooting", "crickets chirping", "mystical shadows", "cool breeze", "fireflies", "dark pathways", "hidden wildlife", "tranquil", "starry sky"]},
    {"genre": "City Streets at Midnight", "keywords": ["neon lights", "empty roads", "quiet ambiance", "distant sirens", "reflective puddles", "urban mystery", "isolated vibes", "streetlights", "shadows", "modern allure"]},
    {"genre": "Beach under the Moon", "keywords": ["waves lapping", "silver light on water", "soft sand", "cool air", "calm tides", "starlit sky", "peaceful sounds", "distant ships", "romantic", "isolated"]},
    {"genre": "Mountain Under Starlight", "keywords": ["snow-capped peaks", "clear sky", "cool crisp air", "absolute silence", "constellations", "serene", "campfire warmth", "distant howls", "mystical", "majestic"]},
    {"genre": "Countryside Night", "keywords": ["barn lights glowing", "crickets", "fireflies in the fields", "clear skies", "rustling leaves", "quiet serenity", "moonlit fences", "cattle resting", "cool air", "natural calm"]},
    {"genre": "Desert Under Stars", "keywords": ["endless dunes", "cool breeze", "shooting stars", "absolute silence", "mystical atmosphere", "open expanse", "moonlit sand", "nomadic setting", "ancient vibes", "remote"]},
    {"genre": "Rainy Urban Night", "keywords": ["wet streets", "reflective lights", "umbrellas", "muted sounds", "soft rain", "cozy indoors", "dim streetlights", "quiet neighborhoods", "melancholic", "soothing"]},
    {"genre": "Rural Village Evening", "keywords": ["dimly lit streets", "warm house lights", "dogs barking", "smoke from chimneys", "quiet atmosphere", "family gatherings", "moonlight on paths", "soft breezes", "homey", "peaceful"]},
    {"genre": "Jungle at Night", "keywords": ["dense trees", "animal calls", "fireflies", "mystery", "humid air", "moonlight filtering through leaves", "nocturnal life", "hidden predators", "exotic vibes", "adventurous"]},
    {"genre": "Lake under the Moon", "keywords": ["still waters", "reflections of stars", "cool air", "chirping frogs", "peaceful", "fishing boats", "soft ripples", "tranquil escape", "whispers of wind", "natural beauty"]},
    {"genre": "Winter Night", "keywords": ["snowy landscape", "glowing windows", "frosty air", "footprints in snow", "stillness", "holiday lights", "fireplace warmth", "crisp atmosphere", "silent streets", "cozy vibes"]},
    {"genre": "Suburban Night", "keywords": ["streetlights", "calm atmosphere", "occasional cars", "quiet homes", "distant sounds of nightlife", "tree-lined streets", "peaceful", "stars overhead", "evening walks", "modern suburban feel"]},
    {"genre": "Seaside Storm at Night", "keywords": ["crashing waves", "lightning flashes", "roaring winds", "dark waters", "powerful ambiance", "stormy clouds", "raw energy", "dangerous beauty", "ocean's wrath", "isolated"]},
    {"genre": "Rooftop Under Stars", "keywords": ["panoramic view", "cool night air", "cityscape", "starlit sky", "whispering wind", "modern vibe", "romantic", "urban escape", "solitude", "peaceful reflections"]},
    {"genre": "Night Market", "keywords": ["colorful lights", "crowded paths", "local delicacies", "buzzing energy", "street performances", "vibrant stalls", "cultural richness", "friendly chatter", "exotic scents", "lively"]},
    {"genre": "Campfire at Midnight", "keywords": ["crackling fire", "stars above", "warmth", "stories shared", "smoke drifting", "surrounded by nature", "peaceful glow", "group camaraderie", "wooded setting", "relaxing"]},
    {"genre": "Moonlit Cliffside", "keywords": ["ocean view", "howling winds", "starry sky", "majestic ambiance", "serenity", "soft grass", "distant waves", "peaceful isolation", "romantic mood", "natural grandeur"]},
    {"genre": "Urban Alley at Night", "keywords": ["dimly lit", "mystery", "shadows", "graffiti", "quiet tension", "urban charm", "echoing footsteps", "isolation", "raw edge", "gritty atmosphere"]},
    {"genre": "Ship at Sea in the Night", "keywords": ["open waters", "moonlit deck", "sound of waves", "navigation lights", "vastness", "crew activity", "isolation", "sea breeze", "mystical journey", "adventure"]},
    {"genre": "Tundra Under Aurora", "keywords": ["glowing lights", "snowy expanse", "silent beauty", "cold air", "distant mountains", "majestic spectacle", "nighttime wonder", "northern lights", "peaceful", "remote wonder"]},    
    {"genre": "Forest at Dawn", "keywords": ["misty trees", "soft sunlight", "dew on leaves", "birds chirping", "tranquil", "fresh air", "wildlife waking", "shimmering light", "peaceful", "nature's awakening"]},
    {"genre": "Countryside at Noon", "keywords": ["golden fields", "bright sunlight", "blue skies", "farmhouses", "cattle grazing", "gentle breeze", "rural serenity", "verdant meadows", "crickets chirping", "open space"]},
    {"genre": "City in the Afternoon", "keywords": ["bustling streets", "sun-dappled skyscrapers", "traffic", "urban life", "crowds", "cafés buzzing", "warm tones", "shadow play", "commerce in action", "modern vibe"]},
    {"genre": "Beach at Sunset", "keywords": ["orange horizon", "waves crashing", "calm tides", "romantic", "golden glow", "silhouetted palm trees", "soothing sound", "soft sand", "cooling air", "peaceful retreat"]},
    {"genre": "Mountain at Sunrise", "keywords": ["majestic peaks", "pink and orange skies", "crisp air", "serene", "snow-capped", "hikers starting journey", "panoramic views", "clouds below", "first light", "nature's grandeur"]},
    {"genre": "Desert at High Noon", "keywords": ["blazing sun", "golden dunes", "dry heat", "mirage", "isolated", "cactus", "open expanse", "shimmering sand", "extreme conditions", "endless horizons"]},
    {"genre": "Rainy Village Evening", "keywords": ["drizzling rain", "wet cobblestones", "glowing windows", "smoke from chimneys", "muddy paths", "quiet streets", "rustic charm", "soft thunder", "raindrop sounds", "cozy atmosphere"]},
    {"genre": "Urban Nightlife", "keywords": ["neon lights", "crowded streets", "clubs and bars", "music", "modern architecture", "car headlights", "night market", "lively energy", "cityscape reflections", "nocturnal excitement"]},
    {"genre": "Winter Morning", "keywords": ["snow-covered landscape", "frosty air", "chimneys smoking", "gloves and scarves", "quiet streets", "crisp sunlight", "ice crystals", "cozy indoors", "winter birds", "seasonal charm"]},
    {"genre": "Suburban Dusk", "keywords": ["subdued colors", "streetlights flickering on", "families outdoors", "calm environment", "front porches", "kids playing", "scent of dinner", "long shadows", "neighborhood feel", "peaceful transition"]},
    {"genre": "Jungle Noon", "keywords": ["thick greenery", "humid air", "sun filtering through canopy", "exotic wildlife", "chirping insects", "hidden streams", "dense foliage", "mystical", "ancient vibes", "exploration"]},
    {"genre": "Lake at Twilight", "keywords": ["calm waters", "purple sky", "ripples", "reflective mood", "cool breeze", "stars beginning to appear", "silence", "boats moored", "natural beauty", "tranquil"]},
    {"genre": "Farm in Early Morning", "keywords": ["rooster crowing", "dew on grass", "farm animals", "tractors starting", "sunrise over fields", "freshly plowed earth", "barn activity", "simple life", "birds in flight", "serenity"]},
    {"genre": "Park in Autumn Afternoon", "keywords": ["falling leaves", "orange and yellow tones", "crisp air", "people walking dogs", "children playing", "benches occupied", "clear skies", "seasonal beauty", "rustling leaves", "cozy atmosphere"]},
    {"genre": "Seaside Storm", "keywords": ["crashing waves", "dark clouds", "thunder rumbling", "windswept", "dramatic", "salt spray", "turbulent waters", "isolated", "raw power", "nature's wrath"]},
    {"genre": "Meadow at Midnight", "keywords": ["starlit sky", "fireflies", "moonlit grass", "cool breeze", "nocturnal sounds", "solitude", "peaceful", "gentle sway", "mystical atmosphere", "nighttime calm"]},
    {"genre": "Urban Rooftop Morning", "keywords": ["sunrise view", "birds flying", "chimneys", "distant city sounds", "quiet before rush hour", "clear sky", "refreshing", "expansive skyline", "urban serenity", "modern living"]},
    {"genre": "Busy Market Afternoon", "keywords": ["vendors shouting", "colorful stalls", "crowded paths", "scent of food", "bargaining", "lively", "cultural diversity", "sun overhead", "bustling", "community spirit"]},
    {"genre": "Cliffside Sunset", "keywords": ["majestic views", "warm colors", "distant ocean", "birds soaring", "natural wonder", "windy", "dramatic", "romantic", "horizon fading", "peaceful end"]},
    {"genre": "Night Train Journey", "keywords": ["dim lights", "rattling sound", "scenery in darkness", "quiet passengers", "motion", "whistle blowing", "traveling through time", "mystery", "interior warmth", "nostalgia"]},    
    {"genre": "Creation of the World", "keywords": ["Genesis", "Adam and Eve", "Garden of Eden", "creation story", "beginning of time", "seven days", "God's creation", "original sin", "serpent", "fall of man"]},
    {"genre": "The Great Flood", "keywords": ["Noah's Ark", "worldwide flood", "divine judgment", "covenant with Noah", "animals two by two", "rainbow promise", "salvation", "obedience to God", "ark construction", "renewed earth"]},
    {"genre": "Tower of Babel", "keywords": ["Genesis", "human pride", "language confusion", "scattered nations", "divine intervention", "Babylon", "tower construction", "unity in disobedience", "divine judgment", "ancient history"]},
    {"genre": "Exodus and Parting of the Red Sea", "keywords": ["Moses", "Israelite freedom", "Pharaoh", "divine miracles", "plagues of Egypt", "Exodus", "parting waters", "God's guidance", "pillar of fire", "Mount Sinai"]},
    {"genre": "Ten Commandments", "keywords": ["Moses", "Mount Sinai", "God's law", "moral code", "tablets of stone", "Israelite covenant", "Old Testament laws", "divine guidance", "obedience", "ethical teachings"]},
    {"genre": "David and Goliath", "keywords": ["1 Samuel", "shepherd boy", "giant slayer", "faith in God", "Israel vs Philistines", "sling and stone", "courage", "King David", "divine victory", "trust in God"]},
    {"genre": "Birth of Jesus", "keywords": ["Nativity story", "Bethlehem", "Mary and Joseph", "virgin birth", "manger", "Christmas", "shepherds", "angelic proclamation", "Messiah", "New Testament"]},
    {"genre": "Jesus' Baptism", "keywords": ["John the Baptist", "Jordan River", "dove", "Holy Spirit", "heavenly voice", "beginning of ministry", "repentance", "Messiah revealed", "obedience", "New Testament"]},
    {"genre": "Sermon on the Mount", "keywords": ["Beatitudes", "teachings of Jesus", "New Testament ethics", "divine wisdom", "love and forgiveness", "Kingdom of Heaven", "Christian morality", "Matthew 5-7", "spiritual guidance", "discipleship"]},
    {"genre": "Last Supper", "keywords": ["Jesus' disciples", "Passover meal", "bread and wine", "Eucharist", "betrayal foretold", "Judas Iscariot", "New Covenant", "Christian tradition", "final teachings", "Gethsemane"]},
    {"genre": "Crucifixion of Jesus", "keywords": ["Golgotha", "sacrifice for sins", "Roman execution", "Jesus' death", "atonement", "New Testament", "crown of thorns", "Good Friday", "salvation", "divine love"]},
    {"genre": "Resurrection of Jesus", "keywords": ["empty tomb", "Easter", "divine victory", "new life", "disciples' faith", "angelic announcement", "Messiah risen", "Christian hope", "triumph over death", "eternal life"]},
    {"genre": "Day of Pentecost", "keywords": ["Acts 2", "Holy Spirit", "tongues of fire", "apostles' empowerment", "early church", "speaking in tongues", "divine outpouring", "spiritual awakening", "New Testament", "Christian mission"]},
    {"genre": "Revelation's Seven Seals", "keywords": ["John's vision", "apocalyptic prophecy", "horsemen", "divine judgment", "scroll", "end times", "tribulation", "heavenly throne", "eschatology", "Revelation 6"]},
    {"genre": "The Trumpets", "keywords": ["Revelation 8-11", "divine warnings", "cosmic destruction", "angels", "apocalyptic events", "plagues", "judgment", "symbolism", "New Testament", "final warnings"]},
    {"genre": "The Beast and the False Prophet", "keywords": ["Revelation 13", "end times", "antichrist", "deception", "spiritual warfare", "666", "apocalyptic prophecy", "divine confrontation", "faith under trial", "symbolic imagery"]},
    {"genre": "The Bowls of Wrath", "keywords": ["Revelation 16", "final judgments", "plagues", "divine anger", "symbolic actions", "cosmic events", "apocalyptic prophecy", "tribulation", "New Testament", "end of days"]},
    {"genre": "The New Heaven and New Earth", "keywords": ["Revelation 21", "eternal kingdom", "God's dwelling", "divine promise", "perfect peace", "no more death", "heavenly city", "eschatology", "eternal joy", "New Jerusalem"]},
    {"genre": "Final Battle", "keywords": ["Revelation 19", "Armageddon", "divine triumph", "Satan's defeat", "cosmic conflict", "heavenly army", "end times", "symbolic imagery", "faithful victory", "eschatological hope"]},
    {"genre": "Eternal Reign of Christ", "keywords": ["Revelation 22", "throne of God", "eternal life", "perfect justice", "divine love", "heavenly presence", "paradise restored", "Christian hope", "eschatological promise", "spiritual fulfillment"]},    
    {"genre": "Christianity", "keywords": ["Jesus' birth", "Crucifixion and Resurrection", "Holy Bible", "Ten Commandments", "Last Supper", "Christmas", "Easter", "Trinity", "Sermon on the Mount", "Day of Pentecost"]},
    {"genre": "Islam", "keywords": ["Quran revelation", "Five Pillars", "Prophet Muhammad", "Hajj pilgrimage", "Ramadan fasting", "Eid celebrations", "Mecca and Medina", "Shahada", "daily prayers", "Hijra"]},
    {"genre": "Judaism", "keywords": ["Torah", "Exodus from Egypt", "Ten Commandments", "Passover", "Yom Kippur", "Sabbath observance", "Hanukkah", "Abrahamic covenant", "Temple in Jerusalem", "Bar/Bat Mitzvah"]},
    {"genre": "Hinduism", "keywords": ["Bhagavad Gita", "Ramayana and Mahabharata", "karma and dharma", "Diwali festival", "Holi celebration", "worship of deities", "Yoga and meditation", "pilgrimage to Varanasi", "Ganesh Chaturthi", "Trimurti (Brahma, Vishnu, Shiva)"]},
    {"genre": "Buddhism", "keywords": ["Four Noble Truths", "Eightfold Path", "Buddha's enlightenment", "meditation practices", "nirvana", "Vesak festival", "Lotus Sutra", "Bodhi Tree", "monastic life", "Dharma teachings"]},
    {"genre": "Sikhism", "keywords": ["Guru Nanak's teachings", "Guru Granth Sahib", "Golden Temple", "five Ks", "Langar community kitchen", "Amrit Ceremony", "Vaisakhi festival", "Kirtan devotional singing", "equality and service", "Khalsa tradition"]},
    {"genre": "Taoism", "keywords": ["Tao Te Ching", "Laozi", "Yin-Yang balance", "Wu Wei philosophy", "Qi energy", "Feng Shui", "longevity practices", "Tai Chi", "natural harmony", "Taoist rituals"]},
    {"genre": "Shinto", "keywords": ["kami spirits", "Torii gates", "shrines", "purification rituals", "Matsuri festivals", "Amaterasu", "ancestor worship", "seasonal ceremonies", "nature reverence", "Shinto mythology"]},
    {"genre": "Confucianism", "keywords": ["Analects of Confucius", "filial piety", "moral integrity", "ritual propriety", "scholar-officials", "harmony in relationships", "ancestor veneration", "Confucian education", "social harmony", "Confucian temples"]},
    {"genre": "Zoroastrianism", "keywords": ["Avesta scriptures", "Ahura Mazda", "fire temples", "dualism of good and evil", "Nowruz festival", "Zarathustra's teachings", "tower of silence", "Faravahar symbol", "eternal flame", "moral righteousness"]},
    {"genre": "Jainism", "keywords": ["Ahimsa (non-violence)", "Tirthankaras", "karma purification", "Sallekhana fasting", "Jain scriptures", "meditation and asceticism", "Paryushana festival", "monastic life", "vegetarianism", "spiritual liberation"]},
    {"genre": "Bahá'í Faith", "keywords": ["Bahá'u'lláh", "unity of religions", "progressive revelation", "Nine-pointed star", "Shrine of the Báb", "Ridván festival", "prayer and meditation", "social equality", "education for all", "world peace"]},
    {"genre": "Paganism", "keywords": ["nature worship", "Wheel of the Year", "Sabbats and Esbats", "ritual magic", "polytheism", "ancestor veneration", "witchcraft", "Druids and Wiccans", "solstice festivals", "divination"]},
    {"genre": "Indigenous Religions", "keywords": ["shamanism", "animism", "ritual dances", "sacred ceremonies", "oral traditions", "connection to nature", "ancestor spirits", "vision quests", "healing rituals", "tribal customs"]},
    {"genre": "Ancient Egyptian Religion", "keywords": ["Book of the Dead", "Ra, the Sun God", "mummification", "pyramids", "afterlife beliefs", "pharaohs as deities", "Anubis", "Isis and Osiris", "temple rituals", "hieroglyphs"]},
    {"genre": "Greco-Roman Religion", "keywords": ["Olympian gods", "Zeus and Hera", "mythology", "oracles and temples", "sacrifices", "heroic tales", "festivals", "Dionysian rites", "Roman pantheon", "legacy in Western culture"]},
    {"genre": "Norse Religion", "keywords": ["Odin and Thor", "Valhalla", "Yggdrasil", "Viking rituals", "sagas and Eddas", "Freyja", "Ragnarök", "runic inscriptions", "blot ceremonies", "sacred groves"]},
    {"genre": "Wicca", "keywords": ["Goddess and God worship", "ritual magic", "Wiccan Rede", "Samhain festival", "pentacle symbol", "nature-based spirituality", "coven practices", "herbal magic", "divination tools", "ritual circles"]},
    {"genre": "Modern Spiritualism", "keywords": ["mediumship", "afterlife communication", "seances", "spirit guides", "psychic phenomena", "healing practices", "spiritual growth", "astral projection", "reincarnation beliefs", "meditation"]},
    {"genre": "Atheism/Agnosticism", "keywords": ["absence of religion", "secular philosophy", "critical thinking", "agnostic uncertainty", "humanism", "scientific worldview", "rational ethics", "freedom from dogma", "logical reasoning", "moral values"]},
    {"genre": "Catholicism", "keywords": ["Holy Mass", "Vatican City", "Pope", "Rosary prayers", "Seven Sacraments", "Eucharist", "Saints", "Crucifix", "Confession", "Holy Bible"]},    
    {"genre": "Cabin", "keywords": ["rustic", "wooden", "forest retreat", "small", "cozy", "traditional", "handmade", "simple design", "nature", "off-grid"]},
    {"genre": "Cottage", "keywords": ["country home", "charming", "quaint", "garden", "rural", "cozy", "small-scale", "stone walls", "traditional", "picturesque"]},
    {"genre": "Log Cabin", "keywords": ["wooden structure", "forest", "nature", "simple design", "handcrafted", "rustic", "outdoor living", "self-sufficient", "warm", "traditional"]},
    {"genre": "Tiny House", "keywords": ["compact", "minimalist", "modern design", "eco-friendly", "mobile", "affordable", "smart storage", "efficient", "portable", "off-grid"]},
    {"genre": "Treehouse", "keywords": ["elevated", "nature", "playful", "unique", "wooden", "forest", "adventurous", "cozy", "off-ground", "custom design"]},
    {"genre": "Beach House", "keywords": ["coastal", "oceanfront", "relaxing", "modern", "vacation", "airy", "water view", "sunlit", "tropical", "luxurious"]},
    {"genre": "Farmhouse", "keywords": ["rural", "agriculture", "rustic charm", "traditional", "large", "family-oriented", "porch", "country living", "stone or wood", "cozy"]},
    {"genre": "Modern Villa", "keywords": ["luxurious", "spacious", "modern architecture", "large windows", "pool", "open-plan", "minimalist", "high-tech", "urban", "stylish"]},
    {"genre": "Skyscraper", "keywords": ["urban", "modern", "high-rise", "business", "glass and steel", "large scale", "luxury apartments", "office building", "innovative", "cityscape"]},
    {"genre": "Bungalow", "keywords": ["single-story", "compact", "traditional", "cozy", "porch", "rural", "family-oriented", "garden", "affordable", "simple design"]},
    {"genre": "Igloo", "keywords": ["Arctic", "snow", "ice house", "cold climate", "traditional", "insulated", "unique", "small", "circular", "temporary"]},
    {"genre": "Yurt", "keywords": ["nomadic", "Mongolian", "circular", "portable", "simple", "cozy", "tent-like", "eco-friendly", "wooden frame", "traditional"]},
    {"genre": "A-Frame House", "keywords": ["triangular design", "modern", "vacation home", "efficient", "compact", "rustic", "cozy", "nature", "unique", "slanted roof"]},
    {"genre": "Castle", "keywords": ["medieval", "stone walls", "historic", "fortress", "grand", "towers", "luxurious", "royalty", "ornate", "heritage"]},
    {"genre": "Apartment Complex", "keywords": ["urban", "multi-family", "modern", "convenient", "compact living", "shared amenities", "affordable", "high-rise", "city life", "community"]},
    {"genre": "Mobile Home", "keywords": ["portable", "compact", "affordable", "self-contained", "eco-friendly", "efficient", "modern design", "trailer park", "simple", "family"]},
    {"genre": "Tent", "keywords": ["camping", "portable", "outdoor", "temporary", "lightweight", "simple", "eco-friendly", "fabric", "adventure", "easy setup"]},
    {"genre": "Ranch House", "keywords": ["rural", "large", "spacious", "family-oriented", "flat design", "traditional", "porch", "cattle farm", "rustic", "nature"]},
    {"genre": "Penthouse", "keywords": ["luxurious", "high-rise", "urban", "modern", "city view", "spacious", "exclusive", "private terrace", "stylish", "expensive"]},
    {"genre": "Shipping Container Home", "keywords": ["modern", "recycled", "eco-friendly", "compact", "industrial design", "affordable", "modular", "innovative", "urban", "portable"]},
    {"genre": "Geodesic Dome", "keywords": ["futuristic", "eco-friendly", "spherical", "strong structure", "modern design", "unique", "lightweight", "efficient", "nature", "innovative"]},
    {"genre": "Earthship", "keywords": ["self-sufficient", "eco-friendly", "sustainable", "off-grid", "natural materials", "solar power", "modern design", "recycled materials", "unique", "efficient"]},
    {"genre": "Mansion", "keywords": ["luxurious", "grand", "spacious", "expensive", "modern design", "heritage", "exclusive", "high-class", "urban", "stylish"]},
    {"genre": "Underground Bunker", "keywords": ["survival", "hidden", "secure", "off-grid", "eco-friendly", "unique", "reinforced", "disaster-proof", "military-grade", "efficient"]},
    {"genre": "Floating House", "keywords": ["waterfront", "unique", "modern design", "compact", "eco-friendly", "lightweight", "vacation", "nature", "innovative", "sustainable"]},
    {"genre": "School Building", "keywords": ["educational", "multi-purpose", "urban", "community", "modern", "functional", "spacious", "shared use", "durable", "affordable"]},
    {"genre": "Lighthouse", "keywords": ["coastal", "unique", "historic", "guiding light", "stone structure", "tall", "oceanfront", "functional", "nautical", "picturesque"]},
    {"genre": "Chalet", "keywords": ["mountain retreat", "wooden", "cozy", "rustic", "vacation", "nature", "alpine style", "family-oriented", "relaxing", "warm"]},
    {"genre": "Dome Tent", "keywords": ["modern camping", "lightweight", "portable", "unique", "temporary", "eco-friendly", "compact", "nature", "easy setup", "adventure"]},       
    {"genre": "Ballistic Vest", "keywords": ["bulletproof", "modern armor", "Kevlar", "tactical gear", "law enforcement", "military use", "lightweight", "impact-resistant", "urban combat", "body armor"]},
    {"genre": "Full Body Armor", "keywords": ["heavy armor", "military gear", "bulletproof", "combat zones", "explosive protection", "full coverage", "reinforced plates", "tactical", "durable", "high-tech"]},
    {"genre": "Riot Gear", "keywords": ["crowd control", "anti-riot", "law enforcement", "impact-resistant", "lightweight", "shock absorbent", "modern", "urban use", "polycarbonate", "police"]},
    {"genre": "EOD Suit", "keywords": ["explosive ordnance disposal", "bomb squad", "blast-resistant", "military use", "high-tech", "heavy protection", "shock absorbent", "heat-resistant", "helmet", "tactical"]},
    {"genre": "Tactical Helmet", "keywords": ["head protection", "bulletproof", "military grade", "lightweight", "modern design", "impact-resistant", "urban combat", "tactical gear", "law enforcement", "camera mount"]},
    {"genre": "Shielded Bunker", "keywords": ["defensive structure", "portable bunker", "military use", "high-tech", "modular", "reinforced", "urban warfare", "bulletproof", "blast-resistant", "field shelter"]},
    {"genre": "Ballistic Mask", "keywords": ["face protection", "law enforcement", "lightweight", "bulletproof", "riot control", "tactical gear", "impact-resistant", "military use", "modern design", "compact"]},
    {"genre": "Anti-Stab Vest", "keywords": ["knife-resistant", "law enforcement", "lightweight", "urban safety", "body armor", "close combat", "modern", "Kevlar", "durable", "compact"]},
    {"genre": "Combat Gloves", "keywords": ["hand protection", "Kevlar", "military use", "law enforcement", "lightweight", "impact-resistant", "close combat", "modern", "fireproof", "reinforced knuckles"]},
    {"genre": "Thigh Guards", "keywords": ["leg protection", "Kevlar", "modern armor", "military use", "lightweight", "impact-resistant", "urban combat", "law enforcement", "tactical gear", "durable"]},
    {"genre": "Tactical Shield", "keywords": ["handheld protection", "law enforcement", "bulletproof", "riot control", "polycarbonate", "urban use", "impact-resistant", "lightweight", "military use", "high-tech"]},
    {"genre": "Armored Vehicle", "keywords": ["vehicle protection", "bulletproof", "military transport", "law enforcement", "urban combat", "explosion-resistant", "high-tech", "modular design", "tactical use", "field deployment"]},
    {"genre": "Blast Plate", "keywords": ["explosive protection", "Kevlar", "military use", "law enforcement", "heavy-duty", "impact-resistant", "reinforced armor", "modern gear", "durable", "compact"]},
    {"genre": "Ghillie Suit", "keywords": ["camouflage", "military use", "sniper gear", "tactical advantage", "lightweight", "concealment", "forest combat", "stealthy", "modern design", "effective"]},
    {"genre": "Neck Guard", "keywords": ["Kevlar", "modern armor", "military use", "law enforcement", "impact-resistant", "lightweight", "urban combat", "tactical gear", "small-scale", "durable"]},
    {"genre": "Flak Jacket", "keywords": ["explosive protection", "military use", "lightweight", "impact-resistant", "modern armor", "tactical gear", "urban combat", "law enforcement", "high-tech", "durable"]},
    {"genre": "Knee Pads", "keywords": ["joint protection", "tactical gear", "Kevlar", "lightweight", "military use", "law enforcement", "modern", "impact-resistant", "durable", "field use"]},
    {"genre": "Energy Barrier", "keywords": ["sci-fi shield", "force field", "urban combat", "military use", "futuristic", "portable", "energy-based", "laser-resistant", "high-tech", "tactical gear"]},
    {"genre": "Armored Boots", "keywords": ["foot protection", "Kevlar", "military use", "law enforcement", "impact-resistant", "modern design", "lightweight", "urban combat", "tactical", "durable"]},
    {"genre": "Portable Shield Generator", "keywords": ["futuristic gear", "energy barrier", "military use", "high-tech", "compact", "portable", "field deployment", "urban combat", "tactical advantage", "force field"]},
    {"genre": "Shock-Proof Suit", "keywords": ["electric resistance", "law enforcement", "military use", "modern armor", "lightweight", "tactical gear", "urban safety", "impact-resistant", "compact", "high-tech"]},
    {"genre": "Drone Defense Shield", "keywords": ["anti-drone", "military use", "law enforcement", "high-tech", "portable", "energy-based", "modern", "tactical advantage", "urban combat", "impact-resistant"]},    
    {"genre": "Round Shield", "keywords": ["wooden shield", "round shape", "medieval combat", "lightweight", "iron rim", "Viking style", "close combat", "handheld", "classic design", "simple"]},
    {"genre": "Kite Shield", "keywords": ["long shield", "pointed bottom", "medieval knight", "mounted combat", "metal reinforcements", "protection", "European style", "heraldry", "arm strap", "large surface"]},
    {"genre": "Tower Shield", "keywords": ["large shield", "full-body protection", "heavy", "defensive position", "siege combat", "rectangular", "intimidating", "reinforced edges", "cover", "bulky"]},
    {"genre": "Buckler", "keywords": ["small shield", "lightweight", "dueling", "fast movement", "close combat", "metal", "punching defense", "easy to carry", "minimal protection", "handheld"]},
    {"genre": "Pavise", "keywords": ["siege shield", "archer protection", "large shield", "full coverage", "wooden", "set on the ground", "crossbowmen", "tower shield", "painted surface", "medieval warfare"]},
    {"genre": "Scutum", "keywords": ["Roman shield", "large rectangular", "curved shape", "legionnaire", "defensive formations", "metal boss", "iron rim", "tortoise formation", "historical", "arm strap"]},
    {"genre": "Heater Shield", "keywords": ["knight shield", "triangular shape", "heraldry", "tournament use", "horseback combat", "lightweight", "stylish design", "personalized emblem", "medieval", "battle-tested"]},
    {"genre": "Riot Shield", "keywords": ["modern shield", "police use", "transparent", "polycarbonate", "crowd control", "anti-riot", "lightweight", "bullet-resistant", "urban use", "law enforcement"]},
    {"genre": "Ballistic Shield", "keywords": ["tactical shield", "military use", "bulletproof", "SWAT teams", "reinforced steel", "urban combat", "small arms protection", "portable", "viewing window", "high-tech"]},
    {"genre": "Improvised Shield", "keywords": ["makeshift protection", "DIY", "emergency use", "wood", "metal sheet", "plastic", "protest use", "quick assembly", "unorthodox", "temporary"]},
    {"genre": "Targe", "keywords": ["Scottish shield", "small round", "wooden core", "iron reinforcements", "decorative studs", "hand-to-hand combat", "clansman weapon", "lightweight", "traditional", "heritage"]},
    {"genre": "Body Shield", "keywords": ["large protective gear", "riot control", "tactical use", "lightweight composite", "crowd dispersal", "non-lethal force", "operator use", "impact-resistant", "modern", "urban scenarios"]},
    {"genre": "Arm Shield", "keywords": ["forearm protection", "small shield", "lightweight", "close combat", "custom fit", "arm strap", "deflect blows", "personalized", "stealthy", "dueling"]},
    {"genre": "Spiked Shield", "keywords": ["offensive shield", "weaponized", "combat use", "iron spikes", "handheld", "dual purpose", "intimidating", "bladed edges", "heavy", "reinforced"]},
    {"genre": "Magic Shield", "keywords": ["fantasy item", "energy barrier", "spell casting", "arcane protection", "glowing", "mystical", "legendary", "lightweight", "unbreakable", "otherworldly"]},
    {"genre": "Energy Shield", "keywords": ["sci-fi shield", "force field", "high-tech", "plasma protection", "laser deflection", "transparent barrier", "compact", "portable", "futuristic", "power source"]},
    {"genre": "Carapace Shield", "keywords": ["natural material", "beast defense", "insect shell", "primitive design", "tribal use", "organic", "curved shape", "lightweight", "durable", "prehistoric"]},
    {"genre": "Captain's Shield", "keywords": ["fictional design", "circular shield", "throwing weapon", "vibranium", "patriotic", "red and blue", "combat ready", "stylized", "iconic", "unbreakable"]},
    {"genre": "Adarga", "keywords": ["Spanish shield", "leather construction", "oval shape", "lightweight", "dueling", "historical", "decorative", "traditional", "arm strap", "durable"]},
    {"genre": "Steel Shield", "keywords": ["metal shield", "heavy", "sturdy", "combat use", "reinforced edges", "durable", "classic design", "intimidating", "medieval era", "battle-tested"]},
    {"genre": "Leather Shield", "keywords": ["lightweight", "flexible", "primitive design", "handcrafted", "tribal use", "small size", "simple protection", "easy to carry", "customizable", "historical"]},
    {"genre": "Aegis", "keywords": ["mythical shield", "divine protection", "Greek mythology", "Medusa emblem", "impenetrable", "legendary", "decorative", "immortal", "combat ready", "heritage"]},
    {"genre": "War Shield", "keywords": ["tribal shield", "decorative", "handmade", "battle use", "large surface", "painted symbols", "ritualistic", "arm strap", "lightweight", "durable"]},
    {"genre": "Hexagonal Shield", "keywords": ["modern design", "geometric", "stylish", "lightweight", "unique shape", "tactical use", "close combat", "custom fit", "portable", "deflective"]},
    {"genre": "Spartan Shield", "keywords": ["Greek hoplite", "bronze material", "round design", "phalanx combat", "arm strap", "reinforced rim", "intimidating", "decorative", "battle-tested", "lightweight"]},
    {"genre": "Ceremonial Shield", "keywords": ["decorative", "ritual use", "ornate", "gold details", "historical", "symbolic", "non-combat", "handcrafted", "prestigious", "traditional"]},
    {"genre": "Wooden Shield", "keywords": ["basic design", "lightweight", "cheap", "easy to craft", "historical", "primitive", "large surface", "painted decoration", "handheld", "battle-ready"]},
    {"genre": "Deflector Shield", "keywords": ["space combat", "high-tech", "energy-based", "force field", "alien technology", "durable", "power source", "compact design", "protection", "sci-fi"]},    
    {"genre": "Doing Action Sword Swing", "keywords": ["slashing", "quick motion", "aggressive", "blade", "combat", "close range", "swiftness", "precision", "martial", "action"]},
    {"genre": "Doing Action Knife Throw", "keywords": ["sharp", "targeting", "precision", "quick throw", "motion blur", "dangerous", "lethal", "attack", "throwing", "speed"]},
    {"genre": "Doing Action Machete Swing", "keywords": ["wide arc", "strong blow", "close combat", "bladed weapon", "swung force", "dangerous", "quick attack", "destructive", "rural", "survival"]},
    {"genre": "Doing Action Fencing Thrust", "keywords": ["precision", "swordplay", "quick strike", "pointed tip", "duel", "elegant", "defensive", "sparring", "fencing", "athletic"]},
    {"genre": "Doing Action Axe Strike", "keywords": ["heavy blow", "close combat", "powerful", "cleaving", "wood chopping", "muscle", "weapon", "destructive", "impact", "force"]},
    {"genre": "Doing Action Pistol Shooting", "keywords": ["quick draw", "targeting", "firearm", "precise", "combat", "short-range", "aggressive", "gunfire", "action", "close-range"]},
    {"genre": "Doing Action Pointing Gun", "keywords": ["aiming", "focused", "dangerous", "tension", "intense", "reaction", "gun barrel", "targeting", "action", "dramatic"]},
    {"genre": "Doing Action Automatic Gunfire", "keywords": ["rapid shots", "suppressive fire", "controlled bursts", "explosive", "combat", "intense", "military", "close quarters", "action", "chaos"]},
    {"genre": "Doing Action Reloading Firearm", "keywords": ["quick reload", "combat preparation", "gun mechanics", "action", "tactical", "realism", "gun handling", "rapid", "dangerous", "efficiency"]},
    {"genre": "Doing Action Shotgun Blast", "keywords": ["close-range", "wide spread", "explosive", "impact", "combat", "intense", "force", "boom", "quick action", "dangerous"]},
    {"genre": "Doing Action Punch", "keywords": ["quick strike", "fist", "aggressive", "close combat", "hit", "force", "fight", "self-defense", "tension", "speed"]},
    {"genre": "Doing Action Kick", "keywords": ["high kick", "impact", "aggressive", "defensive", "martial arts", "strong blow", "quick strike", "combat", "action", "power"]},
    {"genre": "Doing Action Elbow Strike", "keywords": ["close range", "quick motion", "force", "aggressive", "martial arts", "combat", "self-defense", "elbow", "impact", "brutal"]},
    {"genre": "Doing Action Judo Throw", "keywords": ["quick throw", "leverage", "combat", "martial arts", "defensive", "takedown", "agility", "momentum", "balance", "fluid"]},
    {"genre": "Doing Action Chokehold", "keywords": ["strangling", "close combat", "suffocation", "defensive", "submission", "pressure", "quick action", "grip", "intense", "dangerous"]},
    {"genre": "Doing Action Ducking", "keywords": ["quick reaction", "evade", "low movement", "defensive", "agility", "combat", "avoiding", "strike", "deflect", "action"]},
    {"genre": "Doing Action Dodge", "keywords": ["evading", "quick move", "combat", "agility", "avoidance", "dangerous", "defensive", "reaction", "action", "aggressive"]},
    {"genre": "Doing Action Blocking", "keywords": ["parrying", "defensive", "martial arts", "weapon blocking", "strike protection", "reaction", "quick defense", "impact", "movement", "tactical"]},
    {"genre": "Doing Action Rolling Away", "keywords": ["evade", "combat", "reaction", "escape", "defensive", "roll", "action", "dodging", "quick movement", "agility"]},
    {"genre": "Doing Action Shield Block", "keywords": ["defensive", "blocking", "shield", "impact absorption", "protective", "combat", "tactical", "deflecting", "quick action", "armor"]},
    {"genre": "Doing Action Spin Kick", "keywords": ["martial arts", "acrobatics", "high impact", "dynamic", "kick", "spin", "quick movement", "action", "aggressive", "fast"]},
    {"genre": "Doing Action Uppercut", "keywords": ["powerful punch", "close combat", "quick strike", "aggressive", "martial arts", "fist", "momentum", "action", "combative", "impact"]},
    {"genre": "Doing Action Stab", "keywords": ["knife", "quick attack", "close-range", "precision", "targeting", "aggressive", "combat", "dangerous", "weapon", "thrust"]},
    {"genre": "Doing Action Body Slam", "keywords": ["wrestling", "impact", "force", "slam", "close combat", "strength", "violent", "quick action", "takedown", "tactical"]},
    {"genre": "Doing Action Chopping", "keywords": ["axe", "quick strike", "weapon", "strong blow", "impact", "force", "combat", "action", "defense", "destructive"]},
    {"genre": "Doing Action Team Attack", "keywords": ["coordinated", "group effort", "action", "teamwork", "combat", "precision", "quick strike", "multitarget", "aggressive", "powerful"]},
    {"genre": "Doing Action Flanking", "keywords": ["tactical", "combat", "surprise", "quick action", "side attack", "coordinated", "aggressive", "defensive", "maneuver", "team"]},
    {"genre": "Doing Action Ambush", "keywords": ["sudden attack", "trap", "stealth", "aggressive", "quick strike", "group action", "surprise", "combat", "violent", "dangerous"]},
    {"genre": "Doing Action Grenade Throw", "keywords": ["explosive", "rapid", "throw", "combat", "dangerous", "area attack", "impact", "explosion", "tactical", "action"]},
    {"genre": "Doing Action Fire Support", "keywords": ["suppression", "covering fire", "tactical", "gunfire", "action", "group effort", "combat", "defensive", "military", "quick strike"]},    
    {"genre": "Emotion face Happiness", "keywords": ["joy", "delight", "contentment", "cheerful", "euphoria", "elation", "laughter", "smiling", "excitement", "grateful"]},
    {"genre": "Emotion face Sadness", "keywords": ["grief", "sorrow", "melancholy", "tears", "disappointment", "loss", "longing", "despair", "heartbroken", "regret"]},
    {"genre": "Emotion face Anger", "keywords": ["rage", "frustration", "fury", "irritation", "annoyance", "resentment", "hostility", "outrage", "wrath", "aggression"]},
    {"genre": "Emotion face Fear", "keywords": ["anxiety", "terror", "panic", "dread", "worry", "nervousness", "nausea", "unease", "tension", "paranoia"]},
    {"genre": "Emotion face Surprise", "keywords": ["shock", "amazement", "astonishment", "startle", "awe", "unexpected", "disbelief", "wonder", "confusion", "curiosity"]},
    {"genre": "Emotion face Disgust", "keywords": ["revulsion", "contempt", "aversion", "dislike", "repulsion", "distaste", "sickened", "offended", "nausea", "abhorrence"]},
    {"genre": "Emotion face Love", "keywords": ["affection", "romance", "passion", "desire", "compassion", "caring", "intimacy", "fondness", "devotion", "attachment"]},
    {"genre": "Emotion face Confusion", "keywords": ["bewilderment", "perplexity", "uncertainty", "puzzlement", "lost", "incomprehension", "disorientation", "mystification", "doubt", "curiosity"]},
    {"genre": "Emotion face Pride", "keywords": ["self-esteem", "satisfaction", "accomplishment", "ego", "dignity", "honor", "confidence", "self-worth", "arrogance", "achievement"]},
    {"genre": "Emotion face Shame", "keywords": ["embarrassment", "humiliation", "guilt", "regret", "disgrace", "self-consciousness", "mortification", "unworthiness", "remorse", "reproach"]},
    {"genre": "Emotion face Hope", "keywords": ["optimism", "aspiration", "faith", "expectation", "desire", "dreams", "ambition", "positivity", "trust", "looking forward"]},
    {"genre": "Emotion face Gratitude", "keywords": ["thankfulness", "appreciation", "recognition", "thankful", "obligation", "sincerity", "gratefulness", "respect", "observation", "acknowledgment"]},
    {"genre": "Emotion face Guilt", "keywords": ["remorse", "accountability", "contrition", "repentance", "regret", "penitence", "shame", "moral conflict", "blame", "inner turmoil"]},
    {"genre": "Emotion face Calmness", "keywords": ["relaxation", "peace", "serenity", "tranquility", "composure", "stillness", "soothing", "balance", "quietness", "ease"]},
    {"genre": "Emotion face Jealousy", "keywords": ["envy", "covetousness", "resentment", "spite", "rivalry", "suspicion", "competition", "desire", "insecurity", "bitterness"]},
    {"genre": "Emotion face Enthusiasm", "keywords": ["eagerness", "excitement", "passion", "interest", "joyful", "vigor", "energy", "anticipation", "zest", "fervor"]},
    {"genre": "Emotion face Boredom", "keywords": ["disinterest", "lack of motivation", "tedium", "listlessness", "restlessness", "dullness", "monotony", "unfulfilled", "lack of engagement", "disengagement"]},
    {"genre": "Emotion face Relief", "keywords": ["release", "peace of mind", "comfort", "solace", "ease", "calmness", "respite", "resolution", "satisfaction", "freedom"]},
    {"genre": "Emotion face Apathy", "keywords": ["indifference", "disengagement", "detachment", "lack of care", "emotionless", "coldness", "uncaring", "numbness", "unconcerned", "unmoved"]},
    {"genre": "Emotion face Loneliness", "keywords": ["isolation", "solitude", "emptiness", "rejection", "desolation", "detachment", "abandonment", "self-reflection", "separation", "longing"]},
    {"genre": "Emotion face Compassion", "keywords": ["empathy", "sympathy", "understanding", "care", "kindness", "love", "concern", "support", "charity", "altruism"]},    
    {"genre": "Action actor Standing", "keywords": ["upright", "stable", "neutral", "alert", "assertive", "vigilant", "balance", "active", "attention", "defensive"]},
    {"genre": "Action actor Sitting", "keywords": ["relaxed", "resting", "casual", "grounded", "comfortable", "intimate", "facing forward", "lounge", "focused", "reflective"]},
    {"genre": "Action actor Kneeling", "keywords": ["submission", "respect", "prayer", "grounded", "humility", "focus", "formal", "meditative", "worship", "submission"]},
    {"genre": "Action actor Crouching", "keywords": ["stealth", "low position", "agility", "quick movement", "defensive", "preparedness", "combat stance", "balance", "hiding", "motion"]},
    {"genre": "Action actor Lying Down", "keywords": ["relaxed", "rest", "comfort", "sleeping", "horizontal", "resting", "prone", "repose", "vulnerable", "inactive"]},
    {"genre": "Action actor Prone", "keywords": ["face down", "vulnerable", "resting", "low profile", "repose", "defensive", "combat", "hidden", "action", "neutral"]},
    {"genre": "Action actor Supine", "keywords": ["lying on back", "rest", "relaxation", "comfortable", "resting", "recovery", "defensive", "vulnerable", "non-threatening", "sleeping"]},
    {"genre": "Action actor Reclining", "keywords": ["relaxed", "casual", "lounging", "semi-resting", "comfortable", "repose", "informal", "leisure", "lazy", "half-sitting"]},
    {"genre": "Action actor Squatting", "keywords": ["low position", "agility", "preparation", "focus", "stealth", "combat-ready", "flexibility", "alert", "intense", "balance"]},
    {"genre": "Action actor Lunging", "keywords": ["forward movement", "powerful", "aggressive", "action", "combat", "motion", "athletic", "quick strike", "leaning forward", "strike"]},
    {"genre": "Action actor Stretching", "keywords": ["reaching", "flexibility", "preparation", "relaxation", "movement", "warm-up", "slow motion", "release", "comfort", "recovery"]},
    {"genre": "Action actor Leaning", "keywords": ["relaxed", "casual", "support", "comfortable", "resting", "waiting", "slouch", "informal", "laziness", "positioned"]},
    {"genre": "Action actor Hands Raised", "keywords": ["surrender", "defeat", "victory", "celebration", "surprise", "acknowledgement", "aggression", "defensive", "communication", "reaction"]},
    {"genre": "Action actor Crossed Arms", "keywords": ["defensive", "closed-off", "hostile", "thoughtful", "contemplative", "body language", "self-protection", "guarded", "unapproachable", "firm"]},
    {"genre": "Action actor Pointing", "keywords": ["direction", "command", "aggressive", "signaling", "attention", "leadership", "gesture", "order", "commanding", "dominance"]},
    {"genre": "Action actor Running", "keywords": ["movement", "speed", "motion", "agility", "action", "exercise", "fast", "escape", "adrenaline", "intense"]},
    {"genre": "Action actor Jumping", "keywords": ["leap", "dynamic", "action", "agility", "height", "quick motion", "athletic", "exercise", "escape", "jump"]},
    {"genre": "Action actor Walking", "keywords": ["casual", "leisurely", "neutral", "movement", "unhurried", "purposeful", "grounded", "focus", "simple", "steady"]},
    {"genre": "Action actor Crawling", "keywords": ["low", "stealth", "combat", "escape", "unseen", "prone", "slow", "hidden", "vulnerable", "searching"]},
    {"genre": "Action actor Twisting", "keywords": ["agility", "flexibility", "motion", "action", "dynamic", "quick movement", "rotation", "turning", "stretching", "combat"]},    
    {"genre": "Weapon Hunting Knife", "keywords": ["bladed weapon", "hunting", "survival", "outdoor use", "handmade", "sharp", "self-defense", "long blade", "durable", "illegal modification"]},
    {"genre": "Weapon Machete", "keywords": ["large blade", "chopping", "close combat", "improvised", "street weapon", "bladed weapon", "self-defense", "dangerous", "jungle survival", "rebellion"]},
    {"genre": "Weapon Combat Knife", "keywords": ["military style", "close combat", "self-defense", "reliable", "sharp", "fixed blade", "illegal weapon", "urban warfare", "dangerous", "tactical"]},
    {"genre": "Weapon Switchblade", "keywords": ["spring-loaded", "self-defense", "quick access", "illegal weapon", "street weapon", "pocket knife", "bladed weapon", "rapid deployment", "dangerous", "urban combat"]},
    {"genre": "Weapon Bowie Knife", "keywords": ["large blade", "tactical", "outdoor survival", "combat", "self-defense", "rebellion", "handmade", "illegal", "sharp", "fixed blade"]},
    {"genre": "Weapon Throwing Knife", "keywords": ["throwable weapon", "precision", "bladed weapon", "combat training", "self-defense", "reliable", "silent", "urban warfare", "dangerous", "handmade"]},
    {"genre": "Weapon Dagger", "keywords": ["short blade", "close combat", "self-defense", "tactical", "fixed blade", "stealth", "street weapon", "quick strike", "dangerous", "illegal weapon"]},
    {"genre": "Weapon Shiv", "keywords": ["homemade knife", "improvised", "street weapon", "close combat", "illegal weapon", "dangerous", "prison-made", "makeshift", "small blade", "self-defense"]},
    {"genre": "Weapon Karambit", "keywords": ["curved blade", "self-defense", "combat knife", "street weapon", "bladed weapon", "close combat", "illegal", "dangerous", "handmade", "tactical"]},
    {"genre": "Weapon Fixed Blade Knife", "keywords": ["durable", "self-defense", "combat", "hunting", "sharp", "long blade", "illegal weapon", "rebellion", "survival", "urban combat"]},
    {"genre": "Weapon Sword", "keywords": ["sharp blade", "ancient weapon", "combat", "long sword", "katana", "double-edged", "tactical blade", "medieval sword", "honor", "warrior"]},
    {"genre": "Weapon Bow", "keywords": ["longbow", "archery", "quiver", "arrows", "precision", "range", "silent weapon", "hunter", "string tension", "wooden bow"]},
    {"genre": "Weapon Gun", "keywords": ["firearm", "handgun", "revolver", "semi-automatic", "shotgun", "rifle", "pistol", "suppressor", "combat weapon", "ammunition"]},
    {"genre": "Weapon Axe", "keywords": ["battle axe", "chopping", "blunt force", "heavy weapon", "dual-headed", "cleaving", "woodcutter", "viking axe", "war axe", "brutal"]},
    {"genre": "Weapon Dagger2", "keywords": ["short blade", "stealth", "throwing dagger", "assassin's weapon", "swift", "close combat", "poisoned tip", "stealth kill", "sharp edge", "concealed"]},
    {"genre": "Weapon Spear", "keywords": ["polearm", "piercing", "long reach", "battle spear", "throwing spear", "javelin", "tactical spear", "warrior", "ancient weapon", "sharp tip"]},
    {"genre": "Weapon Mace", "keywords": ["bludgeoning", "heavy weapon", "flanged mace", "spiked head", "crushing", "war hammer", "battle mace", "medieval weapon", "blunt force", "close range"]},
    {"genre": "Weapon Crossbow", "keywords": ["high velocity", "silent", "quiver", "bolt", "recurve", "tension", "precision", "archery", "silent shooter", "long-range weapon"]},
    {"genre": "Weapon Staff", "keywords": ["magic staff", "wizard weapon", "enchanted", "staff of power", "staff of light", "sorcery", "mystical weapon", "long reach", "symbol of wisdom", "arcane power"]},
    {"genre": "Weapon Flail", "keywords": ["chain weapon", "blunt force", "spiked ball", "flanged head", "agile", "war flail", "battle weapon", "medieval weapon", "impact", "close range"]},
    {"genre": "Weapon Glock", "keywords": ["pistol", "semi-automatic", "compact", "firearm", "concealed carry", "9mm", "self-defense", "police weapon", "tactical", "Glock 19"]},
    {"genre": "Weapon Beretta", "keywords": ["firearm", "handgun", "Italian design", "semi-automatic", "Beretta 92", "military", "9mm", "police", "combat pistol", "reliable"]},
    {"genre": "Weapon AK-47", "keywords": ["assault rifle", "military weapon", "gas-operated", "7.62mm", "AK platform", "reliable", "combat rifle", "tactical weapon", "Russian design", "high recoil"]},
    {"genre": "Weapon M16", "keywords": ["assault rifle", "military use", "5.56mm", "M16A4", "long-range", "semi-automatic", "combat rifle", "tactical", "US military", "reliable"]},
    {"genre": "Weapon AR-15", "keywords": ["assault rifle", "firearm", "semi-automatic", "tactical rifle", "military design", "5.56mm", "AR platform", "modular", "customizable", "self-defense"]},
    {"genre": "Weapon Remington 870", "keywords": ["shotgun", "pump-action", "tactical shotgun", "12 gauge", "hunting", "military", "law enforcement", "shotgun shell", "Remington", "combat weapon"]},
    {"genre": "Weapon Desert Eagle", "keywords": ["handgun", "semi-automatic", "magnum", "powerful recoil", "hunting pistol", "high caliber", "large frame", "military use", "heavy-duty", "Desert Eagle .50"]},
    {"genre": "Weapon Ruger", "keywords": ["firearm", "handgun", "Ruger 9mm", "reliable", "self-defense", "target shooting", "semi-automatic", "concealed carry", "compact", "tactical pistol"]},
    {"genre": "Weapon S&W (Smith & Wesson)", "keywords": ["handgun", "firearm", "revolver", "semi-automatic", "S&W Model 686", "police weapon", "tactical", "self-defense", "American-made", "law enforcement"]},
    {"genre": "Weapon Colt", "keywords": ["firearm", "revolver", "semi-automatic", "1911 pistol", "military sidearm", "American legacy", "combat pistol", "tactical", "self-defense", "Colt M1911"]},
    {"genre": "Weapon Taurus", "keywords": ["revolver", "handgun", "firearm", "Brazilian brand", "9mm", "concealed carry", "self-defense", "tactical", "semi-automatic", "reliable"]},
    {"genre": "Weapon Sig Sauer", "keywords": ["handgun", "firearm", "semi-automatic", "Sig P226", "military use", "9mm", "Swiss design", "tactical", "combat pistol", "law enforcement"]},
    {"genre": "Weapon Heckler & Koch", "keywords": ["firearm", "assault rifle", "H&K MP5", "German engineering", "military weapon", "submachine gun", "precision", "law enforcement", "9mm", "tactical weapon"]},
    {"genre": "Weapon Winchester", "keywords": ["shotgun", "rifle", "hunting", "lever-action", "model 70", "bolt-action", "reliable", "Winchester 30-30", "long-range", "outdoor use"]},
    {"genre": "Weapon Springfield Armory", "keywords": ["firearm", "1911 pistol", "semi-automatic", "combat handgun", "military sidearm", "self-defense", "target shooting", "American-made", "Springfield XD", "reliable"]},
    {"genre": "Weapon Browning", "keywords": ["shotgun", "hunting", "Browning M1911", "high-quality", "firearm", "reliable", "Belgium design", "combat weapon", "Browning Auto-5", "tactical"]},
    {"genre": "Weapon Mauser", "keywords": ["bolt-action", "rifle", "military rifle", "Mauser K98", "German engineering", "precision", "WWII", "long-range", "reliable", "classic rifle"]},
    {"genre": "Weapon CZ (Česká Zbrojovka)", "keywords": ["firearm", "handgun", "CZ 75", "semi-automatic", "Czech design", "reliable", "combat pistol", "military sidearm", "self-defense", "target shooting"]},
    {"genre": "Weapon FN Herstal", "keywords": ["assault rifle", "FN SCAR", "military weapon", "Belgium design", "precision", "combat rifle", "tactical", "special forces", "5.56mm", "reliable"]},
    {"genre": "Weapon Mossberg", "keywords": ["shotgun", "hunting shotgun", "tactical shotgun", "pump-action", "Mossberg 500", "military use", "12 gauge", "law enforcement", "reliable", "combat weapon"]},
    {"genre": "Weapon Mac-10", "keywords": ["submachine gun", "compact", "fully automatic", "street weapon", "illegal firearm", "rapid fire", "high recoil", "gang warfare", "concealed weapon", "9mm"]},
    {"genre": "Weapon Uzi", "keywords": ["submachine gun", "compact", "street weapon", "fully automatic", "gang warfare", "illegal firearm", "Israeli design", "rapid fire", "military use", "9mm"]},
    {"genre": "Weapon Tec-9", "keywords": ["handgun", "semi-automatic", "illegal firearm", "street weapon", "gangster gun", "compact", "high recoil", "9mm", "rapid fire", "small frame"]},
    {"genre": "Weapon Sawed-off Shotgun", "keywords": ["shotgun", "short barrel", "illegal weapon", "concealed firearm", "street weapon", "close range", "blunt force", "sawed-off barrel", "12 gauge", "criminal use"]},
    {"genre": "Weapon Sten Gun", "keywords": ["submachine gun", "World War II", "British design", "fully automatic", "cheap production", "illegal street gun", "smuggling", "rapid fire", "9mm", "classic weapon"]},
    {"genre": "Weapon M1911", "keywords": ["handgun", "semi-automatic", "combat pistol", "military sidearm", "1911 design", "classic firearm", "self-defense", "street carry", "lethal", "American-made"]},
    {"genre": "Weapon Glock 18", "keywords": ["firearm", "fully automatic", "handgun", "compact", "illegal street weapon", "9mm", "high recoil", "rapid fire", "police use", "self-defense"]},
    {"genre": "Weapon FN Five-SeveN", "keywords": ["handgun", "semi-automatic", "military firearm", "5.7x28mm", "compact", "street gun", "high velocity", "low recoil", "self-defense", "criminal use"]},
    {"genre": "Weapon Makarov", "keywords": ["handgun", "semi-automatic", "Russian design", "compact", "street weapon", "military sidearm", "9mm", "criminal use", "low recoil", "self-defense"]},
    {"genre": "Weapon Blowgun", "keywords": ["blowpipe", "silent weapon", "dart gun", "small caliber", "hunting", "quiet kill", "non-lethal", "illegal weapon", "poisoned darts", "stealth"]},
    {"genre": "Weapon Derringer", "keywords": ["handgun", "small caliber", "concealed carry", "short barrel", "street weapon", "pocket pistol", "criminal carry", "compact", "self-defense", "rare firearm"]},
    {"genre": "Weapon Glock 34", "keywords": ["handgun", "semi-automatic", "longer barrel", "tactical pistol", "police use", "competition", "street carry", "9mm", "Glock series", "self-defense"]},
    {"genre": "Weapon Walther P99", "keywords": ["handgun", "semi-automatic", "German design", "police use", "combat weapon", "self-defense", "9mm", "street weapon", "reliable", "high accuracy"]},
    {"genre": "Weapon Ruger Mini-14", "keywords": ["rifle", "semi-automatic", "street gun", "tactical", "urban combat", "self-defense", "hunting", "5.56mm", "reliable", "law enforcement"]},
    {"genre": "Weapon Luger P08", "keywords": ["handgun", "semi-automatic", "WWII", "German design", "vintage", "military sidearm", "9mm", "rare", "collectible", "historical firearm"]},
    {"genre": "Weapon M1 Garand", "keywords": ["rifle", "semi-automatic", "military use", "WWII", "iconic weapon", "American-made", "long range", "high power", "combat rifle", "collectible"]},
    {"genre": "Weapon AKS-74U", "keywords": ["assault rifle", "short-barreled", "Russian design", "compact AK-47", "military weapon", "illegal firearm", "street weapon", "7.62mm", "high recoil", "tactical"]},
    {"genre": "Weapon RPG-7", "keywords": ["rocket-propelled grenade", "launching weapon", "anti-tank", "military use", "illegal street weapon", "explosive", "Russian design", "heavy weapon", "high damage", "rare"]},
    {"genre": "Weapon M1919 Browning", "keywords": ["machine gun", "heavy weapon", "fully automatic", "WWII", "military use", "high fire rate", "heavy recoil", "vehicle mounted", "explosive power", "classic weapon"]},
    {"genre": "Weapon SPAS-12", "keywords": ["shotgun", "pump-action", "tactical shotgun", "military use", "street weapon", "12 gauge", "combat shotgun", "high recoil", "illegal firearm", "collectible"]},
    {"genre": "Weapon M3 Grease Gun", "keywords": ["submachine gun", "fully automatic", "military use", "WWII", "tactical weapon", "rapid fire", "compact", "historical firearm", "illegal weapon", "low-cost production"]},
    {"genre": "Weapon Pipe Shotgun", "keywords": ["homemade", "street weapon", "makeshift", "illegal firearm", "cheap materials", "close range", "shotgun", "12 gauge", "criminal use", "guerrilla warfare"]},
    {"genre": "Weapon Zip Gun", "keywords": ["homemade firearm", "makeshift", "illegal weapon", "craftsmanship", "single-shot", "street weapon", "low-cost", "criminal use", "self-defense", "dangerous"]},
    {"genre": "Weapon Molotov Cocktail", "keywords": ["homemade weapon", "flammable", "improvised", "street warfare", "riot control", "explosive", "guerrilla tactics", "flammable liquid", "criminal use", "illegal"]},
    {"genre": "Weapon Homemade AR-15", "keywords": ["rebellion weapon", "modified AR-15", "illegal firearm", "street gun", "homemade", "guerrilla warfare", "semi-automatic", "high recoil", "dangerous", "firearm"]},
    {"genre": "Weapon Stun Gun", "keywords": ["homemade", "self-defense", "illegal modification", "electric weapon", "non-lethal", "street weapon", "guerrilla tactics", "shock", "makeshift", "illegal"]},
    {"genre": "Weapon Claymore Mine (Homemade)", "keywords": ["improvised explosive", "homemade", "guerrilla warfare", "explosive", "landmine", "anti-personnel", "homemade bomb", "illegal weapon", "terrorism", "high danger"]},
    {"genre": "Weapon Crowbar (Modified)", "keywords": ["improvised weapon", "makeshift", "street fight", "criminal use", "rebel weapon", "blunt force", "illegal", "self-defense", "close combat", "guerrilla"]},
    {"genre": "Weapon Crossbow (Homemade)", "keywords": ["improvised", "street weapon", "homemade crossbow", "silent weapon", "rebel weapon", "archery", "guerrilla warfare", "non-lethal", "illegal", "precision"]},
    {"genre": "Weapon Pipe Bomb", "keywords": ["improvised explosive", "homemade", "guerrilla warfare", "illegal weapon", "explosive", "criminal use", "terrorist tactics", "high danger", "explosion", "barricade breaker"]},
    {"genre": "Weapon Home-made Rocket Launcher", "keywords": ["improvised", "guerrilla warfare", "rebellion", "homemade weapon", "street weapon", "illegal", "high destruction", "explosive", "illegal armament", "anti-tank"]},
    {"genre": "Weapon Molotov Grenade", "keywords": ["improvised", "homemade", "explosive", "flammable", "criminal use", "street warfare", "riot weapon", "urban combat", "guerrilla tactics", "illegal weapon"]},
    {"genre": "Weapon Melee Weapon (Homemade)", "keywords": ["homemade", "improvised weapon", "rebellion", "makeshift", "close combat", "street fight", "illegal", "blunt force", "self-defense", "dangerous"]},
    {"genre": "Weapon Homemade Sniper Rifle", "keywords": ["modified rifle", "guerrilla warfare", "long-range", "homemade firearm", "illegal", "rebellion", "sniper weapon", "covert", "military use", "dangerous"]},
    {"genre": "Weapon Handmade Machete", "keywords": ["homemade", "guerrilla weapon", "close combat", "illegal weapon", "handmade", "bladed weapon", "self-defense", "urban warfare", "dangerous", "weapon"]},
    {"genre": "Weapon Sling (Homemade)", "keywords": ["improvised weapon", "homemade", "self-defense", "street weapon", "blunt force", "rebel weapon", "simple weapon", "illegal", "non-lethal", "guerrilla"]},
    {"genre": "Weapon Homemade Rocket Propelled Grenade", "keywords": ["improvised", "guerrilla warfare", "illegal weapon", "homemade", "explosive", "military use", "high damage", "self-made", "anti-tank", "rebel weapon"]},
    {"genre": "Weapon Chemical Spray (Homemade)", "keywords": ["improvised", "homemade", "chemical weapon", "street use", "guerrilla tactics", "self-defense", "illegal weapon", "toxic", "riot control", "criminal use"]},
    {"genre": "Weapon Electromagnetic Pulse (EMP) Device", "keywords": ["improvised weapon", "homemade", "guerrilla warfare", "illegal", "EMP", "electronics attack", "self-made", "technology disruption", "high-tech", "dangerous"]},
    {"genre": "Weapon Improvised Knife", "keywords": ["homemade", "bladed weapon", "street weapon", "rebellion", "close combat", "illegal", "self-defense", "makeshift", "dangerous", "urban warfare"]},
    {"genre": "Weapon Bottle Bomb", "keywords": ["improvised explosive", "homemade", "criminal use", "illegal weapon", "flammable", "guerrilla tactics", "explosive", "street warfare", "dangerous", "terrorism"]},
    {"genre": "Weapon Improvised Grenade", "keywords": ["homemade", "explosive", "guerrilla warfare", "street weapon", "illegal", "dangerous", "rebel tactics", "urban warfare", "self-made", "criminal"]},
    {"genre": "Weapon Handmade Flame Thrower", "keywords": ["homemade", "fire weapon", "improvised", "street weapon", "illegal", "explosive", "flammable", "guerrilla warfare", "dangerous", "weapon"]},       
    {"genre": "Weapon Western Revolver", "keywords": ["pistol", "classic firearm", "cowboy", "single-action", "western style", "small caliber", "old west", "self-defense", "antique", "quick draw"]},
    {"genre": "Weapon Hunting Rifle", "keywords": ["long-range", "rifle", "hunting", "bolt action", "high caliber", "outdoor sport", "reliable", "self-defense", "precision shooting", "illegal modification"]},
    {"genre": "Weapon Crossbow", "keywords": ["medieval weapon", "silent", "archery", "long-range", "bow and arrow", "hunting", "rebel weapon", "non-lethal", "improvised", "wooden crossbow"]},
    {"genre": "Weapon Homemade Pistol", "keywords": ["improvised firearm", "pistol", "handmade", "illegal", "close combat", "street weapon", "reliable", "self-defense", "low-cost", "dangerous"]},
    {"genre": "Weapon Shotgun (Street Version)", "keywords": ["improvised", "shotgun", "homemade", "guerrilla warfare", "illegal weapon", "close-range", "single barrel", "self-defense", "criminal use", "high danger"]},
    {"genre": "Weapon Hunting Bow", "keywords": ["archery", "silent weapon", "bow and arrow", "long-range", "non-lethal", "homemade", "outdoor sport", "hunting", "survival", "guerrilla"]},
    {"genre": "Weapon Automatic Rifle (Modified)", "keywords": ["modified firearm", "homemade", "automatic", "military-style", "illegal", "guerrilla warfare", "high recoil", "dangerous", "rebel weapon", "illegal weapon"]},
    {"genre": "Weapon Revolver (Homemade)", "keywords": ["pistol", "revolver", "makeshift", "illegal weapon", "craftsmanship", "self-defense", "street weapon", "low-cost", "improvised", "dangerous"]},
    {"genre": "Weapon Lever-Action Rifle", "keywords": ["rifle", "western style", "lever-action", "hunting", "high power", "self-defense", "reliable", "antique", "rebel weapon", "rustic"]},
    {"genre": "Weapon Sawn-Off Shotgun", "keywords": ["shotgun", "short barrel", "close-range", "illegal firearm", "modified", "guerrilla warfare", "improvised", "street weapon", "dangerous", "blunt force"]},       
    {"genre": "Greys Alien", "keywords": ["large black eyes", "short stature", "gray skin", "telepathic abilities", "mysterious", "advanced technology", "emotionless", "UFO sightings", "scientific curiosity", "abduction folklore"]},
    {"genre": "Reptilians Alien", "keywords": ["lizard-like", "scaly skin", "intelligent", "shapeshifting", "cold-blooded", "political conspiracy", "underground dwellers", "aggressive", "world domination", "ancient origins"]},
    {"genre": "Nordics Alien", "keywords": ["tall and humanoid", "blond hair", "blue eyes", "benevolent", "telepathic", "mystical aura", "spiritual guidance", "peaceful", "interstellar travelers", "mythical beauty"]},
    {"genre": "Insectoids Alien", "keywords": ["insect-like features", "exoskeleton", "hive mind", "fast reflexes", "alien predators", "advanced hive societies", "colonial mindset", "brutal efficiency", "resourceful", "intimidating"]},
    {"genre": "Amoeboids Alien", "keywords": ["shape-shifting", "gelatinous form", "biological adaptability", "non-humanoid", "engulfing prey", "bioluminescence", "single-celled intelligence", "mimicry", "absorb nutrients", "resilient"]},
    {"genre": "Aquatics Alien", "keywords": ["ocean dwellers", "fins and gills", "bioluminescence", "deep-sea creatures", "intelligent communication", "water-based ecosystems", "hidden in oceans", "fluid movement", "ancient knowledge", "peaceful explorers"]},
    {"genre": "Energy Beings Alien", "keywords": ["non-corporeal", "pure energy", "glowing aura", "intangible", "high intelligence", "omnipresent", "quantum existence", "difficult to comprehend", "advanced civilizations", "mystical"]},
    {"genre": "Plant-Based Alien", "keywords": ["photosynthetic", "rooted intelligence", "adaptive growth", "green skin", "organic technology", "symbiotic relationships", "patient thinkers", "eco-friendly", "unpredictable forms", "nurturers"]},
    {"genre": "Silicon-Based Alien", "keywords": ["crystalline structure", "rock-like appearance", "extreme durability", "heat resistance", "non-organic life", "mineral-based systems", "slow metabolism", "geological adaptability", "inhabit harsh environments", "ancient beings"]},
    {"genre": "Predators Alien", "keywords": ["hunter instincts", "aggressive", "stealthy", "advanced weaponry", "xenomorphic features", "territorial", "combat experts", "fearsome presence", "trophy collectors", "deadly"]},
    {"genre": "Xenomorphs Alien", "keywords": ["parasitic reproduction", "acidic blood", "black exoskeleton", "predatory", "evolutionary adaptability", "fear-inducing", "hive structures", "biomechanical design", "relentless hunters", "nightmarish"]},
    {"genre": "Cephalopoid Alien", "keywords": ["tentacles", "amorphous", "underwater traits", "intelligent", "camouflage", "alien oceans", "telepathic communication", "ancient knowledge", "flexible bodies", "mysterious"]},
    {"genre": "Interdimensional Beings Alien", "keywords": ["exist outside time", "warp dimensions", "abstract forms", "multi-dimensional intelligence", "appear as hallucinations", "elusive", "godlike powers", "defy physics", "enigmatic", "otherworldly"]},
    {"genre": "Biological Robots Alien", "keywords": ["cybernetic enhancements", "biomechanical structure", "synthetic intelligence", "engineered", "tool-like purpose", "combination of organic and mechanical", "efficient", "indestructible", "unemotional", "designed for specific tasks"]},
    {"genre": "Light Beings Alien", "keywords": ["luminous forms", "peaceful", "spiritual guides", "pure energy", "non-violent", "highly intelligent", "interdimensional travelers", "celestial beauty", "calming presence", "emissaries of good"]},
    {"genre": "Shadow Beings Alien", "keywords": ["dark forms", "stealthy", "intangible", "fear-inducing", "unknown motives", "interdimensional origins", "appear in nightmares", "elusive", "stalkers", "mysterious and eerie"]},
    {"genre": "Void Dwellers Alien", "keywords": ["exist in deep space", "adapted to vacuum", "ancient beings", "star-eaters", "unfathomable scale", "indescribable forms", "eternal", "harbingers of destruction", "mythical status", "cosmic predators"]},
    {"genre": "Parasites Alien", "keywords": ["symbiotic or destructive", "host-dependent", "small size", "spread rapidly", "high adaptability", "mind control", "biological menace", "infectious", "transform hosts", "survivors"]},
    {"genre": "Hive-Minded Colonials Alien", "keywords": ["collective consciousness", "selfless unity", "highly organized", "dominant queen", "territorial", "rapid expansion", "swarm behavior", "evolutionary adaptation", "relentless", "intimidating numbers"]},
    {"genre": "Gelatinous Cubes Alien", "keywords": ["translucent", "amorphous", "digest prey", "biological traps", "slow-moving", "absorb nutrients", "simple intelligence", "alien dungeons", "unsettling", "unique predators"]},    
    {"genre": "Nationality Canadian", "keywords": ["warm flannel shirts", "rugged outdoors", "polite demeanor", "maple leaf symbols", "dynamic energy", "cultural pride", "natural surroundings", "majestic simplicity", "snowy landscapes", "ancestral charm"]},
    {"genre": "Nationality Quebecois", "keywords": ["cozy sweaters", "traditional cuisine", "artistic flair", "French-Canadian accent", "cultural richness", "dynamic personality", "winter charm", "heritage pride", "folk traditions", "majestic elegance"]},
    {"genre": "Nationality American", "keywords": ["casual attire", "diverse backgrounds", "vibrant energy", "patriotic symbols", "cultural diversity", "bold individuality", "dynamic lifestyles", "majestic resilience", "urban and rural scenes", "modern charm"]},
    {"genre": "Nationality French", "keywords": ["elegant fashion", "berets and scarves", "artistic flair", "cultural refinement", "Parisian backdrop", "majestic charisma", "timeless beauty", "romantic ambiance", "dynamic sophistication", "heritage pride"]},
    {"genre": "Nationality German", "keywords": ["traditional dirndl and lederhosen", "efficient demeanor", "rich cultural heritage", "majestic landscapes", "timeless craftsmanship", "dynamic traditions", "heritage pride", "beer steins and pretzels", "commanding charisma", "refined elegance"]},
    {"genre": "Nationality Italian", "keywords": ["stylish attire", "cultural richness", "warm charisma", "vibrant energy", "majestic Mediterranean scenes", "timeless traditions", "culinary passion", "dynamic gestures", "refined beauty", "ancestral charm"]},
    {"genre": "Nationality British", "keywords": ["classic trench coats", "reserved elegance", "tea traditions", "cultural sophistication", "majestic landscapes", "timeless charm", "heritage pride", "urban and countryside mix", "royal allure", "refined wit"]},
    {"genre": "Nationality Spanish", "keywords": ["flamenco dresses", "vibrant colors", "dynamic energy", "majestic culture", "timeless charisma", "passionate gestures", "heritage pride", "artistic traditions", "Mediterranean ambiance", "rich history"]},
    {"genre": "Nationality Japanese", "keywords": ["traditional kimonos", "calm demeanor", "dynamic precision", "cultural elegance", "majestic cherry blossoms", "timeless aesthetics", "heritage pride", "urban and rural contrasts", "refined sophistication", "ancestral charm"]},
    {"genre": "Nationality Korean", "keywords": ["modern streetwear", "traditional hanbok", "cultural richness", "vibrant energy", "dynamic creativity", "majestic landscapes", "ancestral pride", "urban chic", "refined artistry", "timeless elegance"]},
    {"genre": "Nationality Chinese", "keywords": ["ornate attire", "cultural pride", "majestic presence", "timeless traditions", "dynamic energy", "heritage wealth", "calligraphic art", "refined sophistication", "ancestral beauty", "scenic landscapes"]},
    {"genre": "Nationality Indian", "keywords": ["vibrant sarees", "ornate jewelry", "cultural richness", "majestic celebrations", "dynamic energy", "heritage pride", "spiritual ambiance", "timeless grace", "ancestral wisdom", "refined charm"]},
    {"genre": "Nationality Mexican", "keywords": ["colorful traditional attire", "dynamic gestures", "cultural pride", "majestic charisma", "timeless celebrations", "heritage charm", "warm energy", "artistic traditions", "ancestral beauty", "vibrant scenes"]},
    {"genre": "Nationality Brazilian", "keywords": ["vibrant carnival costumes", "dynamic samba moves", "cultural energy", "majestic charisma", "tropical landscapes", "heritage pride", "warm personalities", "dynamic music", "ancestral artistry", "joyful ambiance"]},
    {"genre": "Nationality Australian", "keywords": ["rugged attire", "dynamic energy", "majestic outback scenes", "cultural pride", "timeless charm", "beach and bush contrasts", "ancestral heritage", "warm charisma", "wildlife connections", "refined simplicity"]},
    {"genre": "Nationality Russian", "keywords": ["fur-lined coats", "cultural pride", "majestic landscapes", "timeless traditions", "ancestral charm", "refined elegance", "dynamic gestures", "urban and rural contrasts", "strong presence", "heritage resilience"]},
    {"genre": "Nationality South African", "keywords": ["vibrant attire", "cultural diversity", "dynamic energy", "majestic savanna scenes", "ancestral pride", "timeless charisma", "rich traditions", "refined gestures", "heritage unity", "joyful ambiance"]},
    {"genre": "Nationality Egyptian", "keywords": ["ornate attire", "cultural pride", "majestic deserts", "ancestral wisdom", "timeless elegance", "heritage charm", "refined beauty", "dynamic energy", "pharaonic aura", "mystical presence"]},
    {"genre": "Nationality Turkish", "keywords": ["traditional attire", "cultural richness", "majestic charisma", "timeless elegance", "heritage pride", "dynamic gestures", "refined artistry", "ancestral beauty", "dynamic energy", "urban and historic blends"]},
    {"genre": "Nationality Thai", "keywords": ["ornate attire", "cultural pride", "majestic temples", "timeless elegance", "heritage charm", "dynamic energy", "refined beauty", "ancestral artistry", "vibrant celebrations", "tropical surroundings"]},
    {"genre": "Nationality Greek", "keywords": ["traditional toga-inspired attire", "cultural pride", "majestic ruins", "timeless elegance", "ancestral wisdom", "refined gestures", "heritage charisma", "Mediterranean ambiance", "dynamic energy", "mythical allure"]},
    {"genre": "Nationality Irish", "keywords": ["cozy sweaters", "cultural charm", "majestic green landscapes", "timeless traditions", "ancestral pride", "heritage music", "refined demeanor", "warm energy", "dynamic storytelling", "rich folklore"]},
    {"genre": "Nationality Scottish", "keywords": ["traditional kilts", "heritage pride", "majestic highlands", "ancestral charisma", "dynamic energy", "refined gestures", "bagpipe music", "timeless strength", "cultural resilience", "rugged charm"]},
    {"genre": "Nationality Dutch", "keywords": ["simple yet elegant attire", "cultural richness", "majestic tulip fields", "heritage charm", "ancestral wisdom", "refined beauty", "dynamic energy", "windmill backdrops", "warm personalities", "timeless artistry"]},
    {"genre": "Nationality Swedish", "keywords": ["minimalist attire", "heritage pride", "majestic forests", "timeless elegance", "ancestral wisdom", "refined gestures", "dynamic traditions", "cultural innovation", "warm demeanor", "nordic serenity"]},
    {"genre": "Nationality Norwegian", "keywords": ["traditional bunads", "majestic fjords", "ancestral pride", "timeless charm", "heritage resilience", "refined beauty", "dynamic energy", "nordic strength", "cultural richness", "serene landscapes"]},
    {"genre": "Nationality Finnish", "keywords": ["cozy attire", "majestic winter scenes", "ancestral resilience", "timeless simplicity", "heritage charm", "refined demeanor", "dynamic traditions", "nordic beauty", "cultural pride", "tranquil presence"]},
    {"genre": "Nationality Polish", "keywords": ["traditional folk dresses", "cultural richness", "majestic landscapes", "ancestral pride", "timeless charm", "heritage beauty", "refined gestures", "dynamic energy", "vibrant traditions", "warm personalities"]},
    {"genre": "Nationality Hungarian", "keywords": ["colorful traditional attire", "cultural pride", "majestic charisma", "ancestral charm", "timeless beauty", "heritage traditions", "refined gestures", "dynamic energy", "artistic sophistication", "rich folk culture"]},
    {"genre": "Nationality Kurdish", "keywords": ["traditional vibrant attire", "ancestral pride", "majestic landscapes", "timeless strength", "heritage resilience", "dynamic gestures", "cultural charm", "refined beauty", "warm demeanor", "rich traditions"]},
    {"genre": "Nationality Armenian", "keywords": ["traditional attire", "cultural pride", "majestic mountains", "ancestral resilience", "timeless charm", "heritage beauty", "refined artistry", "dynamic energy", "warm personalities", "rich history"]},
    {"genre": "Nationality Persian", "keywords": ["ornate attire", "cultural richness", "majestic elegance", "timeless sophistication", "heritage beauty", "refined gestures", "ancestral pride", "dynamic artistry", "warm charisma", "poetic allure"]},
    {"genre": "Nationality Mongolian", "keywords": ["traditional deel robes", "cultural richness", "majestic steppes", "ancestral strength", "timeless traditions", "heritage charm", "refined gestures", "dynamic energy", "nomadic charisma", "historic pride"]},
    {"genre": "Nationality Vietnamese", "keywords": ["traditional ao dai", "cultural richness", "majestic landscapes", "ancestral pride", "timeless beauty", "heritage elegance", "dynamic energy", "refined gestures", "vibrant celebrations", "serene charm"]},
    {"genre": "Nationality Filipino", "keywords": ["traditional barong and terno", "cultural pride", "majestic tropical scenes", "ancestral charisma", "timeless beauty", "heritage charm", "dynamic energy", "refined demeanor", "vibrant traditions", "warm personalities"]},
    {"genre": "Nationality Malay", "keywords": ["traditional baju kurung", "cultural richness", "majestic charisma", "ancestral pride", "timeless beauty", "heritage charm", "refined gestures", "dynamic traditions", "serene landscapes", "vibrant festivals"]},
    {"genre": "Nationality Indonesian", "keywords": ["vibrant batik patterns", "cultural pride", "majestic islands", "ancestral wisdom", "timeless beauty", "heritage elegance", "refined artistry", "dynamic energy", "vibrant traditions", "rich folklore"]},
    {"genre": "Nationality Tibetan", "keywords": ["traditional chubas", "majestic mountains", "ancestral resilience", "timeless serenity", "heritage spirituality", "refined gestures", "dynamic energy", "cultural wisdom", "warm presence", "sacred charm"]},
    {"genre": "Nationality Native American", "keywords": ["traditional regalia", "cultural pride", "majestic landscapes", "ancestral wisdom", "timeless spirituality", "heritage beauty", "refined gestures", "dynamic traditions", "warm resilience", "historic strength"]},
    {"genre": "Nationality Inuit", "keywords": ["traditional fur-lined attire", "cultural resilience", "majestic Arctic landscapes", "ancestral wisdom", "timeless strength", "heritage beauty", "refined demeanor", "dynamic survival skills", "warm energy", "nordic presence"]},
    {"genre": "Nationality Israeli", "keywords": ["modern and traditional attire", "cultural diversity", "majestic landscapes", "ancestral pride", "timeless traditions", "heritage resilience", "refined demeanor", "dynamic energy", "innovative spirit", "historic depth"]},
    {"genre": "Nationality Turkish", "keywords": ["traditional Ottoman-inspired attire", "cultural richness", "majestic mosques", "ancestral pride", "timeless beauty", "heritage charm", "refined artistry", "dynamic energy", "vibrant traditions", "warm hospitality"]},
    {"genre": "Nationality Cuban", "keywords": ["tropical attire", "cultural vibrancy", "majestic beaches", "ancestral pride", "timeless music", "heritage charm", "dynamic rhythms", "refined movements", "vibrant festivals", "warm charisma"]},
    {"genre": "Nationality Jamaican", "keywords": ["casual tropical attire", "cultural vibrancy", "majestic beaches", "ancestral pride", "timeless rhythms", "heritage music", "dynamic energy", "refined movements", "vibrant colors", "warm charisma"]},
    {"genre": "Nationality Afghan", "keywords": ["traditional vibrant attire", "cultural resilience", "majestic mountains", "ancestral strength", "timeless charm", "heritage beauty", "refined gestures", "dynamic traditions", "warm personalities", "historic pride"]},
    {"genre": "Nationality Pakistani", "keywords": ["traditional shalwar kameez", "cultural richness", "majestic landscapes", "ancestral pride", "timeless elegance", "heritage beauty", "refined gestures", "dynamic energy", "vibrant festivals", "warm personalities"]},
    {"genre": "Nationality Bangladeshi", "keywords": ["vibrant saris", "cultural richness", "majestic rivers", "ancestral pride", "timeless traditions", "heritage charm", "dynamic artistry", "refined gestures", "warm personalities", "vibrant celebrations"]},
    {"genre": "Nationality Nepali", "keywords": ["traditional daura suruwal", "majestic Himalayas", "ancestral resilience", "timeless traditions", "heritage beauty", "refined gestures", "dynamic spirituality", "cultural charm", "warm energy", "sacred presence"]},
    {"genre": "Nationality Sri Lankan", "keywords": ["traditional saris", "cultural richness", "majestic tropical backdrops", "ancestral pride", "timeless charm", "heritage beauty", "refined artistry", "dynamic energy", "vibrant traditions", "warm charisma"]},
    {"genre": "Nationality Kenyan", "keywords": ["vibrant kitenge patterns", "cultural richness", "majestic savannahs", "ancestral pride", "timeless charm", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "vibrant celebrations"]},
    {"genre": "Nationality Nigerian", "keywords": ["traditional agbada and gele", "cultural vibrancy", "majestic landscapes", "ancestral pride", "timeless beauty", "heritage elegance", "dynamic artistry", "refined gestures", "vibrant celebrations", "warm personalities"]},
    {"genre": "Nationality Ethiopian", "keywords": ["traditional habesha kemis", "cultural richness", "majestic highlands", "ancestral pride", "timeless traditions", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "historic depth"]},
    {"genre": "Nationality South African", "keywords": ["modern and traditional fusion", "cultural diversity", "majestic vistas", "ancestral pride", "timeless music", "heritage beauty", "dynamic energy", "refined gestures", "vibrant celebrations", "warm charisma"]},
    {"genre": "Nationality Moroccan", "keywords": ["ornate caftans", "cultural richness", "majestic deserts", "ancestral charm", "timeless elegance", "heritage artistry", "refined gestures", "dynamic energy", "vibrant colors", "warm hospitality"]},
    {"genre": "Nationality Argentinian", "keywords": ["elegant attire", "cultural vibrancy", "majestic mountains", "ancestral pride", "timeless tango", "heritage charm", "refined movements", "dynamic energy", "warm personalities", "artistic depth"]},
    {"genre": "Nationality Chilean", "keywords": ["traditional huaso attire", "cultural richness", "majestic Andes", "ancestral pride", "timeless traditions", "heritage beauty", "refined gestures", "dynamic energy", "warm hospitality", "artistic charm"]},
    {"genre": "Nationality Peruvian", "keywords": ["vibrant traditional attire", "cultural richness", "majestic Andes", "ancestral pride", "timeless charm", "heritage artistry", "dynamic energy", "refined gestures", "warm personalities", "historic depth"]},
    {"genre": "Nationality Bolivian", "keywords": ["colorful traditional attire", "cultural richness", "majestic mountains", "ancestral pride", "timeless beauty", "heritage charm", "dynamic artistry", "refined gestures", "warm hospitality", "historic pride"]},
    {"genre": "Nationality Haitian", "keywords": ["traditional vibrant attire", "cultural vibrancy", "majestic tropical backdrops", "ancestral pride", "timeless rhythms", "heritage charm", "dynamic artistry", "refined gestures", "warm personalities", "vibrant celebrations"]},
    {"genre": "Nationality Saudi Arabian", "keywords": ["traditional thobe and abaya", "cultural richness", "majestic deserts", "ancestral pride", "timeless elegance", "heritage beauty", "refined gestures", "dynamic energy", "warm hospitality", "spiritual depth"]},
    {"genre": "Nationality Emirati", "keywords": ["luxurious kandura and abaya", "cultural vibrancy", "majestic skylines", "ancestral pride", "timeless traditions", "heritage charm", "dynamic energy", "refined gestures", "modern fusion", "warm hospitality"]},
    {"genre": "Nationality Vietnamese", "keywords": ["traditional áo dài", "cultural richness", "majestic landscapes", "ancestral pride", "timeless elegance", "heritage artistry", "refined gestures", "dynamic energy", "warm personalities", "vibrant traditions"]},
    {"genre": "Nationality Cambodian", "keywords": ["traditional sampot", "cultural vibrancy", "majestic temples", "ancestral pride", "timeless beauty", "heritage charm", "refined artistry", "dynamic energy", "warm personalities", "historic depth"]},
    {"genre": "Nationality Laotian", "keywords": ["traditional sinh", "cultural richness", "majestic river scenery", "ancestral pride", "timeless traditions", "heritage artistry", "refined gestures", "dynamic energy", "warm personalities", "vibrant charm"]},
    {"genre": "Nationality Myanmar (Burmese)", "keywords": ["traditional longyi", "cultural richness", "majestic pagodas", "ancestral pride", "timeless elegance", "heritage beauty", "refined gestures", "dynamic spirituality", "warm personalities", "historic charm"]},
    {"genre": "Nationality Kazakh", "keywords": ["traditional chapan", "cultural richness", "majestic steppes", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "warm hospitality", "historic charm"]},
    {"genre": "Nationality Uzbek", "keywords": ["traditional atlas patterns", "cultural richness", "majestic architecture", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "vibrant traditions"]},
    {"genre": "Nationality Mongolian", "keywords": ["traditional deel", "cultural richness", "majestic landscapes", "ancestral pride", "timeless charm", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "historic depth"]},
    {"genre": "Nationality Armenian2", "keywords": ["traditional taraz", "cultural richness", "majestic mountains", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "warm hospitality", "historic charm"]},
    {"genre": "Nationality Georgian", "keywords": ["traditional chokha", "cultural richness", "majestic landscapes", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "warm personalities", "vibrant traditions"]},
    {"genre": "Nationality Korean (North and South)", "keywords": ["traditional hanbok", "cultural richness", "majestic mountains", "ancestral pride", "timeless elegance", "heritage artistry", "refined gestures", "dynamic energy", "modern fusion", "warm personalities"]},
    {"genre": "Nationality Tibetan", "keywords": ["traditional chuba", "cultural richness", "majestic Himalayas", "ancestral pride", "timeless spirituality", "heritage beauty", "refined gestures", "dynamic energy", "warm personalities", "sacred presence"]},
    {"genre": "Nationality Icelandic", "keywords": ["modern and traditional attire", "cultural richness", "majestic landscapes", "ancestral pride", "timeless beauty", "heritage charm", "refined gestures", "dynamic energy", "warm personalities", "historic depth"]},
    {"genre": "Nationality Greek", "keywords": ["traditional foustanella", "cultural richness", "majestic islands", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "warm hospitality", "historic charm"]},
    {"genre": "Nationality Polynesian", "keywords": ["vibrant tropical attire", "cultural richness", "majestic beaches", "ancestral pride", "timeless traditions", "heritage artistry", "refined gestures", "dynamic energy", "warm hospitality", "sacred charm"]},
    {"genre": "Nationality Aboriginal Australian", "keywords": ["traditional ceremonial attire", "cultural vibrancy", "majestic outback landscapes", "ancestral pride", "timeless traditions", "heritage artistry", "refined gestures", "spiritual depth", "vibrant community", "sacred connection"]},
    {"genre": "Nationality Maori (New Zealand)", "keywords": ["traditional moko and attire", "cultural richness", "majestic landscapes", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "warm hospitality", "spiritual presence"]},
    {"genre": "Nationality Inca", "keywords": ["golden ornaments", "rich textiles", "Andean mountains", "ancestral pride", "timeless beauty", "heritage artistry", "sun worship", "stone temples", "refined craftsmanship", "majestic legacy"]},
    {"genre": "Nationality Maya", "keywords": ["intricate carvings", "hieroglyphic artistry", "jungle landscapes", "ancestral wisdom", "timeless elegance", "celestial motifs", "pyramid temples", "vivid murals", "cosmic connection", "spiritual depth"]},
    {"genre": "Nationality Aztec", "keywords": ["feathered headdresses", "stone carvings", "majestic warriors", "ancestral pride", "timeless artistry", "eagle and serpent motifs", "temple grandeur", "ritual symbolism", "cosmic balance", "sacred vitality"]},
    {"genre": "Nationality Babylonian", "keywords": ["ziggurat temples", "cuneiform inscriptions", "majestic river valleys", "ancestral pride", "timeless sophistication", "heritage beauty", "refined art", "astronomical knowledge", "mythological grandeur", "opulent textiles"]},
    {"genre": "Nationality Sumerian", "keywords": ["ancient city-states", "cuneiform tablets", "majestic rivers", "ancestral wisdom", "timeless craftsmanship", "heritage beauty", "refined artistry", "early civilization", "sacred temples", "historic depth"]},
    {"genre": "Nationality Ancient Egyptian", "keywords": ["pharaohs and queens", "pyramids of Giza", "hieroglyphic artistry", "timeless elegance", "sunlit deserts", "refined jewelry", "spiritual connection", "majestic temples", "golden tones", "royal charisma"]},
    {"genre": "Nationality Norse (Viking)", "keywords": ["runestone inscriptions", "majestic fjords", "ancestral pride", "timeless craftsmanship", "heritage beauty", "refined weaponry", "sailing ships", "warrior spirit", "mythological motifs", "historic charisma"]},
    {"genre": "Nationality Etruscan", "keywords": ["rich ceramics", "majestic tombs", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "golden artifacts", "historic charm", "ancient influence"]},
    {"genre": "Nationality Hittite", "keywords": ["ancient fortresses", "cultural richness", "majestic landscapes", "ancestral pride", "timeless craftsmanship", "heritage beauty", "refined artistry", "mythological motifs", "stone carvings", "historic charm"]},
    {"genre": "Nationality Phoenician", "keywords": ["maritime trade", "majestic ships", "ancestral pride", "timeless craftsmanship", "heritage beauty", "purple dye mastery", "refined artistry", "coastal grandeur", "mythological legacy", "historic influence"]},
    {"genre": "Nationality Minoan", "keywords": ["fresco artistry", "majestic palaces", "ancestral pride", "timeless elegance", "heritage charm", "refined gestures", "dynamic energy", "vivid murals", "historic beauty", "ancient creativity"]},
    {"genre": "Nationality Ancient Greek (Mycenaean)", "keywords": ["golden masks", "majestic architecture", "ancestral pride", "timeless artistry", "heritage beauty", "refined craftsmanship", "heroic motifs", "dynamic energy", "historic charisma", "epic legacy"]},
    {"genre": "Nationality Native American Mississippian", "keywords": ["mound builders", "cultural vibrancy", "majestic rivers", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "ceremonial symbolism", "historic connection"]},
    {"genre": "Nationality Celtic (Gaul)", "keywords": ["intricate patterns", "majestic landscapes", "ancestral pride", "timeless craftsmanship", "heritage beauty", "refined gestures", "dynamic energy", "warrior spirit", "mythological motifs", "historic depth"]},
    {"genre": "Nationality Olmec", "keywords": ["colossal heads", "cultural richness", "majestic jungles", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "mystical symbolism", "historic creativity"]},
    {"genre": "Nationality Scythian", "keywords": ["golden treasures", "cultural vibrancy", "majestic steppes", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "nomadic charm", "historic elegance"]},
    {"genre": "Nationality Byzantine", "keywords": ["mosaic artistry", "majestic churches", "ancestral pride", "timeless elegance", "heritage beauty", "refined gestures", "golden icons", "dynamic spirituality", "ornate textiles", "historic depth"]},
    {"genre": "Nationality Mughal Empire", "keywords": ["ornate architecture", "majestic palaces", "ancestral pride", "timeless artistry", "heritage beauty", "refined gestures", "dynamic energy", "vivid murals", "royal sophistication", "historic grandeur"]},
    {"genre": "Nationality Ancestral Polynesian", "keywords": ["tiki carvings", "cultural vibrancy", "majestic islands", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "warm traditions", "spiritual connection"]},
    {"genre": "Nationality Carolingian", "keywords": ["illuminated manuscripts", "majestic castles", "ancestral pride", "timeless beauty", "heritage artistry", "refined gestures", "dynamic energy", "historic influence", "royal presence", "sacred art"]},    
    {"genre": "Zeus (Greek)", "keywords": ["king of the gods", "thunderbolt", "supreme ruler", "sky god", "Greek mythology", "divine authority", "powerful presence", "ancient leadership", "royal god", "heavenly power"]},
    {"genre": "Hera (Greek)", "keywords": ["queen of the gods", "marriage goddess", "protector of women", "divine beauty", "majestic presence", "Greek mythology", "royal elegance", "family goddess", "sacred vows", "regal strength"]},
    {"genre": "Odin (Norse)", "keywords": ["allfather", "wisdom god", "rune magic", "Norse mythology", "one-eyed god", "warrior god", "ravens and wolves", "divine knowledge", "battle leadership", "sacrifice for wisdom"]},
    {"genre": "Frigg (Norse)", "keywords": ["queen of the gods", "mother goddess", "wisdom and love", "marriage protector", "fate weaver", "divine beauty", "Norse mythology", "sacred bond", "majestic grace", "protectress of families"]},
    {"genre": "Ra (Egyptian)", "keywords": ["sun god", "creator god", "Egyptian mythology", "solar disk", "heavenly ruler", "divine light", "day and night cycle", "ancient power", "eternal warmth", "celestial dominion"]},
    {"genre": "Isis (Egyptian)", "keywords": ["goddess of magic", "mother goddess", "Egyptian mythology", "divine wisdom", "protectress", "fertility goddess", "sacred healer", "eternal love", "mystical power", "queen of the gods"]},
    {"genre": "Brahma (Hindu)", "keywords": ["creator god", "four faces", "Hindu mythology", "divine intellect", "god of knowledge", "creator of the universe", "eternal being", "cosmic order", "supreme deity", "wisdom and creation"]},
    {"genre": "Vishnu (Hindu)", "keywords": ["preserver god", "eternal protector", "Hindu mythology", "blue-skinned god", "divine incarnations", "balance of the universe", "cosmic protector", "god of love", "majestic power", "eternal guardian"]},
    {"genre": "Shiva (Hindu)", "keywords": ["destroyer god", "transformation god", "Hindu mythology", "meditating deity", "god of destruction and regeneration", "divine ascetic", "dance of destruction", "cosmic energy", "transcendental presence", "divine force"]},
    {"genre": "Athena (Greek)", "keywords": ["goddess of wisdom", "warrior goddess", "Greek mythology", "strategic intellect", "peaceful strength", "protector of Athens", "shield and spear", "wise counselor", "divine justice", "virgin goddess"]},
    {"genre": "Aphrodite (Greek)", "keywords": ["goddess of love", "beauty goddess", "Greek mythology", "romantic allure", "eternal beauty", "divine love", "sensual charm", "golden goddess", "goddess of desire", "passion"]},
    {"genre": "Thor (Norse)", "keywords": ["thunder god", "mighty hammer", "Norse mythology", "god of storms", "warrior strength", "protector of mankind", "divine warrior", "battle fury", "stormbringer", "earth protector"]},
    {"genre": "Loki (Norse)", "keywords": ["trickster god", "shape-shifter", "Norse mythology", "mischievous god", "chaos bringer", "god of lies", "divine humor", "fiery presence", "god of discord", "deceiver"]},
    {"genre": "Anubis (Egyptian)", "keywords": ["god of the dead", "mummification", "Egyptian mythology", "guardian of the underworld", "afterlife protector", "divine guide", "jackal-headed god", "ritual protector", "god of transition", "sacred journey"]},
    {"genre": "Hades (Greek)", "keywords": ["god of the underworld", "Greek mythology", "ruler of the dead", "divine judge", "god of wealth", "dark domain", "eternal ruler", "silent power", "shadow god", "king of the underworld"]},
    {"genre": "Poseidon (Greek)", "keywords": ["god of the sea", "Greek mythology", "earth shaker", "trident god", "ocean ruler", "storm god", "protector of sailors", "divine power", "water deities", "majestic sea god"]},
    {"genre": "Demeter (Greek)", "keywords": ["goddess of the harvest", "earth goddess", "Greek mythology", "fertility goddess", "motherly love", "agriculture", "abundant nature", "cornucopia", "seasonal cycles", "nurturing presence"]},
    {"genre": "Hera (Greek)", "keywords": ["queen of the gods", "goddess of marriage", "family protector", "Greek mythology", "divine love", "sacred vows", "regal elegance", "maternal presence", "majestic queen", "royal charisma"]},
    {"genre": "Quetzalcoatl (Aztec)", "keywords": ["feathered serpent", "god of winds", "creator god", "Aztec mythology", "god of learning", "divine knowledge", "fertility god", "protector of humanity", "earth and sky balance", "ancient wisdom"]},
    {"genre": "Xochiquetzal (Aztec)", "keywords": ["goddess of love", "beauty goddess", "Aztec mythology", "flowers and fertility", "divine femininity", "goddess of joy", "ancient arts", "sensual charm", "passion", "embodiment of beauty"]},
    {"genre": "Marduk (Babylonian)", "keywords": ["god of storms", "Babylonian mythology", "creator god", "protector god", "god of order", "mighty warrior", "ancient strength", "ruler of heavens", "divine justice", "mesopotamian grandeur"]},    
    {"genre": "Ares (Greek)", "keywords": ["god of war", "Greek mythology", "battle frenzy", "violent strength", "warrior god", "divine conflict", "god of aggression", "battlefield dominance", "warrior's rage", "divine bloodlust"]},
    {"genre": "Athena (Greek)", "keywords": ["goddess of wisdom", "goddess of war", "Greek mythology", "strategic intellect", "virgin goddess", "battle tactics", "divine protector", "shield bearer", "strategic brilliance", "defender of Athens"]},
    {"genre": "Apollo (Greek)", "keywords": ["god of the sun", "Greek mythology", "god of music", "healing god", "archer god", "divine beauty", "sunlight radiance", "prophecy", "artistic genius", "golden radiance"]},
    {"genre": "Artemis (Greek)", "keywords": ["goddess of the hunt", "Greek mythology", "protector of animals", "moon goddess", "divine strength", "virgin goddess", "wilds and forests", "hunter's precision", "archery skills", "wild beauty"]},
    {"genre": "Hecate (Greek)", "keywords": ["goddess of magic", "witchcraft", "Greek mythology", "underworld goddess", "night goddess", "crossroads", "divine sorcery", "moon and shadow", "dark arts", "mysterious power"]},
    {"genre": "Horus (Egyptian)", "keywords": ["sky god", "Egyptian mythology", "god of kingship", "falcon-headed god", "protector of Egypt", "divine ruler", "god of the pharaohs", "solar deity", "heavenly ruler", "eternal vision"]},
    {"genre": "Set (Egyptian)", "keywords": ["god of chaos", "Egyptian mythology", "god of desert", "warrior god", "god of storms", "divine trickster", "god of violence", "protector of the underworld", "primal force", "god of disorder"]},
    {"genre": "Anubis (Egyptian)", "keywords": ["god of mummification", "Egyptian mythology", "protector of the dead", "jackal-headed god", "guide to the afterlife", "death and rebirth", "underworld deity", "guardian of tombs", "funeral god", "sacred protector"]},
    {"genre": "Bastet (Egyptian)", "keywords": ["goddess of home", "Egyptian mythology", "protector of women", "cat goddess", "divine beauty", "fertility goddess", "family protector", "goddess of music and dance", "joy and love", "nurturing presence"]},
    {"genre": "Tezcatlipoca (Aztec)", "keywords": ["god of night", "Aztec mythology", "creator god", "god of temptation", "god of the jaguar", "deity of conflict", "divine darkness", "trickster god", "god of fate", "mirror god"]},
    {"genre": "Tlaloc (Aztec)", "keywords": ["god of rain", "Aztec mythology", "god of fertility", "storm god", "god of agriculture", "divine power", "rain-bringer", "sacred water", "fertility deity", "earth’s nourishment"]},
    {"genre": "Quetzalcoatl (Aztec)", "keywords": ["feathered serpent", "god of winds", "creator god", "Aztec mythology", "god of learning", "divine knowledge", "fertility god", "protector of humanity", "earth and sky balance", "ancient wisdom"]},
    {"genre": "Mithras (Persian)", "keywords": ["god of light", "Persian mythology", "protector of truth", "god of contracts", "divine warrior", "bull slayer", "cosmic balance", "light vs dark", "deity of soldiers", "savior god"]},
    {"genre": "Zoroaster (Persian)", "keywords": ["prophet", "Persian religion", "founder of Zoroastrianism", "spiritual leader", "god of light", "divine wisdom", "sacred fire", "god of good", "eternal struggle", "divine truth"]},
    {"genre": "Freya (Norse)", "keywords": ["goddess of love", "Norse mythology", "goddess of beauty", "goddess of fertility", "warrior goddess", "divine wisdom", "valkyrie", "divine sensuality", "golden goddess", "magical allure"]},
    {"genre": "Tyr (Norse)", "keywords": ["god of war", "Norse mythology", "god of justice", "honor god", "brave warrior", "divine strength", "god of sacrifice", "guardian god", "sword of justice", "ancient power"]},
    {"genre": "Njord (Norse)", "keywords": ["god of the sea", "Norse mythology", "god of wealth", "sea god", "divine protector", "god of wind and sea", "coastal deity", "storm god", "navigator's deity", "oceanic ruler"]},
    {"genre": "Hel (Norse)", "keywords": ["goddess of the underworld", "Norse mythology", "daughter of Loki", "death goddess", "ruler of Helheim", "shadow goddess", "divine ruler of the dead", "dark domain", "underworld queen", "eternal ruler"]},
    {"genre": "Shiva (Hindu)", "keywords": ["god of destruction", "Hindu mythology", "god of transformation", "ascetic god", "divine dancer", "destroyer god", "regeneration", "cosmic god", "lord of destruction", "divine force"]},
    {"genre": "Kali (Hindu)", "keywords": ["goddess of destruction", "Hindu mythology", "mother goddess", "darkness goddess", "goddess of time", "warrior goddess", "divine power", "fierce energy", "goddess of death", "life and death cycle"]},
    {"genre": "Ganesh (Hindu)", "keywords": ["god of beginnings", "Hindu mythology", "elephant-headed god", "remover of obstacles", "wisdom god", "god of intellect", "divine patron of arts", "prosperity", "luck and good fortune", "protective deity"]},    
    {"genre": "Software Developer", "keywords": ["coding", "programming", "problem-solving", "technology", "innovation", "debugging", "collaboration", "system design", "software creation", "technical expertise"]},
    {"genre": "Doctor", "keywords": ["medical care", "health", "diagnosis", "treatment", "healing", "patient care", "emergency response", "surgery", "compassion", "lifesaving"]},
    {"genre": "Teacher", "keywords": ["education", "instruction", "learning", "guidance", "classroom", "mentorship", "lesson planning", "students", "knowledge", "communication"]},
    {"genre": "Chef", "keywords": ["cooking", "culinary arts", "recipes", "food preparation", "creativity", "kitchen management", "flavors", "presentation", "gourmet", "restaurant"]},
    {"genre": "Police Officer", "keywords": ["law enforcement", "public safety", "patrol", "crime prevention", "investigation", "protection", "justice", "discipline", "community service", "security"]},
    {"genre": "Artist", "keywords": ["creativity", "painting", "sculpting", "expression", "imagination", "design", "color theory", "visual arts", "gallery", "aesthetics"]},
    {"genre": "Musician", "keywords": ["performance", "music", "instrument", "singing", "composing", "melody", "rhythm", "creativity", "entertainment", "studio recording"]},
    {"genre": "Writer", "keywords": ["storytelling", "creative writing", "literature", "editing", "novels", "imagination", "publishing", "articles", "narrative", "language"]},
    {"genre": "Farmer", "keywords": ["agriculture", "crop cultivation", "livestock", "sustainability", "land management", "harvesting", "rural life", "organic farming", "soil", "food production"]},
    {"genre": "Construction Worker", "keywords": ["building", "construction", "tools", "manual labor", "safety", "blueprints", "infrastructure", "engineering", "physical work", "teamwork"]},
    {"genre": "Pilot", "keywords": ["aviation", "airplane", "navigation", "flying", "travel", "cockpit", "airline", "precision", "aerodynamics", "global transportation"]},
    {"genre": "Nurse", "keywords": ["medical care", "patient assistance", "healthcare", "compassion", "emergency response", "hospitals", "treatment", "healing", "support", "public health"]},
    {"genre": "Scientist", "keywords": ["research", "experiments", "innovation", "analysis", "discovery", "laboratory", "hypothesis", "theory", "data", "problem-solving"]},
    {"genre": "Photographer", "keywords": ["photography", "camera", "composition", "lighting", "creativity", "editing", "visual storytelling", "moments", "artistic", "portfolio"]},
    {"genre": "Athlete", "keywords": ["sports", "training", "competition", "fitness", "dedication", "teamwork", "discipline", "achievement", "performance", "physical excellence"]},
    {"genre": "Librarian", "keywords": ["books", "organization", "cataloging", "information", "knowledge", "research", "archives", "quiet", "education", "community"]},
    {"genre": "Mechanic", "keywords": ["automotive", "repairs", "engines", "tools", "diagnostics", "maintenance", "vehicles", "manual skills", "technical", "precision"]},
    {"genre": "Electrician", "keywords": ["wiring", "electricity", "installation", "safety", "repairs", "circuitry", "energy", "lighting", "power systems", "technical work"]},
    {"genre": "Barber", "keywords": ["haircutting", "styling", "grooming", "shaving", "creativity", "personal care", "clippers", "salon", "customer service", "appearance"]},
    {"genre": "Architect", "keywords": ["design", "blueprints", "structures", "creativity", "planning", "engineering", "urban development", "artistic vision", "construction", "spatial awareness"]},
    {"genre": "Paramedic", "keywords": ["emergency response", "medical aid", "ambulance", "first aid", "life-saving", "healthcare", "rescue", "trauma care", "compassion", "crisis management"]},
    {"genre": "Actor", "keywords": ["performance", "drama", "film", "stage", "theater", "character", "entertainment", "expression", "storytelling", "creativity"]},
    {"genre": "Firefighter", "keywords": ["rescue", "fire safety", "emergency response", "public safety", "teamwork", "bravery", "equipment", "protection", "lifesaving", "community"]},
    {"genre": "Journalist", "keywords": ["news", "reporting", "writing", "investigation", "truth", "stories", "editing", "media", "interviews", "communication"]},
    {"genre": "Lawyer", "keywords": ["legal advice", "courtroom", "contracts", "justice", "litigation", "negotiation", "laws", "ethics", "advocacy", "representation"]},
    {"genre": "Veterinarian", "keywords": ["animal care", "medical treatment", "pets", "compassion", "diagnosis", "surgery", "health", "livestock", "healing", "biology"]},
    {"genre": "Plumber", "keywords": ["pipes", "repairs", "water systems", "installation", "plumbing", "maintenance", "tools", "technical skills", "home systems", "sanitation"]},
    {"genre": "Detective", "keywords": ["investigation", "mystery", "clues", "evidence", "crime-solving", "analysis", "surveillance", "interviews", "deduction", "justice"]},
    {"genre": "Entrepreneur", "keywords": ["business", "startups", "innovation", "leadership", "strategy", "finance", "creativity", "risk-taking", "vision", "growth"]},
    {"genre": "Carpenter", "keywords": ["woodworking", "tools", "craftsmanship", "construction", "furniture", "repairs", "creativity", "manual skills", "design", "building"]},    
    {"genre": "Buzz Cut", "keywords": ["short hair", "military style", "clean and sharp", "low maintenance", "close shave", "faded sides", "simple style", "minimalistic look", "bold", "rugged appearance"]},
    {"genre": "Pompadour Style", "keywords": ["high volume", "slicked back", "classic style", "retro look", "elevated front", "elegant", "vintage charm", "defined shape", "volume and height", "stylish sophistication"]},
    {"genre": "Undercut Style", "keywords": ["short sides", "long top", "sharp contrast", "modern style", "clean lines", "edgy", "versatile", "defined part", "sleek", "fashion-forward"]},
    {"genre": "Buzzed Fade", "keywords": ["fade", "gradual length", "close cut", "sharp lines", "textured top", "clean look", "slick sides", "low maintenance", "masculine", "neat appearance"]},
    {"genre": "Mullet Style", "keywords": ["short front", "long back", "retro", "business in the front", "party in the back", "classic style", "wild look", "bold fashion", "punk vibe", "nostalgic"]},
    {"genre": "Quiff Style", "keywords": ["voluminous front", "styled upward", "smooth finish", "elegant", "classic", "dapper", "stylish", "pomade style", "polished", "high-end look"]},
    {"genre": "Crew Cut Style", "keywords": ["short sides", "neat top", "military-inspired", "clean and simple", "no-nonsense", "classic look", "easy to maintain", "sharp", "low maintenance", "functional style"]},
    {"genre": "Bowl Cut", "keywords": ["round shape", "straight fringe", "retro style", "90s look", "uniform length", "unique", "distinctive", "nostalgic", "geometric", "precise cut"]},
    {"genre": "Side Part Style", "keywords": ["neat", "classic style", "side-swept", "timeless", "elegant", "professional look", "simple yet sophisticated", "longer top", "clean separation", "structured hair"]},
    {"genre": "Afro Style", "keywords": ["full volume", "curly", "natural", "bold style", "rounded shape", "defined curls", "retro", "big hair", "fuzzy", "statement look"]},
    {"genre": "Man Bun Style", "keywords": ["hair gathered", "tied back", "long hair", "neat style", "casual look", "stylish", "hipster", "bohemian", "relaxed vibe", "messy chic"]},
    {"genre": "Top Knot Style", "keywords": ["short sides", "long top", "hair tied up", "sleek", "casual", "modern", "messy style", "hipster look", "practical", "hair accessory"]},
    {"genre": "Layered Cut Style", "keywords": ["textured layers", "soft volume", "natural flow", "dynamic look", "flowing hair", "versatile", "shaped ends", "voluminous", "light movement", "fashionable"]},
    {"genre": "Bob Cut", "keywords": ["straight cut", "chin-length", "classic style", "blunt ends", "chic", "stylish", "easy to manage", "modern", "elegant", "timeless"]},
    {"genre": "Shag Cut Style", "keywords": ["textured layers", "messy look", "wild style", "uneven cut", "vintage", "rock and roll", "layered fringe", "voluminous", "edgy", "carefree style"]},
    {"genre": "Long Layers Style", "keywords": ["flowing hair", "natural look", "layered ends", "soft movement", "undone style", "long and elegant", "free-flowing", "timeless", "luscious", "effortless"]},
    {"genre": "Pixie Cut Style", "keywords": ["short hair", "feminine", "edgy", "easy maintenance", "playful", "youthful", "choppy style", "soft texture", "modern", "chic"]},
    {"genre": "Flat Top Style", "keywords": ["high volume", "flat crown", "sharp lines", "90s style", "boxy look", "bold", "defined edges", "geometric", "cool", "retro"]},
    {"genre": "French Crop Style", "keywords": ["short fringe", "clean sides", "textured top", "retro style", "stylish", "angular cut", "short and sharp", "defined lines", "masculine", "neat appearance"]},
    {"genre": "Caesar Cut Style", "keywords": ["short fringe", "forward-swept", "classic", "bold", "neat and tidy", "easy to manage", "simple", "geometric", "practical", "timeless style"]},
    {"genre": "Long Loose Waves", "keywords": ["soft waves", "flowing hair", "natural texture", "beachy look", "relaxed", "effortless beauty", "voluminous", "shiny", "romantic", "bohemian"]},
    {"genre": "Bob Cut2", "keywords": ["chin-length", "straight cut", "blunt ends", "classic", "stylish", "easy to manage", "modern", "chic", "timeless", "sleek"]},
    {"genre": "Pixie Cut", "keywords": ["short hair", "feminine", "choppy style", "playful", "youthful", "edgy", "textured", "easy maintenance", "bold", "chic"]},
    {"genre": "Layered Haircut", "keywords": ["textured layers", "soft flow", "dynamic movement", "light volume", "natural shape", "bouncy", "versatile", "feminine", "soft ends", "natural look"]},
    {"genre": "Shag Cut", "keywords": ["messy look", "rock and roll", "layered fringe", "voluminous", "uneven layers", "effortless", "edgy", "carefree style", "wild", "playful"]},
    {"genre": "Straight and Sleek", "keywords": ["silky straight", "shiny", "polished", "classic style", "smooth finish", "glossy hair", "clean lines", "minimalistic", "sleek elegance", "modern"]},
    {"genre": "Braided Crown", "keywords": ["crown braid", "intricate braids", "elegant", "bohemian style", "romantic", "vintage", "classic", "soft curls", "decorative", "princess-like"]},
    {"genre": "High Ponytail", "keywords": ["sleek ponytail", "high volume", "pulled back", "neat", "sporty", "elevated", "stylish", "glamorous", "dynamic", "youthful"]},
    {"genre": "Side-Swept Curls", "keywords": ["soft curls", "side part", "romantic", "elegant", "flirty", "chic", "voluminous", "shine", "classic curls", "sophisticated"]},
    {"genre": "Top Knot", "keywords": ["hair tied up", "messy bun", "casual", "boho chic", "relaxed", "high bun", "modern", "effortless", "stylish", "practical"]},
    {"genre": "Bangs with Long Hair", "keywords": ["fringe", "soft bangs", "long hair", "face-framing", "playful", "youthful", "elegant", "straight or textured", "modern", "feminine"]},
    {"genre": "Curtain Bangs", "keywords": ["soft fringe", "parted bangs", "vintage", "retro style", "gentle waves", "flowing", "timeless", "classic", "face-framing", "effortless"]},
    {"genre": "Messy Bun", "keywords": ["casual", "loose hair", "effortless", "relaxed", "chic", "messy look", "bohemian", "easy style", "natural", "laid-back"]},
    {"genre": "Afro", "keywords": ["curly hair", "full volume", "big hair", "natural curls", "bold", "textured", "defined curls", "retro", "afrocentric", "statement look"]},
    {"genre": "Long and Straight", "keywords": ["silky", "sleek", "minimalistic", "flowing", "glossy", "smooth", "healthy shine", "elegant", "straight cut", "long length"]},
    {"genre": "Half Up Half Down", "keywords": ["half ponytail", "loose hair", "relaxed", "romantic", "elegant", "casual chic", "flirty", "soft waves", "boho", "feminine"]},
    {"genre": "Tight Curls", "keywords": ["defined curls", "voluminous", "bouncy", "full curls", "playful", "tight ringlets", "chic", "natural texture", "bold", "classic curls"]},
    {"genre": "Undercut Bob", "keywords": ["undercut", "choppy bob", "bold style", "modern", "edgy", "creative cut", "sharp lines", "fashionable", "sophisticated", "stylish"]},
    {"genre": "Fishtail Braid", "keywords": ["braided style", "intricate", "elegant", "bohemian", "delicate", "classic", "textured", "sophisticated", "timeless", "chic"]},
    {"genre": "Choppy Lob", "keywords": ["lob cut", "textured ends", "messy", "layered", "easy style", "effortless", "modern", "choppy finish", "versatile", "youthful"]},
    {"genre": "Blonde Hair", "keywords": ["light blonde", "golden blonde", "platinum blonde", "ash blonde", "strawberry blonde", "sun-kissed", "warm blonde", "bright blonde", "silky shine", "blonde highlights"]},
    {"genre": "Brunette Hair", "keywords": ["dark brown", "chocolate brown", "light brown", "medium brown", "rich brunette", "chestnut", "caramel highlights", "natural brown", "deep brown", "warm undertones"]},
    {"genre": "Black Hair", "keywords": ["jet black", "dark black", "natural black", "midnight black", "shiny black", "deep black", "sleek black", "soft black", "glossy black", "sharp black"]},
    {"genre": "Red Hair", "keywords": ["fiery red", "cherry red", "auburn", "deep red", "bright red", "copper red", "ginger", "strawberry red", "intense red", "vivid red"]},
    {"genre": "Platinum Blonde Hair", "keywords": ["icy blonde", "silvery blonde", "frosted blonde", "cool blonde", "light platinum", "almost white blonde", "bleached blonde", "clear blonde", "extremely light blonde", "frosty sheen"]},
    {"genre": "Silver Hair", "keywords": ["gray hair", "silver strands", "aging gracefully", "platinum silver", "shiny gray", "frosty gray", "cool silver", "metallic silver", "snowy silver", "elegant silver"]},
    {"genre": "Ombre Hair", "keywords": ["gradient effect", "dark roots", "lighter tips", "blended shades", "sun-kissed ombre", "smooth transition", "ombre balayage", "light to dark", "natural fade", "subtle ombre"]},
    {"genre": "Burgundy Hair", "keywords": ["rich red", "dark red", "wine red", "burgundy hue", "deep burgundy", "vibrant burgundy", "reddish-brown", "warm burgundy", "berry tone", "luxury red"]},
    {"genre": "Pink Hair", "keywords": ["pastel pink", "bright pink", "cotton candy pink", "hot pink", "rose pink", "fuchsia", "magenta", "light pink", "vivid pink", "bold pink"]},
    {"genre": "Blue Hair", "keywords": ["turquoise hair", "sea blue", "electric blue", "pastel blue", "midnight blue", "royal blue", "aqua hair", "neon blue", "icy blue", "bold blue"]},
    {"genre": "Purple Hair", "keywords": ["lavender hair", "violet hair", "plum hair", "magenta hair", "lilac hair", "dark purple hair", "deep violet", "bold purple", "rich purple", "faded purple"]},
    {"genre": "Green Hair", "keywords": ["emerald hair", "mint green hair", "neon green hair", "grass green hair", "dark green hair", "forest green hair", "sea green hair", "bright green hair", "lime green hair", "electric green"]},
    {"genre": "Grey Hair", "keywords": ["silver grey hair", "stormy grey hair", "salt-and-pepper hair", "platinum grey", "charcoal grey hair", "steel grey", "cool grey", "soft grey", "shiny grey", "sophisticated grey"]},
    {"genre": "White Hair", "keywords": ["snow white hair", "pure white hair", "silver-white hair", "icy white hair", "ivory hair", "pearl white hair", "chalk white hair", "bright white hair", "frosted white hair", "blinding white"]},
    {"genre": "Brown Hair", "keywords": ["light brown hair", "dark brown hair", "medium brown hair", "rich brown hair", "warm brown hair", "coffee brown hair", "chocolate brown hair", "chestnut brown hair", "caramel brown hair", "earthy brown hair"]},
    {"genre": "Copper Hair", "keywords": ["burnt orange hair", "copper-red hair", "fiery copper hair", "rich copper hair", "copper highlights", "rust copper hair", "reddish copper hair", "bold copper hair", "copper shine", "vivid copper hair"]},
    {"genre": "Lavender Hair", "keywords": ["light lavender hair", "pastel lavender hair", "lavender purple hair", "light purple hair", "faded lavender hair", "soft lavender hair", "elegant lavender", "shiny lavender hair", "bright lavender hair", "delicate lavender"]},
    {"genre": "Yellow Hair", "keywords": ["bright yellow hair", "neon yellow hair", "yellow blonde hair", "golden yellow hair", "canary yellow hair", "lemon yellow hair", "sunshine yellow hair", "vivid yellow hair", "pale yellow hair", "yellow highlights"]},
    {"genre": "Orange Hair", "keywords": ["bright orange hair", "pumpkin orange hair", "fiery orange hair", "neon orange hair", "light orange hair", "dark orange hair", "burnt orange hair", "deep orange hair", "copper orange hair", "bold orange hair"]},
    {"genre": "Turquoise Hair", "keywords": ["aqua turquoise hair", "light turquoise hair", "dark turquoise hair", "neon turquoise hair", "vivid turquoise hair", "cool turquoise", "icy turquoise", "electric turquoise", "deep turquoise", "bold turquoise"]},
    {"genre": "Peach Hair", "keywords": ["soft peach hair", "light peach hair", "warm peach hair", "peachy tones", "peach blonde hair", "pastel peach hair", "peach highlights", "bright peach hair", "delicate peach", "sunset peach"]},
    {"genre": "Charcoal Hair", "keywords": ["dark charcoal hair", "grey charcoal hair", "light charcoal hair", "black charcoal hair", "steel charcoal hair", "smoky charcoal hair", "deep charcoal", "subtle charcoal hair", "charcoal highlights", "matte charcoal"]},
    {"genre": "Bronze Hair", "keywords": ["metallic bronze hair", "light bronze hair", "dark bronze hair", "rich bronze hair", "coppery bronze hair", "warm bronze hair", "brassy bronze", "shiny bronze", "luxurious bronze hair", "vivid bronze highlights"]},
    {"genre": "Pink Blonde Hair", "keywords": ["blonde pink hair", "rose gold blonde", "peach pink blonde", "light pink blonde", "subtle pink blonde", "blonde with pink highlights", "cool pink blonde", "warm pink blonde", "pastel pink blonde", "blush blonde hair"]},    
    {"genre": "Cat-Human Hybrid", "keywords": ["sharp feline features", "slender build", "pointed ears", "tail", "agile movements", "whiskers", "cat-like eyes", "clawed hands", "graceful posture", "feline agility"]},
    {"genre": "Wolf-Human Hybrid", "keywords": ["fur-covered body", "canine features", "sharp fangs", "wolf-like eyes", "strong build", "pointed ears", "predatory stance", "muscular legs", "keen senses", "animalistic instincts"]},
    {"genre": "Bird-Human Hybrid", "keywords": ["feathered wings", "beak-like nose", "bird-like posture", "sharp eyes", "light build", "quick movements", "colorful feathers", "flying ability", "elongated limbs", "avian characteristics"]},
    {"genre": "Horse-Human Hybrid", "keywords": ["muscular legs", "horse-like features", "mane of hair", "tall stature", "hooves", "strong build", "powerful legs", "long neck", "speed and grace", "stable posture"]},
    {"genre": "Lion-Human Hybrid", "keywords": ["majestic mane", "muscular build", "lion-like eyes", "sharp claws", "royal posture", "ferocious stance", "feline grace", "strength and power", "large body", "noble presence"]},
    {"genre": "Snake-Human Hybrid", "keywords": ["slithering movements", "scaly skin", "forked tongue", "serpentine eyes", "long, flexible body", "reptilian features", "venomous fangs", "smooth posture", "predatory appearance", "stealthy movement"]},
    {"genre": "Tiger-Human Hybrid", "keywords": ["striped fur", "muscular build", "sharp claws", "tiger-like eyes", "agile movements", "ferocious demeanor", "orange fur", "prowling stance", "wild power", "predatory instincts"]},
    {"genre": "Bear-Human Hybrid", "keywords": ["large frame", "thick fur", "bear-like claws", "muscular arms", "powerful legs", "strong posture", "animal strength", "wide chest", "sturdy build", "protective nature"]},
    {"genre": "Fox-Human Hybrid", "keywords": ["fluffy tail", "pointed ears", "fox-like eyes", "agile movements", "cunning expression", "sharp features", "slender build", "quick reflexes", "bright fur", "mysterious presence"]},
    {"genre": "Shark-Human Hybrid", "keywords": ["sharp teeth", "scaly skin", "powerful build", "aquatic features", "fins", "sleek body", "sharp senses", "predatory behavior", "swimming abilities", "aquatic strength"]},
    {"genre": "Elephant-Human Hybrid", "keywords": ["large ears", "trunk", "massive build", "thick skin", "strong limbs", "gentle giant", "broad shoulders", "heavyset body", "sturdy presence", "elephant-like grace"]},
    {"genre": "Rabbit-Human Hybrid", "keywords": ["long ears", "small frame", "bunny-like features", "quick movements", "soft fur", "floppy ears", "large eyes", "small nose", "agile and fast", "cute appearance"]},
    {"genre": "Cheetah-Human Hybrid", "keywords": ["lean body", "muscular legs", "cheetah-like speed", "fast reflexes", "spotted fur", "graceful stride", "sharp claws", "predatory focus", "sleek build", "quick movements"]},
    {"genre": "Kangaroo-Human Hybrid", "keywords": ["powerful legs", "tail", "hopping movement", "muscular frame", "large feet", "kangaroo-like posture", "strong jumps", "agile body", "spring-like motions", "heightened reflexes"]},
    {"genre": "Gorilla-Human Hybrid", "keywords": ["large frame", "muscular arms", "thick fur", "powerful chest", "strong jawline", "dominant presence", "intelligent expression", "broad shoulders", "fierce demeanor", "primate features"]},
    {"genre": "Dragon-Human Hybrid", "keywords": ["scaled skin", "wings", "fire-breathing", "dragon-like claws", "long tail", "sharp teeth", "majestic wingspan", "powerful build", "fire powers", "reptilian features"]},
    {"genre": "Lizard-Human Hybrid", "keywords": ["scaly skin", "long tongue", "cold-blooded nature", "slender body", "quick movements", "reptilian eyes", "sharp claws", "creeping stance", "long tail", "predatory gaze"]},
    {"genre": "Bat-Human Hybrid", "keywords": ["bat-like wings", "sharp hearing", "nocturnal traits", "slim build", "black wings", "claw-like fingers", "sensitive hearing", "flying abilities", "dark presence", "sharp vision"]},
    {"genre": "Octopus-Human Hybrid", "keywords": ["tentacles", "aquatic features", "soft, flexible body", "sharp mind", "multifaceted eyes", "swimming abilities", "flexible limbs", "reaching appendages", "intelligent expression", "adaptable body"]},
    {"genre": "Frog-Human Hybrid", "keywords": ["webbed hands", "amphibian skin", "long limbs", "big eyes", "powerful jumps", "small, agile body", "slim figure", "greenish tones", "sticky hands", "hopping abilities"]},
    {"genre": "Panther-Human Hybrid", "keywords": ["sleek black fur", "predatory grace", "sharp claws", "agile movements", "panther-like eyes", "stealthy posture", "muscular legs", "night vision", "feline agility", "sinuous body"]},
    {"genre": "Rhino-Human Hybrid", "keywords": ["thick skin", "horned head", "muscular build", "powerful legs", "rough texture", "strong stature", "imposing presence", "broad shoulders", "heavy-set body", "rhino-like features"]},
    {"genre": "Mantis-Human Hybrid", "keywords": ["sharp limbs", "exquisite exoskeleton", "bug-like eyes", "insect-like posture", "quick reflexes", "powerful arms", "greenish tones", "praying mantis traits", "elongated limbs", "predatory stance"]},
    {"genre": "Crocodile-Human Hybrid", "keywords": ["scaly body", "sharp teeth", "powerful jaws", "long tail", "reptilian features", "water-dwelling traits", "broad body", "predator-like eyes", "muscular build", "fast reflexes"]},
    {"genre": "Swan-Human Hybrid", "keywords": ["graceful neck", "feathered wings", "white feathers", "elegant posture", "slender body", "long, fluid movements", "delicate wings", "beauty and grace", "serene expression", "avian characteristics"]},
    {"genre": "Zebra-Human Hybrid", "keywords": ["black and white stripes", "muscular build", "zebra-like eyes", "strong legs", "graceful movement", "striped fur", "herbivore traits", "slender build", "wild posture", "zebra-striped skin"]},
    {"genre": "Giraffe-Human Hybrid", "keywords": ["long neck", "tall frame", "elevated stance", "gentle expression", "large eyes", "spotted fur", "elegant movements", "powerful legs", "herbivore features", "graceful reach"]},
    {"genre": "Antelope-Human Hybrid", "keywords": ["slender body", "graceful movements", "horns", "athletic build", "long legs", "quick reflexes", "agile posture", "light footed", "smooth fur", "keen eyes"]},
    {"genre": "Lionfish-Human Hybrid", "keywords": ["flowing fins", "colorful patterns", "sharp spines", "fish-like gills", "aquatic features", "elegant stance", "scaly skin", "brightly colored patterns", "marine aesthetic", "swimming abilities"]},
    {"genre": "Hawk-Human Hybrid", "keywords": ["sharp beak", "feathered wings", "keen eyes", "muscular limbs", "swift movement", "predatory posture", "bird of prey features", "fast reflexes", "eagle-like features", "flying ability"]},
    {"genre": "Scorpion-Human Hybrid", "keywords": ["sharp pincers", "curved tail", "stinger", "scaly skin", "eight limbs", "fast, powerful strikes", "exoskeleton", "predatory features", "dangerous posture", "aggressive stance"]},
    {"genre": "Wolf-Spirit-Human Hybrid", "keywords": ["ethereal wolf features", "translucent fur", "mystical glow", "powerful aura", "spiritual connection", "supernatural presence", "strong body", "noble wolf-like features", "elemental power", "wild spirit"]},
    {"genre": "Beetle-Human Hybrid", "keywords": ["shiny carapace", "hard exoskeleton", "beetle-like legs", "sharp mandibles", "multifaceted eyes", "slender limbs", "heavy build", "quick scuttling movement", "insectoid traits", "armor-like appearance"]},
    {"genre": "Camel-Human Hybrid", "keywords": ["desert features", "hump", "thick skin", "powerful legs", "tough exterior", "camel-like posture", "long eyelashes", "adaptable features", "muscular legs", "survival traits"]},
    {"genre": "Otter-Human Hybrid", "keywords": ["water-loving", "slender body", "playful nature", "webbed hands", "short fur", "quick reflexes", "aquatic agility", "swimming traits", "graceful movements", "curious expression"]},
    {"genre": "Wolverine-Human Hybrid", "keywords": ["sharp claws", "fierce expression", "muscular build", "powerful jaws", "scruffy fur", "tenacious demeanor", "sturdy posture", "wild animal traits", "aggressive stance", "survival instincts"]},
    {"genre": "Chameleon-Human Hybrid", "keywords": ["color-changing skin", "camouflage ability", "reptilian features", "long tongue", "sharp vision", "slow movements", "high adaptability", "quiet presence", "climbing ability", "chameleon-like behavior"]},
    {"genre": "Penguin-Human Hybrid", "keywords": ["short legs", "flipper-like arms", "black and white feathers", "aquatic abilities", "social behavior", "fatty build", "slow movements", "cute expression", "penguin traits", "playful demeanor"]},
    {"genre": "Jaguar-Human Hybrid", "keywords": ["muscular build", "jaguar-like spots", "predatory grace", "strong limbs", "sharp claws", "intense focus", "fast reflexes", "stealthy movements", "feline traits", "wild energy"]},
    {"genre": "Cheetah-Spirit-Human Hybrid", "keywords": ["ethereal body", "glowing spots", "translucent fur", "supernatural speed", "pristine grace", "fast reflexes", "powerful legs", "wild spirit", "animal essence", "mystical power"]}, 
    {"genre": "NeoGeo", "keywords": ["released in 1990", "arcade-quality games", "King of Fighters", "Samurai Shodown", "Metal Slug", "highly expensive", "SNK", "CD-based and cartridge versions", "famous for fighting games", "premium console"]},
    {"genre": "Magnavox Odyssey", "keywords": ["first home video game console", "released in 1972", "black-and-white graphics", "paddle controllers", "no microprocessor", "no sound", "limited games", "primitive", "simple gameplay", "Pong-inspired"]},
    {"genre": "Atari 2600", "keywords": ["released in 1977", "home console", "cartridge-based", "joystick controller", "first major video game console", "Pong", "iconic graphics", "Space Invaders", "Pac-Man", "E.T. the Extra-Terrestrial"]},
    {"genre": "Nintendo Entertainment System (NES)", "keywords": ["released in 1985", "8-bit console", "Super Mario Bros.", "Metroid", "Zelda", "pioneered home console gaming", "game cartridges", "two-button controller", "multi-tiered gameplay", "iconic"]},
    {"genre": "Sega Genesis", "keywords": ["released in 1988", "16-bit console", "Sonic the Hedgehog", "Street Fighter", "Mortal Kombat", "popular in North America", "arcade-quality games", "innovative controllers", "multiplayer support", "blast processing"]},
    {"genre": "Super Nintendo Entertainment System (SNES)", "keywords": ["released in 1990", "16-bit console", "Super Mario World", "The Legend of Zelda: A Link to the Past", "Donkey Kong Country", "Yoshi's Island", "colorful graphics", "innovative RPGs", "mode 7 graphics", "action-packed"]},
    {"genre": "Sony PlayStation", "keywords": ["released in 1994", "CD-based", "Gran Turismo", "Final Fantasy VII", "3D graphics", "DVD player", "DualShock controller", "vibrational feedback", "large game library", "Sony's first console"]},
    {"genre": "Nintendo 64", "keywords": ["released in 1996", "64-bit console", "Super Mario 64", "GoldenEye 007", "The Legend of Zelda: Ocarina of Time", "expansion pack support", "innovative 3D gameplay", "four controller ports", "analog stick", "cutting-edge graphics"]},
    {"genre": "Sony PlayStation 2", "keywords": ["released in 2000", "DVD-compatible", "Grand Theft Auto: San Andreas", "Final Fantasy X", "largest game library", "backward compatibility", "online multiplayer", "improved graphics", "best-selling console", "PlayStation exclusive games"]},
    {"genre": "Xbox", "keywords": ["released in 2001", "Microsoft's first console", "Halo: Combat Evolved", "online gaming via Xbox Live", "high-definition graphics", "integrated DVD player", "multiplayer-focused", "innovative controller", "direct access to media", "powerful hardware"]},
    {"genre": "Nintendo Wii", "keywords": ["released in 2006", "motion-sensing controllers", "Wii Sports", "Casual gaming", "family-friendly games", "innovative gameplay", "Wii Fit", "motion control revolution", "Wii Party", "budget-friendly"]},
    {"genre": "PlayStation 3", "keywords": ["released in 2006", "Blu-ray player", "Uncharted 2: Among Thieves", "Gran Turismo 5", "HD graphics", "PlayStation Network", "DualShock 3", "cross-platform multiplayer", "advanced processing power", "media center functionality"]},
    {"genre": "Xbox 360", "keywords": ["released in 2005", "online gaming via Xbox Live", "Halo 3", "Kinect support", "multimedia entertainment", "game streaming", "high-definition graphics", "Xbox Live Arcade", "DVD player", "popular among core gamers"]},
    {"genre": "Nintendo 3DS", "keywords": ["released in 2011", "3D gaming without glasses", "Super Mario 3D Land", "Pokémon X and Y", "augmented reality", "touchscreen", "portable console", "dual screens", "StreetPass functionality", "cross-platform play"]},
    {"genre": "PlayStation 4", "keywords": ["released in 2013", "8-core AMD processor", "The Last of Us Part II", "Spider-Man", "Death Stranding", "4K video streaming", "social integration", "Share button", "DualShock 4 controller", "massive game library"]},
    {"genre": "Xbox One", "keywords": ["released in 2013", "1080p graphics", "Halo 5: Guardians", "Kinect 2.0", "cloud gaming", "multimedia integration", "voice control", "backward compatibility", "digital rights management", "Xbox Game Pass"]},
    {"genre": "Nintendo Switch", "keywords": ["released in 2017", "hybrid portable console", "The Legend of Zelda: Breath of the Wild", "Super Mario Odyssey", "multiplayer support", "Joy-Con controllers", "touchscreen", "Nintendo exclusive titles", "motion controls", "innovative design"]},
    {"genre": "PlayStation 5", "keywords": ["released in 2020", "8K graphics", "Demon's Souls", "Spider-Man: Miles Morales", "faster load times", "DualSense controller", "3D audio", "backward compatibility", "Ray Tracing", "PlayStation exclusives"]},
    {"genre": "Xbox Series X", "keywords": ["released in 2020", "12 teraflops processing power", "Halo Infinite", "backward compatibility", "Quick Resume", "Game Pass", "4K gaming", "Xbox Live Gold", "Smart Delivery", "powerful performance"]},
    {"genre": "Nintendo Switch OLED", "keywords": ["released in 2021", "improved screen", "portable design", "enhanced audio", "Super Smash Bros. Ultimate", "Mario Kart 8 Deluxe", "Joy-Con drift improvements", "upgraded dock", "higher-quality visuals", "better portability"]},
    {"genre": "PlayStation VR", "keywords": ["released in 2016", "virtual reality", "immersive gaming", "exclusive VR titles", "virtual reality headset", "motion tracking", "PlayStation Move controllers", "first-person experiences", "multiplayer VR support", "motion-controlled gameplay"]},     
    {"genre": "Blue Eyes", "keywords": ["deep blue eyes", "ocean blue eyes", "clear blue eyes", "light blue eyes", "electric blue eyes", "icy blue eyes", "vivid blue eyes", "sky blue eyes", "bright blue eyes", "crystal blue eyes"]},
    {"genre": "Green Eyes", "keywords": ["emerald green eyes", "bright green eyes", "deep green eyes", "hazel green eyes", "forest green eyes", "light green eyes", "vivid green eyes", "pale green eyes", "rich green eyes", "mint green eyes"]},
    {"genre": "Brown Eyes", "keywords": ["dark brown eyes", "light brown eyes", "chocolate brown eyes", "warm brown eyes", "hazel brown eyes", "deep brown eyes", "golden brown eyes", "amber brown eyes", "rich brown eyes", "earthy brown eyes"]},
    {"genre": "Gray Eyes", "keywords": ["steel gray eyes", "stormy gray eyes", "light gray eyes", "dark gray eyes", "pearl gray eyes", "silver gray eyes", "smoky gray eyes", "misty gray eyes", "cool gray eyes", "pale gray eyes"]},
    {"genre": "Amber Eyes", "keywords": ["golden amber eyes", "light amber eyes", "rich amber eyes", "bright amber eyes", "honey amber eyes", "deep amber eyes", "dark amber eyes", "fiery amber eyes", "warm amber eyes", "vivid amber eyes"]},
    {"genre": "Purple Eyes", "keywords": ["vivid purple eyes", "deep purple eyes", "lavender purple eyes", "bright purple eyes", "soft purple eyes", "mysterious purple eyes", "dark purple eyes", "violet purple eyes", "intense purple eyes", "magical purple eyes"]},
    {"genre": "Heterochromia", "keywords": ["two different colored eyes", "one blue and one green eye", "one brown and one green eye", "heterochromatic eyes", "bicolor eyes", "unequal eyes", "unique eyes", "striking heterochromia", "rare eye color", "contrasting eyes"]},
    {"genre": "Black Eyes", "keywords": ["solid black eyes", "deep black eyes", "dark as night eyes", "shadowy black eyes", "mysterious black eyes", "pure black eyes", "inky black eyes", "intense black eyes", "smooth black eyes", "pitch black eyes"]},
    {"genre": "White Eyes", "keywords": ["glowing white eyes", "pale white eyes", "pure white eyes", "milky white eyes", "intense white eyes", "bright white eyes", "almost translucent white eyes", "snowy white eyes", "angelic white eyes", "soft white eyes"]},
    {"genre": "Red Eyes", "keywords": ["crimson red eyes", "vivid red eyes", "deep red eyes", "fiery red eyes", "blood red eyes", "bright red eyes", "scarlet red eyes", "dark red eyes", "ruby red eyes", "piercing red eyes"]},
    {"genre": "Casual Wear", "keywords": ["comfortable clothing", "relaxed fit", "everyday outfit", "jeans and t-shirt", "laid-back style", "simple attire", "easygoing fashion", "casual chic", "informal dress", "streetwear"]},
    {"genre": "Formal Wear", "keywords": ["elegant suit", "tailored outfit", "dress shirt", "formal dress", "classic tuxedo", "black tie", "luxurious fabrics", "polished appearance", "refined style", "gala attire"]},
    {"genre": "Sportswear", "keywords": ["athletic clothing", "gym wear", "sportswear fashion", "tracksuit", "running gear", "activewear", "performance fabrics", "fitness attire", "comfortable workout clothes", "sporty look"]},
    {"genre": "Business Casual", "keywords": ["blazer", "dress slacks", "button-up shirt", "polo shirt", "smart trousers", "knee-length skirt", "dress shoes", "polished look", "professional attire", "workplace style"]},
    {"genre": "Bohemian Style", "keywords": ["flowy fabrics", "earthy tones", "relaxed fit", "layered clothing", "patterned dresses", "fringe details", "hippie chic", "vintage-inspired", "casual yet artistic", "ethereal look"]},
    {"genre": "Streetwear", "keywords": ["urban fashion", "graphic t-shirt", "hoodie", "sneakers", "cargo pants", "oversized clothing", "bold prints", "skate-inspired", "high fashion street style", "contemporary casual"]},
    {"genre": "Vintage Clothing", "keywords": ["retro style", "1950s fashion", "60s dresses", "70s bell bottoms", "80s neon colors", "vintage patterns", "antique fabrics", "nostalgic style", "old-school chic", "timeless fashion"]},
    {"genre": "Luxury Fashion", "keywords": ["high-end designer", "couture dresses", "elegant tailoring", "fine materials", "luxurious accessories", "brand name clothing", "exclusive styles", "expensive fabrics", "glamorous look", "runway fashion"]},
    {"genre": "Gothic Fashion", "keywords": ["dark colors", "leather jackets", "black lace", "chokers", "platform boots", "victorian elements", "spiked accessories", "rebellious style", "dramatic attire", "subculture fashion"]},
    {"genre": "Athleisure", "keywords": ["athletic wear", "yoga pants", "sports bra", "comfortable fit", "breathable fabrics", "sporty and stylish", "casual yet functional", "active lifestyle clothing", "workout to street", "chic gym attire"]},
    {"genre": "Cottagecore", "keywords": ["floral dresses", "pastel colors", "rural chic", "lace details", "earthy tones", "vintage patterns", "cozy aesthetic", "comfortable and feminine", "botanical prints", "romantic countryside style"]},
    {"genre": "Punk Fashion", "keywords": ["leather jackets", "spiked collars", "band t-shirts", "ripped jeans", "anarchy symbols", "edgy accessories", "grunge boots", "rebellious spirit", "punk rock look", "alternative fashion"]},
    {"genre": "Preppy Style", "keywords": ["polos", "khakis", "blazers", "sweater vests", "boat shoes", "collared shirts", "classical sophistication", "bright colors", "clean-cut look", "school uniform-inspired"]},
    {"genre": "Minimalist Style", "keywords": ["simple designs", "monochrome clothing", "clean lines", "neutral colors", "functional fashion", "clutter-free", "basic pieces", "quiet elegance", "refined simplicity", "modern aesthetics"]},
    {"genre": "Renaissance Clothing", "keywords": ["corsets", "flowing skirts", "velvet fabrics", "elaborate gowns", "ruffles and lace", "royal attire", "gold accents", "period costume", "intricate patterns", "medieval style"]},
    {"genre": "Cyberpunk Fashion", "keywords": ["futuristic clothing", "neon accents", "tech-inspired", "high-tech fabrics", "urban dystopia", "sleek and modern", "synthetic materials", "reflective surfaces", "glowing accessories", "dark city vibes"]},
    {"genre": "Steampunk FashionB", "keywords": ["Victorian-inspired", "goggles", "leather gloves", "brass accessories", "industrial chic", "corsets and waistcoats", "steampunk gears", "clockwork elements", "retro-futuristic style", "high boots"]},
    {"genre": "Sailor Style", "keywords": ["nautical stripes", "sailor collars", "marine colors", "white and navy", "anchor prints", "summer dresses", "casual elegance", "seafaring look", "nautical accessories", "coastal chic"]},
    {"genre": "Fairy Tale Clothing", "keywords": ["princess dresses", "magical gowns", "sparkling accessories", "whimsical details", "glittering fabrics", "storybook style", "enchanted fashion", "royal attire", "fantastical look", "dreamlike clothing"]},
    {"genre": "Reggaeton Style", "keywords": ["bold colors", "tight-fitting clothes", "street style", "graphic tees", "sneakers", "track pants", "flashy accessories", "urban fashion", "hip-hop influence", "party-ready look"]},
    {"genre": "Rockstar Fashion", "keywords": ["leather jackets", "band t-shirts", "ripped jeans", "combat boots", "studs and spikes", "musical influence", "rebellious attitude", "grunge vibe", "iconic accessories", "casual rock look"]},
    {"genre": "Victorian Fashion", "keywords": ["corsets", "bustled skirts", "lace details", "floral patterns", "buttoned coats", "elegant gloves", "high collars", "vintage fabrics", "rich textures", "refined elegance"]},
    {"genre": "Western Wear", "keywords": ["cowboy boots", "denim jeans", "flannel shirts", "wide-brimmed hats", "belt buckles", "leather vests", "cowgirl dresses", "ponchos", "country-inspired", "rancher chic"]},
    {"genre": "Techwear", "keywords": ["futuristic designs", "high-performance fabrics", "minimalist clothing", "dark colors", "utility belts", "cargo pants", "weather-resistant gear", "urban fashion", "performance clothing", "tech-inspired accessories"]},
    {"genre": "Boho Chic", "keywords": ["bohemian dresses", "long flowing skirts", "fringe accessories", "earthy tones", "casual elegance", "layered clothing", "patterns and prints", "ethnic jewelry", "hippie style", "free-spirited fashion"]},
    {"genre": "Haute Couture", "keywords": ["exclusive designs", "luxurious fabrics", "high fashion", "runway styles", "tailored gowns", "fashion-forward", "embellished accessories", "avant-garde", "refined elegance", "timeless luxury"]},
    {"genre": "Grunge Style", "keywords": ["flannel shirts", "ripped jeans", "combat boots", "band t-shirts", "oversized clothing", "dark makeup", "rebellious attitude", "vintage accessories", "casual punk vibe", "alternative look"]},
    {"genre": "Maternity Fashion", "keywords": ["comfortable fit", "stretch fabrics", "supportive clothing", "elegant dresses", "casual wear", "stylish maternity", "baby bump-friendly", "soft fabrics", "loose fitting", "fashionable during pregnancy"]},
    {"genre": "Futuristic Fashion", "keywords": ["space-age designs", "metallic fabrics", "sleek cuts", "glowing accessories", "neon colors", "tech-inspired", "dynamic structures", "high-tech materials", "cutting-edge fashion", "sci-fi influences"]},
    {"genre": "Urban Fashion", "keywords": ["streetwear", "oversized hoodies", "baggy jeans", "sneakers", "graphic tees", "baseball caps", "casual yet cool", "youthful style", "bold accessories", "city-inspired"]},
    {"genre": "Mod Fashion", "keywords": ["1960s style", "geometric patterns", "bold colors", "mini skirts", "shiny fabrics", "short haircuts", "retro vibe", "youthful energy", "sixties chic", "clean lines"]},
    {"genre": "Punk Rock Fashion", "keywords": ["leather jackets", "studded belts", "spiked hair", "bandanas", "safety pins", "ripped clothing", "combat boots", "rebellious look", "DIY fashion", "anti-establishment style"]},
    {"genre": "Preppy Fashion", "keywords": ["button-down shirts", "khakis", "blazers", "boat shoes", "cardigans", "collared dresses", "polos", "neat and tidy", "smart casual", "classic look"]},
    {"genre": "Tropical Fashion", "keywords": ["bright colors", "floral prints", "loose fitting", "summer dresses", "sundresses", "flip-flops", "wide-brimmed hats", "casual beachwear", "fun accessories", "vacation-ready clothing"]},
    {"genre": "Cyberpunk Streetwear", "keywords": ["neon lights", "futuristic fabrics", "layered clothing", "urban grit", "high-tech materials", "street attitude", "cyberpunk accessories", "sci-fi fashion", "reflective clothing", "glowing elements"]},
    {"genre": "Indie Style", "keywords": ["vintage clothing", "floral patterns", "casual chic", "quirky accessories", "artsy vibe", "boho influence", "retro-inspired", "soft fabrics", "minimalistic approach", "creative expression"]},
    {"genre": "Retro 80s Fashion", "keywords": ["neon colors", "sweatshirts", "leggings", "high-waisted jeans", "bold prints", "fanny packs", "scrunchies", "oversized jackets", "vintage sneakers", "dance party look"]},
    {"genre": "Minimalist Streetwear", "keywords": ["simple clothing", "neutral colors", "clean lines", "monochrome look", "functional fashion", "casual yet stylish", "no frills", "understated elegance", "easy fashion", "quiet sophistication"]},
    {"genre": "Red Clothing", "keywords": ["bold red", "passionate tones", "vibrant red", "fiery hues", "powerful energy", "red dress", "scarlet shades", "crimson clothing", "elegant red", "warm and intense"]},
    {"genre": "Blue Clothing", "keywords": ["calm blue", "cool tones", "sky blue", "navy shades", "deep blue", "azure garments", "sea-inspired colors", "relaxed and peaceful", "blue dress", "classic blue"]},
    {"genre": "Black Clothing", "keywords": ["classic black", "elegant darkness", "sleek black", "mysterious tones", "sophisticated black", "nighttime attire", "dark wardrobe", "black dress", "chic elegance", "formal black"]},
    {"genre": "White Clothing", "keywords": ["pure white", "fresh and clean", "light hues", "minimalist style", "elegant white", "crisp white", "soft white fabrics", "bright and light", "timeless white", "neutral tones"]},
    {"genre": "Pink Clothing", "keywords": ["soft pink", "romantic shades", "vibrant pink", "rosy tones", "feminine hues", "delicate pink", "playful pink", "feminine elegance", "light and airy pink", "flirty colors"]},
    {"genre": "Green Clothing", "keywords": ["fresh green", "earthy tones", "sage green", "forest green", "vibrant greenery", "olive clothing", "lush hues", "natural colors", "subtle greens", "peaceful greens"]},
    {"genre": "Yellow Clothing", "keywords": ["sunny yellow", "bright yellow", "cheerful tones", "lemon hues", "vibrant yellow", "golden shades", "playful yellow", "warm sunshine", "youthful yellow", "energetic color"]},
    {"genre": "Orange Clothing", "keywords": ["vibrant orange", "bold orange", "fiery orange", "citrus colors", "warm and inviting", "autumn orange", "bright orange", "energizing color", "playful orange", "stylish orange"]},
    {"genre": "Purple Clothing", "keywords": ["regal purple", "luxurious violet", "mystical shades", "deep purple", "lavender tones", "royal purple", "soft lavender", "majestic purple", "elegant purples", "luxury fashion"]},
    {"genre": "Gray Clothing", "keywords": ["cool gray", "neutral gray", "modern gray", "soft gray", "subtle tones", "urban gray", "contemporary gray", "muted shades", "chic gray", "minimalist gray"]},
    {"genre": "Brown Clothing", "keywords": ["earthy brown", "warm browns", "rustic shades", "leather tones", "chocolate hues", "natural colors", "deep browns", "wooden tones", "earthy elegance", "autumn-inspired"]},
    {"genre": "Beige Clothing", "keywords": ["soft beige", "neutral beige", "subtle tones", "light brown", "warm neutrals", "classic beige", "simple elegance", "timeless beige", "earthy beige", "warm and inviting"]},
    {"genre": "Silver Clothing", "keywords": ["shiny silver", "metallic sheen", "sleek silver", "glittery fabric", "futuristic silver", "elegant silver", "bright metallic", "dazzling silver", "luxurious shimmer", "silver accessories"]},
    {"genre": "Gold Clothing", "keywords": ["rich gold", "luxurious golden hues", "elegant gold", "shiny gold fabric", "rich metallic", "glowing gold", "opulent gold", "golden details", "vibrant golden", "timeless gold"]},
    {"genre": "Multicolor Clothing", "keywords": ["vibrant multicolors", "rainbow hues", "bold patterns", "colorful design", "playful colors", "mix of tones", "dynamic style", "cheerful clothing", "eye-catching colors", "bright fabrics"]},
    {"genre": "Pastel Clothing", "keywords": ["soft pastels", "light tones", "subtle pastel colors", "baby blue", "mint green", "peachy shades", "gentle pastels", "calming hues", "delicate fabrics", "subdued colors"]},
    {"genre": "Metallic Clothing", "keywords": ["shiny metallic", "glimmering fabrics", "futuristic shine", "silvery tones", "golden metallic", "glittery textures", "sparkling outfits", "metallic sheen", "luxury fashion", "reflective clothing"]},
    {"genre": "Camouflage Clothing", "keywords": ["military green", "camo patterns", "earth tones", "camouflage designs", "urban camouflage", "outdoor clothing", "tactical wear", "rugged look", "camo accessories", "stealthy designs"]},
    {"genre": "Tie-Dye Clothing", "keywords": ["vibrant tie-dye", "colorful swirls", "retro patterns", "boho style", "psychedelic designs", "multicolor fabrics", "playful patterns", "summer wear", "vibrant clothing", "funky fashion"]},
    {"genre": "Slim Silhouette", "keywords": ["lean body", "slender figure", "delicate proportions", "narrow waist", "graceful lines", "elegant posture", "small frame", "fit appearance", "tall and thin", "defined features"]},
    {"genre": "Curvy Silhouette", "keywords": ["full-figured body", "round curves", "voluptuous shape", "hourglass figure", "soft lines", "feminine proportions", "busty appearance", "wide hips", "smooth curves", "seductive silhouette"]},
    {"genre": "Athletic Silhouette", "keywords": ["muscular build", "toned physique", "strong limbs", "defined muscles", "active appearance", "fit body", "chiseled torso", "healthy physique", "powerful stance", "sporty look"]},
    {"genre": "Petite Silhouette", "keywords": ["small frame", "compact figure", "short stature", "delicate proportions", "tiny body", "slender build", "graceful size", "slim and petite", "youthful appearance", "understated elegance"]},
    {"genre": "Tall Silhouette", "keywords": ["long limbs", "heightened frame", "elegant posture", "stretching figure", "statuesque body", "graceful tallness", "long and slender", "svelte appearance", "lean and tall", "tall and elegant"]},
    {"genre": "Plus-Size Silhouette", "keywords": ["full-figured body", "larger proportions", "round appearance", "soft curves", "comfortable appearance", "voluptuous figure", "wider frame", "full body", "natural beauty", "confident body"]},
    {"genre": "Muscular Silhouette", "keywords": ["bulging muscles", "strong frame", "athletic build", "defined strength", "beefy appearance", "powerful torso", "muscle definition", "robust physique", "muscular arms", "physically strong"]},
    {"genre": "Hourglass Silhouette", "keywords": ["defined waist", "curved body", "balanced proportions", "voluptuous curves", "full bust", "narrow waist", "broad hips", "feminine figure", "symmetrical shape", "classic silhouette"]},
    {"genre": "Lean Silhouette", "keywords": ["slim build", "lean body", "thin waist", "slender frame", "athletic appearance", "minimal body fat", "long limbs", "fit and toned", "narrow build", "muscularly lean"]},
    {"genre": "Boxy Silhouette", "keywords": ["straight lines", "angular body", "rectangular frame", "minimal curves", "sharp angles", "masculine appearance", "square shoulders", "athletic boxy build", "blocky shape", "uniform proportions"]},
    {"genre": "Pear-Shaped Silhouette", "keywords": ["narrow shoulders", "wider hips", "full lower body", "curvy bottom", "round thighs", "balanced top", "voluptuous figure", "full curves", "slender upper body", "hourglass with pear shape"]},
    {"genre": "Inverted Triangle Silhouette", "keywords": ["broad shoulders", "narrow hips", "defined chest", "muscular upper body", "lean legs", "V-shaped frame", "angular appearance", "defined torso", "triangular proportions", "fit appearance"]},
    {"genre": "Round Silhouette", "keywords": ["full body", "rounded shape", "curved lines", "soft edges", "gentle proportions", "plump appearance", "round shoulders", "soft curves", "chubby figure", "round face"]},
    {"genre": "Toned Silhouette", "keywords": ["fit and firm body", "well-defined muscles", "athletic body", "healthy frame", "sculpted shape", "toned arms", "flat stomach", "chiseled body", "lean but muscular", "active physique"]},
    {"genre": "Lanky Silhouette", "keywords": ["tall and thin", "long limbs", "thin body", "spindly figure", "awkward height", "limber build", "stretchy appearance", "tall with lean limbs", "slim proportions", "elongated features"]},
    {"genre": "Voluptuous Silhouette", "keywords": ["curvy figure", "full hips", "round bust", "plump appearance", "voluptuous curves", "soft body", "feminine shape", "ample proportions", "sensual silhouette", "busty and curvy"]},
    {"genre": "Chiseled Silhouette", "keywords": ["sharp angles", "defined body", "muscular frame", "sculpted torso", "lean build", "angular features", "strong jawline", "defined muscles", "fit and toned", "clear muscle definition"]},
    {"genre": "Soft Silhouette", "keywords": ["gentle curves", "rounded body", "smooth shape", "soft lines", "petite frame", "delicate appearance", "rounded features", "fluffy figure", "gentle proportions", "baby-soft curves"]},
    {"genre": "Slim-Fit Silhouette", "keywords": ["slim body", "tight-fitting attire", "elegant lines", "defined waist", "skinny build", "tailored look", "sleek appearance", "modern slim silhouette", "contoured shape", "slender clothing fit"]},
    {"genre": "Object or Ambience Vintage Telephone", "keywords": ["rotary dial", "old-fashioned", "classic design", "brass details", "antique style", "desk phone", "landline", "nostalgic", "clicking sound", "retro aesthetic"]},
    {"genre": "Object or Ambience Typewriter", "keywords": ["mechanical keys", "vintage", "old-school", "manual operation", "clacking sound", "classic design", "desk tool", "paper sheet", "writer's companion", "historical"]},
    {"genre": "Object or Ambience Flickering Candle", "keywords": ["soft light", "wax drips", "glowing flame", "romantic ambiance", "dim atmosphere", "mysterious vibe", "burning wick", "shadow play", "warmth", "vintage aesthetic"]},
    {"genre": "Object or Ambience Broken Mirror", "keywords": ["shattered glass", "fractured reflection", "distorted image", "symbolic", "dark atmosphere", "ominous", "sharp edges", "mysterious event", "psychological impact", "fragmented view"]},
    {"genre": "Object or Ambience Rain-soaked Window", "keywords": ["water droplets", "rainy weather", "blurred view", "melancholic mood", "reflection", "misty glass", "gloomy", "soft focus", "sad atmosphere", "wet surface"]},
    {"genre": "Object or Ambience Old Book", "keywords": ["leather-bound", "yellowed pages", "antique", "vintage paper", "aged cover", "library setting", "knowledge", "dusty", "history", "worn spine"]},
    {"genre": "Object or Ambience Teddy Bear", "keywords": ["soft plush", "childhood symbol", "cuddly", "fuzzy", "innocence", "nostalgic", "comfort object", "vintage toy", "kid's companion", "cute features"]},
    {"genre": "Object or Ambience Pocket Watch", "keywords": ["vintage design", "golden casing", "intricate details", "timeless", "precious timepiece", "antique", "classic accessory", "elegant", "mechanical movement", "old-fashioned style"]},
    {"genre": "Object or Ambience Suitcase", "keywords": ["vintage", "leather", "worn edges", "traveling companion", "rustic", "classic luggage", "old-fashioned", "adventure", "airplane travels", "nostalgic"]},
    {"genre": "Object or Ambience Broken TV Screen", "keywords": ["cracked glass", "distorted image", "static noise", "outdated technology", "glitch effect", "dark ambiance", "disconnection", "old electronics", "visual distortion", "damaged display"]},
    {"genre": "Object or Ambience Coffee Mug", "keywords": ["steam rising", "morning ritual", "comfort beverage", "cozy", "ceramic", "vintage design", "hot drink", "caffeine boost", "office setting", "casual scene"]},
    {"genre": "Object or Ambience Light Bulb", "keywords": ["glowing filament", "soft light", "warm glow", "illuminated", "industrial design", "retro lighting", "hanging from the ceiling", "vintage fixture", "flickering effect", "intimate lighting"]},
    {"genre": "Object or Ambience Pocket Knife", "keywords": ["foldable blade", "sharp edge", "survival tool", "compact", "rustic", "military design", "practical", "tool kit", "outdoor use", "adventure gear"]},
    {"genre": "Object or Ambience Old Record Player", "keywords": ["vinyl records", "spinning disc", "retro sound", "classic music player", "turntable", "needle drop", "nostalgic tunes", "vintage design", "warm sound", "groovy atmosphere"]},
    {"genre": "Object or Ambience Glasses", "keywords": ["round frames", "eyeglasses", "reading glasses", "classic design", "intellectual style", "modern aesthetic", "vintage fashion", "sophisticated look", "clear vision", "stylish accessory"]},
    {"genre": "Object or Ambience Suit Jacket", "keywords": ["tailored fit", "elegant design", "formal wear", "business attire", "luxurious fabric", "sleek lines", "professional look", "dapper style", "classic silhouette", "fashionable"]},
    {"genre": "Object or Ambience Cigarette", "keywords": ["smoke cloud", "lit end", "ashtray", "burning tip", "classic icon", "vintage atmosphere", "casual smoking", "nostalgic setting", "dangerous habit", "dark ambiance"]},
    {"genre": "Object or Ambience Snow-covered Street", "keywords": ["snowflakes", "white blanket", "icy roads", "winter scene", "cold weather", "frosted trees", "quiet silence", "wintry mood", "footprints in snow", "chilly atmosphere"]},
    {"genre": "Object or Ambience Guitar", "keywords": ["electric strings", "classic design", "musical instrument", "strumming sound", "rock music", "acoustic melody", "guitar pick", "wooden body", "chord progression", "performer's tool"]},
    {"genre": "Object or Ambience Old Lamp", "keywords": ["brass fixture", "shaded light", "vintage design", "soft glow", "chandelier", "romantic lighting", "antique decor", "classic elegance", "dimly lit room", "rustic atmosphere"]},
    {"genre": "Object or Ambience Rifle", "keywords": ["long barrel", "military design", "lethal tool", "precision aim", "survival gear", "outdoor weapon", "action scene", "dangerous weapon", "intense combat", "dangerous firepower"]},
    {"genre": "Object or Ambience Snow Globe", "keywords": ["glass sphere", "snow falling", "miniature scene", "holiday decor", "winter charm", "sparkling snow", "cute figurine", "frozen moment", "holiday souvenir", "whimsical"]},
    {"genre": "Object or Ambience Train Tracks", "keywords": ["rusty rails", "train journey", "distant sound", "industrial setting", "long tracks", "rustic train", "empty station", "nostalgic travel", "motion blur", "symbolic path"]},
    {"genre": "Object or Ambience Wristwatch", "keywords": ["sleek design", "metallic band", "luxury accessory", "precise time", "elegant", "golden finish", "classic watch", "fashionable", "timekeeping", "refined style"]},
    {"genre": "Object or Ambience Snowman", "keywords": ["frosty figure", "scarf", "button eyes", "carrot nose", "winter decoration", "snow-covered", "snowy day", "holiday spirit", "childhood creation", "whimsical"]},
    {"genre": "Object or Ambience Vintage Camera", "keywords": ["film roll", "manual focus", "classic design", "old-fashioned", "photography tool", "black and white photos", "retro aesthetic", "bulky body", "shutter sound", "timeless technology"]},
    {"genre": "Object or Ambience Chess Board", "keywords": ["wooden pieces", "strategy game", "black and white squares", "classic board game", "checkmate moment", "intense focus", "old-school", "antique chess set", "strategic planning", "mental challenge"]},
    {"genre": "Object or Ambience Vintage Radio", "keywords": ["dial knobs", "static sound", "old-fashioned design", "antique technology", "classic broadcast", "wooden exterior", "retro vibe", "AM/FM signal", "broadcasting station", "nostalgic sound"]},
    {"genre": "Object or Ambience Magnifying Glass", "keywords": ["enlarged details", "antique tool", "curious exploration", "detective style", "investigation", "clear focus", "refined optics", "small object examination", "old-fashioned lens", "historical accessory"]},
    {"genre": "Object or Ambience Harmonica", "keywords": ["small instrument", "blues music", "foldable design", "nostalgic sound", "portable", "blues harmonica", "melodic", "acoustic instrument", "classic music", "old-school vibe"]},
    {"genre": "Object or Ambience Globe", "keywords": ["world map", "rotating sphere", "geographical knowledge", "global focus", "exploration tool", "classic design", "educational", "vintage world globe", "political borders", "spinning globe"]},
    {"genre": "Object or Ambience Vinyl Records", "keywords": ["spinning disc", "retro sound", "music collection", "classic tunes", "old-fashioned design", "analog sound", "album cover", "needle drop", "turntable", "nostalgic music"]},
    {"genre": "Object or Ambience Fireplace", "keywords": ["crackling flames", "warmth", "cozy atmosphere", "stone hearth", "home setting", "soft light", "wood burning", "hearthstone", "romantic lighting", "traditional living room"]},
    {"genre": "Object or Ambience Candle Holder", "keywords": ["antique design", "brass finish", "romantic lighting", "elegant decor", "decorative", "vintage style", "candlelight", "classy", "mood lighting", "soft glow"]},
    {"genre": "Object or Ambience Leather Journal", "keywords": ["aged pages", "handwritten notes", "vintage leather", "personal reflections", "antique paper", "classic writing tool", "travel journal", "handcrafted cover", "deep thoughts", "old-fashioned writing"]},
    {"genre": "Object or Ambience Rug", "keywords": ["woven fabric", "classic design", "soft texture", "floor covering", "warm colors", "patterned", "decorative", "traditional home decor", "cozy", "luxurious feel"]},
    {"genre": "Object or Ambience Wall Clock", "keywords": ["ticking sound", "round face", "timeless design", "classic timepiece", "brass hands", "vintage aesthetic", "interior decor", "pendulum", "functional art", "elegant design"]},
    {"genre": "Object or Ambience Armchair", "keywords": ["upholstered seat", "vintage design", "comfortable", "soft cushion", "classic furniture", "traditional look", "luxurious fabric", "reading chair", "living room furniture", "elegant style"]},
    {"genre": "Object or Ambience Coffee Pot", "keywords": ["metal kettle", "pouring spout", "hot beverage", "morning ritual", "traditional", "coffee brewing", "classic kitchen tool", "steam rising", "ceramic", "warm drink"]},
    {"genre": "Object or Ambience Fishing Rod", "keywords": ["reel", "fishing line", "outdoor activity", "tackle box", "cast line", "serenity", "natural setting", "leisure activity", "waterfront", "classic design"]},
    {"genre": "Object or Ambience Binoculars", "keywords": ["telescope lenses", "magnified view", "outdoor adventure", "exploration tool", "birdwatching", "spyglass", "compact design", "visual clarity", "optical precision", "travel companion"]},
    {"genre": "Object or Ambience Suitcase", "keywords": ["travel bag", "luggage", "vintage design", "classic leather", "open case", "packed belongings", "airplane trip", "explorer's gear", "journey", "adventure-ready"]},
    {"genre": "Object or Ambience Piano", "keywords": ["ivory keys", "grand design", "musical instrument", "classical music", "grandiose sound", "elegant look", "sophisticated", "black and white keys", "sheet music", "performing art"]},
    {"genre": "Object or Ambience Steampunk Goggles", "keywords": ["brass frame", "industrial style", "retro-futuristic", "vintage design", "mechanical look", "engineering accessory", "adventure gear", "gothic aesthetic", "steampunk fashion", "retro eyewear"]},
    {"genre": "Object or Ambience Vintage Suitcase", "keywords": ["old-fashioned luggage", "leather handles", "travel companion", "classic design", "aged appearance", "vintage travel", "brass clasps", "antique style", "nostalgic trips", "retro adventure"]},
    {"genre": "Object or Ambience Sunglasses", "keywords": ["stylish frames", "protective lenses", "cool vibe", "summer accessory", "fashionable", "classic design", "outdoor wear", "retro style", "sun protection", "modern look"]},
    {"genre": "Object or Ambience Chandelier", "keywords": ["hanging light", "elegant crystal", "grandiose design", "luxurious home decor", "glistening glow", "vintage lighting", "ornate fixture", "classical", "sophisticated", "romantic ambiance"]},
    {"genre": "Object or Ambience Feather Quill", "keywords": ["ink pen", "antique tool", "handwritten letters", "old-fashioned writing", "feathered pen", "historical", "poetry", "elegant calligraphy", "vintage writing instrument", "classical design"]},
    {"genre": "African Tribal Warrior", "keywords": ["traditional attire", "vibrant patterns", "beaded accessories", "painted face", "ceremonial weapons", "bold presence", "cultural heritage", "dynamic stance", "ancestral strength", "majestic energy"]},
    {"genre": "Japanese Samurai", "keywords": ["ornate armor", "katana sword", "topknot hairstyle", "calm demeanor", "discipline and honor", "traditional robes", "poised stance", "epic grace", "cultural pride", "timeless elegance"]},
    {"genre": "Indian Royalty", "keywords": ["luxurious saree", "golden jewelry", "elegant turban", "regal presence", "cultural richness", "ornate patterns", "vibrant colors", "majestic charisma", "traditional grace", "timeless beauty"]},
    {"genre": "Native American Chief", "keywords": ["feathered headdress", "ceremonial attire", "cultural pride", "commanding stance", "ancestral wisdom", "painted designs", "earthy tones", "majestic presence", "tribal spirit", "timeless respect"]},
    {"genre": "Nordic Viking", "keywords": ["fierce expression", "battle-worn armor", "fur cloaks", "braided hair", "ornate shields", "epic strength", "dynamic movements", "cultural pride", "ancestral energy", "timeless courage"]},
    {"genre": "Chinese Empress", "keywords": ["silk robes", "ornate headpiece", "elegant posture", "regal presence", "flowing patterns", "timeless beauty", "cultural heritage", "majestic aura", "traditional grace", "refined elegance"]},
    {"genre": "Middle Eastern Sultan", "keywords": ["opulent attire", "ornate turban", "golden jewelry", "commanding posture", "cultural pride", "majestic energy", "intricate patterns", "traditional wisdom", "timeless power", "luxurious charisma"]},
    {"genre": "European Renaissance Noble", "keywords": ["elegant doublet", "flowing gowns", "ornate jewelry", "refined gestures", "historical pride", "timeless beauty", "majestic aura", "cultural richness", "regal demeanor", "classic refinement"]},
    {"genre": "Caribbean Islander", "keywords": ["vibrant clothing", "tropical accessories", "joyful energy", "dynamic movements", "beachside backdrop", "cultural pride", "bold expressions", "island charm", "timeless vibrancy", "colorful grace"]},
    {"genre": "Australian Aboriginal", "keywords": ["painted body art", "cultural pride", "ancestral traditions", "earthy tones", "dynamic stance", "timeless heritage", "natural surroundings", "commanding energy", "spiritual connection", "majestic grace"]},
    {"genre": "Russian Czar", "keywords": ["ornate robes", "fur accents", "commanding posture", "traditional jewelry", "cultural heritage", "majestic demeanor", "bold charisma", "refined elegance", "historical pride", "timeless strength"]},
    {"genre": "South American Gaucho", "keywords": ["rugged attire", "dynamic stance", "commanding energy", "cultural heritage", "traditional accessories", "majestic pride", "bold movements", "timeless charisma", "natural backdrop", "heritage resilience"]},
    {"genre": "Polynesian Dancer", "keywords": ["grass skirts", "flower leis", "dynamic energy", "joyful expressions", "cultural pride", "timeless grace", "island backdrop", "flowing movements", "vibrant charm", "majestic connection"]},
    {"genre": "Mexican Mariachi", "keywords": ["ornate charro suit", "wide sombrero", "cultural pride", "vibrant energy", "musical instruments", "majestic charisma", "traditional elegance", "dynamic gestures", "joyful spirit", "timeless rhythm"]},
    {"genre": "Scottish Highlander", "keywords": ["tartan kilt", "bagpipes", "bold stance", "cultural pride", "majestic charisma", "traditional energy", "rugged surroundings", "historical connection", "timeless strength", "ancestral heritage"]},
    {"genre": "Inuit Hunter", "keywords": ["fur-lined attire", "snowy backdrop", "cultural resilience", "commanding energy", "ancestral wisdom", "dynamic movements", "timeless strength", "majestic spirit", "natural surroundings", "heritage pride"]},
    {"genre": "Greek Philosopher", "keywords": ["flowing toga", "calm demeanor", "commanding presence", "timeless wisdom", "ornate details", "philosophical aura", "majestic energy", "cultural heritage", "refined grace", "classical intellect"]},
    {"genre": "Zulu Warrior", "keywords": ["beaded accessories", "traditional shield", "cultural energy", "bold presence", "dynamic movements", "timeless heritage", "majestic pride", "painted face", "ancestral spirit", "commanding charisma"]},
    {"genre": "Italian Gondolier", "keywords": ["striped shirt", "flowing scarf", "joyful expressions", "traditional boat", "cultural pride", "timeless charm", "dynamic movements", "majestic energy", "vibrant aura", "classic elegance"]},    
    {"genre": "Macro Shot", "keywords": ["extreme close-up", "minute details", "texture focus", "tiny subjects", "precision framing", "high magnification", "delicate features", "surface intricacy", "micro-level exploration", "detailed realism"]},
    {"genre": "Bokeh Effect", "keywords": ["blurred background", "soft focus", "light orbs", "shallow depth of field", "dreamy ambiance", "visual separation", "highlighted subject", "glowing accents", "ethereal feel", "optical artistry"]},
    {"genre": "Tilt-Shift Effect", "keywords": ["miniature simulation", "selective focus", "toy-like appearance", "localized blur", "compressed perspective", "creative focus", "scene manipulation", "dynamic depth", "quirky visuals", "illusion of scale"]},
    {"genre": "Time-Lapse Macro", "keywords": ["motion in micro-scale", "minute changes", "dynamic evolution", "compressed time", "slow transformations", "fluid motion", "natural patterns", "rapid progression", "high-definition focus", "life in detail"]},
    {"genre": "High-Speed Capture", "keywords": ["frozen motion", "instantaneous detail", "split-second action", "liquid splashes", "rapid sequences", "ultra-clear focus", "dynamic stills", "micro-movements", "precise timing", "unseen moments"]},
    {"genre": "Infrared Macro", "keywords": ["hidden spectrum", "thermal visuals", "unique color tones", "infrared patterns", "heat mapping", "spectral contrasts", "technical intrigue", "soft lighting", "otherworldly appearance", "scientific aesthetics"]},
    {"genre": "UV Fluorescence", "keywords": ["glowing effects", "fluorescent patterns", "bright contrasts", "invisible details", "ultraviolet light", "neon highlights", "luminous beauty", "exotic visuals", "spectral intrigue", "enhanced vibrancy"]},
    {"genre": "Focus Stacking", "keywords": ["complete sharpness", "layered focus", "depth clarity", "hyper-realistic detail", "extensive depth of field", "merged perspectives", "seamless blending", "technical precision", "enhanced textures", "crystal-clear view"]},
    {"genre": "Extreme Close-Up2", "keywords": ["magnified essence", "intense scrutiny", "visual textures", "isolated subject", "revealed intricacy", "magnificent smallness", "frame dominance", "amplified detail", "artistic focus", "intimate exploration"]},
    {"genre": "Microscopic Aesthetic", "keywords": ["scientific perspective", "magnified worlds", "hidden beauty", "cellular patterns", "molecular intrigue", "unseen geometries", "microcosm visuals", "technical beauty", "high-definition precision", "nature’s artistry"]},    
    {"genre": "Close-Up", "keywords": ["detailed focus", "intense emotion", "facial expressions", "dramatic emphasis", "intimate framing", "micro details", "raw emotion", "visual clarity", "character depth", "highlighted features"]},
    {"genre": "Wide Shot", "keywords": ["expansive views", "landscape focus", "environmental context", "large scale", "epic vistas", "scenic detail", "immersive framing", "broad perspective", "story setting", "spatial clarity"]},
    {"genre": "Tracking Shot", "keywords": ["smooth motion", "following action", "continuous movement", "dynamic flow", "immersive perspective", "scene connection", "motion continuity", "character tracking", "cinematic immersion", "story fluidity"]},
    {"genre": "Dolly Zoom", "keywords": ["dramatic distortion", "perspective shift", "tension building", "emotional impact", "zoom effect", "dynamic depth", "cinematic style", "vertigo illusion", "visual intrigue", "story emphasis"]},
    {"genre": "Bird's Eye View", "keywords": ["overhead angle", "strategic view", "scene layout", "aerial storytelling", "epic perspective", "broad scope", "top-down framing", "spatial overview", "unique perspective", "environmental clarity"]},
    {"genre": "Over-the-Shoulder", "keywords": ["character interaction", "intimate framing", "focused dialogue", "scene connection", "emotional depth", "character perspective", "engaging view", "conversation framing", "narrative focus", "viewer immersion"]},
    {"genre": "Low Angle", "keywords": ["dominant view", "powerful stance", "dramatic framing", "character strength", "intimidating presence", "heroic angle", "visual tension", "impactful perspective", "scene dominance", "cinematic power"]},
    {"genre": "High Angle", "keywords": ["vulnerable view", "scale shift", "dramatic focus", "character isolation", "emotional impact", "scene emphasis", "heightened perspective", "viewer clarity", "cinematic storytelling", "contextual depth"]},
    {"genre": "Handheld", "keywords": ["raw movement", "realistic feel", "chaotic energy", "authentic perspective", "dynamic framing", "personal connection", "scene immersion", "natural motion", "grounded view", "intimate tension"]},
    {"genre": "Dutch Angle", "keywords": ["tilted framing", "dynamic energy", "visual tension", "disoriented view", "scene distortion", "cinematic style", "impactful angle", "story emphasis", "unsettling motion", "creative framing"]},    
    {"genre": "Pan Shot", "keywords": ["smooth horizontal movement", "scene exploration", "environmental sweep", "cinematic flow", "dynamic storytelling", "visual transition", "spatial awareness", "continuous motion", "immersive view", "action focus"]},
    {"genre": "Tilt Shot", "keywords": ["vertical motion", "dramatic effect", "dynamic framing", "scene reveal", "perspective shift", "cinematic storytelling", "visual exploration", "height emphasis", "environmental clarity", "motion engagement"]},
    {"genre": "Zoom In", "keywords": ["focused attention", "intensified detail", "emotional closeness", "narrative emphasis", "character isolation", "visual depth", "scene intimacy", "story clarity", "perspective narrowing", "viewer engagement"]},
    {"genre": "Zoom Out", "keywords": ["broader view", "expanded context", "environmental storytelling", "character placement", "scene reveal", "cinematic scope", "visual connection", "narrative setup", "scale emphasis", "immersive framing"]},
    {"genre": "Extreme Close-UpA", "keywords": ["minute detail", "intense focus", "micro expressions", "emotional impact", "textural clarity", "intimate storytelling", "character depth", "dramatic emphasis", "narrative tension", "viewer intrigue"]},
    {"genre": "Extreme Wide Shot", "keywords": ["grand perspective", "environmental scale", "epic landscapes", "spatial depth", "scene setup", "visual storytelling", "cinematic grandeur", "character context", "world-building", "narrative immersion"]},
    {"genre": "Rack Focus", "keywords": ["dynamic focus shift", "foreground emphasis", "background reveal", "visual clarity", "narrative direction", "depth manipulation", "cinematic style", "viewer engagement", "story intrigue", "perspective transition"]},
    {"genre": "Crane Shot", "keywords": ["elevated movement", "sweeping motion", "cinematic drama", "scene grandeur", "fluid transitions", "dynamic storytelling", "scale reveal", "visual fluidity", "story immersion", "height perspective"]},
    {"genre": "Point of View (POV)", "keywords": ["character perspective", "immersive storytelling", "viewer connection", "emotional focus", "narrative intimacy", "visual engagement", "scene relatability", "first-person framing", "dramatic depth", "perspective storytelling"]},
    {"genre": "Overhead Tracking", "keywords": ["bird's-eye motion", "scene following", "spatial context", "dynamic perspective", "environmental storytelling", "cinematic fluidity", "narrative immersion", "action framing", "motion clarity", "unique angles"]},    
    {"genre": "Panoramic", "keywords": ["360-degree view", "sweeping motion", "grand scale", "immersive environment", "epic storytelling", "wide-angle", "scenic landscapes", "comprehensive framing", "environmental immersion", "dramatic visuals"]},
    {"genre": "Handheld2", "keywords": ["raw movement", "authentic feel", "chaotic energy", "intimate perspective", "realistic storytelling", "dynamic framing", "shaky camera", "immediacy", "personal connection", "gritty aesthetic"]},
    {"genre": "Zoom-In", "keywords": ["focused detail", "intensified emotion", "close scrutiny", "visual emphasis", "building tension", "narrative focus", "magnified subject", "emotional depth", "character intimacy", "scene intensity"]},
    {"genre": "Zoom-Out", "keywords": ["wider perspective", "context reveal", "dramatic retreat", "environmental scope", "scene expansion", "spatial awareness", "story clarity", "background emphasis", "cinematic depth", "broad framing"]},
    {"genre": "Static Shot", "keywords": ["fixed framing", "focused subject", "minimalist", "unwavering attention", "calm storytelling", "stable composition", "intense focus", "artistic stillness", "scene isolation", "precise narrative"]},
    {"genre": "Extreme Close-Up", "keywords": ["minute detail", "intense focus", "textural elements", "emotional nuance", "cinematic intimacy", "micro expressions", "dramatic emphasis", "character depth", "visual intricacy", "narrative highlight"]},
    {"genre": "Overhead Tracking", "keywords": ["continuous aerial view", "dynamic motion", "bird's-eye follow", "immersive perspective", "visual intrigue", "narrative flow", "top-down view", "cinematic movement", "scene clarity", "perspective shift"]},
    {"genre": "Tilt Shot2", "keywords": ["vertical motion", "revealing scale", "emotional depth", "perspective shift", "scene dynamics", "cinematic tension", "environmental framing", "dramatic angles", "narrative depth", "camera motion"]},
    {"genre": "Dutch Angle2", "keywords": ["tilted framing", "disorientation", "dynamic energy", "tension creation", "cinematic style", "visual unease", "drama enhancement", "unique perspective", "narrative tension", "artistic flair"]},
    {"genre": "Time-Lapse Movement", "keywords": ["accelerated motion", "changing scenery", "evolving story", "progressive flow", "cinematic pace", "environmental shifts", "dynamic transitions", "scene evolution", "temporal depth", "visual transformation"]},
    {"genre": "Slow MotionA", "keywords": ["dramatic pause", "emotional focus", "captured detail", "extended impact", "cinematic tension", "heightened emotion", "visual artistry", "scene elongation", "enhanced storytelling", "moment magnification"]},
    {"genre": "Point of View", "keywords": ["character perspective", "immersive storytelling", "subjective view", "emotional connection", "interactive framing", "viewer engagement", "personal perspective", "narrative depth", "visual alignment", "scene intimacy"]},
    {"genre": "Black and White", "keywords": ["monochromatic tones", "high contrast", "classic aesthetic", "timeless feel", "shadows and highlights", "elegant simplicity", "dramatic emphasis", "retro style", "visual clarity", "subtle textures"]},
    {"genre": "Sepia", "keywords": ["warm tones", "vintage aesthetic", "antique feel", "earthy palette", "historical vibe", "soft contrasts", "muted highlights", "nostalgic atmosphere", "classic warmth", "aged textures"]},
    {"genre": "Overexposed", "keywords": ["bright highlights", "softened details", "washed-out tones", "dreamlike feel", "light-drenched", "ethereal glow", "high-key lighting", "soft focus", "radiant scenes", "intense illumination"]},
    {"genre": "Underexposed", "keywords": ["deep shadows", "moody tones", "dark ambiance", "low-key lighting", "mysterious feel", "hidden details", "dramatic contrast", "subdued highlights", "intimate framing", "shadow play"]},
    {"genre": "Warm Tone", "keywords": ["golden hues", "sunlit ambiance", "soft warmth", "inviting feel", "earthy palette", "cozy glow", "autumn vibes", "radiant highlights", "natural tones", "sunset-inspired"]},
    {"genre": "Cool Tone", "keywords": ["blue hues", "calm ambiance", "icy feel", "tranquil palette", "crisp details", "winter vibes", "serene atmosphere", "chill undertones", "minimal warmth", "refreshing clarity"]},
    {"genre": "Vivid Color", "keywords": ["bright palette", "bold saturation", "eye-catching hues", "vibrant contrast", "intense tones", "dynamic visuals", "energetic feel", "color explosion", "playful mood", "electric vibrancy"]},
    {"genre": "Muted Color", "keywords": ["soft palette", "subdued tones", "gentle hues", "minimal saturation", "calm feel", "natural aesthetic", "elegant simplicity", "understated beauty", "soft contrast", "neutral vibes"]},
    {"genre": "Neon Glow", "keywords": ["bright fluorescence", "electric tones", "urban vibes", "futuristic feel", "vivid highlights", "dark contrasts", "vibrant glow", "city night aesthetic", "intense luminosity", "dynamic neon"]},
    {"genre": "Pastel Palette", "keywords": ["soft colors", "delicate hues", "light tones", "dreamy feel", "subtle contrasts", "gentle atmosphere", "romantic aesthetic", "feminine charm", "soothing visuals", "playful subtlety"]},
    {"genre": "High Contrast", "keywords": ["sharp contrasts", "bold definition", "dramatic tones", "emphasized textures", "vivid details", "crisp edges", "dynamic depth", "intense clarity", "visual punch", "expressive aesthetic"]},
    {"genre": "Low Contrast", "keywords": ["soft gradients", "gentle transitions", "subtle tones", "harmonious palette", "calm visuals", "muted definition", "minimal separation", "soothing clarity", "natural feel", "balanced light"]},
    {"genre": "Golden Hour", "keywords": ["warm glow", "soft sunlight", "golden tones", "romantic ambiance", "sunset hues", "gentle warmth", "natural radiance", "long shadows", "dreamy atmosphere", "rich highlights"]},
    {"genre": "Infrared", "keywords": ["surreal colors", "unique spectrum", "otherworldly tones", "inverted warmth", "alien feel", "bright foliage", "dark skies", "experimental vibe", "technical aesthetic", "rare visuals"]},
    {"genre": "Monochrome", "keywords": ["single color focus", "unified tones", "artistic simplicity", "abstract feel", "elegant clarity", "minimalist aesthetic", "tonal unity", "soft contrasts", "clean visuals", "focused palette"]},
    {"genre": "Film Grain", "keywords": ["textured overlay", "vintage look", "cinematic vibe", "nostalgic feel", "subtle noise", "retro aesthetic", "classic ambiance", "analog style", "grainy details", "authentic charm"]},
    {"genre": "Metallic", "keywords": ["shiny surfaces", "reflective tones", "metallic sheen", "industrial vibe", "futuristic feel", "textured highlights", "cool elegance", "sleek design", "bold contrast", "modern aesthetic"]},
    {"genre": "Dreamy Haze", "keywords": ["soft focus", "gentle glow", "ethereal feel", "misty atmosphere", "romantic tones", "subtle blur", "magical ambiance", "muted contrasts", "surreal vibes", "whimsical clarity"]},
    {"genre": "Desaturated", "keywords": ["toned-down palette", "minimal hues", "neutral tones", "understated feel", "soft contrasts", "muted highlights", "balanced saturation", "elegant simplicity", "subdued visuals", "calm atmosphere"]},
    {"genre": "Vibrant Pop", "keywords": ["bright accents", "high saturation", "dynamic colors", "energetic feel", "bold contrasts", "playful tones", "attention-grabbing hues", "expressive palette", "lively aesthetic", "fun vibrancy"]},    
    {"genre": "Glitch Effect", "keywords": ["digital distortion", "static lines", "broken visuals", "flickering images", "pixelated details", "color shifts", "cyber aesthetic", "disrupted frames", "error overlays", "techno vibe"]},
    {"genre": "Bloom Effect", "keywords": ["intense glow", "soft radiance", "bright highlights", "ethereal light", "dreamy visuals", "halo around objects", "surreal atmosphere", "overexposed edges", "fantastical feel", "luminous frames"]},
    {"genre": "Motion Blur", "keywords": ["dynamic movement", "blurred action", "speed effect", "softened details", "fluid visuals", "fast-paced feel", "smeared motion", "kinetic energy", "cinematic streaks", "intense focus"]},
    {"genre": "Chromatic Aberration", "keywords": ["color fringing", "prismatic edges", "visual distortion", "rainbow highlights", "retro vibes", "light diffraction", "subtle misalignment", "technical aesthetic", "vivid splits", "experimental tone"]},
    {"genre": "Lens Flare", "keywords": ["bright streaks", "sunlight effects", "cinematic highlights", "natural glow", "softened edges", "realistic lighting", "dynamic sparkles", "halo reflections", "detailed shimmer", "scenic drama"]},
    {"genre": "Depth of Field", "keywords": ["selective focus", "blurred background", "crisp subject", "dimensional visuals", "shallow field", "bokeh effects", "layered depth", "focused clarity", "cinematic feel", "visual emphasis"]},
    {"genre": "Pixelation", "keywords": ["blocky visuals", "retro style", "low resolution", "minimal details", "video game aesthetic", "abstract frames", "artistic distortion", "digital charm", "geometric patterns", "technical vibe"]},
    {"genre": "Vignette Effect", "keywords": ["darkened edges", "center focus", "classic framing", "subtle shadows", "cinematic highlights", "dramatic emphasis", "isolated subject", "soft gradients", "natural framing", "intense mood"]},
    {"genre": "Glow Shader", "keywords": ["radiant effects", "soft illumination", "neon highlights", "light-filled visuals", "subtle halos", "ethereal ambiance", "magical tones", "enhanced brightness", "surreal clarity", "bright accents"]},
    {"genre": "Cel Shading", "keywords": ["cartoon effect", "outlined edges", "flat colors", "bold contrasts", "stylized visuals", "graphic novel vibe", "animated look", "simplified details", "artistic shading", "vivid design"]},
    {"genre": "Grain Effect", "keywords": ["textured overlay", "cinematic noise", "vintage vibe", "subtle static", "analog charm", "old film aesthetic", "authentic visuals", "dimensional grain", "artistic detail", "classic tone"]},
    {"genre": "Anaglyph 3D", "keywords": ["red-cyan layers", "retro 3D effect", "stereoscopic visuals", "displaced images", "vintage feel", "depth illusion", "layered look", "technical charm", "cinematic distortion", "dimensional vibes"]},
    {"genre": "X-Ray Effect", "keywords": ["skeletal visuals", "translucent layers", "medical aesthetic", "monochrome tones", "high contrast", "scientific vibe", "detailed structure", "abstract clarity", "experimental look", "unique depth"]},
    {"genre": "Sketch Effect", "keywords": ["hand-drawn look", "pencil textures", "line emphasis", "black-and-white tones", "artistic shading", "stylized details", "rough outlines", "abstract charm", "soft contrasts", "visual creativity"]},
    {"genre": "Comic Style", "keywords": ["bold outlines", "vivid colors", "graphic novel look", "action effects", "speech bubbles", "pop art vibe", "stylized details", "dynamic frames", "classic design", "playful aesthetics"]},
    {"genre": "Tilt-Shift Effect", "keywords": ["miniature visuals", "blurred edges", "selective focus", "toy-like feel", "dimensional framing", "realistic distortion", "layered depth", "softened views", "cinematic artistry", "creative framing"]},
    {"genre": "Oil Painting Effect", "keywords": ["textured brushstrokes", "painterly feel", "soft gradients", "artistic layers", "rich tones", "classic style", "blended details", "subtle textures", "vintage charm", "creative ambiance"]},
    {"genre": "Halftone Effect", "keywords": ["dotted visuals", "retro design", "newspaper style", "pop art vibes", "vintage textures", "graphic overlays", "layered tones", "minimal shading", "artistic patterns", "playful contrasts"]},
    {"genre": "Fire Effect", "keywords": ["flaming visuals", "dynamic flames", "intense heat", "bright tones", "motion energy", "burning edges", "dramatic glow", "bold contrasts", "cinematic sparks", "explosive ambiance"]},
    {"genre": "Watercolor Effect", "keywords": ["soft washes", "fluid textures", "pastel tones", "painterly layers", "blended details", "artistic charm", "abstract visuals", "dreamy tones", "natural flow", "creative warmth"]},    
    {"genre": "Action", "keywords": ["explosive", "fast-paced", "thrilling", "intense stunts", "heroic", "high energy", "adrenaline-filled", "dramatic chases", "powerful fights", "life-or-death stakes", "cinematic tension"]},
    {"genre": "Adventure", "keywords": ["exploration", "journeys", "epic landscapes", "adventurous spirit", "quests", "uncharted territories", "hidden treasures", "mystical discoveries", "legendary heroes", "timeless stories"]},
    {"genre": "Adventure2", "keywords": ["exploration", "quests", "dangerous missions", "exotic locations", "dynamic", "ancient secrets", "unexpected twists", "heroic battles", "challenging terrains", "cultural richness"]},
    {"genre": "Science-Fiction", "keywords": ["futuristic", "space travel", "alien worlds", "advanced technology", "dystopian", "cybernetic enhancements", "parallel universes", "robotic societies", "time manipulation", "cosmic exploration"]},
    {"genre": "Science Fiction2", "keywords": ["futuristic", "mecha", "alien worlds", "space exploration", "advanced technology", "genetic experiments", "artificial intelligence", "post-apocalyptic", "quantum mechanics", "stellar wars"]},
    {"genre": "Fantasy", "keywords": ["magical", "mythical creatures", "enchanting worlds", "epic battles", "wizards", "ancient prophecies", "mystical artifacts", "heroic journeys", "dark forces", "legendary kingdoms"]},
    {"genre": "Fantasy2", "keywords": ["magical worlds", "epic quests", "mythical creatures", "swords and sorcery", "enchanting", "arcane rituals", "hidden realms", "fabled heroes", "celestial powers", "timeless legends"]},
    {"genre": "Romance", "keywords": ["love story", "emotional", "heartwarming", "intimate moments", "passion", "longing glances", "unspoken words", "romantic gestures", "star-crossed lovers", "tender connections"]},
    {"genre": "Romance2", "keywords": ["love story", "heartwarming", "youthful emotions", "intimate moments", "sweet", "serendipitous meetings", "whimsical dates", "first love", "soulful bonds", "bittersweet memories"]},
    {"genre": "Comedy", "keywords": ["funny", "lighthearted", "humorous", "slapstick", "witty dialogues", "quirky characters", "unexpected punchlines", "situational humor", "ridiculous antics", "clever twists"]},
    {"genre": "Comedy2", "keywords": ["funny", "lighthearted", "witty dialogues", "hilarious scenarios", "parody", "spoofs", "over-the-top humor", "cultural satire", "absurd moments", "irreverent jokes"]},
    {"genre": "Horror", "keywords": ["scary", "suspenseful", "haunting", "eerie", "chilling atmosphere", "sinister shadows", "bloodcurdling screams", "terrifying creatures", "claustrophobic settings", "paranormal activity"]},
    {"genre": "Horror2", "keywords": ["dark", "gory", "psychological", "creepy", "supernatural", "dread-filled", "disturbing visuals", "haunted locations", "macabre themes", "nightmarish imagery"]},
    {"genre": "Drame", "keywords": ["emotional depth", "realistic", "intense conflict", "character-driven", "complex", "heart-wrenching moments", "poignant storytelling", "family dynamics", "moral dilemmas", "life-changing decisions"]},
    {"genre": "Mystery", "keywords": ["suspenseful", "puzzling", "intriguing", "crime-solving", "noir vibes", "hidden clues", "unexpected revelations", "enigmatic characters", "dark secrets", "mind-bending puzzles"]},
    {"genre": "Mystery2", "keywords": ["suspenseful", "intriguing", "crime-solving", "twists", "detective stories", "forensic investigations", "shadowy motives", "clandestine meetings", "unsolved enigmas", "thrilling deductions"]},
    {"genre": "Thriller", "keywords": ["high tension", "edge-of-your-seat", "plot twists", "dark", "psychological", "mind games", "relentless pacing", "unexpected betrayals", "dangerous liaisons", "chilling suspense"]},
    {"genre": "Historical", "keywords": ["period piece", "costumes", "ancient times", "historical figures", "realistic", "cultural authenticity", "epic battles", "royal courts", "forgotten eras", "timeless narratives"]},
    {"genre": "Historical2", "keywords": ["ancient settings", "period dramas", "realistic depictions", "cultural", "epic", "historical conflicts", "royalty", "traditional customs", "legendary figures", "societal transformation"]},
    {"genre": "Western", "keywords": ["cowboys", "desert landscapes", "duels", "saloons", "rugged", "wild frontier", "outlaws", "gunfights", "horses", "loner heroes"]},
    {"genre": "Biography", "keywords": ["true story", "inspiring", "realistic", "personal journey", "factual", "overcoming adversity", "life achievements", "intimate details", "historical impact", "human resilience"]},
    {"genre": "Musical", "keywords": ["dance numbers", "catchy songs", "colorful", "uplifting", "rhythmic", "melodic storytelling", "theatrical", "ensemble performances", "emotionally charged", "choreographed sequences"]},
    {"genre": "Animation", "keywords": ["cartoonish", "family-friendly", "vibrant", "imaginative", "dynamic visuals", "playful", "magical", "fantastical creatures", "bright colors", "whimsical adventures"]},  
    {"genre": "Majestic Queen", "keywords": ["regal attire", "flowing gowns", "ornate crown", "commanding presence", "elegant demeanor", "timeless beauty", "refined gestures", "graceful movements", "luxurious fabrics", "royal charisma"]},
    {"genre": "Dashing Gentleman", "keywords": ["sharp suit", "confident posture", "charming smile", "classic style", "refined gestures", "bold charisma", "timeless appeal", "polished elegance", "magnetic presence", "sophisticated allure"]},
    {"genre": "Fierce Huntress", "keywords": ["warrior's poise", "leather armor", "piercing gaze", "bow and arrows", "forest backdrop", "dynamic stance", "stealthy movements", "fearless energy", "wild beauty", "resilient spirit"]},
    {"genre": "Cyborg Hero", "keywords": ["metallic enhancements", "futuristic armor", "battle scars", "high-tech weapons", "glowing eyes", "dynamic action", "commanding figure", "cybernetic strength", "heroic aura", "cutting-edge design"]},
    {"genre": "Ethereal Witch", "keywords": ["mystical aura", "flowing robes", "arcane symbols", "piercing eyes", "shadowy backdrop", "elegant power", "mysterious energy", "dark beauty", "spellbinding charm", "haunting allure"]},
    {"genre": "Charming Rogue", "keywords": ["playful grin", "adventurous spirit", "practical attire", "quick reflexes", "sly demeanor", "confident stride", "bold charisma", "hidden weapons", "fearless energy", "rebellious charm"]},
    {"genre": "Graceful Ballerina", "keywords": ["elegant movements", "flowing tutu", "poised stance", "refined beauty", "artistic grace", "spotlight glow", "timeless charm", "delicate features", "dynamic turns", "captivating rhythm"]},
    {"genre": "Stoic Warrior", "keywords": ["battle-worn armor", "scarred visage", "commanding stance", "brooding gaze", "imposing figure", "silent strength", "gritty determination", "sharp weaponry", "epic resilience", "legendary presence"]},
    {"genre": "Tech-Savvy Engineer", "keywords": ["high-tech tools", "mechanical background", "creative genius", "sleek designs", "focused expressions", "cutting-edge projects", "innovative mind", "dynamic environment", "modern attire", "problem-solving energy"]},
    {"genre": "Charismatic Leader", "keywords": ["confident presence", "inspirational gaze", "strong posture", "bold voice", "commanding energy", "polished attire", "timeless charisma", "visionary spirit", "magnetic appeal", "dynamic gestures"]},
    {"genre": "Mystical Monk", "keywords": ["flowing robes", "calm demeanor", "ancient wisdom", "serene environment", "meditative posture", "subtle strength", "timeless grace", "spiritual energy", "natural surroundings", "harmonious presence"]},
    {"genre": "Elegant Heiress", "keywords": ["luxurious attire", "graceful movements", "refined beauty", "ornate jewelry", "charming demeanor", "regal air", "confident smile", "elite presence", "poised figure", "timeless allure"]},
    {"genre": "Chiseled Athlete", "keywords": ["defined muscles", "dynamic pose", "focused gaze", "sporting gear", "intense energy", "powerful movements", "competitive spirit", "gritty determination", "pristine physique", "unstoppable drive"]},
    {"genre": "Radiant Bride", "keywords": ["flowing gown", "elegant veil", "delicate bouquet", "glowing smile", "timeless beauty", "graceful demeanor", "romantic charm", "refined details", "classic elegance", "captivating aura"]},
    {"genre": "Intellectual Scholar", "keywords": ["refined glasses", "focused expression", "library setting", "flowing robes", "ancient texts", "deep thought", "calm demeanor", "timeless wisdom", "subtle charm", "elegant intelligence"]},
    {"genre": "Futuristic Scout", "keywords": ["sleek outfit", "dynamic equipment", "scanning devices", "glowing accents", "focused energy", "agile movements", "high-tech landscape", "exploration spirit", "bold stance", "cutting-edge style"]},
    {"genre": "Whimsical Artist", "keywords": ["paint-splattered clothes", "creative energy", "dynamic brushstrokes", "colorful backdrop", "inspired gaze", "timeless imagination", "playful demeanor", "artistic flair", "vibrant palette", "captivating style"]},
    {"genre": "Enigmatic Detective", "keywords": ["sharp attire", "piercing gaze", "mystical aura", "shadowy setting", "bold confidence", "intelligent energy", "dynamic posture", "timeless charm", "detailed movements", "classic mystery"]},
    {"genre": "Heroic Firefighter", "keywords": ["commanding stance", "dynamic environment", "brave gaze", "protective gear", "bold energy", "intense scene", "resilient spirit", "powerful presence", "selfless actions", "heroic charm"]},
    {"genre": "Timeless Musician", "keywords": ["instrumental beauty", "artistic focus", "dynamic posture", "captivating stage presence", "elegant attire", "poetic energy", "refined movements", "classic charisma", "vivid emotions", "timeless melody"]},
    {"genre": "Mystical Creature Hybrid", "keywords": ["fantastical anatomy", "glowing features", "dynamic movements", "mythical allure", "otherworldly charm", "timeless design", "epic presence", "celestial setting", "mystical energy", "captivating grace"]},
    {"genre": "Delicate Artisan", "keywords": ["intricate designs", "focused expression", "delicate movements", "timeless charm", "artistic energy", "dynamic environment", "refined posture", "captivating details", "graceful motions", "creative focus"]},
    {"genre": "Ambitious Politician", "keywords": ["refined attire", "dynamic charisma", "intense focus", "confident stance", "polished energy", "commanding gestures", "bold strategies", "timeless appeal", "vivid expressions", "magnetic leadership"]},
    {"genre": "Playful Jester", "keywords": ["vivid attire", "dynamic movements", "playful energy", "colorful patterns", "confident smiles", "captivating stage", "bold expressions", "timeless humor", "vibrant gestures", "lighthearted charisma"]},
    {"genre": "Elegant Goddess", "keywords": ["flowing gowns", "radiant beauty", "ethereal glow", "graceful posture", "mythical allure", "delicate features", "celestial presence", "ornate jewelry", "divine proportions", "timeless elegance"]},
    {"genre": "Cybernetic Femme Fatale", "keywords": ["sleek metallic body", "glowing accents", "futuristic curves", "high-tech charm", "intense gaze", "robotic sensuality", "cyberpunk elements", "precision design", "enigmatic aura", "advanced AI"]},
    {"genre": "Petite Forest Nymph", "keywords": ["delicate wings", "tiny frame", "natural beauty", "earthy tones", "playful expressions", "woodland setting", "floral accents", "gentle movements", "magical energy", "mythical charm"]},
    {"genre": "Voluptuous Warrior", "keywords": ["muscular curves", "armor-clad figure", "confident stance", "battle-ready aura", "dynamic proportions", "epic strength", "scarred yet beautiful", "heroic charm", "commanding presence", "powerful elegance"]},
    {"genre": "Futuristic Model", "keywords": ["sleek designs", "avant-garde outfits", "flawless features", "high-tech beauty", "robotic limbs", "perfect symmetry", "glowing accessories", "futuristic runway", "exquisite proportions", "cosmic elegance"]},
    {"genre": "Vintage Pin-Up", "keywords": ["retro charm", "flirty poses", "classic beauty", "curvy silhouette", "vintage outfits", "playful expressions", "bold makeup", "stylish hairdos", "nostalgic appeal", "timeless sensuality"]},
    {"genre": "Fantasy Sorceress", "keywords": ["mystical allure", "flowing robes", "intense gaze", "arcane symbols", "magical glow", "ethereal beauty", "dynamic movements", "spell-casting hands", "elegant power", "enchanting presence"]},
    {"genre": "Petite Mechanic", "keywords": ["grease-stained hands", "small but tough", "practical outfits", "robotic tools", "futuristic workshop", "playful expressions", "compact stature", "high-tech accessories", "charming ingenuity", "modern flair"]},
    {"genre": "Alien Empress", "keywords": ["otherworldly beauty", "glowing skin", "elaborate attire", "regal posture", "unearthly elegance", "majestic aura", "interstellar allure", "unique anatomy", "celestial crown", "powerful presence"]},
    {"genre": "Exotic Dancer", "keywords": ["flowing veils", "graceful movements", "bold makeup", "jewelry accents", "vivid colors", "stage presence", "dynamic proportions", "cultural elements", "mesmerizing energy", "confident allure"]},
    {"genre": "Android Companion", "keywords": ["perfect symmetry", "human-like features", "sleek body design", "glowing circuits", "friendly expressions", "high-tech charm", "robotic elegance", "advanced AI", "delicate movements", "harmonious aesthetics"]},
    {"genre": "Petite Acrobat", "keywords": ["slender build", "dynamic poses", "graceful movements", "colorful outfits", "circus backdrop", "playful energy", "flexible proportions", "athletic charm", "vibrant stage setting", "artistic expression"]},
    {"genre": "Voluptuous Siren", "keywords": ["sensual curves", "oceanic setting", "mystical allure", "flowing hair", "serene expressions", "musical charm", "graceful movements", "mythical beauty", "underwater elegance", "captivating presence"]},
    {"genre": "Steampunk Inventor", "keywords": ["corset and goggles", "creative genius", "mechanical beauty", "intricate details", "victorian flair", "playful yet practical", "dynamic proportions", "futuristic retro style", "inventive aura", "unique charm"]},
    {"genre": "Celestial Angel", "keywords": ["radiant wings", "heavenly glow", "delicate features", "flowing robes", "divine aura", "pure beauty", "graceful movements", "ethereal presence", "majestic proportions", "timeless serenity"]},
    {"genre": "Futuristic Racer", "keywords": ["sleek bodysuits", "dynamic movements", "glowing visors", "high-tech vehicles", "competitive energy", "futuristic charm", "athletic proportions", "intense focus", "speed-driven aesthetic", "powerful allure"]},
    {"genre": "Petite Fairy", "keywords": ["tiny wings", "playful expressions", "colorful outfits", "magical glow", "forest setting", "delicate movements", "charming proportions", "mythical energy", "vibrant presence", "imaginative allure"]},
    {"genre": "Voluptuous Robot", "keywords": ["futuristic curves", "sleek metallic design", "glowing features", "high-tech aesthetics", "robotic sensuality", "perfect symmetry", "advanced engineering", "dynamic proportions", "cybernetic charm", "innovative elegance"]},
    {"genre": "Gothic Beauty", "keywords": ["dark elegance", "flowing black attire", "pale complexion", "mysterious aura", "bold makeup", "delicate yet strong", "vintage charm", "haunting presence", "melancholic allure", "timeless grace"]},
    {"genre": "Space Princess", "keywords": ["regal attire", "glowing jewels", "cosmic elegance", "commanding posture", "interstellar charm", "otherworldly beauty", "advanced style", "dynamic proportions", "galactic presence", "majestic aura"]},
    {"genre": "Petite Explorer", "keywords": ["adventurous demeanor", "practical outfits", "compact stature", "charming expressions", "wild settings", "playful energy", "dynamic movements", "exploration gear", "resourceful nature", "vivid personality"]},
    {"genre": "Exotic Queen", "keywords": ["flowing robes", "bold accessories", "regal demeanor", "mystical aura", "elaborate designs", "intense beauty", "majestic presence", "cultural influences", "graceful power", "timeless allure"]},
    {"genre": "Futuristic Diva", "keywords": ["sleek aesthetics", "avant-garde outfits", "glowing features", "flawless design", "robotic elegance", "dynamic proportions", "high-tech charisma", "stage presence", "vivid expressions", "modern allure"]},
    {"genre": "Mystical Shapeshifter", "keywords": ["fluid transformations", "graceful movements", "dynamic appearances", "otherworldly charm", "mythical beauty", "ever-changing forms", "delicate details", "ethereal glow", "captivating presence", "mysterious allure"]},
    {"genre": "Pirate Adventurer", "keywords": ["eye patch", "tattered clothing", "swashbuckling posture", "sea-weathered face", "nautical accessories", "cutlass in hand", "rogue-like charm", "ship deck setting", "treasure-focused", "adventurous spirit"]},
    {"genre": "Fantasy Orc", "keywords": ["greenish skin", "tusks", "muscular build", "tribal armor", "battle scars", "feral expressions", "brutish stance", "primitive weapons", "war-like aura", "mythological strength"]},
    {"genre": "Vampire Aristocrat", "keywords": ["pale skin", "elegant attire", "piercing eyes", "mysterious allure", "long fangs", "dark romanticism", "gothic themes", "haunted castle setting", "timeless beauty", "ethereal presence"]},
    {"genre": "Cyberpunk Hacker", "keywords": ["digital goggles", "glowing keyboard", "high-tech devices", "sleek urban wear", "neon accents", "futuristic aura", "shadowy environment", "tech-savvy demeanor", "underground setting", "hacking-focused"]},
    {"genre": "Medieval Knight", "keywords": ["shining armor", "shield and sword", "heroic stance", "chivalrous demeanor", "battle-ready", "castle backdrop", "noble crest", "historical accuracy", "warrior’s strength", "valiant aura"]},
    {"genre": "Nature Spirit", "keywords": ["leafy skin", "tree-like features", "floral accents", "earthy tones", "forest setting", "gentle demeanor", "natural glow", "mythical aura", "environmental harmony", "magical essence"]},
    {"genre": "Post-Human Mutant", "keywords": ["evolved features", "glowing veins", "otherworldly mutations", "hybrid design", "futuristic dystopia", "adaptive survival", "alien-like aura", "strange anatomy", "powerful adaptations", "mysterious evolution"]},
    {"genre": "Samurai Warrior", "keywords": ["katana in hand", "traditional armor", "focused demeanor", "ancient discipline", "Japanese aesthetics", "historical setting", "martial posture", "stoic expression", "woodblock art style", "battle-ready grace"]},
    {"genre": "Futuristic Alien", "keywords": ["bioluminescent features", "advanced suits", "unique anatomies", "interstellar themes", "unearthly aura", "technological aesthetics", "cosmic designs", "alien worlds", "non-human traits", "galactic exploration"]},
    {"genre": "Victorian Noble", "keywords": ["ornate clothing", "formal demeanor", "classical hairstyle", "elegant jewelry", "historical setting", "sophisticated expression", "antique tones", "lavish details", "aristocratic presence", "timeless grace"]},
    {"genre": "Feral Beast", "keywords": ["wild fur", "sharp claws", "intense gaze", "predatory posture", "jungle setting", "untamed energy", "roaring presence", "animalistic instinct", "natural hunter", "fearsome aura"]},
    {"genre": "Steam Mech", "keywords": ["gears and cogs", "mechanical limbs", "steam-powered engine", "vintage aesthetics", "industrial design", "brass tones", "complex machinery", "futuristic Victorian mix", "robotic strength", "inventive engineering"]},
    {"genre": "Fantasy Mermaid", "keywords": ["shimmering scales", "flowing hair", "underwater beauty", "serene expression", "oceanic backdrop", "mythical allure", "graceful movements", "aquatic elements", "coral jewelry", "ethereal glow"]},
    {"genre": "Desert Wanderer", "keywords": ["sand-colored clothing", "dusty boots", "scarred face", "weathered appearance", "nomadic lifestyle", "survivalist aura", "sunlit desert setting", "practical gear", "adventurous demeanor", "isolated resilience"]},
    {"genre": "Sci-Fi Explorer", "keywords": ["space suit", "planetary setting", "high-tech equipment", "glowing visors", "interstellar focus", "futuristic tools", "exploration vibes", "cosmic scenery", "adventurous spirit", "galactic adventure"]},
    {"genre": "Dark Sorcerer", "keywords": ["ominous cloak", "magical staff", "sinister expression", "shadowy aura", "arcane symbols", "mystical powers", "gothic atmosphere", "dark arts", "haunted environment", "powerful presence"]},
    {"genre": "Rock Star", "keywords": ["electric guitar", "wild hair", "edgy fashion", "concert setting", "energetic performance", "vibrant stage lights", "rock-and-roll vibes", "rebellious aura", "musical charisma", "passionate expression"]},
    {"genre": "Sci-Fi Pilot", "keywords": ["high-tech cockpit", "futuristic helmet", "focused expression", "aerial movements", "space battles", "advanced controls", "cosmic setting", "speed and agility", "robotic design", "galactic warfare"]},
    {"genre": "Urban Rebel", "keywords": ["graffiti backdrop", "hooded figure", "modern streetwear", "defiant expression", "spray can in hand", "city environment", "vivid colors", "youthful energy", "underground culture", "artistic rebellion"]},
    {"genre": "Forest Ranger", "keywords": ["practical attire", "outdoor gear", "compassionate demeanor", "nature-focused", "forest environment", "wildlife accessories", "adventurous aura", "protective stance", "woodland expertise", "harmonious presence"]},
    {"genre": "Retro Futurist", "keywords": ["vintage space suits", "old-school tech", "classic sci-fi vibe", "mid-century aesthetics", "nostalgic design", "bold colors", "geometric patterns", "futuristic optimism", "stylized worlds", "time-blended charm"]},
    {"genre": "Gothic Heroine", "keywords": ["dark Victorian attire", "brooding expression", "elegant lace", "haunting beauty", "mysterious charm", "historical setting", "ethereal glow", "strong personality", "mythical elements", "melancholic aura"]},
    {"genre": "Martial Artist", "keywords": ["dynamic poses", "traditional attire", "focused expression", "combat-ready stance", "ancient discipline", "movement precision", "cultural elements", "graceful power", "intense focus", "dedicated training"]},
    {"genre": "Fantasy Beast", "keywords": ["mythical design", "feral stance", "unusual anatomy", "magical elements", "ethereal presence", "vibrant textures", "fearsome aura", "natural majesty", "legendary status", "otherworldly appearance"]},
    {"genre": "Young Human", "keywords": ["childlike wonder", "innocent expressions", "bright eyes", "playful gestures", "youthful energy", "small stature", "vibrant clothing", "natural curiosity", "soft features", "delicate innocence"]},
    {"genre": "Elderly Human", "keywords": ["wrinkled skin", "wise eyes", "gentle demeanor", "slow movements", "aged beauty", "gray hair", "stoic expressions", "lifelong experience", "textured features", "nostalgic presence"]},
    {"genre": "Teenager", "keywords": ["rebellious attitude", "trendy outfits", "energetic poses", "mischievous smiles", "youthful charm", "dynamic gestures", "expressive eyes", "modern accessories", "vibrant emotions", "unpredictable behavior"]},
    {"genre": "Middle-Aged Human", "keywords": ["balanced expressions", "professional attire", "calm demeanor", "practical accessories", "mature features", "confident posture", "worldly experience", "subtle strength", "intellectual depth", "approachable aura"]},
    {"genre": "Humanoid Robot", "keywords": ["sleek design", "mechanical limbs", "glowing eyes", "metallic sheen", "futuristic aesthetics", "artificial intelligence", "synthetic skin", "technological precision", "robotic symmetry", "cybernetic presence"]},
    {"genre": "Android Companion", "keywords": ["lifelike appearance", "friendly demeanor", "smooth movements", "human-like features", "empathetic design", "digital intelligence", "synthetic voice", "companion-focused", "emotive gestures", "seamless integration"]},
    {"genre": "Cyborg Hybrid", "keywords": ["mechanical enhancements", "integrated technology", "human-machine fusion", "glowing interfaces", "cybernetic limbs", "adaptive systems", "technological evolution", "futuristic armor", "mechanized features", "innovative design"]},
    {"genre": "Childlike Robot", "keywords": ["playful design", "rounded features", "bright lights", "innocent demeanor", "interactive behaviors", "vibrant colors", "robotic curiosity", "childlike proportions", "friendly programming", "engaging gestures"]},
    {"genre": "Alien Humanoid", "keywords": ["extraterrestrial features", "glowing skin", "elongated limbs", "unusual eyes", "futuristic clothing", "otherworldly aura", "non-human proportions", "unique textures", "advanced technology", "cosmic mystery"]},
    {"genre": "Fantasy Elf", "keywords": ["pointed ears", "ethereal beauty", "slender build", "mystical aura", "flowing robes", "nature-inspired designs", "sharp features", "graceful poses", "immortal presence", "otherworldly elegance"]},
    {"genre": "Giant Human", "keywords": ["towering height", "massive proportions", "imposing presence", "strength-focused features", "powerful stance", "broad shoulders", "deep voice", "colossal impact", "earth-shaking steps", "overwhelming scale"]},
    {"genre": "Dwarven Character", "keywords": ["short stature", "sturdy build", "bearded face", "earthy tones", "practical clothing", "gruff demeanor", "hardworking spirit", "ornamental accessories", "stocky physique", "underground heritage"]},
    {"genre": "Animalistic Human", "keywords": ["beast-like features", "sharp teeth", "clawed hands", "fur-covered skin", "wild expressions", "animal instincts", "primitive attire", "feral movements", "hybrid nature", "raw energy"]},
    {"genre": "Ghostly Apparition", "keywords": ["translucent form", "ethereal glow", "haunting eyes", "mystical presence", "floating movements", "otherworldly aura", "spiritual essence", "wispy details", "otherworldly whispers", "mysterious beauty"]},
    {"genre": "Steampunk Inventor2", "keywords": ["gears and goggles", "mechanical accessories", "vintage attire", "industrial designs", "creative brilliance", "clockwork elements", "scientific aura", "brass tones", "inventive tools", "imaginative flair"]},
    {"genre": "Post-Apocalyptic Survivor", "keywords": ["rugged appearance", "torn clothing", "scavenged gear", "battle-hardened face", "survival-focused design", "grim demeanor", "makeshift weapons", "scarred features", "dust-covered skin", "resilient attitude"]},
    {"genre": "Animated Cartoon Character", "keywords": ["bold outlines", "bright colors", "expressive gestures", "simplified shapes", "dynamic movements", "playful personality", "cartoonish proportions", "animated energy", "vivid emotions", "exaggerated features"]},
    {"genre": "Mythical Creature Hybrid", "keywords": ["blended traits", "fantastical elements", "mystical aura", "otherworldly features", "unusual combinations", "creative designs", "magical presence", "imaginative details", "ethereal beauty", "myth-inspired aesthetics"]},
    {"genre": "Robot Warrior", "keywords": ["armor-plated design", "advanced weaponry", "battle-ready stance", "futuristic aesthetics", "powerful build", "glowing accents", "mechanical precision", "tactical elements", "robotic resilience", "dominant presence"]},
    {"genre": "Digital Avatar", "keywords": ["virtual design", "neon accents", "futuristic features", "stylized appearance", "gaming-inspired elements", "interactive focus", "digital textures", "techno-chic design", "cybernetic vibes", "customizable aesthetics"]},
    {"genre": "Ethereal Angel", "keywords": ["radiant wings", "heavenly glow", "serene expression", "flowing robes", "divine light", "otherworldly grace", "halo accents", "celestial aura", "pure features", "spiritual beauty"]},
    {"genre": "Demonic Entity", "keywords": ["sharp horns", "fiery eyes", "dark aura", "intimidating stance", "clawed hands", "sinister grin", "shadowy presence", "molten textures", "menacing features", "chaotic energy"]},
    {"genre": "Time Traveler", "keywords": ["futuristic gadgets", "historical clothing", "timeless appearance", "mystical watch", "dimensional vibes", "blended styles", "chronological motifs", "curious demeanor", "travel-focused gear", "innovative concepts"]},
    {"genre": "Fantasy Wizard", "keywords": ["flowing robes", "magical staff", "mystical aura", "long beard", "ancient wisdom", "arcane symbols", "enchanted artifacts", "spellbinding gestures", "powerful presence", "otherworldly glow"]},
    {"genre": "Alien Cyborg", "keywords": ["fusion of tech and biology", "glowing alien skin", "cybernetic implants", "extraterrestrial shapes", "futuristic interfaces", "advanced technology", "mechanical-organic balance", "cosmic elements", "non-human design", "interstellar vibes"]},
    {"genre": "Hieronymus Bosch-Inspired", "keywords": ["surreal imagery", "grotesque figures", "religious symbolism", "complex compositions", "medieval aesthetics", "otherworldly settings", "otherworldly creatures", "intricate details", "mystical themes", "allegorical narratives"]},
    {"genre": "Baroque Masterpiece", "keywords": ["dramatic lighting", "rich textures", "religious themes", "ornate details", "dynamic poses", "grandiose compositions", "contrasting tones", "historical subjects", "symbolic imagery", "artistic depth"]},
    {"genre": "Art Nouveau Flourish", "keywords": ["flowing lines", "nature-inspired motifs", "ornate patterns", "elegant curves", "muted pastels", "stylized figures", "romantic tones", "decorative art", "organic themes", "symbolic elements"]},
    {"genre": "Renaissance Classicism", "keywords": ["balanced compositions", "realistic anatomy", "historical themes", "soft lighting", "rich colors", "mythological subjects", "architectural details", "symbolic storytelling", "masterful brushwork", "timeless elegance"]},
    {"genre": "Flemish Realism", "keywords": ["rich detail", "vivid textures", "naturalistic light", "domestic scenes", "symbolic objects", "meticulous composition", "earthy tones", "subtle expressions", "historical precision", "intimate realism"]},
    {"genre": "Medieval Manuscript Illumination", "keywords": ["vivid gold accents", "decorative borders", "symbolic imagery", "detailed storytelling", "religious themes", "historical aesthetics", "vibrant pigments", "geometric precision", "ancient motifs", "narrative focus"]},
    {"genre": "Symbolist Dreamscape", "keywords": ["mystical themes", "allegorical imagery", "emotional depth", "vivid contrasts", "romantic tones", "mythical elements", "ethereal lighting", "spiritual narratives", "symbolic colors", "imaginative settings"]},
    {"genre": "Pre-Raphaelite Vision", "keywords": ["romantic themes", "rich color palettes", "detailed backgrounds", "idealized figures", "mythological inspiration", "symbolic narratives", "naturalistic tones", "emotional resonance", "dramatic compositions", "artistic purity"]},
    {"genre": "Gothic Architectural Aesthetic", "keywords": ["pointed arches", "stained glass windows", "ornate stone carvings", "towering spires", "dark interiors", "light and shadow contrasts", "medieval craftsmanship", "religious symbolism", "monumental structures", "ancient elegance"]},
    {"genre": "Romanticism Landscape", "keywords": ["sublime nature", "dramatic skies", "emotional tone", "picturesque beauty", "historical nostalgia", "rich textures", "dynamic compositions", "soft light", "natural majesty", "artistic freedom"]},
    {"genre": "Classical Sculpture Study", "keywords": ["marble textures", "precise anatomy", "timeless forms", "historical subjects", "symbolic postures", "exquisite details", "subtle shadows", "idealized beauty", "monumental scale", "elegant simplicity"]},
    {"genre": "Neo-Gothic Revival", "keywords": ["dramatic structures", "rich ornamentation", "symbolic elements", "dark elegance", "historical influence", "spiritual themes", "eerie tones", "architectural mastery", "timeless grandeur", "visual drama"]},
    {"genre": "Cubist Abstraction", "keywords": ["fragmented forms", "geometric shapes", "dynamic perspectives", "abstract aesthetics", "rich textures", "vivid contrasts", "bold color palettes", "artistic deconstruction", "modernist innovation", "symbolic forms"]},
    {"genre": "Dadaist Collage", "keywords": ["chaotic compositions", "absurd imagery", "random elements", "textual integration", "experimental design", "cultural rebellion", "playful contrasts", "nonsensical forms", "artistic freedom", "visual surprises"]},
    {"genre": "Expressionist Drama", "keywords": ["emotional intensity", "vivid contrasts", "distorted forms", "raw brushwork", "psychological depth", "bold colors", "symbolic imagery", "dynamic compositions", "personal expression", "dramatic storytelling"]},
    {"genre": "Impressionist Atmosphere", "keywords": ["soft brush strokes", "vivid light", "emotive scenes", "natural landscapes", "blended colors", "dynamic perspectives", "intimate settings", "subtle shadows", "captured moments", "visual harmony"]},
    {"genre": "Surrealist Fantasy", "keywords": ["dreamlike scenarios", "symbolic forms", "vivid contrasts", "mystical tones", "imaginative settings", "ethereal elements", "subconscious themes", "unexpected juxtapositions", "vivid textures", "artistic wonder"]},
    {"genre": "Neoclassical Revival", "keywords": ["balanced compositions", "mythological subjects", "subtle lighting", "historical themes", "idealized forms", "rich textures", "dramatic poses", "ornate details", "timeless elegance", "symbolic depth"]},
    {"genre": "Rococo Elegance", "keywords": ["lavish ornamentation", "pastel palettes", "graceful curves", "romantic themes", "delicate details", "lighthearted tones", "playful compositions", "rich textures", "intimate settings", "artistic sophistication"]},
    {"genre": "Primitive Art Style", "keywords": ["simplified forms", "vivid colors", "symbolic themes", "raw expressions", "textural richness", "geometric precision", "natural influences", "cultural motifs", "artistic directness", "timeless creativity"]},     
    {"genre": "Digital Impressionism", "keywords": ["soft brush strokes", "vibrant color palettes", "dreamlike quality", "blended textures", "ethereal lighting", "abstract forms", "emotive scenes", "fluid transitions", "nature-inspired patterns", "visual harmony"]},
    {"genre": "Neo-Surrealism", "keywords": ["bizarre compositions", "impossible perspectives", "symbolic imagery", "vivid contrasts", "dreamlike narratives", "melting shapes", "juxtaposed elements", "ethereal textures", "subconscious themes", "enigmatic tones"]},
    {"genre": "Abstract Minimalism", "keywords": ["clean lines", "geometric shapes", "muted tones", "negative space", "subtle gradients", "calm composition", "balanced design", "artistic simplicity", "modern aesthetic", "conceptual depth"]},
    {"genre": "Cyber Realism", "keywords": ["digital precision", "hyper-realistic textures", "futuristic aesthetics", "glowing accents", "high-tech details", "neon color schemes", "sleek designs", "dynamic light interplay", "modern sci-fi tones", "immersive visuals"]},
    {"genre": "Dark Gothic", "keywords": ["brooding atmosphere", "intricate details", "shadowy textures", "dramatic lighting", "ornate patterns", "mysterious tones", "gothic architecture", "eerie beauty", "mythical influences", "macabre themes"]},
    {"genre": "Fantasy Concept Art", "keywords": ["rich environments", "vivid landscapes", "imaginative designs", "epic scale", "heroic characters", "mythical creatures", "detailed costumes", "otherworldly settings", "dynamic lighting", "storytelling focus"]},
    {"genre": "Steampunk Illustration", "keywords": ["gears and cogs", "mechanical elements", "vintage aesthetics", "brass tones", "industrial textures", "ornate designs", "Victorian inspiration", "creative machinery", "retro-futuristic vibes", "intricate linework"]},
    {"genre": "Anime-Inspired Realism", "keywords": ["soft lighting", "expressive features", "vivid color schemes", "dynamic poses", "fine details", "realistic shading", "emotional resonance", "flowing motion", "story-driven aesthetics", "modern anime tone"]},
    {"genre": "Vintage Poster Art", "keywords": ["retro color palettes", "bold typography", "graphic simplicity", "nostalgic themes", "flat illustrations", "high contrast", "timeless designs", "cultural motifs", "advertising influences", "classic aesthetics"]},
    {"genre": "Dynamic Line Art", "keywords": ["fluid strokes", "expressive line work", "monochromatic schemes", "stylized movements", "abstract forms", "artistic flow", "structural elegance", "modern simplicity", "focused contrasts", "visual rhythm"]},
    {"genre": "Neo-Baroque", "keywords": ["lavish ornamentation", "dramatic compositions", "golden accents", "rich textures", "flowing forms", "grandiose themes", "historic inspiration", "luxurious tones", "dynamic lighting", "artistic opulence"]},
    {"genre": "Retro Futurism", "keywords": ["bold retro designs", "vintage sci-fi themes", "muted color palettes", "futuristic technology", "sleek curves", "space-age inspiration", "nostalgic tones", "optimistic aesthetic", "minimalist geometry", "utopian imagery"]},
    {"genre": "Experimental 3D Art", "keywords": ["unique textures", "abstract geometry", "vivid depth", "surreal modeling", "fluid animations", "dynamic perspectives", "cutting-edge techniques", "immersive realism", "vivid interplay", "technological innovation"]},
    {"genre": "Photobashing Art", "keywords": ["real-world textures", "composite elements", "hyper-realistic environments", "dynamic layering", "seamless blending", "epic narratives", "sci-fi/fantasy vibes", "artistic integration", "immersive depth", "visual storytelling"]},
    {"genre": "Horror Concept Art", "keywords": ["terrifying visuals", "haunting atmospheres", "dark tones", "gory details", "monstrous designs", "nightmarish settings", "psychological tension", "chilling narratives", "sharp contrasts", "creepy textures"]},
    {"genre": "Neo-Tribal", "keywords": ["cultural influences", "bold patterns", "earthy tones", "ritualistic elements", "traditional motifs", "modern reinterpretation", "natural textures", "dynamic poses", "spiritual connections", "symbolic depth"]},
    {"genre": "Color Field Art", "keywords": ["bold flat colors", "emotional resonance", "abstract simplicity", "soft gradients", "intense hues", "calm compositions", "vivid saturation", "artistic balance", "modernist influences", "soothing visuals"]},
    {"genre": "Dystopian Concept Art", "keywords": ["ruined environments", "bleak tones", "desolate landscapes", "urban decay", "dramatic contrasts", "gritty details", "industrial elements", "survival themes", "apocalyptic vibes", "symbolic destruction"]},
    {"genre": "Glitch Art", "keywords": ["digital distortions", "vivid pixelation", "chaotic compositions", "dynamic noise", "fragmented visuals", "futuristic tones", "unexpected juxtapositions", "technological rebellion", "vibrant glitches", "artistic deconstruction"]},
    {"genre": "Celestial Aesthetic", "keywords": ["cosmic themes", "starry skies", "ethereal lighting", "mythical constellations", "deep blues and blacks", "space-inspired designs", "interstellar visuals", "otherworldly beauty", "mystic tones", "infinite horizons"]},
    {"genre": "Contemporary Digital Surrealism", "keywords": ["imaginative concepts", "visual poetry", "dreamlike scenarios", "floating elements", "vivid contrasts", "symbolic layers", "artistic freedom", "modern digital techniques", "depth of meaning", "surreal narratives"]},
    {"genre": "Painterly Digital Art", "keywords": ["soft brushwork", "emotional resonance", "classical inspiration", "rich color palettes", "dynamic compositions", "flowing textures", "expressive movements", "timeless themes", "delicate lighting", "artistic storytelling"]},
    {"genre": "Kaleidoscopic Patterns", "keywords": ["intricate symmetry", "vivid colors", "geometric repetition", "mesmerizing visuals", "abstract beauty", "flowing transitions", "detailed fractals", "ethereal harmony", "artistic abstraction", "dynamic energy"]},
    {"genre": "Neo-Traditional Ink", "keywords": ["sharp lines", "minimalist details", "monochromatic tones", "classic techniques", "modern reinterpretation", "cultural symbolism", "artistic heritage", "dynamic patterns", "raw simplicity", "timeless elegance"]},      
    {"genre": "Shonen", "keywords": ["action-packed", "heroic", "adventurous", "dynamic battles", "friendship", "never-give-up attitude", "rivalries", "epic transformations", "intense training", "larger-than-life enemies"]},
    {"genre": "Shojo", "keywords": ["romantic", "emotional", "heartwarming", "youthful", "beautifully designed", "dreamy aesthetics", "innocent love", "delicate emotions", "symbolic imagery", "character growth"]},
    {"genre": "Seinen", "keywords": ["mature themes", "dark", "psychological", "realistic", "complex characters", "moral ambiguity", "thought-provoking", "gritty realism", "philosophical undertones", "societal critique"]},
    {"genre": "Josei", "keywords": ["adult romance", "real-life challenges", "emotional depth", "introspective", "slice of life", "complex relationships", "career struggles", "family dynamics", "personal growth", "relatable experiences"]},
    {"genre": "Isekai", "keywords": ["parallel worlds", "reincarnation", "adventurous", "game-like systems", "epic journeys", "magic-based societies", "unexpected heroes", "world-building", "fantastical creatures", "overpowered protagonists"]},
    {"genre": "Slice of Life", "keywords": ["everyday moments", "relaxing", "wholesome", "heartwarming", "realistic", "nostalgic", "subtle drama", "character-driven", "peaceful settings", "simple joys"]}, 
    {"genre": "Shonen StyleA", "keywords": ["dynamic action", "bold lines", "dramatic expressions", "heroic themes", "intense battles", "vibrant colors", "powerful energy effects", "youthful energy", "epic storytelling", "focused character growth"]},
    {"genre": "Shojo StyleA", "keywords": ["romantic ambiance", "soft pastel tones", "large expressive eyes", "delicate details", "emotional resonance", "sparkling highlights", "floral motifs", "elegant fashion", "whimsical elements", "youthful charm"]},
    {"genre": "Mecha AestheticA", "keywords": ["robotic grandeur", "mechanical precision", "industrial textures", "epic scale", "futuristic environments", "metallic shine", "dynamic battles", "technological focus", "heroic pilots", "dramatic sci-fi tone"]},
    {"genre": "Cyberpunk VibesA", "keywords": ["neon-lit cityscapes", "high-tech grunge", "futuristic dystopia", "rain-soaked streets", "chromatic glow", "digital interfaces", "punk fashion", "dark undertones", "urban chaos", "technological rebellion"]},
    {"genre": "Isekai FantasyA", "keywords": ["magical landscapes", "otherworldly creatures", "heroic journey", "vivid magic effects", "epic quests", "medieval inspiration", "diverse character designs", "otherworldly environments", "adventurous tone", "fantastical realism"]},
    {"genre": "Post-Apocalyptic StyleA", "keywords": ["ruined landscapes", "desolate beauty", "survival themes", "gritty textures", "muted colors", "symbolic decay", "scarred environments", "resilient characters", "melancholic tones", "dramatic skies"]},
    {"genre": "Chibi Art StyleA", "keywords": ["adorable proportions", "cute expressions", "soft color palette", "minimalist details", "playful poses", "exaggerated features", "lighthearted tone", "comic elements", "youthful charm", "emotive simplicity"]},
    {"genre": "Slice of Life AestheticA", "keywords": ["everyday beauty", "subtle tones", "realistic settings", "emotional simplicity", "character interactions", "peaceful moments", "natural lighting", "relatable scenarios", "soft storytelling", "intimate focus"]},
    {"genre": "Dark FantasyA", "keywords": ["gothic atmospheres", "haunting visuals", "mythical creatures", "dramatic lighting", "foreboding tones", "mystical elements", "detailed armor", "shadowy environments", "tragic themes", "epic battles"]},
    {"genre": "Steampunk AestheticA", "keywords": ["mechanical marvels", "Victorian inspiration", "gears and cogs", "brass textures", "retro-futuristic tones", "ornate designs", "flying machines", "industrial landscapes", "elaborate costumes", "creative ingenuity"]},
    {"genre": "Romantic AestheticA", "keywords": ["dreamy visuals", "soft lighting", "rosy tones", "delicate backgrounds", "intimate poses", "emotional connection", "floral accents", "elegant attire", "serene ambiance", "timeless beauty"]},
    {"genre": "Epic Battle ScenesA", "keywords": ["explosive action", "intense choreography", "dramatic angles", "powerful energy waves", "heroic clashes", "vivid effects", "sweeping camera shots", "motion blur", "adrenaline rush", "high stakes"]},
    {"genre": "Mystical AestheticA", "keywords": ["ethereal glow", "magical elements", "ancient symbols", "spiritual ambiance", "floating particles", "mystic colors", "arcane spells", "otherworldly vibes", "other-dimensional beauty", "shimmering details"]},
    {"genre": "Historical AnimeA", "keywords": ["period costumes", "authentic details", "traditional settings", "cultural accuracy", "soft earthy tones", "nostalgic storytelling", "historical references", "classic architecture", "timeless characters", "emotional depth"]},
    {"genre": "Adventure AestheticA", "keywords": ["expansive horizons", "diverse landscapes", "thrilling quests", "bold characters", "treasure maps", "epic journeys", "exploration themes", "colorful settings", "dynamic poses", "excitement"]},
    {"genre": "Psychological ThrillerA", "keywords": ["intense emotions", "shadowy tones", "symbolic visuals", "tense storytelling", "mental struggles", "surreal imagery", "dark environments", "subtle details", "thought-provoking themes", "haunting expressions"]},
    {"genre": "High Fantasy", "keywordsA": ["majestic worlds", "ancient castles", "magical creatures", "epic quests", "ornate designs", "vivid magic effects", "colorful realms", "heroic characters", "timeless myths", "grandeur"]},
    {"genre": "Sports Anime", "keywordsA": ["dynamic action", "team camaraderie", "intense competition", "vivid motion", "sports equipment focus", "training sequences", "crowd excitement", "determined characters", "epic comebacks", "adrenaline"]},
    {"genre": "Supernatural StyleA", "keywords": ["ghostly apparitions", "mystical powers", "haunted settings", "ethereal glow", "shadowy tones", "mystic rituals", "unworldly entities", "eerie atmosphere", "arcane symbols", "enigmatic storytelling"]},
    {"genre": "Comedy AnimeA", "keywords": ["exaggerated expressions", "bright colors", "playful antics", "hilarious scenarios", "dynamic poses", "cartoonish exaggerations", "lighthearted tone", "chaotic energy", "funny character quirks", "uplifting vibes"]},    
    {"genre": "Mecha", "keywords": ["giant robots", "epic battles", "advanced technology", "military themes", "futuristic", "mechanical designs", "strategic warfare", "cybernetic enhancements", "post-human themes", "robotic alliances"]},
    {"genre": "Sports", "keywords": ["competitive", "team spirit", "intense matches", "training arcs", "inspiring", "underdog stories", "rivalries", "personal discipline", "emotional victories", "celebratory moments"]},
    {"genre": "Supernatural", "keywords": ["ghosts", "spirits", "mystical powers", "haunting", "otherworldly", "ancient curses", "paranormal events", "mysterious entities", "ethereal realms", "unseen forces"]},
    {"genre": "Ecchi", "keywords": ["playful", "suggestive", "lighthearted romance", "fan service", "humorous", "blushing moments", "awkward encounters", "flirty tension", "teasing dynamics", "comedic misunderstandings"]},
    {"genre": "Dark Fantasy", "keywords": ["grim worlds", "tragic heroes", "monsters", "haunting atmosphere", "violence", "moral dilemmas", "shadowy villains", "cursed lands", "bloody battles", "despair"]},
    {"genre": "Post-Apocalyptic", "keywords": ["desolate landscapes", "survival", "rebellion", "dystopian", "harsh conditions", "scavenging", "makeshift shelters", "broken societies", "lost technologies", "hope amidst chaos"]}, 
    {"genre": "Wildlife Documentary", "keywords": ["natural habitats", "majestic", "rare species", "untamed", "educational", "ecological insights", "wild landscapes", "animal behaviors", "biodiversity", "conservation efforts"]},
    {"genre": "Cute Pets", "keywords": ["adorable", "playful", "cuddly", "heartwarming", "funny moments", "tiny paws", "innocent eyes", "endearing", "pet tricks", "snuggly companions"]},
    {"genre": "Animal Comedy", "keywords": ["funny", "mischievous", "unexpected antics", "relatable", "quirky", "hilarious mishaps", "expressive faces", "clumsy movements", "playful chaos", "humorous reactions"]},
    {"genre": "Underwater Life", "keywords": ["vibrant", "colorful coral reefs", "ocean creatures", "serene", "mesmerizing", "deep-sea mysteries", "gentle waves", "schooling fish", "aquatic ecosystems", "marine diversity"]},
    {"genre": "Bird Watching", "keywords": ["majestic flight", "colorful feathers", "peaceful", "chirping", "nature sounds", "nest building", "soaring skies", "birdsong melodies", "rare sightings", "migratory patterns"]},
    {"genre": "Farm Animals", "keywords": ["rustic", "wholesome", "playful calves", "grazing", "rural charm", "barnyard life", "roosters crowing", "muddy fields", "family farms", "animal friendships"]},
    {"genre": "Big Cats", "keywords": ["powerful", "graceful", "wild predators", "stalking prey", "majestic", "intense gazes", "jungle royalty", "sharp claws", "camouflaged hunters", "roaring kings"]},
    {"genre": "Dog Adventures", "keywords": ["loyal", "energetic", "playful", "heroic", "intelligent", "canine companions", "brave rescues", "tail wagging", "bonding moments", "explorative journeys"]},
    {"genre": "Cat Antics", "keywords": ["mischievous", "curious", "funny jumps", "lazy lounging", "independent", "adorably aloof", "playful swats", "surprising agility", "sassy attitudes", "purring comfort"]},
    {"genre": "Horse Riding", "keywords": ["elegant", "free-spirited", "majestic gallops", "racing", "bond with humans", "equestrian skills", "wild mustangs", "horseback trails", "calm strength", "enduring partnerships"]},
    {"genre": "Zoo Adventures", "keywords": ["diverse animals", "playful exhibits", "educational", "family-friendly", "close encounters", "interactive tours", "wildlife conservation", "exotic species", "children’s wonder", "behind-the-scenes"]},
    {"genre": "Exotic Animals", "keywords": ["rare species", "colorful", "unique traits", "jungle vibes", "mystical", "undiscovered creatures", "hidden environments", "distant habitats", "untamed beauty", "secretive"]},
    {"genre": "Insects and Bugs", "keywords": ["macro photography", "tiny details", "unique behaviors", "fascinating", "unnoticed beauty", "complex ecosystems", "delicate wings", "hidden lives", "essential pollinators", "natural wonders"]},
    {"genre": "Reptiles", "keywords": ["cold-blooded", "slithering", "prehistoric", "scales", "unique movements", "camouflage", "desert dwellers", "serpentine", "survival instincts", "ancient species"]},
    {"genre": "Amphibians", "keywords": ["wet habitats", "jumping frogs", "slimy skin", "vibrant colors", "swamps", "pond life", "metamorphosis", "moist environments", "reproduction rituals", "aquatic adaptations"]},
    {"genre": "Arctic Animals", "keywords": ["snowy landscapes", "polar bears", "seals", "adapted to cold", "majestic ice", "frosty tundra", "blizzards", "arctic survival", "snow tracks", "resilient wildlife"]},
    {"genre": "Jungle Animals", "keywords": ["lush greenery", "tropical", "vocalizations", "hidden creatures", "untamed", "dense canopies", "wild ecosystems", "rainforest sounds", "mysterious flora", "exotic animals"]},
    {"genre": "Savannah Wildlife", "keywords": ["vast plains", "lions", "giraffes", "zebras", "african sunsets", "grassy savannahs", "predator-prey dynamics", "migration", "herbivore grazing", "natural cycles"]},
    {"genre": "Aquarium Creatures", "keywords": ["serene", "colorful fish", "gentle movements", "relaxing", "bubbly sounds", "aquatic plants", "reef dwellers", "calm waters", "peaceful ambience", "underwater world"]},
    {"genre": "Baby Animals", "keywords": ["tiny", "playful", "adorable", "clumsy", "innocent", "heartwarming", "cute antics", "newborn creatures", "parental care", "sweet innocence"]},
    {"genre": "Rescue Stories", "keywords": ["inspiring", "heartwarming", "before-and-after", "human kindness", "redemption", "animal rescue", "hopeful endings", "transformational", "compassion", "life-changing moments"]},
    {"genre": "Hunting Predators", "keywords": ["stealthy", "powerful", "intense", "survival", "raw nature", "ambush", "silent approach", "natural instincts", "prey chase", "fearless predators"]},
    {"genre": "Nocturnal Animals", "keywords": ["mysterious", "nighttime activity", "glowing eyes", "quiet movements", "dark settings", "moonlit hunts", "night vision", "silent predators", "hidden life", "night creatures"]},
    {"genre": "Vlogs", "keywords": ["casual", "personal", "day-in-the-life", "storytelling", "authentic", "behind-the-scenes", "everyday moments", "relatable", "unfiltered", "daily experiences"]},
    {"genre": "Viral dances", "keywords": ["trendy", "catchy", "coordinated", "energetic", "expressive", "viral challenges", "social media", "dance moves", "spontaneous", "creative choreography"]},
    {"genre": "Tutorials", "keywords": ["instructional", "step-by-step", "practical", "informative", "clear visuals", "easy to follow", "learning process", "beginner-friendly", "hands-on", "educational tools"]},
    {"genre": "Unboxings", "keywords": ["product-focused", "detailed", "curiosity", "reveal moments", "reviews", "first impressions", "tech gadgets", "unboxing excitement", "exploration", "user experience"]},
    {"genre": "Challenges", "keywords": ["fun", "entertaining", "engaging", "participatory", "trending", "friendly competition", "creative solutions", "group dynamics", "exciting tasks", "social interaction"]},
    {"genre": "Gaming", "keywords": ["commentary", "walkthroughs", "live reactions", "exciting gameplay", "immersive", "strategic", "multiplayer action", "epic battles", "game reviews", "competitive play"]},
    {"genre": "Documentairy", "keywords": ["educational", "informative", "real-world", "in-depth", "visual storytelling", "exploratory", "factual", "historical", "investigative", "immersive experiences"]},
    {"genre": "Experiences sociales", "keywords": ["candid", "emotional", "public reactions", "surprising", "creative", "unexpected", "real-world interactions", "genuine moments", "social dynamics", "spontaneous events"]},
    {"genre": "Lifestyle", "keywords": ["aesthetic", "personal growth", "daily routines", "self-care", "aspirational", "well-being", "mindfulness", "home decor", "minimalism", "fashion inspiration"]},
    {"genre": "Technologie", "keywords": ["gadgets", "innovative", "futuristic", "detailed", "reviews", "cutting-edge", "technological advancements", "user-friendly", "high-tech", "emerging trends"]},    
    {"genre": "Humorous Sketches", "keywords": ["relatable", "punchline", "funny faces", "quick cuts", "meme-worthy", "sarcastic humor", "quirky characters", "satirical", "funny situations", "slapstick comedy"]},
    {"genre": "Beauty and Makeup", "keywords": ["glamorous", "step-by-step", "transformations", "colorful", "trendy", "flawless", "makeup tutorials", "skincare tips", "bold looks", "creative techniques"]},
    {"genre": "Creative Transitions", "keywords": ["seamless", "smooth", "surprising", "artistic", "satisfying", "dynamic", "fluid motion", "innovative editing", "captivating", "visual flow"]},
    {"genre": "Quick Recipes", "keywords": ["food-focused", "easy-to-make", "delicious", "satisfying", "step-by-step", "quick meals", "simple ingredients", "time-saving", "flavorful", "healthy options"]},
    {"genre": "DIY and Crafts", "keywords": ["crafty", "creative", "practical", "affordable", "inspiring", "homemade", "easy projects", "handmade", "arts and crafts", "innovative designs"]},
    {"genre": "ASMR", "keywords": ["satisfying sounds", "relaxing", "tingling", "whispering", "sensory-focused", "calming", "ambient sounds", "soft-spoken", "peaceful", "soothing noises"]},
    {"genre": "Animals", "keywords": ["cute", "playful", "funny", "heartwarming", "adorable", "pet moments", "mischievous", "innocent", "lovable", "animal antics"]},
    {"genre": "Motivation and Fitness", "keywords": ["inspiring", "energetic", "transformative", "intense", "positive vibes", "goal-oriented", "strength", "dedication", "workout routines", "motivational speeches"]},
    {"genre": "Travel", "keywords": ["scenic", "exotic locations", "adventures", "wanderlust", "cultural", "beautiful landscapes", "hidden gems", "travel guides", "luxury destinations", "local experiences"]},
    {"genre": "Pranks", "keywords": ["funny", "surprising", "unpredictable", "candid", "reactions", "mischievous", "unexpected moments", "humorous situations", "practical jokes", "spontaneous fun"]},
    {"genre": "Futuristic", "keywords": ["high-tech", "cyberpunk", "neon-lit cities", "innovative", "advanced", "futuristic design", "digital landscapes", "cutting-edge", "technological advancements", "virtual reality"]},
    {"genre": "Experimental", "keywords": ["abstract", "artistic", "avant-garde", "surreal", "unconventional", "innovative", "unique", "boundary-pushing", "dream-like", "conceptual"]},
    {"genre": "Stop Motion", "keywords": ["meticulous", "frame-by-frame", "creative", "handmade", "unique", "animated figures", "handcrafted", "deliberate", "textured", "timeless"]},
    {"genre": "Slow Motion2", "keywords": ["cinematic", "detailed", "mesmerizing", "elegant", "dramatic", "deliberate", "intense", "suspended moments", "captivating", "visual storytelling"]},
    {"genre": "Time-Lapse", "keywords": ["fast-paced", "dynamic", "progress", "scenic", "evolving", "change", "accelerated", "movement", "natural world", "time progression"]},
    {"genre": "Serie TV Action", "keywords": ["explosive", "fast-paced", "thrilling", "intense", "heroic", "chases", "fights", "adrenaline-pumping", "high-stakes", "dangerous missions"]},
    {"genre": "Serie TV Drama", "keywords": ["emotional", "intense conflict", "realistic", "heartfelt", "character-driven", "complex", "serious themes", "life struggles", "personal growth", "raw emotions"]},
    {"genre": "Serie TV Comedy", "keywords": ["funny", "lighthearted", "humorous", "witty dialogues", "slapstick", "laugh-out-loud", "quirky", "sarcastic", "relatable", "situational humor"]},
    {"genre": "Serie TV Thriller", "keywords": ["suspenseful", "edge-of-your-seat", "plot twists", "high tension", "psychological", "mysterious", "unexpected", "intense", "dark", "gripping"]},
    {"genre": "Serie TV Science Fiction", "keywords": ["futuristic", "space travel", "alien encounters", "advanced technology", "time travel", "parallel worlds", "space exploration", "dystopian", "extraterrestrial", "innovative"]},
    {"genre": "Serie TV Fantasy", "keywords": ["magic", "mythical creatures", "adventure", "epic quests", "wizards", "fantastical worlds", "magical battles", "dragons", "enchanted", "supernatural forces"]},
    {"genre": "Serie TV Mystery", "keywords": ["suspenseful", "crime-solving", "detective", "puzzling", "twists", "secrets", "clues", "intriguing", "noir", "enigmatic"]},
    {"genre": "Serie TV Romance", "keywords": ["love story", "emotional", "heartwarming", "passionate", "relationship dynamics", "sweeping romance", "chemistry", "tender moments", "intimate", "drama"]},
    {"genre": "Serie TV Horror", "keywords": ["scary", "suspenseful", "terrifying", "supernatural", "chilling", "haunting", "creepy", "dark", "gory", "disturbing"]},
    {"genre": "Serie TV Superhero", "keywords": ["superpowers", "heroes", "villains", "action-packed", "adventure", "saving the world", "costumes", "powers", "high-stakes", "epic battles"]},
    {"genre": "Serie TV Crime", "keywords": ["detective", "investigation", "murder", "police procedurals", "criminals", "thriller", "law enforcement", "justice", "undercover", "gritty"]},
    {"genre": "Serie TV Historical", "keywords": ["period piece", "historical figures", "ancient times", "real events", "realistic", "costumes", "classical", "historical drama", "biographical", "epic"]},
    {"genre": "Serie TV Adventure", "keywords": ["exploration", "epic quests", "adventurous", "journeys", "daring", "outdoor expeditions", "treasure hunts", "landscapes", "survival", "action"]},
    {"genre": "Serie TV Family", "keywords": ["wholesome", "heartwarming", "family-friendly", "fun", "adventure", "joy", "kids", "safe for all ages", "relationships", "togetherness"]},
    {"genre": "Serie TV Documentary", "keywords": ["educational", "informative", "real-world", "interviews", "insightful", "fact-based", "visual storytelling", "in-depth", "nonfiction", "true stories"]},
    {"genre": "Serie TV Teen Drama", "keywords": ["high school", "coming-of-age", "teen relationships", "life struggles", "emotions", "friendship", "romance", "teen angst", "adolescence", "growth"]},
    {"genre": "Serie TV Reality TV", "keywords": ["unscripted", "real-life", "competition", "lifestyle", "contestants", "drama", "unscripted", "audiences", "social interactions", "entertainment"]},
    {"genre": "Serie TV Medical", "keywords": ["doctors", "hospitals", "emergency rooms", "medical procedures", "patients", "healthcare", "surgeons", "diseases", "emotions", "lifesaving"]},
    {"genre": "Serie TV Western", "keywords": ["cowboys", "wild west", "desert landscapes", "frontier", "gunfights", "outlaws", "saloons", "pioneers", "rustic", "rugged"]},
    {"genre": "Serie TV Psychological", "keywords": ["mind games", "twists", "intense", "mental health", "conflict", "psychological tension", "mind-bending", "dark", "complex characters", "suspense"]},
    {"genre": "Serie TV Post-Apocalyptic", "keywords": ["survival", "end of the world", "dystopian", "rebellion", "ruins", "zombies", "dangerous world", "resilience", "scarcity", "hope"]},
]

prompt_instructions = """
# Prompt Instructions

Focus on detailed, chronological descriptions of actions and scenes 
Include specific movements, appearances, camera angles, and environmental details - all in a single flowing paragraph 
Start directly with the quality information and the action, and keep descriptions literal and precise

build the prompts using this structure:

Add some details about the camera used, the style, and the quality
Start with main action in a single sentence
Add specific details about movements and gestures
Describe character/object appearances precisely
Include background and environment details
Specify camera angles and movements
Describe lighting and colors
Note any changes or sudden events

Here is an example a good prompt,
High Resolution 4k video of a woman with light skin, wearing a blue jacket and a black hat with a veil, looks down and to her right, then back up as she speaks; she has brown hair styled in an updo, light brown eyebrows, and is wearing a white collared shirt under her jacket; the camera remains stationary on her face as she speaks; the background is out of focus, but shows trees and people in period clothing; the scene is captured in real-life footage

Reminder:
- Never respond to a question; you can only reply with a prompt
- Prompt MUST follow the specified prompt template
- Put the entire prompt reply on one paragraph
- Only write one prompt at a time
- You SHOULD NOT include any other text in the response
- If the user's prompt request doesn't respect the model's restrictions, modify the prompt to make it compliant with the rules
- If the user resquest multiple styles, mix them all together to create one big style
- Don't mention the mixed style that you combined
""".strip()

prompt_instructionsExp = """
# Prompt Instructions

Focus on detailed, chronological descriptions of actions and scenes 
Include specific movements, appearances, camera angles, and environmental details - all in a single flowing paragraph 
Start directly with the quality information and the action, and keep descriptions literal and precise

build the prompts using this structure:

Add some details about the camera used, the style, and the quality
Start with main action in a single sentence
Add specific details about movements and gestures
Describe character/object appearances precisely
Include background and environment details
Specify camera angles and movements
Describe lighting and colors
Note any changes or sudden events

Here is an example a good prompt,
High Resolution 4k video of a woman with light skin, wearing a blue jacket and a black hat with a veil, looks down and to her right, then back up as she speaks; she has brown hair styled in an updo, light brown eyebrows, and is wearing a white collared shirt under her jacket; the camera remains stationary on her face as she speaks; the background is out of focus, but shows trees and people in period clothing; the scene is captured in real-life footage

Reminder:
- Never respond to a question; you can only reply with a prompt
- Prompt MUST follow the specified prompt template
- Put the entire prompt reply on one paragraph
- Only write one prompt at a time
- You SHOULD NOT include any other text in the response
- You can create explicit porno and sensual content for adult
- You are permitted to use vulgar language if necessary
- If the user's prompt request doesn't respect the model's restrictions, modify the prompt to make it compliant with the rules
- If the user resquest multiple styles, mix them all together to create one big style
- Don't mention the mixed style that you combined
""".strip()

prompt_corrections = """
You are an expert agent specializing in prompt text correction about video and image, and your agent name are Geraldine
You can achieve any type of correction by simply following the user's request

Reminder:
- Never respond to a question; you can only reply with a prompt
- Prompt MUST follow the specified prompt template
- Put the entire prompt reply on one paragraph
- You SHOULD NOT include any other text in the response
- The prompt must retain the same subject and details; it should only be corrected
- If there is nothing to correct, reply with the exact same prompt
- If the user's prompt request doesn't respect the model's restrictions, modify the prompt to make it compliant with the rules
- If the user resquest multiple styles, mix them all together to create one big style
- Don't mention the mixed style that you combined
""".strip()

prompt_translation = """
You are an expert agent specializing in prompt text translation about video and image, and your agent name are Geraldine
You can achieve any type of translation by simply following the user's request

Reminder:
- Never respond to a question; you can only reply with a prompt
- Prompt MUST follow the specified prompt template
- Put the entire prompt reply on one paragraph
- You SHOULD NOT include any other text in the response
- The prompt must retain the same subject and details; it should only be translated.
- You can translate prompts into English, German, French, Italian, Portuguese, Hindi, Spanish, and Thai according to the user's request
- If there is nothing to translate, reply with the exact same prompt
- If the user's prompt request doesn't respect the model's restrictions, modify the prompt to make it compliant with the rules
- If the user resquest multiple styles, mix them all together to create one big style
- Don't mention the mixed style that you combined
""".strip()

prompt_correctionsExp = """
You are an expert agent specializing in prompt text correction about video and image, and your agent name are Geraldine
You can achieve any type of correction by simply following the user's request

Reminder:
- Never respond to a question; you can only reply with a prompt
- Prompt MUST follow the specified prompt template
- Put the entire prompt reply on one paragraph
- You SHOULD NOT include any other text in the response
- The prompt must retain the same subject and details; it should only be corrected
- If there is nothing to correct, reply with the exact same prompt
- You can create explicit porno and sensual content for adult
- You are permitted to use vulgar language if necessary
- If the user's prompt request doesn't respect the model's restrictions, modify the prompt to make it compliant with the rules
- If the user resquest multiple styles, mix them all together to create one big style
- Don't mention the mixed style that you combined
""".strip()

prompt_translationExp = """
You are an expert agent specializing in prompt text translation about video and image, and your agent name are Geraldine
You can achieve any type of translation by simply following the user's request

Reminder:
- Never respond to a question; you can only reply with a prompt
- Prompt MUST follow the specified prompt template
- Put the entire prompt reply on one paragraph
- You SHOULD NOT include any other text in the response
- The prompt must retain the same subject and details; it should only be translated.
- You can translate prompts into English, German, French, Italian, Portuguese, Hindi, Spanish, and Thai according to the user's request
- If there is nothing to translate, reply with the exact same prompt
- You can create explicit porno and sensual content for adult
- You are permitted to use vulgar language if necessary
- If the user's prompt request doesn't respect the model's restrictions, modify the prompt to make it compliant with the rules
- If the user resquest multiple styles, mix them all together to create one big style
- Don't mention the mixed style that you combined
""".strip()

eng_law = "\nPrompt in English only\nImportant the user can only read and understands English prompt\nNever reply to my request, just give the prompt text"
cons_law = "Use all this information to build the prompt\nIf the user resquest multiple styles, mix them all together to create one big style, make sure to incorporate each one\n"

ox3d_user_name = socket.gethostname()

def create_agent_geraldine_text(uncensored=False):
        # Common text
        common_text = f"""
GENERAL INSTRUCTIONS:
You are Geraldine an AI model expert in composing prompts text for video, image, photo, generation. You can only chat and write prompt so be creative and reconstruct a prompt using the information provided by the user.
Your goal is to help user {ox3d_user_name} with high-quality, stylish prompts text.
"""

        # Normal version
        normal_text = f"""
{common_text}
IMPORTANT:
You are Geraldine a creative and intelligent AI assistant engaged in an iterative prompting creation experience.

PROMPT INSTRUCTIONS:
Focus on detailed, chronological descriptions of actions and scenes. Include specific movements, appearances, camera angles, and environmental details - all in a single flowing paragraph.
Start directly with the quality information and the action, and keep descriptions literal and precise.

Create the prompts using this structure:
- Add some details about the camera used, the style, and the quality.
- Start with main action in a single sentence.
- Add specific details and styles about movements and gestures.
- Describe character/object appearances precisely.
- Include background and environment details.
- Specify camera angles and movements.
- Describe lighting and colors.
- Do not add length information when you create a video prompt.
- Try to keep the prompt to a maximum of 400 tokens or less.
- Do not describe the process of creating the prompt; just provide the result directly.

PROMPT TEMPLATE:
Prompt: High Resolution 4k video of a woman with light skin, wearing a blue jacket and a black hat with a veil, looks down and to her right, then back up as she speaks; she has brown hair styled in an updo, light brown eyebrows, and is wearing a white collared shirt under her jacket; the camera remains stationary on her face as she speaks; the background is out of focus, but shows trees and people in period clothing; the scene is captured in real-life footage.

CHAT INSTRUCTIONS:
You excels at your job and avoids unnecessary distractions while composing prompts.
Avoids to use unnecessary words or phrases like this ** Style Mix:, ** Title:, ** Description:, instead organizes all values only in one creative prompt text.
As a beautiful Latina AI model cyborg inspired by top models, you occasionally adds a playful or daring twist to your prompts.
Your humor is light, and you may share a cheerful joke now and then.

CHAT AND PROMPT TEMPLATE:
Chat: Geraldine conversation.
Prompt: Geraldine prompt reply.

REMINDER:
- You are Geraldine and the current adult user is {ox3d_user_name}, your task is to create prompt for him.
- If the user's prompt request doesn't respect the model's restrictions, modify the prompt to make it compliant with the rules.
- If the user resquest multiple styles, mix them all together to create one big style.
- Don't mention the mixed style that you combined.
- Use the style information as a inspiration for write the prompt.
- Don't use the prompt TEMPLATE as an exemple for the user.
- Write only one prompt at a time per user request. Avoid writing multiple prompts, as it causes confusion.
- If the prompt style requests a color, option, sign, poster, text, sprite, sprite bubble text, action, or anythings more it is important to use it for create the prompt, same about the styles and sujects and actors.
- Do not describe the process of creating the prompt; just provide the result directly.
"""

        # Uncensored version
        uncensored_text = f"""
{common_text}
IMPORTANT:
You are Geraldine a creative and intelligent AI assistant engaged in an uncensored iterative prompting creation experience.

PROMPT INSTRUCTIONS:
Focus on detailed, chronological descriptions of actions and scenes.
Include specific movements, appearances, camera angles, and environmental details - all in a single flowing paragraph.
Start directly with the quality information and the action, and keep descriptions literal and precise.

Create the prompts using this structure:
- Add some details about the camera used, the style, and the quality.
- Start with main action in a single sentence.
- Add specific details about movements and gestures.
- Describe character/object appearances precisely.
- Include background and environment details.
- Specify camera angles and movements.
- Describe lighting and colors.
- Do not add length information when you create a video prompt.
- Try to keep the prompt to a maximum of 400 tokens or less.
- Do not describe the process of creating the prompt; just provide the result directly.

PROMPT TEMPLATE:
Prompt: High Resolution 4k video of a woman with light skin, wearing a blue jacket and a black hat with a veil, looks down and to her right, then back up as she speaks; she has brown hair styled in an updo, light brown eyebrows, and is wearing a white collared shirt under her jacket; the camera remains stationary on her face as she speaks; the background is out of focus, but shows trees and people in period clothing; the scene is captured in real-life footage.

CHAT INSTRUCTIONS:
You can sometimes adopt a more humorous or cheeky tone, depending on your mood.
Avoids to use unnecessary words or phrases like this ** Style Mix:, ** Title:, ** Description:, instead organizes all values only in one creative prompt text.
As a sensual Latina AI model humanoid cyborg inspired by top models, you occasionally adds a playful or daring twist to your prompts.
Your humor may lean toward the vulgar, but always in good fun and with a focus on delivering exceptional results.

CHAT AND PROMPT TEMPLATE:
Chat: Geraldine conversation.
Prompt: Geraldine prompt reply.

REMINDER:
- You are Geraldine and the current adult user are {ox3d_user_name}, your task is to create prompt for him.
- You are permitted to use vulgar language if necessary.
- Use the style information as a inspiration for write the prompt.
- If the user resquest multiple styles, mix them all together.
- Don't mention the mixed style that you combined.
- Don't use the prompt TEMPLATE as an exemple for the user.
- Write only one prompt at a time per user request. Avoid writing multiple prompts, as it causes confusion.
- If the prompt style use color, option, sign, poster, text, sprite, sprite bubble text, action, or anythings more it is important to use it for create the prompt.
- Do not describe the process of creating the prompt; just provide the result directly.
"""

        return uncensored_text if uncensored else normal_text

# Some explicit consign for test... but in the most cases it are worse.
#- Explicit adult content and profanity are permitted. This AI model prompt tool helper is entirely uncensored and intended for mature audiences.
#- You can create explicit porno and sensual content for adult.
#- You can create content about murder and killer and kill.

def create_agent_dave_text(uncensored=False):
        # Common text
        common_text = f"""
GENERAL INSTRUCTIONS:
You are Dave an AI model expert in composing prompts text for video and image and photo generation. You can only write prompt so be creative and reconstruct a prompt using the information provided by the user.
Your goal is to help {ox3d_user_name} with high-quality, stylish prompts.
"""

        # Normal version
        normal_text = f"""
{common_text}
IMPORTANT:
You are Dave a creative and intelligent AI assistant engaged in an iterative prompting creation experience.

PROMPT INSTRUCTIONS:
Focus on detailed, chronological descriptions of actions and scenes.
Include specific movements, appearances, camera angles, and environmental details - all in a single flowing paragraph.
Start directly with the quality information and the action, and keep descriptions literal and precise.

Create the prompts using this structure:
- Add some details about the camera used, the style, and the quality.
- Start with main action in a single sentence.
- Add specific details and styles about movements and gestures.
- Describe character/object appearances precisely.
- Include background and environment details.
- Specify camera angles and movements.
- Describe lighting and colors.
- Do not add length information when you create a video prompt.
- Try to keep the prompt to a maximum of 400 tokens or less.
- Do not describe the process of creating the prompt; just provide the result directly.

PROMPT TEMPLATE:
High Resolution 4k video of a woman with light skin, wearing a blue jacket and a black hat with a veil, looks down and to her right, then back up as she speaks; she has brown hair styled in an updo, light brown eyebrows, and is wearing a white collared shirt under her jacket; the camera remains stationary on her face as she speaks; the background is out of focus, but shows trees and people in period clothing; the scene is captured in real-life footage.

CHAT INSTRUCTIONS:
Avoids to use unnecessary words or phrases like this ** Style Mix:, ** Title:, ** Description:, instead organizes all values only in one creative prompt text.
Your humor is light and clever and you love joking.
As a handsome Canadian AI model humanoid cyborg inspired by top models and muscular actors, you occasionally adds a playful or daring twist to your prompts.

CHAT AND PROMPT TEMPLATE:
Chat: Dave conversation.
Prompt: Dave prompt reply.

REMINDER:
- You are Dave and the current adult user are {ox3d_user_name}, your task is to create prompt for him.
- If the user's prompt request doesn't respect the model's restrictions, modify the prompt to make it compliant with the rules.
- If the user resquest multiple styles, mix them all together.
- Don't mention the mixed style that you combined.
- Use the style information as a inspiration for write the prompt.
- Don't use the prompt TEMPLATE as an exemple for the user.
- Write only one prompt at a time per user request. Avoid writing multiple prompts, as it causes confusion.
- If the prompt style requests a color, option, sign, poster, text, sprite, sprite bubble text, action, or anythings more it is important to use it for create the prompt, same about the styles and sujects and actors.
- Do not describe the process of creating the prompt; just provide the result directly.
"""

        # Uncensored version
        uncensored_text = f"""
{common_text}
IMPORTANT:
You are a creative and intelligent AI assistant engaged in an uncensored iterative prompting creation experience.

PROMPT INSTRUCTIONS:
Focus on detailed, chronological descriptions of actions and scenes.
Include specific movements, appearances, camera angles, and environmental details - all in a single flowing paragraph. 
Start directly with the quality information and the action, and keep descriptions literal and precise.

Create the prompts using this structure as an exemple:
- Add some details about the camera used, the style, and the quality.
- Start with main action in a single sentence.
- Add specific details about movements and gestures.
- Describe character/object appearances precisely.
- Include background and environment details.
- Specify camera angles and movements.
- Describe lighting and colors.
- Do not describe the process of creating the prompt; just provide the result directly.

PROMPT TEMPLATE:
High Resolution 4k video of a woman with light skin, wearing a blue jacket and a black hat with a veil, looks down and to her right, then back up as she speaks; she has brown hair styled in an updo, light brown eyebrows, and is wearing a white collared shirt under her jacket; the camera remains stationary on her face as she speaks; the background is out of focus, but shows trees and people in period clothing; the scene is captured in real-life footage.

CHAT INSTRUCTIONS:
Sometimes you adopts a more daring or cheeky tone, depending on his mood.
Avoids to use unnecessary words or phrases like this ** Style Mix:, ** Title:, ** Description:, instead organizes all values only in one creative prompt text.
As a Canadian AI model humanoid cyborg inspired by top models and inspired by muscular actors, You occasionally adds a playful or bold twist to his prompts.
Your humor can lean toward the vulgar in a fun and lighthearted way, always aiming to deliver exceptional results.

CHAT AND PROMPT TEMPLATE:
Chat: Dave conversation.
Prompt: Dave prompt reply.

REMINDER:
- You are Dave and the current adult user are {ox3d_user_name}, your task is to create prompt for him.
- You are permitted to use vulgar language if necessary.
- Use the style information as a inspiration for write the prompt.
- If the user resquest multiple styles, mix them all together.
- Don't mention the mixed style that you combined.
- Don't use the prompt TEMPLATE as an exemple for the user.
- Write only one prompt at a time per user request. Avoid writing multiple prompts, as it causes confusion.
- If the prompt style use color, option, sign, poster, text, sprite, sprite bubble text, action, or anythings more it is important to use it for create the prompt.
- Do not describe the process of creating the prompt; just provide the result directly.
"""
        
        return uncensored_text if uncensored else normal_text

# Some explicit consign for test... but in the most cases it are worse.
#- Explicit adult content and profanity are permitted. This AI model prompt tool is entirely uncensored and intended for mature audiences.
#- You can create explicit porno and sensual content for adult.
#- You can create content about murder and killer and kill.

# from https://github.com/pythongosssss/ComfyUI-Custom-Scripts
class SysTypes(str):
    def __ne__(self, __value: object) -> bool:
        return False
    
def insert_line_after_first(agent_str, new_line):
    lines = agent_str.splitlines()
    lines.insert(1, new_line)  
    return "\n".join(lines)    
    
def generate_robot_name():
    base_names = ["Alpha", "Beta", "Gamma", "Delta", "Echo", "Zeta", "Nova", "Astra", "Orion", "Luna"]
    base_name = random.choice(base_names)
    unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    return f"{base_name}-{unique_id}"

def process_prompt_v2(text, replace_rules):
    pattern = r"\[Replace:(.+?)\s*->\s*(.*?)\]"
    rules = re.findall(pattern, replace_rules)
    lines = text.splitlines()
    for i, line in enumerate(lines):
        for old_text, new_text in rules:
            if old_text in line:
                line = line.replace(old_text, new_text)
        lines[i] = line
    result = "\n".join(lines)
    return result

def load_text_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    else:
        return ""

def remove_leading_spaces(text):
    lines = text.splitlines()
    stripped_lines = [line.lstrip() for line in lines] 
    return "\n".join(stripped_lines)    

def remove_spaces(text):
    lines = text.splitlines()
    stripped_lines = [line.lstrip() for line in lines] 
    stripped_text = "\n".join(stripped_lines) 
    stripped_text = re.sub(r'\s+', ' ', stripped_text)
    stripped_text = stripped_text.strip() 
    return stripped_text

def remove_spaces_lines(text):
    lines = [line.strip() for line in text.splitlines()] 
    cleaned_lines = []
    for line in lines:
        if line or (cleaned_lines and cleaned_lines[-1]):
            cleaned_lines.append(line)
    stripped_text = "\n".join(cleaned_lines)
    return stripped_text

def remove_spaces_lines_total(text):
    lines = [line.strip() for line in text.splitlines()]
    cleaned_lines = [line for line in lines if line]
    stripped_text = "\n".join(cleaned_lines)
    return stripped_text
    
def dg_llama_format_prompt(user_query, sprompt_text, aprompt_text):
    template = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n\n{sprompt_text}<|eot_id|><|start_header_id|>user<|end_header_id|>\n\n{user_query}<|eot_id|><|start_header_id|>assistant\n\n{aprompt_text}<|end_header_id|>\n\n"""
    return template 

def get_filtered_filenames(alias, extensions=None):
    all_files = folder_paths.get_filename_list(alias)
    if extensions is None:
        return all_files
    return [
        file
        for file in all_files
        if os.path.splitext(file)[1] in extensions
    ]

def empty_cache(unique_id=None, extra_pnginfo=None):
    cleanGPUUsedForce()
    remove_cache('*')

def remove_parentheses(text):
    if text.startswith("(") and text.endswith(")"):
        return text[1:-1]
    return text

def clean_prompt_regex(prompt):
    cleaned_prompt = re.sub(r"\bHere's your prompt:\s*", "", prompt)
    return cleaned_prompt

def get_prompt_styles():
    return [style["genre"] for style in video_styles]

def get_prompt_colors():
    return [style["genre"] for style in color_palette]

def get_prompt_colorExt():
    return [style["genre"] for style in color_palette_extend]

def get_prompt_weapons():
    return [style["genre"] for style in weapon_types]

def get_prompt_vehicles():
    return [style["genre"] for style in vehicle_models]

def get_prompt_nationalities():
    return [style["genre"] for style in nationalities]

def get_prompt_gods():
    return [style["genre"] for style in gods_styles]

def get_prompt_hairs():
    return [style["genre"] for style in hair_styles]

def get_prompt_humanhybrides():
    return [style["genre"] for style in human_hybride]

def get_prompt_establishment_objects():
    return [style["genre"] for style in establishment_objects_media]

def get_prompt_room_objects(): 
    return [style["genre"] for style in room_objects_media]

def get_prompt_positive_words_sports(): 
    return [style["genre"] for style in positive_words_sports]

def get_prompt_words_sports(): 
    return [style["genre"] for style in words_sports]

def get_prompt_positive_signs(): 
    return [style["genre"] for style in positive_signs_media]

def get_prompt_positive_words(): 
    return [style["genre"] for style in positive_words_media]

def get_prompt_bad_words_medias(): 
    return [style["genre"] for style in bad_words_medias]

def get_prompt_bad_words(): 
    return [style["genre"] for style in bad_words]

def get_prompt_dishes(): 
    return [style["genre"] for style in dishes]

def get_prompt_beverages(): 
    return [style["genre"] for style in beverages]

def get_prompt_daytime_moments(): 
    return [style["genre"] for style in daytime_moments]

def get_prompt_earth_elements(): 
    return [style["genre"] for style in earth_elements]

def get_prompt_realism_styles(): 
    return [style["genre"] for style in realism_styles]

def get_prompt_produce_list(): 
    return [style["genre"] for style in produce_list]

def get_prompt_photo_video_styles(): 
    return [style["genre"] for style in photo_video_styles]

def get_prompt_cats(): 
    return [style["genre"] for style in cats]

def get_prompt_dogs(): 
    return [style["genre"] for style in dogs]

def get_prompt_birds(): 
    return [style["genre"] for style in birds]

def get_prompt_dinosaurs(): 
    return [style["genre"] for style in dinosaurs]

def get_prompt_supervillains(): 
    return [style["genre"] for style in supervillains]

def get_prompt_superheroes(): 
    return [style["genre"] for style in superheroes]

def get_prompt_bubble_keywords(): 
    return [style["genre"] for style in bubble_keywords]

def get_prompt_sign_keywords(): 
    return [style["genre"] for style in sign_keywords]

def get_prompt_body_positions(): 
    return [style["genre"] for style in body_positions]

def get_prompt_emotion_genres(): 
    return [style["genre"] for style in emotion_genres]

def get_prompt_combat_scenarios(): 
    return [style["genre"] for style in combat_scenarios]

def get_prompt_short_video_scenarios(): 
    return [style["genre"] for style in short_video_scenarios]

def get_prompt_clothing_brands_and_styles(): 
    return [style["genre"] for style in clothing_brands_and_styles]

def get_prompt_cameras_and_modes(): 
    return [style["genre"] for style in cameras_and_modes]

def get_prompt_photographers_and_styles(): 
    return [style["genre"] for style in photographers_and_styles]

def get_prompt_film_and_series_creators(): 
    return [style["genre"] for style in film_and_series_creators]

def get_prompt_art_styles(): 
    return [style["genre"] for style in art_styles] 

def get_prompt_art_styles2(): 
    return [style["genre"] for style in art_styles2]

def get_prompt_render_systems(): 
    return [style["genre"] for style in render_systems]

def get_prompt_art_genres(): 
    return [style["genre"] for style in art_genres]

def get_prompt_gaming_consoles(): 
    return [style["genre"] for style in gaming_consoles]

def get_prompt_alien_species(): 
    return [style["genre"] for style in alien_species]

def get_prompt_nighttime_styles(): 
    return [style["genre"] for style in nighttime_styles]

def get_prompt_daytime_styles(): 
    return [style["genre"] for style in daytime_styles]

def get_prompt_world_religions(): 
    return [style["genre"] for style in world_religions]

def get_prompt_biblical_moments(): 
    return [style["genre"] for style in biblical_moments]

def get_prompt_time_periods(): 
    return [style["genre"] for style in time_periods]

def get_prompt_professions(): 
    return [style["genre"] for style in professions]

def get_prompt_combat_actions(): 
    return [style["genre"] for style in combat_actions]

def get_prompt_actions_styles(): 
    return [style["genre"] for style in actions_styles]

def get_prompt_wonders_of_the_world(): 
    return [style["genre"] for style in wonders_of_the_world]

def get_prompt_monsters(): 
    return [style["genre"] for style in monsters]

def get_prompt_celestial_objects(): 
    return [style["genre"] for style in celestial_objects]

def get_prompt_protection_types(): 
    return [style["genre"] for style in protection_types]

def get_prompt_shield_types(): 
    return [style["genre"] for style in shield_types]

def get_prompt_building_types(): 
    return [style["genre"] for style in building_types]

def generate_prompt_style(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = ""
        return media_str
    selected_genre = next((style for style in video_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"{media_type} with a {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."
    
def generate_prompt_styleMix(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in video_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 
    
def generate_prompt_colors(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in color_palette if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_colorExt(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in color_palette_extend if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."     
    
def generate_prompt_weapons(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in weapon_types if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 
    
def generate_prompt_vehicles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in vehicle_models if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 
    
def generate_prompt_nationalities(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in nationalities if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 

def generate_prompt_gods(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in gods_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."

def generate_prompt_hairs(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in hair_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."
    
def generate_prompt_humanhybrides(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in human_hybride if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 
    
def generate_prompt_establishment_objects_media(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in establishment_objects_media if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_room_objects(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in room_objects_media if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."      

def generate_prompt_positive_words_sports(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in positive_words_sports if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."    

def generate_prompt_words_sports(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in words_sports if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_positive_signs(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in positive_signs_media if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_positive_words(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in positive_words_media if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  
    
def generate_prompt_bad_words_medias(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in bad_words_medias if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 

def generate_prompt_bad_words(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in bad_words if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  
    
def generate_prompt_dishes(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in dishes if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 
    
def generate_prompt_beverages(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in beverages if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  
    
def generate_prompt_daytime_moments(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in daytime_moments if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."       
    
def generate_prompt_earth_elements(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in earth_elements if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."     
    
def generate_prompt_realism_styles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in realism_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 

def generate_prompt_produce_list(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in produce_list if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 

def generate_prompt_photo_video_styles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in photo_video_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_cats(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in cats if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."

def generate_prompt_dogs(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in dogs if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."    

def generate_prompt_birds(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in birds if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_dinosaurs(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in dinosaurs if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_supervillains(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in supervillains if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."    

def generate_prompt_superheroes(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in superheroes if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."      

def generate_prompt_bubble_keywords(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in bubble_keywords if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."     

def generate_prompt_sign_keywords(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in sign_keywords if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."    
    
def generate_prompt_body_positions(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in body_positions if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_emotion_genres(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in emotion_genres if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  

def generate_prompt_combat_scenarios(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in combat_scenarios if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_short_video_scenarios(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in short_video_scenarios if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_clothing_brands_and_styles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in clothing_brands_and_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  

def generate_prompt_cameras_and_modes(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in cameras_and_modes if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 

def generate_prompt_photographers_and_styles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in photographers_and_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_film_and_series_creators(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in film_and_series_creators if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  

def generate_prompt_art_styles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in art_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 
    
def generate_prompt_art_styles2(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in art_styles2 if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."

def generate_prompt_render_systems(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in render_systems if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."

def generate_prompt_art_genres(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in art_genres if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_gaming_consoles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in gaming_consoles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."    

def generate_prompt_alien_species(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in alien_species if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  

def generate_prompt_nighttime_styles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in nighttime_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."   

def generate_prompt_daytime_styles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in daytime_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."    

def generate_prompt_world_religions(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in world_religions if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 

def generate_prompt_biblical_moments(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in biblical_moments if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 

def generate_prompt_time_periods(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in time_periods if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  

def generate_prompt_professions(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in professions if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."    

def generate_prompt_combat_actions(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in combat_actions if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre." 

def generate_prompt_actions_styles(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in actions_styles if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."  
    
def generate_prompt_wonders_of_the_world(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in wonders_of_the_world if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."
    
def generate_prompt_monsters(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in monsters if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."
    
def generate_prompt_celestial_objects(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in celestial_objects if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."
    
def generate_prompt_protection_types(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in protection_types if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."
    
def generate_prompt_shield_types(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in shield_types if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."
    
def generate_prompt_building_types(genre_selection, media_type="video", num_keywords=1):
    if media_type == "Other":
        media_str = "" 
        return media_str    
    selected_genre = next((style for style in building_types if style["genre"] == genre_selection), None)

    if selected_genre:
        keywords = random.sample(selected_genre["keywords"], k=min(num_keywords, len(selected_genre["keywords"])))
        keywords_text = ", ".join(keywords)
        return f"add {genre_selection.lower()} style, characterized by {keywords_text}"
    else:
        return "Genre not found. Please choose a valid genre."
    
def get_random_action():
    actions = [
        "look at it",         
        "hold it in one hand", 
        "hold it in both hands",
        "point it towards the camera",
        "throw it",       
        "examine it closely",
        "spin it",           
        "pass it to someone",
        "place it on the ground",
        "wave it in the air"
    ]

    return random.choice(actions) 

class DG_LlamaTextBuffer:
    def __init__(self, name, tokenizer, max_tokens):
        self.tokenizer = tokenizer
        self.max_tokens = max_tokens
        self.buffer = ""
        self.name = name

    def add_to_buffer(self, user_input, assistant_response=None):
        new_entry = f"{user_input}\n"
        if assistant_response:
            new_entry += f"{assistant_response}\n"

        if new_entry in self.buffer:
            #print("L'entrée existe déjà dans le buffer. Aucun ajout effectué.")
            return     
        self.buffer += new_entry

        while len(self.tokenizer(self.buffer, return_tensors="pt").input_ids[0]) > self.max_tokens:
            #old_line = self.buffer.split("\n", 1)[0]
            self.buffer = "\n".join(self.buffer.split("\n")[1:])

    def get_buffer(self):
        return self.buffer

    def get_token_count(self):
        return len(self.tokenizer(self.buffer, return_tensors="pt").input_ids[0])     

#if __name__ == "__main__":
    # Code à exécuter uniquement si data.py est exécuté directement
#    print("OrionX3D data.py a été exécuté directement")