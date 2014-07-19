'use strict'

angular.module('clientApp')
  .controller 'UserCtrl', ($scope, $http) ->

                                    ########
                                    # Init #
                                    ########

    # Basic settings and utils
    api = '/saiban/api/'

    # Study level
    $scope.level = 0
    $scope.description = ''

    # Get user level and description
    $scope.getLevel = ->
      promise = $http.get(api + 'get-level/')

      promise.success (data)->
        $scope.level = data.level
        $scope.description = data.description

    # Update level
    $scope.changeLevel = (level)->
      $scope.level = level
      promise = $http.post(api + 'change-level/', { level: level })

      promise.success (data)->
        $scope.level = data.level
        $scope.description = data.description

                                 ##############
                                 # Kanji grid #
                                 ##############

    $scope.kanjiStatus = {}

    # Show kanji info
    $scope.showInfo = (kanji) ->
      promise = $http.get("#{api}get-kanji/#{kanji}/")

      promise.success (data) ->
        $scope.kanjiStatus = data
        $('#kanjiInfo').modal('show')

                                  ###########
                                  # On load #
                                  ###########

    # Get user's level
    $scope.getLevel()
