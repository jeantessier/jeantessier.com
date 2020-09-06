#!/usr/bin/perl

use lib '../lib';
require 'books_json.pl';

print "Content-type: application/json\n";
print "\n";
print &DocumentAsJson();
