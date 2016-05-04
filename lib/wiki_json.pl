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

sub WikiContentsAsJson {
    local (@lines) = @_;

    local ($in_paragraph, $in_quote, $in_ordered_list, $in_unordered_list, $in_html);

    local ($result) = "";

    foreach $line (@lines) {
        if ($line =~ /^\s*$/) {
            if ($in_paragraph) {
                $in_paragraph = !$in_paragraph;
                $result .= "</p>";
            } elsif ($in_quote) {
                $in_quote = !$in_quote;
                $result .= "</pre>";
            } elsif ($in_ordered_list) {
                $in_ordered_list = !$in_ordered_list;
                $result .= "</ol>";
            } elsif ($in_unordered_list) {
                $in_unordered_list = !$in_unordered_list;
                $result .= "</ul>";
            } elsif ($in_html) {
                $in_html = !$in_html;
            }
        } elsif ($line =~ /^---(\++)\s*(.*)\s*/) {
            local $level = (length $1) + 1;
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
                        $result .= "<ol>";
                    } elsif ($marker eq "*" && !$in_unordered_list) {
                        $in_unordered_list = !$in_unordered_list;
                        $result .= "<ul>";
                    } elsif (!$in_quote) {
                        $in_quote = !$in_quote;
                        $result .= "<pre>";
                    }
                } elsif ($line =~ /^</) {
                    $in_html = !$in_html;
                } else {
                    $in_paragraph = !$in_paragraph;
                    $result .= "<p>";
                }
            }
        }

        $line =~ s/=([^=]*)=/<span class=\"code\">\1<\/span>/g;
        $line =~ s/_([^_]*)_/<i>\1<\/i>/g;
        $line =~ s/\*([^*]*)\*/<b>\1<\/b>/g;
        $line =~ s/\[\[([^\]]*)\]\[(.*\.((gif)|(jpg)|(png)))\]\]/<a target="_blank" href="\1"><img border="0" src="\2" \/><\/a><br \/>/gi;
        $line =~ s/\[\[([^\]]*\.((gif)|(jpg)|(png)))\]\]/<img src="\1" \/><br \/>/gi;
        $line =~ s/\[\[(\d\d\d\d-\d\d-\d\d)\]\]/<a href="#\1">\1<\/a>/gi;
        $line =~ s/\[\[([^\]]*)\]\[(.*)\]\]/<a target="_blank" href="\1">\2<\/a>/g;

        $line =~ s/%2A/\*/gi;
        $line =~ s/%3D/=/gi;
        $line =~ s/%5F/_/gi;

        $line =~ s/\\/\\\\/g;
        $line =~ s/"/\\"/g;
        $line =~ s/\n/\\n/g if $in_quote;
        $line =~ s/^\s+// if $in_html;

        $result .= $line;
    }

    if ($in_paragraph) {
        $result .= "</p>";
    } elsif ($in_quote) {
        $result .= "</pre>";
    } elsif ($in_ordered_list) {
        $result .= "</ol>";
    } elsif ($in_unordered_list) {
        $result .= "</ul>";
    }

    $result =~ s/((\w|")\/?>)\n(<\w)/\1\3/g;
    $result =~ s/\n(<\w)/ \1/g;
    $result =~ s/\n(\W)/\1/g;
    $result =~ s/([.;])\n/\1  /g;
    $result =~ s/\n/ /g;

    return $result
}

sub JsonList {
    local (@params) = @_;

    return "[" . join(",", @params) . "]";
}

sub JsonRecord {
    local (%params) = @_;

    return "{" . join(",", map { &JsonText($_) . ":" . $params{$_} } keys %params) . "}";
}

sub JsonText {
    local ($text) = @_;

    $text =~ s/([^\\])"/\1\\"/g;

    return "\"" . $text . "\"";
}

1;
