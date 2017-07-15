(function () {
    'use strict';

    angular
        .module('fitnessbuddy.users.services', [])
        .service('Users', Users);

    Users.$inject = ['$http'];
    function Users($http) {
        this.register = function(username, password) {
            return $http.post('/api/users/create/', {
                username: username,
                password: password,
            });
        };

        this.login = function(username, password) {
            return $http.post('/api/users/token-auth/', {
                username: username,
                password: password,
            });
        };
    }

})();
