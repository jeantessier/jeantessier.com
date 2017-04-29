angular

    .module("myApp")

    .controller("myCtrl", ["$scope", function($scope) {
        $scope.converter = new Showdown.converter();
        $scope.textarea = "# Title";
        $scope.markdown = function() {
            return $scope.converter.makeHtml($scope.textarea);
        };
    }]);
