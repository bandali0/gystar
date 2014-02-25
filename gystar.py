#!/usr/bin/python

from datetime import date
import getpass
import sys
sys.path.append("./PyGithub")
from github import Github
from github import GithubException
from github import InputFileContent


def main():
    username = raw_input("Your GitHub username: ")
    password = getpass.getpass()
    g = Github(username, password)

    u = g.get_user()

    print "Retreiving your repositories..."
    repos = u.get_starred()
    print "done."

    str_gist_body = u"Your starred repositories:\n\n"
    sys.stdout.write("Trying to build a list of the repositories")
    sys.stdout.flush()
    try:
        for repo in repos:
            str_gist_body += repo.name + u" " + repo.html_url + "\n"
            sys.stdout.write(".")
            sys.stdout.flush()
        print
    except GithubException as ghe:
        #print "Incorrect username or password."
        print
        print ghe
        sys.exit(1)

    pub_string = raw_input("Make the gist public? [y/N]: ").lower()
    make_public = len(pub_string) > 0 and pub_string[0] == 'y'
    files = {'stars': InputFileContent(str_gist_body)}
    todaydate = str(date.today().strftime("%a %b %d, %Y"))
    try:
        u.create_gist(make_public, files,
                      "A list of your starred repos (generated on "
                      + todaydate + " )")
    except GithubException as ghe:
        print "Sorry, there was a problem creating your gist.",
        print "Here's the exception:"
        print ghe


main()
