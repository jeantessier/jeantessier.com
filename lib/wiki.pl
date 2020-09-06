$WIKI_DIRNAME = "data";

if ($0 =~ /(\w+)_\w+\./) {
    $WIKI_NAME = $1;
}

sub GetWikiTitle {
    open(FILEHANDLE, "$WIKI_DIRNAME/${WIKI_NAME}_title.txt");
    local ($title, @subtitle) = <FILEHANDLE>;
    chomp $title;
    close(FILEHANDLE);

    return $title;
}

sub GetWikiFiles {
    local ($ext) = @_;

    opendir(DIRHANDLE, $WIKI_DIRNAME);
    local (@files) = grep { /^${WIKI_NAME}_\d{4}-\d{2}-\d{2}(_\w)?.${ext}$/ } readdir(DIRHANDLE);
    closedir(DIRHANDLE);

    return map { "${WIKI_DIRNAME}/$_" } reverse sort @files;
}

1;
