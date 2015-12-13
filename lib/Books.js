angular

    .module("booksApp", ["ngResource"])

    .filter("sanitize", ['$sce', function($sce) {
        return function(htmlCode) {
            return $sce.trustAsHtml(htmlCode);
        }
    }])

    .controller("BooksCtrl", ['BooksModel', function(BooksModel) {
        var books = this;

        books.title = "Readings";

        BooksModel.all().then(function(result) {
            books.title = result.title;
            books.books = result.books;
        });
    }])

    .service("BooksModel", ['$http', '$log', '$q', 'BACKEND_URL', function($http, $log, $q, BACKEND_URL) {
        var service = this;

        service.all = function() {
            $log.info("Calling " + BACKEND_URL);

            var deferred = $q.defer();

            $http.get(BACKEND_URL)
                    .success(function(data, status, headers, config) {
                        $log.info("success data");
                        $log.info(data);
                        service.title = data.title;
                        service.books = data.books;
                        deferred.resolve(service);
                    })
                    .error(deferred.reject);

            return deferred.promise;
        };
    }]);
