(function () {
    'use strict';

    angular
        .module('fitnessbuddy.routes', [
            'ngRoute',
        ])
        .config(config);

        config.$inject = ['$routeProvider', '$locationProvider'];

        function config($routeProvider, $locationProvider) {

            $locationProvider.html5Mode(true).hashPrefix('!');

            $routeProvider

            .when('/', {
                templateUrl: 'static/templates/index.html',
            })

            .when('/login', {
                templateUrl: 'static/templates/login.html',
            })

            .when('/register', {
                templateUrl: 'static/templates/register.html',
            })

            .when('/search', {
                templateUrl: 'static/templates/search.html',
            });

        }

})();
