
from kortical.api import _api, code, data, deployment, experiment_framework, instance, model, superhuman_calibration


def init(url=None, b64_credentials=None, reset_config=False):
    if reset_config:
        _api.reset_config(url, b64_credentials)
    return _api.init(url, b64_credentials)


def get(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.get(url, *args, **kwargs)


def post(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.post(url, *args, **kwargs)


def delete(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.delete(url, *args, **kwargs)


def post_file(url, fields, filename, filepath, *args, description=None, throw=True, **kwargs):
    kwargs['throw'] = throw
    kwargs['description'] = description
    return _api.post_file(url, fields, filename, filepath, *args, **kwargs)
