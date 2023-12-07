import copy 

def format_parameter(param_name, param_details, required_params, indent=6, type_hints=True):
    """Format a single parameter, handling nested objects if necessary."""
    param_type = param_details.get("type", "unknown")
    param_desc = param_details.get("description", "")
    is_required = "required" if param_name in required_params else "optional"
    type_info = ""
    if type_hints:
        type_info = f"[{param_type}, {is_required}] "
    output = f"{' ' * indent}{param_name}: {type_info}{param_desc}\n"

    # Handle nested object parameters
    if param_type == "object" and "properties" in param_details:
        nested_properties = param_details["properties"]
        nested_required = set(param_details.get("required", []))
        for nested_name, nested_details in nested_properties.items():
            output += format_parameter(nested_name, nested_details, nested_required, indent + 2, type_hints)

    return output

def format_functions(functions, type_hints=True):
    output = "Available functions:\n"
    for func in functions:
        # Extract function details
        name = func["name"]
        description = func.get("description", "")
        parameters = func.get("parameters", {}).get("properties", {})
        required_params = set(func.get("parameters", {}).get("required", []))

        # Format function details
        output += f"- {name}:\n    description: {description}\n    parameters:\n"
        for param_name, param_details in parameters.items():
            output += format_parameter(param_name, param_details, required_params, type_hints=type_hints)

    return output

class JdFunctionInjector:
    DEFAULT_PREFIX = "As an artificial intelligence assistant, choose the appropriate function and its parameters from the provided list according to the user input. Please provide your answer in JSON format."
    
    def __init__(self, prefix=DEFAULT_PREFIX, type_hints=True) -> None:
        self.prefix = prefix
        self.type_hints = type_hints

    def __call__(self, messages, functions):
        # Clone the messages list to avoid modifying the original list
        updated_messages = copy.deepcopy(messages)

        # Check if there are any messages in the list
        if updated_messages and updated_messages[-1]['role'] == 'user':
            formatted_functions = format_functions(functions, self.type_hints)
    
            # Append the new message to the content of the last message
            last_message_content = updated_messages[-1]["content"]
            updated_last_message_content = f"{self.prefix}\n\nInput: {last_message_content}\n\n{formatted_functions}"
            updated_messages[-1]["content"] = updated_last_message_content

        return updated_messages