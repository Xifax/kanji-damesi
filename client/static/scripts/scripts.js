(function(){"use strict";angular.module("clientApp",[])}).call(this),function(){"use strict";angular.module("clientApp").controller("MainCtrl",["$scope",function(a){return a.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"]}])}.call(this),function(){"use strict";angular.module("clientApp").controller("QuizCtrl",["$scope","$http",function(a,b){var c,d,e,f,g,h,i;for(c="/saiban/api/",a.currentKanji={front:"?",radicals:[{front:"?"}]},a.quiz={readings:{kun:"?",on:"?",nanori:"?"},meanings:"?",examples:"?",answer:"?"},a.timer={began:0,answered:0},a.kanjiLog=[],a.groupsSeen=[],a.activeGroup={kanji:[]},i=1;5>=i;i++)a.activeGroup.kanji.push({front:"?"});return a.loading=!1,d=function(a){return console.log(a)},f=function(a){return console.log(a?"Correct!":"Wrong!")},g=function(b){return"?"!==a.activeGroup.kanji[0].front&&a.groupsSeen.push(a.activeGroup),a.activeGroup=b.group,a.currentKanji={front:"?",radicals:[{front:"?"}]},a.quiz=b.quiz},h=function(){return a.loading=!0},e=function(){return a.loading=!1},a.getRandomGroup=function(){var a;return h(),a=b.get(c+"random-group"),a.success(function(a){return g(a),e()}),a.error(function(a){return d(a),e()})},a.getNextGroup=function(){var a;return h(),a=b.get(c+"next-group/"),a.success(function(a){return g(a),e()}),a.error(function(a){return d(a),e()})},a.answerWith=function(i){var j,k;return h(),j=i.front===a.quiz.answer.front,f(j),k=b.post(c+"answer/",{correct:j,delay:10,kanji:a.quiz.answer.front}),k.success(function(b){return a.kanjiLog.push({answered:i,answer:a.quiz.answer,correct:j,toggled:!1}),g(b),e()}),k.error(function(a){return d(a),e()})},a.skipQuestion=function(a){var f;return h(),f=b.post(c+"skip/",{kanji:a}),f.success(function(a){return g(a),e()}),f.error(function(a){return d(a),e()})},a.zoomKanji=function(b){return a.currentKanji=b},a.toggleLogItemInfo=function(a){return a.toggled=!a.toggled},a.getNextGroup()}]),angular.module("clientApp").filter("reverse",function(){return function(a){return a.slice().reverse()}})}.call(this),function(){"use strict";angular.module("clientApp").controller("UserCtrl",["$scope",function(a){return a.awesomeThings=["HTML5 Boilerplate","AngularJS","Karma"]}])}.call(this);