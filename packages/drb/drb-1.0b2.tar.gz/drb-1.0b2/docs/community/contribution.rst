.. _contribution:

Contributions
=============

Contribution process
--------------------
We are pleased to receive all users contributions. Each contribution shall be
documented in english, and code styling shall follow
`PEP8 <https://www.python.org/dev/peps/pep-0008>`_ recommendations.
You can also join the moderators team. Please contact me.

Contribution process is based on gitlab best practice and processes the
following schema:

.. image:: ../modification_process.png

How to contribute
-----------------
Contributor shall work in its own fork of the project and provides its
contributions via the merge request process. The merge request shall be
approved and merged by a maintainers. So the step-by-step procedure to
contribute is:

- Fork the project,
- Locally clone forked repository.
- Once created, the modification branch could be submitted as merge request in
  ``Draft`` proposal state.
- Once feature/bug finalized, ``Draft`` flag shall be removed and the
  assignees/maintainers notified for merge.

Before submission, contributor shall clean up, squash and rebase its commits to
be easily inserted as fast-forward into the main branch. Please read
`<https://chris.beams.io/posts/git-commit>`_ as commit writing best practices
for this project. The related issue/bug identifier shall be reported into the
commit message, otherwise, the issue shall be commented/closed accordingly.

Configuration management
------------------------
The project uses the `versioneer
<https://github.com/python-versioneer/python-versioneer>`_ tool to manage
releases deployment. Then, the version management and deployment are coupled
and can be performed in the same process. This process secures the deployment
process preventing a developer from accidentally deploying and erasing a
release version. Versioneer tool checks the local repository then generates a
``dirty`` release when repository is not clean. This process can also be useful
when developer needs to deploy snapshots. Multiple and dirty deployment of
versions are forbidden in `pypi <https://pypi.org/project/drb>`_ repository,
this behavior also secures the version erasing risks.

Setup environment
+++++++++++++++++
The environment shall be configured to deploy the python library onto Pypi
public  repository.The application used to manage module deployment is
``twine``. This application shall be configured via ``${HOME}/.pypirc`` file as
followed. Alternatively, the private gael's repository can be set (See
``[gael]`` entry.

.. code-block:: cfg

    [distutils]
    index-servers =
        pypi
        drb
    [pypi]
    username = __token__
    password = pypi-XXX

    [drb]
    repository = https://upload.pypi.orgr/legacy/
    username = __token__
    password = pypi-YYY

    [gael]
    repository = https://repository.gael-systems.com/repository/python-gael/
    username = username
    password = password


The important part is the drb section which defines the remote repository and
credentials or token for the deployment (See
`<https://pypi.org/help/#apitoken>`_ for details).

Release & Deployment
++++++++++++++++++++
The version management is performed automatically with git tags. Setting the
version is coupled with the deployment process within the CI/CD process.

To generate a new version, tag the master branch with the expected version and
push the new tag version into git:

.. code-block::

    git tag 1.0-rc1
    git push origin 1.0-rc1

On pushing new tag, a pipeline is automatically executed to control:

- code format compliance with PEP8
- code source security with plugins bandit and semgrep
- code unitary tests with Python 3.8 and Python 3.9
- code coverage computation
- deploy the release into pypi repository.

Branching model
+++++++++++++++
In git, thanks to the tag oriented release, the branching model fixes the
following rules:

- All the contributions are merged into the main branch.
- Contribution Merge Requests are merged using fast-forward mode.
- A dedicated release-xx branch can be created for post-release
  fixes(hotfixes).

Tag management
++++++++++++++
Drb project follows the `PEP440 <https://www.python.org/dev/peps/pep-0440>`_
recommendations for the tag representation. Versions are represented with the
couple of (Major, Minor) version numbers. Modifiers such as alpha (``aN``),
beta(``bN``), release candidate(``rcN``), or post release (``.postN``) are
possible as followed:

- alpha version: ``1.0a1``
- beta version: ``1.0b1``
- release candidate version: ``1.0rc1``
- final version : ``1.0``
- post release (hotfix): ``1.0.post1``
