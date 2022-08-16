"""
@author: Layundji
@version : 1.0

This module provide a small manager for GET requests toward the metamob database.
To learn more about metamob API, go see the doc : https://metamob.fr/aide/api

for details, jump to the Metamob_API class
"""

import os
import requests
import datetime
import json

class Metamob_API :
    """
    Manager for addressing Metamob.

    Properties :
        - parent          (obj)  a parent class for object composition
        - verbose         (bool) make the manager speaking during processes
        - token_name      (str)  name a environmental variable holding the metamob API key
        - header          (dict) expected header for metamob GET request
        - base_url        (str)  metamob API domain
        - endpoints       (dict) all API endpoints
        - freeze          (bool) if True, refrain the manager from sending requests and purging the cache
        - reqstack_limit  (int)  maximal number of requests that can be cached
        - reqsdata_perish (timedelta) living time of cached data until they get out of date and purged
        - data            (list) requests response data. contain the request url, time, response status code and content

    Standard workflow (see requests method) :
        (1) check if manager is freeze -> escape workflow
        (2) remove old data from cache (data older than reqsdata_perish)
        (3) check if request url is already present in cache -> escape workflow
        (4) check if the amount of requests in cache is not too large (reqstack_limit) -> escape workflow
        (5) process GET request and extract request time, url and response content, status_code
        (6) reduce content data according to endpoint dependant protocols
        (7) store data

    request contents are stored in the data property that follow a list of dict architecture. dict feature the following key-values :
        - 'req'  -> the url used for request
        - 'time' -> the time at which the request has performed
        - 'resp' -> the status code response
        - 'data' -> the response reduced content, json formated

    """

    def __init__(self, parent=None, token_name = "MMTK", verbose=False, freeze=False, reqstack_limit=60, reqsdata_expire=120, **kwargs) :
        self.parent = parent

        self.verbose = verbose

        self.token_name = token_name
        self.header = {'HTTP-X-APIKEY' : os.environ.get(self.token_name)}
        self.base_url = "https://api.metamob.fr"
        self.endpoints = {
            'users'         : '/utilisateurs',
            'user'          : '/utilisateurs/{pseudo}',
            'user_monsters' : '/utilisateurs/{pseudo}/monstres',
            'monsters'      : '/monstres',
            'monster'       : '/monstres/{id}',
            'servers'       : '/serveurs',
            'server'        : '/serveurs/{id}',
            'kralas'        : '/kralamoures',
            'krala'         : '/kralamoures/{id}',
            'areas'         : '/zones',
            'subareas'      : '/souszones'
        }

        self.freeze = freeze
        self.reqstack_limit = reqstack_limit
        self.reqsdata_perish = datetime.timedelta(seconds=reqsdata_expire)
        self.data = []
        if self.verbose == False : self.speak = self._mute
        self.__post_init__()

    def __post_init__(self) :
        pass

    def __str__(self) :
        now = datetime.datetime.now()
        result = " --- METAMOB API --- "
        result += "\n\t"+"url".ljust(60)+"t".rjust(7)+"resp".rjust(8)+"size".rjust(8)
        for i in self.data :
            dt = now-i['time']
            if dt > self.reqsdata_perish : dt = 'expired'
            else : dt = dt.seconds
            size = len(i['data'])
            result += f"\n\t{i['req']:<60}{dt:>7}{i['resp']:>8}{size:>8}"
        return result

    def get_reqstack_limit(self) :
        """return the max number of requests responses that are stored"""
        return self.reqstack_limit
    def can_handle_requests_stack(self, number) :
        """true if the given number of requests would not raise 903"""
        return len(self.data)+number <= self.reqstack_limit

    def reload_token(self, token_name) :
        """reload metamob api token from environnemental variables"""
        self.token_name = token_name
        self.header = {'HTTP-X-APIKEY' : os.environ.get(self.token_name)}

    def freeze(self) :
        """freeze the metamob api object"""
        self.freeze = True
    def defreeze(self) :
        """defreeze the metamob api object"""
        self.freeze = False

    ### EXTRACT DATA FROM STORAGE ###
    def get_data(self) :
        """return the stored data"""
        return self.data
    def get_user_monsters_data(self, pseudo) :
        """return the response data corresponding to a user_monsters request of specified pseudo"""
        result = []
        req = self.endpoints['user_monsters'].format(pseudo=pseudo)
        for item in self.data :
            if req in item['req'] : result.append( item['data'] )
        return result
    def get_krala_data(self) :
        """return the response data corresponding to all krala calendar request"""
        result = []
        for item in self.data :
            if self.endpoints['kralas'] in item['req'] : result.append(item['data'])
        return result
    def get_monster_data(self) :
        """return the response data conrresponding to monsters request"""
        result = []
        for item in self.data :
            if self.endpoints['monsters'] in item['req'] :result.append(item['data'])
        return result

    ### VERBOSITY ###
    def _mute(self,*args,**kargs) :
        pass
    def speak(self, chain) :
        print(f"MTM_API >>> {chain}")

    ### DATA CLEANER ###
    def reduce_user_monsters_data(self,response_content) :
        """take the content of a user_monsters GET request and reformat it"""
        length = len(response_content)
        for index in range(length-1,-1,-1) :
            obj = response_content[index]
            if obj['recherche'] + obj['propose'] == "00" :
                del response_content[index]
        self.speak(f"reducing data from {length} to {len(response_content)}")
        return response_content
    def reduce_user_data(self, response_content) :
        """take the content of a user GET request and reformat it"""
        return response_content
    def reduce_kralas_data(self, response_content) :
        """"take the content of a krala GET request and reformat it"""
        return response_content
    def reduce_monsters_data(self, response_content):
        """take the content of a monsters GET request and reformat it"""
        for item in response_content :
            del item['zone']
            del item['type']
            del item['id']
        return response_content

    def reduce_content(self, response_content, data_type) :
        """redirect a GET request response content to its appropriate protocol for formating"""
        if data_type == 'users' : return response_content
        if data_type == 'user' : return self.reduce_user_data(response_content)
        if data_type == 'user_monsters' : return self.reduce_user_monsters_data(response_content)
        if data_type == 'monsters' : return self.reduce_monsters_data(response_content)
        if data_type == 'monster' : return response_content
        if data_type == 'servers' : return response_content
        if data_type == 'server' : return response_content
        if data_type == 'kralas' : return self.reduce_kralas_data(response_content)
        if data_type == 'krala' : return response_content
        if data_type == 'areas' : return response_content
        if data_type == 'subareas' : return response_content
        return response_content

    ### CORE REQUEST ###
    def purge_old_requests(self) :
        """remove from data property all request data considered as expired"""
        self.speak(f"purging old request among {len(self.data)} cached requests")
        now = datetime.datetime.now()
        for index in range(len(self.data)-1,-1,-1) :
            time = self.data[index]['time']
            dtime = now-time
            if dtime>self.reqsdata_perish : del self.data[index]
        self.speak(f"purging done, {len(self.data)} request left cached")
    def is_api_overloaded(self) :
        """True if number of stored data are over reqstack_limit, False instead"""
        if len(self.data) >= self.reqstack_limit :
            self.speak(f"number of cached requests is {len(self.data)} and hit limit {self.reqstack_limit} : api overloaded")
            return True
        else :
            self.speak(f"number of cached requests is {len(self.data)} and is below limit of {self.reqstack_limit} : running")
            return False
    def is_request_cached(self,url_req) :
        """True if the asked request is already present in data"""
        for r in self.data :
            if url_req == r['req'] :
                self.speak(f"{url_req} found in cache")
                return True
        self.speak(f"{url_req} not found in cache")
        return False
    def requests(self, endpoint, filter="", pseudo=None, id=None) :
        """
        return the response status code (int) or one of the following custom status code (int) :
            - 901 > API manager has been freezed
            - 902 > the asked request has been found in cache
            - 903 > the API is overloaded and might get a 429 'Too Many Requests' response

        status code 9xx bypass GET request to the API.
        when a GET request is performed, then store the response in data property.
        """
        if self.freeze : return 901
        self.purge_old_requests()
        url_req = self.endpoints[endpoint].format(pseudo=pseudo, id=id) + filter
        if self.is_request_cached(url_req) : return 902
        if self.is_api_overloaded() : return 903
        url = self.base_url+url_req
        self.speak(f"addressing metamob API with GET {url}")
        response = requests.get(url, headers=self.header)
        self.speak(f"metamob responses with status {response.status_code}")
        reqtime = datetime.datetime.now()
        if response.ok  :
            content = json.loads(response.content.decode('utf-8'))
            content = self.reduce_content(content,data_type = endpoint)
            self.speak(f"content of length {len(content)} added to cache, bound on time {reqtime}")
        else :
            content = []
        self.data.append( {'req':url_req, 'time':reqtime, 'resp':response.status_code, 'data':content} )
        self.speak("END")
        return response.status_code

    ### SHORTCUT ###
    def fetch_user(self, pseudo) :
        """ shortcut to user info request """
        self.speak(f"START _ get user info for {pseudo}")
        return self.requests('user',pseudo=pseudo)
    def fetch_user_monsters(self, pseudo, filter="?type=archimonstre") :
        """ shortcut to user monster request """
        self.speak(f"START _ get user monsters for {pseudo}")
        return self.requests('user_monsters',filter=filter,pseudo=pseudo)
    def fetch_krala(self, server) :
        """ shortcut to krala request """
        self.speak(f"START _ get krala calendar on {server}")
        return self.requests('kralas',filter=f"?serveur={server}")
    def fetch_monsters(self, filter="?type=archimonstre") :
        """ shortcut to monsters request"""
        self.speak(f"START _ get monsters")
        return self.requests('monsters', filter = filter)


if __name__ == "__main__" :
    import time

    api = Metamob_API(0, verbose=True, reqstack_limit=60, reqsdata_expire=70)

    if api.can_handle_requests_stack(4) :
        resp = api.fetch_monsters()
        resp = api.fetch_krala(server="")
        resp = api.fetch_user_monsters(pseudo="Garfunk")
        resp = api.fetch_user(pseudo="Garfunk")

    print(api)


# END
