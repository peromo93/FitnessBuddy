(function () {
    'use strict';

    angular
        .module('fitnessbuddy.users.directives', [])
        .directive('pwMatch', pwMatch);


    function pwMatch() {
        return {
            require: 'ngModel',
            link: function(scope, elem, attrs, ngModel) {
                var password1 = '#' +  attrs.pwMatch;
                elem.add(password1).on('keyup', function() {
                    scope.$apply(function() {
                        var valid = ( elem.val() === $(password1).val() );
                        ngModel.$setValidity('pwmatch', valid);
                    });
                });
            },
        };
    }


})();
