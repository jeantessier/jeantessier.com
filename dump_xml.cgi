#!/usr/bin/perl

use Digest::SHA qw(hmac_sha1_hex);
use POSIX qw(strftime);

$timestamp = strftime "%Y-%m-%d %H:%M:%W", localtime;

open(OUTFILE, ">>dump.out");
print OUTFILE "$timestamp $ENV{'SCRIPT_URI'}\n";

open(KEYFILE, "github.secret");
chomp($secret = <KEYFILE>);
close(KEYFILE);

print STDOUT "Content-type: application/xml\n";
print STDOUT "\n";

print OUTFILE "REQUEST_METHOD: $ENV{'REQUEST_METHOD'}\n";
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    print OUTFILE "QUERY_STRING: $ENV{'QUERY_STRING'}\n";
}

$xml = "";

$xml .= "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n";
$xml .= "\n";
$xml .= "<response>\n";
$xml .= "    <request>\n";
$xml .= "        <method>$ENV{'REQUEST_METHOD'}</method>\n";
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    $xml .= "        <query-string>$ENV{'QUERY_STRING'}</query-string>\n";
}
$xml .= "    </request>\n";

print OUTFILE "\n";
print OUTFILE "Headers:\n";
foreach $key (sort(keys(%ENV))) {
    if ($key =~ /^HTTP_(.*)/) {
        print OUTFILE "$1: $ENV{$key}\n";
    }
}

$count = 0;
$xml .= "    <headers count=\"" . (scalar grep { /^HTTP_/ } keys(%ENV)) . "\">\n";
foreach $key (sort(keys(%ENV))) {
    if ($key =~ /^HTTP_(.*)/) {
        $xml .= "        <header name=\"$1\">$ENV{$key}</header>\n";
        $count++;
    }
}
$xml .= "    </headers>\n";

if (defined $ENV{'CONTENT_LENGTH'}) {
    $contents = "";
    read (STDIN, $contents, $ENV{'CONTENT_LENGTH'});
    print OUTFILE "\n";
    print OUTFILE "Contents:\n";
    print OUTFILE "$contents\n";

    $digest = hmac_sha1_hex($contents, $secret);

    print OUTFILE "\n";
    print OUTFILE "Digest: sha1=" . $digest . "\n";

    $escapedContents = $contents;
    $escapedContents =~ s/&/&amp;/g;
    $escapedContents =~ s/</&lt;/g;
    $escapedContents =~ s/>/&gt;/g;

    $xml .= "    <contents digest=\"$digest\">$escapedContents</contents>\n";
}

$xml .= "    <author>\n";
$xml .= "        <name>Jean Tessier</name>\n";
$xml .= "        <email>jean\@jeantessier.com</email>\n";
$xml .= "    </author>\n";
$xml .= "</response>\n";

print STDOUT $xml;

print OUTFILE "\n";
print OUTFILE "Output:\n";
print OUTFILE $xml;

print OUTFILE "\n";
close(OUTFILE);