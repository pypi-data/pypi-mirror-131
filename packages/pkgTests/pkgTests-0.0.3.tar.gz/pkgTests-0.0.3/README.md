# Test Package 

[![GitHub license](https://img.shields.io/github/license/chenchih/PackageTest)](https://github.com/chenchih/PackageTest/blob/main/LICENSE)


Still on process, not ready for use yet! Currently studying and planning !



## 1. Version

- 0.0.1 inital version
- 0.0.2 update readme.md
- 0.0.3 adding init function for gui(pyautogui) and web (selenium)

## 2. Example and Description
This is a test package, which include these item:
- [x] Calculate Test
- [x] Hello world Test
- [x ] Adding PyautoGUI module
- [x] Adding selenium

### Hello World Package
> **Method name**: helloworld

```python
from pkgTest import helloworld as hello
print(hello.hellotest())

# output

```

### calculate Package
> **Method name**: calculate

- #### Calculate  sum of range X value, start to end 

```python
from pkgTest import calculate as cal
result = cal.sumvalue(1,300)
print(result) 
# output
The sum of 1, ~ 300 is: 44850 
```

- ####  Calculator operator with  two value X and Y 
```python
from pkgTest import calculate as cal
cal.add(5,5)
cal.minus(5,5)
cal.multiply(5,5)
cal.divide(5,5)

# output
10 #adding
0  #subtract
25 #multiply
1  #divide
```


- ####  GUI for pyautogui fucntion
```python
from pkgTest import gui
 gui.getvalue()
# output
Point(x=429, y=393)
```
- ####  web using selenium module to open browser
```python
from pkgTest import web 
web.webaccess("https://google.com")
# output

```

## 3. Package and Distribution building 



- #### Method 1 using setup.py

      - **File name:**
          - setup.py and setup.cfg
      - **How to build:** 

    > 1. create build: #python setup.py sdist bdist_wheel


- #### Method 2 using setup.py and setup.cfg(using metadata)

    If you want wants to convert setup.py to setup.cfg, please 

    - **How to build:**     
      
      > create build: #python setup.py sdist bdist_wheel
      
    - **Code:setup.py**       
      
       1. change setup_nocode.py to setup.py
       
       2. convert setup.py to setup.cfg  used: 
       
         `#setup-py-upgrade .`
      
      3. setup.py will overwrite as below
      
      ```
         setuptools.setup()
         import setuptools
      ```
      
     - **Code:setup.cfg**         
    ```
    [metadata]
    name = pkgTest
    version = 0.0.1
    author = ChenChih.Lee
    author_email=jacklee26@gmail.com
    description = My first Python Hello world library
    long_description = file: README.md
    long_description_content_type = text/markdown
    url = https://github.com/chenchih/PackageTest
    license = MIT
    classifiers = 
    Development Status :: 1 - Planning
    Intended Audience :: Developers
    Programming Language :: Python :: 3
    Operating System :: Unix
    Operating System :: MacOS :: MacOS X
    Operating System :: Microsoft :: Windows
    [options]
    include_package_data = True
    packages = find:
    install_requires = selenium
    [options.package_data]
    * =
        *.xml
        *.txt
    ```

- #### Method 3 using myproject.toml and setup.cfg(using metadata)

  - **How to build:**
    
     > 1. Install build package #py -m pip install --upgrade build     
     >
     > 2. Create build: 
     >
     >    #python -m build     
     >
    > 3. install it           
	  >    #pip install .    
    >    OR 
    >    #pip install package name
    
  -  **Code:** myproject.toml
  
    ```
    [build-system]
    requires = [
        "setuptools>=42",
        "wheel"
    ]
    build-backend = "setuptools.build_meta"
    ```