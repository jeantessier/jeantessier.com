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
    local (@files) = &GetWikiFiles("txt");

    return &JsonList(map { &DocumentPartAsJson($_) } @files);
}

sub DocumentPartAsJson {
    local ($filename) = @_;
    local ($date, $year, $month, $day);

    local ($date);
    if ($filename =~ /((\d{4})-(\d{2})-(\d{2}))/) {
        $date = $1;
        $year = $2;
        $month = $3;
        $day = $4;
    }

    open(FILEHANDLE, $filename);
    local (@lines) = <FILEHANDLE>;
    close(FILEHANDLE);

    return &JsonRecord(
        date => &JsonText($date),
        pretty_date => &JsonText("$MONTH{$month} $day, $year"),
        body => &JsonText(&WikiContentsAsJson(@lines)),
    );
}
