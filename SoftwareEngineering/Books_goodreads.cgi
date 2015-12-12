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

$DIRNAME = "data";

if ($0 =~ /(\w+)_goodreads\./) {
    $DOCUMENT = $1;
}

@HEADINGS = (
    "Title",
    "Author",
    "ISBN",
    "ISBN13",
    "Publisher",
    "Year Published",
    "Original Publication Year",
    "Date Read",
    "Date Added",
    "Bookshelves",
    "Exclusive Shelf",
    "My Review",
);

&PrintContentType();
&PrintDocumentHeader($DOCUMENT);
&PrintDocumentParts($DOCUMENT);
&PrintDocumentFooter();

sub PrintContentType {
}

sub PrintDocumentHeader {
    print join(",", @HEADINGS) . "\n";
}

sub PrintDocumentParts {
    local ($document) = @_;

    opendir(DIRHANDLE, $DIRNAME);
    local (@files) = grep { /^${document}_\d{4}-\d{2}-\d{2}.*.txt$/ } readdir(DIRHANDLE);
    closedir(DIRHANDLE);

    foreach $file (reverse sort @files) {
        &PrintDocumentPart("$DIRNAME/$file");
    }
}

sub PrintDocumentPart {
    local ($filename) = @_;

    open(FILEHANDLE, $filename);
    local (@lines) = <FILEHANDLE>;
    close(FILEHANDLE);

    local (%meta_data, @isbn, @titles, @authors, @years);

    do {
        $line = shift(@lines);
        chomp $line;

        if ($line =~ /(\w+):\s*(.*)/) {
            local ($key, $value) = ($1, $2);

            if ($key eq "title") {
                if ($value =~ /\[\[.*\]\[(.*)\]\]/) {
                    $value = $1;
                }
                push @titles, $value;
            } elsif ($key eq "isbn") {
                push @isbn, $value;
            } elsif ($key eq "author") {
                push @authors, $value;
            } elsif ($key eq "year") {
                push @years, $value;
            } else {
                $meta_data{$key} = $value;
            }
        }
    } until ($line =~ /^\s*$/);

    print &CsvEscape(@titles[0]) . ",";
    print &CsvEscape(join(",", @authors)) . ",";
    print '="' . @isbn[0] . '",';
    if (defined $meta_data{"isbn13"}) {
        print '="' . $meta_data{"isbn13"} . '",';
    } else {
        print ",";
    }
    print &CsvEscape($meta_data{"publisher"}) . ",";
    print &CsvEscape(@years[0]) . ",";
    print &CsvEscape(@years[0]) . ",";
    if (defined $meta_data{"stop"}) {
        print &CsvEscape($meta_data{"stop"}) . ",";
    } else {
        print ",";
    }
    if (defined $meta_data{"acquired"}) {
        print &CsvEscape($meta_data{"acquired"}) . ",";
    } else {
        print ",";
    }
    print '"software",';
    if (defined $meta_data{"stop"}) {
        print '"read",';
    } elsif (defined $meta_data{"start"}) {
        print '"currently-reading",';
    } else {
        print '"to-read",';
    }
    print &CsvEscape(&WikiContents(@lines));
    print "\n";
}

sub CsvEscape {
    local ($text) = @_;

    if ($text =~ /[,"\n]/) {
        $text =~ s/"/""/g;
        return '"' . $text . '"'
    } else {
        return $text
    }
}

sub WikiContents {
    local (@lines) = @_;

    local ($in_paragraph, $in_quote, $in_ordered_list, $in_unordered_list, $in_html, @output);

    foreach $line (@lines) {
        if ($line =~ /^\s*$/) {
            if ($in_paragraph) {
                $in_paragraph = !$in_paragraph;
            } elsif ($in_quote) {
                $in_quote = !$in_quote;
                push(@output, "</pre>\n");
            } elsif ($in_ordered_list) {
                $in_ordered_list = !$in_ordered_list;
                push(@output, "</ol>\n");
            } elsif ($in_unordered_list) {
                $in_unordered_list = !$in_unordered_list;
                push(@output, "</ul>\n");
            } elsif ($in_html) {
                $in_html = !$in_html;
            }
        } elsif ($line =~ /^---(\++)\s*(.*)\s*/) {
            local $level = length $1;
            local $title = $2;

            $line = "<h$level>$title</h$level>\n";
        } elsif ($line =~ /^(\s*)((\S+)\s*(\S.*))/) {
            local ($indent, $text, $marker, $content) = ($1, $2, $3, $4);

            local ($indent_level) = length $indent;
            chomp $text;
            chomp $content;

            if (!$in_paragraph && !$in_quote && !$in_html && ($marker =~ /^\d+$/ || $marker eq "*")) {
                $line = "<li>$content</li>\n";
            }

            if (!$in_paragraph && !$in_quote && !$in_ordered_list && !$in_unordered_list && !$in_html) {
                if ($indent_level) {
                    if ($marker =~ /^\d+$/ && !$in_ordered_list) {
                        $in_ordered_list = !$in_ordered_list;
                        push(@output, "<ol>\n");
                    } elsif ($marker eq "*" && !$in_unordered_list) {
                        $in_unordered_list = !$in_unordered_list;
                        push(@output, "<ul>\n");
                    } elsif (!$in_quote) {
                        $in_quote = !$in_quote;
                        push(@output, "<pre>\n");
                    }
                } elsif ($line =~ /^</) {
                    $in_html = !$in_html;
                } else {
                    $in_paragraph = !$in_paragraph;
                }
            }
        }

        $line =~ s/=([^=]*)=/\1/g;
        $line =~ s/_([^_]*)_/<i>\1<\/i>/g;
        $line =~ s/\*([^*]*)\*/<b>\1<\/b>/g;
        $line =~ s/\[\[([^\]]*)\]\[(.*\.((gif)|(jpg)))\]\]/<a href="\1"><img border="0" src="\2" \/><\/a><br \/>/gi;
        $line =~ s/\[\[([^\]]*\.((gif)|(jpg)))\]\]/<img src="\1" \/><br \/>/gi;
        $line =~ s/\[\[(\d\d\d\d-\d\d-\d\d)\]\]/<a href="#\1">\1<\/a>/gi;
        $line =~ s/\[\[([^\]]*)\]\[(.*)\]\]/<a href="\1">\2<\/a>/g;

        $line =~ s/%2A/\*/gi;
        $line =~ s/%3D/=/gi;
        $line =~ s/%5F/_/gi;

        push(@output, $line);
    }

    if ($in_paragraph) {
    } elsif ($in_quote) {
        push(@output, "</pre>\n");
    } elsif ($in_ordered_list) {
        push(@output, "</ol>\n");
    } elsif ($in_unordered_list) {
        push(@output, "</ul>\n");
    }

    local ($text) = join("", @output);
    $text =~ s/\n\n/<br\/><br\/>/gi;
    $text =~ s/\n/ /gi;

    return $text;
}

sub PrintDocumentFooter {
}
