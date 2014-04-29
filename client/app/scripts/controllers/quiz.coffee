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
    $scope.currentKanji =
      front: '?',
      radicals: [front: '?']

    $scope.quiz =
      # TODO: ponder, if shoud use 'meaning' or array of 'meanings' and so on
      readings:
        kun: '?',
        on: '?',
        namae: '?',
      meanings: '?',
      examples: '?',
      answer: '?'
      # examples: 'にっぽんではえいごきょういくがさかんである',

    $scope.timer =
      began: 0,
      answered: 0

    $scope.kanjiLog = []
    $scope.groupsSeen = []
    $scope.activeGroup = { kanji: [] }
    $scope.loading = false
    # Pre-fill active group with '?'
    $scope.activeGroup.kanji.push({front: '?'}) for [1..5]

                                   #########
                                   # Utils #
                                   #########

    # Show notification
    fail = (message)-> console.log(message)

    # Show answer status
    got_it = (correct)->
      if correct
        console.log('Correct!')
      else
        console.log('Wrong!')

    # Set new kanji group
    newKanjiGroup = (data) ->
      if $scope.activeGroup.kanji[0].front != '?'
        $scope.groupsSeen.push($scope.activeGroup)

      $scope.activeGroup = data.group
      $scope.currentKanji = {front: '?', radicals: [front: '?']}
      $scope.quiz = data.quiz

    # Start some time-consuming action
    start = -> $scope.loading = true

    # Finish time-consuming action
    fin = -> $scope.loading = false

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
    $scope.getNextGroup = ->
      start()
      promise = $http.get(api + 'next-group/')

      promise.success (data)->
        newKanjiGroup(data)
        fin()

      promise.error (data)->
        fail(data)
        fin()

    # Answer with kanji
    $scope.answerWith = (kanji) ->
      start()
      # Check answer
      correct = kanji.front == $scope.quiz.answer
      got_it(correct)

      promise = $http.post(api + 'answer/',
        {'correct': correct,
        # TODO: measure time for an answer
        'delay': 10,
        'kanji': $scope.quiz.answer}
      )

      promise.success (data)->
        # TODO: notify on success/failure
        newKanjiGroup(data)
        fin()

      promise.error (data)->
        fail(data)
        fin()

    # Skip this kanji
    $scope.skipQuestion = (kanji) ->
      start()
      promise = $http.post(api + 'skip/', {'kanji': kanji})

      promise.success (data)->
        newKanjiGroup(data)
        fin()

      promise.error (data)->
        fail(data)
        fin()

    # Zoom kanji (and components) on hover
    $scope.zoomKanji = (kanji) -> $scope.currentKanji = kanji
    # TODO: Zoom radical

                                  ###########
                                  # On load #
                                  ###########

    # Get new group on load
    # $scope.getRandomGroup()
    $scope.getNextGroup()

