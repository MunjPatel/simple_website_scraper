class GSEExceptions(Exception):
    """
    
    Scraper exceptions class which inherits properties of the 'Exception' class. Returns a string as output.
    Specifically for scraping list of websites using GSE.

    """
    def __init__(self,_arg_:str)->None:
        self._arg_ = _arg_
        super().__init__(self._arg_)
    def __str__(self) -> str:
        return self._arg_
    
class ScraperExceptions(Exception):
    """
    
    Scraper exceptions class which inherits properties of the 'Exception' class. Returns a string as output.
    Specifically for scraping list of websites without GSE.

    """
    def __init__(self,_arg_:str)->None:
        self._arg_ = _arg_
        super().__init__(self._arg_)
    def __str__(self) -> str:
        return self._arg_
    
class NumError(GSEExceptions):
    """
    
    Exception raised when number of desired links either exceeds 105 or is equal to 0.
    
    """
    pass

class ZeroResultsError(GSEExceptions):
    """
    
    Exception raised when no results are generated for a given combination of number of results and query.
    
    """
    pass

class UACreateError(GSEExceptions or ScraperExceptions):
    """
    
    Exception raised when fake user-agent generation fails.
    
    """
    pass

class ZeroUrlError(GSEExceptions or ScraperExceptions):
    """
    
    Exception raised when an empty list of urls in passed to the threadpool-executor.
    
    """
    pass

class WaitTimeError(GSEExceptions or ScraperExceptions):
    """
    
    Exception raised when the wait time value of 0 or less is given when making requests.
    
    """
    pass

class InvalidSimilarityMetric(GSEExceptions or ScraperExceptions):
    """
    
    Exception raised when the similarity metric entered by user is not one of values of: 

    (1) r(ratio)
    (2) pr(partial_ratio)
    (3) tsr_set(token_set_ratio)
    (4) ptsr_set(partial_token_set_ratio)
    (5) tsr_sort(token_sort_ratio)
    (6) ptsr_sort(partial_token_sort_ratio)
    
    """
    pass