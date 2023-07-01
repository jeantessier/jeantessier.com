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

print "Content-type: application/json\n";
print "\n";
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

    $filename =~ /(?<date>(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2}))/;

    return &JsonRecord(
        date => &JsonText($+{date}),
        pretty_date => &JsonText("$MONTH{$+{month}} $+{day}, $+{year}"),
        body => &JsonText(&MarkdownContentsAsJson(@lines)),
    );
}
