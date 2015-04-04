app.controller('myCtrl', function($scope, $sce) {
    $scope.converter = new Showdown.converter();
    $scope.textarea = "# Title";
    $scope.markdown = function() {
        return $sce.trustAsHtml($scope.converter.makeHtml($scope.textarea));
    };
});
