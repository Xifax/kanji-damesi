'use strict'

angular.module('clientApp')
  .controller 'QuizCtrl', ($scope, $http, $document) ->

                                    ########
                                    # Init #
                                    ########

    # Basic settings and utils
    api = '/saiban/api/'

    # Kanji zoom status
    $scope.showBigKanji = true

    # Session info
    $scope.session =
      correct: 0
      wrong: 0

    # Init models and data
    $scope.currentKanji =
      front: '?',
      radicals: [front: '?']

    $scope.quiz =
      readings:
        kun: '?',
        on: '?',
        nanori: '?',
        examples: ['?'],
      meanings: '?',
      examples: '?',
      answer: '?'

    $scope.timer =
      began: 0,
      answered: 0

    $scope.kanjiLog = []
    $scope.logLimit = $scope.baseLimit = 3
    maxLimit = 15

    # #Fill with test data
    # $scope.kanjiLog.push({
    #   'answered': {'front': '明', 'compounds': [{'front': '明日'}]}
    #   'answer': {'front': '日', 'compounds': [{'front': '明日'}]}
    #   'correct': true
    # })
    # $scope.kanjiLog.push({
    #   'answered': {'front': '数', 'compounds': [{'front': '数学'}]}
    #   'answer': {'front': '学', 'compounds': [{'front': '数学'}]}
    #   'correct': false
    # })
    # $scope.kanjiLog.push({
    #   'answered': {'gloss': 'Number', 'front': '数', 'compounds': [{'front': '数学'}]}
    #   'answer': {'front': '学', 'compounds': [{'front': '数学'}]}
    #   'correct': true
    #   'toggled': true
    # })

    $scope.groupsSeen = []
    $scope.activeGroup = { kanji: [] }
    # Pre-fill active group with '?'
    $scope.activeGroup.kanji.push({front: '?'}) for [1..5]
    $scope.loading = false

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

    # Shuffle elements of array
    shuffle = (array) ->
      m = array.length

      # While there remain elements to shuffle
      while m
        # Pick a remaining element…
        i = Math.floor(Math.random() * m--)

        # And swap it with the current element.
        t = array[m]
        array[m] = array[i]
        array[i] = t

      return array

    # Set new kanji group
    newKanjiGroup = (data) ->
      if $scope.activeGroup.kanji[0].front != '?'
        $scope.groupsSeen.push($scope.activeGroup)

      $scope.activeGroup = data.group
      # Shuffle kanji order
      shuffle($scope.activeGroup.kanji)
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
    # TODO: allow to select by numbers
    $scope.answerWith = (kanji) ->
      start()

      # Check answer
      correct = kanji.front == $scope.quiz.answer.front

      # Display notification
      got_it(correct)

      promise = $http.post(api + 'answer/',
        {'correct': correct,
        # TODO: measure time for an answer
        'delay': 10,
        'kanji': $scope.quiz.answer.front}
      )

      promise.success (data)->
        # Shuffle compounds
        shuffle($scope.quiz.answer.compounds)
        shuffle(kanji.compounds)

        # Update kanji log
        $scope.kanjiLog.push({
          'answered': kanji,
          'answer': $scope.quiz.answer,
          'correct': correct,
          'toggled': false,
          'skipped': false
        })

        # Update current group
        newKanjiGroup(data)
        fin()

      promise.error (data)->
        fail(data)
        fin()

    # Skip this kanji
    $scope.skipQuestion = (kanji) ->
      start()
      promise = $http.post(api + 'skip/', {'kanji': kanji.front})

      promise.success (data)->
        # Update kanji log
        $scope.kanjiLog.push({
          'answered': $scope.quiz.answer,
          'answer': $scope.quiz.answer,
          'toggled': false,
          'correct': false,
          'skipped': true
        })
        newKanjiGroup(data)
        fin()

      promise.error (data)->
        fail(data)
        fin()

    # Zoom kanji (and components) on hover
    $scope.zoomKanji = (kanji) -> $scope.currentKanji = kanji
    # TODO: Zoom radical

    # Show/hide kanji info from log
    $scope.toggleLogItemInfo = (item) -> item.toggled  = !item.toggled

    # Toggle log limit
    $scope.toggleLimit = ->
      if $scope.logLimit == $scope.baseLimit
        $scope.logLimit = maxLimit
      else
        $scope.logLimit = $scope.baseLimit

                                  ###########
                                  # Hotkeys #
                                  ###########

    $document.bind '49', (event) =>
        console.debug(event)


                                  ###########
                                  # On load #
                                  ###########

    # Get new group on load
    $scope.getNextGroup()

                             ######################
                             # Additional filters #
                             ######################

# Reverse array filter
angular.module('clientApp')
  .filter 'reverse', ->
    (items) ->
      items.slice().reverse()
