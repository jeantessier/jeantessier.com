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

use Getopt::Std;

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

getopts ("d:hn:");

if ($opt_h || !$opt_n) {
    print STDERR "USAGE: txt2html [-d datadir] [-h] -n name\n";
    print STDERR "\n";
    print STDERR "Reads in \"name\"_yyyy-mm-dd.txt files from \"datadir\" and\n";
    print STDERR "writes them out as HTML in \"name\" directory.\n";
    print STDERR "\n";
    print STDERR "    -d  directory to read files from (defaults to \"data\").\n";
    print STDERR "    -h  Prints a help screen (this screen).\n";
    print STDERR "    -n  prefix for files in \"datadir\".\n";
    print STDERR "\n";
    print STDERR "Copyright Jean Tessier, 2013.\n";
    print STDERR "\n";

    exit 1;
}

$DIRNAME = $opt_d ? $opt_d : "data";
$DOCUMENT = $opt_n;

&PrintDocuments($DIRNAME, $DOCUMENT);

sub PrintDocuments {
    local ($dirname, $document) = @_;

    opendir(DIRHANDLE, $dirname);
    local (@files) = grep { /^${document}_\d{4}-\d{2}-\d{2}.txt$/ } readdir(DIRHANDLE);
    closedir(DIRHANDLE);

    foreach $file (reverse sort @files) {
        $file =~ /^${document}_(\d{4}-\d{2}-\d{2}).txt$/;
        local ($infile) = "$dirname/$file";
        local ($outfile) = "$document/$1.html";

        local ($in_dev, $in_ino, $in_mode, $in_nlink, $in_uid, $in_gid, $in_rdev, $in_size, $in_atime, $in_mtime, $in_ctime, $in_blksize, $in_blocks) = stat $infile;
        local ($out_dev, $out_ino, $out_mode, $out_nlink, $out_uid, $out_gid, $out_rdev, $out_size, $out_atime, $out_mtime, $out_ctime, $out_blksize, $out_blocks) = stat $outfile;

        if ($in_mtime > $out_mtime) {
            &PrintDocument($infile, $outfile);
        }
    }

    &PrintIndex($document, map { "$dirname/$_" } reverse sort @files);
}

