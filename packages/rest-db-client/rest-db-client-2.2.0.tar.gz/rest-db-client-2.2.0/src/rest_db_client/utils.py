from datetime import datetime, timedelta


# depreciated
def isoformat(object):
    return to_isoformat(object)


def to_isoformat(object):
    if isinstance(object, datetime):
        return object.strftime("%Y-%m-%dT%H:%M:%S.%f")
    else:
        raise NotImplementedError


def from_isoformat(string):
    dt, _, us = string.partition(".")
    dt = datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z")) if us else 0
    return dt + timedelta(microseconds=us)


def delete_domain(client, domain):
    """Deletes a domain and all models within it.

    :param domain: name of the domain.
    :rtype: bool
    """
    return client.drop(domain)


def delete_model(client, domain, model):
    """Deletes a model of a domain.

    :param domain: Name of the domain.
    :param model: Name of the model.
    :rtype: bool
    """
    domain = client[domain]
    return domain.drop(model)


def delete_datasets(client, domain, model, filter=None):
    domain = client[domain]
    model = domain[model]
    return model.delete(filter)


def load_datasets(
        client, domain, model, filter=None, fields=None, sort=None,
        limit=None, page=None, pagesize=None):
    """Loads datasets from a domain model.

    :param domain: Name of the domain.
    :param model: Name of the model.
    :param filter: Filter to apply. Set to ``None`` to match all.
    :param fields: (optional) Dataset fields to be returned.
    :param sort: (optional) Specify sorting of datasets.
    :param limit: (optional) Restrict the number of returned datasets.
    :param page: (optional) Define which page to return.
    :param pagesize: (optional) Define the size of a page.
    :rtype: list of dicts
    """
    domain = client[domain]
    model = domain[model]
    datasets = model.find(filter, fields, sort, limit, page, pagesize)
    return datasets


def save_datasets(client, domain, model, datasets):
    """Saves datasets into a domain model.

    :param domain: Name of the domain.
    :param model: Name of the model.
    :param datasets: List of dicts.
    :param replace: (optional) If ``True``, the model will be cleared first.
    :rtype: bool
    """
    domain = client[domain]
    model = domain[model]
    return model.insert(datasets)


def save_dataframe(client, domain, model, df, datetime_fields=None):
    """Saves a dataframe into a domain model.

    :param domain: Name of the domain.
    :param model: Name of the model.
    :param df: A Pandas dataframe.
    :param replace: (optional) If ``True``, the model will be cleared first.
    :rtype: bool
    """
    domain = client[domain]
    model = domain[model]
    if datetime_fields:
        if not isinstance(datetime_fields, list):
            datetime_fields = [datetime_fields]
        for datetime_field in datetime_fields:
            df[datetime_field] = df[datetime_field].apply(
                lambda x: isoformat(x))
    return model.insert_df(df)


def load_dataframe(
        client, domain, model, filter=None, fields=None, sort=None,
        limit=None, page=None, pagesize=None, datetime_fields=None):
    """Loads a dataframe from a domain model.

    :param domain: Name of the domain.
    :param model: Name of the model.
    :param filter: Filter to apply. Set to ``None`` to match all.
    :param fields: (optional) Dataset fields to be returned.
    :param sort: (optional) Specify sorting of datasets.
    :param limit: (optional) Restrict the number of returned datasets.
    :param page: (optional) Define which page to return.
    :param pagesize: (optional) Define the size of a page.
    :rtype: dataframe
    """
    import pandas as pd
    datasets = load_datasets(
        client, domain, model, filter, fields, sort, limit, page, pagesize)
    df = pd.DataFrame(datasets)
    if not df.empty and datetime_fields:
        if not isinstance(datetime_fields, list):
            datetime_fields = [datetime_fields]
        for datetime_field in datetime_fields:
            df[datetime_field] = pd.to_datetime(df[datetime_field])
    return df
