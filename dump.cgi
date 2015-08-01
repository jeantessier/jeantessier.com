#!/usr/bin/perl

print "Content-type: text/plain\n";
print "\n";

print "REQUEST_METHOD: $ENV{'REQUEST_METHOD'}\n";
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    print "QUERY_STRING: $ENV{'QUERY_STRING'}\n";
}

print "\n";
print "Headers:\n";
foreach $key (sort(keys(%ENV))) {
    if ($key =~ /^HTTP_(.*)/) {
        print "$1: $ENV{$key}\n";
    }
}

if (defined $ENV{'CONTENT_LENGTH'}) {
    $contents = "";
    read (STDIN, $contents, $ENV{'CONTENT_LENGTH'});
    print "\n";
    print "Contents:\n";
    print "\n";
    print "$contents\n";
}
