# INFORMATION UPDATED:
Updated Workflow V5 Release

What's New:

I have made a lot of fixes and changes.
I have added DeepSeek R1 support.
I have created a Llama model loader and a DeepSeek model loader.
I have fixed some issues when using GGUF models; it should now work better.
I have added more individual options for better configuration of all nodes.

OLD Video:
https://www.youtube.com/watch?v=Pdb8dWybHy8

I will soon upload a YouTube video to demonstrate how it works and how I use my Llama prompt, sampler, refiner, and upscaler.

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
  
- input external_subject: This pin is used to connect external text to add to your Llama prompt request. For example, I sometimes use it with Florence2: I provide an image to Florence, and it generates a prompt from the image, which I then pass to Llama to create a new prompt based on my instructions or the added styles.
  
- input assistant: This pin is used to provide text to the assistant, but for random prompt generation, it’s not a particularly useful option. I included it anyway in case someone absolutely wants to send a message to the assistant, but I recommend not using it if it’s solely for prompts.
  
- input remove_from_prompt: This pin is used to connect a text window where you can write the words or phrases you want to remove or modify.
Sometimes Llama can go its own way and use or repeat words you don’t want. This option allows you to remove them. For example: [Replace:Create a -> A]. With this command, "Create a" will be replaced with "A."

- model_file: This variable is used to load the Llama model. It displays the names of the models you’ve downloaded into the Models folder of my custom_node.
  
- styles_variation: This variable is used when you are applying styles. For example, if you use a nationality style and want to force Llama to add more details about the style, you can increase the variation. This will cause more words related to the chosen style to be added. Generally, a variation of 1 or 2 is sufficient, but it’s possible to go up to 10 for most styles.
  
- prompt_styles: This variable is used to add styles to your prompt. For example, if you make a request to Llama with "a woman" or "a dog," you can activate the styles and add the styles you want. Llama will then mix your request with the provided styles.
  
- reset_model: This option is for resetting the Llama model in case there’s an issue. It’s very, very rare to need this option, but it’s available just in case.
  
- use_bit_mode: Okay, this option is an important one in my opinion. It’s the compression model used for the Llama model. With my node, it’s possible to load both GGUF models and the original SafeTensors models. Personally, I use the 4-bit mode with the original models.
In general, GGUF models are very good and help a lot with memory usage, but for my part, with Llama, the original models in 4-bit mode work much better than GGUF. They seem to cause fewer memory issues and appear to be faster as well. It’s up to you to decide which works better in your configuration, whether it’s GGUF or the original models.

- prompt_mode: This changes the mode of the prompt, whether it’s for images, videos, or other types of requests.
  
- only_english: This option forces Llama to operate only in English. However, to be honest, sometimes Llama can do its own thing, so it might not always follow this instruction. But in general, it works.
This issue is especially noticeable if you try using the nodes with Llama 3.2 1B. I don’t recommend the 1B model because it’s smaller, generates many more errors, and doesn’t understand everything very well. In my opinion, the best models are the 3.1 8B and 3.2 3B or larger.

- use_seeder: This option is used to activate Llama’s samples mode and enable my seeder implementation to provide a simple seed, similar to how it's done in ComfyUI.
  
- use_mix_styles: This option activates or deactivates all styles connected or selected in the node. It also disables the mix_styles output.
 
- use_custom_prompt: In the node, there is a text box named custom_prompt. This option is used to activate the use of a custom prompt. Llama will not modify this prompt. It’s the same as writing a prompt yourself in standard ComfyUI. Llama will never alter this prompt, and styles will not be applied, nor will the external subject be applied to this custom prompt.
It’s a way to bypass Llama and test a custom prompt.

- use_external_subject: This activates the external subject if the use_external_subject option is enabled.
 
- max_token: This option is for setting the maximum tokens to use in Llama. Currently, it is locked to 4096 because with all options active, it can require a large token buffer. I’ll see if I can implement a better solution later. Currently, it’s not really causing issues with the 3B model or larger, but it might cause problems with the 1B model. Personally, I don’t recommend using the 1B model with this node. It’s supposed to work, but the 1B model often gives poor results and doesn’t understand the instructions very well.
  
