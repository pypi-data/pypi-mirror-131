Release History
===============

**1.3.4 2021-12-15**

*   added the ``run`` command
*   added the ability to start **awftp** with a command file, to allow commands
    to be executed manually.

**1.3.3 2021-12-07**

*   output of ``lls`` now sorted by filename

**1.3.2 2021-12-06**

*   minor change in MonitoredReader

**1.3.1 2021-12-03**

*   documentation corrections

**1.3.0 2021-11-30**

*   changed API version integration so that all version-specific features
    are enabled up to the version provided by the contacted AW
*   max. API known is 3.1.0 now
*   added ``coll``, ``ìnvacc``, ``ìnvls``, ``ìnvrej`` commands
*   disabled SAML authentication, as it us not officially supported
    for FS&S API

**1.2.5 2021-11-26**

*   fixed a display flaw in a situation where the login failed
*   fixed a bug that caused not asking for a password if ``open`` was
    used without parameters

**1.2.4 2021-11-25**

*   enabled the ``progress`` command
*   fixed ``get`` so that it does not load the entire file to be downloaded in memory
    before saving to disk (credits to John Stegeman)
*   fixed ``put`` so that it works even when ``progress`` is turned off
*   the list of snapshots created by ``snap -l`` is now properly sorted
*   fixed loading/saving the command history

**1.2.2 2019-05-20**

*   tuned *get* to work properly with huge files

**1.2.0 2018-97-20**

*   added wildcards to *ls*

**1.1.6 2019-05-20**

*   tuned *get* to work properly with huge files

**1.1.5 2017-11-16**

*   fixed a bug in *ls* that caused awftp to crash for some users

**1.1.4 2017-11-01**

*   fixed a bug that made *readline* unusable on MacOS

**1.1.3 2017-10-30**

*   fixed a bug that caused awftp to crash on the *lpwd* and *status* commands
    when the local directory doesn't exist (deleted underneath)

**1.1.2 2017-09-22**

*   added a macOS binary
*   now more tolerant when opening the history file fails

**1.1.1 2017-08-29**

*   fixed a typo in the installation description (thanks to Guido H.)

**1.1.0 2017-06-23**

*   added an option to list the Identity Providers supported by HCP Anywhere
*   added an option to authenticate against a SAML IDP
    --> tested against ADFS SAML IDP only at this time
*   removed the *idps* command, as it is useless now

**1.0.3 2017-06-14**

*   fixed pip install

**1.0.2 2017-06-14**

*   CTRL-D now equals the *bye* command
*   new command:

    *   *idps* - list identity providers supported by the AW server

**1.0.1 2017-05-21**

*   fixed a bug that caused *ls* to fail while a snapshot was active

**1.0.0 2017-05-19**

*   now supporting HCP Anywhere FS&S API 3.0.0
*   added support for multiple FS&S API versions (always trying to use the
    highest one). New/updated commands:

    *   *get* - added progress meter
    *   *hist* - shows the history of a file
    *   *link* - added ``-d`` to delete a link
    *   *links* - list active links
    *   *put* - added ``-u`` to update an existing file, added progress meter
    *   *search* - allows to search for folder/files with a specific pattern
        in their name
    *   *snap* - allows to work with the data at a given snapshot
    *   *restore* - restore deleted files and previous versions of files
    *   *user* - info about the user's settings in HCP Anywhere

*   added ability to force using a specific FS&S API version (``--api``)
*   added the possibility to cancel a command by CTRL-C w/o leaving **awftp**
*   added handling loss of connection to Anywhere server
*   added the ability to start awftp w/o telling a HCP Anywhere server on the
    command line (similar to ftp, use *open* inside **awftp**)
*   Now catching UnicodeEncodeErrors to remind the user to use an UTF-8 system
    language

**0.2.0 2017-04-02**

*   fixed a bug in setup.py

**0.1.9 2017-02-15**

*   re-factored the code for single-file binary creation using pyinstaller
*   Fixed a bug that caused awftp to crash when using **lls**
*   Fixed a missing dependency for *click*

**0.1.7 2016-11-09**

*   Fixed failing imports


**0.1.5 2016-07-07**

*   Changed getting the user's id from pwd.getpwuid() to os.getuid() for
    Windows compatibility

**0.1.4 2016-06-16**

*   some work to get it into pypi


**0.1.0 2016-06-13**

*   initial release
