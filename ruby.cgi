#!/usr/bin/ruby

require "cgi"
cgi = CGI.new("html3")

cgi.out() do
  cgi.html() do
    cgi.head { cgi.title { "Ruby Test" } } +
    cgi.body() do
      cgi.h1 { "Test for Ruby" } +
      cgi.table() do
        cgi.tr() do
          cgi.td() { "name" } + cgi.td() { "value" }
        end
        cgi.params do |name, value|
          cgi.tr() do
            cgi.td() { name } + cgi.td() { value }
          end
        end
      end
    end
  end
end

