# -*- coding: utf-8 -*-
from plone import api
from rer.sitesearch.interfaces import IRERSiteSearchSettings
from zope.component import getMultiAdapter
from zope.component import ComponentLookupError
from rer.sitesearch.interfaces import ISiteSearchCustomFilters
from zope.globalrequest import getRequest

import logging

logger = logging.getLogger(__name__)


def get_types_groups():
    values = api.portal.get_registry_record(
        "types_grouping", interface=IRERSiteSearchSettings, default=[]
    )
    if not values:
        return {}
    res = {"order": [], "values": {}}
    portal = api.portal.get()
    request = getRequest()
    for value in values:
        label = _extract_label(value.get("label", ""))
        res["order"].append(label)
        res["values"][label] = {"types": value.get("types", []), "count": 0}
        advanced_filters = value.get("advanced_filters", "")
        icon = value.get("icon", "")
        if icon:
            res["values"][label]["icon"] = icon
        if advanced_filters:
            try:
                adapter = getMultiAdapter(
                    (portal, request),
                    ISiteSearchCustomFilters,
                    name=advanced_filters,
                )
                res["values"][label]["advanced_filters"] = adapter()
            except ComponentLookupError:
                logger.error(
                    'Unable to get adapter "{}"'.format(advanced_filters)
                )
    return res


def get_indexes_mapping():
    values = api.portal.get_registry_record(
        "available_indexes", interface=IRERSiteSearchSettings, default=[]
    )
    if not values:
        return {}
    res = {"order": [], "values": {}}
    for value in values:
        label = _extract_label(value.get("label", ""))
        index = value.get("index", "")
        res["order"].append(index)
        res["values"][index] = {"label": label, "values": {}}
    return res


def _extract_label(value):
    string_value = ""
    if len(value) == 1:
        string_value = value[0]
    else:
        current_lang = api.portal.get_current_language()
        string_value = ""
        for option in value:
            lang, label = option.split("|")
            if lang and lang == current_lang:
                string_value = label
                break
    return string_value
