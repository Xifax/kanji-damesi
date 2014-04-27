(function() {
  'use strict';
  describe('Controller: UserCtrl', function() {
    var UserCtrl, scope;
    beforeEach(module('clientApp'));
    UserCtrl = {};
    scope = {};
    beforeEach(inject(function($controller, $rootScope) {
      scope = $rootScope.$new();
      return UserCtrl = $controller('UserCtrl', {
        $scope: scope
      });
    }));
    return it('should attach a list of awesomeThings to the scope', function() {
      return expect(scope.awesomeThings.length).toBe(3);
    });
  });

}).call(this);

/*
//@ sourceMappingURL=user.js.map
*/