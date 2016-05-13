//
// This query returns all books, similar to Books_json.cgi's output.
//
db.book.aggregate([
    {$unwind: "$reviews"},
    {$lookup: {
        from: "review",
        localField: "reviews",
        foreignField: "_id",
        as: "review"
    }},
    {$unwind: "$review"},
    {$project: {
        _id: false,
        name: true,
        authors: true,
        titles: true,
        publisher: true,
        years: true,
        start: "$review.start",
        stop: "$review.stop",
        body: "$review.body"
    }},
    {$sort: {start: -1}}
]);

//
// This is an alternative that includes unwanted fields such as "_id" and may be less efficient.
//
db.book.find({}, {_id: false}).map(function(book) {
    var review = db.review.findOne({_id: {$in: book.reviews}});
    book.start = review.start;
    book.stop = review.stop;
    book.body = review.body;
    return book;
});

//
// This index will be useful when looking up books by name.
//
db.book.createIndex({name: 1}, {name: "idx_name", unique: true});

//
// This query performs a search for one book by name and replicates the format of Books_json.cgi.
//
var name = "Sex_at_Dawn"
db.book.aggregate([
    {$match: {name: name}},
    {$unwind: "$reviews"},
    {$lookup: {
        from: "review",
        localField: "reviews",
        foreignField: "_id",
        as: "review"
    }},
    {$unwind: "$review"},
    {$project: {
        _id: false,
        name: true,
        authors: true,
        titles: true,
        publisher: true,
        years: true,
        start: "$review.start",
        stop: "$review.stop",
        body: "$review.body"
    }}
]);
