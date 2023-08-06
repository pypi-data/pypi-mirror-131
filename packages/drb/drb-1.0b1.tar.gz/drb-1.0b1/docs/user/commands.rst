.. _commands:

Command line
------------
The environment comes with a preconfigured Makefile able to set up and prepare python environment to run tests and
coverage. It also provides target to deploy new release manually.

Clean-up the environment from cache and lightweight components. It does not
removed downloaded dependencies (from venv directory), nor distributions.

.. code-block::

   make clean

The dist-clean command full cleans the repository as it has been cloned first.
Following the call of dist-clean the virtual environment and all the caches
will be removed.

.. code-block::

   make dist-clean

Run the unitary tests.

.. code-block::

   make test

Check if the source code properly follows the `PEP8` directives. This test is
also used in gitlab pipelines to accept pushed sources.
make coverage

.. code-block::

   make lint

Run the test coverage and generates a html report into htmlcov directory.

.. code-block::

   make coverage

Prepare a distribution locally into dist directory. When no tag is present on
the current commit, or modified files are present into the local directory, the
distribution process creates a dirty version to be safety deploy to the
repository.

.. code-block::

   make dist

Prepare and deploy a distribution into the gael's remote Pipy repository.
This command is run automatically when pushing a new tag.

.. code-block::

   make dist-deploy
