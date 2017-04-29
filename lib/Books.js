angular

  .module('booksApp', ['ngSanitize'])

  .controller('BooksCtrl', ['BooksModel', BooksModel => {
    var books = this

    books.title = 'Readings'

    BooksModel.all().then(result => {
      books.title = result.title
      books.books = result.books
    })
  }])

  .service('BooksModel', ['$http', '$log', '$q', 'BACKEND_URL', ($http, $log, $q, BACKEND_URL) => {
    var service = this

    service.all = () => {
      $log.info('Calling ' + BACKEND_URL)

      var deferred = $q.defer()

      $http.get(BACKEND_URL)
        .then(response => {
          $log.info('success data')
          $log.info(response.data)
          service.title = response.data.title
          service.books = response.data.books
          deferred.resolve(service)
        })
        .catch(deferred.reject)

      return deferred.promise
    }
  }])
