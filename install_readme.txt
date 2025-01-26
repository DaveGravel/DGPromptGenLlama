Updated Workflow V4 Release
I'm excited to share the updated version of my workflow (V4)!
It using my llama prompt gen node + my sampler refiner.

Key Features:
Custom Prompt Support: This version allows sequences to use custom prompts.
Quick Upscale Video: Added functionality for quick video upscaling.
FaceSwap Fixes: Resolved several issues with nodes in FaceSwap mode.

Key Features about LTX video workflow:
Custom Prompt Support: This version allows sequences to use custom prompts.
Quick Upscale Video: Added functionality for quick video upscaling.
FaceSwap Fixes: Resolved several issues with nodes in FaceSwap mode.

Llama prompt gen workflow + my sampler refiner.

Installation Instructions:

Custom Nodes Installation:

Updating the old version:
Copy the custom_nodes folder into ComfyUI/custom_nodes.
Restart ComfyUI and load the updated V4 workflow.

Installing LLama prompt gen and my samplers Node:

Open a terminal or command prompt and execute the following:
Don't forget to update the folder paths to match your ComfyUI installation.

E:\New_comfy_ui\python_embeded\python.exe -m pip install -r E:\New_comfy_ui\ComfyUI\custom_nodes\ConfyUI_DG_Llama3_2_PromptGen\requirements-windows.txt

Restart ComfyUI.
Look in the node folder to find a quick workflow test.

Downloading LLama Model

Navigate to the Models folder inside custom_nodes/ConfyUI_DG_Llama3_2_PromptGen directory.

Open a command prompt from this folder and run:
git clone https://huggingface.co/chuanli11/Llama-3.2-3B-Instruct-uncensored

or for the original model

git clone https://huggingface.co/meta-llama/Llama-3.2-3B

It is supposed to look like this:
custom_nodes/ConfyUI_DG_Llama3_2_PromptGen/Models/Llama-3.2-3B-Instruct-uncensored
custom_nodes/ConfyUI_DG_Llama3_2_PromptGen/Models/Llama-3.2-3B

For GGUF Models

Create a folder inside the Models directory.
Manually download the GGUF files and place them in this folder.

The node is also compatible with Llama 3.1 8B. If you have enough memory, it is an excellent version of the model. However, the 3.2 1B version is not very good for prompts or translations, so I don't really recommend it. It is a small model designed more for mobile phones. On the other hand, the Llama 3.2 3B version is one of the best for its size. It offers the advantage of not using up all your memory while still delivering very good results despite its smaller size.

My custom Llama node can load both the original models and GGUF models. However, on my PC configuration, the original or fine-tuned versions work better than the GGUF version. In 4-bit, the original models seem to be much faster than GGUF. The GGUF version appears to use and require more memory for decompression. It's up to you to decide which one you prefer, but in my case, the original 4-bit models provide excellent performance and results.