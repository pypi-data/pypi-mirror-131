Savory
======

About
-----

Savory is a cli tool for managing saltstack git repositories

Commandline
-----------

.. code:: shell

    Usage: savory [OPTIONS]

    Options:
      -f, --file TEXT         repository file
      -r, --repo TEXT         repository file repo
      -t, --tag TEXT          repository file tag
      -d, --destination TEXT  repository file destination
      --help                  Show this message and exit.

fetch reposities from a local repository file:

.. code:: shell

    savory --file localfile.yml

fetch reposities from a repository file in a git repo:

.. code:: shell

    savory --file repofile_in_repo.yml \
           --repo git@gitserver:saltstack/savory.git \
           --tag master \
           --destination /tmp

Repository file example
-----------------------

.. code:: yaml

    defaults:
      destination: /srv/salt
      type: formula

    repositories:
      - formula1
      - formula2
      - formula3
      - pillar_data

    formula1:
      repo: git@gitserver:saltstack/formula1.git
      tag: 1.0.0

    formula2:
      repo: git@gitserver:saltstack/formula2.git
      tag: 1.0.1

    formula3:
      repo: git@gitserver:saltstack/formula3.git
      tag: 1.0.3

    pillar_data:
      repo: git@gitserver:saltstack/pillar_data.git
      tag: prod
      destination: /srv/pillar
      type: pillar

In the above example formula1, formula2 and formula3 are using git tags
(recommended for formulas) and a branch for the pillar\_data repo.

Install
-------

-  install savory

   .. code:: shell

       pip3 install savory

-  create a new git user and make sure that this user has quest
   permissions to all repositories that you want to manage with savory
-  create a new keypair and place the keys in .ssh

   .. code:: shell

       [root@salt-master ~]# ssh-keygen -t ed25519
       Generating public/private ed25519 key pair.
       Enter file in which to save the key (/root/.ssh/id_ed25519): /root/.ssh/gitlab
       Enter passphrase (empty for no passphrase): 
       Enter same passphrase again: 
       Your identification has been saved in /root/.ssh/gitlab.
       Your public key has been saved in /root/.ssh/gitlab.pub.
       The key fingerprint is:
       SHA256:abcdefghijklmnopqrstuvwABCDEFGHIJKLMNOP+RST root@salt-master
       The key's randomart image is:
       +--[ED25519 256]--+
       |  BX^.+.   . o ..|
       |..o^.@ ..o. . o. |
       |+++.%   +.      .|
       |o=.o .   .    .. |
       |o..     S    . E.|
       |.             . .|
       |             . . |
       |              o  |
       |             .   |
       +----[SHA256]-----+

-  adjust the gitlab user in gitlab and add the public key generated in
   the previous step to this user
-  copy the systemd files from
   https://gitlab.com/solvinity/savory/-/tree/main/systemd and place
   them in /etc/systemd/system
-  enable savory.timer by running

   .. code:: shell

       systemctl enable savory.timer

-  verify in journalctl if the repositories are cloned to the configured
   location specified in the repository file.

To-do
-----

Implement cleanup/delete of unused repositories
