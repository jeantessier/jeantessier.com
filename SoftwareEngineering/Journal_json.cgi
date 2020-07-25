#!/usr/bin/perl

#
#   Copyright (c) 2001, Jean Tessier
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
