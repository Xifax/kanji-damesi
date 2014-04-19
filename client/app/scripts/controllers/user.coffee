'use strict'

angular.module('clientApp')
  .controller 'UserCtrl', ($scope) ->
    $scope.awesomeThings = [
      'HTML5 Boilerplate'
      'AngularJS'
      'Karma'
    ]

    $scope.test = false
    console.log($scope.test)
