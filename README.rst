===============
diksiyonaryo-ph
===============

We will scrape `KWF's Diksiyonaryo website <http://diksiyonaryo.ph>`_ to use more "advanced" search queries.

Requirements
------------

This project uses Python 3. We recommend using `pyenv <https://github.com/pyenv/pyenv>`_ to switch between different versions of Python in your machine.

Pipfile is used for installing and locking the dependencies. Check the `pipenv <https://github.com/pypa/pipenv>`_ page for instructions on how to install pipenv on your machine.

Finally, for the database, you need to install `MongoDB <https://www.mongodb.com/>`_.

Initial Setup
-------------

Install dependencies using pipenv: ::

    $ pipenv install

For convenience, you can also set up an alias for pipenv commands in your ``~/.bash_profile``: ::

    alias diks="pipenv run python diksiyonaryo.py"

After that we can run the app using: ::

    $ cd <project dir>  # go to the project directory
    $ diks init         # initialize the database
    $ diks fetch        # fetch data from http://diksiyonaryo.ph
    $ diks run          # run the app

For a list of commands, you can run: ::

    $ diks --help

Advanced Setup
--------------

You can pass a settings file (.py) to the app using the ``--settings`` flag: ::

    $ diks --settings=config.settings.custom init

For an easy way to modify your settings, you can create a ``.env`` file in the project's root directory to store your environment variables. This will automatically be loaded by pipenv. ::

    $ touch .env

Alternatively, you can also use ``.proj-env`` to add your own configuration. ::

    $ cp .proj-env.example .proj-env

You can use ``.proj-env`` if you don't want pipenv to load it automatically. You can also use `direnv <https://github.com/direnv/direnv>`_ to disable pipenv's feature of automatically loading ``.env`` files by putting this in your project's ``.envrc``: ::

    export PIPENV_DONT_LOAD_ENV=1

Easy Stats
----------

We ran ``diks fetch`` and got 67689 words across 689 pages. ::

    words_count = {
        'P': 8559,  # 86 pages
        'S': 6295,  # 63 pages
        'B': 6225,  # 63 pages
        'K': 5792,  # 58 pages
        'A': 5210,  # 53 pages
        'T': 5078,  # 51 pages
        'L': 4019,  # 41 pages
        'M': 3653,  # 37 pages
        'D': 3529,  # 36 pages
        'H': 2982,  # 30 pages
        'I': 2522,  # 26 pages
        'G': 2291,  # 23 pages
        'E': 1889,  # 19 pages
        'C': 1397,  # 14 pages
        'R': 1335,  # 14 pages
        'O': 1277,  # 13 pages
        'N': 1171,  # 12 pages
        'F': 995,   # 10 pages
        'U': 986,   # 10 pages
        'W': 739,   # 8 pages
        'V': 501,   # 6 pages
        'J': 270,   # 3 pages
        'Y': 269,   # 3 pages
        'Q': 257,   # 3 pages
        'Ng': 256,  # 3 pages
        'Z': 140,   # 2 pages
        'X': 44,    # 1 page
        'Ñ': 8,     # 1 page
    }
    
    classes_count = {
        '.definition-text': 93006,
        '.definition': 92797,
        '.sense-counter': 92797,
        '.sense-content': 92797,
        '.sense': 92797,
        '.gray': 77137,
        '.divider': 77137,
        '.pos': 67689,
        '.pronunciation': 67689,
        '.etymology': 61831,
        '.domain': 25421,
        '.sense-synonyms': 17023,
        '.alternate-pronunciation': 16562,
        '.sense-confer': 3958,
        '.derivative': 2386,
        '.sense-affixForms': 2154,
        '.sense-variant': 1789,
        '.definition-example': 1098,
        '.subsense-counter': 380,
    }

Running Tests
-------------
Run ``py.test`` from diksiyonaryo: ::

    $ cd <project dir>
    $ diks test

Contributing
------------

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not ready to be an open source contributor; that your skills aren't nearly good enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at all, you can contribute code to open source. Contributing to open source projects is a fantastic way to advance one's coding skills. Writing perfect code isn't the measure of a good developer (that would disqualify all of us!); it's trying to create something, making mistakes, and learning from those mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can help out by writing documentation, tests, or even giving feedback about the project (and yes - that includes giving feedback about the contribution process). Some of these contributions may be the most valuable to the project as a whole, because you're coming to the project with fresh eyes, so you can see the errors and assumptions that seasoned contributors have glossed over.
