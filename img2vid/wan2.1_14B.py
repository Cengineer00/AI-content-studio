from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained("Wan-AI/Wan2.1-I2V-14B-720P")

prompt = "Astronaut in a jungle, cold color palette, muted colors, detailed, 8k"
image = pipe(prompt).images[0]