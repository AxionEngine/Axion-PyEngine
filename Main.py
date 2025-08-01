import json
import importlib.util
import sys
import os

def load_component(component_path):
    """Dynamically load a component from a Python file"""
    module_name = os.path.basename(component_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, component_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    # Load configuration
    try:
        with open('load.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: load.json not found!")
        sys.exit(1)
    
    # Determine which component to load
    component_to_load = config['default_mode']
    
    # Try to load the requested component
    try:
        if component_to_load == "project_manager":
            pm = load_component('components/manager/project_manager.py')
            pm.run()
        elif component_to_load == "engine":
            engine = load_component('components/core/engine/engine.py')
            engine.run()
        else:
            raise ValueError(f"Unknown component: {component_to_load}")
    except Exception as e:
        print(f"Failed to load {component_to_load}: {str(e)}")
        print(f"Falling back to {config['fallback_mode']}")
        
        # Fallback to engine mode
        try:
            engine = load_component('components/core/engine/engine.py')
            engine.run()
        except Exception as fallback_error:
            print(f"Critical failure: {str(fallback_error)}")
            sys.exit(1)

if __name__ == "__main__":
    main()
