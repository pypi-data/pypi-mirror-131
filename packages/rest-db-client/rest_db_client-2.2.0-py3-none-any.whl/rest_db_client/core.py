import datetime
import requests


class RestDbClient:

    def __init__(self, host="http://localhost", port=None, url=None):
        if port is None and url is None:
            raise ValueError(
                "You must supply either Host and Port pair or an URL")
        if port and not isinstance(port, int):
            raise TypeError("port must be an instance of int")
        self.url = url if url is not None else "{}:{}".format(host, port)

    def __repr__(self):
        return "RestClient({})".format(self.url)

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(
                "RestClient has no attribute {}. To access the {} domain"
                ", use client[{}].".format(name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        return Domain(self, name)

    def drop(self, domain):
        r = requests.delete(self.url + '/' + domain)
        return 1 if r.status_code == 200 else 0

    def find(self):
        r = requests.get(self.url)
        if r.status_code != 200:
            return None
        return r.json()


class Domain:

    def __init__(self, client, name):
        self.client = client
        self.name = name
        self.url = client.url + '/' + name

    def __repr__(self):
        return "Domain({}, {})".format(self.client, self.name)

    def __getattr__(self, name):
        if name.startswith('_'):
            raise AttributeError(
                "Domain has no attribute {}. To access the {} model, "
                "use domain[{}].".format(name, name, name))
        return self.__getitem__(name)

    def __getitem__(self, name):
        return Model(self, name)

    def drop(self, model):
        r = requests.delete(self.url + '/' + model)
        return 1 if r.status_code == 200 else 0

    def find(self):
        r = requests.get(self.url)
        if r.status_code != 200:
            return None
        return r.json()


class Model:

    def __init__(self, domain, name):
        self.domain = domain
        self.name = name
        self.url = domain.url + '/' + name

    def __repr__(self):
        return "Model({}, {})".format(self.domain, self.name)

    def __getitem__(self, _id):
        if not isinstance(_id, str):
            raise ValueError("index must be an instance of str")
        r = requests.get(self.url + '/' + _id)
        if r.status_code != 200:
            return None
        return r.json()

    def insert(self, datasets):
        """Inserts a single dataset or a list of datasets. A dataset is
        a Python dictionary."""
        if not isinstance(datasets, list):
            datasets = [datasets]
        r = requests.post(self.url, json=datasets)
        if r.status_code == 201:
            return r.json().get('count')
        else:
            return 0

    def insert_df(self, dataframe):
        """Inserts a Pandas dataframe."""
        return self.insert(dataframe.to_dict(orient='records'))

    def find(
            self, filter=None, fields=None, sort=None, limit=None, page=None,
            pagesize=None):
        """Returns datasets from the model.

        :param filter: Filter to apply. Can be set to ``None`` to match all.
        :param fields: (optional) Dataset fields to be returned.
        :param sort: (optional) Specify sorting of datasets.
        :param limit: (optional) Restrict the number of returned datasets.
        :param page: (optional) Define which page to return.
        :param pagesize: (optional) Define the size of a page.
        :rtype: list of dicts
        """
        # filtering
        _filter = _parse_filter(filter)

        # projection
        _fields = ""
        if fields:
            if not isinstance(fields, list):
                raise ValueError('fields must be an instance of list')
            values = ','.join(fields)
            _fields = '_fields={}'.format(values)

        # sorting
        _sort = ""
        if sort:
            if not isinstance(sort, list):
                sort = [sort]
            values = ','.join(sort)
            _sort = '_sort={}'.format(values)

        # limiting and paging
        _limit = ""
        _page = ""
        _pagesize = ""
        if limit:
            _limit = "_limit={}".format(limit)
        elif page:
            _page = "_page={}".format(page)
            if pagesize:
                _pagesize = "_pagesize={}".format(pagesize)

        # build the query string
        query = ""
        if _filter:
            query += _filter + '&'
        if _fields:
            query += _fields + '&'
        if _sort:
            query += _sort + '&'
        if _page:
            query += _page + '&'
        if _pagesize:
            query += _pagesize + '&'
        if _limit:
            query += _limit + '&'

        if query:
            query = '?' + query
        if query.endswith('&'):
            query = query[:-1]

        r = requests.get(self.url + query)
        if r.status_code != 200:
            return None
        return r.json()

    def replace(self, _id, dataset):
        """Replaces the dataset that matches given ``_id`` with the
        new dataset."""
        if isinstance(dataset, list):
            dataset = dataset[0]
        for key, value in dataset.items():
            if isinstance(value, datetime.date):
                dataset[key] = value.isoformat()
        try:
            r = requests.put(self.url + '/' + str(_id), json=dataset)
        except Exception:
            return 0
        if r.status_code == 200:
            return r.json().get('count')
        else:
            return 0

    def modify(self, _id, dataset):
        """Modifies (updates) the dataset that matches given ``_id`` with
        the new dataset fields."""
        if isinstance(dataset, list):
            dataset = dataset[0]
        for key, value in dataset.items():
            if isinstance(value, datetime.date):
                dataset[key] = value.isoformat()
        try:
            r = requests.patch(self.url + '/' + str(_id), json=dataset)
        except Exception:
            return 0
        if r.status_code == 200:
            return r.json().get('count')
        else:
            return 0

    def delete(self, filter=None):
        """Deletes datasets from the model.

        :param filter: Filter to apply. Set to ``None`` to match all.
        :rtype: bool
        """
        # filtering
        _filter = _parse_filter(filter)
        # build the query string
        query = ""
        if _filter:
            query = '?' + _filter
        r = requests.delete(self.url + query)
        if r.status_code == 200:
            return r.json().get('count')
        else:
            return 0


def _parse_filter(filter):
    _filter = ""
    if filter:
        if not isinstance(filter, dict):
            raise ValueError('filter must be an instance of dict')
        for key, value in filter.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    if not isinstance(v, list):
                        value = "{}:{}".format(k, v)
                    else:
                        v = str(v)[1:-1]
                        v = v.replace(" ", "")  # remove spaces
                        v = v.replace("'", "")  # remove quotes
                        value = "{}:{}".format(k, v)
                    _filter += "{}={}&".format(key, value)
            elif isinstance(value, list):
                _value = str(value)[1:-1]
                value = _value.replace(" ", "")
                _filter += "{}={}&".format(key, value)
            else:
                value = str(value)
                _filter += "{}={}&".format(key, value)
        if _filter.endswith('&'):
            _filter = _filter[:-1]
    return _filter