- top_p: Adjusts the creativity of the AI's responses by controlling how many possible words it considers. Lower values make outputs more predictable; higher values allow for more varied and creative responses.
 
- top_k: Limits the AI to choose from the top 'k' most probable words. Lower values make responses more focused; higher values introduce more variety and potential surprises.
  
- temperature: Controls the randomness of the output; higher values produce more random results.
  
- repetition_penality: Penalty for repeated tokens; higher values discourage repetition.
  
- clear_extra_mem_gpu: This option attempts to free up some GPU memory at the end of using the Llama model. It can help for systems with limited VRAM.
  
- subject: This option text box is where you make a prompt request to Llama. Normally, you use a simple prompt, such as "a woman at the beach," and then apply styles to enhance it. Alternatively, instead of using styles, you can write your own request.
But keep in mind, the main node is random and has no memory. So, if you make a prompt request, it won’t remember your previous prompt in the next request. If you want to interact with Llama and have it remember your previous questions and prompts, you must use the DGLlamaChatUser node. Afterward, you can copy the result into the custom_prompt of the main node to generate the image.

- custom_prompt: This is the text box for writing a custom prompt without using Llama. It can be very useful for prompts that you modify yourself, or if there's an issue with the DGLlamaChatUser node, or simply for testing a simple prompt. When you use custom_prompt, the styles are also disabled, as well as the external_subject.
  
- use_uncensored_agent: This option is for enabling the uncensored mode of the Llama model. It doesn’t work with the original models; you need to use finetuned uncensored models. However, even with those, some uncensored models might not be 100% uncensored, so it’s possible the model may refuse to use this option.
That said, there are models that are nearly 100% uncensored, and with those, it works well. Otherwise, the original Llama model can also do things that are usually censored, depending on how you ask. Often, the regular model can seem more uncensored than the finetuned uncensored models, hehe. The best approach is to try it with or without and see if there’s a difference, and what the model is willing or not willing to do.

- use_internal_agent: This uses the internal agent that I implemented. This agent is not modifiable unless you modify it directly in the code. It’s the default agent for the DGPromptGenLlama node, and it’s typically very good for generating random prompts mixed with styles, which can be quite surprising.
If this option is turned off, you need to connect a text box to the agent pin to use your own instructions for the agent.
  
- use_internal_remove: This activates or disables the remove_from_prompt option if you're using it to remove text from the generated prompt in Llama.
  
- use_assistant: This is used to activate or deactivate the assistant. Normally, this option is never needed for prompt generation in this node, as the agent is configured in such a way that it doesn’t require the assistant.
  
- disable_generation: This disables the Llama generation for this node. It’s not really needed, but just in case, I’ve added the possibility.
  
- output prompt: This is the output prompt generated by Llama or the output from your custom_prompt.
  
- output llama3_pipe: This is the Llama pipe used to share the Llama model with my other nodes.
  
- output mix_styles: These are the styles used in this node, and it has an output in case you want to use the same styles in other nodes. It returns an empty value when the styles are disabled in the node.

# OX3DKSamplerAdvLTX
This node has no direct connection with the Llama nodes. It comes from another one of my projects, but it’s very useful with Llama. Essentially, it’s a multi-pass sampler. It performs a simple pass followed by a second pass to refine the result, with or without upscaling. I won’t explain all the details here, but if you watch my video for the Llama node, I use it in the video, so you can see how it works and what it’s useful for.
This node originates from a node sampler project I made for the Video LTX model, but it works with all image models compatible with ComfyUI samplers.

