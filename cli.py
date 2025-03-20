#!/usr/bin/env python3
import sys
from datetime import datetime
from content_creation_tools.tasks import (
    TextToImageTask,
    TextToVideoTask,
    ImageToVideoTask,
    TypeFlowTask,
    StableScrollTask,
    TranscriberTask,
    # ImageUpscalingTask,
    # StableScrollTool,
    # StyleTransferTool
)

class ContentCreationCLI:
    def __init__(self):
        # TODO: Define name in task classes
        self.tasks = [
            TextToImageTask(),
            TextToVideoTask(),
            ImageToVideoTask(),
            TypeFlowTask(),
            StableScrollTask(),
            TranscriberTask(),
        ]

    def show_menu(self, title, options):
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
            print("│ Commands: [h]help [q]quit [enter]defaults")
            param_input = input("╞> ").strip().lower()

            if param_input == 'h':
                print(handler.get_parameter_help())
                continue
            if param_input == 'q':
                return None
            if param_input == '':
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

    def handle_generation_flow(self, handler):
        current_model = None

        while True:
            try:
                # Check if list_models method exists
                if callable(getattr(handler, "list_models", None)):
                    # Model selection for tasks requiring models
                    models = handler.list_models()
                    model_choice = self.show_menu(
                        f"Choose Model for {handler}",
                        {str(i+1): name for i, name in enumerate(models)}
                    )
                    
                    if model_choice == 'q':
                        return
                    
                    try:
                        current_model = models[int(model_choice)-1]
                    except:
                        print("! Invalid model selection")
                        continue
                else:
                    current_model = handler.get_model()

                # Parameter handling
                params = self.get_parameters(current_model)
                if not params:
                    return

                # Input collection
                input_data = current_model.get_input()

                # Execution
                print("\n╭─ Generating...")
                result = handler.execute(
                    model=current_model, 
                    params=params, 
                    input_data=input_data
                )
                print("╰─ Done!")
                
                # TODO: Result handling
                timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
                handler.handle_result(result, timestamp)

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
                    "AI Content Studio",
                    {str(i+1): name for i, name in enumerate(self.tasks)}
                )

                if task_choice == 'q':
                    break

                try:
                    task = self.tasks[int(task_choice)-1]
                except:
                    print("! Invalid selection")
                    continue

                self.handle_generation_flow(task)

        except KeyboardInterrupt:
            print("\nExiting...")
        finally:
            print("\nThank you for using the AI Content Studio!")

if __name__ == "__main__":
    cli = ContentCreationCLI()
    sys.exit(cli.run())