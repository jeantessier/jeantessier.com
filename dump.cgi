#!/usr/bin/perl

use Digest::SHA qw(hmac_sha1_hex);
use POSIX qw(strftime);

$timestamp = strftime "%Y-%m-%d %H:%M:%S", localtime;

open(KEYFILE, "github.secret");
chomp($secret = <KEYFILE>);
close(KEYFILE);

open(OUTFILE, ">>dump.out");
print OUTFILE "============================================================\n";
print OUTFILE "$timestamp $ENV{'SCRIPT_URI'}\n";

print STDOUT "Content-type: text/plain\n";
print STDOUT "\n";

print OUTFILE "REQUEST_METHOD: $ENV{'REQUEST_METHOD'}\n";
print STDOUT "REQUEST_METHOD: $ENV{'REQUEST_METHOD'}\n";
if (defined $ENV{'QUERY_STRING'}) {
    print OUTFILE "QUERY_STRING: $ENV{'QUERY_STRING'}\n";
    print STDOUT "QUERY_STRING: $ENV{'QUERY_STRING'}\n";
}
if (defined $ENV{'CONTENT_TYPE'}) {
    print OUTFILE "CONTENT_TYPE: $ENV{'CONTENT_TYPE'}\n";
    print STDOUT "CONTENT_TYPE: $ENV{'CONTENT_TYPE'}\n";
}
if (defined $ENV{'CONTENT_LENGTH'}) {
    print OUTFILE "CONTENT_LENGTH: $ENV{'CONTENT_LENGTH'}\n";
    print STDOUT "CONTENT_LENGTH: $ENV{'CONTENT_LENGTH'}\n";
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

    $digest = hmac_sha1_hex($contents, $secret);

    print OUTFILE "\n";
    print OUTFILE "Contents:\n";
    print OUTFILE "\n";
    print OUTFILE "$contents\n";
    print OUTFILE "\n";
    print OUTFILE "Digest: sha1=$digest\n";

    print STDOUT "\n";
    print STDOUT "Contents:\n";
    print STDOUT "\n";
    print STDOUT "$contents\n";
    print STDOUT "\n";
    print STDOUT "Digest: sha1=$digest\n";
}

print OUTFILE "\n";
print OUTFILE "============================================================\n";
close(OUTFILE);
