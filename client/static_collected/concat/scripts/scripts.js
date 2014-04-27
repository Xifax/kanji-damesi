(function () {
  'use strict';
  angular.module('clientApp', []);
}.call(this));
/*
//@ sourceMappingURL=app.js.map
*/
(function () {
  'use strict';
  angular.module('clientApp').controller('MainCtrl', [
    '$scope',
    function ($scope) {
      return $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];
    }
  ]);
}.call(this));
/*
//@ sourceMappingURL=main.js.map
*/
(function () {
  'use strict';
  angular.module('clientApp').controller('QuizCtrl', [
    '$scope',
    '$http',
    function ($scope, $http) {
      var api, fail, fin, got_it, newKanjiGroup, start, _i;
      api = '/saiban/api/';
      $scope.currentKanji = {
        front: '?',
        radicals: [{ front: '?' }]
      };
      $scope.quiz = {
        readings: '\u3055\u304b\u3093, \u3046\u3064\u304f\u3057.\u3044, \u304b\u304c\u3084.\u304d, \u30b4\u30a6, \u30ad\u30e7\u30a6, \u30aa\u30a6',
        meanings: 'flourishing, successful, beautiful, vigorous',
        examples: '\u306b\u3063\u307d\u3093\u3067\u306f\u3048\u3044\u3054\u304d\u3087\u3046\u3044\u304f\u304c\u3055\u304b\u3093\u3067\u3042\u308b',
        answer: 'kanji'
      };
      $scope.timer = {
        began: 0,
        answered: 0
      };
      $scope.groupsSeen = [];
      $scope.activeGroup = { kanji: [] };
      $scope.loading = false;
      for (_i = 1; _i <= 5; _i++) {
        $scope.activeGroup.kanji.push({ front: '?' });
      }
      fail = function (message) {
        return console.log(message);
      };
      got_it = function (correct) {
        if (correct) {
          return console.log('Correct!');
        } else {
          return console.log('Wrong!');
        }
      };
      newKanjiGroup = function (data) {
        if ($scope.activeGroup.kanji[0].front !== '?') {
          $scope.groupsSeen.push($scope.activeGroup);
        }
        $scope.activeGroup = data.group;
        $scope.currentKanji = {
          front: '?',
          radicals: [{ front: '?' }]
        };
        return $scope.quiz = data.quiz;
      };
      start = function () {
        return $scope.loading = true;
      };
      fin = function () {
        return $scope.loading = false;
      };
      $scope.getRandomGroup = function () {
        var promise;
        start();
        promise = $http.get(api + 'random-group');
        promise.success(function (data) {
          newKanjiGroup(data);
          return fin();
        });
        return promise.error(function (data) {
          fail(data);
          return fin();
        });
      };
      $scope.getNextGroup = function () {
        var promise;
        start();
        promise = $http.get(api + 'next-group/');
        promise.success(function (data) {
          newKanjiGroup(data);
          return fin();
        });
        return promise.error(function (data) {
          fail(data);
          return fin();
        });
      };
      $scope.answerWith = function (kanji) {
        var correct, promise;
        start();
        correct = kanji.front === $scope.quiz.answer;
        got_it(correct);
        promise = $http.post(api + 'answer/', {
          'correct': correct,
          'delay': 10,
          'kanji': $scope.quiz.answer
        });
        promise.success(function (data) {
          newKanjiGroup(data);
          return fin();
        });
        return promise.error(function (data) {
          fail(data);
          return fin();
        });
      };
      $scope.skipQuestion = function (kanji) {
        var promise;
        start();
        promise = $http.post(api + 'skip/', { 'kanji': kanji });
        promise.success(function (data) {
          newKanjiGroup(data);
          return fin();
        });
        return promise.error(function (data) {
          fail(data);
          return fin();
        });
      };
      $scope.zoomKanji = function (kanji) {
        return $scope.currentKanji = kanji;
      };
      return $scope.getNextGroup();
    }
  ]);
}.call(this));
/*
//@ sourceMappingURL=quiz.js.map
*/
(function () {
  'use strict';
  angular.module('clientApp').controller('UserCtrl', [
    '$scope',
    function ($scope) {
      return $scope.awesomeThings = [
        'HTML5 Boilerplate',
        'AngularJS',
        'Karma'
      ];
    }
  ]);
}.call(this));  /*
//@ sourceMappingURL=user.js.map
*/