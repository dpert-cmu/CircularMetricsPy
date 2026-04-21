---
title: "CircularMetricsPy: A Jupyter notebook-based interface to the Ellen MacArthur Foundation's Circulytics framework" 
tags:
  - Python
  - Circular economy
  - business
  - Sustainability
  - ipywidgets
authors:
  - name: Daniel Pert
    orcid: 0000-0002-3228-9510
    affiliation: 1
  - name: Ana Inés Torres
    orcid: 0000-0001-8747-3406
    affiliation: 1
affiliations:
 - name: Department of Chemical Engineering, Carnegie Mellon University, Pittsburgh, Pennsylvania, USA
   index: 1
date: 3 January 2026
bibliography: references.bib

---

# Summary

CircularMetricsPy is a Jupyter notebook-based user interface for the calculation of a company’s Circulytics score written in Python, based on the Ellen MacArthur Foundation’s archived methodology. It uses ipywidgets to define a set of functions that create graphical user interfaces for the data entry and calculation of scores for different categories of indicators used in Circulytics, including those involving a weighted sum of answers to multiple dropdown items, checkboxes, and numerical slider widgets. The user interface widgets for each indicator are created automatically based on JSON-formatted Python dictionaries. 

# Statement of need

The circular economy is an industrial paradigm that aims to eliminate waste and natural resource extraction through product reuse and material recirculation and recycling [@dull2023building]. The circular economy has the potential to significantly reduce waste, pollution, and raw material extraction through the recovery of otherwise lost economic value of end-of-life products and materials and ensuring material needs continue to be met for future generations to enjoy. However, the transition to a circular economy requires the effort of numerous firms in different parts of the supply chain.

Circulytics is a tool developed by the Ellen MacArthur Foundation that enables a company to measure their circular economy performance, or “circularity” [@the_ellenmacarthur_foundation_circulytics-_2022]. It calculates an overall score based on a weighted sum of scores for different “themes,” each of which is based on the answers to different indicators related to that theme, which are chosen based on the economic sector of the company. Circulytics is also heavily aligned with the European Sustainability Reporting Standards (ESRS), which require companies operating in the EU to report sustainability data, and much of the data required by ESRS is already included in Circulytics.

However, the Circulytics platform is closed to submissions, making it difficult for companies to track their circularity and identify areas for improvement. Although the Circulytics methodology and list of indicators is still available for reference, it requires substantial effort for a company to calculate its Circulytics score. Our tool increases the accessibility of Circulytics for companies wishing to increase their circularity level or meet ESRS requirements but lacking the expertise or resources required to conduct an internal circularity assessment at a detailed level.

Additionally, although Circulytics was designed to measure how well a company contributes to the circular economy, it is unclear how well Circulytics aligns with broader sustainability goals and whether improvements in a firm's Circulytics score lead to burden-shifting to other companies. More broadly, there is a lack of understanding of the current circularity level of companies, which strategies are the most effective for improving circularity, and how well business-level circularity translates to overall supply chain-level circularity, sustainability, and economic gains while avoiding so-called "rebound effects," or unintended consequences of circularity improvements resulting from behavioral changes of firms or consumers [@lowe_methods_2024]. The developed tool will help researchers answer these questions by enabling the use of Circulytics in circular supply chain models that include multiple firms. We hope this will enable the improvement of Circulytics to avoid burden-shifting and more holistically measure circular performance.

# State of the field

Although various web-based tools have been developed in the context of circularity assessment, such as the Circularity Calculator [@depauw_2021], Circular Packaging Assessment Tool [@the_recycling_partnership_circular_2023], and Material Circularity Indicator (MCI) calculator [@jim_goddin_material], none of them provide a holistic assessment of circularity across company operations at the level of detail of Circulytics. Instead, most existing tools measure the circularity of a single product rather than a company and focus on materials without considering other aspects of circularity, such as water and energy. Furthermore, no publicly-available software exists to calculate a firm's Circulytics score.

# Software Design

CircularMetricsPy includes a Jupyter notebook written in Python that can be used to calculate a company's Circulytics score based on data entered into a series of graphical user interfaces (GUIs) created with [ipywidgets](https://github.com/jupyter-widgets/ipywidgets). It is designed to be consistent with the methodology published by the Ellen MacArthur Foundation and uses a generalizable API to create the GUIs based on data defining the different indicators. Thus, it not only enables user-friendly circularity assessment but is also extensible to other applications requiring mixed numeric and categorical data entry and processing, such as surveys for human subject research or quizzes assessing student understanding in academic coursework.


# Acknowledgements

This material is based upon work supported by the National Science Foundation under Award No. 2339068 (NSF CAREER Award PI AI Torres) and Eastman Chemical Company (2025 Eastman Graduate Summer Fellowship).
Disclaimer: Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the National Science Foundation or Eastman Chemical Company.

# References

