#!/usr/bin/ruby -w

require 'cgi'

$PROGRAM_NAME =~ /(\w+)\./ && $DOCUMENT = $1

PART_RE = Regexp.new("^" + $DOCUMENT + "_\\d+-\\d+-\\d+.txt")
data_dir = Dir.new("data")
entries = data_dir.select {|filename| PART_RE === filename}

cgi = CGI.new("html4")

cgi.out do

cgi.html do

cgi.head {cgi.title {$DOCUMENT} } +

cgi.body do
    cgi.h1 {$DOCUMENT} +
    cgi.p {"These are the books I've read."} +
    cgi.ul do
	entries.each {|entry| cgi.li {entry}}
    end
end

end

end



