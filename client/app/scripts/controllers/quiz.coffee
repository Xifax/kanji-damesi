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

    # Timer status
    $scope.timerActive = true

    # Session stats
    $scope.session =
      correct: 0
      wrong: 0
      total: 0
      answerExp: 0
      totalExp: 0
      averageTime: 0
      totalTime: 0

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

      # Update session and profile
      if ($scope.profile.experience != 0) and (data.profile.experience != 0)
        $scope.session.answerExp = data.profile.experience - $scope.profile.experience
      $scope.session.totalExp += $scope.session.answerExp

      $scope.profile = data.profile


      # Start timer
      if $scope.timerActive
        $scope.$broadcast('timer-start')
      else
        $scope.ponderingTime = 0

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

      $scope.selectedKanji = kanji
      start()

      # Check answer
      correct = kanji.front == $scope.quiz.answer.front

      # Display notification
      # TODO: calculate experience on client!
      got_it(correct)

      if correct
        $scope.session.correct += 1
      else
        $scope.session.wrong += 1
      $scope.session.total += 1

      $scope.session.averageTime = $scope.session.totalTime / $scope.session.total

      promise = $http.post(api + 'answer/',
        {'correct': correct,
        'delay': $scope.ponderingTime,
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
    $scope.toggleLogItemInfo = (item) ->
      item.toggled  = !item.toggled
      # Pause timer if item info is toggled
      if item.toggled
        $scope.timerActive = false
        $scope.$broadcast('timer-stop')
      # Check all the items in kanjiLog
      else
        if ($scope.kanjiLog.every (item) -> not item.toggled)
          $scope.timerActive = true
          $scope.$broadcast('timer-resume')

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

    # Pause/resume timer
    $scope.pauseResumeTimer = () ->
      if $scope.timerActive
        $scope.$broadcast('timer-stop')
      else
        $scope.$broadcast('timer-resume')

      $scope.timerActive = !$scope.timerActive


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
      (event, data) =>
        $scope.ponderingTime = data.millis
        $scope.session.totalTime += data.millis
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

