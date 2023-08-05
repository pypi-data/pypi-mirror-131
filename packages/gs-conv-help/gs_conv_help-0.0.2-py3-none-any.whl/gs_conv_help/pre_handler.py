import json


def get_context(dispatcher, tracker, domain):
    channel = "whatsapp"  # if 'whatsapp' in str(tracker.sender_id) else "gip"
    entities = tracker.latest_message["entities"]
    dicts = {}
    for item in entities:
        dicts[item["entity"]] = item["value"]
    entity_dict = dicts
    gs_context_dict = tracker.get_slot("gs_context")
    if gs_context_dict is None:
        slots = {}
        active_menu = ""
        active_menu_state = []
        menu_handled = False
        live_dict = {}
        past_conversation = ""
    else:
        gs_context_dict = json.loads(gs_context_dict)
        slots = gs_context_dict["slots"]
        active_menu = gs_context_dict["active_menu"]
        active_menu_state = gs_context_dict["active_menu_state"]
        menu_handled = gs_context_dict["menu_handled"]
        live_dict = gs_context_dict["live_dict"]
        past_conversation = gs_context_dict["past_conversation"]

    gs_context = {"sender_id": tracker.sender_id, "channel": channel,
                  "active_menu": active_menu, "active_menu_state": active_menu_state, "slots": slots, "menu_handled": menu_handled, "live_dict": live_dict, "past_conversation": past_conversation}
    current_intent = {"intent": tracker.latest_message['intent'].get('name'),
                      "entities": entity_dict,
                      "user_text": tracker.latest_message["text"]}
    current_context = {"current_intent": current_intent,
                       "domain": domain, "response_queue": []}

    return gs_context, current_context
