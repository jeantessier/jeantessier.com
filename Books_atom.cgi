#!/usr/bin/perl

use POSIX qw(strftime);

use lib './lib';
require 'wiki.pl';

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
    print "    <id>https://jeantessier.com/${document}.html</id>\n";
    print "    <link href=\"https://jeantessier.com/${document}.html\"/>\n";
    print "    <link href=\"https://jeantessier.com/${document}_atom.cgi\" rel=\"self\"/>\n";
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

    local ($published_date);
    if ($filename =~ /(\d{4}-\d{2}-\d{2})/) {
        $published_date = $1;
    }

    local ($mtime) = (stat($filename))[9];
    local ($updated) = strftime "%Y-%m-%dT%H:%M:%SZ", gmtime($mtime);

    open(FILEHANDLE, $filename);
    local (@lines) = <FILEHANDLE>;
    close(FILEHANDLE);

    local (%meta_data);

    local ($line);
    do {
        $line = shift(@lines);
        chomp $line;

        if ($line =~ /(\w+):\s*(.*)/) {
            local ($key, $value) = ($1, $2);

            if ($key eq "title") {
                if ($value =~ /\[(.*)\]\(.*\)/) {
                    $meta_data{'title'} = $1 unless defined $meta_data{'title'};
                } else {
                    $meta_data{'title'} = $value unless defined $meta_data{'title'};
                }
            } else {
                $meta_data{$key} = $value unless defined $meta_data{$key};
            }
        }
    } until ($line =~ /^\s*$/);

    $meta_data{'title'} =~ s/&agrave;/&#224;/g;
    $meta_data{'title'} =~ s/&egrave;/&#232;/g;
    $meta_data{'title'} =~ s/&eacute;/&#233;/g;
    $meta_data{'title'} =~ s/&ecirc;/&#234;/g;
    $meta_data{'title'} =~ s/&ocirc;/&#244;/g;
    $meta_data{'title'} =~ s/&ouml;/&#246;/g;
    $meta_data{'title'} =~ s/&uacute;/&#250;/g;
    $meta_data{'title'} =~ s/&uuml;/&#252;/g;

    print "\n";
    print "    <entry>\n";
    print "        <title>" . $meta_data{'title'} . "</title>\n";
    print "        <id>https://jeantessier.com/${document}.html#" . $meta_data{'name'} . "</id>\n";
    print "        <link href=\"https://jeantessier.com/${document}.html#" . $meta_data{'name'} . "\"/>\n";
    print "        <published>${published_date}T00:00:00Z</published>\n";
    print "        <updated>$updated</updated>\n";
    print "        <content type=\"text/markdown\">\n";

    &PrintWikiContents(@lines);

    print "\n";
    if ($meta_data{"start"} =~ /(\d{4}-\d{2}-\d{2})/) {
        print "Started reading: `$1`  \n";
    } else {
        print "Started reading: _not started_  \n";
    }
    print "        <td>Finished reading:</td>\n";
    if (defined $meta_data{"start"}) {
        if ($meta_data{"stop"} =~ /(\d{4}-\d{2}-\d{2})/) {
            print "Finished reading: `$1`  \n";
        } else {
            print "Finished reading: _in progress_\n";
        }
    }

    print "        </content>\n";
    print "    </entry>\n";
}

sub PrintWikiContents {
    local (@lines) = @_;

    foreach $line (@lines) {
        $line =~ s/&(?!amp|lt|gt)/&amp;/g;
        $line =~ s/</&lt;/g;
        $line =~ s/>/&gt;/g;

        print $line;
    }
}

sub PrintDocumentFooter {
    print "\n";
    print "</feed>\n";
}
