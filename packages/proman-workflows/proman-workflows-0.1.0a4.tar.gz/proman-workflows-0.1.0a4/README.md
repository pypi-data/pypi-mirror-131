# proman-workflows

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://spdx.org/licenses/MPL-2.0)
[![Build Status](https://travis-ci.org/python-proman/proman-workflows.svg?branch=master)](https://travis-ci.org/python-proman/proman-workflows)
[![codecov](https://codecov.io/gh/python-proman/proman-workflows/branch/master/graph/badge.svg)](https://codecov.io/gh/python-proman/proman-workflows)

## Overview

This project is a task runner to help automate common development tasks for
projects using Python.

The goal of this effort is help implement DevSecOps practices consistly with
the Software Development Lifecycle (SDLC) without burdening developers.

The objectives for achieving this goal are:
- Enforce use of commit signing
- Introduce QA tools early in development
- SAST scanning
- Encapulate processes for seamless integration with CI/CD systems
- Make TUF compliant packages for PyPI

## Install

The project can be installed using the following command:

```
pip install proman-workflows
```

The above will only install the workflows but not all dependencies. The
additional dependencies can be install with:

```
pip install proman-workflow[all]
```

### Usage

Currently, there are three command line utilities included with this install.
This is due to the primary CLI tool being under heavy development.

The `workflow-tools` command provides direct access to each of integrations
provided by the task runner. It can either be used directory or extended as
a library for additional workflows.

The `workflow-setup` command

The `workflow` command is the intended CLI for the task runner but is still
under development. It will allow control of integrated tools through abstracted
phases accessible to a developer. The functionality is still imited at this time.

### Setup

Setup a signing key for development:

```
workflow-tools setup
```

## FAQ

Q: Why should developers use this?
A: Coodinating procedures and setup for multiple team members and projects is difficult and error
prone. Task runners are purpose built to solve this problem.

Q: Why not include this using project templates?
A: Since this is distributed as a library updates and changes can be much more easilly distributed.

Q: Why not use Invocations
A: While this project is inspired by Invocations, it does not support a pluggable architecture.

## Refereces

- https://theupdateframework.io/
- https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.04232020.pdf
