import numpy as np, pandas as pd
import ipywidgets as w
from typing import List, Dict
from params import *

clip_0_to_100 = lambda x: max(0.0, min(100.0, float(x)))
clip_0_to_1 = lambda x: max(0.0, min(1.0, float(x)))

def to_letter_score(score):
    s = clip_0_to_100(score)
    bands = [
        (88.89, 100.0, 'A'), (77.78, 88.89, 'A-'), (66.67, 77.78, 'B'), (55.56, 66.67, 'B-'),
        (44.44, 55.56, 'C'), (33.33, 44.44, 'C-'), (22.22, 33.33, 'D'), (11.11, 22.22, 'D-'), (0.0, 11.11, 'E')
    ]
    for lo, hi, letter in bands:
        if s >= lo and s <= hi:
            return letter
    return 'E'

def asset_row_widgets(label):
    asset_label = w.Label(value=label, layout=w.Layout(width='225px'), style = {'description_width': 'initial'})
    mass_label = w.Label(value = f"{ASSET_AVG_MASS[label]} t/item" if label != "Buildings" else f"{ASSET_AVG_MASS[label]} t/m2", layout=w.Layout(width='120px'))
    mass_estimate = w.BoundedFloatText(value=0.0, min=0.0, disabled=False, layout=w.Layout(width='200px'),style = {'description_width': 'initial'})
    
    return {
        'name': label,
        'mass_widget': mass_estimate,
        'mass_box': w.HBox([asset_label, mass_label, mass_estimate]),
        'applicable_and_mass_not_available': w.Checkbox(value=False, layout=w.Layout(width='200px')),
        'not_applicable': w.Checkbox(value=False, layout=w.Layout(width='150px')),
    }

def weighted_average(items):
    """
    Calculate the weighted average of a list of (score, weight) pairs.
    
    Parameters
    ----------
    items (list[tuple[float, float]]): List of tuples where each tuple contains a score and its corresponding weight.

    Returns
    -------
    float
        The weighted average of the scores.
    """
    wsum = sum(w for _,w in items)
    if wsum<=0: return 0.0
    return sum(s*w for s,w in items)/wsum

def compute_outcomes_theme_weights(company):
    weights = {6:0.0,7:0.0,8:0.0,9:0.0,10:0.0,11:0.0}
    ind = company['industry_type']
    services = bool(company.get('services_sold',False))
    mats = bool(company.get('material_flows',False))
    own = bool(company.get('ownership',False))
    water = bool(company.get('water_intensive',False))
    energy_prod = bool(company.get('energy_producer',False))
    if ind in finance_industry_classes:
        weights[11] = 0.7
        if water: weights[8]=0.1; weights[10]=0.1; weights[9]=0.1
        else: weights[8]=0.15; weights[10]=0.15
        return weights
    if energy_prod:
        weights[10] = 0.7
        if water: weights[8]=0.1; weights[9]=0.1; weights[9]=0.1
        else: weights[8]=0.15; weights[10]=0.15
        return weights
    if mats and not services:
        weights[6] = 0.7
        if water: weights[8]=0.1; weights[10]=0.1; weights[9]=0.1
        else: weights[8]=0.15; weights[10]=0.15
        return weights
    if services and not mats:
        weights[7] = 0.7
        if water: weights[8]=0.1; weights[10]=0.1; weights[9]=0.1
        else: weights[8]=0.15; weights[10]=0.15
        return weights
    if services and mats:
        if own: weights[6]=0.65; weights[7]=0.05
        else: weights[6]=0.05; weights[7]=0.65
        if water: weights[8]=0.1; weights[10]=0.1; weights[9]=0.1
        else: weights[8]=0.15; weights[10]=0.15
        return weights
    raise AssertionError("Company must either be a financial institution, have material flows, or have services.")

def theme6_indicator_weights(company_info, masses, theme_indicator_widgets):
    if not company_info['material_flows']:
        raise AssertionError("Theme 6 weighting can only be computed for companies with material flows.")
    if not company_info['ownership']:
        if company_info["types_of_flows"] == "Products and materials that are designed to be consumed":
            applicable_inds = ['6b']
        else:
            applicable_inds = ['6b', '6c']
    elif company_info["types_of_flows"] == "Products and materials that are designed to be consumed":
        applicable_inds = ['6a','6b','6d','6e']
    elif company_info["types_of_flows"] == "Products and materials that are designed to be used":
        applicable_inds = ['6a','6c','6d','6e','6f_part1','6f_part2']
    else: 
        applicable_inds = ['6a','6b','6c','6d','6e','6f_part1','6f_part2']
    denoms = {'6a':masses.get('M_IN',0.0),
              '6b':masses.get('M_WASTE1',0.0),
              '6c':masses.get('M_WASTE2',0.0),
              '6d':masses.get('M_PROD1',0.0)+masses.get('M_PROD2',0.0),
              '6e':masses.get('M_PROD1',0.0)+masses.get('M_PROD2',0.0)+masses.get('M_WASTE1',0.0)+masses.get('M_WASTE2',0.0),
              '6f_part1':masses.get('M_PROD2',0.0),
    }
    if '6f_part2' in applicable_inds:
        denoms['6f_part2'] = (theme_indicator_widgets[6]['6f_part1']['sliders'][0].value)*masses.get('M_PROD2',0.0)
    denoms = {k:v for k,v in denoms.items() if k in applicable_inds}
    total = sum(denoms.values())
    return {k:(v/total) if total>0 else 0.0 for k,v in denoms.items()}

def theme9_indicator_weights(demand_ml, outflow_ml):
    total = demand_ml + outflow_ml
    if total<=0: return {'9a':0.0,'9b':0.0,'9c':0.0,'9d':0.0}
    d = demand_ml/total; o = outflow_ml/total
    return {'9a':d*0.5,'9b':d*0.5,'9c':o*0.5,'9d':o*0.5}

def theme10_indicator_weights(use_mwh, prod_mwh, is_producer):
    if not is_producer: return {'10a':1.0,}
    total = use_mwh + prod_mwh
    if total<=0: return {'10a':0.5,'10b':0.5}
    return {'10a':use_mwh/total,'10b':prod_mwh/total}

def build_theme_8_indicator_ui():
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
    return asset_widgets_procured, asset_widgets_owned, ui_8_procured, ui_8_owned

