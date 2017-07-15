(function () {
    'use strict';

    angular
        .module('fitnessbuddy.users.controllers', [
            'angular-jwt',
        ])
        .controller('RegisterController', RegisterController)
        .controller('LoginController', LoginController)
        .controller('LogoutController', LogoutController);

    RegisterController.$inject = ['$location', '$scope', 'Users'];
    function RegisterController($location, $scope, Users) {
        var vm = this;

        vm.register = function() {
            Users.register(vm.username, vm.password1)
                .then(function(response, status, headers, config) { // success
                    Users.login(vm.username, vm.password1);
                }, function(response, status, headers, config) { // error
                    vm.errors = response.data;
                });
        };
    }

    LoginController.$inject = ['$location', '$rootScope', 'Users', 'jwtHelper', 'authManager'];
    function LoginController($location, $rootScope, Users, jwtHelper, authManager) {
        var vm = this;

        vm.login = function() {
            Users.login(vm.username, vm.password)
                .then(function(response, status, headers, config) { // success
                    try {
                        var token = jwtHelper.decodeToken(response.data.token);
                        localStorage.setItem('token', response.data.token);
                        localStorage.setItem('username', token.username);
                        $rootScope.user = token.username;
                        authManager.authenticate();
                        $location.url('/');
                    }
                    catch (e) {
                        localStorage.setItem('token', '');
                        localStorage.setItem('username', '');
                        $rootScope.user = 'Guest';
                        vm.errors = {'token': [e]};
                    }
                }, function(response, status, headers, config) { // error
                    vm.errors = response.data;
                });
        };
    }

    LogoutController.$inject = ['$location', '$rootScope', 'authManager'];
    function LogoutController($location, $rootScope, authManager) {
        authManager.unauthenticate();
        localStorage.setItem('token', '');
        localStorage.setItem('username', '');
        $rootScope.user = 'Guest';
        $location.url('/');
    }

})();
