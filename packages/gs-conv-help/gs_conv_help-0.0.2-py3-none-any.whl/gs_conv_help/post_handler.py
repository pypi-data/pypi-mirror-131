import json
from rasa_sdk.events import (SlotSet)
    
def post_handle(dispatcher, gs_context, current_context):
    response_queue = current_context["response_queue"]
    for element in response_queue:
        if type(element) == (str):
            dispatcher.utter_message(text = element)
        else:
            dispatcher.utter_message(text = json.dumps(element))
    return
def get_events(gs_context, current_context):
    
    return SlotSet('gs_context',json.dumps(gs_context))