def create_weighting_info_ui(company_info, applicable_outcomes_themes):
    weighting_boxes = {}

    theme_6_header = w.HTML(value='<h1>Weighting information for Theme 6. Products and materials</h1>')
    M_in_description = w.Label(value='Please provide M_IN, the total annual mass of all inflow products and materials (metric tonnes)')
    M_in = w.BoundedFloatText(value=0.0, min=0.0)
    M_In_container = w.VBox([M_in_description, M_in])
    items_for_box = [theme_6_header, M_In_container]

    M_prod1_description = w.Label(value='Please provide the total annual outflow mass of products and materials that are designed to be consumed (e.g. food and feed) (metric tonnes). Subsequently referred to as M_PROD1.')
    M_prod1 = w.BoundedFloatText(value=0.0, min=0.0)
    M_prod1_container = w.VBox([M_prod1_description, M_prod1])

    M_prod2_description = w.Label(value='Please provide the total annual outflow mass of products and materials that are designed to be used (metric tonnes). Subsequently referred to as M_PROD2.')
    M_prod2 = w.BoundedFloatText(value=0.0, min=0.0)
    M_prod2_container = w.VBox([M_prod2_description, M_prod2])

    M_waste1_description = w.Label(value='Please provide the total annual outflow mass of materials processing waste and by-products that originate from products that are designed to be consumed (e.g. food waste) (metric tonnes). Subsequently referred to as M_WASTE1.', layout=w.Layout(width='1400px'))
    M_waste1 = w.BoundedFloatText(value=0.0, min=0.0)
    M_waste1_container = w.VBox([M_waste1_description, M_waste1])

    M_waste2_description = w.Label(value='Please provide the total annual outflow mass of materials processing waste and by-products that originate from products that are designed to be used (metric tonnes). Subsequently referred to as M_WASTE2.')
    M_waste2 = w.BoundedFloatText(value=0.0, min=0.0)
    M_waste2_container = w.VBox([M_waste2_description, M_waste2])

    if company_info['types_of_flows'] != "Products and materials that are designed to be used":
        items_for_box.append(M_prod1_container)

    if company_info['types_of_flows'] != "Products and materials that are designed to be consumed":
        items_for_box.append(M_prod2_container)

    if company_info['types_of_flows'] != "Products and materials that are designed to be used":
        items_for_box.append(M_waste1_container)

    if company_info['types_of_flows'] != "Products and materials that are designed to be consumed":
        items_for_box.append(M_waste2_container)

    weighting_boxes[6] = w.VBox(items_for_box)

    theme_7_header = w.HTML(value='<h1>Weighting information for Theme 7. Services</h1>')
    services_description = w.Label(value='Please provide the % share of total annual revenue that comes from your company’s services.')
    services = w.BoundedFloatText(value=0.0, min=0.0, max=100.0)
    services_container = w.VBox([theme_7_header, services_description, services])

    weighting_boxes[7] = services_container

    asset_widgets_procured, asset_widgets_owned, ui_8_procured, ui_8_owned = build_theme_8_indicator_ui()

    theme_8_header = w.HTML(value='<h1>Weighting information for Theme 8. Plant, property, and equipment assets</h1>')
    theme_8_subheader = w.HTML(value=
                                 """
                                 <ul>
                                 <li>You should include plant, property, and equipment assets used by your company operations (e.g. office buildings and IT equipment).</li>
                                 <li>You should exclude plant, property, and equipment assets owned by your business but used by customers (e.g. reusable pallets in a product-as-a-service business model), they are in scope of Theme 6 (Products and materials).</li>
                                 </ul>
                                 """)

    prompt_0q_part2 = w.HTML('<h3>0q. Part 2. For each plant, property, and equipment asset category procured in the financial year stated at the beginning of the assessment: Select asset categories that cover a minimum of 80% of the mass estimates provided in 0q. Part 1.</h3>')
    subprompt_0q_part2 = w.HTML('<h4>Your selections here will be used to inform the relevance and weighting of asset groups in indicator 8b.</h4>')
    header = w.Label(value='Asset group', layout=w.Layout(width='200px'))
    asset_selection_table_0q = w.VBox([prompt_0q_part2,subprompt_0q_part2, header] + [w.Checkbox(value=False, description=a, indent=False, style={'description_width': 'initial'}) for a in ASSET_GROUPS])

    prompt_0r_part2 = w.HTML('<h3>0r. Part 2. For each plant, property and equipment asset category procured during or before the financial year (FY) stated at the beginning of the assessment (and owned or leased at any point during the FY). Select asset categories that cover a minimum of 80% of the mass estimates provided in 0r. Part 1.</h3>')
    subprompt_0r_part2 = w.HTML('<h4>Your selections here will be used to inform the relevance and weighting of asset groups in indicator 8b.</h4>')
    header = w.Label(value='Asset group', layout=w.Layout(width='200px'))
    asset_selection_table_0r = w.VBox([prompt_0r_part2, subprompt_0r_part2, header] + [w.Checkbox(value=False, description=a, indent=False, style={'description_width': 'initial'}) for a in ASSET_GROUPS])

    weighting_boxes[8] = w.VBox([theme_8_header, theme_8_subheader, ui_8_procured, ui_8_owned, asset_selection_table_0q, asset_selection_table_0r])

    theme_9_header = w.HTML(value='<h1>Weighting information for Theme 9. Water</h1>')
    theme_9_instructions = w.HTML(value='''
       <ul>
       <li>You should include water flows for operational processes (e.g. cooling water or water used in processes that are not incorporated into products and materials, like water used for dyeing).</li>
        <li>You should exclude material outflows that have water incorporated (e.g. beverages, processed foods, water content in wood), as they are in scope of Theme 6: Products and materials.</li>
        <li>Please refer to the Water Guidelines in the Method Introduction Appendix for more detail on how to account for water in Circulytics.</li>
       </ul>
    ''')
    water_demand_desc = w.Label(value='Please provide the total annual water demand (sourcing plus internal recirculation) volume (megalitres) for your company.')
    water_demand = w.BoundedFloatText(value=0.0, min=0.0)
    water_demand_container = w.VBox([water_demand_desc, water_demand])

    water_outflow_desc = w.Label(value='Please provide the total annual water outflow volume (megalitres) for your company.')
    water_outflow = w.BoundedFloatText(value=0.0, min=0.0)
    water_outflow_container = w.VBox([water_outflow_desc, water_outflow])

    weighting_boxes[9] = w.VBox([theme_9_header, theme_9_instructions, water_demand_container, water_outflow_container])

    theme_10_header = w.HTML(value='<h1>Weighting information for Theme 10. Energy</h1>')
    energy_use_desc = w.Label(value='What is the total annual energy usage (MWh) of your operations?')
    energy_use = w.BoundedFloatText(value=0.0, min=0.0)
    energy_use_container = w.VBox([energy_use_desc, energy_use])
    
    energy_prod_desc = w.Label(value='What is the total annual energy production (MWh) of your company?')
    energy_prod = w.BoundedFloatText(value=0.0, min=0.0)
    if company_info['energy_producer']:
        energy_prod_container = w.VBox([energy_prod_desc, energy_prod])
        weighting_boxes[10] = w.VBox([theme_10_header, energy_use_container, energy_prod_container])
    else:
        weighting_boxes[10] = w.VBox([theme_10_header, energy_use_container])

    theme_11_header = w.HTML(value='<h1>Weighting information for Theme 11. Finance</h1>')
    finance_weight_prompt = w.Label(value='What was the total size of each of the following categories at the end of the financial year stated at the beginning of the assessment (in USD)?')
    lending = w.BoundedFloatText(value=0.0, min=0.0, max=1e10, description='Lending')
    fixed_income = w.BoundedFloatText(value=0.0, min=0.0, max=1e10, description='Fixed income',style = {'description_width': 'initial'}, layout=w.Layout(width='300px'))
    private_eq = w.BoundedFloatText(value=0.0, min=0.0, max=1e10, description='Private equity',style = {'description_width': 'initial'}, layout=w.Layout(width='300px'))
    listed_eq = w.BoundedFloatText(value=0.0, min=0.0, max=1e10, description='Listed equity',style = {'description_width': 'initial'}, layout=w.Layout(width='300px'))
    other_fin_1 = w.BoundedFloatText(value=0.0, min=0.0, max=1e10, description='Other (please specify)',style = {'description_width': 'initial'}, layout=w.Layout(width='300px'))
    other_fin_1_text_entry = w.Text(value='')
    other_fin_2 = w.BoundedFloatText(value=0.0, min=0.0, max=1e10, description='Other (please specify)',style = {'description_width': 'initial'}, layout=w.Layout(width='300px'))
    other_fin_2_text_entry = w.Text(value='')
    other_fin_3 = w.BoundedFloatText(value=0.0, min=0.0, max=1e10, description='Other (please specify)',style = {'description_width': 'initial'}, layout=w.Layout(width='300px'))
    other_fin_3_text_entry = w.Text(value='')
    finance_widgets = [lending, fixed_income, private_eq, listed_eq, other_fin_1,other_fin_1_text_entry, other_fin_2, other_fin_2_text_entry, other_fin_3, other_fin_3_text_entry]
    weighting_boxes[11] = w.VBox([theme_11_header, finance_weight_prompt,lending, fixed_income, private_eq, listed_eq, other_fin_1,other_fin_1_text_entry, other_fin_2, other_fin_2_text_entry, other_fin_3, other_fin_3_text_entry])
    return weighting_boxes, M_in, M_prod1, M_prod2, M_waste1, M_waste2, water_demand, water_outflow, energy_use, energy_prod, asset_widgets_procured, asset_widgets_owned, finance_widgets

