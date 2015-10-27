#!/usr/bin/perl

use Digest::SHA qw(hmac_sha1_hex);

open(KEYFILE, "github.secret");
chomp($secret = <KEYFILE>);
close(KEYFILE);

print "Content-type: text/plain\n";
print "\n";

if (defined $ENV{'CONTENT_LENGTH'}) {
    $contents = "";
    read (STDIN, $contents, $ENV{'CONTENT_LENGTH'});

    $digest = hmac_sha1_hex($contents, $secret);

    if ($digest == $ENV{'HTTP_X_HUB_SIGNATURE'}) {
        eval "git pull";
        print "OK\n";
    } else {
        print "HTTP_X_HUB_SIGNATURE: $ENV{'HTTP_X_HUB_SIGNATURE'}\n";
        print "digest: $digest\n";
        print "No match!\n";
    }
} else {
    print "No payload!\n";
}
