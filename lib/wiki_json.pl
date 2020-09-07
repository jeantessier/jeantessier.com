require 'wiki.pl';

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
        } elsif ($line =~ /^(\s*)((\S+)\s*(\S.*)?)/) {
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

        $line =~ s/=([^=]+)=/<code>\1<\/code>/g;
        $line =~ s/_([^_]+)_/<i>\1<\/i>/g;
        $line =~ s/\*([^*]+)\*/<b>\1<\/b>/g;
        $line =~ s/\[\[([^\]]*)\]\[(.*\.((gif)|(jpg)|(png)))\]\]/<a target="_blank" rel="noopener" href="\1"><img border="0" src="\2" \/><\/a><br \/>/gi;
        $line =~ s/\[\[([^\]]*\.((gif)|(jpg)|(png)))\]\]/<img src="\1" \/><br \/>/gi;
        $line =~ s/\[\[(\d\d\d\d-\d\d-\d\d)\]\]/<a href="#\1">\1<\/a>/gi;
        $line =~ s/\[\[(#[^\]]*)\]\[(.*)\]\]/<a href="\1">\2<\/a>/g;
        $line =~ s/\[\[([^\]]*)\]\[(.*)\]\]/<a target="_blank" rel="noopener" href="\1">\2<\/a>/g;

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
    $result =~ s/\n(<)/\1/g;
    $result =~ s/([.;])\n/\1  /g;
    $result =~ s/\n/ /g;

    return $result
}

sub MarkdownContentsAsJson {
    local (@lines) = @_;

    chomp(@lines);
    local ($result) = join('\n', @lines);

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

    $text =~ s/((\\[^n])|("))/\\\1/g;

    return "\"" . $text . "\"";
}

1;
