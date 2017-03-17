import boto3 

dir_index = 0
ingredient_index = 0
in_recipe = False

dir_list = []
ingredient_list = []

in_directions = False

def lambda_handler(event, context):
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.af592cd8-bf56-4a68-b526-3dcb61bde70d"):
        raise ValueError("Invalid Application ID")
    
    if event["session"]["new"]:
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

def on_session_started(session_started_request, session):
    print "Starting new session."

def on_launch(launch_request, session):
    return get_welcome_response()

def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "start_directions_intent":
        return handle_start_directions_intent(intent, session)
    elif intent_name == "next_ingredient_intent":
        return handle_next_ingredient_intent(intent, session)
    elif intent_name == "next_step_intent":
        return handle_next_step_intent(intent, session)
    elif intent_name == "last_ingredient_intent":
        return handle_last_ingredient_intent(intent, session)
    elif intent_name == "last_step_intent":
        return handle_last_step_intent(intent, session)
    elif intent_name == "restart_intent":
        return handle_restart_intent(intent, session)
    elif intent_name == "start_ingredients_intent":
        return handle_start_ingredients_intent(intent, session)
    elif intent_name == "exit_intent":
        return handle_exit_intent(intent, session)
    elif intent_name == "welcome_intent":
        return get_welcome_response(intent, session)
    elif intent_name == "options_intent":
        return handle_options_intent(intent, session)
    elif intent_name == "food_choices_intent":
        return handle_food_choices_intent(intent, session)


    else:
        raise ValueError("Invalid intent")

def on_session_ended(session_ended_request, session):
    print "Ending session."
    # Cleanup goes here...

def handle_session_end_request():
    card_title = ""
    speech_output = "Thank you for using the BART skill.  See you next time!"
    should_end_session = True

    return build_response({}, build_speechlet_response(card_title, speech_output, None, should_end_session))

def get_welcome_response():
    session_attributes = {}
    card_title = "Recipe Assisstant"
    speech_output = "recipe assisstant, what recipe would you like to make?"

    reprompt_text = "Please ask me for recipe assistance."
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def handle_start_ingredients_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions

    card_title = intent["name"]
    session_attributes = {}
    should_end_session = False
    ingredient_index = 0
    speech_output = 'We will start by saying the ingredients. '\
                    'Say next ingredient to proceed or last ingredient to go back. '\
                    'You will need ' + str(ingredient_list[ingredient_index]) + '.'

    in_directions = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))

def handle_start_directions_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions
    card_title = intent["name"]
    session_attributes = {}
    should_end_session = False
    dir_index = 0
    in_directions = True
    speech_output = "We will now read the directions. Say next step to go forward or last step to go backwards. Say start again to start over. " \
                   " The first step is to " + str(dir_list[dir_index]) + '.'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))

def handle_next_ingredient_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions

    card_title = intent["name"]
    # emergency_type = intent['slots']['help_call']['value']
    session_attributes = {}
    should_end_session = False
    speech_output = ""

    if ingredient_index >= len(ingredient_list) - 1:
        speech_output = " These are all the required ingredients. We will proceed with the directions. Say read recipe to proceed. "
        in_directions = True
    else:
        ingredient_index += 1
        speech_output = str(ingredient_list[ingredient_index]) + '.'

    if ingredient_index == len(ingredient_list) - 1:
        speech_output += " These are all the required ingredients. We will proceed with the directions. Say read recipe to proceed. "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))
def handle_next_step_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions

    card_title = intent["name"]
    session_attributes = {}
    should_end_session = False
    speech_output = ""

    if dir_index >= len(dir_list) - 1:
        speech_output = " You have finished the recipe! Enjoy your meal."
    else:
        dir_index += 1
        speech_output = str(dir_list[dir_index]) + '.'

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))


def handle_last_step_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions
 
    card_title = intent["name"]
    # emergency_type = intent['slots']['help_call']['value']
    session_attributes = {}
    should_end_session = False
    speech_output = ""

    if dir_index != 0:
        dir_index -= 1
    
    speech_output = dir_list[dir_index]

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))
def handle_last_ingredient_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions
 
    card_title = intent["name"]
    session_attributes = {}
    should_end_session = False
    speech_output = ""

    if ingredient_index != 0:
        ingredient_index -= 1
    speech_output = ingredient_list[ingredient_index]

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))
def handle_restart_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions

    card_title = intent["name"]
    session_attributes = {}
    should_end_session = False
    speech_output = ""

    if in_directions:
        dir_index = 0
        speech_output = "The first step is " + dir_list[dir_index]
    else:
        ingredient_index = 0
        speech_output = "You will need a " + ingredient_list[ingredient_index]

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))

def handle_exit_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions

    card_title = intent["name"]
    session_attributes = {}
    should_end_session = True
    speech_output = "Goodbye. Have a good life. "

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))
def handle_options_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions

    card_title = intent["name"]
    session_attributes = {}
    should_end_session = False
    speech_output = "You can say: quit or exit. You can also say: find recipe name where recipe name is the name of your recipe, I'd like to make recipe name, where recipe name is the name of your recipe."


    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))

#copy prog02
def handle_food_choices_intent(intent, session):
    global in_recipe, dir_index, dir_list, ingredient_list, ingredient_index, in_directions

    card_title = intent["name"]
    session_attributes = {}
    should_end_session = False
    speech_output = ""

    dynamodb = boto3.resource('dynamodb',
      # aws_session_token=aws_session_token,
      aws_access_key_id='AKIAIXDMBN2ENR6HG7UQ',
      aws_secret_access_key='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',
      region_name='us-east-1'
    )

    table = dynamodb.Table('RecipeList')
    data = table.scan().get('Items')
    # print 'data', data
    food_type = intent['slots']['food_choice']['value']

    found_recipe = False
    for i, recipe_dict in enumerate(data):
        print recipe_dict['RecipeName'].lower(), str(food_type).lower(), 'aaaaaaaaaaaaaaaaaaaaaa'
        if recipe_dict['RecipeName'].lower() == str(food_type).lower():
            found_recipe = True
            in_recipe = True
            dir_index = 0
            ingredient_index = 0
            ingredient_list = data[i].get('IngredientsList').split('\n')
            dir_list = data[i].get('PrepDirections').split('\n')

    if not found_recipe:
        speech_output = "Recipe not found."
        return build_response(session_attributes, build_speechlet_response(
            card_title, speech_output, None, should_end_session
        ))


    speech_output = "Recipe found. Say ingredients when you are ready to begin the recipe."

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, None, should_end_session
    ))

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        "outputSpeech": {
            "type": "PlainText",
            "text": output
        },
        "card": {
            "type": "Simple",
            "title": title,
            "content": output
        },
        "reprompt": {
            "outputSpeech": {
                "type": "PlainText",
                "text": reprompt_text
            }
        },
        "shouldEndSession": should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        "version": "1.0",
        "sessionAttributes": session_attributes,
        "response": speechlet_response
    }