def create_indicator_ui(company_info, industry_type, finance_widgets, asset_widgets_owned, asset_widgets_procured):
    # Build the UI interfaces to enter the indicators
    theme_indicator_ui_boxes = {}
    theme_indicator_widgets = {}
    for theme_num, indicators in theme_indicators.items():
        theme_indicator_widgets[theme_num] = {}
        theme_items = []
        theme_items.append(w.HTML(f"<h1>Theme {theme_num}: {theme_names[theme_num]}</h1>"))
        theme_items.append(w.HTML(f"<h2>{theme_descriptions[theme_num]}</h2>"))
        for indicator, info in indicators.items():
            if not company_info['energy_producer'] and indicator == '10b':
                continue
            if not company_info['ownership'] and theme_num == 6 and indicator not in ['6b', '6c']:
                continue
            if company_info["types_of_flows"] == "Products and materials that are designed to be consumed" and theme_num == 6 and indicator in ['6c','6f']:
                continue
            if company_info["types_of_flows"] == "Products and materials that are designed to be used" and theme_num == 6 and indicator == '6b':
                continue
            if info["type"] == "dropdown":
                container, widget = build_dropdown_block(indicator, info['prompt'], info['options'], info['scores'], subprompt = info.get('subprompt', None), bonus_checkbox=info.get('bonus_checkbox', None))
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = widget
            elif info["type"] == "checkbox":
                container, widget = build_checkbox_block(indicator, info['prompt'], info['options'], subprompt = info.get('subprompt', None))
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = widget
            elif info["type"] == "grouped_checkbox":
                container, widget = build_grouped_checkbox_block(indicator, info['prompt'], info['group labels'], info["group sublabels"], info["group options"], subprompt = info.get('subprompt', None))
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = widget
            elif info["type"] == "both":
                container, widget = build_both_block(indicator, info['prompt'], info['dropdown_options'], info['dropdown_scores'], info.get('checkbox_label', "Select all that apply:"), info['checkbox_options'], subprompt = info.get('subprompt', None))
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = widget
            elif info["type"] == "slider":
                container, widget = build_slider_block(indicator, info['prompt'], subprompt = info.get('subprompt', None))
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = widget
            elif info["type"] == "sliders":
                if indicator == "6f_part1":
                    if "UP" in industry_type.value:
                        weights = info["weights_upstream"]
                    else:
                        weights = info["weights_other"]
                elif theme_num == 11: # finance
                    lending, fixed_income, private_eq, listed_eq, other_fin_1,other_fin_1_text_entry, other_fin_2, other_fin_2_text_entry, other_fin_3, other_fin_3_text_entry = finance_widgets
                    category_labels = []
                    category_weights = []
                    for cat, wid in zip(['Lending', 'Fixed income', 'Private equity', 'Listed equity'], [lending, fixed_income, private_eq, listed_eq]):
                        if wid.value > 0.0:
                            category_labels.append(cat)
                            category_weights.append(wid.value)
                    if other_fin_1.value > 0.0:
                        if other_fin_1_text_entry.value.strip() != "":
                            category_labels.append(other_fin_1_text_entry.value.strip())
                        else:
                            category_labels.append("Other 1")
                        category_weights.append(other_fin_1.value)
                    if other_fin_2.value > 0.0:
                        if other_fin_2_text_entry.value.strip() != "":
                            category_labels.append(other_fin_2_text_entry.value.strip())
                        else:
                            category_labels.append("Other 2")
                        category_weights.append(other_fin_2.value)
                    if other_fin_3.value > 0.0:
                        if other_fin_3_text_entry.value.strip() != "":
                            category_labels.append(other_fin_3_text_entry.value.strip())
                        else:
                            category_labels.append("Other 3")
                        category_weights.append(other_fin_3.value)
                    info['items'] = [{"label": lab, "type": "slider"} for lab in category_labels]

                    total_weight = (lending.value + fixed_income.value + private_eq.value + listed_eq.value + other_fin_1.value + other_fin_2.value + other_fin_3.value)
                    if total_weight > 0.0:
                        weights = [w/total_weight for w in category_weights]
                    else:
                        weights = [0.0 for _ in category_weights]
                else:
                    weights = info.get("weights", None)

                container, api = build_composite_slider_block(
                    indicator,
                    info['prompt'],
                    info['items'],
                    weights=weights,
                    subprompt = info.get('subprompt', None)
                )
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = api
            elif info["type"] == "multiple_dropdown":
                container, api = build_grouped_multiple_dropdown_block(
                    indicator,
                    info['prompt'],
                    info['column_descriptions'],
                    info['dropdown_options'],
                    info['dropdown_scores'],
                    info['rows_label'],
                    description_width=info.get('description_width', 'initial'),
                    dropdown_width_px=info.get('cell_width_px', 360),
                    first_col_width_px=info.get('first_col_width_px', 500)
                )
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = api
            elif info["type"] == "checkbox_table":
                if indicator == "8b":
                    total_asset_mass_owned = sum([wid['mass_widget'].value for wid in asset_widgets_owned])
                    if total_asset_mass_owned == 0:
                        owned_asset_weights = {wid['name']: 0.0 for wid in asset_widgets_owned}
                    else:
                        owned_asset_weights = {wid['name']: wid['mass_widget'].value/total_asset_mass_owned for wid in asset_widgets_owned}
                    cell_weights = {}
                    for ri, row in enumerate(info['rows']):
                        for ci, col in enumerate(info['columns']):
                            cell_weights[(ri,ci)] = owned_asset_weights.get(row, 0.0)*info['col_scores'][ci]
                    info['cell_scores'] = cell_weights
                container, api = build_checkbox_table_block(
                    indicator,
                    info['prompt'],
                    info.get('subprompt', None),
                    info['rows'],
                    column_labels=info.get('columns', []),
                    column_descriptions=info.get('column_descriptions', None),
                    index_col_name = info.get('index_col_name', ""),
                    per_col_scores=info.get('col_scores', None),
                    per_cell_scores=info.get('cell_scores', None),
                    description_width=info.get('description_width', 'initial'),
                    cell_width_px=info.get('cell_width_px', 500),
                    first_col_width_px=info.get('first_col_width_px', 500)
                )
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = api
            elif info['type'] == 'float':
                label = w.Label(value=info['prompt'])
                kwargs = {"value": 0.0}
                if 'min' in info:
                    kwargs['min'] = info['min']
                if 'max' in info:
                    kwargs['max'] = info['max']
                float_box = w.BoundedFloatText(**kwargs)
                container = w.VBox([label, float_box])
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = float_box
            elif indicator == "8a":
                total_asset_mass_procured = sum([wid['mass_widget'].value for wid in asset_widgets_procured])
                if total_asset_mass_procured == 0:
                    procured_asset_weights = {wid['name']: 0.0 for wid in asset_widgets_procured}
                else:
                    procured_asset_weights = {wid['name']:wid['mass_widget'].value/total_asset_mass_procured for wid in asset_widgets_procured}

                container, api = build_percentage_table_block(
                    indicator,
                    info['prompt'],
                    info['rows'],
                    info['columns'],
                    info['column_descriptions'],
                    info['column_weights'],
                    procured_asset_weights,
                    asset_widgets_procured=asset_widgets_procured,
                    index_col_name=info.get('index_col_name', "")
                )
                theme_items.append(container)
                theme_indicator_widgets[theme_num][indicator] = api
            else:
                raise NotImplementedError(f"User interface for Indicator type {info['type']} not implemented yet.")

        theme_box = w.VBox(theme_items)
        theme_indicator_ui_boxes[theme_num] = theme_box
    return theme_indicator_ui_boxes, theme_indicator_widgets
    
