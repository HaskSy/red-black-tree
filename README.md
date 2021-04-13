# Red-Black Tree

Standard red-black tree implementation. For now supports only addition of non-duplicate values. 

This implementation was made especially for JetBrains Internships 2021


# Testing

to run tests using console:
 * Please launch tests from the root directory of project
 * If you want to run all test files (well now there is only one), then type in console:
```bash
python -m unittest discover tests
```
 * If you want to run one exact test, then, for example, type:
```bash
python -m unittest tests/test_RBTree.py
```
or any other test file.


Things which are tested:

1) test_RBTree.py - non-randomized tests
    * Default comparator checking
    * Check proper work of find() and contains() function 
    * Testing left and right rotation
    
2) test_random_inputs.py - randomized tests
    * For each test func creates 20 different arrays with 25 or less data.
    * Testing include() (avoiding taking attributes from NoneType)
    * Checking tree for coloring mistakes