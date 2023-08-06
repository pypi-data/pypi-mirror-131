.. _readthedocs.org: http://www.readthedocs.org
.. _bower: http://www.bower.io
.. _sphinx: http://www.sphinx-doc.org
.. _compass: http://www.compass-style.org
.. _sass: http://www.sass-lang.com
.. _wyrm: http://www.github.com/snide/wyrm/
.. _grunt: http://www.gruntjs.com
.. _node: http://www.nodejs.com
.. _demo: http://cosmo-docs.phys.ethz.ch/uhammer/

**********************
Cosmology Sphinx Theme
**********************

View a working demo_. It is an adapted version of the readthedocs.org_. theme.



Installation
============

Via package
-----------

Download the package or add it to your ``requirements.txt`` file:

.. code:: bash

    $ pip install sphinx_pynpoint_theme

In your ``conf.py`` file:

.. code:: python

    import sphinx_pynpoint_theme

    html_theme = "sphinx_pypoint_theme"

    html_theme_path = [sphinx_pynpoint_theme.get_html_theme_path()]

