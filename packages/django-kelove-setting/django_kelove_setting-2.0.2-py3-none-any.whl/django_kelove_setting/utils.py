"""
utils.py
By IT小强xqitw.cn <mail@xqitw.cn>
At 1/29/21 10:46 AM
"""
from django.apps import apps
from django.conf import settings

from . import load_object, KELOVE_SETTINGS_APP_KEY
from .setting_forms import Settings as SettingsForm


def get_settings_form_class(form_class):
    """
    根据表单标识获取表单配置类
    :param form_class:
    :return:
    """

    if isinstance(form_class, str):
        try:
            form = load_object(form_class)
        except (ModuleNotFoundError, AttributeError):
            form = None
    else:
        form = form_class

    if not issubclass(form, SettingsForm):
        form = None
    return form


def get_all_settings_form(load_form=True):
    """
    获取所有配置表单类
    :param load_form: 是否加载类
    :return:
    """
    app_configs = apps.get_app_configs()
    kelove_settings = [
        j
        for i in app_configs
        for j in getattr(i, KELOVE_SETTINGS_APP_KEY, [])
        if hasattr(i, KELOVE_SETTINGS_APP_KEY)
    ]
    kelove_settings += [i for i in getattr(settings, 'KELOVE_SETTINGS_CLASSES', [])]
    kelove_settings = list(set(kelove_settings))
    if not load_form:
        return kelove_settings
    kelove_settings_form_set = []
    for kelove_setting in kelove_settings:
        _form = get_settings_form_class(form_class=kelove_setting)
        if not _form:
            continue
        kelove_settings_form_set.append(_form)
    return list(kelove_settings_form_set)
