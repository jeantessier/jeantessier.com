#!/usr/bin/perl

require './lib/wiki_json.pl';

$DIRNAME = "data";

if ($0 =~ /(\w+)_mongo\./) {
    $DOCUMENT = $1;
}

print &DocumentAsMongo($DOCUMENT);

sub DocumentAsMongo {
    local ($document) = @_;

    return &DocumentPartsAsMongo($document) . "\n";
}

sub DocumentPartsAsMongo {
    local ($document) = @_;

    opendir(DIRHANDLE, $DIRNAME);
    local (@files) = grep { /^${document}_\d{4}-\d{2}-\d{2}.txt$/ } readdir(DIRHANDLE);
    closedir(DIRHANDLE);

    local ($user_stmt) = "var jean = db.users.findOne(" . &JsonRecord(email => &JsonText("jean\@jeantessier.com")) . ");";
    local ($clear_user_stmt) = "db.users.updateOne(" . &JsonRecord("_id" => "jean._id") . "," . &JsonRecord("\$unset" => &JsonRecord(reviews => &JsonText(""))) . ");";
    local ($drop_stmt) = join("\n", "db.books.drop();", "db.reviews.drop();");
    local (@book_stmts) = map { &DocumentPartAsMongo("$DIRNAME/$_") } reverse sort @files;

    return join("\n\n", $user_stmt, $clear_user_stmt, $drop_stmt, @book_stmts);
}

sub DocumentPartAsMongo {
    local ($filename) = @_;

    open(FILEHANDLE, $filename);
    local (@lines) = <FILEHANDLE>;
    close(FILEHANDLE);

    local (%meta_data, @titles, @authors, @years);

    do {
        $line = shift(@lines);
        chomp $line;

        if ($line =~ /(\w+):\s*(.*)/) {
            local ($key, $value) = ($1, $2);

            if ($key eq "title") {
                push @titles, $value;
            } elsif ($key eq "author") {
                push @authors, $value;
            } elsif ($key eq "year") {
                push @years, $value;
            } else {
                $meta_data{$key} = $value;
            }
        }
    } until ($line =~ /^\s*$/);

    local ($book_stmt) = "var book = db.books.insertOne(" .
        &JsonRecord(
            name => &JsonText($meta_data{"name"}),
            authors => &JsonList(map { &JsonText($_) } @authors),
            titles => &JsonList(map {
                if (/\[\[([^\]]*)\]\[_(.*)_\]\]/) {
                    &JsonRecord(
                        title => &JsonText($2),
                        link => &JsonText($1),
                    );
                } elsif (/\[\[([^\]]*)\]\[(.*)\]\]/) {
                    &JsonRecord(
                        title => &JsonText($2),
                        link => &JsonText($1),
                    );
                } else {
                    &JsonRecord(
                        title => &JsonText($_),
                        link => "null",
                    );
                }
            } @titles),
            publisher => &JsonText($meta_data{"publisher"}),
            years => &JsonList(map { &JsonText($_) } @years),
            reviews => &JsonList(),
        ) . ");";

    local ($review_stmt) = "var review = db.reviews.insertOne(" .
        &JsonRecord(
            body => &JsonText(&WikiContentsAsJson(@lines)),
            start => &JsonText($meta_data{"start"}),
            stop => (exists $meta_data{"stop"}) ? &JsonText($meta_data{"stop"}) : "null",
            book => "book.insertedId",
            reviewer => "jean._id",
        ) . ");";

    local ($user_review_stmt) = "db.users.updateOne(" .
        &JsonRecord("_id" => "jean._id") . "," .
        &JsonRecord("\$addToSet" => &JsonRecord(reviews => "review.insertedId")) . ");";

    local ($book_review_stmt) = "db.books.updateOne(" .
        &JsonRecord("_id" => "book.insertedId") . "," .
        &JsonRecord("\$addToSet" => &JsonRecord(reviews => "review.insertedId")) . ");";

    return join("\n", $book_stmt, $review_stmt, $user_review_stmt, $book_review_stmt);
}
