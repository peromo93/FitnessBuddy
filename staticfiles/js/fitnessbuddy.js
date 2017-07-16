(function () {
    'use strict';

    angular
        .module('fitnessbuddy', [
            'fitnessbuddy.routes',
            'fitnessbuddy.controllers',
            'fitnessbuddy.users',
            'angular-jwt',
        ])
        .config(config)
        .run(run);

        /* App configuration */
        config.$inject = ['$httpProvider', 'jwtOptionsProvider'];
        function config($httpProvider, jwtOptionsProvider) {

            // setup JWT authentication and interceptor
            jwtOptionsProvider.config({
                tokenGetter: function() {
                    return localStorage.getItem('token');
                },
                authPrefix: 'JWT ',
                unauthenticatedRedirectPath: 'login',
            });

            $httpProvider.interceptors.push('jwtInterceptor');
        }

        /* App run */
        run.$inject = ['$rootScope', '$http', 'authManager'];
        function run($rootScope, $http, authManager) {

            // check auth token on refresh and update current user
            authManager.checkAuthOnRefresh();
            if(!authManager.isAuthenticated()) {
                $rootScope.user = 'Guest';
            }
            else {
                $rootScope.user = localStorage.getItem('username');
            }

            // redirect to login when unauthenticated
            authManager.redirectWhenUnauthenticated();

            // setup csrf for Django
            $http.defaults.xsrfHeaderName = 'X-CSRFToken';
            $http.defaults.xsrfCookieName = 'csrftoken';
        }

})();
