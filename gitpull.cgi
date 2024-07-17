#!/usr/bin/perl

use Digest::SHA qw(hmac_sha1_hex);
use Time::HiRes qw(time);

$start_time = time();

open(KEYFILE, "gitpull.secret");
chomp($secret = <KEYFILE>);
close(KEYFILE);

if (defined $ENV{'CONTENT_LENGTH'}) {
    $contents = "";
    read (STDIN, $contents, $ENV{'CONTENT_LENGTH'});

    $digest = "sha1=" . hmac_sha1_hex($contents, $secret);

    if ($digest eq $ENV{'HTTP_X_HUB_SIGNATURE'}) {
        print "Content-type: text/plain\n";
        print "\n";
        print "OK\n";
        print "\n";
        print "git pull\n";
        print `git pull`;
        print "./githistory.sh\n";
        print `./githistory.sh`;
        print "./generate_contents.sh\n";
        print `./generate_contents.sh`;
    } else {
        print "Status: 400 Bad Request\n";
        print "Content-type: text/plain\n";
        print "\n";
        print "No match!\n";
    }
} else {
    print "Status: 400 Bad Request\n";
    print "Content-type: text/plain\n";
    print "\n";
    print "Missing payload!\n";
}

$stop_time = time();
$delta_ms = ($stop_time - $start_time) * 1_000;

print "\n";
print sprintf("Duration: %0.3f ms.\n", $delta_ms);
