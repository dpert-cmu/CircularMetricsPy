# CircularMetricsPy

## Statement of need
CircularMetricsPy is a Jupyter notebook-based user interface written in Python that calculates a company’s Circulytics score based on the Ellen MacArthur Foundation’s [archived methodology](https://www.circulytics.com/). It uses [ipywidgets](https://github.com/jupyter-widgets/ipywidgets) to define a set of functions that create graphical user interfaces for the data entry and calculation of scores for different categories of indicators used in Circulytics, including those involving a weighted sum of answers to multiple dropdown items, checkboxes, and numerical slider widgets. The user interface widgets for each indicator are created automatically based on JSON-formatted Python dictionaries in `params.py`. 

Since the Circulytics platform is closed to submissions, it is difficult for companies to track their circularity and identify areas for improvement. Although the Circulytics methodology and list of indicators is still [available for reference](https://www.ellenmacarthurfoundation.org/resources/circulytics/resources), it still requires substantial effort for a company to calculate its Circulytics score manually. By enabling user-friendly circularity assessment, our tool makes Circulytics more accessibile to companies wishing to increase their circularity level.

The Circulytics calculator is also extensible to other applications requiring mixed numeric and categorical data entry and processing, such as surveys for human subject research or quizzes assessing student understanding in academic coursework.
## Installation instructions
After cloning the repository, run `pip install -e .` from the root directory to install the package.

Dependencies:
- ipywidgets
- numpy
- pandas
- json
- IPython
- ipykernel
## Example usage
see [CircularMetricsPy.ipynb](https://github.com/dpert-cmu/circulytics_calculator/blob/main/CircularMetricsPy.ipynb)
## API documentation
see [API_documentation.md](https://github.com/dpert-cmu/circulytics_calculator/blob/main/API_documentation.md)
## Community guidelines
## Tests
see [Test_cases.md](https://github.com/dpert-cmu/circulytics_calculator/blob/main/tests/Test_case.md)
