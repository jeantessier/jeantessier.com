# jeantessier.com

This project hosts the raw files I use to run
[my personal website](https://jeantessier.com/).

## Installation

Just drop everything in a folder under your webserver and enable `.cgi` to run
CGI scripts.  The scripts assume that Perl is installed on the system.

## Reusability

Most of this project is only useful to me.  You might be interested in my custom
blog management scripts and how they aggregate a bunch of text files in a
custom, homegrown wiki notation to create blog-like pages.

## Structure

The root directory is the main page for the site, including my resume.  There
are folders for sub-sections of the site.  The most interesting one is
`SoftwareEngineering`.  At both the top-level and in `SoftwareEngineering`,
there are some blog-like features:

- `Books.html`
- `BooksBackLog.html`
- `SoftwareEngineering/Books.html`
- `SoftwareEngineering/BooksBackLog.html`
- `SoftwareEngineering/Journal.html`

These [React](https://reactjs.org/) apps take their input from the `data` folder
next to them.  The name of the app has to match the prefix of the files in the
`data` folder.

`Books` helps me document the books I read.  I'm also copying the information to
[Goodreads.com](http://goodreads.com/).

`BooksBackLog` is just for me to keep track of the books on my to-do list.

`Journal` is my personal blog.  It does not support comments and the notation is
the bare minimum I need to get by.
