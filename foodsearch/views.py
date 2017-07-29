# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from FitnessBuddy.helper import get_food_report, get_search_results
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from foodsearch.serializers import FoodSearchQuerySerializer, FoodTransformSerializer


# Create your views here.
class FoodSearchQuery(APIView):
    """
    Query USDA NDB Search API for search results
    URL parameters required are:
        q - food search terms
        ds - data source (standard, branded, or both)
        page - page number to request
    """

    def get(self, request, format=None):
        search_terms = request.query_params.get('q')
        data_source = request.query_params.get('ds')
        page = request.query_params.get('page')
        max_items = 50

        # validate data source
        if data_source not in ['standard', 'branded', 'both']:
            return Response(
                'Must provide "ds" parameter as "standard", "branded", or "both".',
                status=status.HTTP_400_BAD_REQUEST)

        # validate page
        if not page or not page.isdigit():
            return Response(
                '"page" parameter must be provided as an integer.',
                status=status.HTTP_400_BAD_REQUEST)

        # validate search terms
        if not search_terms:
            return Response(
                'Must provide search terms with "q" parameter.',
                status=status.HTTP_400_BAD_REQUEST)

        result = get_search_results(search_terms, data_source, page, max_items)

        if result:
            search_serializer = FoodSearchQuerySerializer(result)
            return Response(search_serializer.data)

        return Response(
            'Must provide parameters "q", "ds", and "page".',
            status=status.HTTP_400_BAD_REQUEST)


class FoodDetail(APIView):
    """
    Query USDA NDB Food Reports v1 API for a specific food
    URL parameters required are:
        ndbno - USDA NDB food number
    """

    def get(self, request, format=None):
        ndbno = request.query_params.get('ndbno')

        # ndbno must be not None and contain only digits
        if not ndbno or not ndbno.isdigit():
            return Response(
                'Parameter "ndbno" must be provided as a string of only digits.',
                status=status.HTTP_400_BAD_REQUEST)

        food_report = get_food_report(ndbno)

        if food_report:
            food_serializer = FoodTransformSerializer(food_report)
            return Response(food_serializer.data)

        return Response(
            'Must provide valid "ndbno" parameter for the desired food.',
            status=status.HTTP_400_BAD_REQUEST)
