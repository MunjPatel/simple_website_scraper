import json
from scraper_exceptions.exceptions import UACreateError
from logging_functions.logs import Logger
from faker import Faker
from fake_useragent import UserAgent as ua_exception
from my_fake_useragent import UserAgent as ua_priority

log_instance = Logger()
log_instance.get_logger()
    
class FakeUserAgent:
    """
    
    Class used to generate fake user-agent for request headers using the fake_useragent and my_fake_useragent libraries. 

    It comprises of the fake_ua() method which can be called to generate the user-agent string.

    """
    def fake_ua(self)->str:
        """
        
        Uses fake_useragent and my_fake_useragent libraries to generate a user-agent string.

        Inputs: self
        Outputs: str
        Exceptions: UACreateError
        
        """
        try:
            ua = ua_priority()
            user_agent = ua.random() 
            return str(user_agent).strip()
        except:
            try:
                try:
                    ua = ua_exception()
                    user_agent = ua.random
                    return str(user_agent).strip()
                except:
                    return str(Faker().user_agent())
            except:
                log_instance.get_warning(arg=UACreateError("Temporary user-agent string generation failed. User-Agent key will be removed from request headers."))
                return None

def header_dictionary()->dict:
    """
    
    Used to fetch the predefined header dictionary used while sending requests to the google search engine.

    Input: None
    Output: Dictionary

    """
    try:
        # Try reading the json file.
        with open(r"artifacts\gse_headers.json","r") as json_data:
            headers = json.load(json_data)
        return headers["google"]
    except ValueError:
        # Raise this error if script fails to decode json file.
        raise ValueError("Failed to decode json file.")
    except Exception as e:
        raise Exception(f"Following error occured: {str(e)}.")