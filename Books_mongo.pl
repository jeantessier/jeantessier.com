#!/usr/bin/perl

#
#   Copyright (c) 2001, Jean Tessier
#   All rights reserved.
#
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions
#   are met:
#
#       * Redistributions of source code must retain the above copyright
#         notice, this list of conditions and the following disclaimer.
#
#       * Redistributions in binary form must reproduce the above copyright
#         notice, this list of conditions and the following disclaimer in the
#         documentation and/or other materials provided with the distribution.
#
#       * Neither the name of Jean Tessier nor the names of his contributors
#         may be used to endorse or promote products derived from this software
#         without specific prior written permission.
#
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#   A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT SHALL THE REGENTS OR
#   CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#   PROCU# ENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#   PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#   LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#   NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#   SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

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
