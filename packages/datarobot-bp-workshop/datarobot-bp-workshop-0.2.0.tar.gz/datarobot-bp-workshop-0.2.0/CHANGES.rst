#########
Changelog
#########

0.2.0
=====

New Features
************
Adds support for newest DataRobot python client: 2.27


0.1.16
======

Bug Fixes
************
Improve support of Custom Tasks by ensuring version is properly retrieved,
set, and sent, even if the task is shared with you.


0.1.15
======

Bug Fixes
************
Fix a minor bug where `versions` were not set in certain cases on a `CustomTask`.


0.1.14
======

Bug Fixes
************
Improve support of Custom Tasks by automatically updating retrieved task
definitions for shared custom tasks, fixing issues with `to_source_code`
without manual task refresh.


0.1.13
======

New Features
************
Introduces the ability to link user-owned blueprints to and unlink
user-owned blueprints from a project

0.1.12.post1
============

Bug Fixes
************
Fix regression to `list` method, causing it to fail to execute.


0.1.12
=========

Bug Fixes
************
Update CustomTrainingModel to CustomTask to reflect changes in DataRobot Client

New Features
************
Added support for sharing and improved blueprint search support


0.1.11
=========

Bug Fixes
************
Improve stability and usability of upcoming features.

New Features
************
Added upgrade suggestion on first initialization of a Workshop, if version is outdated.


0.1.10
=========

Bug Fixes
************
Ensure an exception is raised if initialization fails, instead of only printing to stderr.

Documentation Changes
*********************
Fixes typos and image updates


0.1.9
=========

New Features
************
Backwards Compatability and New Client Version Support


0.1.8
=========

Documentation Changes
*********************
Added the DataRobot Tool and Utility Agreement links in the setup.py and documentation pages.


0.1.7
=========

New Features
************
Initial Public Release!