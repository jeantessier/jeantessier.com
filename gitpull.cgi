#!/usr/bin/perl

use Digest::SHA qw(hmac_sha256_hex);
use Time::HiRes qw(time);

$start_time = time();

open(KEYFILE, "gitpull.secret");
chomp($secret = <KEYFILE>);
close(KEYFILE);

if (defined $ENV{'CONTENT_LENGTH'}) {
    $contents = "";
    read (STDIN, $contents, $ENV{'CONTENT_LENGTH'});

    $digest = "sha256=" . hmac_sha256_hex($contents, $secret);

    if ($digest eq $ENV{'HTTP_X_HUB_SIGNATURE_256'}) {
        print "Content-type: application/json\n";
        print "\n";
        print "{\n";
        print "\"git pull\": \"" . `git pull` . "\",\n";
        print "\"./githistory.sh\": \"" . `./githistory.sh` . "\",\n";
        print "\"./generate_contents.sh\": \"" . `./generate_contents.sh` . "\",\n";

        $stop_time = time();
        $delta_ms = ($stop_time - $start_time) * 1_000;

        print "\"duration\": " . sprintf("%0.3f", $delta_ms) . " ms\"\n";
        print "}\n";
    } else {
        print "Status: 401 Unauthorized\n";
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