![Screenshot 2025-01-20 210404x](https://github.com/user-attachments/assets/6f1c62ce-989d-4f86-9379-e77b5842a5de)

# OX3DKSamplerLTX
Again, this node has no relation with the Llama node, but it can be useful with the Video LTX model. My Llama node is also well-suited for use with the LTX model.

![Screenshot 2025-01-20 211902](https://github.com/user-attachments/assets/a5a9aaff-1797-4846-9f1d-c87e8b01f51f)

# DGLlamaChatUser
This node is one of my favorites; it’s the one I have the most fun with.
In this node, I’ve implemented an agent system, and this agent has a memory buffer, so it remembers the conversation or prompts. The memory isn’t very large, but it’s enough to make the experience more enjoyable and even fun at times. Personally, I often use this node to create my prompts, and then I use them in the custom_prompt text box of my main node. Sometimes, I pass the full prompt back to Llama to let it modify it.

- prompt_mode: This is used to choose whether the prompt is for an image, a video, or "Other." When the option is set to "Other," it doesn’t use anything specific. If you want to specify the type of prompt or something else yourself, select "Other."

- llama3_reset: This resets the Llama agent completely and clears its memory. You should use this option when you change the type of agent.
As of now, when you reset the agent, it clears the memory. However, when the project is released, I may change the functionality so that it doesn’t erase the memory, since there is already another option to simply clear the memory.

- llama3_agent_type: This option is for selecting your agent. You can create your agents using the DGLlamaAgentUserEdit node, or manually create the agent as an .agt file within the folder of my custom node. The .agt is just a format I’ve given, but it’s still a simple text file.
  
- llama3_agent_clear: This clears the chat memory with the Llama agent. It can be useful if Llama is relying too much on the history or if it refuses to do something. You may need to clear the memory if you want to try again, as sometimes it will say no, but in another generation, it might say yes.
Occasionally, the model might view the prompt as violent or explicit and refuse to carry out the prompt for your request. Clearing the memory can help in this case. Also, sometimes the normal mode is more open than the uncensored mode. This is because, in the uncensored configuration, if you use certain words, the model might set a flag and refuse to process anything related to those words.
  
- use_external_subject: Same as with other nodes.
  
- use_mix_styles: Same as with other nodes.

![Screenshot 2025-01-20 210612x](https://github.com/user-attachments/assets/a971e8a5-3828-4c50-afcb-35016ed1321b)

# DGLlamaAgentUserEdit
This node is very similar to the DGLlamaChatUser node, but it’s not implemented in exactly the same way. It’s functional, but still under construction. This node is primarily used for creating agents and saving their configurations, and it’s possible to load the saved agent into the DGLlamaChatUser node.
It’s also possible to use this node as a simple prompt generator, but I recommend using DGLlamaChatUser if you only need to generate prompts. It may also change if I have time to update my project.

![Screenshot 2025-01-20 210750](https://github.com/user-attachments/assets/98068944-a287-491b-bbd1-618d9cade7a2)

# DGLlamaStyles
This is a large list of styles to use with my Llama nodes. It adds a bit more "ingredients" to the big soup that Llama will prepare for us as a prompt, hehe.

![Screenshot 2025-01-20 210919](https://github.com/user-attachments/assets/9baf023b-29d6-4ab8-be89-463c7a667875)

# Multiple node styles
The DGLlamaStyles node contains all the styles in one large list, and it’s quite extensive. I’ve separated some styles to make them easier to use, but there are many more style nodes than what this screenshot shows. The style nodes work exactly the same way as the main DGLlamaStyles node.
There’s also a DGLlamaMixStylesMulti node, which allows you to connect several style nodes that combine into one large final style.

![Screenshot 2025-01-20 211347](https://github.com/user-attachments/assets/6be249e1-a96d-40a6-b88e-b6c8afffd82e)

# DGLlamaAgentTranslate
This is a special node with a simple internal agent for translating prompts or other text. The agent is not modifiable, unless you change it directly in the code. It’s just a very simple tool to assist with translations.

![Screenshot 2025-01-20 211153](https://github.com/user-attachments/assets/3b2b13ea-387d-4396-9bbd-9786af143da9)

# DGLlamaAgentCorrection
This node is similar to the translate node. It’s a quick and simple agent for applying corrections or modifications to your prompt. Again, in this node, the agent is not modifiable. While it’s possible to do translations or corrections with the DGLlamaChatUser node, both of these nodes work well for me. Sometimes, the model performs better in certain situations without the memory buffer. Both of these nodes do not have memory.

![Screenshot 2025-01-20 211635](https://github.com/user-attachments/assets/0a53ab11-a553-412e-a3b7-55037bab1374)
