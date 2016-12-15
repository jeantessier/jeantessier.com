#!/usr/bin/perl

use Digest::SHA qw(hmac_sha1_hex);
use POSIX qw(strftime);

$timestamp = strftime "%Y-%m-%d %H:%M:%W", localtime;

open(OUTFILE, ">>dump.out");
print OUTFILE "============================================================\n";
print OUTFILE "$timestamp $ENV{'SCRIPT_URI'}\n";

open(KEYFILE, "github.secret");
chomp($secret = <KEYFILE>);
close(KEYFILE);

print STDOUT "Content-type: text/plain\n";
print STDOUT "\n";

print STDOUT "REQUEST_METHOD: $ENV{'REQUEST_METHOD'}\n";
print OUTFILE "REQUEST_METHOD: $ENV{'REQUEST_METHOD'}\n";
if (defined $ENV{'QUERY_STRING'}) {
    print STDOUT "QUERY_STRING: $ENV{'QUERY_STRING'}\n";
    print OUTFILE "QUERY_STRING: $ENV{'QUERY_STRING'}\n";
}

print STDOUT "\n";
print OUTFILE "\n";
print STDOUT "Headers:\n";
print OUTFILE "Headers:\n";
foreach $key (sort(keys(%ENV))) {
    if ($key =~ /^HTTP_(.*)/) {
        print STDOUT "$1: $ENV{$key}\n";
        print OUTFILE "$1: $ENV{$key}\n";
    }
}

if (defined $ENV{'CONTENT_LENGTH'}) {
    $contents = "";
    read (STDIN, $contents, $ENV{'CONTENT_LENGTH'});
    print STDOUT "\n";
    print OUTFILE "\n";
    print STDOUT "Contents:\n";
    print OUTFILE "Contents:\n";
    print STDOUT "\n";
    print OUTFILE "\n";
    print STDOUT "$contents\n";
    print OUTFILE "$contents\n";

    $digest = hmac_sha1_hex($contents, $secret);

    print STDOUT "\n";
    print OUTFILE "\n";
    print STDOUT "Digest: sha1=" . $digest . "\n";
    print OUTFILE "Digest: sha1=" . $digest . "\n";
}

print OUTFILE "\n";
print OUTFILE "============================================================\n";
close(OUTFILE);
