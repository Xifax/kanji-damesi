'use strict'

angular.module('clientApp')
  .controller 'QuizCtrl', ($scope, $http, $document, $timeout, $hotkey) ->

                                    ########
                                    # Init #
                                    ########

    # Basic settings and utils
    api = '/saiban/api/'

    # Visiblitiy status
    $scope.show =
      # Info sections
      bigKanji: true,
      example:  false,
      groupKey:  true,
      stats:  true,
      # Notifications
      ok: false,
      no: false,

    # Session stats
    $scope.session =
      correct: 0
      wrong: 0
      total: 0
      experience: 0

    # Timer
    $scope.ponderingTime = 0

    # Global stats
    $scope.profile =
      streak: 0
      experience: 0
      level: 0
      points: 1
      multiplier: 100


    # Init models and data
    $scope.currentKanji =
      front: '?',
      radicals: [front: '?']

    # Selected answer
    $scope.selectedKanji = {}
    $scope.skippedKanji = false

    $scope.quiz =
      readings:
        kun: '?',
        on: '?',
        nanori: '?',
        examples: ['?'],
      meanings: '?',
      answer: '?'

    $scope.timer =
      began: 0,
      answered: 0

    $scope.kanjiLog = []
    $scope.logLimit = $scope.baseLimit = 3
    maxLimit = 15

    $scope.groupsSeen = []
    $scope.activeGroup = { kanji: [] }
    # Pre-fill active group with '?'
    $scope.activeGroup.kanji.push({front: '?'}) for [1..5]
    $scope.loading = false

                                   #########
                                   # Utils #
                                   #########

    # Show notification
    flashOverlay = (element) ->
      $scope.show[element] = true

      $timeout(
        () -> $scope.show[element] = false,
        700
      )

    # Show notification on server resopnse
    fail = (message)-> console.log(message)
    success = (message)-> console.log(message)

    # Show answer status
    got_it = (correct)->
      if correct
        flashOverlay('ok')
      else
        flashOverlay('no')

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
      $scope.profile = data.profile

      # Start timer
      $scope.$broadcast('timer-start')

    # Start some time-consuming action
    start = -> $scope.loading = true

    # Finish time-consuming action
    fin = -> $scope.loading = false

    # Update log with answer
    updateLog = (kanji, correct, skipped) ->
        $scope.kanjiLog.push({
          'answered': kanji,
          'answer': $scope.quiz.answer,
          'examples': $scope.quiz.examples,
          'correct': correct,
          'skipped': skipped,
          'toggled': false,
        })

    # Log kanji as skipped
    logAsSkipped = () ->
      updateLog($scope.quiz.answer, false, true)

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
      if $scope.loading
        return

      $scope.$broadcast('timer-stop')
      # console.log($scope.ponderingTime)

      $scope.selectedKanji = kanji
      start()

      # Check answer
      correct = kanji.front == $scope.quiz.answer.front

      # Display notification
      got_it(correct)

      if correct
        $scope.session.correct += 1
      else
        $scope.session.wrong += 1
      $scope.session.total += 1

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
        updateLog(kanji, correct, false)

        # Update current group
        newKanjiGroup(data)
        fin()

      promise.error (data)->
        fail(data)
        fin()

    # Skip this kanji
    $scope.skipQuestion = (kanji) ->
      if $scope.loading
        return

      $scope.skippedKanji = true
      start()
      promise = $http.post(api + 'skip/', {'kanji': kanji.front})

      promise.success (data)->
        # Update kanji log
        logAsSkipped()
        newKanjiGroup(data)
        $scope.skippedKanji = false
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

    # Get exp to next level
    $scope.toNextLevel = () ->
      return ($scope.profile.level + 1) * $scope.profile.multiplier

    # Get progressbar width
    $scope.progressExp = () ->
      width: $scope.profile.experience / $scope.toNextLevel() * 100 + '%'

    # Check if kanji is selected
    $scope.isSelected = (kanji) ->
      $scope.selectedKanji == kanji

    # Get date format based on time length
    $scope.timeFormat = (time) ->
      console.log(time)
      readable = switch time
        when time < 9000 then 'Yep!'
          # return $filter('date')(time, 's.s')
        # when 60 * 1000 > time > 9 * 1000 then return 'ss.s'
        # when time > 60 * 1000 then return 'm:ss'
        else 'What'

      console.log(readable)

                                  ###########
                                  # Hotkeys #
                                  ###########


    # Answer with keys
    [1..5].map (key) ->
      $hotkey.bind("#{key}", (event) =>
        $scope.answerWith($scope.activeGroup.kanji[key - 1])
      )

    # Skip with 'S
    $hotkey.bind("S", (event) =>
      $scope.skipQuestion($scope.quiz.answer)
    )

                                   #########
                                   # Timer #
                                   #########

    # Update timer when finished answering
    $scope.$on(
      'timer-stopped',
      (event, data) => $scope.ponderingTime = data.millis
    )

    # $scope.$on(
    #   'timer-tick',
    #   (event, data) =>
    #     $scope.ponderingTime = data.millis
    # )



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

