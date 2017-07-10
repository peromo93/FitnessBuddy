import md5
import json
import datetime
import requests
from FitnessBuddy.secrets import NDB_API_KEY
from users.models import Profile
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.core.cache import cache

# calories, total fat, saturated fat, poly fat, mono fat,
# total carbohydrates, dietary fiber, sugar, protein
nutrient_id_list = ['208', '204', '606', '646', '645',
                    '205', '291', '269', '203']

# FoodEntry model variable names
nutrient_name_list = ['calories', 'tfa', 'sfa', 'pufa', 'mufa',
                      'carb', 'fiber', 'sugar', 'protein']

# maps nutrient id -> (FoodEntry variable name)
nutrient_lookup = {
    '208': 'calories',  '204': 'tfa',       '606': 'sfa',
    '646': 'pufa',      '645': 'mufa',      '205': 'carb',
    '291': 'fiber',     '269': 'sugar',     '203': 'protein'
}


def safe_cache_key(value):
    """
    Replaces invalid memcache control characters with an underscore.
    Returns an md5 hexdigest of value if len(value) > 250.
    """

    for char in value:
        if ord(char) < 33:
            value = value.replace(char, '_')

    if len(value) <= 250:
        return value

    return md5.new(value).hexdigest()


def parse_date_from_url(kwargs):
    """
    Parse and validate a date from URL kwargs or 404
    """

    month = kwargs.get('month')
    day = kwargs.get('day')
    year = kwargs.get('year')

    try:
        date = datetime.date(month=int(month), day=int(day), year=int(year))
    except ValueError:
        raise Http404

    return date


def get_profile_from_url(kwargs):
        """
        Try to get profile from URL kwargs or 404
        """

        username = kwargs.get('username')
        if username:
            return get_object_or_404(Profile, user__username=username)
        else:
            raise Http404


def get_food_report(ndbno):
    """
    Return a food report given a valid ndbno. This function will check the
    cache for the food report. If the food report doesn't exist in the
    cache, query USDA NDB API and add food report to cache.
    Is food report for given ndbno is not found, return None.
    """

    key = safe_cache_key('detail/?ndbno=%s' % ndbno)
    food_report = cache.get(key)

    if food_report:  # cache hit
        return food_report
    else:  # cache miss
        r = requests.get('https://api.nal.usda.gov/ndb/reports',
                         {'ndbno': ndbno, 'type': 'b',
                          'format': 'json', 'api_key': NDB_API_KEY})
        if r.status_code == requests.codes.ok:
            food_report = json.loads(r.text).get('report').get('food')

            # include only nutrients that are in the id list above
            food_report['nutrients'] = [nutrient for nutrient
                                        in food_report.get('nutrients')
                                        if nutrient.get('nutrient_id')
                                        in nutrient_id_list]

            cache.set(key, food_report)
            return food_report


def get_search_results(search_terms, data_source, page, max_items):
    """
    Return a search results given search terms, data source, page,
    and maximum number of search results. This function will check the
    cache for the search query. If the search doesn't exist in the
    cache, query USDA NDB API and add search results to cache.
    If search is unsuccesful, return None.
    """

    key = safe_cache_key(
        'list/?q=%s&ds=%s&page=%s' % (search_terms, data_source, page))
    search_results = cache.get(key)

    if search_results:  # cache hit
        return search_results
    else:  # cache miss
        if data_source == 'standard':  # determine "ds" parameter for USDA API
            data_source = 'Standard Reference'
        elif data_source == 'branded':
            data_source = 'Branded Food Products'
        else:
            data_source = None

        r = requests.get('https://api.nal.usda.gov/ndb/search',
                         {'q': search_terms, 'ds': data_source,
                          'max': max_items, 'offset': (int(page)*max_items),
                          'format': 'json', 'api_key': NDB_API_KEY})
        if r.status_code == requests.codes.ok:
            search_results = json.loads(r.text).get('list')
            cache.set(key, search_results)
            return search_results
