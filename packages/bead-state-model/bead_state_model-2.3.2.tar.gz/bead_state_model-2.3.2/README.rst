
``bead_state_model``
====================

``bead_state_model`` is a python package to simulate biopolymers like actin and microtubules.
Polymers are modeled as linearly connected beads. The polymers can form connections
via cross-links or motors. Instead of explicitly simulating these binding
proteins, they are implicitly represented by the state of a bead in a polymer,
hence the name ``bead_state_model``.

.. image:: docs/_static/species_isolated_and_reactions.svg
   :width: 50%
   :align: center

This package was developed with systems that include *external* particles in mind.
``bead_state_model`` is a wrapper around the simulation framework `ReaDDy2 <https://readdy.github.io/>`_,
and leverages ReaDDy's python API to implement polymers, cross-links and motors. To
add non-polymer particles, the user can make full use of ReaDDy's functionality to define
particles and bonds and reactions between particles. This allows users to build systems like
these:

.. figure:: docs/_static/systems_microrheo_and_indentation.svg
   :align: center

   (Left) Slice of a cross-linked 3D network with a passive microsphere for microrheology measurements.
   (Right) A microsphere gets pressed into a layer of polymers.

You can find the project page on `gitlab <https://gitlab.com/ilyas.k/bead_state_model>`.
A built version of the documentation is on our `lab website <http://akbg.uni-goettingen.de/docs/bead_state_model/>`_

Install
-------

The full install instructions can be found in the
`online manual <http://akbg.uni-goettingen.de/docs/bead_state_model/install.html>`_.

In short:

1. Install `miniconda3 <https://docs.conda.io/en/latest/miniconda.html>`_.
2. Install readdy in a new environment:

  .. code:: bash

     # add conda-forge channel
     conda config --add channels conda-forge
     conda config --set channel_priority strict

     # create environment
     conda create -n bead_state python=3.9

     # activate new environment
     conda activate bead_state

     conda install readdy==2.0.9

3. Install ``bead_state_model``:

  .. code:: bash

     pip install bead-state-model

For Developers
--------------

The ``Makefile`` is the central place of "documentation" of the development pipeline.
Have a look at the make targets ``build``, ``upload`` and ``test``. Tests
of the examples (command ``pytest tests/examples``) require the ``actomyosin-analyser``
package to be installed. So in order to run tests, you can install your local project
folder in editable mode with

.. code::

   pip install -e .[test]

Another option is to also clone the
`actomyosin-analyser project <https://gitlab.com/ilyas.k/actomyosin_analyser>`_
and install it in editable mode in the same virtualenv, since it
is recommended to perform all analyses with that package, and changes to
``bead_state_model`` might make adaptations in ``actomyosin_analyser`` necessary anyway.
Before you commit changes to the master branch, make sure that all tests are passed. There
is no continuous integration pipeline configured currently, since I didn't manage
to set it up properly with conda (conda makes it a bit tricky, since all commands are
executed with ``/bin/sh`` rather than ``/bin/bash`` for which conda was configured).