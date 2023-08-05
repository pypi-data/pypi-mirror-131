# Gupshup Conversation Helpers

## version 0.0.2 UPDATE

Support for image URL iss available in quick reply card now.

1. This repository contains artifacts to help accelerate development of conversational interfaces using Rasa & Gip
2. Refer [dialog-as-code.md](https://gitlab.gupshup.io/aiml/gs-conv-helpers/-/tree/master/docs) document to get started with understanding.

## Installation

1. Use the command mentioned in the pypi.
2. Pre Requisites of this package is rasa in a environment.
3. python version below 3.8

## Methods

### Pre Handler

Pre Handler contain a method, get_context.

1. get_context is used to set the gs_context from previous context and creates current_context dict.
2. Get_context interanal sets few variables at the start of the conversion i.e active_menu,active_menu_state,menu_handled, live_dict
3. These variables get refreshed each time accordingly.

        import gs_conv_help as helpers
        gs_context,current_context = helpers.get_context(dispatcher, tracker, domain)

### Post handler

Post handler contain 2 methods, post_handle and get_events.

1. post_handle is used to pass the response queue messages to the platform.
2. get_events is used to set back the gs_context varible to slots of rasa.

        helpers.post_handle(dispatcher,gs_context,current_context)

### Response cards

Response cards contain a method, show_response_card.

1. show_response_card is used to convert a simple text or quick reply ot list into appropriate format.
2. This method is used whenever there is a requirement of utter.

        helpers.show_response_card(gs_context,current_context,response_json)

### Menu handler

Menu handler contain 2 methods, handle_active_menu and activate_menu.

1. Menu, for any bot has to declared in domain.yml file of the bot.
2. Whenevere a intent which triggers men is encountered then activate_menu is called with the intent name.
3. activate_menu sets the menu_handled in gs_context to True which will help us to keep the conversation within menu.
4. handle_active_menu method will be activated when menu_handled is true. this method will traverse through the menu options.
5. In this current version, User entered text should exactly match with the options provided to traverse in the menu.
6. Once all the options in the menu gets filled it will return current intent as "Menu_Completed" in current_context.

    **Menu handler code is still in development**

        helpers.activate_menu(gs_context,current_context,"clothes")
        helpers.handle_active_menu(gs_context,current_context)

### DB handler

Menu handler is a class, which is initiated with database info.

1. once the class object is created we can use few methods for opertions.
2. methods are csv_to_db, get_document_for_key and set_document_for_key.

Sample Variables:

 gs_context:

        {
        "sender_id": "03d362d4-aad9-4fc4-8ed0-84930852a38d_whatsapp:918217708911",
        "channel": "whatsapp",
        "active_menu": "clothes",
        "active_menu_state": ["clothes", "Women", "Custom Search"],
        "slots": {},
        "menu_handled": True,
        "past_conversation": "",
        "live_dict": { "Text Search": "", "Image Search": "" }
        }

Current context:

        {
        "current_intent": {
        "intent": "goodbye",
        "entities": {},
        "user_text": "Custom Search"
        },
        "domain": {
        "config": { "store_entities_as_slots": "True" },
        "session_config": {
        "session_expiration_time": 60,
        "carry_over_slots_to_new_session": "True"
        },
        "intents": [
        { "restart": { "use_entities": "True" } },
        { "greet": { "use_entities": "True" } },
        { "goodbye": { "use_entities": "True" } },
        { "clothes": { "use_entities": "True" } },
        { "support": { "use_entities": "True" } },
        { "nlu_fallback": { "use_entities": "True" } },
        { "main_menu": { "use_entities": "True" } },
        { "out_of_scope": { "use_entities": "True" } },
        { "check_human": { "use_entities": "True" } },
        { "affirm": { "use_entities": "True" } },
        { "deny": { "use_entities": "True" } },
        { "inform": { "use_entities": "True" } },
        { "welcome": { "use_entities": "True" } },
        { "later": { "use_entities": "True" } },
        { "gender": { "use_entities": "True" } },
        { "search": { "use_entities": "True" } },
        { "productsearch": { "use_entities": "True" } },
        { "faqs": { "use_entities": "True" } },
        { "help": { "use_entities": "True" } },
        { "thankyou": { "use_entities": "True" } },
        { "Feedback": { "use_entities": "True" } },
        { "product_menu": { "use_entities": "True" } }
        ],
        "entities": ["category", "gender_ent", "product", "main_menu"],
        "slots": {
        "gs_context": {
                "type": "rasa.shared.core.slots.TextSlot",
                "initial_value": "None",
                "auto_fill": "True",
                "influence_conversation": "True"
        }
        },
        "responses": {},
        "actions": ["action_custom_handler"],
        "forms": {},
        "e2e_actions": []
        },
        "response_queue": [
        {
        "type": "quick_reply",
        "content": {
                "type": "text",
                "header": "",
                "text": "Great🤓 now, please choose if you want to do a text search or Image Search \nPlease choose one from the below options",
                "caption": ""
        },
        "msgid": "qr1",
        "options": [
                { "type": "text", "title": "Text Search" },
                { "type": "text", "title": "Image Search" }
        ]
        }
        ]
        }


sample menu written in domain yml for a bot:

```
menus:
  clothes:
    Invalid-choice-message: That doesn't appear to be a valid choice
    prompt: Alright! I'm curious 🤩 as to what kind of outfits you're looking for, please choose one category.
    Card_Type: quick_reply
    Women:
      Invalid-choice-message: That doesn't appear to be a valid choice
      List_Header: Please choose from the following
      Card_Type: list
      List_category: select any one
      prompt: |-
        Awesome 🤩🤩 now you can customize your attire according to your preferred style, grab the best deals or search the best match. 
        Please choose one from the below options
      Custom Search:
        Invalid-choice-message: That doesn't appear to be a valid choice
        Card_Type: quick_reply
        prompt: |-
          Great🤓 now, please choose if you want to do a text search or Image Search 
          Please choose one from the below options
        Category:
          - Text Search
          - Image Search
      Create Whole Outfit:
        Invalid-choice-message: That doesn't appear to be a valid choice
        Card_Type: quick_reply
        prompt: |-
          We will help you create a unique, versatile wardrobe, so you never have to think about what to wear again. 
          Let's get to know your style with a few quick questions. 
          What kind of outfits you're looking for, please choose one category.
        Category:
          - Text Search
          - Image Search
      Style my outfit:
        Invalid-choice-message: That doesn't appear to be a valid choice
        Card_Type: quick_reply
        prompt: Now find effortless ways to become more fashionable. You can find matching apparel and accessory from head to toes.
        Clothes:
          - Top Wear
          - Bottom wear
        Accessories:
          - Top Wear
          - Bottom wear
        Shoes:
          - Top Wear
          - Bottom wear
      Offers:
        Invalid-choice-message: That doesn't appear to be a valid choice
        List_Header: Please choose from the following
        Card_Type: list
        List_category: select any one
        prompt: Check out the best offers and deals here. Please choose one from the options below😊
        Category:
          - x % off
          - best seller
          - fresh in stock
          - picked by celebrity
          - others 
    Men:
      Invalid-choice-message: That doesn't appear to be a valid choice
      List_Header: Please choose from the following
      Card_Type: list
      List_category: select any one
      prompt: |-
        Awesome 🤩🤩 now you can customize your attire according to your preferred style, grab the best deals or search the best match. 
        Please choose one from the below options
      Custom Search:
        Invalid-choice-message: That doesn't appear to be a valid choice
        Card_Type: quick_reply
        prompt: |-
          Great🤓 now, please choose if you want to do a text search or Image Search 
          Please choose one from the below options
        Category:
          - Text Search
          - Image Search
      Style my outfit:
        Invalid-choice-message: That doesn't appear to be a valid choice
        Card_Type: quick_reply
        prompt: Now find effortless ways to become more fashionable. You can find matching apparel and accessory from head to toes.
        Clothes:
          - Top Wear
          - Bottom wear
        Accessories:
          - Top Wear
          - Bottom wear
        Shoes:
          - Top Wear
          - Bottom wear
      Offers:
        Invalid-choice-message: That doesn't appear to be a valid choice
        List_Header: Please choose from the following
        Card_Type: list
        List_category: select any one
        prompt: Check out the best offers and deals here. Please choose one from the options below😊
        Category:
          - x % off
          - best seller
          - fresh in stock
          - picked by celebrity
          - others
```