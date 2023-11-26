#!/usr/bin/perl

use lib './lib';
require 'books_json.pl';

if (!grep { /--no-headers/ } @ARGV) {
    print "Content-type: application/json\n";
    print "\n";
}
print &DocumentAsJson();
