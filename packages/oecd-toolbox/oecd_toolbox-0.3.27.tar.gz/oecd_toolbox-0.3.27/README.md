# OECD Toolbox
A library of abstract classes that can serve as a skeleton for writing downloaders and converters for DbNomics style fetchers.
Additionally it contains utility/helper functions to handle common operations or transformations in both the downloading and conversion process.   


## Build the project

To build the project, after changes, make sure the version number in _setup.cfg_ is updated.
Then issue the following command:

```powershell
python -m build
```


## Publish the project on pypi.org
WARNING!!! make sure no confidential data is stored in the published package

The package is published on pypi.org. Manually manage the available variants of the package [here](https://pypi.org/manage/project/oecd-toolbox/releases/).
Access details are stored in the Practices teams access details store.

To push the distributions that are available in the toolbox's _dist_ folder use twine with the commandline:

```powershell
twine upload dist/*
```


