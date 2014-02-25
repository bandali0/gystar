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

    make_public = get_yes_no_input("Make the gist public?", False)
    files = {'stars': InputFileContent(str_gist_body)}
    todaydate = str(date.today().strftime("%a %b %d, %Y"))
    we_are_good = True
    try:
        starsgist = u.create_gist(make_public, files,
                                  "A list of your starred repos (generated on "
                                  + todaydate + " )")
        print "A gist containing all your starred repos " \
            + "was successfully created!"
        print "The gist is available at: " + starsgist.html_url
    except GithubException as ghe:
        print "Sorry, there was a problem creating your gist.",
        print "Here's the exception:"
        print ghe
        we_are_good = False

    if we_are_good:
        delete_all_starred = \
            get_yes_no_input("Should I unstar all the repos as well?", False)
        if delete_all_starred:
            try:
                for repo in repos:
                    u.remove_from_starred(repo)
            except GithubException as ghe:
                we_are_good = False
                print ghe
                sys.exit(1)

            if we_are_good:
                print "All repos were unstarred!"


def get_yes_no_input(question, default):
    q_prefix = [" [y/N]: ", " [Y/n]: "]
    str_answer = raw_input(question + q_prefix[default]).lower()
    if not default:
        return len(str_answer) > 0 and str_answer[0] == 'y'
    else:
        if len(str_answer) == 0:
            return True
        else:
            return str_answer[0] == 'y'


main()
