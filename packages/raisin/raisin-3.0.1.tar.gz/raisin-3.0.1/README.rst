
***************************************
Raisin: To perform cluster work easily!
***************************************

.. Pour la syntaxe voir: https://deusyss.developpez.com/tutoriels/Python/SphinxDoc/
.. Pour les docstrings voir: https://numpydoc.readthedocs.io/en/latest/format.html

Project Philosophy
^^^^^^^^^^^^^^^^^^

| The main aim of project\ *raisin*\  is to \ **share physical resources**\  of your laptop with a community.
| In counterpart, you can \ **benefit from the community resources**\ .
| There are 2 sides in this project:

1. Resources usage
------------------

| The \ *raisin*\  API wants to be as close as possible to the 'threading' and 'multiprocessing' python APIs.
| The advantage in using \ *raisin*\  rather than 'threading' or 'multiprocessing' is that the computing power is greatly increased (depending on the number of connected resources).
| Though \ *raisin*\  is based on 'multiprocessing' module - that splits tasks among the resources of a single computer - it also shares the load over the different machines in the network. Everything is automatically and intelligently orchestrated relying on code analysis and graph theory.

\ *raisin*\  wants to be \ **as simple as possible**\ . That’s why the code analysis and the resources management are automated. It also uses a bunch of classes and functions default parameters that are suitable for most usages.

| However, you can tune \ *raisin*\  behavior as you want since all these parameters are \ **fully customizable**\ .
| \ *raisin*\  is a multi-OS module 100% written in python in order to keep installation reliable and simple.
| Although \ *raisin*\  uses powerful modules such as 'sympy', 'numpy', 'giacpy', 'pycryptodomex', 'tkinter'... these modules are not required (they are sometimes not easy to install). This will just lead to less efficiency, but no failure!

In a future version, \ *raisin*\  will be able to perform automatic parallelization, a little like 'pydron'.

2. Resources sharing
--------------------

| To be able to use community resources, you must give in return!
| That’s why, when \ *raisin*\  is installed as a python package, you have to install the 'application' part.
| To do this, execute the ``python3 raisin/communication/server.py`` command.

.. | The \ **security**\  is a primordial aspect.
.. | You can join or create your own cluster (e.g. friends working on a same project, ...), one at a time. The different clusters are waterproof between them. The data are encrypted. Machines must identify one another within a given cluster.

.. Your comfort while you are offering resources is guaranteed. \ *raisin*\  is \ **not intrusive**\ , it uses your resources - RAM, CPU, fan noise and bandwidth - only if they are available. Naturally, you can control how you want to share your resources (timetable, rate, ...).

Examples
^^^^^^^^

server code

.. code:: python

    import raisin

    with raisin.Server(20001) as server:
        server.serve_forever()

client code

.. code:: python

    import raisin
    from raisin.encapsulation import make_tasks

    def my_function(x):
        """just a test"""
        return x**2

    tasks_gen = make_tasks((f, f, f), ([2], [3], [4]))

    with raisin.TasksSharer(tasks_gen) as tasks_sharer:
        tasks_sharer.start()
        for res in tasks_sharer:
            print(res)


* See the `documentation <http://raisin-docs.ddns.net/>`_ for more details and examples.
