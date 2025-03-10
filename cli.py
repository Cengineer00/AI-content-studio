#!/usr/bin/env python3
import sys
from datetime import datetime
from content_creation_tools.tasks import (
    TextToImageTask,
    TextToVideoTask,
    ImageToVideoTask,
    # ImageUpscalingTask,
    # StableScrollTool,
    # StyleTransferTool
)

class ContentCreationCLI:
    def __init__(self):
        self.task_registry = {
            '1': {'name': 'Text-to-Image', 'handler': TextToImageTask(), 'needs_model': True},
            '2': {'name': 'Text-to-Video', 'handler': TextToVideoTask(), 'needs_model': True},
            '3': {'name': 'Image-to-Video', 'handler': ImageToVideoTask(), 'needs_model': True},
            # '4': {'name': 'Image-Upscaling', 'handler': ImageUpscalingTask(), 'needs_model': True},
            # '5': {'name': 'Stable-Scrolling', 'handler': StableScrollTool(), 'needs_model': False},
            # '6': {'name': 'Style-Transfer', 'handler': StyleTransferTool(), 'needs_model': False}
        }

    def clear_screen(self):
        print("\033[H\033[J", end="")  # ANSI escape codes for clearing screen

    def show_menu(self, title, options):
        self.clear_screen()
        print(f"╒{'═' * (len(title)+2)}╕")
        print(f"│ {title.upper()} │")
        print(f"╘{'═' * (len(title)+2)}╛")
        for key, value in options.items():
            print(f"  {key}. {value}")
        print("\n  Q. Quit")
        return input("\nSelect option: ").strip().lower()

    def get_parameters(self, handler):
        while True:
            params = {}
            print("\n│ Parameter Input │")
            print("├─────────────────┤")
            print("│ Format: key=value, comma separated")
            print("│ Commands: [h]help [q]quit [d]defaults")
            param_input = input("╞> ").strip().lower()

            if param_input == 'h':
                print(handler.get_parameter_help())
                continue
            if param_input == 'q':
                return None
            if param_input == 'd':
                return handler.validate_parameters({})

            for pair in param_input.split(','):
                pair = pair.strip()
                if not pair:
                    continue
                if '=' not in pair:
                    print(f"! Invalid format: {pair}")
                    params = None
                    break
                key, value = pair.split('=', 1)
                params[key.strip()] = value.strip()
            
            if not params:
                continue

            try:
                return handler.validate_parameters(params)
            except ValueError as e:
                print(f"! Validation Error:\n{e}")

    def handle_generation_flow(self, task):
        handler = task['handler']
        current_model = None

        while True:
            try:
                # Model selection for tasks requiring models
                if task['needs_model']:
                    models = handler.list_models()
                    model_choice = self.show_menu(
                        f"Choose Model for {task['name']}",
                        {str(i+1): name for i, name in enumerate(models)}
                    )
                    
                    if model_choice == 'q':
                        return
                    
                    current_model = handler.get_model(models[int(model_choice)-1])
                    if not current_model:
                        print("! Invalid model selection")
                        continue

                # Parameter handling
                params = self.get_parameters(current_model if task['needs_model'] else handler)
                if not params:
                    return

                # Input collection
                input_data = {}
                if task['name'] in ['Text-to-Image', 'Text-to-Video']:
                    input_data['prompt'] = input("\nEnter creative prompt: ")
                elif task['name'] in ['Image-Upscaling', 'Style-Transfer', 'Stable-Scrolling']:
                    input_data['input_path'] = input("Enter input file path: ")

                # Execution
                print("\n╭─ Generating...")
                result = handler.execute(
                    model=current_model,
                    params=params,
                    **input_data
                )
                print("╰─ Done!")
                
                # TODO: Result handling
                # timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                # output_path = f"output/{task['name']}_{timestamp}.{result['format']}"
                # result['output'].save(output_path)
                print(f"\n✓ Output saved to: {result}")

                # Continuation prompt
                cont = input("\nCreate another? (y/n): ").lower()
                if cont != 'y':
                    break

            except KeyboardInterrupt:
                print("\n! Operation cancelled")
                return
            except Exception as e:
                print(f"\n! Error: {str(e)}")
                if input("Retry? (y/n): ").lower() != 'y':
                    return

    def run(self):
        try:
            while True:
                task_choice = self.show_menu(
                    "Content Creation Suite",
                    {k: v['name'] for k, v in self.task_registry.items()}
                )

                if task_choice == 'q':
                    break

                task = self.task_registry.get(task_choice)
                if not task:
                    print("! Invalid selection")
                    continue

                self.handle_generation_flow(task)

        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            print("\nThank you for using the Content Creation Suite!")

if __name__ == "__main__":
    cli = ContentCreationCLI()
    sys.exit(cli.run())