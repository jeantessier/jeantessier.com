#!/usr/bin/perl

if ($0 =~ /(\w+)\./) {
    $DOCUMENT = $1;
}

print "Content-type: text/html\n";
print "Status: 301 Moved Permanently\n";
print "Location: $DOCUMENT.html\n";
print "\n";
print "Moved to $DOCUMENT.html\n";
