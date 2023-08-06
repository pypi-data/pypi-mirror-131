# Contributing to Drb Python
Thanks for considering to take part in the improvement of the Drb project. Contributions are always welcome!  
Here are guidelines and rules that can be helpful if you plan to want to get involved in the project.

#### Table Of Contents
[How Can I Contribute?](#how-can-i-contribute)
  * [Reporting Bugs](#reporting-bugs)
  * [Suggesting Enhancements](#suggesting-enhancements)
  * [Your First Code Contribution](#your-first-code-contribution)
  * [Merge Requests](#merge-requests)
    * [Commit Message Guidelines](#commit-message-guidelines)
    * [Squash Commits](#squash-commits)


## Reporting Bugs
If you encounter a bug, please let us know about it. See the guide here [GitLab issues](https://docs.gitlab.com/ee/user/project/issues/).

**Before submitting a new issue** you might want to check for an [existing issue](https://gitlab.com/gael10/drb/drb-python/drb/issues) to know if there is already a reported issue. If an issue is already open please feel free
to add a comment to the existing issue instead of creating a new one.

### Submitting your first issue
We encourage using the issue template to improve quality of reported issues. 
Navigate to the issues tab and select `New issue`, then select the **Bug report** template and fill out the form.
To submit a good bug report keep in mind to:
* Use a descriptive title so other people can understand what the issue is about.
* Be specific about the details, for example, what command did you use, what version of Drb and its implementation did you use, and in what environment you observed the bug (CI or development).

## Suggesting Enhancements
If you want to suggest an enhancement, open a new issue and use the **enhancement** label.

**Before submitting an enhancement** please check for existing [feature requests](https://gitlab.com/gael10/drb/drb-python/drb/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement).

Useful things to point out in your feature request:
* Explain your feature request in a way that everyone can understand
* Please try to explain how this feature will improve the drb-python project

## Your First Code Contribution
You can start contributing to drb python project by picking [bug issues](https://gitlab.com/gael10/drb/drb-python/drb/issues?q=is%3Aopen+is%3Aissue+label%3Abug)
These issues can be easier to resolve rather than a feature request and can get you up and running with the code base.

## Pull Requests
The best way to get started with drb python is to grab the sources:

Fork the core repository or/and its implementations into one with your username
```shell script
git clone https://gitlab.com/<your username>/drb.git
```

Create you own branch to start writing code:
```shell script
git checkout -b mybranch
git push origin mybranch
```
You can test any changes with gitlab-runner:

```shell script
gitlab-runner exec shell pep8_check_style
gitlab-runner exec shell unit_tests_3.8
gitlab-runner exec shell unit_tests_3.9
```
And run whatever jobs defined into the _.gitlab-ci.yml_ file.

If everything is done, proceed with [opening a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/)

### Commit Message Guidelines

We follow the commit formatting recommendations found on [Chris Beams' How to Write a Git Commit Message article](https://chris.beams.io/posts/git-commit/).

Well formed commit messages not only help reviewers understand the nature of
the Pull Request, but also assists the release process where commit messages
are used to generate release notes.

A good example of a commit message would be as follows:

```
Summarize changes in around 50 characters or less

More detailed explanatory text, if necessary. Wrap it to about 72
characters or so. In some contexts, the first line is treated as the
subject of the commit and the rest of the text as the body. The
blank line separating the summary from the body is critical (unless
you omit the body entirely); various tools like `log`, `shortlog`
and `rebase` can get confused if you run the two together.

Explain the problem that this commit is solving. Focus on why you
are making this change as opposed to how (the code explains that).
Are there side effects or other unintuitive consequences of this
change? Here's the place to explain them.

Further paragraphs come after blank lines.

 - Bullet points are okay, too

 - Typically a hyphen or asterisk is used for the bullet, preceded
   by a single space, with blank lines in between, but conventions
   vary here

If you use an issue tracker, put references to them at the bottom,
like this:

Resolves: #123
See also: #456, #789
```

Note the `Resolves #123` tag, this references the issue raised and allows us to
ensure issues are associated and closed when a pull request is merged.

Please refer to [the gitlab help page on message types](https://docs.gitlab.com/ee/user/project/issues/crosslinking_issues.html)
for a complete list of issue references.

### Squash Commits

Should your pull request consist of more than one commit (perhaps due to
a change being requested during the review cycle), please perform a git squash
once a reviewer has approved your pull request.

A squash can be performed as follows. Let's say you have the following commits:

    initial commit
    second commit
    final commit

Run the command below with the number set to the total commits you wish to
squash (in our case 3 commits):

    git rebase -i HEAD~3

You default text editor will then open up and you will see the following::

    pick eb36612 initial commit
    pick 9ac8968 second commit
    pick a760569 final commit

    # Rebase eb1429f..a760569 onto eb1429f (3 commands)

We want to rebase on top of our first commit, so we change the other two commits
to `squash`:

    pick eb36612 initial commit
    squash 9ac8968 second commit
    squash a760569 final commit

After this, should you wish to update your commit message to better summarise
all of your pull request, run:

    git commit --amend

You will then need to force push (assuming your initial commit(s) were posted
to gitlab):

    git push origin your-branch --force