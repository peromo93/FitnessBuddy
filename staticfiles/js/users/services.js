(function () {
    'use strict';

    angular
        .module('fitnessbuddy.users.services', [
            'angular-jwt',
        ])
        .service('Users', Users);

    /* Users service */
    Users.$inject = ['$http', '$rootScope', '$location', 'jwtHelper', 'authManager'];
    function Users($http, $rootScope, $location, jwtHelper, authManager) {
        this.register = function(username, password) {

            // POST to registration API endpoint
            return $http.post('/api/users/create/', {
                username: username,
                password: password,
            });
        };

        // POST to token getter API endpoint
        this.login = function(username, password) {
            return $http.post('/api/users/token-auth/', {
                username: username,
                password: password,
            });
        };

        this.getProfile = function() {
            return $http.get('/api/users/' + $rootScope.user + '/');
        };

        this.updateProfile = function(calories, fat, carb, protein, is_public) {
            return $http.put('/api/users/' + $rootScope.user + '/', {
                goal_calories: calories,
                goal_fat: fat,
                goal_carbs: carb,
                goal_protein: protein,
                is_public: is_public,
            });
        };

        // unauthenticate the user and clear any token and username
        // redirect to home page
        this.logout = function() {
            authManager.unauthenticate();
            localStorage.removeItem('token');
            localStorage.removeItem('username');
            $rootScope.user = 'Guest';
            $location.url('/');
        };

        // verify that a token is valid and redirect to dashboard
        // use localStorage to store token and username
        this.tokenAuthentication = function(tokenString) {
            try {
                var token = jwtHelper.decodeToken(tokenString);
                localStorage.setItem('token', tokenString);
                localStorage.setItem('username', token.username);
                $rootScope.user = token.username;
                authManager.authenticate();
                $location.url('/dashboard');
            }
            catch (e) { // this shouldn't happen - clear any token and username
                localStorage.removeItem('token');
                localStorage.removeItem('username');
                $rootScope.user = 'Guest';

                return {'token': [e]}; // return error
            }
        }
    }

})();
