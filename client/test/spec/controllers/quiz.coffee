'use strict'

describe 'Controller: QuizCtrl', ->

  # load the controller's module
  beforeEach module 'clientApp'

  QuizCtrl = {}
  scope = {}

  # Initialize the controller and a mock scope
  beforeEach inject ($controller, $rootScope) ->
    scope = $rootScope.$new()
    QuizCtrl = $controller 'QuizCtrl', {
      $scope: scope
    }

  it 'should have no seen groups at the start', ->
    expect(scope.groupsSeen.length).toBe 0

  it 'should have pre-filled current kanji and active group', ->
    expect(scope.activeGroup.kanji.length).toBe 5
    expect(scope.currentKanji.front).toBe '?'
    expect(scope.currentKanji.radicals.length).toBe 1

  # it 'should change loader status using start() and fin()', ->
  #   expect(scope.loading).toBe false
  #   QuizCtrl.start()
  #   expect(scope.loading).toBe true
  #   QuizCtrl.start()
  #   expect(scope.loading).toBe false

  # it 'should initialize new kanji group based on data from api', ->
  #   data = {group: 'new_data'}
  #   scope.activeGroup = {group: 'active_data'}
  #   QuizCtrl.newKanjiGroup(data)
  #   expect(scope.groupsSeen).toContain(scope.activeGroup)
  #   expect(scope.activeGroup).toBe data
  #   expect(scope.currentKanji.front).toBe '?'
