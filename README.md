remiendo
========

* [What is this?](#what-is-this)
* [Assumptions?](#assumptions)
* [What's in here?](#what-is-in-here)
* [Quick start](#quick-start)
* [Patch S3 graphics](#patch-pym-in-s3-graphics-produced-by-dailygraphics-rig)

What is this?
-------------

Utility repo to sync s3 locally to tweak changes without recreating & redeploying the whole project.

Useful for font fixing when moving towards https and other retrofits

Assumptions
-----------

The following things are assumed to be true in this documentation.

* You are running OSX.
* You are using Python 2.7. (Probably the version that came OSX.)
* You have [virtualenv](https://pypi.python.org/pypi/virtualenv) and [virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) installed and working.

What's in here?
-------------

* ``fabfile`` -- [Fabric](http://docs.fabfile.org/en/latest/) commands for automating setup and deployment.
* ``pym-patched`` -- Pym.js version v1.3.2
* ``app_config.py`` -- Configuration variables.
* ``requirements.txt`` -- Python requirements.

Quick Start
-------------

Bootstrap the project by forking this repo and installing the following:

```
mkvirtualenv remiendo
cd remiendo
pip install -r requirements.txt
```

You'll need to have your AWS credentials, with sufficient permissions to write on that S3 bucket ready on your env vars:
```
## AWS CONFIG
export AWS_ACCESS_KEY_ID=AKIAJXDA4G44GRJCES5Q
export AWS_SECRET_ACCESS_KEY=7RzpW9alXhZGzX+ACW+O+i0bBB/86oPncFLpiJcN
```

Patch pym in S3 graphics produced by dailygraphics rig
------------------------------------------------------

Change the `app_config.PRODUCTION_S3_BUCKET` to the S3 bucket where the graphics are stored.

Inside the `data` folder add a file with a list of the graphics slugs without slashes, one slug per line

Example `data/test.txt`:

```
azmiprimary-liveblog-20120228
bird-building-20120808
black-lung-20120709
budget-battles-20111002
```

Then run

```
fab flat.bulk_deploy_patched_pym:test.txt
```


