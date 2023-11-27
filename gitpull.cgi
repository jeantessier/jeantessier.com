#!/usr/bin/perl

use Digest::SHA qw(hmac_sha1_hex);
use Time::HiRes qw(time);

$start_time = time();

open(KEYFILE, "gitpull.secret");
chomp($secret = <KEYFILE>);
close(KEYFILE);

print "Content-type: text/plain\n";
print "\n";

if (defined $ENV{'CONTENT_LENGTH'}) {
    $contents = "";
    read (STDIN, $contents, $ENV{'CONTENT_LENGTH'});

    $digest = "sha1=" . hmac_sha1_hex($contents, $secret);

    if ($digest == $ENV{'HTTP_X_HUB_SIGNATURE'}) {
        print "OK\n";
        print "\n";
        print "git pull\n";
        print `git pull`;
        print "./githistory.sh\n";
        print `./githistory.sh`;
        print "./generate_contents.sh\n";
        print `./generate_contents.sh`;
    } else {
        print "No match!\n";
    }
} else {
    print "No payload!\n";
}

$stop_time = time();
$delta_ms = ($stop_time - $start_time) * 1_000_000;

print "\n";
print "Duration: $delta_ms ms.\n";
