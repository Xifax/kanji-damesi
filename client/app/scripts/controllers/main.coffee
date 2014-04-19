'use strict'

angular.module('clientApp')
  .controller 'MainCtrl', ($scope) ->
    $scope.awesomeThings = [
      'HTML5 Boilerplate'
      'AngularJS'
      'Karma'
    ]

    # $scope.login = true
    # $scope.switchMode = ->
    #     $scope.login = !$scope.login
