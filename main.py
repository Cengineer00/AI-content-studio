import os
import sys
from datetime import datetime

class ContentGenerator:
    def __init__(self):
        self.task_map = {
            '1': 'Text-to-Image',
            '2': 'Text-to-Video',
            '3': 'Image-to-Video',
            '4': 'Image-Upscaling',
            '5': 'Stable-Scrolling'
        }
        
        self.models = {
            'Text-to-Image': {'1': 'StableDiffusion v1', '2': 'OpenJourney'},
            'Text-to-Video': {'1': 'ModelScope', '2': 'CogVideo'},
            'Image-to-Video': {'1': 'Img2Vid-XL'},
            'Image-Upscaling': {'1': 'SwinIR', '2': 'ESRGAN'},
            'Stable-Scrolling': {'1': 'Scrolly-v1'}
        }

    def show_menu(self, options, title):
        print(f"\n{title}:")
        for key, value in options.items():
            print(f"{key}. {value}")
        return input("Enter your choice: ")

    def get_parameters(self):
        params = {}
        print("\nEnter parameters (format: key=value, separated by commas)")
        print("Example: steps=50, guidance=7.5, width=1024")
        param_input = input("Parameters: ").split(',')
        
        for p in param_input:
            if '=' in p:
                key, value = p.strip().split('=')
                params[key.strip()] = value.strip()
        return params

    def text_to_image(self, model, prompt, params):
        # Implementation example using diffusers
        from diffusers import StableDiffusionPipeline
        import torch

        pipe = StableDiffusionPipeline.from_pretrained(model)
        image = pipe(prompt, **params).images[0]
        
        filename = f"output_{datetime.now().strftime('%Y%m%d%H%M%S')}.png"
        image.save(filename)
        return filename

    def handle_task(self, task, model, params):
        # Add your actual model implementations here
        print(f"\nGenerating {task} with {model}...")
        
        prompt = input("Enter your prompt: ")
        
        if task == 'Text-to-Image':
            result_path = self.text_to_image(model, prompt, params)
        elif task == 'Text-to-Video':
            result_path = "video_output.mp4"  # Implement similarly
        elif task == 'Image-to-Video':
            result_path = "video_output.mp4"   # Implement similarly
        elif task == 'Image-Upscaling':
            result_path = "upscaled_image.png" # Implement using torchvision/ESRGAN
        elif task == 'Stable-Scrolling':
            result_path = "scrolling_video.mp4"
        
        return result_path

    def run(self):
        while True:
            # Task selection
            task_choice = self.show_menu(self.task_map, "Available Tasks")
            task = self.task_map.get(task_choice)
            
            if not task:
                print("Invalid choice!")
                continue

            # Model selection
            model_choice = self.show_menu(self.models[task], f"Available Models for {task}")
            model = self.models[task].get(model_choice)
            
            if not model:
                print("Invalid model choice!")
                continue

            # Parameter input
            params = self.get_parameters()

            # Main generation loop
            while True:
                try:
                    result_path = self.handle_task(task, model, params)
                    print(f"\nGeneration complete! Result saved to: {result_path}")
                    
                    cont = input("Create another with same settings? (y/n): ").lower()
                    if cont != 'y':
                        break
                        
                except KeyboardInterrupt:
                    print("\nOperation cancelled!")
                    break
                except Exception as e:
                    print(f"Error: {str(e)}")
                    break

if __name__ == "__main__":
    generator = ContentGenerator()
    try:
        generator.run()
    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)