'''
This file contains functions to test a sentence for certain topics
'''

from util import utils
from util import detect_question

'''
return format for all functions in this module

{
    "test_result": boolean,
    "info": {
        <specific info for each topic, only if test_result is True>
    }
}
'''
def weather(text):
    '''
    Tests if the text is about weather and identifies any time words

    @param text: the text to analyze

    @return: a dictionary, format is specified at the top of the file
    '''
    output = {
        "test_result": False,
        "info": {}
    }
    
    #posessive determiner and noun phrase
    expression = r"""
    POS_DT: {<NN.*><POS><NN.*>*}
    NP: {<DT|JJ|NN.*>+}
    """
    
    target_words = utils.load_words("data/weather_topic_words.txt")
    chunks = detect_question.match_regex_and_keywords(
            text, expression, target_words)
    '''
    split_text = text.split()
    
    for word in target_words:
        if word in split_text:
            output["test_result"] = True

    if output["test_result"] == False:
        return output

    #maybe factor out into text file
    time_words = utils.load_words("data/weather_time_words.txt")

    return output
    '''

def restaurant(text):
    '''
    Checks if the text is about restaurants

    @param text: the text to analyze

    @return: a dictionary, format is specified at the top of the file
    '''

    output = {
        "test_result": False,
        "info": {}
    }
    
    output["test_result"] = "restaurant" in text.split()
    return output

