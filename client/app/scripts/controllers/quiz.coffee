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
    # TODO: also include radical decomposition
    $scope.currentKanji = '?'
    $scope.quiz = {
        # TODO: ponder, if shoud use 'meaning' or array of 'meanings' and so on
        readings: 'さかん, うつくし.い, かがや.き, ゴウ, キョウ, オウ',
        meanings: 'flourishing, successful, beautiful, vigorous',
        examples: 'にっぽんではえいごきょういくがさかんである',
    }
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
    $scope.loading = false

    #######
    # API #
    #######

    # Get random group
    $scope.getRandomGroup = ->
        $scope.loading = true
        promise = $http.get(api + 'random-group')

        promise.success (data)->
            # Add previous group to log & set new active group
            $scope.groupsSeen.push($scope.activeGroup)
            $scope.activeGroup = data
            $scope.currentKanji = '?'
            $scope.loading = false

        promise.error (data)->
            fail(data)
            $scope.loading = false

    # Get scheduled group
    $scope.getNextGroup = ->
        promise = $http.get(api + 'next-group')

    # Answer with kanji
    $scope.answerWith = (kanji) ->
        promise = $http.post(api + 'answer')

    # Skip this kanji
    $scope.skipQuestion = (kanji) ->
        promise = $http.post(api + 'skip')

    # Zoom kanji (and components) on hover
    $scope.zoomKanji = (kanji) ->
        $scope.currentKanji = kanji.front
