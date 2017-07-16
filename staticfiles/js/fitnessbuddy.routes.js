(function () {
    'use strict';

    angular
        .module('fitnessbuddy.routes', [
            'ngRoute',
        ])
        .config(config);

        /* Route configuration */
        config.$inject = ['$routeProvider', '$locationProvider'];
        function config($routeProvider, $locationProvider) {

            $locationProvider.html5Mode(true).hashPrefix('!');

            $routeProvider

            .when('/', {
                templateUrl: 'static/templates/index.html',
            })

            .when('/login', {
                controller: 'LoginController',
                controllerAs: 'vm',
                templateUrl: 'static/templates/login.html',
            })

            .when('/logout', {
                controller: 'LogoutController',
                template: '', //AngularJS requires template to be set
            })

            .when('/register', {
                controller: 'RegisterController',
                controllerAs: 'vm',
                templateUrl: 'static/templates/register.html',
            })

            .when('/profile', {
                controller: 'ProfileController',
                controllerAs: 'vm',
                templateUrl: 'static/templates/profile.html',
                requiresLogin: true,
            })

            .when('/search', {
                templateUrl: 'static/templates/search.html',
            });

        }

})();
