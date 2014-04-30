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
    $scope.changeLevel= (level)->
      $scope.level = level
      promise = $http.post(api + 'change-level/', { level: level })

      promise.success (data)->
        $scope.level = data.level
        $scope.description = data.description

                                  ###########
                                  # On load #
                                  ###########

    # Get user's level
    $scope.getLevel()
