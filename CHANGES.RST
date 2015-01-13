
Change Log for **CodeFurther**
==============================

v0.1.0.dev6 13th January 2015
-----------------------------
* Added Pull request from @msabramo SHA: cbcbafea74e1998e3740033e0271ab3cb11adc20 to remove additional restructured text chars that break the PyPI module
* Added dev requirement for restview so that I can test for the above
* Added setup requirement for python-gmaps (install_requires)
* Added setup requirement for requests-cache (install_requires)

v0.1.0.dev5 12th January 2015
-----------------------------
* Tidied files in the MANIFEST.in
* Included NULL.rst in the MANIFEST.in
* Included requirements files in the MANIFEST.in - not sure if they should be there yet as I'm learning about packaging Python modules
* Changes the MANIFEST.in to include codefurther/package_info.json
* Update CHANGES.RST
* Renamed CHANGES.rst to have lowercase extension
* Removed orphaned top40demo.py file from project route

v0.1.0.dev4 10th January 2015
-----------------------------
* Minor fix to requirements files

v0.1.0.dev3 10th January 2015
-----------------------------
* Minor fix to requirements files

v0.1.0.dev2 10th January 2015
-----------------------------
* Merged PythonTop40 v0.1.6 (not 0.1.5 as the branch suggests)
* Added support for requests cache for top40
* Moved requests cache temp file to temp directory
* Made the test FileSpoofer class generic across multiple tests
* Added tests to check for malformed JSON in lyrics
* Removed some redundant tests
* Added code to test directions
* Added artist_exists() method for the lyrics module
* Changed the way lyrics handles HTTP errors
* Created helpers module for functions/classes across different modules
* Added PY2 / PY3 compatible code to several modules

**ToDo**:

* Add weather forecast support
* Add Premiership football leagues
* Add IMDB / Movie DB querying
* Lots of other ideas too
* etc.