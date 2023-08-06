# mobrob

### install from files

```console
pip install -e .
```

### install via pip
package the library
```console
python setup.py sdist
```

upload .tar.gz file under `dist/` to pypi
```console
twine upload dist/{packaged file}.tar.gz
```

install
```console
pip install mobrob
```
