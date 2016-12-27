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

print STDOUT "Content-type: application/json\n";
print STDOUT "\n";

print OUTFILE "REQUEST_METHOD: $ENV{'REQUEST_METHOD'}\n";
if (defined $ENV{'QUERY_STRING'}) {
    print OUTFILE "QUERY_STRING: $ENV{'QUERY_STRING'}\n";
}
if (defined $ENV{'CONTENT_TYPE'}) {
    print OUTFILE "CONTENT_TYPE: $ENV{'CONTENT_TYPE'}\n";
}
if (defined $ENV{'CONTENT_LENGTH'}) {
    print OUTFILE "CONTENT_LENGTH: $ENV{'CONTENT_LENGTH'}\n";
}

$metadata{'method'} = $ENV{'REQUEST_METHOD'};
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    $metadata{'query string'} = $ENV{'QUERY_STRING'};
}
if (defined $ENV{'CONTENT_TYPE'}) {
    $metadata{'content type'} = $ENV{'CONTENT_TYPE'};
}
if (defined $ENV{'CONTENT_LENGTH'}) {
    $metadata{'content length'} = $ENV{'CONTENT_LENGTH'};
}
while (my ($k, $v) = each %metadata) {
    push @metadata, '"' . $k . '": "' . $v . '"';
}

$json = "";

$json .= "{\n";
$json .= "    \"request\": {\n";
$json .= "        " . join(",\n        ", @metadata) . "\n";
$json .= "    },\n";

print OUTFILE "\n";
print OUTFILE "Headers:\n";
foreach $key (sort(keys(%ENV))) {
    if ($key =~ /^HTTP_(.*)/) {
        print OUTFILE "$1: $ENV{$key}\n";
    }
}

$count = 0;
$json .= "    \"headers\": {\n";
foreach $key (sort(keys(%ENV))) {
    if ($key =~ /^HTTP_(.*)/) {
        $json .= "        \"$1\": \"$ENV{$key}\",\n";
        $count++;
    }
}
$json .= "        \"count\": $count\n";
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
print OUTFILE "============================================================\n";
close(OUTFILE);
