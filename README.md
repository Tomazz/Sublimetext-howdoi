A Sublimetext editor plugin similar to howdoi command line tool. It was developed for testing of several hypotheses from the research internship in the School of Computing Science at the University of Glasgow.
=====================

Main ideas that we were to investigate during the internship :
- Domain Specific Languages - sometimes we need a very simple, easy to learn solution that may be limited but at least does its job very well
- Compile the code from answers or questions
- **Mine Github**
- **Use Stack Overflow to search for programming related questions and answers. Maybe retrieve the code from answers.**

This program's purpose was to evaluate the usefulness of a tool for programmers from the last 2 points
 
The target user groups were people who
- forgot certain snippets of code
- don't want to browse web to do Stackoverflow search
- scientists from various fields who would like to search for useful software patterns
- beginners
They can do it directly in the text editor with this plugin.

Notes:
At the moment it looks like the github3.py library is the best for interfacing with the Github APIv3:
https://github.com/sigmavirus24/github3.py

For mining Stackoverflow for code we are currently using the Py-Stackexchange open-source library

Github API queries should be placed in the GithubQueries file

<h4>Should move all the paper notes here</h4>
