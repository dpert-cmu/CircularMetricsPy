# API Documentation

## Table of Contents

1. [Utility Functions](#utility-functions)
2. [Weighting Functions](#weighting-functions)
3. [UI Building Functions](#ui-building-functions)
4. [Widget Creation Functions](#widget-creation-functions)

---

## Utility Functions

### `clip_0_to_100(x)`

Lambda function that clips a value to the range [0, 100].

**Parameters:**
- `x` (float): Value to clip

**Returns:**
- `float`: Value clipped to [0.0, 100.0]

**Example:**
```python
# From utils.py
clip_0_to_100 = lambda x: max(0.0, min(100.0, float(x)))

# Usage
score = clip_0_to_100(150)  # Returns 100.0
score = clip_0_to_100(-10)  # Returns 0.0
score = clip_0_to_100(75.5) # Returns 75.5
```

---

### `clip_0_to_1(x)`

Lambda function that clips a value to the range [0, 1].

**Parameters:**
- `x` (float): Value to clip

**Returns:**
- `float`: Value clipped to [0.0, 1.0]

**Example:**
```python
# From utils.py
clip_0_to_1 = lambda x: max(0.0, min(1.0, float(x)))

# Usage
fraction = clip_0_to_1(1.5)  # Returns 1.0
fraction = clip_0_to_1(-0.2) # Returns 0.0
fraction = clip_0_to_1(0.75) # Returns 0.75
```

---
### `weighted_average(items)`
---

### `to_letter_score(score)`

Converts a numeric score (0-100) to a letter grade (A, A-, B, B-, C, C-, D, D-, E).

**Parameters:**
- `score` (float): Numeric score from 0 to 100

**Returns:**
- `str`: Letter grade

**Score Bands:**
- A: 88.89-100.0
- A-: 77.78-88.89
- B: 66.67-77.78
- B-: 55.56-66.67
- C: 44.44-55.56
- C-: 33.33-44.44
- D: 22.22-33.33
- D-: 11.11-22.22
- E: 0.0-11.11

**Example:**
```python
# From Circulytics_Score_Calculator.ipynb
Overall_letter = to_letter_score(100*Overall_score)
# If Overall_score = 0.92, returns 'A'
# If Overall_score = 0.75, returns 'A-'
# If Overall_score = 0.45, returns 'C'
```

---

### `weighted_average(items)`

Calculates a weighted average from a list of (value, weight) tuples.

**Parameters:**
- `items` (list[tuple[float, float]]): List of (value, weight) tuples

**Returns:**
- `float`: Weighted average, or 0.0 if total weight is 0

**Formula:**
```
weighted_average = sum(value_i * weight_i) / sum(weight_i)
```

**Example:**
```
# From Circulytics_Score_Calculator.ipynb
# Calculate enablers score
Enablers_score = weighted_average([
    (theme_scores[tm], ENABLER_THEME_WEIGHTS[tm]) 
    for tm in [1,2,3,4,5]
])

# Example with specific values
items = [(0.8, 0.3), (0.6, 0.5), (0.9, 0.2)]
avg = weighted_average(items)  # Returns (0.8*0.3 + 0.6*0.5 + 0.9*0.2)/1.0 = 0.72

# Calculate outcomes score with varying weights
Outcomes_score = weighted_average([
    (theme_scores[tm], outcomes_theme_weights[tm]) 
    for tm in applicable_outcomes_themes
])

# Zero total weight
items = [(0.5, 0.0), (0.7, 0.0)]
avg = weighted_average(items)  # Returns 0.0

# Single item
items = [(0.85, 1.0)]
avg = weighted_average(items)  # Returns 0.85
```

---

## Weighting Functions

### `compute_outcomes_theme_weights(company)`

Computes the weights for Outcomes themes (6-11) based on company characteristics.

**Parameters:**
- `company` (dict): Dictionary with keys:
  - `industry_type` (str): Industry classification
  - `services_sold` (bool): Whether company sells services
  - `material_flows` (bool): Whether company has material flows
  - `ownership` (bool): Whether company owns material flows
  - `water_intensive` (bool): Whether operations are water-intensive
  - `energy_producer` (bool): Whether company produces energy

**Returns:**
- `dict`: Weights for themes 6-11, e.g., `{6: 0.7, 7: 0.0, 8: 0.15, 9: 0.0, 10: 0.15, 11: 0.0}`

**Example:**
```python
# From Circulytics_Score_Calculator.ipynb
company_info = {
    'industry_type': industry_type.value,
    'services_sold': services_sold.value,
    'material_flows': material_flows.value,
    'ownership': ownership.value,
    'water_intensive': water_intensive.value,
    'energy_producer': energy_producer.value,
    "types_of_flows": types_of_flows.value
}

outcomes_theme_weights = compute_outcomes_theme_weights(company_info)
# For a manufacturing company with material flows and ownership:
# {6: 0.7, 7: 0.0, 8: 0.15, 9: 0.0, 10: 0.15, 11: 0.0}

# For a financial institution that is not water-intensive:
# {6: 0.0, 7: 0.0, 8: 0.15, 9: 0.0, 10: 0.15, 11: 0.7}
```

---

### `theme6_indicator_weights(company_info, masses, theme_indicator_widgets)`

Calculates indicator weights for Theme 6 (Products and materials) based on material flows.

**Parameters:**
- `company_info` (dict): Company characteristics
- `masses` (dict): Mass flows with keys:
  - `M_IN`: Total annual inflow mass (tonnes)
  - `M_PROD1`: Outflow mass of products designed to be consumed (tonnes)
  - `M_PROD2`: Outflow mass of products designed to be used (tonnes)
  - `M_WASTE1`: Waste from products designed to be consumed (tonnes)
  - `M_WASTE2`: Waste from products designed to be used (tonnes)
- `theme_indicator_widgets` (dict): Theme indicator widgets: to get the mass of product that is reused, from indicator 6f part 1

**Returns:**
- `dict`: Weights for applicable Theme 6 indicators (e.g., `{'6a': 0.4, '6b': 0.3, '6d': 0.3}`)

**Example:**
```python
# From Circulytics_Score_Calculator.ipynb
masses = {
    'M_IN': float(M_in.value),
    'M_PROD1': float(M_prod1.value),
    'M_PROD2': float(M_prod2.value),
    'M_WASTE1': float(M_waste1.value),
    'M_WASTE2': float(M_waste2.value)
}
t6_w = theme6_indicator_weights(company_info, masses, theme_indicator_widgets)
# For a company with M_IN=1000, M_PROD2=600, M_WASTE2=400:
# {'6a': 0.5, '6c': 0.2, '6e': 0.3}
```

---

### `theme9_indicator_weights(demand_ml, outflow_ml)`

Calculates indicator weights for Theme 9 (Water) based on water flows.

**Parameters:**
- `demand_ml` (float): Total annual water demand in megalitres
- `outflow_ml` (float): Total annual water outflow in megalitres

**Returns:**
- `dict`: Weights for indicators 9a-9d (e.g., `{'9a': 0.25, '9b': 0.25, '9c': 0.25, '9d': 0.25}`)

**Example:**
```python
# Equal demand and outflow
weights = theme9_indicator_weights(1000, 1000)
# Returns {'9a': 0.25, '9b': 0.25, '9c': 0.25, '9d': 0.25}

# Higher demand
weights = theme9_indicator_weights(3000, 1000)
# Returns {'9a': 0.375, '9b': 0.375, '9c': 0.125, '9d': 0.125}
```

---

### `theme10_indicator_weights(use_mwh, prod_mwh, is_producer)`

Calculates indicator weights for Theme 10 (Energy).

**Parameters:**
- `use_mwh` (float): Total annual energy usage in MWh
- `prod_mwh` (float): Total annual energy production in MWh
- `is_producer` (bool): Whether company produces energy

**Returns:**
- `dict`: Weights for indicators 10a and optionally 10b

**Example:**
```python
# Non-producer
weights = theme10_indicator_weights(5000, 0, False)
# Returns {'10a': 1.0}

# Producer with equal use and production
weights = theme10_indicator_weights(5000, 5000, True)
# Returns {'10a': 0.5, '10b': 0.5}
```

---

## UI Building Functions

### `create_weighting_info_ui(company_info, applicable_outcomes_themes)`

Creates the complete UI for collecting weighting information for all applicable outcomes themes.

**Parameters:**
- `company_info` (dict): Company characteristics dictionary
- `applicable_outcomes_themes` (list[int]): List of Outcomes theme numbers (6-11) applicable to the company

**Returns:**
- `tuple`: Contains:
  - `weighting_boxes` (dict): VBox user interface with widgets for entering weighting info for each theme
  - `M_in` (BoundedFloatText): Total inflow mass widget
  - `M_prod1` (BoundedFloatText): Mass of products designed to be consumed widget
  - `M_prod2` (BoundedFloatText): Mass of products designed to be used widget
  - `M_waste1` (BoundedFloatText): Mass of waste from products designed to be consumed widget
  - `M_waste2` (BoundedFloatText): Mass of waste from products designed to be used widget
  - `water_demand` (BoundedFloatText): Volume of water demand widget
  - `water_outflow` (BoundedFloatText): Volume of water outflow widget
  - `energy_use` (BoundedFloatText): Energy usage widget
  - `energy_prod` (BoundedFloatText): Energy production widget
  - `asset_widgets_procured` (list): Interfaces to widgets for weighting information for indicator 8a (masses of procured assets)
    - Each item is a dict with the following format (see return type of asset_row_widgets): {'name': str (name of asset category), 'mass_widget': w.BoundedFloatText, 'mass_box': w.HBox, 'applicable_and_mass_not_available': w.Checkbox, 'not_applicable': w.Checkbox}
  - `asset_widgets_owned` (list): Interfaces to widgets for weighting information for indicator 8a (masses of procured assets)
    - Each item is a dict with the following format (see return type of asset_row_widgets): {'name': str (name of asset category), 'mass_widget': w.BoundedFloatText, 'mass_box': w.HBox, 'applicable_and_mass_not_available': w.Checkbox, 'not_applicable': w.Checkbox}
  - `finance_widgets` (list): Finance theme widgets

**Example:**
```
weighting_boxes, M_in, M_prod1, M_prod2, M_waste1, M_waste2, \
    water_demand, water_outflow, energy_use, energy_prod, \
    asset_widgets_procured, asset_widgets_owned, finance_widgets = \
    create_weighting_info_ui(company_info, applicable_outcomes_themes)

# Display weighting UI for applicable themes
for tm in applicable_outcomes_themes:
    display(weighting_boxes[tm])
```

---

### `create_indicator_ui(company_info, industry_type, finance_widgets, asset_widgets_owned, asset_widgets_procured)`

Creates the complete UI for all Circulytics indicators based on company characteristics.

**Parameters:**
- `company_info` (dict): Company characteristics
- `industry_type` (ipywidgets.Dropdown): Industry type dropdown widget
- `finance_widgets` (list): Finance theme widgets
- `asset_widgets_owned` (list): Owned asset widgets
- `asset_widgets_procured` (list): Procured asset widgets

**Returns:**
- `tuple`: Contains:
  - `theme_indicator_ui_boxes` (dict): VBox widgets for each theme's indicators
  - `theme_indicator_widgets` (dict): Nested dict of indicator widgets by theme and indicator code

**Example:**
```python
# From Circulytics_Score_Calculator.ipynb
theme_indicator_ui_boxes, theme_indicator_widgets = \
    create_indicator_ui(company_info, industry_type, finance_widgets, 
                       asset_widgets_owned, asset_widgets_procured)

# Display all indicator UIs
for tm in enablers + applicable_outcomes_themes:
    display(theme_indicator_ui_boxes[tm])

# Access specific indicator widget
dropdown_widget = theme_indicator_widgets[1]['1a']['dropdown']
checkbox_widgets = theme_indicator_widgets[1]['1e']
```

---

## Widget Creation Functions

### `asset_row_widgets(label)`

Creates a row of widgets for inputting asset information.

**Parameters:**
- `label` (str): Asset category label (e.g., "IT equipment", "Buildings")

**Returns:**
- `dict`: Contains:
  - `name` (str): Asset category name
  - `mass_widget` (BoundedFloatText): Mass input widget
  - `mass_box` (HBox): Complete row layout
  - `applicable_and_mass_not_available` (Checkbox): Checkbox for missing data
  - `not_applicable` (Checkbox): Checkbox for N/A assets

**Example:**
```python
# Create asset row for IT equipment
it_row = asset_row_widgets("IT equipment")

# Access widgets
mass_value = it_row['mass_widget'].value
is_applicable = not it_row['not_applicable'].value

# Display the row
display(it_row['mass_box'])
```

---

### `build_theme_8_indicator_ui()`

Builds the UI for Theme 8 indicators (Plant, property, and equipment assets).

**Parameters:**
- None

**Returns:**
- `tuple`: Contains:
  - `asset_widgets_procured` (list): Widgets for procured assets (indicator 8a)
  - `asset_widgets_owned` (list): Widgets for owned assets (indicator 8b)
  - `ui_8_procured` (VBox): UI for procured assets (indicator 8a)
  - `ui_8_owned` (VBox): UI for owned assets  (indicator 8b)

**Example:**
```
asset_widgets_procured, asset_widgets_owned, ui_8_procured, ui_8_owned = \
    build_theme_8_indicator_ui()

# Access asset data
total_procured_mass = sum([w['mass_widget'].value for w in asset_widgets_procured])
```

---

### `build_dropdown_block(indicator_code, prompt, options, scores, subprompt=None, bonus_checkbox=None)`

Render a UI box similar to indicators 1a, 1b, and 1c in which the user selects an option from a dropdown menu, with each option having a score
An option for an optional "bonus checkbox" that adds an additional bonus to the indicator score is also provided.

**Parameters:**
- `indicator_code` (str): Indicator code (e.g., '1a')
- `prompt` (str): The main prompt/question for the indicator
- `options` (list[str]): List of option descriptions
- `scores` (list[float]): Corresponding scores for each option
- `subprompt` (str | None): Optional additional prompt text
- `bonus_checkbox` (dict | None): An optional dictionary defining a bonus checkbox with keys 'label' and 'bonus_score', by default None

**Returns:**
- `tuple`: 
  - A VBox widget containing the dropdown and optional bonus checkbox

**Example:**
```
container, ui = build_dropdown_block(
    '1a',
    "How central is circular economy to your CEO’s agenda?",
    ['Not mentioned in external communications',
      'Relevant concept (e.g. materials circulation, a new business model that follows the principles of circular economy, acknowledging that the solution is not just resource efficiency) mentioned in the past 12 months, in external communications',
      'Circular economy mentioned explicitly as a strategic priority once in the past 12 months, in external communications',
      'Circular economy mentioned explicitly as a strategic priority multiple times in the past 12 months, in external communications'],
     [0,0.33,0.67,1.0]
)

# With bonus checkbox
container, ui = build_dropdown_block(
    '9c',
    "To what extent do you have plans in place to extract surplus nutrients, metals, chemicals, heat and similar valuable resources before discharging the water used in your processes and operations?",
    ["Have not assessed yet","Have assessed, currently developing plans","Processes in place for some of the water used in operations, or for some of the relevant resources","Processes in place for majority of the water used in operations and for majority of the relevant resources "],
    [0.0, 0.25, 0.50, 0.75],
    bonus_checkbox={"label": "With processes in place to extract surplus nutrients, metals, chemicals, heat and similar valuable resources from water used in operations, are the majority of the extracted resources subsequently recirculated (e.g. through heat exchange, as nutrient recirculation that meets the qualifying conditions, etc.)? ", "score_bonus": 0.25}
)

# Access selected value
score = ui['dropdown'].value
if ui.get('bonus_checkbox') and ui.get('bonus_checkbox').value:
  score += theme_indicators[9]['9c']['bonus_checkbox']["score_bonus"]
```

---

### `build_checkbox_block(indicator_code, prompt, options, subprompt=None)`

Render a UI box for a 'select all that apply' pattern with checkboxes, similar to indicator 1e.

**Parameters:**
- `indicator_code` (str): Indicator code (e.g., '1e')
- `prompt` (str): The main prompt/question for the indicator
- `options` (list[str]): The list of checkbox options to display to the user
- `subprompt` (str | None): An optional subprompt to display below the main prompt, by default None

**Returns:**
- `tuple`:
  - VBox widget containing the UI
  - list of Checkbox widgets

**Example:**
```python
# Create checkbox block
container, checkboxes = build_checkbox_block(
    '1e',
    'Select all circular economy principles your company applies:',
    ['Design for longevity', 'Design for disassembly', 'Use recycled materials']
)

# Get selected options
selected = [i for i, cb in enumerate(checkboxes) if cb.value]
```

---

### `build_slider_block(indicator_code, prompt, min_val=0, max_val=1, step=0.01, subprompt=None)`

Create a UI box for a single FloatSlider input with a heading and description.

**Parameters:**
- `indicator_code` (str): Indicator code (e.g., '6b')
- `prompt` (str): Descriptive text
- `min_val` (float): Minimum slider value (default 0)
- `max_val` (float): Maximum slider value (default 1)
- `step` (float): Step size (default 0.01)
- `subprompt` (str | None): Optional subprompt

**Returns:**
- `tuple`:
  - VBox widget
  - FloatSlider widget

**Example:**
```python
# Create percentage slider
container, slider = build_slider_block(
    '6b',
    "What % (by mass) of M_WASTE1 (from 0o. Part 1), is material processing waste or by-products that go to landfill or incineration (and are therefore not recirculated)?",
    min_val=0,
    max_val=1,
    step=0.01
)

# Get value
indicator_score_6b = clip_0_to_1(1-slider.value)
```

---

### `build_composite_slider_block(indicator_code, prompt, items, min_val=0.0, max_val=1.0, step=0.01, show_total=True, weights=None, cap_total_at=1.0, subprompt=None)`

Create a UI box for a single indicator with multiple FloatSlider inputs with different weights, plus an optional label for the total score.

**Parameters:**
- `indicator_code` (str): Indicator code
- `prompt` (str): Main prompt
- `items` (list[dict]): List of slider configurations, each with:
  - `label` (str): Slider label
  - Optional per-item overrides for slider parameters: `min`, `max`, `step`, `value`, `sublabel`
- `min_val`, `max_val`, `step` (float): Default slider bounds/step applied when item-level overrides are not provided.
- `show_total` (bool): Whether to show a dynamic total score below the sliders.
- `weights` (list[float] | None): Weights for each slider value used to compute the weighted total. If provided, must match len(items); otherwise, equal weights are used for each slider that add up to 1.
- `cap_total_at` (float): Maximum total score (default 1.0)
- `subprompt` (str | None):An optional subprompt to display below the main prompt

**Returns:**
- `tuple`:
  - VBox: The composite block widget (heading + sliders + total score label).
  - dict API with:
    - `get_values()`: Returns dict of {label: value}
    - `get_weighted_score()`: Returns weighted score
    - `sliders`: List of slider widgets
    - `weights`: List of weight values
    - `labels`: List of label strings

**Example:**
```python
# Create multi-slider for indicator 6f (part 1)
container, api = build_composite_slider_block(
    '6f_part1',
    "What % (by mass) of your products and materials (M_PROD2 from 0n. Part 2) are recirculated in practice in the following ways (only counting the first cycle of recirculation after initial use):",
    items=[
            {"label": "Reuse/redistribution", "type": "slider"},
            {"label": "Refurbishment/remanufacture", "type": "slider"},
            {"label": "Recycling", "type": "slider"},
            {"label": "Qualifying nutrient recirculation", "type": "slider"}
        ],
    weights=[1.0,0.8,0.4,0.4]
)

# Get weighted score
total_score = api['get_weighted_score']()

# Get individual values
values = api['get_values']()  # {'Reuse/redistribution': 0.8, ...}
```

---

### `build_grouped_multiple_dropdown_block(indicator_code, prompt, column_descriptions, dropdown_options, dropdown_scores, rows_label='Row', description_width='initial', dropdown_width_px=500, first_col_width_px=200)`

Build a multi-dropdown UI where dropdowns are grouped into rows and columns, forming a tablular layout.
For example, indicator 3b, where each row is a seniority level in the company, each column is a training level, and each dropdown option relates to what extent training is offered at that level.

**Parameters:**
- `indicator_code` (str): Indicator code (e.g., '3b')
- `prompt` (str): Heading text
- `column_descriptions` (list[str]):Descriptions of the different columns, e.g. [column_1_label, column_2_label, column_3_label, ...]
- `dropdown_options` (list[str]): Descriptions of the dropdown options, e.g. [option_1, option_2, option_3, ...]
- `dropdown_scores` (dict[str, dict[str, list[float]]]): Scores for the dropdown options, grouped by row and column, e.g. { row: { column: [score_for_option_1, score_for_option_2, ...], ... }, ... } Scores should be floats 0..1 in the same order as dropdown_options.
- `rows_label` (str): Label for the first column (row headings).
- `description_width` (str): ipywidgets style for aligning label text.
- `dropdown_width_px` (int): Width of each dropdown widget in pixels.
- `first_col_width_px` (int): Width of the first column (row labels) in pixels.

**Returns:**
- `tuple`:
  - ui : ipywidgets.VBox
        The composite UI block: heading + rows.
  - api : dict
        - "get_selections" -> dict[row] -> dict[column] -> selected option index (int or None)
        - "get_scores"     -> dict[row] -> dict[column] -> selected score (float 0..1)
        - "get_total_score"-> float total score (0..1)
        - "widgets"        -> dict[row] -> dict[column] -> dropdown widget
        - "rows"           -> list of rows in display order
        - "columns"        -> dict[row] -> list of columns

**Example:**
```
# Training assessment by seniority level
container, api = build_grouped_multiple_dropdown_block(
    '3b',
    "To what extent does your company offer circular economy related training within your company?",
    column_descriptions=['General training on circular economy principles and concepts','Training on circular economy specific to your industry or business function','Formal on the job training (mentorships, trainee programmes, apprenticeships) on circular economy'],
    dropdown_options=["Not offered to all", "Offered to all", "Mandatory for all"],
    dropdown_scores={level: {'General training on circular economy principles and concepts': [0.0,0.25,0.5],
                              'Training on circular economy specific to your industry or business function': [0.0,0.50,1.0],
                              'Formal on the job training (mentorships, trainee programmes, apprenticeships) on circular economy': [0.0,0.50,1.0]
                              } for level in ["Directors and above","Managers","Employees"]},
    rows_label = "Seniority Level"
)

# Get overall score
score = api['get_total_score']()
```

---

### `build_checkbox_table_block(indicator_code, prompt, subprompt, row_labels, column_labels=None, column_descriptions=None, index_col_name='', per_col_scores=None, per_cell_scores=None, description_width='initial', cell_width_px=500, first_col_width_px=500)`

Render a table of checkboxes for a single indicator, e.g. indicator 3c

**Parameters:**
- `indicator_code` (str): Indicator code (e.g., '3c')
- `prompt` (str): Main heading
- `subprompt` (str | None): Optional subheading
- `row_labels` (list[str]): Row labels
- `column_labels` (list[str]): Column labels
- `column_descriptions` (list[str] | None): Descriptions for columns
- `index_col_name` (str): Label for first column
- `per_col_scores` (list[float] | None): score per checkbox in each column
- `per_cell_scores` (dict[(int, int), float] | None): Optional fine-grained scores per cell (if you want different columns to contribute differently). If provided, this overrides per_col_scores for those cells.
- `description_width` : str
  - ipywidgets label layout style; 'initial' keeps full label text visible.
- `cell_width_px` : int
  - Width of each checkbox cell (VBox) in pixels.
- `first_col_width_px` : int
  - Width of the first column (row labels) in pixels.

**Returns:**
- `tuple`:
  - `ui` : ipywidgets.VBox
        Composite UI (heading + table + summary).
  - `api` : dict
      - "get_matrix" -> returns dict[row_label] -> dict[column_label] -> bool (checked)
      - "get_row_counts" -> returns dict[row_label] -> int (number of boxes checked in that row)
      - "get_score" -> returns overall score
      - "widgets" -> dict[row_label] -> dict[column_label] -> w.Checkbox
      - "rows" -> list of row labels
      - "cols" -> list of column labels

**Example:**
```
# Circular economy functions table
container, api = build_checkbox_table_block(
    '3c',
    "In which functions do you have individuals or project teams with responsibility for circular economy implementation?",
    None,
    row_labels=['R&D', 'Operations', 'Marketing', 'Finance'],
    column_labels=["Option 1","Option 2","Option 3"],
    column_descriptions=[
      "No individuals or project teams working on circular economy implementation",
      "Individuals or project teams working on circular economy implementation during the financial reporting year stated in 0a",
      "Individuals or teams who have circular economy codified in their job description/targets/incentives and are working on circular economy implementation"
    ],
    per_col_scores=[0.4, 0.4, 0.2]
)

# Get score
score = api['get_score']()

# Check which boxes are selected
matrix = api['get_matrix']()  # {'R&D': {'Strategy': True, ...}, ...}
```

---

### `build_percentage_table_block(indicator_code, prompt, row_labels, column_labels, option_descriptions, option_weights, row_weights, index_col_name='', description_width='initial', cell_width_px=180, step=1, enforce_row_total_100=True, asset_widgets_procured=None)`

Render a table of percentage inputs (BoundedFloatText) e.g. for Indicator 8a with per-asset mass weighting.

**Parameters:**
- `indicator_code` (str): Indicator code (e.g., '8a')
- `prompt` (str): Heading text
- `row_labels` (list[str]): Row labels (e.g., asset categories)
- `column_labels` (list[str]): Short column labels
- `option_descriptions` (list[str]): Longer descriptions corresponding to each column (shown above the table).
- `option_weights` (list[float]): Per-column score weights (e.g., [1.0, 1.0, 0.5, 0.5, 0.0]).
- `row_weights` (dict[str, float]): Per-row weights, e.g. based on asset mass share (e.g., {"IT equipment": 0.2, "Textiles": 0.3, "Furniture": 0.5}).
- `index_col_name` (str): First column header
- `description_width`, `cell_width_px`: Overrides default ipywidgets layout parameters
- `step` (float): Step for percentage input fields, in percent units (e.g., 1.0 -> 1% increment).
- `enforce_row_total_100` (bool): If True, summary will flag rows whose percent total is not 100%.
- `asset_widgets_procured` (list[dict] | None): List of asset widget information with following format:
    {
        'name' (str): asset category name,
        'mass_widget' (w.BoundedFloatText): widget with mass of asset category,
        'mass_box' (w.HBox): UI box for entry of mass,
        'applicable_and_mass_not_available' (w.Checkbox): widget for whether the "Applicable and mass not available" option is selected,
        'not_applicable' (w.Checkbox): widget for whether the "not applicable" option is selected
    }


**Returns:**
- `ui`(ipywidgets.VBox): Composite UI (descriptions + heading + table + summary).
- `api` (dict)
    - "get_matrix" -> dict[row_label][column_label] -> float (value 0..1 as fraction) per-item scores
    - "get_row_totals" -> dict[row_label] -> float (0..1) sum of values for each row
    - "get_row_scores" -> dict[row_label] -> float (0..1) weighted score for each row
    - "get_overall_score" -> float (0..1) weighted sum of row scores (overall indicator score)
    - "widgets" -> dict with references to all widgets, with the following structure:
        - "percent_inputs" -> dict[row_label][column_label] -> w.BoundedFloatText
        - "row_total_labels" -> dict[row_label] -> w.HTML
        - "summary_html" -> w.HTML
        - "warnings_html" -> w.HTML
        - "desc_block" -> w.Accordion (column descriptions)
    - "rows" -> list of rows
    - "cols" -> list of columns

**Example:**
```
container, api = build_percentage_table_block(
    '8a',
    "For each of the asset groups selected in 0q. Part 2: What % (by mass) of your plant, property, and equipment assets procured in the financial year (as stated in 0a.) were procured with the following circular procurement approaches? ",
    row_labels=[
            'IT equipment',
            'Textiles',
            'Furniture',
            'Buildings',
            'Heavy machinery',
            'Mid-weight machinery',
            'Light machinery',
            'Heavy transport',
            'Mid-weight transport',
            'Light transport',
            'Warehousing equipment',
        ],
    column_labels=[
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
            "Option 5"
        ],
    option_descriptions=[
            "Second-hand assets",
            "New assets designed with circular design approaches both during use and end of functional life aspects covered",
            "Only during-use",
            "Only end of functional life",
            "None of the above"
        ],
    option_weights=[1.0, 1.0, 0.5, 0.5, 0.0],
    row_weights=procured_asset_weights, # masses of each asset procured
    asset_widgets_procured=asset_widgets_procured
)

# Get overall weighted score
overall_score = api['get_overall_score']()

# Get per-asset scores
asset_scores = api['get_asset_scores']()  # {'IT equipment': 0.75, ...}
```

---

### `build_both_block(indicator_code, prompt, dropdown_options, dropdown_scores, checkbox_label, checkbox_options, subprompt=None)`

Render a UI box for an indicator that includes both a dropdown and a set of checkboxes, similar to indicator 1d.

**Parameters:**
- `indicator_code` (str): Indicator code (e.g., '1d')
- `prompt` (str): Main prompt
- `dropdown_options` (list[str]): Dropdown option labels
- `dropdown_scores` (list[float]): Scores for dropdown options
- `checkbox_label` (str): Label for checkbox section
- `checkbox_options` (list[str]): Checkbox option labels
- `subprompt` (str | None): Optional subprompt

**Returns:**
- `tuple`:
  - A VBox widget containing the heading, dropdown, and checkboxes
  - tuple of (dropdown widget, list of checkbox widgets)

**Example:**
```
container, (dropdown, checkboxes) = build_both_block(
    '1d',
    "Do you have measurable circular economy targets?",
    dropdown_options=['No targets',
                      'Targets are being developed either for a relevant concept (e.g. materials circulation) or circular economy explicitly',
                      'Targets have been developed on organisation level, but are not SMART targets',
                      'SMART targets have been developed on organisation level',
                      'SMART targets have been developed on organisation level and further down on a sub-unit (e.g. business unit or region) level.'],
    dropdown_scores=[0,0.25,0.5,0.75,0.75],
    checkbox_label="For option 5, select all that apply:",
    checkbox_options= ['Innovation/R&D/design','Corporate strategy','Corporate finance','Supply chain','Production','Sales/marketing','CE/Sustainability','Other']
)

# Get indicator score
dd_widget, cb_widgets = theme_indicator_widgets[1]['1d']
score = clip_0_to_1(dd_widget.value + sum([theme_indicators[1]['1d']['checkbox_scores'][i] for i, cb in enumerate(cb_widgets) if cb.value]))
```

---

### `build_grouped_checkbox_block(indicator_code, prompt, group_labels, group_sublabels, group_options, subprompt=None)`

Render a UI box for a set of checkboxes with a 'select all that apply' pattern divided into groups with headings, similar to indicator 7a part 2.

**Parameters:**
- `indicator_code` (str): Indicator code (e.g., '7a_part2')
- `prompt` (str): The main prompt/question for the indicator
- `group_labels` (list[str]): Headers for each group
- `group_sublabels` (list[str]): Descriptions for each group
- `group_options` (list[list[str]]): Checkbox options for each group
- `subprompt` (str | None): Optional subprompt

**Returns:**
- `tuple`:
  - w.VBox: A VBox widget containing the heading and grouped checkboxes
  - list[list[w.Checkbox]]: A list of lists of Checkbox widgets created for each group

**Example:**
```
container, grouped_cbs = build_grouped_checkbox_block(
    "7a_part2",
    "Select the circular economy principle(s) that the services you highlighted in Part 1 have a positive impact on, and describe the impact. ",
    group_labels=[
                "Eliminate waste & pollution",
                "Keep products & materials in use",
                "Regenerate natural systems"
              ],
    group_sublabels=[
                "All the services that relate to material or products before they are put on the market and that help a circular economy by designing out waste and pollution from the outset. Service activities that offer, enable or facilitate:",
                "All services relating to material or products after they have been used or while in use that help keep materials in the economy, or that help keep the product in use for longer. Service activities that offer, enable or facilitate:",
                "All services that enable keeping nutrients in the (bio)economy, and enhance the health of agricultural and other biological systems the economy relies on. Service activities that offer, enable or facilitate"
            ],
    group_options=[
        # Eliminate waste & pollution — options
        [
            "Designing (as a service) products with longer use life, reusability, and repairability in mind",
            "Addressing material supply/demand imbalances or enabling others to do so (e.g. software for real time manufacturing)",
            "Preventing or reducing product waste accumulation (e.g. business support for industrial symbiosis schemes)"
        ],
        # Keep products & materials in use — options
        [
            "Recirculation and valorisation of products and materials that are waste for others (e.g. marketplace for construction waste)",
            "New recirculation options for existing products / services (e.g. secondary markets)",
            "Sharing materials and/or products (e.g. product as a service)",
            "Accessing durable, repairable products",
            "Increasing the intensity of use of assets (e.g. utilisation tracking software, asset sharing platforms)",
            "Encouraging product maintenance / repair in preference to change in ownership",
            "Product / material information accessibility or fidelity in support of circular economy",
            "Financial incentives for recirculation of products and materials (e.g. buy-back schemes)"
        ],
        # Regenerate natural systems — options
        [
            "Sourcing regeneratively and renewably grown material over materials that are not regeneratively grown or finite (e.g. supply chain consultancy)",
            "Increasing organic nutrient flow in a defined ecosystem (e.g. organic waste management service)",
            "Supporting natural ecosystem processes through improved soil health, biodiversity etc.",
            "Reversing degradation of natural ecosystem process in a defined locality (e.g. conservation management, land management)",
            "The promotion of renewable energy (e.g. improving the flexibility of the electricity grid, energy storage solutions). Please note that biomass needs to meet certain qualifying conditions to count as renewable energy in Circulytics, as outlined in the Definitions."
        ]
    ]
)

# Access first group's checkboxes and count how many are checked
elim_waste_pollution_cbs = grouped_cbs[0]
selected_count = sum([cb.value for cb in elim_waste_pollution_cbs])
```
