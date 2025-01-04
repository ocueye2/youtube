from ollama import Client
from image.imagegen import makeimage

thing = Client(host='http://localhost:8081')

available_functions = {
  'makeimage': makeimage
}

def checkcalls(response, messages):
    global available_functions
    if response.message.tool_calls:
        for tool in response.message.tool_calls:
            if function_to_call := available_functions.get(tool.function.name):
                output = function_to_call(**tool.function.arguments)
            else:
                pass

    if response.message.tool_calls:
        messages.append(response.message)
        messages.append({'role': 'tool', 'content': "done", 'name': tool.function.name})

        final_response = thing.chat('llama3.1', messages=messages)  # Use the send method instead of calling the object
        return final_response.message.content
    else:
        pass