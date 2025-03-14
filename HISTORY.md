# History

## 0.1.0 (2021-10-23)

* First release on PyPI.

## 0.2.7

* Separated logic of grid construction to a `WaferMapGrid` base class
* Python support: 3.9 - 3.13
* Updated dependency versions

## 0.2.8

* Implemented input validation
* Fixed module definition to include `WaferMapGrid`
* Fixed some issues with `conversion_factor`
* Layer visibility when exporting to html or png is now not set by the corresponding function
* made `WaferMapGrid` iterable and addressable: 
    ```python
    for cell in wm:
    ...
    wm[x]
    ```
