#!/usr/bin/perl

#
#   Copyright (c) 2001-2016, Jean Tessier
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

use POSIX qw(strftime);

$DIRNAME = "data";

if ($0 =~ /(\w+)_atom\./) {
    $DOCUMENT = $1;
}

&PrintContentType();
&PrintDocumentHeader($DOCUMENT);
&PrintDocumentParts($DOCUMENT);
&PrintDocumentFooter();

sub PrintContentType {
    print "Content-type: application/atom+xml\n";
    print "\n";
}

sub PrintDocumentHeader {
    local ($document) = @_;

    open(FILEHANDLE, "$DIRNAME/${document}_title.txt");
    local ($title, @subtitle) = <FILEHANDLE>;
    chomp $title;
    close(FILEHANDLE);

    print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n";
    print "\n";
    print "<feed xmlns=\"http://www.w3.org/2005/Atom\">\n";
    print "\n";
    print "    <title>$title</title>\n";
    print "    <id>http://jeantessier.com/SoftwareEngineering/$DOCUMENT.html</id>\n";
    print "    <link href=\"http://jeantessier.com/SoftwareEngineering/$DOCUMENT.html\"/>\n";
    print "    <link href=\"http://jeantessier.com/SoftwareEngineering/${DOCUMENT}_atom.cgi\" rel=\"self\"/>\n";
    print "    <author>\n";
    print "        <name>Jean Tessier</name>\n";
    print "        <email>jean\@jeantessier.com</email>\n";
    print "        <uri>http://jeantessier.com/</uri>\n";
    print "    </author>\n";
    print "    <rights type=\"xhtml\"><div xmlns=\"http://www.w3.org/1999/xhtml\">Copyright (c) 2001-2016, Jean Tessier</div></rights>\n";
}

sub PrintDocumentParts {
    local ($document) = @_;

    opendir(DIRHANDLE, $DIRNAME);
    local (@files) = grep { /^${document}_\d{4}-\d{2}-\d{2}.txt$/ } readdir(DIRHANDLE);
    closedir(DIRHANDLE);

    local ($max_mtime) = 0;
    foreach $file (@files) {
        my $mtime = (stat("$DIRNAME/$file"))[9];
        if ($mtime > $max_mtime) {
            $max_mtime = $mtime;
        }
    }
    local ($updated) = strftime "%Y-%m-%dT%H:%M:%S%z", gmtime($max_mtime);
    print "    <updated>$updated</updated>\n";

    foreach $file (reverse sort @files) {
        &PrintDocumentPart("$DIRNAME/$file");
    }
}

