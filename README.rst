===============
diksiyonaryo-ph
===============

We will scrape `KWF's Diksiyonaryo website <http://diksiyonaryo.ph>`_ to use more "advanced" search queries.

Requirements
------------

This project uses a Pipfile to install and lock dependencies. Check the `pipenv <https://github.com/pypa/pipenv>`_ page for instructions on how to install pipenv on your machine.

Initial Setup
-------------

Install dependencies using pipenv: ::

    $ pipenv install

For convenience, you can also set up an alias for pipenv commands in your ``~/.bash_profile``: ::

    alias diks="pipenv run python diksiyonaryo.py"

After that we can run the app using: ::

    $ cd <project dir>
    $ diks --version
    $ diks --help
    $ diks init_db
    $ diks fetch alphabet
    $ diks fetch words
    $ diks define <word>
    $ diks search <query>
    $ diks run

Advanced Setup
--------------

We can use `direnv <https://github.com/direnv/direnv>`_ to disable pipenv's feature of automatically loading ``.env`` files by putting this in your ``.envrc``: ::

    export PIPENV_DONT_LOAD_ENV=1

Alternatively, you can create a ``.proj-env`` and add your own configuration. ::

    cp .proj-env.example .proj-env

Contributing
------------

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not ready to be an open source contributor; that your skills aren't nearly good enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at all, you can contribute code to open source. Contributing to open source projects is a fantastic way to advance one's coding skills. Writing perfect code isn't the measure of a good developer (that would disqualify all of us!); it's trying to create something, making mistakes, and learning from those mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can help out by writing documentation, tests, or even giving feedback about the project (and yes - that includes giving feedback about the contribution process). Some of these contributions may be the most valuable to the project as a whole, because you're coming to the project with fresh eyes, so you can see the errors and assumptions that seasoned contributors have glossed over.
