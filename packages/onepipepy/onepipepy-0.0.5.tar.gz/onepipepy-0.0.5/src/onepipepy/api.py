import requests
from .models import *


class SearchAPI(object):
    def __init__(self, api):
        self._api = api

    def search_items(self, term, **kwargs):
        get_params = dict()
        for field in ["item_types", "fields", "search_for_related_items", "exact_match", "include_fields", "start",
                      "limit"]:
            if kwargs.get(field):
                get_params[field] = kwargs.get(field)
        url = "/itemSearch"
        get_params["term"] = term
        search_result = Search(**self._api._get(url, get_params))
        return search_result.get(kwargs.get("item_types"))


class DealAPI(object):
    def __init__(self, api):
        self._api = api
        self.url = "/deals"

    def add_deal(self, title, *args, **kwargs):
        url = self.url
        data = kwargs.get("data", dict())
        data["title"] = title
        return Deal(**self._api._post(url=url, data=data))

    def update_deal(self, id, *args, **kwargs):
        url = "/%s/%s" % (self.url, str(id))
        return Deal(**self._api._put(url=url, data=kwargs.get("data")))

    def get_deal_by_id(self, id, *args, **kwargs):
        url = "/%s/%s" % (self.url, str(id))
        return Deal(**self._api._get(url))


class ActivitesAPI(object):
    def __init__(self, api):
        self._api = api
        self.url = "/activites"

    def add_activity(self, deal_id, **kwargs):
        url = self.url
        data = kwargs.get("data", dict())
        data["deal_id"] = deal_id
        return Activites(**self._api._post(url=url, data=data))


class API(object):
    def __init__(self, *args, **kwargs):
        self.pd_key = dict(
            api_token=args[0]
        )
        self._api_prefix = "https://api.pipedrive.com/v1"
        self.headers = {'Content-Type': 'application/json'}

        self.search = SearchAPI(self)
        self.deal = DealAPI(self)
        self.activity = ActivitesAPI(self)

    def _action(self, req):
        try:
            j = req.json()
        except ValueError as e:
            j = {"error": str(e)}
        return j

    def _get(self, url, params=None):
        """Wrapper around request.get() to use the API prefix. Returns a JSON response."""
        if params is None:
            params = {}
        req = requests.get(self._api_prefix + url, params={**self.pd_key, **params})
        return self._action(req)

    def _post(self, url, data={}, **kwargs):
        """Wrapper around request.post() to use the API prefix. Returns a JSON response."""
        req = requests.post(
            self._api_prefix + url + "?api_token=%s" % str(self.pd_key["api_token"]),
            data=data,
            **kwargs
        )
        return self._action(req)

    def _put(self, url, data={}):
        """Wrapper around request.put() to use the API prefix. Returns a JSON response."""
        req = requests.put(
            self._api_prefix + url + "?api_token=%s" % str(self.pd_key["api_token"]),
            data=data
        )
        return self._action(req)

    def _delete(self, url):
        """Wrapper around request.delete() to use the API prefix. Returns a JSON response."""
        req = requests.delete(self._api_prefix + url + "?api_token=%s" % str(self.pd_key["api_token"]))
        return self._action(req)
