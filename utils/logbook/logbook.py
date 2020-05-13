from github import Github

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Ziyou Zhang"
__status__ = "Production"

g = Github("23696ebca5388d6fe9ced9690919e5ed51be90b5")

repo = g.get_repo("ZiyouZhang/Sentrade")
all_issues = repo.get_issues(state='all')
count = 0

with open("logbook.txt", "w") as f:
    for issue in all_issues:
        print("current progress:", issue.number)
        f.write("Task Number: {}\\\\\n".format(issue.number))
        f.write("Task ID: {}\\\\\n".format(issue.id))
        f.write("Title: {}\\\\\n".format(issue.title))
        f.write("Created at: {}\\\\\n".format(issue.created_at))

        f.write("Assignees: ")
        for assignee in issue.assignees:
            f.write("{}({}) ".format(assignee.name, assignee.login))
        f.write("\\\\\n")
        
        f.write("Body: {}\\\\\n".format(issue.body))
        f.write("Closed at: {}\\\\\n".format(issue.closed_at))
        f.write("Closed by: {}({})\\\\\n".format(issue.closed_by.name, issue.closed_by.login))
        f.write("State: {}\\\\\n".format(issue.state))
        f.write(r"\newline")
        f.write("\n")
        count = count + 1

print("total issues:", count)
