#!/usr/bin/perl

use Digest::SHA qw(hmac_sha1_hex);
use POSIX qw(strftime);

$timestamp = strftime "%Y-%m-%d %H:%M:%W", localtime;

open(OUTFILE, ">>dump.out");
print OUTFILE "$timestamp $ENV{'SCRIPT_URI'}\n";

open(KEYFILE, "github.secret");
chomp($secret = <KEYFILE>);
close(KEYFILE);

print STDOUT "Content-type: application/json\n";
print STDOUT "\n";

print OUTFILE "REQUEST_METHOD: $ENV{'REQUEST_METHOD'}\n";
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    print OUTFILE "QUERY_STRING: $ENV{'QUERY_STRING'}\n";
}

$json = "";

$json .= "{\n";
$json .= "    \"request\": {\n";
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    $json .= "        \"method\": \"$ENV{'REQUEST_METHOD'}\",\n";
    $json .= "        \"query string\": \"$ENV{'QUERY_STRING'}\"\n";
} else {
    $json .= "        \"method\": \"$ENV{'REQUEST_METHOD'}\"\n";
}
$json .= "    },\n";

print OUTFILE "\n";
print OUTFILE "Headers:\n";
foreach $key (sort(keys(%ENV))) {
    if ($key =~ /^HTTP_(.*)/) {
        print OUTFILE "$1: $ENV{$key}\n";
    }
}

$json .= "    \"headers\": {\n";
foreach $key (sort(keys(%ENV))) {
    if ($key =~ /^HTTP_(.*)/) {
        $json .= "        \"$1\": \"$ENV{$key}\",\n";
    }
}
$json .= "        \"total\": " . (length keys(%ENV)) . "\n";
$json .= "    },\n";

if (defined $ENV{'CONTENT_LENGTH'}) {
    $contents = "";
    read (STDIN, $contents, $ENV{'CONTENT_LENGTH'});
    print OUTFILE "\n";
    print OUTFILE "Contents:\n";
    print OUTFILE "$contents\n";

    $contentsAsJson = $contents;
    $contentsAsJson =~ s/"/\\"/g;
    $contentsAsJson =~ s/\r/\\r/g;
    $contentsAsJson =~ s/\n/\\n/g;

    $json .= "    \"contents\": \"$contentsAsJson\",\n";

    $digest = hmac_sha1_hex($contents, $secret);

    print OUTFILE "\n";
    print OUTFILE "Digest: sha1=" . $digest . "\n";

    $json .= "    \"digest\": \"$digest\",\n";
}

$json .= "    \"author\": {\n";
$json .= "        \"name\": \"Jean Tessier\",\n";
$json .= "        \"email\": \"jean\@jeantessier.com\"\n";
$json .= "    }\n";
$json .= "}\n";

print STDOUT $json;

print OUTFILE "\n";
print OUTFILE "Output:\n";
print OUTFILE $json;

print OUTFILE "\n";
close(OUTFILE);
