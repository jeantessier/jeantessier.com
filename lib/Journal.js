angular

  .module('journalApp', ['ngSanitize'])

  .constant('BACKEND_URL', 'Journal_json.cgi')

  .controller('JournalCtrl', ['JournalModel', JournalModel => {
    var journal = this

    journal.title = 'My Journal'

    JournalModel.all().then(result => {
      journal.title = result.title
      journal.entries = result.entries
    })
  }])

  .service('JournalModel', ['$http', '$log', '$q', 'BACKEND_URL', ($http, $log, $q, BACKEND_URL) => {
    var service = this

    service.all = () => {
      $log.info('Calling ' + BACKEND_URL)

      var deferred = $q.defer()

      $http.get(BACKEND_URL)
        .then(response => {
          service.title = response.data.title
          service.entries = response.data.entries
          deferred.resolve(service)
        })
        .catch(deferred.reject)

      return deferred.promise
    }
  }])
