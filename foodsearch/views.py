# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests
from FitnessBuddy.secrets import NDB_API_KEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from foodsearch.serializers import FoodSearchQuerySerializer, FoodSerializer
from django.core.cache import cache


# Create your views here.
class FoodSearchQuery(APIView):
    """
    Query USDA NDB Search API for search results
    URL parameters required are:
        q - food search terms
        ds - data source (Standard Reference or Branded Food Products)
        page - page number to request
    """

    def get(self, request, format=None):
        search_terms = request.query_params.get('q')
        data_source = request.query_params.get('ds')
        page = request.query_params.get('page')
        max_items = 50

        # validate data source
        if data_source not in ['standard', 'branded']:
            return Response('Must provide parameters ds parameter as \'standard\' or \'branded\'.',
                            status=status.HTTP_400_BAD_REQUEST)

        # validate page
        if not page or not page.isdigit():
            return Response('Page must be provided as an integer.',
                            status=status.HTTP_400_BAD_REQUEST)

        if search_terms:
            cached_response = cache.get('list/?q=%s&ds=%s&page=%s' %
                                        (search_terms, data_source, page))

            if cached_response:  # cache hit
                search_serializer = FoodSearchQuerySerializer(cached_response)
                return Response(search_serializer.data)

            else:  # cache miss
                ds = 'Standard Reference' if data_source == 'standard' else 'Branded Food Products'
                r = requests.get('https://api.nal.usda.gov/ndb/search',
                                 {'q': search_terms, 'ds': ds,
                                  'max': max_items, 'offset': (int(page)*max_items),
                                  'format': 'json', 'api_key': NDB_API_KEY})
                if r.status_code == requests.codes.ok:
                    results_dict = json.loads(r.text).get('list')
                    cache.set('list/?q=%s&ds=%s&page=%s' %
                              (search_terms, data_source, page), results_dict)

                    search_serializer = FoodSearchQuerySerializer(results_dict)
                    return Response(search_serializer.data)

        return Response('Must provide parameters q, ds, and page.',
                        status=status.HTTP_400_BAD_REQUEST)


class FoodDetail(APIView):
    """
    Query USDA NDB Food Reports v1 API for a specific food
    URL parameters required are:
        ndbno - USDA NDB food number
    """

    # calories, total fat, saturated fat, poly fat, mono fat,
    # total carbohydrates, dietary fiber, sugar, protein
    nutrient_id_list = ['208', '204', '606', '646', '645', '205', '291', '269', '203']

    def get(self, request, format=None):
        ndbno = request.query_params.get('ndbno')

        # check if all digits but use string for query
        # since ndbno may have leading 0s
        if ndbno and ndbno.isdigit():
            cached_response = cache.get('detail/?ndbno=%s' % ndbno)

            if cached_response:  # cache hit
                food_serializer = FoodSerializer(cached_response)
                return Response(food_serializer.data)

            else:  # cache miss
                r = requests.get('https://api.nal.usda.gov/ndb/reports',
                                 {'ndbno': ndbno, 'type': 'b',
                                  'format': 'json', 'api_key': NDB_API_KEY})
                if r.status_code == requests.codes.ok:
                    results_dict = json.loads(r.text).get('report').get('food')

                    # include only nutrients that are in the id list above
                    results_dict['nutrients'] = [nutrient for nutrient
                                                 in results_dict.get('nutrients')
                                                 if nutrient.get('nutrient_id')
                                                 in self.nutrient_id_list]

                    cache.set('detail/?ndbno=%s' % ndbno, results_dict)
                    food_serializer = FoodSerializer(results_dict)
                    return Response(food_serializer.data)

        return Response('Must provide ndbno for the desired food.',
                        status=status.HTTP_400_BAD_REQUEST)
