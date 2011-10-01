#!/usr/bin/perl

#   
#   Copyright (c) 2001-2009, Jean Tessier
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

%MONTH = (
          "01" => "January",
          "02" => "February",
          "03" => "March",
          "04" => "April",
          "05" => "May",
          "06" => "June",
          "07" => "July",
          "08" => "August",
          "09" => "September",
          "10" => "October",
          "11" => "November",
          "12" => "December",
          );

$DIRNAME = "data";

if ($0 =~ /(\w+)\./) {
    $DOCUMENT = $1;
}

&PrintContentType();
&PrintDocumentHeader($DOCUMENT);
&PrintDocumentParts($DOCUMENT);
&PrintDocumentFooter();

sub PrintContentType {
    print "Content-type: text/html\n";
    print "\n";
}

sub PrintDocumentHeader {
    local ($document) = @_;

    open(FILEHANDLE, "$DIRNAME/${document}_title.txt");
    local ($title, @subtitle) = <FILEHANDLE>;
    chomp $title;
    close(FILEHANDLE);

    print "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    print "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
    print "\n";
    print "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
    print "\n";
    print "<head>\n";
    print "<link rel=\"stylesheet\" type=\"text/css\" href=\"style.css\" />\n";
    print "<link rel=\"stylesheet\" type=\"text/css\" href=\"books.css\" />\n";
    print "<link rel=\"shortcut icon\" href=\"images/logoicon.gif\" type=\"/image/gif\" />\n";
    print "<title>$title</title>\n";
    print "<script type=\"text/javascript\" src=\"google_analytics.js\"></script>\n";
    print "</head>\n";
    print "\n";
    print "<body>\n";
    print "\n";
    print "<div align=\"center\">\n";
    print "\n";
    print "<script type=\"text/javascript\"><!--\n";
    print "google_ad_client = \"pub-0113595750383868\";\n";
    print "/* 728x90, created 2/25/09 */\n";
    print "google_ad_slot = \"4082731877\";\n";
    print "google_ad_width = 728;\n";
    print "google_ad_height = 90;\n";
    print "//-->\n";
    print "</script>\n";
    print "<script type=\"text/javascript\"\n";
    print "src=\"http://pagead2.googlesyndication.com/pagead/show_ads.js\">\n";
    print "</script>\n";
    print "\n";
    print "</div>\n";
    print "\n";
    print "<div align=\"right\">\n";
    print @subtitle;
    print "</div>\n";
    print "\n";
    print "<div align=\"center\">\n";
    print "<h1 class=\"highlight title\">$title</h1>\n";
    print "</div>\n";
    print "\n";
    print "<p></p>\n";
    print "\n";
    print "<table border=\"1\" cellspacing=\"1\" cellpadding=\"5\" rules=\"groups\" frame=\"below\">\n";
    print "\n";
    print "    <thead>\n";
    print "    <tr>\n";
    print "        <th>Title</th>\n";
    print "        <th>Author</th>\n";
    print "        <th>Publisher</th>\n";
    print "        <th>Year</th>\n";
    print "    </tr>\n";
    print "    </thead>\n";
}

sub PrintDocumentParts {
    local ($document) = @_;

    opendir(DIRHANDLE, $DIRNAME);
    local (@files) = grep { /^${document}_\d{4}-\d{2}-\d{2}.txt$/ } readdir(DIRHANDLE);
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

    local (%meta_data, @titles, @authors, @years);

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
                    $value = "[[$url][$label]]";
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
    print "    <tbody>\n";
    print "    <tr>\n";
    print "        <td class=\"book\">\n";
    print "            <a name=\"" . $meta_data{"name"} . "\"></a>\n";
    print "            " . join("<br />", @titles) . "\n";
    print "        </td>\n";
    print "        <td class=\"author\">" . join("<br />", @authors) . "</td>\n";
    print "        <td class=\"publisher\">" . $meta_data{"publisher"} . "</td>\n";
    print "        <td class=\"published_year\">" . join("<br />", @years) . "</td>\n";
    print "    </tr>\n";
    print "    <tr>\n";
    print "        <td colspan=\"4\" class=\"lowlight\"><blockquote>\n";
    print "\n";
    print "            <div class=\"review\">\n";
    print "\n";

    &PrintWikiContents(@lines);

    print "\n";
    print "            </div>\n";
    print "\n";
    print "            <table>\n";
    print "                <tr>\n";
    print "                    <td class=\"time\">Started reading:</td>\n";
    if ($meta_data{"start"} =~ /(\d{4}-\d{2}-\d{2})/) {
        print "                    <td class=\"time\">$1</td>\n";
    } else {
        print "                    <td class=\"no_time\">not started</td>\n";
    }
    print "                </tr>\n";
    print "\n";
    print "                <tr>\n";
    print "                    <td class=\"time\">Finished reading:</td>\n";
    if (defined $meta_data{"start"}) {
        if ($meta_data{"stop"} =~ /(\d{4}-\d{2}-\d{2})/) {
            print "                    <td class=\"time\">$1</td>\n";
        } else {
            print "                    <td class=\"no_time\">in progress</td>\n";
        }
    }
    print "                </tr>\n";
    print "            </table>\n";
    print "        </blockquote></td>\n";
    print "    </tr>\n";
    print "    </tbody>\n";
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

            if (!$in_paragraph && !$in_quote && !$in_html && !$in_ordered_list && !$in_unordered_list && !$in_html) {
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
        $line =~ s/\[\[(\d\d\d\d-\d\d-\d\d)\]\]/<a href="#\1">\1<\/a>/gi;
        $line =~ s/\[\[([^\]]*)\]\[(.*)\]\]/<a target="_blank" href="\1">\2<\/a>/g;
        
        $line =~ s/%2A/\*/gi;
        $line =~ s/%3D/=/gi;
        $line =~ s/%5F/_/gi;
        
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
    print "</table>\n";
    print "\n";
    print "</body>\n";
    print "\n";
    print "</html>\n";
}
