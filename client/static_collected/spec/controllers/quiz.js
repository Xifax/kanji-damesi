(function() {
  'use strict';
  describe('Controller: QuizCtrl', function() {
    var QuizCtrl, scope;
    beforeEach(module('clientApp'));
    QuizCtrl = {};
    scope = {};
    beforeEach(inject(function($controller, $rootScope) {
      scope = $rootScope.$new();
      return QuizCtrl = $controller('QuizCtrl', {
        $scope: scope
      });
    }));
    it('should have no seen groups at the start', function() {
      return expect(scope.groupsSeen.length).toBe(0);
    });
    return it('should have pre-filled current kanji and active group', function() {
      expect(scope.activeGroup.kanji.length).toBe(5);
      expect(scope.currentKanji.front).toBe('?');
      return expect(scope.currentKanji.radicals.length).toBe(1);
    });
  });

}).call(this);

/*
//@ sourceMappingURL=quiz.js.map
*/