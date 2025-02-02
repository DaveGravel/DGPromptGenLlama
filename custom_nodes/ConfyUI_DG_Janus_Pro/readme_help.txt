INSTALL:
Change the folder name E:\New_comfy_ui\ by your comfyUI installation folder...

E:\New_comfy_ui\python_embeded\python.exe -m pip install -r E:\New_comfy_ui\ComfyUI\custom_nodes\ConfyUI_DG_Janus_Pro\requirements-windows.txt

Download models:
git clone ComfyUI\custom_nodes\ConfyUI_DG_Janus_Pro\Models>git clone https://huggingface.co/deepseek-ai/Janus-Pro-1B

git clone ComfyUI\custom_nodes\ConfyUI_DG_Janus_Pro\Models>git clone https://huggingface.co/deepseek-ai/Janus-Pro-7B

The model Janus 1.3b doesn't seem to be working for now. The Safetensors file appears to require flash_attn2, which, if I'm not mistaken, is only compatible with Linux. Windows might need a prebuilt library, but I'm not sure if version 2 is built for Windows.

The JanusFlow model also doesn't seem to be working at the moment. The Safetensors file appears to require flash_attn2, which, if I'm not wrong, is only compatible with Linux. Windows might need a prebuilt library, but I'm not sure if version 2 is available for Windows.

I've written the code to load the GGUF file, but it doesn't seem to work.
I think llama.cpp currently supports GGUF, but AutoModelForCausalLM might need an update to get it working properly.
I'm not 100% sure about this, but I can try searching for a fix in another way.
