# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import requests
from FitnessBuddy.secrets import NDB_API_KEY
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from foodsearch.serializers import FoodSearchQuerySerializer, FoodSerializer


# Create your views here.
class FoodSearchQuery(APIView):
    """
    Query USDA NDB Search API for search results
    URL parameters required are:
        q - food search terms
        ds - data source (Standard Reference or Branded Food Products)
        max - maximum number of items to return
        offset - beginning row in the result set to begin
    """

    def get(self, request, format=None):
        search_terms = request.query_params.get('q')
        data_source = request.query_params.get('ds')
        max_items = request.query_params.get('max')
        offset = request.query_params.get('offset')

        if search_terms and data_source and max_items and offset:
            r = requests.get('https://api.nal.usda.gov/ndb/search',
                             {'q': search_terms, 'ds': data_source,
                              'max': max_items, 'offset': offset,
                              'format': 'json', 'api_key': NDB_API_KEY})
            if r.status_code == requests.codes.ok:
                results_dict = json.loads(r.text).get('list')
                search_serializer = FoodSearchQuerySerializer(results_dict)
                return Response(search_serializer.data)

        return Response('Must provide parameters q, ds, max, and offset.',
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

        if ndbno:
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

                food_serializer = FoodSerializer(results_dict)
                return Response(food_serializer.data)

        return Response('Must provide ndbno for the desired food.',
                        status=status.HTTP_400_BAD_REQUEST)
