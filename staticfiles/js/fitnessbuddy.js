(function () {
    'use strict';

    angular
        .module('fitnessbuddy', [
            'fitnessbuddy.routes',
            'fitnessbuddy.users',
            'angular-jwt',
        ])
        .config(config)
        .run(run);

        config.$inject = ['$httpProvider', 'jwtOptionsProvider'];
        function config($httpProvider, jwtOptionsProvider) {
            jwtOptionsProvider.config({
                tokenGetter: function() {
                    return localStorage.getItem('token');
                }
            });

            $httpProvider.interceptors.push('jwtInterceptor');
        }

        run.$inject = ['$rootScope', 'authManager'];
        function run($rootScope, authManager) {
            authManager.checkAuthOnRefresh();

            if(!authManager.isAuthenticated()) {
                $rootScope.user = 'Guest';
            }
            else {
                $rootScope.user = localStorage.getItem('username');
            }
        }

})();
