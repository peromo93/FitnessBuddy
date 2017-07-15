(function () {
    'use strict';

    angular
        .module('fitnessbuddy.users.controllers', [
            'angular-jwt',
        ])
        .controller('RegisterController', RegisterController)
        .controller('LoginController', LoginController)
        .controller('LogoutController', LogoutController);

    /* Registration controller */
    RegisterController.$inject = ['Users'];
    function RegisterController(Users) {
        var vm = this;

        // try to register the user
        // on success, log user in
        // on failure, display errors from response
        vm.register = function() {
            Users.register(vm.username, vm.password1)
                .then(
                    function(response, status, headers, config) { // success
                        Users.login(vm.username, vm.password1)
                            .then(
                                function(response, status, headers, config) { // success
                                    vm.errors = Users.tokenAuthentication(response.data.token);
                                },
                                function(response, status, headers, config) { // error
                                    vm.errors = response.data;
                                }
                            );
                    },
                    function(response, status, headers, config) { // error
                        vm.errors = response.data;
                    }
                );
        };
    }

    /* Login controller */
    LoginController.$inject = ['Users'];
    function LoginController(Users) {
        var vm = this;

        // try to log user in
        // on success, redirect to dashboard
        // on failure, display errors from the response
        vm.login = function() {
            Users.login(vm.username, vm.password)
                .then(
                    function(response, status, headers, config) { // success
                        vm.errors = Users.tokenAuthentication(response.data.token);
                    },
                    function(response, status, headers, config) { // error
                        vm.errors = response.data;
                    }
                );
        };
    }

    /* Logout controller */
    LogoutController.$inject = ['Users'];
    function LogoutController(Users) {
        Users.logout();
    }

})();
