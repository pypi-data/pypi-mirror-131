# BluePrint

`BluePrint` is a light-weight tool that helps configure Python objects with YAML files.

Installation is simple:

```
pip install py-blueprint
```

Or you can checkout its source code from `https://github.com/YANG-H/BluePrint`. And install it with

```
python setup.py install
```

There is a simple sample code in the repository. Run it with:

```
python -m blueprint.run sample/hello_world/simple_run.yaml --name AnythingYouLike
```

If GPU is available and PyTorch is installed, you can also run a distributed version:

```
python -m blueprint.run sample/hello_world/simple_run.yaml --name AnythingYouLike --distributed 1
```

`BluePrint` is in very early design and development. Please contact me at [yanghao.alexis@foxmail.com](mailto:yanghao.alexis@foxmail.com) or raise issues for bug reporting and other suggestions.

## License

`BluePrint` is released under the MIT license. 