sub PrintDocument {
    local ($infile, $outfile) = @_;

    print "$infile --> $outfile\n";

    open INFILEHANDLE, $infile;
    local (@lines) = <INFILEHANDLE>;
    close INFILEHANDLE;

    local (%meta_data, $title, @titles, @authors, @years);

    do {
        $line = shift(@lines);
        chomp $line;

        if ($line =~ /(\w+):\s*(.*)/) {
            local ($key, $value) = ($1, $2);

            if ($key eq "title") {
                if ($value =~ /\[\[(.*)\]\[(.*)\]\]/) {
                    local ($url, $label) = ($1, $2);
                    if (!$title) {
                        $title = $label;
                    }
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

    open OUTFILEHANDLE, "> $outfile";

    print OUTFILEHANDLE "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    print OUTFILEHANDLE "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<head>\n";
    print OUTFILEHANDLE "<link rel=\"stylesheet\" type=\"text/css\" href=\"../style.css\" />\n";
    print OUTFILEHANDLE "<link rel=\"stylesheet\" type=\"text/css\" href=\"../books.css\" />\n";
    print OUTFILEHANDLE "<title>$title</title>\n";
    print OUTFILEHANDLE "<script type=\"text/javascript\" src=\"google_analytics.js\"></script>\n";
    print OUTFILEHANDLE "</head>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<body>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<div class=\"google_ad\">\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<script type=\"text/javascript\"><!--\n";
    print OUTFILEHANDLE "google_ad_client = \"pub-0113595750383868\";\n";
    print OUTFILEHANDLE "/* 728x90, created 2/25/09 */\n";
    print OUTFILEHANDLE "google_ad_slot = \"4082731877\";\n";
    print OUTFILEHANDLE "google_ad_width = 728;\n";
    print OUTFILEHANDLE "google_ad_height = 90;\n";
    print OUTFILEHANDLE "//-->\n";
    print OUTFILEHANDLE "</script>\n";
    print OUTFILEHANDLE "<script type=\"text/javascript\"\n";
    print OUTFILEHANDLE "src=\"http://pagead2.googlesyndication.com/pagead/show_ads.js\">\n";
    print OUTFILEHANDLE "</script>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "</div>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<table border=\"1\" cellspacing=\"1\" cellpadding=\"5\" rules=\"groups\" frame=\"below\">\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "    <thead>\n";
    print OUTFILEHANDLE "    <tr>\n";
    print OUTFILEHANDLE "        <th>Title</th>\n";
    print OUTFILEHANDLE "        <th>Author</th>\n";
    print OUTFILEHANDLE "        <th>Publisher</th>\n";
    print OUTFILEHANDLE "        <th>Year</th>\n";
    print OUTFILEHANDLE "    </tr>\n";
    print OUTFILEHANDLE "    </thead>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "    <tbody>\n";
    print OUTFILEHANDLE "    <tr>\n";
    print OUTFILEHANDLE "        <td class=\"book\">\n";
    print OUTFILEHANDLE "            <a name=\"" . $meta_data{"name"} . "\"></a>\n";
    print OUTFILEHANDLE "            " . join("<br />", @titles) . "\n";
    print OUTFILEHANDLE "        </td>\n";
    print OUTFILEHANDLE "        <td class=\"author\">" . join("<br />", @authors) . "</td>\n";
    print OUTFILEHANDLE "        <td class=\"publisher\">" . $meta_data{"publisher"} . "</td>\n";
    print OUTFILEHANDLE "        <td class=\"published_year\">" . join("<br />", @years) . "</td>\n";
    print OUTFILEHANDLE "    </tr>\n";
    print OUTFILEHANDLE "    <tr>\n";
    print OUTFILEHANDLE "        <td colspan=\"4\" class=\"lowlight\"><blockquote>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "            <div class=\"review\">\n";
    print OUTFILEHANDLE "\n";

    local ($in_paragraph, $in_quote, $in_ordered_list, $in_unordered_list, $in_html);

    foreach $line (@lines) {
        if ($line =~ /^\s*$/) {
            if ($in_paragraph) {
                $in_paragraph = !$in_paragraph;
                print OUTFILEHANDLE "</p>\n";
            } elsif ($in_quote) {
                $in_quote = !$in_quote;
                print OUTFILEHANDLE "</pre>\n";
            } elsif ($in_ordered_list) {
                $in_ordered_list = !$in_ordered_list;
                print OUTFILEHANDLE "</ol>\n";
            } elsif ($in_unordered_list) {
                $in_unordered_list = !$in_unordered_list;
                print OUTFILEHANDLE "</ul>\n";
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
                        print OUTFILEHANDLE "<ol>\n";
                    } elsif ($marker eq "*" && !$in_unordered_list) {
                        $in_unordered_list = !$in_unordered_list;
                        print OUTFILEHANDLE "<ul>\n";
                    } elsif (!$in_quote) {
                        $in_quote = !$in_quote;
                        print OUTFILEHANDLE "<pre>\n";
                    }
                } elsif ($line =~ /^</) {
                    $in_html = !$in_html;
                } else {
                    $in_paragraph = !$in_paragraph;
                    print OUTFILEHANDLE "<p>\n";
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

        print OUTFILEHANDLE $line;
    }

    if ($in_paragraph) {
        print OUTFILEHANDLE "</p>\n";
    } elsif ($in_quote) {
        print OUTFILEHANDLE "</pre>\n";
    } elsif ($in_ordered_list) {
        print OUTFILEHANDLE "</ol>\n";
    } elsif ($in_unordered_list) {
        print OUTFILEHANDLE "</ul>\n";
    }

    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "            </div>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "            <table>\n";
    print OUTFILEHANDLE "                <tr>\n";
    print OUTFILEHANDLE "                    <td class=\"time\">Started reading:</td>\n";
    if ($meta_data{"start"} =~ /(\d{4}-\d{2}-\d{2})/) {
        print OUTFILEHANDLE "                    <td class=\"time\">$1</td>\n";
    } else {
        print OUTFILEHANDLE "                    <td class=\"no_time\">not started</td>\n";
    }
    print OUTFILEHANDLE "                </tr>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "                <tr>\n";
    print OUTFILEHANDLE "                    <td class=\"time\">Finished reading:</td>\n";
    if (defined $meta_data{"start"}) {
        if ($meta_data{"stop"} =~ /(\d{4}-\d{2}-\d{2})/) {
            print OUTFILEHANDLE "                    <td class=\"time\">$1</td>\n";
        } else {
            print OUTFILEHANDLE "                    <td class=\"no_time\">in progress</td>\n";
        }
    }
    print OUTFILEHANDLE "                </tr>\n";
    print OUTFILEHANDLE "            </table>\n";
    print OUTFILEHANDLE "        </blockquote></td>\n";
    print OUTFILEHANDLE "    </tr>\n";
    print OUTFILEHANDLE "    </tbody>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "</table>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "</body>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "</html>\n";

    close OUTFILEHANDLE;
}

sub PrintIndex {
    local ($document, @files) = @_;

    open OUTFILEHANDLE, "> $document/index.html";

    print OUTFILEHANDLE "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
    print OUTFILEHANDLE "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<html xmlns=\"http://www.w3.org/1999/xhtml\">\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<head>\n";
    print OUTFILEHANDLE "<link rel=\"stylesheet\" type=\"text/css\" href=\"../style.css\" />\n";
    print OUTFILEHANDLE "<link rel=\"stylesheet\" type=\"text/css\" href=\"../books.css\" />\n";
    print OUTFILEHANDLE "<title>$document</title>\n";
    print OUTFILEHANDLE "<script type=\"text/javascript\" src=\"google_analytics.js\"></script>\n";
    print OUTFILEHANDLE "</head>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<body>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "<div class=\"index_entries\">\n";
    print OUTFILEHANDLE "\n";

    foreach $file (@files) {
        $file =~ /${document}_(\d{4}-\d{2}-\d{2}).txt$/;
        local ($id) = $1;

        open INFILEHANDLE, $file;
        local (@lines) = <INFILEHANDLE>;
        close INFILEHANDLE;

        local ($title, @authors, $year);

        do {
            $line = shift(@lines);
            chomp $line;

            if ($line =~ /(\w+):\s*(.*)/) {
                local ($key, $value) = ($1, $2);

                if ($key eq "title" && !$title) {
                    $value =~ /\[\[.*\]\[(.*)\]\]/;
                    $title = $1;
                } elsif ($key eq "author") {
                    push @authors, $value;
                } elsif ($key eq "year") {
                    $value =~ /(\d.*\d)/;
                    if (!$year || $year > $1) {
                        $year = $1;
                    }
                }
            }
        } until ($line =~ /^\s*$/);

        print OUTFILEHANDLE "<div class=\"index_entry\">\n";
        print OUTFILEHANDLE "<span class=\"title\"><a href=\"$id.html\">$title</a></span> <span class=\"published_year\">($year)</span>\n";
        print OUTFILEHANDLE "<div class=\"authors\">\n";

        foreach $author (map { /(\S+)$/ } @authors) {
            print OUTFILEHANDLE "<span class=\"author\">$author</span>\n";
        }

        print OUTFILEHANDLE "</div>\n";
        print OUTFILEHANDLE "</div>\n";
    }

    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "</div>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "</body>\n";
    print OUTFILEHANDLE "\n";
    print OUTFILEHANDLE "</html>\n";

    close OUTFILEHANDLE;
}
