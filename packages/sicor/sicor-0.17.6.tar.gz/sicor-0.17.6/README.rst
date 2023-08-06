
.. image:: https://enmap.git-pages.gfz-potsdam.de/sicor/doc/_static/sicor_logo_lr.png
   :width: 300px
   :alt: SICOR Logo

=================================================
SICOR - Sensor Independent Atmospheric Correction
=================================================

Sensor Independent Atmospheric Correction of optical Earth Observation (EO) data from both multispectral and
hyperspectral instruments. Currently, SICOR can be applied to Sentinel-2 and EnMAP data but the implementation of
additional space- and airborne sensors is under development. As a unique feature for the processing of hyperspectral
data, SICOR incorporates a three phases of water retrieval based on Optimal Estimation (OE) including the calculation of
retrieval uncertainties. The atmospheric modeling in case of hyperspectral data is based on the MODTRAN® radiative
transfer code whereas the atmospheric correction of multispectral data relies on the MOMO code. The MODTRAN® trademark is
being used with the express permission of the owner, Spectral Sciences, Inc.

* Please check the documentation_ for installation and usage instructions and in depth information.
* Information on how to **cite the SICOR Python package** can be found in the
  `CITATION <https://git.gfz-potsdam.de/EnMAP/sicor/-/blob/master/CITATION>`__ file.


License
-------
Free software: GNU General Public License v3 or later (GPLv3+)

All images contained in any (sub-)directory of this repository are licensed under the CC0 license which can be found
`here <https://creativecommons.org/publicdomain/zero/1.0/legalcode.txt>`__.

Feature overview
----------------

* Sentinel-2 L1C to L2A processing
* EnMAP L1B to L2A processing
* generic atmospheric correction for hyperspectral airborne and spaceborne data
* retrieval of the three phases of water from hyperspectral data
* calculation of various retrieval uncertainties
  (including a posteriori errors, averaging kernels, gain matrices, degrees of freedom, information content)
* atmospheric correction for Landsat-8: work in progress
* CH4 retrieval from hyperspectral data: work in progress

Status
------

|badge1| |badge2| |badge3| |badge4| |badge5| |badge6| |badge7| |badge8| |badge9|

.. |badge1| image:: https://git.gfz-potsdam.de/EnMAP/sicor/badges/master/pipeline.svg
    :target: https://git.gfz-potsdam.de/EnMAP/sicor/pipelines

.. |badge2| image:: https://git.gfz-potsdam.de/EnMAP/sicor/badges/master/coverage.svg
    :target: https://git.gfz-potsdam.de/EnMAP/sicor/coverage/

.. |badge3| image:: https://img.shields.io/static/v1?label=Documentation&message=GitLab%20Pages&color=orange
    :target: https://enmap.git-pages.gfz-potsdam.de/sicor/doc/

.. |badge4| image:: https://img.shields.io/pypi/v/sicor.svg
    :target: https://pypi.python.org/pypi/sicor

.. |badge5| image:: https://img.shields.io/conda/vn/conda-forge/sicor.svg
        :target: https://anaconda.org/conda-forge/sicor

.. |badge6| image:: https://img.shields.io/pypi/l/sicor.svg
    :target: https://git.gfz-potsdam.de/EnMAP/sicor/-/blob/master/LICENSE

.. |badge7| image:: https://img.shields.io/pypi/pyversions/sicor.svg
    :target: https://img.shields.io/pypi/pyversions/sicor.svg

.. |badge8| image:: https://img.shields.io/pypi/dm/sicor.svg
    :target: https://pypi.python.org/pypi/sicor

.. |badge9| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5535505.svg
   :target: https://doi.org/10.5281/zenodo.5535505

See also the latest coverage_ report and the nosetests_ HTML report.

History / Changelog
-------------------

You can find the protocol of recent changes in the SICOR package
`here <https://git.gfz-potsdam.de/EnMAP/sicor/-/blob/master/HISTORY.rst>`__.

Credits
-------

This software was developed within the context of the EnMAP project supported by the DLR Space Administration with
funds of the German Federal Ministry of Economic Affairs and Energy (on the basis of a decision by the German
Bundestag: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.

The MODTRAN® trademark is being used with the express permission of the owner, Spectral Sciences, Inc.

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
.. _documentation: https://enmap.git-pages.gfz-potsdam.de/sicor/doc/
.. _coverage: https://enmap.git-pages.gfz-potsdam.de/sicor/coverage/
.. _nosetests: https://enmap.git-pages.gfz-potsdam.de/sicor/nosetests_reports/nosetests.html
