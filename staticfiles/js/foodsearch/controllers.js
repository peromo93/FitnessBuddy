(function () {
    'use strict';

    angular
        .module('fitnessbuddy.foodsearch.controllers', [])
        .controller('ListController', ListController);

    /* Food list controller */
    ListController.$inject = ['FoodSearch'];
    function ListController(FoodSearch) {
        var vm = this;

        vm.performSearch = function() {
            FoodSearch.getList(vm.foodName, vm.dataSource, 0)
                .then(
                    function(response, status, headers, config) { // success
                        vm.errors = null;
                        vm.searchResults = response.data.item;
                    },
                    function(response, status, headers, config) { // error
                        vm.searchResults = null;
                        vm.errors = ['No search results.'];
                    }
                );
        };

        vm.foodDetail = function(ndbno) {
            FoodSearch.getDetail(ndbno)
                .then(
                    function(response, status, headers, config) { // success
                        console.log(response.data);
                    },
                    function(response, status, headers, config) { // error
                        console.log('oops');
                    }
                );
        };
    }

})();
