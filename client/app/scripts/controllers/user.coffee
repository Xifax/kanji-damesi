'use strict'

angular.module('clientApp')
  .controller 'UserCtrl', ($scope) ->

                                    ########
                                    # Init #
                                    ########

    # Basic settings and utils
    api = '/saiban/api/'

    # Study level
    $scope.level = 1

    # $scope.getLevel = (user) ->
    #   console.log(user)

    # Update level
    $scope.changeLevel= (level)->
      $scope.level = level
      console.log('test')
      # TODO: update style
      # promise = $http.post(api + 'change-level/', { level: level })

      # promise.success (data)->
      #   console.log(data)

      # promise.error (data)->
      #   console.log(data
