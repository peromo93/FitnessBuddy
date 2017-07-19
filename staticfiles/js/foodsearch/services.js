(function () {
    'use strict';

    angular
        .module('fitnessbuddy.foodsearch.services', [])
        .service('FoodSearch', FoodSearch);

    /* Users service */
    FoodSearch.$inject = ['$http', '$location'];
    function FoodSearch($http, $location) {

        // GET request to food search API endpoint
        this.getList = function(foodName, dataSource, page) {
            return $http.get('/api/search/list/', {
                skipAuthorization: true,
                params: {
                    q: foodName,
                    ds: dataSource,
                    page: page,
                },
            });
        };

        // GET request to food detail API endpoint
        this.getDetail = function(ndbno) {
            return $http.get('/api/search/detail/', {
                skipAuthorization: true,
                params: {
                    ndbno: ndbno,
                },
            });
        };
    }

})();
