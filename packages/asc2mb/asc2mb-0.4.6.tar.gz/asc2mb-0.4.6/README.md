# aSc to ManageBac

## Getting started

Requires Python 3.6 or above. Install Python at [python.org](https://www.python.org). Installing Python also installs a package manager (called `pip`) that can install the command `asc2mb` into your command line enviornment.

After instally Python, open the terminal or command line or PowerShell, and peform the following:

```sh
pip install asc2mb
```

If for some reason the `pip` command doesn't work, you can manually install it by following [the relevant instructions](https://pip.pypa.io/en/stable/installing/) for your system.

### Upgrade

Should you need to update to the latest version, you can do:

```
pip install --upgrade asc2mb
```

## Use

After `pip install` worked, it is now installed on your path, and the command `asc2mb` is now available:

```
asc2mb ~/path/to/xml.xml ~/path/to/save/timetable.csv ~/path/to/save/classes.csv
```

It takes only a second to run. It reports how many records it processed. 

## Miscellaneous

The command takes three required arguments, and there are additional options as well. The three required arguments tell the program where the xml file is located, and where to save the two csv files. 

The options depend on your school's needs. For example, the class id is how ManageBac knows which class you are referring to, so that program helps you derive the class ID based on information contains in the xml file. It's up to you to ensure there are classes that have those IDs in managebac, but the program does produce a csv so that they can be uploaded in bulk.

By default, class id uses the pattern `{class_.short}_{division.name}`, which means "the short name of the class" plus an underscore, plus the name of the division." At the time of publication, having a different pattern is only possible by contacting the author (or, if you're a keen developer, add a pull request).

If you run the program without any options, it'll prompt you to enter them.

```ssh
asc2mb path_to_xml path_to_classes_output_file path_to_timetable_output_file
```






