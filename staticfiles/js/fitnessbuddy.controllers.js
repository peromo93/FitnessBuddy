(function () {
    'use strict';

    angular
        .module('fitnessbuddy.controllers', [])
        .controller('NavigationController', NavigationController);

    /* Navigation controller */
    NavigationController.$inject = ['$location', '$scope'];
    function NavigationController($location, $scope) {

        // keep track of what page we are on
        // each time we change routes update location switches
        $scope.$on('$routeChangeSuccess', function() {
            $scope.isDashboard = $location.path() === '/dashboard';
            $scope.isCalendar  = $location.path() === '/calendar';
            $scope.isFoodLog   = $location.path() === '/foodlog';
            $scope.isWeightLog = $location.path() === '/weightlog';
            $scope.isProfile   = $location.path() === '/profile';
            $scope.isLogin     = $location.path() === '/login';
            $scope.isRegister  = $location.path() === '/register';
            $scope.isSearch    = $location.path() === '/search';
        });

    }

})();
