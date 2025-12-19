import math, json, numpy as np, pandas as pd
import ipywidgets as w
from ipywidgets import interact_manual, FloatText, VBox, Output, Label
from IPython.display import display, Markdown

from indicator_list import *
# Theme 8 weighting information
ASSET_AVG_MASS = {
    'IT equipment': 0.01,              # t/item
    'Textiles': 0.001,                 # t/item
    'Furniture': 0.05,                 # t/item
    'Buildings': 2.5,                  # t/m2
    'Heavy machinery': 50.0,           # t/item
    'Mid-weight machinery': 25.0,      # t/item
    'Light machinery': 0.5,            # t/item
    'Heavy transport': 1000.0,         # t/item
    'Mid-weight transport': 500.0,     # t/item
    'Light transport': 5.0,            # t/item
    'Warehousing equipment': 0.05      # t/item
}
ASSET_GROUPS = list(ASSET_AVG_MASS.keys())

def asset_row_widgets(label):
    asset_label = w.Label(value=f"{label} mass (t, FY)", layout=w.Layout(width='200px'), style = {'description_width': 'initial'})
    mass_label = w.Label(value = f"{ASSET_AVG_MASS[label]} t/item" if label != "Buildings" else f"{ASSET_AVG_MASS[label]} t/m2", layout=w.Layout(width='120px'))
    mass_estimate = w.FloatText(value=0.0, disabled=False, layout=w.Layout(width='200px'),style = {'description_width': 'initial'})
    
    return {
        'name': label,
        'mass_widget': mass_estimate,
        'mass_box': w.HBox([asset_label, mass_label, mass_estimate]),
        'applicable_and_mass_not_available': w.Checkbox(value=False, layout=w.Layout(width='200px')),
        'not_applicable': w.Checkbox(value=False, layout=w.Layout(width='150px')),
    }

asset_widgets_procured = [asset_row_widgets(a) for a in ASSET_GROUPS]
asset_widgets_owned = [asset_row_widgets(a) for a in ASSET_GROUPS]

header_row = w.HBox([
    w.Label(value='Asset Category', layout=w.Layout(width='200px')),
    w.Label(value='Average mass', layout=w.Layout(width='120px')),
    w.Label(value='Mass estimate (metric tonnes)', layout=w.Layout(width='200px')),
    w.Label(value='Applicable and mass estimate not available', layout=w.Layout(width='275px')),
    w.Label(value='Not applicable', layout=w.Layout(width='150px')),
])

prompt_0q_part1 = w.HTML('<h3>0q. Part 1. For each plant, property, and equipment assets category that your company has procured (either to own or to lease) in the financial year stated at the beginning of the assessment, what is the total mass (metric tonnes) of each category?</h3><p>If you do not have the total mass, but know the number of items in each asset category, use the average mass in the table below to estimate the total mass for each asset category.</p>')
asset_rows_procured = [prompt_0q_part1, header_row]

prompt_0r_part1 = w.HTML('<h3>0r. Part 1. For all the plant, property and equipment assets that are procured during or before the financial year (FY) stated at the beginning of the assessment (and are owned or leased by your company at any point during the FY), what is the total mass (metric tonnes) of each category?</h3><p>If you do not have the total mass, but know the number of items in each asset category, you can use the average mass in the table below to estimate the total mass for each asset category.</p>')
asset_rows_owned = [prompt_0r_part1, header_row]

for r in asset_widgets_procured:
    asset_rows_procured.append(w.HBox([r['mass_box'], r['applicable_and_mass_not_available'], r['not_applicable']]))
for r in asset_widgets_owned:
    asset_rows_owned.append(w.HBox([r['mass_box'], r['applicable_and_mass_not_available'], r['not_applicable']]))
ui_8_procured = w.VBox(asset_rows_procured)
ui_8_owned = w.VBox(asset_rows_owned)

prompt_0q_part2 = w.HTML('<h3>0q. Part 2. For each plant, property, and equipment asset category procured in the financial year stated at the beginning of the assessment: Select asset categories that cover a minimum of 80% of the mass estimates provided in 0q. Part 1.</h3>')
subprompt_0q_part2 = w.HTML('<h4>Your selections here will be used to inform the relevance and weighting of asset groups in indicator 8b.</h4>')
header = w.Label(value='Asset group', layout=w.Layout(width='200px'))
asset_selection_table_0q = w.VBox([prompt_0q_part2,subprompt_0q_part2, header] + [w.Checkbox(value=False, description=a, indent=False) for a in ASSET_GROUPS])

prompt_0r_part2 = w.HTML('<h3>0r. Part 2. For each plant, property and equipment asset category procured during or before the financial year (FY) stated at the beginning of the assessment (and owned or leased at any point during the FY). Select asset categories that cover a minimum of 80% of the mass estimates provided in 0r. Part 1.</h3>')
subprompt_0r_part2 = w.HTML('<h4>Your selections here will be used to inform the relevance and weighting of asset groups in indicator 8b.</h4>')
header = w.Label(value='Asset group', layout=w.Layout(width='200px'))
asset_selection_table_0r = w.VBox([prompt_0r_part2, subprompt_0r_part2, header] + [w.Checkbox(value=False, description=a, indent=False) for a in ASSET_GROUPS])
