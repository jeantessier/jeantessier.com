#!/usr/bin/perl

use lib '../lib';
require 'wiki_json.pl';

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

if (!grep { /--no-headers/ } @ARGV) {
    print "Content-type: application/json\n";
    print "\n";
}
print &DocumentAsJson();

sub DocumentAsJson {
    local ($title) = &GetWikiTitle();

    return &JsonRecord(
        title => &JsonText($title),
        entries => &DocumentPartsAsJson(),
    );
}

sub DocumentPartsAsJson {
    local (@files) = &GetWikiFiles();

    return &JsonList(map { &DocumentPartAsJson($_) } @files);
}

sub DocumentPartAsJson {
    local ($filename) = @_;

    open(FILEHANDLE, $filename);
    local (@lines) = <FILEHANDLE>;
    close(FILEHANDLE);

    local (@history);
    if (-T $filename . ".history") {
        open(FILEHANDLE, $filename . ".history");
        while (<FILEHANDLE>) {
            if (/(?<date>\d{4}-\d{2}-\d{2}): (?<message>.*)/) {
                push(@history, {date => $+{date}, message => $+{message}});
            }
        }
        close(FILEHANDLE);
    }

    $filename =~ /(?<date>(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2}))/;

    return &JsonRecord(
        date => &JsonText($+{date}),
        pretty_date => &JsonText("$MONTH{$+{month}} $+{day}, $+{year}"),
        body => &JsonText(&MarkdownContentsAsJson(@lines)),
        history => &JsonList(map {
            &JsonRecord(
                "date" => &JsonText($_->{"date"}),
                "message" => &JsonText($_->{"message"}),
            )
        } @history),
    );
}
