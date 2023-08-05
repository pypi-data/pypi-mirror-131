from .response_cards import show_response_card

def format_response_card_quick_reply(gs_context, current_context, response):
    response_json_quick = {}
    response_json_quick["card_type"] = "quick_reply"
    response_json_quick["header"] = ""
    response_json_quick["body"] = response["title"]
    response_json_quick["caption"] = ""
    filter_buttons = ['Invalid-choice-message','prompt','Card_Type','List_Header','List_Category']
    response["options"] = [x for x in response['options'] if x not in filter_buttons]
    response_json_quick["options"] = response["options"]
#     print(response_json_quick)
    show_response_card(gs_context, current_context, response_json_quick)


def format_response_card_list(gs_context, current_context, response, temp_menu):
    response_json_list = {}
    # print(temp_menu)
    response_json_list['card_type'] = temp_menu['Card_Type']
    response_json_list['main_title'] = temp_menu['List_Header']
    response_json_list['main_body'] = response['title']
    response_json_list['button_text'] = "Show list"
    response_json_list["sections"] = []
    response_json_list_cat1 = {}
    response_json_list_cat1["title"] = temp_menu['List_category']
    options = []
    filter_buttons = ['Invalid-choice-message','prompt','Card_Type','List_Header','List_category']
    response["options"] = [x for x in response['options'] if x not in filter_buttons]
    for button in response["options"]:
        each_option = {}
        each_option["title"] = button
        options.append(each_option)
    response_json_list_cat1["options"] = options
    response_json_list["sections"].append(response_json_list_cat1)
    show_response_card(gs_context, current_context, response_json_list)
#     print(response_json_list)


def activate_menu(gs_context, current_context, selection):
    '''
        This function activates the handle active menu until
        the menu_handled is true.
    '''
    current_context['current_intent']['user_text'] = selection
    gs_context['active_menu'] = selection
    # gs_context['active_menu_state'].append(selection)
    gs_context['menu_handled'] = True
    handle_active_menu(gs_context, current_context)
    return


def handle_active_menu(gs_context,current_context):
    """
        This function will come handy when it is a live dictionary
    """
#     selection = current_context['current_intent']['user_text']
#     print('Print whether the live dictionary is list',isinstance(gs_context['live_dict'][selection],dict))
    if gs_context['menu_handled']:
        selection = current_context['current_intent']['user_text']
        temp_selection = selection.split(" ")
        if len(temp_selection) >1 and temp_selection[-1].isdigit():
            selection = " ".join(temp_selection[:-1])
        response ={}
        if isinstance(gs_context['live_dict'],dict):
            available_key_live_dict = list(gs_context['live_dict'].keys())
        elif isinstance(gs_context['live_dict'],list):
            available_key_live_dict = gs_context['live_dict']
        try:
            if selection in available_key_live_dict:
                temp_menu = gs_context['live_dict'][selection].copy()
                try:
                    option_to_user = list(temp_menu.keys())#available dictionary
                    response['title'] = temp_menu['prompt']
                except:
                    option_to_user = temp_menu
                    response['title'] = 'Please select the options'
                gs_context['menu_handled'] = True
                option_to_user = [x for x in option_to_user if x not in ['Invalid-choice-message','prompt']]
                # response['title'] = temp_menu['prompt']
                if 'Category' not in option_to_user:
                    response['options'] = option_to_user
                    gs_context['live_dict'] = temp_menu
                    print('options without Category')
                    gs_context['active_menu'] = selection
                    gs_context['active_menu_state'].append(selection)
                    # print('normal',response)
                else:
                    category_options = temp_menu['Category']
                    print('options with Category')
                    other_option = temp_menu.keys()
                    left_options = [x for x in other_option if x not in ['Category']]
                    temp_temp_menu = {}
                    for key,value in temp_menu.items():
                        if key in left_options:
                            temp_temp_menu[key] = value
                    for keys in category_options:
                        temp_temp_menu[keys] = ''
                    # print(temp_temp_menu)
                    gs_context['live_dict'] = temp_temp_menu
                    gs_context['active_menu'] = selection
                    gs_context['active_menu_state'].append(selection)
                    left_options.extend(category_options)
                    response['options'] = left_options
                    # print(left_options)
            else:
                temp_menu = gs_context['live_dict'].copy()
                print('Wrong option else')
                response['title'] = gs_context['live_dict']['Invalid-choice-message']
                option_to_user = gs_context['live_dict'].keys()
                option_to_user = [x for x in option_to_user if x not in ['Invalid-choice-message','prompt']]
                response['options'] = option_to_user
            if temp_menu['Card_Type'] == 'list':
                format_response_card_list(gs_context,current_context,response,temp_menu)
            else:
                format_response_card_quick_reply(gs_context,current_context,response)
        except Exception as e:
            if selection in gs_context['live_dict']:
                print('Here I am in the except command')
                gs_context['active_menu_state'].append(selection)
                gs_context['menu_handled']=False
                current_context["current_intent"]={'intent': 'Menu_Completed', 'entities': {}, 'user_text': ''}
            else:
                print('Thas is a wrong option please choose the one from the below')
                response['title'] = 'Thas is a wrong option please choose the one from the below'
                option_to_user = gs_context['live_dict']
                gs_context['menu_handled']=True
                response['options'] = option_to_user
                temp_menu = option_to_user
                if temp_menu['Card_Type'] == 'list':
                    format_response_card_list(gs_context,current_context,response,temp_menu)
                else:
                    format_response_card_quick_reply(gs_context,current_context,response)
    #             print(option_to_user)
                return
        return