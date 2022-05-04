# edgepi-python-sdk

## SDK packaging

- Use setup.py file to edit meta-data when building/created new package
- run ```python -m build``` command in root directory of the SDK create distribution
- run ```py -m twine upload --repository testpypi dist/*``` command to upload the distribution to TestPyPi

## SDK Structure
```
EdgePi-Python-SDK/
├─ DAC/
│  ├─ submodule1.py
│  ├─ submodule2.py
│  ├─ ...
├─ GPIO/
│  ├─ submodule.py
│  ├─ ...
├─ ADC/
│  ├─ submodule.py
│  ├─ ...
├─ LED/
│  ├─ submodule.py
│  ├─ ...
├─ Tests/
│  ├─ Test1.py
│  ├─ ...
package files
build files
readme

```

- Tests folder is excluded from distribution build
- Each module can include multiple python files as needed
- Each module includes quick start sample class that can run right after the installation of the package
