angular

    .module("journalApp", ["ngSanitize"])

    .constant("BACKEND_URL", "Journal_json.cgi")

    .controller("JournalCtrl", ["JournalModel", function(JournalModel) {
        var journal = this;

        journal.title = "My Journal";

        JournalModel.all().then(function(result) {
            journal.title = result.title;
            journal.entries = result.entries;
        });
    }])

    .service("JournalModel", ["$http", "$log", "$q", "BACKEND_URL", function($http, $log, $q, BACKEND_URL) {
        var service = this;

        service.all = function() {
            $log.info("Calling " + BACKEND_URL);

            var deferred = $q.defer();

            $http.get(BACKEND_URL)
                    .success(function(data, status, headers, config) {
                        service.title = data.title;
                        service.entries = data.entries;
                        deferred.resolve(service);
                    })
                    .error(deferred.reject);

            return deferred.promise;
        };
    }]);
