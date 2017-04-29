angular

  .module('myApp')

  .controller('myCtrl', ['$scope', $scope => {
    $scope.converter = new Showdown.converter() // eslint-disable-line new-cap, no-undef
    $scope.textarea = '# Title'
    $scope.markdown = () => {
      return $scope.converter.makeHtml($scope.textarea)
    }
  }])
