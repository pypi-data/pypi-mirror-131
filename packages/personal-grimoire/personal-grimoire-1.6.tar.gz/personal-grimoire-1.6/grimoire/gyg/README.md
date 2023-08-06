# This is used to load the most recent verion of the analytics_lib

Paste this notebook:

```py
builds_folder='dbfs:/temp/jean/grimoire'
latest_version = dbutils.fs.ls(builds_folder)[-1].path
print(f"Using version: {latest_version} ")
dbutils.library.install(latest_version)
dbutils.library.restartPython()
```
