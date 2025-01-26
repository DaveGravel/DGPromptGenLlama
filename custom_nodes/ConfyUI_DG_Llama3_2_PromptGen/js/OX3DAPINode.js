/*
@author: Dave Gravel
@title: ComfyUI OrionX3D Nodes
@web: https://www.youtube.com/@EvadLevarg/videos
@facebook: https://www.facebook.com/dave.gravel1
@nickname: k00m, Evados
@description: This extension is for experimental purposes only. Although I am a proficient Pascal and C++ programmer, I am relatively new to Python and may have made mistakes in the code.
@description: I have created these nodes primarily for my personal use. Some parts of the code are adapted from existing custom nodes, while others are original and designed entirely by me.
*/
/*
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
*/
import { app } from "/scripts/app.js";
import { ComfyWidgets } from "/scripts/widgets.js";

app.registerExtension({
  name: "Comfy.OX3DAPINode",
  async beforeRegisterNodeDef(nodeType, nodeData, app) { 
    const interfaceNodeNames = ["DGLlamaPromptViewer", "DGLlamaSysView"];

    if (interfaceNodeNames.includes(nodeData.name)) {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        const ret = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

        let nodeInstances = app.graph._nodes.filter((wi) => wi.type === nodeData.name),
          nodeName = `${nodeData.name}_${nodeInstances.length}`;

        console.log(`Create ${nodeData.name}: ${nodeName}`);

        const wi = ComfyWidgets.STRING(
          this,
          nodeName,
          [
            "STRING",
            {
              default: "",
              placeholder: "Prompt output...",
              multiline: true,
            },
          ],
          app
        );
        wi.widget.inputEl.readOnly = true;
        return ret;
      };

      const outSet = function (texts) {
        if (texts?.length > 0) {
          let widget_id = this?.widgets.findIndex((w) => w.type === "customtext");

          if (Array.isArray(texts))
            texts = texts
              .filter((word) => word.trim() !== "")
              .map((word) => word.trim())
              .join(" ");

          this.widgets[widget_id].value = texts;
          app.graph.setDirtyCanvas(true);
        }
      };

      const onExecuted = nodeType.prototype.onExecuted;
      nodeType.prototype.onExecuted = function (texts) {
        onExecuted?.apply(this, arguments);
        outSet.call(this, texts?.string);
      };

      const onConfigure = nodeType.prototype.onConfigure;
      nodeType.prototype.onConfigure = function (w) {
        onConfigure?.apply(this, arguments);
        if (w?.widgets_values?.length) {
          outSet.call(this, w.widgets_values);
        }
      };
    }

    if (nodeData.name === "DGLlamaMixStylesMulti") {
      const originalOnNodeCreated = nodeType.prototype.onNodeCreated || function () {};
      nodeType.prototype.onNodeCreated = function () {
        originalOnNodeCreated.apply(this, arguments);

        this._type = "STRING";
        this.inputs_offset = nodeData.name.includes("selective") ? 1 : 0;

        this.addWidget("button", "Update inputs", null, () => {
          if (!this.inputs) {
            this.inputs = [];
          }
          const target_number_of_inputs = this.widgets.find(w => w.name === "inputcount")?.value || 0;
          if (target_number_of_inputs === this.inputs.length) return;

          if (target_number_of_inputs < this.inputs.length) {
            for (let i = this.inputs.length; i >= this.inputs_offset + target_number_of_inputs; i--)
              this.removeInput(i);
          } else {
            for (let i = this.inputs.length + 1 - this.inputs_offset; i <= target_number_of_inputs; ++i)
              this.addInput(`style_${i}`, this._type);
          }
        });
      };
    }
	
	  if (nodeData.name === "DGLlamaChatUser") {	
      const onCreated = nodeType.prototype.onCreated;
        
      nodeType.prototype.onCreated = function() {
		    const node = this;
		
		    const ret = onCreated ? onCreated.apply(node, arguments) : undefined;
		  
	      const uWidget = node.widgets.find(w => w.name === "pause_generation");
		    if (uWidget) {
		      uWidget.value = true;
		      //node.setDirtyCanvas(true, true);
		    }

	      const uWidget2 = node.widgets.find(w => w.name === "llama3_reset");
		    if (uWidget2) {
          uWidget2.value = false;
		      //node.setDirtyCanvas(true, true);
		    }   
        
	      const uWidget3 = node.widgets.find(w => w.name === "llama3_agent_clear_history");
		    if (uWidget3) {
          uWidget3.value = false;
		      //node.setDirtyCanvas(true, true);
		    }         
		
		    return ret;
	    };
	  
	    const onExecuted = nodeType.prototype.onExecuted;
	  
      nodeType.prototype.onExecuted = function() {
		    const node = this;

        const ret = onExecuted ? onExecuted.apply(node, arguments) : undefined;

        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
	        uWidget.value = true;
		      //node.setDirtyCanvas(true, true);
		      //node.onResize?.(node.size);             
        }

	      const uWidget2 = node.widgets.find(w => w.name === "llama3_reset");
		    if (uWidget2) {
          uWidget2.value = false;
		      //node.setDirtyCanvas(true, true);
		    }      
        
	      const uWidget3 = node.widgets.find(w => w.name === "llama3_agent_clear_history");
		    if (uWidget3) {
          uWidget3.value = false;
		      //node.setDirtyCanvas(true, true);
		    }            

		    return ret;
      };

	    const onExecutionStart = nodeType.prototype.onExecutionStart;
	  
      nodeType.prototype.onExecutionStart = function() {
		    const node = this;

        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
	          uWidget.value = true;
		        //node.setDirtyCanvas(true, true);
		        //node.onResize?.(node.size);  
        }

        const uWidget2 = node.widgets.find(w => w.name === "llama3_reset");
		    if (uWidget2) {
          uWidget2.value = false;
		      //node.setDirtyCanvas(true, true);
		    } 
        
	      const uWidget3 = node.widgets.find(w => w.name === "llama3_agent_clear_history");
		    if (uWidget3) {
          uWidget3.value = false;
		      //node.setDirtyCanvas(true, true);
		    }            

        const ret = onExecutionStart ? onExecutionStart.apply(node, arguments) : undefined;

		    return ret;
      };

	    const onConfigure = nodeType.prototype.onConfigure;
 
      nodeType.prototype.onConfigure = function() {
		    const node = this;
		
		    const ret = onConfigure ? onConfigure.apply(node, arguments) : undefined;
			  
        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
		        uWidget.value = true;
		        //node.setDirtyCanvas(true, true);
        }

	      const uWidget2 = node.widgets.find(w => w.name === "llama3_reset");
		    if (uWidget2) {
          uWidget2.value = false;
		      //node.setDirtyCanvas(true, true);
		    }  
        
	      const uWidget3 = node.widgets.find(w => w.name === "llama3_agent_clear_history");
		    if (uWidget3) {
          uWidget3.value = false;
		      //node.setDirtyCanvas(true, true);
		    }            

		    return ret;
      };  
    }

	  if (nodeData.name === "DGLlamaAgentUserEdit") {	
      const onCreated = nodeType.prototype.onCreated;
        
      nodeType.prototype.onCreated = function() {
		    const node = this;
		
		    const ret = onCreated ? onCreated.apply(node, arguments) : undefined;
		  
	      const uWidget = node.widgets.find(w => w.name === "pause_generation");
		    if (uWidget) {
		      uWidget.value = true;
		      //node.setDirtyCanvas(true, true);
		    }   
        
	      const uWidget2 = node.widgets.find(w => w.name === "llama3_reset");
		    if (uWidget2) {
          uWidget2.value = false;
		      //node.setDirtyCanvas(true, true);
		    }  
        
	      const uWidget3 = node.widgets.find(w => w.name === "llama3_agent_clear_history");
		    if (uWidget3) {
          uWidget3.value = false;
		      //node.setDirtyCanvas(true, true);
		    }           
		
		    return ret;
	    };
	  
	    const onExecuted = nodeType.prototype.onExecuted;
	  
      nodeType.prototype.onExecuted = function() {
		    const node = this;

        const ret = onExecuted ? onExecuted.apply(node, arguments) : undefined;

        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
	        uWidget.value = true;
		      //node.setDirtyCanvas(true, true);
		      //node.onResize?.(node.size);             
        }    
        
	      const uWidget2 = node.widgets.find(w => w.name === "llama3_reset");
		    if (uWidget2) {
          uWidget2.value = false;
		      //node.setDirtyCanvas(true, true);
		    }  
        
	      const uWidget3 = node.widgets.find(w => w.name === "llama3_agent_clear_history");
		    if (uWidget3) {
          uWidget3.value = false;
		      //node.setDirtyCanvas(true, true);
		    }           

		    return ret;
      };

	    const onExecutionStart = nodeType.prototype.onExecutionStart;
	  
      nodeType.prototype.onExecutionStart = function() {
		    const node = this;

        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
	          uWidget.value = true;
		        //node.setDirtyCanvas(true, true);
		        //node.onResize?.(node.size);  
        }  
        
	      const uWidget2 = node.widgets.find(w => w.name === "llama3_reset");
		    if (uWidget2) {
          uWidget2.value = false;
		      //node.setDirtyCanvas(true, true);
		    }  
        
	      const uWidget3 = node.widgets.find(w => w.name === "llama3_agent_clear_history");
		    if (uWidget3) {
          uWidget3.value = false;
		      //node.setDirtyCanvas(true, true);
		    }           

        const ret = onExecutionStart ? onExecutionStart.apply(node, arguments) : undefined;

		    return ret;
      };

	    const onConfigure = nodeType.prototype.onConfigure;
 
      nodeType.prototype.onConfigure = function() {
		    const node = this;
		
		    const ret = onConfigure ? onConfigure.apply(node, arguments) : undefined;
			  
        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
		        uWidget.value = true;
		        //node.setDirtyCanvas(true, true);
        }    
        
	      const uWidget2 = node.widgets.find(w => w.name === "llama3_reset");
		    if (uWidget2) {
          uWidget2.value = false;
		      //node.setDirtyCanvas(true, true);
		    }  
        
	      const uWidget3 = node.widgets.find(w => w.name === "llama3_agent_clear_history");
		    if (uWidget3) {
          uWidget3.value = false;
		      //node.setDirtyCanvas(true, true);
		    }           

		    return ret;
      };  
    }

	  if (nodeData.name === "DGLlamaAgentTranslate") {	
      const onCreated = nodeType.prototype.onCreated;
        
      nodeType.prototype.onCreated = function() {
		    const node = this;
		
		    const ret = onCreated ? onCreated.apply(node, arguments) : undefined;
		  
	      const uWidget = node.widgets.find(w => w.name === "pause_generation");
		    if (uWidget) {
		      uWidget.value = true;
		      //node.setDirtyCanvas(true, true);
		    }            
		
		    return ret;
	    };
	  
	    const onExecuted = nodeType.prototype.onExecuted;
	  
      nodeType.prototype.onExecuted = function() {
		    const node = this;

        const ret = onExecuted ? onExecuted.apply(node, arguments) : undefined;

        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
	        uWidget.value = true;
		      //node.setDirtyCanvas(true, true);
		      //node.onResize?.(node.size);             
        }              

		    return ret;
      };

	    const onExecutionStart = nodeType.prototype.onExecutionStart;
	  
      nodeType.prototype.onExecutionStart = function() {
		    const node = this;

        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
	          uWidget.value = true;
		        //node.setDirtyCanvas(true, true);
		        //node.onResize?.(node.size);  
        }             

        const ret = onExecutionStart ? onExecutionStart.apply(node, arguments) : undefined;

		    return ret;
      };

	    const onConfigure = nodeType.prototype.onConfigure;
 
      nodeType.prototype.onConfigure = function() {
		    const node = this;
		
		    const ret = onConfigure ? onConfigure.apply(node, arguments) : undefined;
			  
        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
		        uWidget.value = true;
		        //node.setDirtyCanvas(true, true);
        }            

		    return ret;
      };  
    }

	  if (nodeData.name === "DGLlamaAgentCorrection") {	
      const onCreated = nodeType.prototype.onCreated;
        
      nodeType.prototype.onCreated = function() {
		    const node = this;
		
		    const ret = onCreated ? onCreated.apply(node, arguments) : undefined;
		  
	      const uWidget = node.widgets.find(w => w.name === "pause_generation");
		    if (uWidget) {
		      uWidget.value = true;
		      //node.setDirtyCanvas(true, true);
		    }            
		
		    return ret;
	    };
	  
	    const onExecuted = nodeType.prototype.onExecuted;
	  
      nodeType.prototype.onExecuted = function() {
		    const node = this;

        const ret = onExecuted ? onExecuted.apply(node, arguments) : undefined;

        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
	        uWidget.value = true;
		      //node.setDirtyCanvas(true, true);
		      //node.onResize?.(node.size);             
        }              

		    return ret;
      };

	    const onExecutionStart = nodeType.prototype.onExecutionStart;
	  
      nodeType.prototype.onExecutionStart = function() {
		    const node = this;

        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
	          uWidget.value = true;
		        //node.setDirtyCanvas(true, true);
		        //node.onResize?.(node.size);  
        }             

        const ret = onExecutionStart ? onExecutionStart.apply(node, arguments) : undefined;

		    return ret;
      };

	    const onConfigure = nodeType.prototype.onConfigure;
 
      nodeType.prototype.onConfigure = function() {
		    const node = this;
		
		    const ret = onConfigure ? onConfigure.apply(node, arguments) : undefined;
			  
        const uWidget = node.widgets.find(w => w.name === "pause_generation");         
        if (uWidget) {
		        uWidget.value = true;
		        //node.setDirtyCanvas(true, true);
        }            

		    return ret;
      };  
    }
  },
});

    //if (nodeData.name === "DGPromptGenLlama") {
    //  const originalOnNodeCreated = nodeType.prototype.onNodeCreated || function () {};
    //  nodeType.prototype.onNodeCreated = function () {
    //    originalOnNodeCreated.apply(this, arguments);
    //
    //    this.paused = false; // État de pause
    // 
    //    // Ajouter un bouton pour activer/désactiver la pause
    //    this.addWidget("button", "Pause/Resume", null, () => {
    //      this.paused = !this.paused; // Inverser l'état
    //      console.log(`Paused: ${this.paused}`);
    //    });
    //
    //    // Gestion des sorties
    //    const originalOnExecuted = this.onExecuted;
    //    this.onExecuted = function () {
    //      // Si en pause, mettre en attente
    //      if (this.paused) {
    //        console.log("Process paused. Waiting for user to resume...");
    //        return; // Empêche le traitement de continuer
    //      }
    //
    //      // Appeler le comportement original si non en pause
    //      originalOnExecuted?.apply(this, arguments);
    //    };
    //  };
    //}	