"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import datetime


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Please ask for rahukaalam time by saying rahukaalam today"
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask for rahukaalam time by saying " \
                    "rahukaalam today"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def create_favorite_day_attributes(favorite_day):
    return {"favoriteColor": favorite_day}
    
def speech_output_sun():
    return speech_output_text("Sunday","4.30 PM to 6 PM","3 PM to 4.30 PM","12 Noon to 1.30 PM")

def speech_output_mon():
    return speech_output_text("Monday","7.30 AM to 9 AM","1.30 PM to 3 PM","10.30 AM to 12 Noon")

def speech_output_tue():
    return speech_output_text("Tuesday","3 PM to 4.30 PM","12 Noon to 1.30 PM","9 AM to 10.30 AM")

def speech_output_wed():
    return speech_output_text("Wednesday","12 Noon to 1.30 PM","10.30 AM to 12 Noon","7.30 AM to 9 AM")

def speech_output_thu():
    return speech_output_text("Thursday","1.30 PM to 3 PM","9 AM to 10.30 AM","6 AM to 7.30 AM")

def speech_output_fri():
    return speech_output_text("Friday"	,"10.30 AM to 12 Noon",	"7.30 AM to 9 AM","3 PM to 4.30 PM")

def speech_output_sat():
    return speech_output_text("Saturday",	"9 AM to 10.30 AM","6 AM to 7.30 AM","1.30 PM to 3 PM")


def speech_output_text(day_text,rahu_time_text,gulika_kalam_text,yama_gandam_text,):
    speech_output = "Today is " + day_text + "," + \
                    " Rahu Kaalam is " + rahu_time_text + \
                    " Yama Gandam is " + yama_gandam_text + \
                    " and Gulika Kaalam is " + gulika_kalam_text + \
                    ". Thank you"
    return speech_output



def get_rahukalam_in_session(intent, session):
    """ Gets the Rahukalam in the session and prepares the speech to reply to the
    user.
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    
    
    dayOfWeek=datetime.datetime.today().weekday()
    #dayOfWeek=6
    options = {0 : speech_output_mon,
                1 : speech_output_tue,
                2 : speech_output_wed,
                3 : speech_output_thu,
                4 : speech_output_fri,
                5 : speech_output_sat,
                6 : speech_output_sun,
            }

    speech_output = options[dayOfWeek]()
    
    
    session_attributes = create_favorite_day_attributes(dayOfWeek)
    reprompt_text = "You can ask me to say it again  by saying, " \
                    "repeat"

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetRahukalam":
        return get_rahukalam_in_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.02446798-64b1-4aba-81b7-843eb91ad5f1"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])

