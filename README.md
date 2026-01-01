# Circulytics calculator

## Statement of need
The Circulytics calculator is a Jupyter notebook-based user interface written in Python that calculates a company’s Circulytics score based on the Ellen MacArthur Foundation’s [archived methodology](https://www.circulytics.com/). It uses [ipywidgets](https://github.com/jupyter-widgets/ipywidgets) to define a set of functions that create graphical user interfaces for the data entry and calculation of scores for different categories of indicators used in Circulytics, including those involving a weighted sum of answers to multiple dropdown items, checkboxes, and numerical slider widgets. The user interface widgets for each indicator are created automatically based on JSON-formatted Python dictionaries. 
Since the Circulytics platform is closed to submissions, it is difficult for companies to track their circularity and identify areas for improvement. Although the Circulytics methodology and list of indicators is still [available for reference](https://www.ellenmacarthurfoundation.org/resources/circulytics/resources), it requires substantial effort for a company to calculate its Circulytics score. Thus, our tool increases the accessibility of Circulytics to companies wishing to increase their circularity level by enabling user-friendly circularity assessment.

The Circulytics calculator not only enables user-friendly circularity assessment but is also extensible to other applications requiring mixed numeric and categorical data entry and processing, such as surveys for human subject research or quizzes assessing student understanding in academic coursework.


