# Notes to remind myself how to deploy new versions

* Setup pypy acct, login, verify and whatnot.
* Update setup.cfg and setup.py, minimally with version change, but any other additions too.
* Scripts get added to setup.pt
* Confirm tests pass
* Tag version, commit to GH. Confirm GH action tests pass.
* Create pypy release
** python setup.py sdist bdist_wheel
** twine upload dist/*
*** Enter un/pw for pypipypi
* That should be it.   test it out, pip install, try running a script.
