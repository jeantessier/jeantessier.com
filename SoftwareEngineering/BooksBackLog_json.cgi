#!/usr/bin/perl

#
#   Copyright (c) 2001-2015, Jean Tessier
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

require '../lib/wiki_json.pl';

$DIRNAME = "data";

if ($0 =~ /(\w+)_json\./) {
    $DOCUMENT = $1;
}

print "Content-type: application/json\n";
print "\n";
print &DocumentAsJson($DOCUMENT);

sub DocumentAsJson {
    local ($document) = @_;

    open(FILEHANDLE, "$DIRNAME/${document}_title.txt");
    local ($title, @subtitle) = <FILEHANDLE>;
    chomp $title;
    close(FILEHANDLE);

    return &JsonRecord(
        title => &JsonText($title),
        books => &DocumentPartsAsJson($document),
    );
}

sub DocumentPartsAsJson {
    local ($document) = @_;

    opendir(DIRHANDLE, $DIRNAME);
    local (@files) = grep { /^${document}_\d{4}-\d{2}-\d{2}_\w+.txt$/ } readdir(DIRHANDLE);
    closedir(DIRHANDLE);

    return &JsonList(map { &DocumentPartAsJson("$DIRNAME/$_") } reverse sort @files);
}

sub DocumentPartAsJson {
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

    return &JsonRecord(
        name => &JsonText($meta_data{"name"}),
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
        authors => &JsonList(map { &JsonText($_) } @authors),
        publisher => &JsonText($meta_data{"publisher"}),
        years => &JsonList(@years),
        body => &JsonText(&WikiContentsAsJson(@lines)),
    );
}