def build_dropdown_block(indicator_code: str, prompt: str, options: list[str], scores: list[float], subprompt: str | None = None, bonus_checkbox: dict | None = None) -> w.VBox:
    """
    Render a UI box similar to indicators 1a, 1b, and 1c in which the user selects an option from a dropdown menu, with each option having a score
    An option for an optional "bonus checkbox" that adds an additional bonus to the indicator score is also provided.

    Parameters
    ----------
    indicator_code : str
        The code of the indicator (e.g., '1a')
    prompt : str
        The main prompt/question for the indicator
    options : list[str]
        The list of options to display to the user
    scores : list[float]
        The corresponding scores for each option
    subprompt : str | None, optional
        An optional subprompt to display below the main prompt, by default None
    bonus_checkbox : dict | None, optional
        An optional dictionary defining a bonus checkbox with keys 'label' and 'bonus_score', by default None

    Returns
    -------
    w.VBox
        A VBox widget containing the dropdown and optional bonus checkbox
    """
    prompt_h3 = w.HTML(f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>")
    prompts = [prompt_h3]
    if subprompt is not None:
        subprompt_w = w.Label(value=subprompt)
        prompts.append(subprompt_w)
    
    options_list = [w.Label(value=f"{i+1}: {opt}") for i, opt in enumerate(options)]
    dropdown = w.Dropdown(
        options=[(f"Option {i+1}", scores[i]) for i in range(len(options))],
        description=f"Select Answer:",
        style={'description_width': 'initial'}
    )
    items_for_box = prompts + options_list + [dropdown]
    ui = {'dropdown': dropdown}
    if bonus_checkbox is not None:
        cb = w.Checkbox(value=False, description=bonus_checkbox.get('label',''), indent=False, style={'description_width': 'initial'}, layout=w.Layout(width='800px'))
        items_for_box.append(cb)
        ui['bonus_checkbox'] = cb
    return w.VBox(items_for_box), ui

def build_checkbox_block(indicator_code: str, prompt: str, options: list[str], subprompt: str | None = None) -> w.VBox:
    """
    Render a UI box for a 'select all that apply' pattern with checkboxes, similar to indicator 1e.

    Parameters
    ----------
    indicator_code : str
        The code of the indicator (e.g., '1e')
    prompt : str
        The main prompt/question for the indicator
    options : list[str]
        The list of checkbox options to display to the user
    subprompt : str | None, optional
        An optional subprompt to display below the main prompt, by default None
    
    Returns
    -------
    w.VBox
        A VBox widget containing the heading and checkboxes
    list[w.Checkbox]
        A list of the Checkbox widgets created
    """
    # Heading/prompt
    heading_text = f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>"
    if subprompt is not None:
        if "</" in subprompt:
            heading_text += subprompt
        else:
            heading_text += f"<h4>{subprompt}</h4>"
    heading = w.HTML(heading_text)
    cbs = [w.Checkbox(value=False, description=opt, indent=False, style={'description_width': 'initial'}, layout=w.Layout(width='1000px')) for opt in options]
    return w.VBox([heading] + cbs), cbs

def build_grouped_checkbox_block(indicator_code: str, prompt: str, group_labels: list[str],group_sublabels: list[str], group_options: list[list[str]], subprompt: str | None = None) -> w.VBox:
    """
    Render a UI box for a set of checkboxes with a 'select all that apply' pattern divided into groups with headings, similar to indicator 7a part 2.

    Parameters
    ----------
    indicator_code : str
        The code of the indicator (e.g., '7a_part2')
    prompt : str
        The main prompt/question for the indicator
    group_labels : list[str]
        The list of group headings
    group_sublabels : list[str]
        The list of group sublabels/descriptions
    group_options : list[list[str]]
        The list of checkbox options for each group
    subprompt : str | None, optional
        An optional subprompt to display below the main prompt, by default None

    Returns
    -------
    w.VBox
        A VBox widget containing the heading and grouped checkboxes
    list[list[w.Checkbox]]
        A list of lists of Checkbox widgets created for each group
    """
    prompt_h3 = w.HTML(f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>")
    prompts = [prompt_h3]
    if subprompt is not None:
        if "</" in subprompt:
            subprompt_w = w.HTML(subprompt)
        else:
            subprompt_w = w.Label(value=subprompt)
        prompts.append(subprompt_w)
    all_cbs = []
    for glabel, gsublabel, goptions in zip(group_labels, group_sublabels, group_options):
        group_header = w.HTML(f"<h4>{glabel}</h4>")
        prompts.append(group_header)
        sublabel_w = w.Label(value=gsublabel)
        prompts.append(sublabel_w)
        cbs = [w.Checkbox(value=False, description=opt, indent=False, style={'description_width': 'initial'}, layout=w.Layout(width='1000px')) for opt in goptions]
        prompts.extend(cbs)
        all_cbs.append(cbs)
    return w.VBox(prompts), all_cbs

def build_both_block(indicator_code: str, prompt: str, dropdown_options: list[str], dropdown_scores: list[float], checkbox_label: str, checkbox_options: list[str], subprompt: str | None = None) -> w.VBox:
    """
    Render a UI box for an indicator that includes both a dropdown and a set of checkboxes, similar to indicator 1d.

    Parameters
    ----------
    indicator_code : str
        The code of the indicator (e.g., '1d')
    prompt : str
        The main prompt/question for the indicator
    dropdown_options : list[str]
        The list of dropdown options to display to the user
    dropdown_scores : list[float]
        The corresponding scores for each dropdown option
    checkbox_label : str
        The label/question for the checkbox section
    checkbox_options : list[str]
        The list of checkbox options to display to the user
    subprompt : str | None, optional
        An optional subprompt to display below the main prompt, by default None

    Returns
    -------
    w.VBox
        A VBox widget containing the heading, dropdown, and checkboxes
    tuple[w.Dropdown, list[w.Checkbox]]
        A tuple containing the Dropdown widget and a list of Checkbox widgets created
    """
    prompt_h3 = w.HTML(f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>")
    prompts = [prompt_h3]
    if subprompt is not None:
        subprompt_w = w.Label(value=subprompt)
        prompts.append(subprompt_w)
    dd_opts_visible = [w.Label(value=f"{i+1}: {opt}") for i, opt in enumerate(dropdown_options)]
    dropdown = w.Dropdown(
        options=[(f"Option {i+1}", dropdown_scores[i]) for i in range(len(dropdown_options))],
        description=f"Select Answer:",
        style={'description_width': 'initial'}
    )
    cb_prompt = w.HTML(f"<h4>{checkbox_label}</h4>")
    cbs = [w.Checkbox(value=False, description=opt, indent=False, style={'description_width': 'initial'}) for opt in checkbox_options]
    return w.VBox(prompts + dd_opts_visible + [dropdown, cb_prompt] + cbs), (dropdown, cbs)

def build_slider_block(indicator_code: str, prompt: str, min_val: float = 0, max_val: float = 1, step: float = 0.01, subprompt: str | None = None) -> w.VBox:
    """
    Create a UI box for a single FloatSlider input with a heading and description.
    
    Parameters
    ----------
    indicator_code : str
        The code of the indicator (e.g., "6b" or "10a")
    prompt : str
        Descriptive text for the indicator
    min_val : float, optional
        Minimum slider value (default 0)
    max_val : float, optional
        Maximum slider value (default 1)
    step : float, optional
        Step size for slider (default 0.01)
    
    Returns
    -------
    w.VBox
        A VBox widget containing the heading and slider widget
    w.FloatSlider
        The FloatSlider widget created
    """
    heading = [w.HTML(f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>")]
    if subprompt is not None:
        subprompt_w = w.Label(value=subprompt)
        heading.append(subprompt_w)
    slider = w.FloatSlider(
        value=0,
        min=min_val,
        max=max_val,
        step=step,
        description=f"{indicator_code} (%)",
        style={'description_width': 'initial'},
        layout=w.Layout(width='500px'),
        readout_format='.0%'
    )
    return w.VBox(heading+[slider]), slider

def build_composite_slider_block(
    indicator_code: str,
    prompt: str,
    items: list[dict],
    min_val: float = 0.0,
    max_val: float = 1.0,
    step: float = 0.01,
    show_total: bool = True,
    weights: list[float] | None = None,
    cap_total_at: float = 1.0,
    subprompt: str | None = None
):
    """
    Create a UI box for a single indicator with multiple FloatSlider inputs with different weights, plus an optional label for the total score.

    Parameters
    ----------
    indicator_code : str
        The code of the indicator
    prompt : str
        Descriptive text for the indicator
    items : list[dict]
        List of dicts for the different sliders: [{"label": "Reuse/redistribution"}, {"label": "Refurbishment/remanufacture"}, ...]
        Optional per-item overrides:
            {"label": "...", "min": 0, "max": 1, "step": 0.01, "value": 0}
    min_val, max_val, step : float
        Default slider bounds/step applied when item-level overrides are not provided.
    show_total : bool
        Whether to show a dynamic total score below the sliders.
    weights : list[float] | None
        Weights for each slider value used to compute the weighted total. If provided, must match len(items); otherwise, equal weights are used for each slider that add up to 1.
    cap_total_at : float, default 1.0
        Maximum total score
    subprompt : str | None, optional
        An optional subprompt to display below the main prompt

    Returns
    -------
    ui : ipywidgets.VBox
        The composite block widget (heading + sliders + total score label).
    api : dict
        Helper functions and data:
            - "get_values" -> callable returning a dict {label: value}
            - "get_weighted_score" -> callable returning weighted score
            - "sliders" -> list of slider widgets (each w.FloatSlider)
            - "weights" -> weights list
            - "labels" -> list of item labels
    """
    if weights is None:
        weights = [1.0/len(items)] * len(items)

    # Heading
    heading = [w.HTML(f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>")]
    if subprompt is not None:
        if "</" in subprompt:
            subprompt_w = w.HTML(subprompt)
        else:
            subprompt_w = w.Label(value=subprompt)
        heading.append(subprompt_w)

    # Build sliders
    slider_widgets = []
    slider_widget_containers = []
    labels = []
    for i, item in enumerate(items):
        lbl = item.get("label", f"Item {i+1}")
        labels.append(lbl)
        _min = float(item.get("min", min_val))
        _max = float(item.get("max", max_val))
        _step = float(item.get("step", step))
        _val = float(item.get("value", 0.0))
        
        label = w.HTML(f"<p>{lbl}</p>")
        slider_widget_container_items = [label]
        if "sublabel" in item:
            sublabel = w.Label(value=item["sublabel"], layout=w.Layout(width='400px'))
            slider_widget_container_items.append(sublabel)
        slider = w.FloatSlider(
            value=_val,
            min=_min,
            max=_max,
            step=_step,
            style={'description_width': 'initial'},
            layout=w.Layout(width='600px'),
            readout_format='.0%'
        )
        slider_widget_container_items.append(slider)
        slider_widget_containers.append(w.VBox(slider_widget_container_items))
        slider_widgets.append(slider)

    # Total score label (if enabled)
    score_label = w.Label(value="Total score: 0.00%")

    def get_weighted_score():
        vals = [s.value for s in slider_widgets]
        return max(0, min(cap_total_at, sum(wt * val for wt, val in zip(weights, vals))))

    def recompute_totals(*_):
        score = get_weighted_score()
        total_text = f"Total score: {score:.2%}"
        return total_text

    # Container assembly
    block = w.VBox(heading + slider_widget_containers + ([score_label] if show_total else []))

    # API helpers
    def get_values():
        return {lbl: s.value for lbl, s in zip(labels, slider_widgets)}

    # --- Live update
    def _on_change(_):
        score_label.value = recompute_totals()

    for sw in slider_widgets:
        sw.observe(_on_change, names="value")
    _on_change(None)

    api = {
        "get_values": get_values,
        "get_weighted_score": get_weighted_score,
        "sliders": slider_widgets,
        "weights": weights,
        "labels": labels
    }
    return block, api


def build_grouped_multiple_dropdown_block(
    indicator_code: str,
    prompt: str,
    column_descriptions: list[str],
    dropdown_options: list[str],
    dropdown_scores: dict[str, dict[str, list[float]]],
    rows_label: str = "Row",
    description_width: str = 'initial',
    dropdown_width_px: int = 500,
    first_col_width_px: int = 200
):
    """
    Build a multi-dropdown UI where dropdowns are grouped into rows and columns, forming a tablular layout.
    For example, indicator 3b, where each row is a seniority level in the company, each column is a training level, and each dropdown option relates to what extent training is offered at that level.

    Parameters
    ----------
    indicator_code : str
        e.g., "3b"
    prompt : str
        Heading text for the whole block.
    column_descriptions : list[str]
        Descriptions of the different columns, e.g.
        [column_1_label, column_2_label, column_3_label, ...]
    dropdown_options : list[str]
        Descriptions of the dropdown options, e.g.
        [option_1, option_2, option_3, ...]
    dropdown_scores : dict[str, dict[str, list[float]]]
        Scores for the dropdown options, grouped by row and column, e.g.
        { row: { column: [score_for_option_1, score_for_option_2, ...], ... }, ... }
        Scores should be floats 0..1 in the same order as dropdown_options.
    rows_label : str
        Label for the first column (row headings).
    description_width : str
        ipywidgets style for aligning label text.
    dropdown_width_px : int
        Width of each dropdown widget in pixels.
    first_col_width_px : int
        Width of the first column (row labels) in pixels.

    Returns
    -------
    ui : ipywidgets.VBox
        The composite UI block: heading + rows.
    api : dict
        - "get_selections" -> dict[row] -> dict[column] -> selected option index (int or None)
        - "get_scores"     -> dict[row] -> dict[column] -> selected score (float 0..1)
        - "get_total_score"-> float total score (0..1)
        - "widgets"        -> dict[row] -> dict[column] -> dropdown widget
        - "rows"           -> list of rows in display order
        - "columns"        -> dict[row] -> list of columns
    """
    # --- Heading
    heading = w.HTML(f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>")

    desc_html_parts = []
    labels = [f"Option {i+1}" for i in range(len(column_descriptions))]
    for j, (label, desc) in enumerate(zip(labels, column_descriptions), start=1):
        desc_html_parts.append(f"<p><b>{label}</b>: {desc}</p>")
    desc_html = "<div>" + "\n".join(desc_html_parts) + "</div>"
    desc_block = w.Accordion(children=[w.HTML(value=desc_html)])
    desc_block.set_title(0, "Option descriptions")
    desc_block.selected_index = None  # collapsed by default

    # --- Determine level order
    rows = dropdown_scores.keys()

    # --- Column names
    column_names = w.HBox([w.Label(value=rows_label,style={'description_width': description_width}, layout=w.Layout(width=f"{first_col_width_px}px"))]+[ w.Label(value=d,style={'description_width': description_width}, layout=w.Layout(width=f"{dropdown_width_px}px")) for d in labels])

    # --- Build rows per level
    level_rows = [column_names]                      # list of HBox rows
    widgets_map: dict[str, dict[str, w.Dropdown]] = {}

    for lvl in rows:
        # One dropdown per training; label above dropdown
        col_boxes = []
        widgets_map[lvl] = {}

        for t_label in column_descriptions:
            # Pair options as (label, index) to keep index mapping explicit
            dd_options = [(opt, idx) for idx, opt in enumerate(dropdown_options)]
            dd = w.Dropdown(
                options=dd_options,
                style={'description_width': description_width},
                layout=w.Layout(width=f"{dropdown_width_px}px")
            )
            # Store widget
            widgets_map[lvl][t_label] = dd
            col_boxes.append(dd)

        # Row heading for the level + the three dropdowns
        level_heading = w.Label(value=f"{lvl}",style={'description_width': description_width}, layout=w.Layout(width=f"{first_col_width_px}px"))
        row = w.HBox([level_heading] + col_boxes)
        level_rows.append(row)

    # --- Summary label
    summary_label = w.Label(value="Average score: 0.00%")

    # --- Scoring helpers
    def get_selections():
        # {row: {column: selected_index (int or None)}}
        sel = {}
        for lvl in rows:
            sel[lvl] = {}
            for t_label, dd in widgets_map[lvl].items():
                sel[lvl][t_label] = dd.value
        return sel

    def get_scores():
        # {row: {column: score (float 0..1)}}
        out = {}
        selections = get_selections()
        for lvl in rows:
            out[lvl] = {}
            for t_label, sel_idx in selections[lvl].items():
                score_list = dropdown_scores[lvl][t_label]
                if sel_idx is None:
                    out[lvl][t_label] = 0.0
                else:
                    # Map index to score
                    out[lvl][t_label] = float(score_list[sel_idx])
        return out

    def get_total_score():
        s_map = get_scores()
        level_scores = [max([s_map[lvl][t_label] for t_label in column_descriptions]) for lvl in rows]
        if not level_scores:
            return 0.0
        return np.mean(level_scores)

    # --- Live update
    def _on_change(_):
        summary_label.value = f"Score: {get_total_score():.2%}"

    for lvl in rows:
        for dd in widgets_map[lvl].values():
            dd.observe(_on_change, names="value")
    _on_change(None)

    # --- Assemble UI
    ui = w.VBox([heading, desc_block] + level_rows + [summary_label])

    api = {
        "get_selections": get_selections,
        "get_scores": get_scores,
        "get_total_score": get_total_score,
        "widgets": widgets_map,
        "levels": rows,
       }
    return ui, api


def build_checkbox_table_block(
    indicator_code: str,
    prompt: str,
    subprompt: str | None,
    row_labels: list[str],
    column_labels: list[str] = None,
    column_descriptions: list[str] = None,
    index_col_name: str = "",
    per_col_scores: list[float] = None,
    per_cell_scores: dict[tuple, float] = None,
    description_width: str = 'initial',
    cell_width_px: int = 500,
    first_col_width_px: int = 500
):
    """
    Render a table of checkboxes for a single indicator, e.g. indicator 3c

    Parameters
    ----------
    indicator_code : str
        e.g., "3c".
    prompt : str
        Heading text shown at the top.
    row_labels : list[str]
        Functions/units to list as rows (e.g., Innovation/R&D, Corporate strategy, Supply chain, etc.).
    column_labels : list[str]
        list of column names
    per_col_scores : list[float]
        score per checkbox in each column
    per_cell_scores : dict[(row_idx, col_idx) -> float]
        Optional fine-grained scores per cell (if you want different columns to contribute differently).
        If provided, this overrides per_col_scores for those cells.
    description_width : str
        ipywidgets label layout style; 'initial' keeps full label text visible.
    cell_width_px : int
        Width of each checkbox cell (VBox) in pixels.
    first_col_width_px : int
        Width of the first column (row labels) in pixels.

    Returns
    -------
    ui : ipywidgets.VBox
        Composite UI (heading + table + summary).
    api : dict
        - "get_matrix" -> returns dict[row_label] -> dict[column_label] -> bool (checked)
        - "get_row_counts" -> returns dict[row_label] -> int (number of boxes checked in that row)
        - "get_score" -> returns overall score
        - "widgets" -> dict[row_label] -> dict[column_label] -> w.Checkbox
        - "rows" -> list of row labels
        - "cols" -> list of column labels
    """
    # Defaults
    cols = list(column_labels)
    rows = list(row_labels)
    old_rows = rows
    if per_col_scores is None and per_cell_scores is None:
        per_col_scores = [1.0 / len(cols)] * len(cols)  # equal weights
    # only include rows with non-zero per_cell_scores if provided
    if per_cell_scores is not None:
        rows = [r for ri, r in enumerate(rows) if any([per_cell_scores.get((ri, ci), 0.0) > 0.0 for ci in range(len(cols))])]
    # mapping from new row index to old index since per cell scores are based on old indexing
    new_row_idx2old_idx = {rows.index(r): ri for ri, r in enumerate(old_rows) if r in rows}

    if column_descriptions is not None:
        desc_html_parts = []
        for j, (label, desc) in enumerate(zip(cols, column_descriptions), start=1):
            desc_html_parts.append(f"<p><b>{label}</b>: {desc}</p>")
        desc_html = "<div>" + "\n".join(desc_html_parts) + "</div>"
        desc_block = w.Accordion(children=[w.HTML(value=desc_html)])
        desc_block.set_title(0, "Option descriptions")
        desc_block.selected_index = None  # collapsed by default

    # Heading/prompt
    heading_text = f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>"
    if subprompt is not None:
        if "</" in subprompt:
            heading_text += subprompt
        else:
            heading_text += f"<h4>{subprompt}</h4>"
    heading = w.HTML(heading_text)

    # Build header row
    header_cells = [w.Label(value=index_col_name, style={'description_width': description_width}, layout=w.Layout(width=f"{first_col_width_px}px"))]
    header_cells += [w.Label(value=c, style={'description_width': description_width}, layout=w.Layout(width=f"{cell_width_px}px")) for c in cols]
    header_row = w.HBox(header_cells)

    # Build table body
    table_rows = []
    widgets_map: dict[str, dict[str, w.Checkbox]] = {}

    for r in rows:
        row_heading = w.Label(value=r, style={'description_width': description_width}, layout=w.Layout(width=f"{first_col_width_px}px"))
        cell_vboxes = []
        widgets_map[r] = {}
        for c in cols:
            cb = w.Checkbox(value=False, description="", indent=False,
                            layout=w.Layout(width=f"{cell_width_px}px"))
            # label above checkbox
            cell_vboxes.append(w.VBox([cb], layout=w.Layout(width=f"{cell_width_px}px")))
            widgets_map[r][c] = cb

        table_rows.append(w.HBox([row_heading] + cell_vboxes))

    # Summary label
    summary_label = w.Label(value="Score: 0.00%")

    # Scoring helpers
    def get_matrix():
        # dict[row] -> dict[col] -> bool
        m = {}
        for r in rows:
            m[r] = {}
            for c in cols:
                m[r][c] = bool(widgets_map[r][c].value)
        return m

    def get_col_counts():
        counts = {}
        m = get_matrix()
        for c in cols:
            counts[c] = sum(1 for r in rows if m[r][c])
        return counts

    def get_score():
        """
        Computes score based on:
        - per_cell_scores[(row_idx, col_idx)] if provided,
        - else per_col_scores[col_idx] when any cell in column is selected,
        - else 0.

        Returns a % (0..1).
        """
        total = 0.0
        if per_cell_scores:
            # Sum per selected cell using per_cell_scores
            for ri, r in enumerate(rows):
                for ci, c in enumerate(cols):
                    if widgets_map[r][c].value:
                        total += float(per_cell_scores.get((new_row_idx2old_idx[ri], ci), 0.0))
        elif per_col_scores:
            # Sum per selected column using per_col_scores
            if len(per_col_scores) != len(cols):
                raise ValueError("per_col_scores length must match column_labels length.")
            for ci, c in enumerate(cols):
                total += sum([per_col_scores[ci] for r in rows if widgets_map[r][c].value])
        else:
            # Default: each checked cell contributes equally; normalize to 1 by dividing by total cells
            m = get_matrix()
            checked = sum(1 for r in rows for c in cols if m[r][c])
            total_cells = len(rows) * len(cols)
            total = (checked / total_cells) 
            return total

        return max(0.0, min(total, 1.0))

    # Live updates
    def _on_change(_):
        col_cnts = get_col_counts()
        selected_cols = sum(1 for c, k in col_cnts.items() if k > 0)
        summary_label.value = f"Score: {get_score():.2%}"

    for r in rows:
        for c in cols:
            widgets_map[r][c].observe(_on_change, names="value")
    _on_change(None)

    # Assemble UI
    if column_descriptions is not None:
        ui = w.VBox([heading, desc_block, header_row] + table_rows + [summary_label])
    else:
        ui = w.VBox([heading, header_row] + table_rows + [summary_label])

    # API
    api = {
        "get_matrix": get_matrix,
        "get_col_counts": get_col_counts,
        "get_score": get_score,
        "widgets": widgets_map,
        "rows": rows,
        "cols": cols,
    }
    return ui, api



def build_percentage_table_block(
    indicator_code: str,
    prompt: str,
    row_labels: List[str],
    column_labels: List[str],
    option_descriptions: List[str],
    option_weights: List[float],
    row_weights: Dict[str, float],
    index_col_name: str = "",
    description_width: str = 'initial',
    cell_width_px: int = 180,
    step: float = 1,
    enforce_row_total_100: bool = True,
    asset_widgets_procured= None
):
    """
    Render a table of percentage inputs (BoundedFloatText) e.g. for Indicator 8a with per-asset mass weighting.

    Parameters
    ----------
    indicator_code : str
        e.g., "8a".
    prompt : str
        Heading text shown at the top.
    row_labels : list[str]
        Asset categories as rows (e.g., IT equipment, Textiles, Furniture, ...).
    column_labels : list[str]
        Short column labels (e.g., ["Option 1", "Option 2", ...]).
    option_descriptions : list[str]
        Longer descriptions corresponding to each column (shown above the table).
    option_weights : list[float]
        Per-column score weights (e.g., [1.0, 1.0, 0.5, 0.5, 0.0]).
    row_weights: Dict[str, float]
        Per-row weights, e.g. based on asset mass share (e.g., {"IT equipment": 0.2, "Textiles": 0.3, "Furniture": 0.5}).
    description_width : str
        ipywidgets label style; 'initial' keeps full label text visible.
    cell_width_px : int
        Width of each input cell (VBox) in pixels.
    step : float
        Step for percentage input fields, in percent units (e.g., 1.0 -> 1% increment).
    enforce_row_total_100 : bool
        If True, summary will flag rows whose percent total is not 100%.
    asset_widgets_procured : list[dict] | None
        List of asset widget information with following format:
        {
        'name' (str): asset category name,
        'mass_widget' (w.BoundedFloatText): widget with mass of asset category,
        'mass_box' (w.HBox): UI box for entry of mass,
        'applicable_and_mass_not_available' (w.Checkbox): widget for whether the "Applicable and mass not available" option is selected,
        'not_applicable' (w.Checkbox): widget for whether the "not applicable" option is selected
    }

    Returns
    -------
    ui : ipywidgets.VBox
        Composite UI (descriptions + heading + table + summary).
    api : dict
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
    """

    # --- Validation of inputs ---
    if len(column_labels) != len(option_descriptions):
        raise ValueError("column_labels length must match option_descriptions length.")
    if len(column_labels) != len(option_weights):
        raise ValueError("column_labels length must match option_weights length.")

    cols = list(column_labels)
    rows = list(row_labels)

    # --- Heading / prompt ---
    heading = w.HTML(f"<h3>{indicator_code.split('_')[0]}. {prompt}</h3>")

    # --- Column descriptions (above the table) ---
    # Build a single HTML block with bolded option headers and long text underneath
    desc_html_parts = []
    for j, (label, desc) in enumerate(zip(cols, option_descriptions), start=1):
        desc_html_parts.append(f"<p><b>{label}</b>: {desc}</p>")
    desc_html = "<div>" + "\n".join(desc_html_parts) + "</div>"
    desc_block = w.Accordion(children=[w.HTML(value=desc_html)])
    desc_block.set_title(0, "Option descriptions")
    desc_block.selected_index = None  # collapsed by default

    # --- Header row (Asset | Avg mass | Mass input | Options... | Row total) ---
    header_cells = [
        w.Label(value=index_col_name, style={'description_width': description_width},
                layout=w.Layout(width=f"{cell_width_px}px")),
        w.Label(value="Mass (t, FY)", style={'description_width': description_width},
                layout=w.Layout(width=f"{cell_width_px}px")),
    ]
    header_cells += [
        w.Label(value=c, style={'description_width': description_width},
                layout=w.Layout(width=f"{cell_width_px}px"))
        for c in cols
    ]
    header_cells += [w.Label(value="Row total (%)",
                             style={'description_width': description_width},
                             layout=w.Layout(width=f"{cell_width_px}px"))]
    header_row = w.HBox(header_cells)

    # --- Table body ---
    table_rows = []
    widgets_map: Dict[str, Dict[str, w.Widget]] = {}
    asset_masses =  {wid['name']:wid['mass_widget'].value for wid in asset_widgets_procured}
    total_mass = sum(asset_masses.get(r, 0.0) for r in rows)
    row_total_labels: Dict[str, w.HTML] = {}

    # skip assets with zero mass
    rows = [r for r in rows if asset_masses.get(r, 0.0) > 0.0]
    # Build each row
    for r in rows:
        # Cells: Asset label
        row_asset_label = w.Label(
            value=r, style={'description_width': description_width},
            layout=w.Layout(width=f"{cell_width_px}px")
        )
        
        mass_box = w.Label(
            value=str(asset_masses.get(r, 0.0)), style={'description_width': description_width},
            layout=w.Layout(width=f"{cell_width_px}px")
        )

        # Percent inputs per column (bounded 0..100)
        widgets_map[r] = {}
        percent_boxes = []
        for c in cols:
            pct = w.BoundedFloatText(
                value=0.0, min=0.0, max=100, step=step,
                description="", indent=False,
                layout=w.Layout(width=f"{cell_width_px}px"),
            )
            percent_boxes.append(pct)
            widgets_map[r][c] = pct

        # Row total label (updates live)
        total_lbl = w.HTML(
            value=f"<span>0.00%</span>",
            layout=w.Layout(width=f"{cell_width_px}px")
        )
        row_total_labels[r] = total_lbl

        table_rows.append(w.HBox([row_asset_label, mass_box] + percent_boxes + [total_lbl]))

    # --- Summary section ---
    summary_html = w.HTML(value=f"<b>Score:</b> 0.00%")
    warnings_html = w.HTML(value="")  # row-sum warnings
    summary_box = w.VBox([summary_html, warnings_html])

    # --- Helpers / API ---
    def get_matrix() -> Dict[str, Dict[str, float]]:
        """
        Returns % entries as fractions (0..1).
        dict[row] -> dict[col] -> float in [0,1]
        """
        m: Dict[str, Dict[str, float]] = {}
        for r in rows:
            m[r] = {}
            for c in cols:
                # Convert 0..100 percent to fraction
                val = float(widgets_map[r][c].value or 0.0) / 100.0
                m[r][c] = val
        return m

    def get_row_totals() -> Dict[str, float]:
        """
        Sum of percent fractions for each item in the row.
        dict[row] -> float in [0,1]
        """
        m = get_matrix()
        totals = {}
        for r in rows:
            totals[r] = sum(m[r][c] for c in cols)
        return totals

    def get_row_scores() -> Dict[str, float]:
        """
        Per-row score = weighted sum of values for each item in the row
        dict[row] -> float in [0,1]
        """
        m = get_matrix()
        scores = {}
        for r in rows:
            s = 0.0
            for j, c in enumerate(cols):
                s += m[r][c] * float(option_weights[j])
            scores[r] = max(0.0, min(s, 1.0))
        return scores

    def get_overall_score() -> float:
        """
        Overall weighted score = weighted sum of row scores
        """
        scores = get_row_scores()
        return sum(row_weights[r] * scores[r] for r in rows)

    # --- Live updates ---
    def _update_row_totals_and_summary(_=None):
        # Update row totals
        totals = get_row_totals()
        warnings = []
        for r in rows:
            t = totals[r]
            # Row total label
            pct_str = f"{t:.2%}"
            if enforce_row_total_100 and abs(t - 1.0) > 1e-6:
                # Gentle warning coloring
                row_total_labels[r].value = f"<span style='color:#b00020;font-weight:bold'>{pct_str}</span>"
                warnings.append(f"Row '{r}' totals {pct_str} (should be 100%).")
            else:
                row_total_labels[r].value = f"<span>{pct_str}</span>"

        # Update summary
        overall = get_overall_score()

        summary_html.value = (
            f"<b>Score:</b> {overall:.2%}"
        )
        warnings_html.value = (
            "" if not warnings else
            "<div style='color:#b00020'><b>Warnings:</b><br/>" + "<br/>".join(warnings) + "</div>"
        )

    # Observe changes for mass and percent inputs
    for r in rows:
        for c in cols:
            widgets_map[r][c].observe(_update_row_totals_and_summary, names="value")

    # Initial render/update
    _update_row_totals_and_summary()

    # --- Assemble UI ---
    ui = w.VBox([desc_block, heading, header_row] + table_rows + [summary_box])

    # --- API dict ---
    api = {
        "get_matrix": get_matrix,
        "get_row_totals": get_row_totals,
        "get_row_scores": get_row_scores,
        "get_overall_score": get_overall_score,
        "widgets": {
            "percent_inputs": widgets_map,
            "row_total_labels": row_total_labels,
            "summary_html": summary_html,
            "warnings_html": warnings_html,
            "desc_block": desc_block,
        },
        "rows": rows,
        "cols": cols,
       }
    return ui, api
