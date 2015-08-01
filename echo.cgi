#!/usr/bin/perl

print "Content-type: application/json\n";
print "\n";

$formData = "";
if ($ENV{'REQUEST_METHOD'} eq 'GET') {
    $formData = $ENV{'QUERY_STRING'};
} elsif ($ENV{'REQUEST_METHOD'} eq 'POST') {
    read (STDIN, $formData, $ENV{'CONTENT_LENGTH'});
}

print "{\n";

print "  \"env\": {\n";
foreach $key (sort(keys(%ENV))) {
    print "    \"$key\": \"$ENV{$key}\",\n";
}
print "    \"Jean Tessier\": \"was here!\"\n";
print "  },\n";

print "  \"cookies\": {\n";
foreach $cookie (split(/;\s*/, $ENV{'HTTP_COOKIE'})) {
    if ($cookie =~ /(\w+)=(.*)/) {
        print "    \"$1\": \"$2\",\n";
    }
}
print "    \"Cookie Monster\": \"was here!\"\n";
print "  },\n";

print "  \"form\": {\n";

@pairs = split(/&/, $formData);
foreach $pair (@pairs){
  ($name, $value) = split (/=/, $pair);
  $name =~ tr/+/ /;
  $name =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $name =~ s/(['"])/\\$1/g;
  $name =~ s/\r?\n/\\\n/g;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ s/(['"])/\\$1/g;
  $value =~ s/\r?\n/\\\n/g;
  print "    \"$name\": \"$value\",\n";
}

print "    \"Jean Tessier\": \"was here, too!\"\n";
print "  }\n";

print "}\n";
