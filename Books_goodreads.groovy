def document = "Books"
def dirname = "data"

def headers = [
        "Title",
        "Author",
        "ISBN",
        "My Rating",
        "Average Rating",
        "Publisher",
        "Binding",
        "Year Published",
        "Original Publication Year",
        "Date Read",
        "Date Added",
        "Bookshelves",
        "My Review",
]

println headers.join(", ")

new File(dirname).eachFileMatch(~/.*${document}(BackLog)?_\d.*/) { file ->



    println "${file} [${file.getClass().name}]"
}

def readHeaders(file) {

}