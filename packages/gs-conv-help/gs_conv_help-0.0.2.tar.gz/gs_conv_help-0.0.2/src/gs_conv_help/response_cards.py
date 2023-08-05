import json
from pathlib import Path
from time import localtime,strftime

def show_response_card(gs_context,current_context,response_details):
    channel = gs_context['channel']
    if response_details['card_type'] == 'list':
        validate_list(channel,response_details)
        list_json = render_list(channel,response_details)
        current_context['response_queue'].append(list_json)
    elif response_details['card_type'] == 'quick_reply':
        validate_quick_reply(channel,response_details)
        quick_reply_json = render_quick_reply(channel,response_details)
        current_context['response_queue'].append(quick_reply_json)
    elif response_details['card_type'] == 'text':
        text = response_details['message']
        current_context['response_queue'].append(str(text))
    elif response_details['card_type'] == 'file':
        file_json = render_file(channel,response_details)
        current_context['response_queue'].append(file_json) 
    elif response_details['card_type'] == 'image':
        img_json = render_image(channel,response_details)
        current_context['response_queue'].append(img_json)                
    return

def validate_list(channel,response_details):
    if channel == 'whatsapp':
        len_title = len(response_details['main_title'])
        if len_title > 60:
            raise Exception("main_title has exceeded the character limit of 60!")
        len_body = len(response_details['main_body'])
        if len_body > 1024:
            raise Exception("main_body has exceeded the character limit of 1024!")
        len_button = len(response_details['button_text'])
        if len_button > 20:
            raise Exception("button_text has exceeded the character limit of 20!")
        for section in response_details['sections']:
            if 'title' not in section.keys():
                raise Exception("Section does not have a Title!")
            for option in section['options']:
                len_opt_title = len(option['title'])
                if len_opt_title > 24:
                    raise Exception(f"'{option['title']}' has exceeded the character limit of 24!")
                if 'description' in option.keys():
                    len_desc = len(option['description'])
                    if len_desc > 72:
                        raise Exception(f"'{option['description']}' has exceeded the character limit of 72!")
    return

def render_list(channel,response_details):
    list_json = {}
    if channel == 'whatsapp':
        main_title = response_details['main_title']
        main_body = response_details['main_body']
        button_text = response_details['button_text']
        section_list = response_details['sections']
        item_list = []
        for section in section_list:
            section_body = {}
            section_body['title'] = section['title']
            elements = section['options']
            options_list = []
            for element in elements:
                options = {}
                options['type'] = 'text'
                options['title'] = element['title']
                if 'description' in element.keys():
                    options['description'] = element['description']
                if 'postbackText' in element.keys():
                    options['postbackText'] = element['postbackText']
                options_list.append(options)
            section_body['options'] = options_list
            item_list.append(section_body)
        list_json['type'] = 'list'
        list_json['title'] = main_title
        list_json['body'] = main_body
        list_json['msgid'] = 'lst1'
        list_json['globalButtons'] = []
        list_json['globalButtons'].append({"type":"text","title":str(button_text)})
        list_json['items'] = item_list
    return list_json

def validate_quick_reply(channel,response_details):
    if channel == 'whatsapp':
        if 'header' in response_details.keys():
            len_header = len(response_details['header'])
            if len_header > 60:
                raise Exception("header has exceeded the character limit of 60!")
        if 'caption' in response_details.keys():
            len_caption = len(response_details['caption'])
            if len_caption > 60:
                raise Exception("cation has exceeded the character limit of 60!")
        len_options = len(response_details['options'])
        if len_options > 3:
            raise Exception("You cannot use more than 3 quick reply buttons in whatsapp!")
    return

def render_quick_reply(channel,response_details):
    quick_reply_json = {}
    if channel == 'whatsapp':
        buttons = response_details['options']
        options_list = []
        for button in buttons:
            button_dict = {}
            button_dict['type'] = 'text'
            button_dict['title'] = str(button)
            options_list.append(button_dict)
        quick_reply_json['type'] = 'quick_reply'
        quick_reply_json['content'] = {}
        quick_reply_json['content']['type'] = 'text'
        if 'content_type' in response_details.keys():
            quick_reply_json['content']['type'] = response_details['content_type']
        if 'header' in response_details.keys():
            quick_reply_json['content']['header'] = response_details['header']
        quick_reply_json['content']['text'] = response_details['body']
        if 'caption' in response_details.keys():
            quick_reply_json['content']['caption'] = response_details['caption']
        if 'url' in response_details.keys():
            quick_reply_json['content']['url'] = response_details['url']
        quick_reply_json['msgid'] = 'qr1'
        quick_reply_json['options'] = options_list
    return quick_reply_json

def render_file(channel,response_details):
    file_json = {}
    if channel == 'whatsapp':
        file_json['type'] = 'file'
        file_json['url'] = response_details['url']
        file_json['filename'] = response_details['filename']
    return file_json

