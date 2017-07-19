(function () {
    'use strict';

    angular
        .module('fitnessbuddy.users.controllers', [
            'angular-jwt',
        ])
        .controller('RegisterController', RegisterController)
        .controller('LoginController', LoginController)
        .controller('ProfileController', ProfileController)
        .controller('SettingsController', SettingsController)
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
                                    vm.errors = Users.tokenAuthentication(response.data.token, 'dashboard');
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
                        vm.errors = Users.tokenAuthentication(response.data.token, 'dashboard');
                    },
                    function(response, status, headers, config) { // error
                        vm.errors = response.data;
                    }
                );
        };
    }

    /* Update profile controller */
    ProfileController.$inject = ['Users'];
    function ProfileController(Users) {
        var vm = this;

        Users.getProfile()
            .then(
                function(response, status, headers, config) { // success
                    vm.calories = response.data.goal_calories;
                    vm.fat = response.data.goal_fat.toFixed(2);
                    vm.carb = response.data.goal_carbs.toFixed(2);
                    vm.protein = response.data.goal_protein.toFixed(2);
                    vm.is_public = response.data.is_public;
                },
                function(response, status, headers, config) { // error
                    console.log('epic fail');
                }
            );

        vm.updateProfile = function() {
            Users.updateProfile(vm.calories, vm.fat, vm.carb, vm.protein, vm.is_public)
                .then(
                    function(response, status, headers, config) { // success
                        vm.success = 'Profile updated successfully!';
                    },
                    function(response, status, headers, config) { // error
                        vm.errors = response.data;
                    }
                );
        }
    }

    /* Update settings controller */
    SettingsController.$inject = ['$rootScope', 'Users'];
    function SettingsController($rootScope, Users) {
        var vm = this;
        vm.username = $rootScope.user;

        vm.updateSettings = function() {
            Users.updateSettings(vm.username, vm.password1)
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

    /* Logout controller */
    LogoutController.$inject = ['Users'];
    function LogoutController(Users) {
        Users.logout();
    }

})();
