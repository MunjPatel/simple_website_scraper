import requests as re
import time
import random
from scraper_exceptions.exceptions import NumError,WaitTimeError
from src.utils import header_dictionary, log_instance
from src.multithreading import MultipleRequests, SimilarityScore, user_agent, ZeroResultsError, ZeroUrlError
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError, HTTPError, ConnectTimeout, Timeout

multi_requests = MultipleRequests()
similarity_score = SimilarityScore()

class GoogleSearchUrls:
    def __init__(self)->None:
        pass
    def get_urls(self,search_string:str,num_results:int, wait_period:str)->list:
        """
        
        Function that generates a list of URLs. It will exclude any google/youtube links. 

        Input: self
        Output: list
        Exceptions: ConnectTimeout, HTTPError, JSONDecodeError, Timeout, ConnectionError
        
        """
        if type(num_results) == int and (1 <= num_results <= 105) and type(wait_period) == int and wait_period > 0:
            try:
                choices = random.choice([i for i in range(5,11)])
                log_instance.get_critical(f"Applying {choices} second buffer delay before sending request to GSE for given query.")
                time.sleep(choices)
                log_instance.get_info(f":::Searching google for: '{search_string}':::")
                url = "https://www.google.com/search?q=" + "+".join(search_string.lower().split(" ")) + "&num=" + str(num_results + 20)
                url_headers = header_dictionary()
                if user_agent is None:
                    del url_headers["User-Agent"]
                else:
                    url_headers["User-Agent"] = url_headers["User-Agent"].format(user_agent)
                response = re.request("GET", url, headers=url_headers, timeout=wait_period)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    l_href = [href.get("href") for href in soup.find_all('a', href=True)]
                    l_pseudo_links = [link for link in [l_href[index].split(str(l_href[index][l_href[index].find("https") - 1]))[1]
                                                        for index in range(len(l_href)) if "https" in l_href[index]] if
                                    "https" in link and len(link) > 0]
                    l_https = [l_pseudo_links[index].split('&')[0] for index in range(len(l_pseudo_links))
                            if len(l_pseudo_links[index].split('&')) > 0]
                    global l_links
                    l_links = []
                    for links in l_https:
                        split_again = links.split('%')
                        if len(split_again) == 1 and "youtube.com" not in links and "google.com" not in links:
                            l_links.append(links)
                        elif len(split_again) >= 2 and "youtube.com" not in links and "google.com" not in links:
                            l_links.append(split_again[0])
                        else:
                            pass
                    l_links = [i for i in l_links if "'" not in i[-int(0.6 * len(l_links)):]]
                    l_links = list(set(l_links))[:num_results]
                    if len(l_links) == 0:
                        raise ZeroResultsError(_arg_ = f"Number of links generated: {len(l_links)}. Failed to generate links from google! Make sure you have a stable internet connection.")
                    else:
                        pass
                    log_instance.get_critical(f"Succsessfully generated: {len(l_links)} links.")
                    return l_links
            except ConnectionError:
                log_instance.get_critical(str(ConnectionError(f"Encountered an error while trying to connect to GSE.")))
                return []
            except HTTPError:
                log_instance.get_critical(str(HTTPError(f"Request to GSE unsuccessfull.")))
                return []
            except ValueError:
                log_instance.get_critical(str(ValueError(f"Failed to decode server json response from GSE.")))
                return []
            except ConnectTimeout:
                log_instance.get_critical(str(ConnectTimeout(f"Request timed-out while trying to connect to GSE.")))
                return []
            except Timeout:
                log_instance.get_critical(str(Timeout(f"GSE failed to complete request in timeout-period.")))
                return []
            except Exception as e:
                log_instance.get_critical(str(Exception(f"Following error occured: {str(e)} when trying to connect to GSE.")))
                return []
        elif type(num_results) != int:
            raise TypeError(f"Process terminated. Wrong input type entered. 'num_results' is expected to be {int}, "
                        f"entered {type(num_results)} instead.")
        elif num_results > 105 or num_results < 1:
            raise NumError(_arg_ = f"Process terminated. You can only search for 1 <= num_results <= 105, entered {num_results} instead.")
        elif type(wait_period) != int:
            raise TypeError(f"Expected 'wait_time' argument of type {int}, got {type(wait_period)} instead.")
        elif wait_period <= 0:
            raise WaitTimeError(f"Expected 'wait_time' argument to be a non-zero positive integer, given {wait_period} instead.")


class GoogleSearchSimilarity:
    log_instance.clear_logs()
    def score(self, search_string:str, num_results:int, wait_time:int)->dict:
        """
        
        Method that generates a dicitonary of multiple urls and similarity scores based on the input query and the number of results desired.

        Inputs: self
        Outputs: dict

        
        """
        url_list = GoogleSearchUrls().get_urls(search_string,num_results,wait_period=wait_time)
        if len(url_list) != 0:
            results = multi_requests.parallel_requests(urls = url_list, input_string=search_string, wait_time=wait_time)
            return results
        else:
            raise ZeroUrlError(_arg_ = "Failed to generate urls from GSE. Make sure your input string is correct and internet connection is stable.")

if __name__ == "__main__":
    search = GoogleSearchSimilarity()
    strings = ["Assumptions of Linear Regression model.","Assumptions of MLR model.","SSR, SSE and SST in regression."]
    for string in strings:
        results = search.score(search_string=string, num_results=105, wait_time=1)
        print(results)