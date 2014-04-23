'use strict'

angular.module('clientApp')
  .controller 'QuizCtrl', ($scope, $http) ->

    ########
    # Init #
    ########

    # Basic settings and utils
    api = '/saiban/api/'

    # Show notification
    fail = (message)->
        console.log(message)

    # Init models and data
    $scope.groupsSeen = []
    $scope.activeGroup = {
        kanji: [
            {front: '托'},
            {front: '瑚'},
            {front: '珊'},
            {front: '醐'},
            {front: '醍'}
        ]
    }

    #######
    # API #
    #######

    # Get random group
    $scope.getRandomGroup = ->
        promise = $http.get(api + 'random-group')

        promise.success (data)->
            # Add previous group to log & set new active group
            $scope.groupsSeen.push($scope.activeGroup)
            $scope.activeGroup = data

        promise.error (data)->
            fail(data)

    # Get scheduled group
    $scope.getNextGroup = ->
        promise = $http.get(api + 'next-group')

    # Answer with kanji
    $scope.answerWith = (kanji) ->
        promise = $http.post(api + 'answer')
