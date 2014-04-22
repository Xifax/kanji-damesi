'use strict'

angular.module('clientApp')
  .controller 'QuizCtrl', ($scope, $http) ->
    $scope.awesomeThings = [
      'HTML5 Boilerplate'
      'AngularJS'
      'Karma'
    ]

    api = '/saiban/api/'

    $scope.groups = []
    $scope.activeGroup = {}
    #     kanji: [
    #         {front: '托'},
    #         {front: '瑚'},
    #         {front: '珊'},
    #         {front: '醐'},
    #         {front: '醍'}
    #     ]
    # }

    $scope.getNextGroup = ->
        $scope.groups.push($scope.activeGroup)
        # $scope.activeGroup = {} # get from api

        promise = $http.get(api + 'next-group')

        promise.success (data)->
            console.log(data)
            $scope.activeGroup.kanji = data


    $scope.answerWith = (kanji) ->
        # select kanji and send to api
        $scope.test = ''
