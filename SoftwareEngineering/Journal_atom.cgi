#!/usr/bin/perl

use POSIX qw(strftime);

use lib '../lib';
require 'wiki.pl';

%MONTH = (
          "01" => "January",
          "02" => "February",
          "03" => "March",
          "04" => "April",
          "05" => "May",
          "06" => "June",
          "07" => "July",
          "08" => "August",
          "09" => "September",
          "10" => "October",
          "11" => "November",
          "12" => "December",
          );

&PrintContentType();
&PrintDocumentHeader();
&PrintDocumentParts();
&PrintDocumentFooter();

sub PrintContentType {
    print "Content-type: application/atom+xml\n";
    print "\n";
}

sub PrintDocumentHeader {
  local ($document) = &GetWikiName();
  local ($title) = &GetWikiTitle();

    print "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n";
    print "\n";
    print "<feed xmlns=\"http://www.w3.org/2005/Atom\">\n";
    print "\n";
    print "    <title>$title</title>\n";
    print "    <id>https://jeantessier.com/SoftwareEngineering/${document}.html</id>\n";
    print "    <link href=\"https://jeantessier.com/SoftwareEngineering/${document}.html\"/>\n";
    print "    <link href=\"https://jeantessier.com/SoftwareEngineering/${document}_atom.cgi\" rel=\"self\"/>\n";
    print "    <author>\n";
    print "        <name>Jean Tessier</name>\n";
    print "        <email>jean\@jeantessier.com</email>\n";
    print "        <uri>https://jeantessier.com/</uri>\n";
    print "    </author>\n";
    print "    <rights type=\"xhtml\"><div xmlns=\"http://www.w3.org/1999/xhtml\">Copyright (c) 2001, Jean Tessier</div></rights>\n";
}

sub PrintDocumentParts {
  local ($document) = &GetWikiName();
  local (@files) = &GetWikiFiles();

    local ($max_mtime) = 0;
    foreach $file (@files) {
        my $mtime = (stat($file))[9];
        if ($mtime > $max_mtime) {
            $max_mtime = $mtime;
        }
    }
    local ($updated) = strftime "%Y-%m-%dT%H:%M:%SZ", gmtime($max_mtime);
    print "    <updated>$updated</updated>\n";

    foreach $file (reverse sort @files) {
        &PrintDocumentPart($document, $file);
    }
}

sub PrintDocumentPart {
    local ($document, $filename) = @_;

    local ($mtime) = (stat($filename))[9];
    local ($updated) = strftime "%Y-%m-%dT%H:%M:%SZ", gmtime($mtime);

    $filename =~ /(?<published_date>(?<year>\d{4})-(?<month>\d{2})-(?<day>\d{2}))/;

    print "\n";
    print "    <entry>\n";
    print "        <title>$MONTH{$+{month}} $+{day}, $+{year}</title>\n";
    print "        <id>https://jeantessier.com/SoftwareEngineering/${document}.html#$+{published_date}</id>\n";
    print "        <link href=\"https://jeantessier.com/SoftwareEngineering/${document}.html#$+{published_date}\"/>\n";
    print "        <published>$+{published_date}T00:00:00Z</published>\n";
    print "        <updated>$updated</updated>\n";
    print "        <content type=\"text/markdown\">\n";

    open(FILEHANDLE, $filename);

    local ($line);
    while ($line = <FILEHANDLE>) {
        $line =~ s/&(?!amp|lt|gt)/&amp;/g;
        $line =~ s/</&lt;/g;
        $line =~ s/>/&gt;/g;

        print $line;
    }

    close(FILEHANDLE);

    print "        </content>\n";
    print "    </entry>\n";
}

sub PrintDocumentFooter {
    print "\n";
    print "</feed>\n";
}
