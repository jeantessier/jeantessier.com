angular

    .module("journalApp", ["ngSanitize"])

    .constant("BACKEND_URL", "Journal.json")

    .controller("JournalCtrl", ["$scope", "JournalModel", function($scope, JournalModel) {
        const journal = this

        const converter = new showdown.Converter({
            emoji: 'true',
            ghCodeBlocks: 'true',
            openLinksInNewWindow: 'true',
            splitAdjacentBlockquotes: 'true',
            strikethrough: 'true',
            tables: 'true',
        })
        $scope.markdown = text => converter.makeHtml(text)

        journal.title = "My Journal"

        JournalModel.all().then(result => {
            journal.title = result.title
            journal.entries = result.entries
        })
    }])

    .service("JournalModel", ["$http", "$log", "$q", "BACKEND_URL", function($http, $log, $q, BACKEND_URL) {
        const service = this

        service.all = () => {
            $log.info("Calling " + BACKEND_URL)

            const deferred = $q.defer()

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