def render_image(channel,response_details):
    image_json = {}
    if channel == 'whatsapp':
        image_json['type'] = 'image'
        image_json['originalUrl'] = response_details['url']
        image_json['previewUrl'] = response_details['url']
        image_json['caption'] = response_details['caption']
    return image_json

def behave_extract_bot_response_text(channel,bot_response):
    if channel == 'whatsapp':
        bot_text = ''
        if len(bot_response) > 1:
            for resp in bot_response:
                if resp['text'][0] != '{':
                    bot_text = resp['text']
                    break
        else:
            bot_text = bot_response[0]['text']
        return bot_text

def behave_compare_text(input_text,bot_text):
    if input_text == bot_text:
        return True
    return False

def behave_extract_bot_response_quick_reply(channel,bot_response):
    if channel == 'whatsapp':
        bot_text = ''
        bot_buttons = []
        if len(bot_response) > 1:
            for resp in bot_response:
                if resp['text'][0] == '{':
                    qr_json = json.loads(resp['text'])
                    bot_text = qr_json['content']['text']
                    for option in qr_json['options']:
                        bot_buttons.append(option['title'])  
                    break
        else:
            qr_json = json.loads(bot_response[0]['text'])
            bot_text = qr_json['content']['text']
            for option in qr_json['options']:
                bot_buttons.append(option['title'])
        return bot_text.strip(),bot_buttons.sort()  

def behave_compare_quick_reply(input_message,bot_message,button_input,bot_buttons):
    if (input_message == bot_message) and (button_input == bot_buttons):
        return True
    return False

def behave_extract_bot_response_list(channel,bot_response):
    if channel == 'whatsapp':
        bot_text = ''
        bot_list = []
        if len(bot_response) > 1:
            for resp in bot_response:
                if resp['text'][0] == '{':
                    list_json = json.loads(resp['text'])
                    bot_text = list_json['body']
                    for item in list_json['items']:
                        list_element = {}
                        list_element["Category"] = item['title']
                        list_element["Items"] = []
                        for option in item['options']:
                            list_element["Items"].append(option['title'])
                        bot_list.append(list_element)
                    break
        else:
            list_json = json.loads(bot_response[0]['text'])
            bot_text = list_json['body']
            for item in list_json['items']:
                list_element = {}
                list_element["Category"] = item['title']
                list_element["Items"] = []
                for option in item['options']:
                    list_element["Items"].append(option['title'])
                bot_list.append(list_element)
        return bot_text.strip(),bot_list          

def behave_compare_list(input_message,bot_message,list_input,bot_list):      
    list_comparison = True
    for category in list_input:
        category['Items'].sort()
    for category in bot_list:
        category['Items'].sort()
    for element in list_input:
        if element not in bot_list:
            list_comparison = False
    for element in bot_list:
        if element not in list_input:
            list_comparison = False
    if (input_message == bot_message) and (list_comparison == True):
        return True
    return False

def log_behave_failures(card_type,input_message,bot_message,input_features,output_features):
    log_location = '/tmp/behave_failed.log'
    myfile = Path(log_location)
    myfile.touch(exist_ok=True)
    #timenow=strftime("%Y-%m-%d %H:%M:%S", localtime())
    if card_type == 'text':           
        with open(log_location, "a") as file_object:
            file_object.write("\n{0} - {1} validation failed!\n".format(str(strftime("%Y-%m-%d %H:%M:%S", localtime())),str(card_type)))
            file_object.write("Input/Feature Text:\n")
            file_object.write(input_message)
            file_object.write("\nOutput/Bot Text:\n")
            file_object.write(bot_message)
    if card_type == 'list':           
        with open(log_location, "a") as file_object:
            file_object.write("\n{0} - {1} validation failed!\n".format(str(strftime("%Y-%m-%d %H:%M:%S", localtime())),str(card_type)))
            file_object.write("Input/Feature Text:\n")
            file_object.write(input_message)
            file_object.write("\nInput/Feature Options:\n")
            file_object.write(str(input_features))
            file_object.write("\nOutput/Bot Text:\n")
            file_object.write(bot_message)
            file_object.write("\nOutput/Bot Options:\n")
            file_object.write(str(output_features))
    if card_type == 'quick_reply':           
        with open(log_location, "a") as file_object:
            file_object.write("\n{0} - {1} validation failed!\n".format(str(strftime("%Y-%m-%d %H:%M:%S", localtime())),str(card_type)))
            file_object.write("Input/Feature Text:\n")
            file_object.write(input_message)
            file_object.write("\nInput/Feature Options:\n")
            file_object.write(str(input_features))
            file_object.write("\nOutput/Bot Text:\n")
            file_object.write(bot_message)
            file_object.write("\nOutput/Bot Options:\n")
            file_object.write(str(output_features))
    return
