from diffusers import StableDiffusionPipeline, DDPMScheduler
import torch
if True:    # Load the Stable Diffusion pipeline
    pipe = StableDiffusionPipeline.from_pretrained(
        "CompVis/stable-diffusion-v1-4",
        revision="fp16",
        torch_dtype=torch.float16
    )
    pipe.to("cuda")

    # Replace the scheduler
    pipe.scheduler = DDPMScheduler(beta_start=0.00085, beta_end=0.012, beta_schedule="scaled_linear")
    
def makeimage(prompt):
    try:
        image = pipe(prompt, num_inference_steps=30, guidance_scale=7.5).images[0]
        image.save("image.png")
    except:
        print("Error generating image")

if __name__ == "__main__":
    makeimage("A house")