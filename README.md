# DGPromptGenLlama
Hello, I’m Dave Gravel. By trade, I’m a C++ programmer specializing in 3D and Physics, along with anything related to this field. I have a basic understanding of almost all programming languages, but the two I’ve used the most and in which I excel are Pascal and C++. I’m familiar with the logic of most other languages, though I haven’t worked with them extensively. As a result, my code may include some repetitive logic and certain methods that could be better implemented, but overall, everything should still work pretty well, hehe.

A year ago, or maybe a little more, I had created a Llama 3.1 node. However, since it was difficult to get it working due to the size of the Llama 3.1 8B model and because some tools for loading the Llama model at the time conflicted with other tools in ComfyUI, I decided not to make it public.

When Llama 3.2 was released, I tested the tools again, and the conflicts seem to be resolved now, and Llama works very well. So, I decided to update my node, DGPromptGenLlama, and while building it, I realized that some cool options could be added, like styles and a few other features I’ll discuss below.

Since everything seems to be working well for me now, I decided to share it with the public. This way, it might be useful for others as well. It’s a great tool if you’re running out of ideas for writing your prompts.

With this, you’ll be able to create amazing images and videos. Or you can simply use Llama like ChatGPT, as it’s possible to configure and create your own agents for anything, not just for prompts.

![Screenshot 2025-01-20 205531x](https://github.com/user-attachments/assets/788dc40e-0bc0-45ae-a8d6-d5e5432d2aee)

- input seeder: Llama doesn’t use the standard seed method; instead, it uses the samples method. I’ve tried to implement a basic seeder to make it work similarly to the ComfyUI seed system.
 
- input mix_styles: With this pin, we can connect styles, and these styles will be added to your Llama prompt request.
  
- input agent: With this node, there are two possible methods for the agent: either you connect a text window with the agent instructions, or you use the node's internal agent. This internal agent does not have memory, ensuring that it behaves completely randomly. For agents with memory, you need to use the DGLlamaChatUser node.
  
- input external_suject: This pin is used to connect external text to add to your Llama prompt request. For example, I sometimes use it with Florence2: I provide an image to Florence, and it generates a prompt from the image, which I then pass to Llama to create a new prompt based on my instructions or the added styles.
  
- input assistant: This pin is used to provide text to the assistant, but for random prompt generation, it’s not a particularly useful option. I included it anyway in case someone absolutely wants to send a message to the assistant, but I recommend not using it if it’s solely for prompts.
  
- input remove_from_prompt: This pin is used to connect a text window where you can write the words or phrases you want to remove or modify.
Sometimes Llama can go its own way and use or repeat words you don’t want. This option allows you to remove them. For example: [Replace:Create a -> A]. With this command, "Create a" will be replaced with "A."

- model_file: This variable is used to load the Llama model. It displays the names of the models you’ve downloaded into the Models folder of my custom_node.
  
- styles_variation: This variable is used when you are applying styles. For example, if you use a nationality style and want to force Llama to add more details about the style, you can increase the variation. This will cause more words related to the chosen style to be added. Generally, a variation of 1 or 2 is sufficient, but it’s possible to go up to 10 for most styles.
  
- prompt_styles: This variable is used to add styles to your prompt. For example, if you make a request to Llama with "a woman" or "a dog," you can activate the styles and add the styles you want. Llama will then mix your request with the provided styles.
  
- reset_model:
- use_bit_mode:
- prompt_mode:
- only_english:
- use_seeder:
- use_mix_styles:
- use_custom_prompt:
- use_external_suject:
- max_token:
- top_p:
- top_k:
- temperature:
- repetition_penality:
- clear_extra_mem_gpu:
- suject:
- custom_prompt:
- use_uncensored_agent:
- use_internal_agent:
- use_internal_remove:
- use_assistant:
- disable_generation:
- output prompt:
- output llama3_pipe:
- output mix_styles:

![Screenshot 2025-01-20 210404x](https://github.com/user-attachments/assets/6f1c62ce-989d-4f86-9379-e77b5842a5de)

![Screenshot 2025-01-20 211902](https://github.com/user-attachments/assets/a5a9aaff-1797-4846-9f1d-c87e8b01f51f)

![Screenshot 2025-01-20 210612x](https://github.com/user-attachments/assets/a971e8a5-3828-4c50-afcb-35016ed1321b)

![Screenshot 2025-01-20 210750](https://github.com/user-attachments/assets/98068944-a287-491b-bbd1-618d9cade7a2)

![Screenshot 2025-01-20 210919](https://github.com/user-attachments/assets/9baf023b-29d6-4ab8-be89-463c7a667875)

![Screenshot 2025-01-20 211347](https://github.com/user-attachments/assets/6be249e1-a96d-40a6-b88e-b6c8afffd82e)

![Screenshot 2025-01-20 211153](https://github.com/user-attachments/assets/3b2b13ea-387d-4396-9bbd-9786af143da9)

![Screenshot 2025-01-20 211635](https://github.com/user-attachments/assets/0a53ab11-a553-412e-a3b7-55037bab1374)
