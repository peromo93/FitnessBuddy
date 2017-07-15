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
                }
            });

            $httpProvider.interceptors.push('jwtInterceptor');
        }

        /* App run */
        run.$inject = ['$rootScope', 'authManager'];
        function run($rootScope, authManager) {

            // check auth token on refresh and update current user
            authManager.checkAuthOnRefresh();
            if(!authManager.isAuthenticated()) {
                $rootScope.user = 'Guest';
            }
            else {
                $rootScope.user = localStorage.getItem('username');
            }
        }

})();
