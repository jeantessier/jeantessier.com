require 'wiki_json.pl';

sub DocumentAsJson {
    local ($title) = &GetWikiTitle();

    return &JsonRecord(
        title => &JsonText($title),
        books => &DocumentPartsAsJson(),
    );
}

sub DocumentPartsAsJson {
    local (@files) = &GetWikiFiles();

    return &JsonList(map { &DocumentPartAsJson($_) } @files);
}

sub DocumentPartAsJson {
    local ($filename) = @_;

    open(FILEHANDLE, $filename);
    local (@lines) = <FILEHANDLE>;
    close(FILEHANDLE);

    local (%meta_data, @titles, @authors, @years);

    do {
        $line = shift(@lines);
        chomp $line;

        if ($line =~ /(\w+):\s*(.*)/) {
            local ($key, $value) = ($1, $2);

            if ($key eq "title") {
                push @titles, $value;
            } elsif ($key eq "author") {
                push @authors, $value;
            } elsif ($key eq "year") {
                push @years, $value;
            } else {
                $meta_data{$key} = $value;
            }
        }
    } until ($line =~ /^\s*$/);

    return &JsonRecord(
        name => &JsonText($meta_data{"name"}),
        titles => &JsonList(map {
            if (/\[(.*)\]\((.*)\)/) {
                &JsonRecord(
                    title => &JsonText($1),
                    link => &JsonText($2),
                );
            } else {
                &JsonRecord(
                    title => &JsonText($_),
                    link => "null",
                );
            }
        } @titles),
        authors => &JsonList(map { &JsonText($_) } @authors),
        publisher => &JsonText($meta_data{"publisher"}),
        years => &JsonList(map { &JsonText($_) } @years),
        acquired => (exists $meta_data{"acquired"}) ? &JsonText($meta_data{"acquired"}) : "null",
        start => (exists $meta_data{"start"}) ? &JsonText($meta_data{"start"}) : "null",
        stop => (exists $meta_data{"stop"}) ? &JsonText($meta_data{"stop"}) : "null",
        body => &JsonText(&MarkdownContentsAsJson(@lines)),
    );
}

1;