sub PrintDocumentPart {
    local ($filename) = @_;

    local ($year, $month, $day);
    if ($filename =~ /(\d{4})-(\d{2})-(\d{2})/) {
        $year = $1;
        $month = $2;
        $day = $3;
    }

    local ($mtime) = (stat($filename))[9];
    local ($updated) = strftime "%Y-%m-%dT%H:%M:%S%z", gmtime($mtime);

    open(FILEHANDLE, $filename);
    local (@lines) = <FILEHANDLE>;
    close(FILEHANDLE);

    local (%meta_data, @titles, @authors, @years);

    local ($line);
    do {
        $line = shift(@lines);
        chomp $line;

        if ($line =~ /(\w+):\s*(.*)/) {
            local ($key, $value) = ($1, $2);

            if ($key eq "title") {
                if ($value =~ /\[\[(.*)\]\[(.*)\]\]/) {
                    local ($url, $label) = ($1, $2);
                    $url =~ s/\*/%2A/gi;
                    $url =~ s/=/%3D/gi;
                    $url =~ s/_/%5F/gi;
                    $url =~ s/&/&amp;/gi;
                    $label =~ s/&eacute;/&#233;/g;
                    $label =~ s/&uacute;/&#250;/g;
                    $value = "[[$url][$label]]";
                    $meta_data{'title'} = $label unless defined $meta_data{'title'};
                }
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

    foreach (@titles) {
        s/\[\[([^\]]*)\]\[_(.*)_\]\]/<a target="_blank" href="\1"><i>\2<\/i><\/a>/g;
        s/\[\[([^\]]*)\]\[(.*)\]\]/<a target="_blank" href="\1">\2<\/a>/g;
    }

    print "\n";
    print "    <entry>\n";
    print "        <title>" . $meta_data{'title'} . "</title>\n";
    print "        <id>http://jeantessier.com/$DOCUMENT.cgi#" . $meta_data{'name'} . "</id>\n";
    print "        <link href=\"http://jeantessier.com/$DOCUMENT.cgi#" . $meta_data{'name'} . "\"/>\n";
    print "        <published>${year}-${month}-${day}T00:00:00Z</published>\n";
    print "        <updated>$updated</updated>\n";
    print "        <content type=\"xhtml\"><div xmlns=\"http://www.w3.org/1999/xhtml\">\n";

    &PrintWikiContents(@lines);

    print "\n";
    print "<table>\n";
    print "    <tr>\n";
    print "        <td>Started reading:</td>\n";
    if ($meta_data{"start"} =~ /(\d{4})-(\d{2})-(\d{2})/) {
        print "        <td>$1</td><td>/</td><td>$2</td><td>/</td><td>$3</td>\n";
    } else {
        print "        <td colspan=\"5\"><i>not started</i></td>\n";
    }
    print "    </tr>\n";
    print "    <tr>\n";
    print "        <td>Finished reading:</td>\n";
    if (defined $meta_data{"start"}) {
        if ($meta_data{"stop"} =~ /(\d{4})-(\d{2})-(\d{2})/) {
            print "        <td>$1</td><td>/</td><td>$2</td><td>/</td><td>$3</td>\n";
        } else {
            print "        <td colspan=\"5\"><i>in progress</i></td>\n";
        }
    }
    print "    </tr>\n";
    print "</table>\n";

    print "        </div></content>\n";
    print "    </entry>\n";
}

sub PrintWikiContents {
    local (@lines) = @_;

    local ($in_paragraph, $in_quote, $in_ordered_list, $in_unordered_list, $in_html);

    foreach $line (@lines) {
        if ($line =~ /^\s*$/) {
            if ($in_paragraph) {
                $in_paragraph = !$in_paragraph;
                print "</p>\n";
            } elsif ($in_quote) {
                $in_quote = !$in_quote;
                print "</pre>\n";
            } elsif ($in_ordered_list) {
                $in_ordered_list = !$in_ordered_list;
                print "</ol>\n";
            } elsif ($in_unordered_list) {
                $in_unordered_list = !$in_unordered_list;
                print "</ul>\n";
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
                        print "<ol>\n";
                    } elsif ($marker eq "*" && !$in_unordered_list) {
                        $in_unordered_list = !$in_unordered_list;
                        print "<ul>\n";
                    } elsif (!$in_quote) {
                        $in_quote = !$in_quote;
                        print "<pre>\n";
                    }
                } elsif ($line =~ /^</) {
                    $in_html = !$in_html;
                } else {
                    $in_paragraph = !$in_paragraph;
                    print "<p>\n";
                }
            }
        }

        $line =~ s/=([^=]*)=/<code>\1<\/code>/g;
        $line =~ s/_([^_]*)_/<i>\1<\/i>/g;
        $line =~ s/\*([^*]*)\*/<b>\1<\/b>/g;
        $line =~ s/\[\[([^\]]*)\]\[(.*\.((gif)|(jpg)))\]\]/<a target="_blank" href="\1"><img border="0" src="\2" \/><\/a><br \/>/gi;
        $line =~ s/\[\[([^\]]*\.((gif)|(jpg)))\]\]/<img src="\1" \/><br \/>/gi;
        $line =~ s/\[\[(\w+)\]\]/<a href="#\1">\1<\/a>/gi;
        $line =~ s/\[\[([^\]]*)\]\[(.*)\]\]/<a target="_blank" href="\1">\2<\/a>/g;

        $line =~ s/%2A/\*/gi;
        $line =~ s/%3D/=/gi;
        $line =~ s/%5F/_/gi;

        $line =~ s/&nbsp;/&#160;/g;
        $line =~ s/&agrave;/&#224;/g;
        $line =~ s/&egrave;/&#232;/g;
        $line =~ s/&eacute;/&#233;/g;
        $line =~ s/&ecirc;/&#234;/g;
        $line =~ s/&ocirc;/&#244;/g;
        $line =~ s/&ouml;/&#246;/g;
        $line =~ s/&uacute;/&#250;/g;
        $line =~ s/&uuml;/&#252;/g;

        print $line;
    }

    if ($in_paragraph) {
        print "</p>\n";
    } elsif ($in_quote) {
        print "</pre>\n";
    } elsif ($in_ordered_list) {
        print "</ol>\n";
    } elsif ($in_unordered_list) {
        print "</ul>\n";
    }
}

sub PrintDocumentFooter {
    print "\n";
    print "</feed>\n";
}
