import frappe
from .search_function_experimental_adv import search
from ..doctype import Doctype

# Intelligent search adv
def activity_search_helper(args):
    searchKey = args.get("query")
    search_result = search(searchKey)
    # return search_result
    response = []
    if search_result:
        for activity_group_name in search_result:
                response.append({"business_activity_group_name": activity_group_name})
    return response