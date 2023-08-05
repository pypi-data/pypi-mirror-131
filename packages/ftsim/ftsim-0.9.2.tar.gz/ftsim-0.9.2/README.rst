.. Sollte mit index.rst in docs abgestimmt sein !


FTSim - Warehouse Transport Simulation
======================================

This Python Package simulates and visualizes the transport of loadunits 
in a simple warehouse environment. 

Different layouts and optionally orders are stored in a database
and can be used, changed, added by the user.

The loadunits can be transported in and between areas, like
conveyor belts, workstations for picking and storage areas.
This can be done manually, automatically or driven by orders.

The basic idea of this project was dealing with the question
if the time required for a batch of orders is predictable.

Work in progress
================

The  Softwareproject `FTSim` is still **at work**, and the documentation is not finished,
but runs stable under MS-Windows and linux, and probably also under MacOS.

If You have any questions, suggestions, corrections,
don't hesitate to contact me at g.w.sachs@gmx.de.

Audiance
========

The project can be used just for playing, or to train sql skills.
For developers the combination of tkinter, sqlite and threading
might be of interest. The main iussue was about the question if the time required for a batch of orders
is predictable.

Installation
============
The project does not need any extra packages, its all in
the standard library. 
Make sure you are using python3:

.. code-block:: text

    $ pip install ftsim

and run it:

.. code-block:: text

    $ ftsim

Documentation
=============

`<https://ftsim.readthedocs.io>`_

It will look like this
======================

.. image:: https://github.com/gerpark/ftsim/raw/master/prj105layout.png 

