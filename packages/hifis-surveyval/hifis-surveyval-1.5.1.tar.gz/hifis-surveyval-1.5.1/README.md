<!--
hifis-surveyval
Framework to help developing analysis scripts for the HIFIS Software survey.

SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
-->

# HIFIS-Surveyval

This project is used to develop analysis scripts for the HIFIS Software survey.

## Table of Content

* [Installation](#installation)
* [Getting Started](#getting-started)
* [Start Analysis from Command-Line-Interface](#start-analysis-from-command-line-interface)
* [Contribute with Own Analysis Scripts](#contribute-with-own-analysis-scripts)
* [Resources](#resources)
* [Author Information](#author-information)
* [Contributors](#contributors)
* [License](#license)

## Getting Started

The project's documentation contains a section to help you as a 
[user of the analysis scripts](#getting-for-users) 
to run the analysis scripts or as a 
[developer of the framework](#getting-started-for-developers)
to set up the development environment.

### Getting Started for Users

#### Installation

To install the package locally, you can use 
[Pip](https://pip.pypa.io/en/stable/).

```shell
pip install hifis-surveyval
```

After the installation, you can use the tool from the command line with 
`hifis-surveyval --help`.

### Getting Started for Developers

#### Installation

To install the package locally, you can use 
[Poetry](https://python-poetry.org/).

#### Using Poetry

If you want to actively contribute changes to the project, you are required to
also install the development packages alongside the framework.

```shell
git clone https://gitlab.hzdr.de/hifis/overall/surveys/hifis-surveyval.git
cd hifis-surveyval
poetry install
```

After the installation, you can use the tool from the command line with 
`poetry run hifis-surveyval --help`

Poetry installs some packages that are required for performing quality checks.
Usually they are also performed via GitLab CI, but can also be executed locally.

It is common practice to run some checks locally before pushing them online.
Therefore, execute below commands:
```console
$ # Order your imports
$ isort -rc .
$ make lint
```

The following documentation references the pip installation.
You can use the same commands with a poetry installation, if you prefix your 
commands with `poetry run COMMAND`.

## Start Analysis from Command-Line-Interface

The survey analysis package is a program to be executed on the
Command-Line-Interface (CLI).

### Quick Start Example: Run Analysis

Due to sensible defaults of the project's configurations you need to have the 
analysis scripts, the preprocessing script as well as metadata and data files
in certain locations in order to run the survey analysis.
This configuration file _hifis-surveyval.yml_ which includes these defaults is
created with the command `hifis-surveyval init`.
Please put your analysis scripts into a sub-folder called _scripts_.
The preprocessing script _preprocess.py_ is expected in the root folder of the
project.
Make sure that the file _meta.yml_ is put into sub-folder _metadata_.
Finally, copy the CSV data file of your survey to a central location like a
_data_ sub-folder and tell the program the path to that data file on the
command line when running the survey analysis.

Now you can do the following to start the survey analysis from the CLI:

```shell script
hifis-surveyval analyze data/<data_file_name>.csv
```

The output is then put into a sub-folder within the folder _output_ 
which is named after the stamp of the current date-time if not specified 
differently.

**Caution:** 
Depending on the Operating System used an issue with the file 
encoding might occur.
There might be data-CSV-files around which are encoded with `UTF-8-BOM`
which causes errors when read in on Windows OS.
In this case you need to change the encoding to `UTF-8` before running
the survey analysis.

### Flags

The program accepts two flags:

1. Help flag
2. Verbosity flag

#### Help flag

Calling the program with the _help_-flag is the first thing to do
when being encountered with this program.
It outputs a so-called _Usage_-message to the CLI:

```shell script
$ hifis-surveyval --help
```

Please issue this command on the CLI and read the detailed 
_Usage_-message before continuing with reading the documentation
of the _Usage_-message here.

#### Verbosity flag

The _verbosity_-flag can be provided in order to specify the verbosity
of the output to the CLI.
This flag is called `--verbose` or `-v` for short:

```shell script
hifis-surveyval --verbose <COMMAND>
```
```shell script
hifis-surveyval -v <COMMAND>
```

The verbosity of the output can be increased even more 
by duplicating the flag `--verbose` or `-v` up to two times:

```shell script
hifis-surveyval --verbose --verbose --verbose <COMMAND>
```
```shell script
hifis-surveyval -vvv <COMMAND>
```

### Commands

There are three different commands implemented which come with its own set of
flags and parameters:

1. Command _version_
2. Command _init_
3. Command _analyze_

#### Command _version_
 
The `version` command outputs the version number of this CLI-program like so:

```shell script
hifis-surveyval version
```

#### Command _init_

Before you start the analysis you may want to change the defaults of the
configuration variables.
In order to do so, you can create a configuration file that is named 
_hifis-surveyval.yml_ by issuing the _init_ command:

```shell script
hifis-surveyval init
```

This file contains the following information:

```YAML
ANONYMOUS_QUESTION_ID: _
DATA_ID_SEPARATOR: _
HIERARCHY_SEPARATOR: /
ID_COLUMN_NAME: id
METADATA: metadata
OUTPUT_FOLDER: output
OUTPUT_FORMAT: SCREEN
PREPROCESSING_FILENAME: preprocess.py
SCRIPT_FOLDER: scripts
SCRIPT_NAMES: []
CUSTOM_PLOT_STYLE: "report_style"  # Optional
```

> ##### Concepts that You Need to Know
>
>- **QuestionCollection**: This concept refers to a set of `Questions` that 
>  cover the same topic.
>- **Question**: This concept refers to an atomic `Question` that can not be on
>  its own and needs to be wrapped up into a `QuestionCollection`.
> 
> *Note:* Other terms that may describe similar concepts are `question`
> (which equals to `QuestionCollection`) and `sub-question` (which equals to
> `Question`).

> ##### Configuration File Entries Explained
>
> - `ANONYMOUS_QUESTION_ID` defines a placeholder for Question IDs. The CSV data
>  might not explicitly mention a full ID of a Question but solely the
>  QuestionCollection ID. In this case the HIFIS Surveyval Framework adds a
>  character, by default *_* (underscore), to the QuestionCollection ID to mark
>  this situation.
> - The CSV data file is structured into header and body rows. The header row
>  consists of a comma-separated list of column names. Some column names contain
>  a separator character that concatenates the QuestionCollection ID with the
>  Question ID, the `DATA_ID_SEPARATOR`. This variable indicates which character 
>  is used to separate these IDs. If not specified otherwise, it defaults to
>  *_* (underscore).
>- This `DATA_ID_SEPARATOR` character is internally replaced by a different
>  character, the so called `HIERARCHY_SEPARATOR`, which defaults to a */*
>  (slash).
>- With `ID_COLUMN_NAME` you may want to specify the name of the _id_ column in
>  the CSV data file.
>- Each analysis needs metadata about the questions asked in the survey and
>  answers that participants may give. Setting `METADATA` specifies the location
>  of the metadata files which are by default located in a folder called
>  _metadata_. Be aware that it is recommended to have one YAML file per
>  QuestionCollection. Each YAML file then covers the metadata of a single
>  QuestionCollection and is named according to the ID of this
>  QuestionCollection.
>- You may specify the output folder by setting `OUTPUT_FOLDER` which is named
>  _output_ by default.
>- You may prefer a specific output format like _PDF_, _PNG_, _SVG_ or
>  _SCREEN_ which you may select via `OUTPUT_FORMAT`.
>  The default value is _SCREEN_.
>  Note: Be aware that other output formats like text or markdown files may be
>  created, which depends largely upon the implementation of the analysis
>  scripts.
>- You might want to tell the program where to find the preprocessing file
>  _preprocess.py_ that preprocesses and filters your survey data according to 
>  specific rules.
>  You can do so by setting `PREPROCESSING_FILENAME`.
>- You may specify the folder which contains the analysis scripts with setting
>  `SCRIPT_FOLDER`, which is the _scripts_ folder by default.
>- With `SCRIPT_NAMES` you may select a subset of the analysis scripts available
>  as a list that ought to be executed.
>  This list is empty by default, which means, all scripts are executed.

---

> **Hint for LimeSurvey Users**
>
> There is an option `Expression Manager code` in LimeSurvey when exporting the
> data into a CSV file that uses the separator character `_` (underscore) to
> concatenate QuestionCollection ID and Question ID in the CSV data header. 
> Otherwise the default `[]` is used which is not compatible with the HIFIS
> Surveyval Framework.

---

##### Additional Files Generated

Additional to the configuration file, three more files are created:

1. File _preprocess.py_ is created in the root folder of the project.
2. File _example_script.py_ is created in the _scripts_ folder of the project.
3. File _style_template.mplstyle_ is created in the _custom_plot_styles_
folder of the project.

#### Command _analyze_

The more interesting command is the `analyze` command
which comes with a _data_-parameter.
The _data_-parameter can _not_ be omitted and need to be given explicitly
in order to be able to start the analysis.
This is an example of how to do the analysis:

```shell script
hifis-surveyval analyze data/<data_file_name>.csv
```

## Contribute with Own Analysis Scripts

### Essential Requirements for Developing Own Analysis Scripts

As you might have read in the previous sections the actual analysis scripts 
reside in a specific folder called `scripts`.
All scripts in that folder will be automatically discovered by the package 
`hifis-surveyval` when running the analysis.
In order that the program recognizes the scripts in that folder as
analysis scripts they need to fulfill the following two criteria:

1. The filename need to end on `.py`.
2. The file need to contain a function called `run` without any parameters.

```python
"""
A dummy script for testing the function dispatch

.. currentmodule:: hifis_surveyval.scripts.dummy
.. moduleauthor:: HIFIS Software <software@hifis.net>
"""

def run():
    print("Example Script")
```

If both requirements are satisfied the program will execute the `run`-functions
of the analysis scripts in an arbitrary order.

### File-System Structure of the Core Component

```shell script
$ tree hifis_surveyval/
hifis_surveyval
├── cli.py
├── core
│   ├── dispatch.py
│   ├── preprocess.py
│   ├── settings.py
│   └── util.py
├── data_container.py
├── files
│   ├── example_preprocess.py
│   ├── example_script.py
│   ├── preprocess.py
│   ├── scripts
│   │   └── example-01-accessing-data.py
│   └── style_template.mplstyle
├── hifis_surveyval.py
├── models
│   ├── answer_option.py
│   ├── answer_types.py
│   ├── mixins
│   │   ├── mixins.py
│   │   ├── uses_settings.py
│   │   └── yaml_constructable.py
│   ├── question_collection.py
│   ├── question.py
│   └── translated.py
├── plotting
│   ├── matplotlib_plotter.py
│   ├── plot_styles
│   │   └── report_style.mplstyle
│   ├── plotter.py
│   └── supported_output_format.py
└── printing
    └── printer.py
```

### Matplotlib Custom Plot Styles

Files with file ending `.mplstyle` contain styling information for _Matplotlib_
plots.
An example Matplotlib plot style template called `style_template.mplstyle` is
created with the `init`-command of the _HIFIS-Surveyval_ framework.
These files can be put in a folder called `custom_plot_styles`.
Custom plot style files that are generally used within the framework need to be
put into folder `hifis_surveyval/plotting/plot_styles/`.
Plots created with _Matplotlib_ accept a `kwargs`-argument `plot_style_name`
which chooses which plot style to use for the plot.
Styles in folder `custom_plot_styles` have precedence over styles in folder
`hifis_surveyval/plotting/plot_styles/` if they have the same name.

## Resources

Below are some handy resource links:

* [Project Documentation](TODO)
* [Click](https://click.palletsprojects.com/en/7.x) is a Python package for creating beautiful command line interfaces in a composable way with as little code as necessary.
* [Sphinx](http://www.sphinx-doc.org/en/master/) is a tool that makes it easy to create intelligent and beautiful documentation, written by Geog Brandl and licnsed under the BSD license.
* [pytest](https://docs.pytest.org/en/latest/) helps you write better programs.
* [GNU Make](https://www.gnu.org/software/make/) is a tool which controls the generation of executables and other non-source files of a program from the program's source files.

## Author Information

_HIFIS-Surveyval_ was created by 
[HIFIS Software Services](https://software.hifis.net/).

## Contributors

We would like to thank and give credits to the following contributors of this
project:

* Be the first to be named here!

## License

Copyright © 2021 HIFIS Software <support@hifis.net>

This work is licensed under the following license(s):
* Everything else is licensed under [GPL-3.0-or-later](LICENSES/GPL-3.0-or-later.txt)

Please see the individual files for more accurate information.

> **Hint:** We provided the copyright and license information in accordance to the [REUSE Specification 3.0](https://reuse.software/spec/).
