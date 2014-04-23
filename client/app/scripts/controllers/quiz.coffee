'use strict'

angular.module('clientApp')
  .controller 'QuizCtrl', ($scope, $http) ->

    ########
    # Init #
    ########

    # Basic settings and utils
    api = '/saiban/api/'

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
            {front: '?'},
            {front: '?'},
            {front: '?'},
            {front: '?'},
            {front: '?'}
            # Examples #
            # {front: '托'},
            # {front: '瑚'},
            # {front: '珊'},
            # {front: '醐'},
            # {front: '醍'}
        ]
    }
    $scope.loading = false

    #########
    # Utils #
    #########

    # Show notification
    fail = (message)->
        console.log(message)

    # Set new kanji group
    newKanjiGroup = (data) ->
        $scope.groupsSeen.push($scope.activeGroup)
        $scope.activeGroup = data
        $scope.currentKanji = '?'

    # Start some time-consuming action
    start = ->
        $scope.loading = true

    # Finish time-consuming action
    fin = ->
        $scope.loading = false

    #######
    # API #
    #######

    # Get random group
    $scope.getRandomGroup = ->
        start()
        promise = $http.get(api + 'random-group')

        promise.success (data)->
            # Add previous group to log & set new active group
            newKanjiGroup(data)
            fin()

        promise.error (data)->
            fail(data)
            fin()

    # Get scheduled group
    # TODO: implement
    $scope.getNextGroup = ->
        promise = $http.get(api + 'next-group/')

    # Answer with kanji
    # TODO: implement
    $scope.answerWith = (kanji) ->
        promise = $http.put(api + 'answer/')

    # Skip this kanji
    $scope.skipQuestion = (kanji) ->
        start()
        promise = $http.put(api + 'skip/')

        promise.success (data)->
            newKanjiGroup(data)
            fin()

        promise.error (data)->
            fail(data)
            fin()

    # Zoom kanji (and components) on hover
    $scope.zoomKanji = (kanji) ->
        $scope.currentKanji = kanji.front

    ###########
    # On load #
    ###########

    # Get new group on load
    $scope.getRandomGroup()

