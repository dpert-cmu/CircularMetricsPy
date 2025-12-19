"""
Input parameters for Circulytics
"""
import ipywidgets as w

layout = w.Layout(width='1000px')

industry_classes = [
    # Consumer / End Products (CP)
    "CP.1 Consumer/end products: Apparel, textiles, footwear",
    "CP.2 Consumer/end products: Building products and household goods",
    "CP.3 Consumer/end products: E-commerce and retail",
    "CP.4 Consumer/end products: Electronic appliances",
    "CP.5 Consumer/end products: Food and beverage",
    "CP.6 Consumer/end products: Health and personal care",
    "CP.7 Consumer/end products: Industrial machinery",
    "CP.8 Consumer/end products: Leisure products, toys",
    "CP.9 Consumer/end products: Transportation products",
    "CP.10 Consumer/end products: Other consumer/end products",

    # Intermediate Products (IP)
    "IP.1 Intermediate products: Construction materials not specified elsewhere",
    "IP.2 Intermediate products: Metal products and parts",
    "IP.3 Intermediate products: Packaging",
    "IP.4 Intermediate products: Plastic products and parts",
    "IP.5 Intermediate products: Wood, paper, and other natural fiber products",
    "IP.6 Intermediate products: Other intermediate products",

    # Upstream Processing (UP)
    "UP.1 Upstream processing: Cement manufacturing",
    "UP.2 Upstream processing: Chemicals manufacturing (incl. intermediate and end product chemicals)",
    "UP.3 Upstream processing: Mining and metals",
    "UP.4 Upstream processing: Up and mid-stream oil and gas",
    "UP.5 Upstream processing: Wood, pulp, natural fibers processing",
    "UP.6 Upstream processing: Other upstream materials processing",

    # Agriculture, Forestry, Fishing (AF)
    "AF.1 Agriculture for food or fiber",
    "AF.2 Animal husbandry, aquaculture, fishing",
    "AF.3 Forestry and silviculture",
    "AF.4 Other agriculture, forestry, fishing",

    # Infrastructure (IN)
    "IN.1 Construction and building: residential, industrial and civil engineering",
    "IN.2 Real estate management and property development",
    "IN.3 Water utilities and waste water management",
    "IN.4 Waste management and materials recirculation",
    "IN.5 Other infrastructure",

    # Transportation (TR)
    "TR.1 Transportation of goods: freight, logistics, storage",
    "TR.2 Transportation of people: airlines, rail, taxis services, cruise lines, marine transport, etc.",
    "TR.3 Other transportation",

    # Energy (EN)
    "EN.1 Downstream oil and gas for energy",
    "EN.2 Electricity generation",
    "EN.3 Energy grid and other infrastructure",
    "EN.4 Energy retail and other services",
    "EN.5 Energy storage",
    "EN.6 Other energy",

    # Finance and Insurance (FI)
    "FI.1 Asset management and ownership",
    "FI.2 Commercial and retail banking",
    "FI.3 Insurance",
    "FI.4 Investment banking",
    "FI.5 Other finance and insurance",

    # Services (SE)
    "SE.1 Education and research",
    "SE.2 Healthcare and social work services",
    "SE.3 Hospitality and leisure facilities",
    "SE.4 Media and entertainment",
    "SE.5 Marketing, communications, PR agencies",
    "SE.6 Professional and commercial services not specified elsewhere",
    "SE.7 Non-profit organisations (incl. philanthropic funders and NGOs not specified elsewhere)",
    "SE.8 Repair, refurbishing, remanufacturing services",
    "SE.9 Telecommunications, software and IT services",
    "SE.10 Other services",

    # Institutions, Governments and Cities (IGC)
    "IGC.1 International and multilateral organisations",
    "IGC.2 European institutions",
    "IGC.3 National government",
    "IGC.4 Subnational government",
    "IGC.5 City government",
    "IGC.6 Local government",
    "IGC.7 Other policy-oriented organisations (incl. policy-oriented NGOs, think tanks and research institutes)"
]
finance_industry_classes = [
    "FI.1 Asset management and ownership",
    "FI.2 Commercial and retail banking",
    "FI.3 Insurance",
    "FI.4 Investment banking",
    "FI.5 Other finance and insurance",
]

theme_names = {
    1: "Strategy and Planning",
    2: "Innovation",
    3: "People and Skills",
    4: "Operations",
    5: "External Engagement",
    6: "Products and materials",
    7: "Services",
    8: "Plant, property, and equipment assets",
    9: "Water",
    10: "Energy",
    11: "Finance",
}
enablers = [1,2,3,4,5]
outcomes = [6,7,8,9,10,11]


ENABLER_THEME_WEIGHTS = {1:0.30,2:0.20,3:0.15,4:0.15,5:0.20}
THEME_5_INDICATOR_WEIGHTS = {'5a':0.30,'5b':0.30,'5c':0.15,'5d':0.15,'5e':0.10}

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


theme_descriptions = {
    1: "Have you placed the circular economy at the heart of your strategy?",
    2: "Are the conditions in place to support the development of innovative circular products and services? Are you innovating towards new circular economy products, systems, or services?",
    3: "Are you supporting your employees? Have you employed people to develop the skills required to transition to a circular business model?",
    4: "Have you invested sufficiently in your digital systems and plant, property, and equipment assets to support the change?",
    5: "Are you promoting your circular economy initiatives and influencing those in your business sphere, such as clients or your supply chain?",
    6: "Are the materials you procure and the products you design supporting a circular economy?",
    7: "Are the services you provide supporting a circular economy?",
    8: "Are you procuring and decommissioning your plant, property, and equipment assets in ways that support a circular economy?",
    9: "If you operate in a water-intensive industry, are you using water in a circular way?",
    10: "Are you procuring renewable energy and (if you are an energy provider) producing renewable energy to support a circular economy?",
    11: "If you are a financial institution, are you intentionally financing companies and projects that support a circular economy?",
}

theme_1_indicators = {
    '1a': {"prompt": "How central is circular economy to your CEO’s agenda?",
        "options": ['Not mentioned in external communications',
                    'Relevant concept (e.g. materials circulation, a new business model that follows the principles of circular economy, acknowledging that the solution is not just resource efficiency) mentioned in the past 12 months, in external communications',
                    'Circular economy mentioned explicitly as a strategic priority once in the past 12 months, in external communications',
                    'Circular economy mentioned explicitly as a strategic priority multiple times in the past 12 months, in external communications'],
            "scores": [0,0.33,0.67,1.0],
                    "type": "dropdown"},
        '1b': {"prompt": "Does your organisational risk management include risks and opportunities related to the transition to a circular economy, and the risks of staying in a linear economy?",
                "options": ['No',
                            'Yes for some parts of the organisation',
                            'Yes for the majority of the organisation',
                            'Yes for the entire organisation'],
                "scores": [0,0.33,0.67,1.0],
                            "type": "dropdown"},
        '1c': {"prompt": "Is your strategy aligned with becoming more circular?",
                "options": ['No relevant mentions of circular economy',
                            'Relevant concept (e.g. materials circulation, new business models that follow the principles of circular economy, not just resource efficiency) mentioned as part of strategic priorities',
                            'Circular economy explicitly mentioned as part of strategic priorities'],
                "scores": [0,0.5,1.0],
                            "type": "dropdown"},
        '1d': {"prompt": "Do you have measurable circular economy targets?",
                "dropdown_options": ['No targets',
                            'Targets are being developed either for a relevant concept (e.g. materials circulation) or circular economy explicitly',
                            'Targets have been developed on organisation level, but are not SMART targets',
                            'SMART targets have been developed on organisation level',
                            'SMART targets have been developed on organisation level and further down on a sub-unit (e.g. business unit or region) level.'],
            "dropdown_scores": [0,0.25,0.5,0.75,0.75],
            "checkbox_options": ['Innovation/R&D/design','Corporate strategy','Corporate finance','Supply chain','Production','Sales/marketing','CE/Sustainability','Other'],
            "checkbox_scores": [0.05]*8,
                            "type": "both"},
        '1e': {"prompt": "Are the following publicly available (e.g. in an annual report)?",
                "options": ['Circular economy strategy','Measurable circular economy targets'],
                "scores": [0.5,0.5],
                "type": "checkbox"},
        '1f': {"prompt": "Do you have a circular economy implementation plan?",
                "options": ['No',
                        'An implementation plan is being developed either for a relevant concept (e.g. materials circulation) or circular economy explicitly',
                        'An implementation plan, which does not go to an actionable level of detail (i.e. does not describe owner, timeline, resource requirements, prerequisites, or potential roadblocks), has been developed',
                        'A detailed implementation plan has been developed for each relevant function/business unit/region with owner, timeline, resource requirements, prerequisites and potential roadblocks ',
                        'A detailed implementation plan has been developed as a key priority to be (in part) implemented in the next 12 months',
                        'A circular economy implementation plan has begun implementation and will be periodically reviewed'],
                        "scores": [0,0.2,0.4,0.6,0.8,1.0],
                            "type": "dropdown"}
        }



theme_2_indicators = {
    "2a_empowerment": {
        "prompt": "To what extent is leadership involved in supporting circular innovation/development projects?",
        "subprompt": "Empowerment: Individuals leading innovation projects have the mandate from top management to work on circular economy innovation and regularly report to top management on circular innovation KPIs.",
        "options": [
            "Not in place",
            "Yes, for at least one innovation project",
            "Yes, for majority of innovation projects",
            "Yes, for all innovation projects"
        ],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    },
    "2a_purpose": {
        "prompt": "To what extent are tools and metrics in place to support circular innovation/development projects?",
        "subprompt": "Purpose: Innovation project briefs outline their contribution towards the company-wide circular economy strategy.",
        "options": [
            "Not in place",
            "Yes, for at least one innovation project",
            "Yes, for majority of innovation projects",
            "Yes, for all innovation projects"
        ],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    },
    "2b_tools": {
        "prompt": "To what extent are tools and metrics in place to support circular innovation/development projects?",
        "subprompt": "Tailored circular economy tools (design guidelines, material selection tools, proof of concept tools, and other resources) are made available to design, sales and marketing, and other relevant teams.",
        "options": ["Not in place", "Yes, for at least one innovation project", "Yes, for majority of innovation projects", "Yes, for all innovation projects"],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    },
    "2b_metrics": {
        "prompt": "To what extent are tools and metrics in place to support circular innovation/development projects?",
        "subprompt": "Tailored circular economy metrics developed for specific innovation projects are used to inform and evaluate design choices and are aligned with strategy and planning on circular economy.",
        "options": ["Not in place", "Yes, for at least one innovation project", "Yes, for majority of innovation projects", "Yes, for all innovation projects"],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    },
    "2c_external_collab": {
        "prompt": "To what extent do you collaborate on circular innovation/development projects? ",
        "subprompt": "External: Regular collaboration (e.g. with customers, suppliers, reverse cycle operators, start-ups) drives circular innovation.",
        "options": ["Not in place", "Yes, for at least one innovation project", "Yes, for majority of innovation projects", "Yes, for all innovation projects"],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    },
    "2c_internal_collab": {
        "prompt": "To what extent do you collaborate on circular innovation/development projects? ",
        "subprompt": "Internal: Innovation projects are led by multidisciplinary teams throughout the projects’ development.",
        "options": ["Not in place", "Yes, for at least one innovation project", "Yes, for majority of innovation projects", "Yes, for all innovation projects"],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    },
    "2d_user_data": {
        "prompt": "To what extent are different data systems in place to support circular innovation/development projects? ",
        "subprompt": """User data: this informs the initial design brief and design choices throughout the projects' development. This includes how data on customers’ use of the products/services can be used to
                inform circular innovation projects. For example, user data for a car manufacturer includes: how
                customers use and share the vehicle; for how long is the vehicle in operation vs. when it’s parked; for
                how long is the product retained; etc.""",
        "options": ["Not in place", "Yes, for at least one innovation project", "Yes, for majority of innovation projects", "Yes, for all innovation projects"],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    },
    "2d_systems_data": {
        "prompt": "To what extent are different data systems in place to support circular innovation/development projects? ",
        "subprompt": """Systems data: data covering the entire product/service journey and the broader system it sits within in
                    (suppliers, manufacturers, marketers, and social, environmental, and technological trends and impacts)
                    is used to inform design choices. Systems data refers to information, beyond direct customers, that
                    inform circular innovation projects. For example, for a car manufacturer this may include: broader
                    trends in mobility for a circular economy and needs from multiple stakeholders involved.""",
        "options": ["Not in place", "Yes, for at least one innovation project", "Yes, for majority of innovation projects", "Yes, for all innovation projects"],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    }
}


theme_3_indicators = {
    "3a_bottom_up": {
        "prompt": "To what extent are your circular economy strategy and implementation plans communicated internally?",
        "subprompt": "Bottom up communication of circular economy initiatives, examples, opportunities. Select all that apply",
        "options": [
            "Internal circular economy case examples communicated using intranet, newsletters, campaigns, etc",
            "Internal feedback channel (which includes circular economy ideas) in use, and has demonstrably led to new circular economy activities or changes to existing activities",
            "Circular economy employee platform, community or committee (e.g. to develop internal or external circular economy activities, products, services)",
            "Circular economy challenges, such as business plan pitching, etc. where anyone can take part",
            "Other (please specify)",
            "Other (please specify)",
        ],
        "scores": [0.50, 0.50, 0.50, 0.50, 0.50,0.50],  # each selected adds its %; cap at 1.0 in code
        "type": "checkbox"
    },
    "3a_top_down": {
        "prompt": "To what extent are your circular economy strategy and implementation plans communicated internally?",
        "subprompt": "Top down communication of circular economy strategy and implementation plans. Select all that apply.",
        "options": [
            "Not communicated / strategy does not exist",
            "Conceptual basis communicated with unit heads",
            "Implications for units communicated",
            "Roles & responsibilities communicated"
        ],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown"
    },
    "3b": {
        "prompt": "To what extent does your company offer circular economy related training within your company?",
        "dropdown_descriptions": {level: ['General training on circular economy principles and concepts','Training on circular economy specific to your industry or business function','Formal on the job training (mentorships, trainee programmes, apprenticeships) on circular economy'] for level in ["Directors and above","Managers","Employees"]},
        "dropdown_options": {level: ["Not offered to all", "Offered to all", "Mandatory for all"] for level in ["Directors and above","Managers","Employees"]},
        "dropdown_scores": {level: {'General training on circular economy principles and concepts': [0.0,0.25,0.5],
                                    'Training on circular economy specific to your industry or business function': [0.0,0.50,1.0],
                                    'Formal on the job training (mentorships, trainee programmes, apprenticeships) on circular economy': [0.0,0.50,1.0]
                                    } for level in ["Directors and above","Managers","Employees"]},
        "type": "multiple_dropdown"
    },
    "3c": {
        "prompt": "In which functions do you have individuals or project teams with responsibility for circular economy implementation?",
        "rows": [
            "Innovation/R&D/design","Corporate strategy","Corporate finance","Supply chain",
            "Production","Sales/marketing","CE/Sustainability","Other"
        ],
        "columns": [
            "No individuals or project teams working on circular economy implementation",
            "Individuals or project teams working on circular economy implementation during the financial reporting year stated in 0a",
            "Individuals or teams who have circular economy codified in their job description/targets/incentives and are working on circular economy implementation"
        ],
        "col_scores": [0.0,0.15,0.20], 
        "type": "checkbox_table"
    }
}

theme_4_indicators = {
    "4a": {
        "prompt": "To what extent is your company implementing digital systems to support circular products or circular services? — select all that apply.",
        "subprompt": """
                • Such digital systems can be either owned or outsourced.
                • This includes both internal and client-facing digital systems that are relevant to the delivery of
                products and services.
                • Digital systems do not have to be purpose built in order to qualify as ‘support circular products
                or circular services’. Existing digital systems can qualify if they meet the criteria set out in the
                definitions for circular products or circular services.
                """,
        "options": [
            "Digital systems required to deliver the circular economy strategy have been identified",
            "The suitability of all relevant digital systems to support circular products and circular services has been reviewed within the last three financial years",
            "Procedural policies have been (re)written for all relevant digital systems to support circular products or circular services, as identified by the last review (within the last three financial years) ",
            "(Re)design of digital systems has been implemented, as identified in the last review (within the last three financial years), and the systems are now suitable to support the delivery of circular products or circular services",
            "At least one pilot case digital system has been reviewed, and relevant procedural policies and (re)designs have been implemented to support circular products or circular services "
        ],
        "scores": [0.25, 0.25, 0.25, 0.25, 0.10],  # EMF exemplar: 25% each + 10% pilot
        "type": "checkbox"
    },
    "4b": {
        "prompt": "To what extent is your company implementing plant, property, and equipment assets to support circular products or circular services? — select all that apply.",
        "subprompt": """
• Such plant, property, and equipment assets can be either owned or outsourced.
• This includes both internal and client-facing plant, property, and equipment assets that are relevant
to the delivery of products and services.
• Plant, property, and equipment assets do not have to be purpose built in order to qualify as
‘support circular products or circular services’. Existing plant, property, and equipment assets can
qualify if they meet the criteria set out in the definitions for circular products or circular services.
                """,
        "options": [
            "Assets needed to deliver on the circular economy strategy have been identified",
            "The suitability of all relevant assets to support circular products and circular services has been reviewed within the last three financial years",
            "Procedural policies have been (re)written for all relevant assets to support circular products or circular services, as identified by the last review (within the last three financial years)",
            "(Re)design of assets has been implemented, as identified in the last review (within the last three financial years), and they are now suitable to support the delivery of circular products or circular services ",
            "At least one pilot case asset has been reviewed, and relevant procedural policies and (re)designs have been implemented to support circular products or circular services"
        ],
        "scores": [0.25, 0.25, 0.25, 0.25, 0.10],
        "type": "checkbox"
    }
}

theme_5_indicators = {
    "5a": {
        "prompt": "To what extent do you engage with suppliers to increase sourcing based on circular economy principles? ",
        "subprompt": 
        """
• Supplier here includes suppliers of materials / products / plant, property, and equipment assets, as
well as suppliers you engage with at the end-of-use or end of functional life of materials / products
/ plant, property, and equipment assets
        """,
        "options": [
            "No interactions involving circular economy as a topic","Ad-hoc interactions involving circular economy as a topic",
            "Ongoing programme with one or more of the top five suppliers by mass using circular economy principles",
            "Ongoing programme with all of the top five suppliers by mass using circular economy principles ",
            "Supplier requirements based on circular economy principles, as specified in contracts, are in place with all of your top five suppliers by mass"
        ],
        "scores": [0.0, 0.25, 0.50, 0.75, 1.0],
        "type": "dropdown",
        "weight": 0.30
    },
    "5b": {
        "prompt": "To what extent do you engage with customers on advancing circular economy topics?",
        "subprompt": "See additional resource: Ellen MacArthur Foundation How to Communicate Circular Economy toolkit",
        "options": ["No interactions involving circular economy as a topic","Ad-hoc interactions involving circular economy as a topic (e.g. circular design guide)",
                    "Ad-hoc interactions involving circular economy as a topic AND a plan in development for an ongoing programme using circular economy principles (e.g. collaboration in communicating the benefits of products and services based on circular economy principles)",
                    "Ongoing programme using circular economy principles with less than 50% of your customers (e.g. repair programme, product as a service, refill scheme, collection and composting service)",
                    "Ongoing programme using circular economy principles with more than 50% of your customers (e.g. repair programme, product as a service, refill scheme, collection and composting service)"],
        "scores": [0.0, 0.25, 0.50, 0.75, 1.0],
        "type": "dropdown",
        "weight": 0.30
    },
    "5c": {
        "prompt": "To what extent do you engage with policymakers to support the transition to a circular economy?",
        "subprompt": "Inspiration for relevant policy topics is included in the Universal Circular Economy Policy Goals",
        "options": ["No interactions involving circular economy as a topic",
                    "Ad-hoc interactions involving circular economy as a topic (e.g. informing policy makers on circular economy topics) ","Regular engagement with policymakers involving circular economy as a topic ",
                    "Regular engagement with existing results to accelerate the transition to a circular economy"],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown",
        "weight": 0.15
    },
    "5d": {
        "prompt": "To what extent do you engage with external investors and/or financiers of your company on circular economy topics?",
        "subprompt": "If the company does not have external investors or financiers, ‘financiers of your company’ may include the owner(s) of the company, or the majority shareholder(s).",
        "options": ["No interactions involving circular economy as a topic",
                    "Ad-hoc interactions involving circular economy as a topic",
                    "Ad-hoc interactions involving circular economy as a topic AND a plan in development for a programme on circular economy specific financing",
                    "Ongoing programme on circular economy specific financing (e.g. regular reporting to investors on the business’ circular economy impacts or securing favourable lending terms due to circular economy alignment)"],
        "scores": [0.0, 0.33, 0.67, 1.0],
        "type": "dropdown",
        "weight": 0.15
    },
    "5e": {
        "prompt": "Do you have a membership of or actively engage with circular economy related initiatives?",
        "rows": [
            "Ellen MacArthur Foundation Business Network",
            "Platform for Accelerating the Circular Economy (PACE)",
            "WBCSD Factor10 Programme",
            "GreenBiz Executive Network",
            "The African Circular Economy Network (ACEN)",
            "The African Circular Economy Alliance (ACEA)",
            "European Remanufacturing Council",
            "Coalition on Circular Economy (Latin America and the Caribbean)",
            "Other"
        ],
        "columns": ["membership", "active engagement"],
        "col_scores": {0.33, 0.67},
        "type": "checkbox_table", 
        "weight": 0.10
    }
}

theme_6_indicators = {
    "6a": {
        "prompt": "What % (by mass) of MIN (from 0m) is:",
        "items": [
            {"label": "Non-virgin (e.g. reused and recycled products and materials)", "type": "slider"},
            {"label": "Sourced from by-products/waste streams (e.g. offcuts of a material that has not previously been in a product)", "type": "slider"},
            {"label": "Virgin but renewable and regeneratively produced: For food, medicine and products for direct human consumption or other products where non-virgin materials are not a legally permitted sourcing option", "type": "slider"},
            {"label": "Virgin but renewable and regeneratively produced: For product and materials designed to be used (not consumed), where non-virgin materials are a legally permitted sourcing option", "type": "slider"},
            {"label": "Virgin but renewable and sustainably produced (products and materials that are produced sustainably, but not regeneratively): For food, medicine and products for direct human consumption or other products where non-virgin materials are not a legally permitted sourcing option", "type": "slider"},
            {"label": "Virgin but renewable and sustainably produced (products and materials that are produced sustainably, but not regeneratively): For product and materials designed to be used (not consumed), where non-virgin materials are a legally permitted sourcing option", "type": "slider"},
            {"label": "None of the above (virgin and not sustainably or regeneratively produced)", "type": "slider"},
            {"label": "Data not available", "type": "slider"},  
        ],
        "weights": [1.0,1.0,1.0,0.5,0.8,0.4,0.0,0.0],
        "type": "sliders"
    },
    "6b": {
        "prompt": "What % (by mass) of MWASTE1 (from 0o. Part 1), is material processing waste or by-products that go to landfill or incineration (and are therefore not recirculated)?",
        "type": "slider",
    },
    "6c": {
        "prompt": "What % (by mass) of MWASTE2 (from 0o. Part 2) is materials processing waste or by-products that go to landfill or incineration (and are therefore not recirculated)?",
        "type": "slider",
    },
    "6d": {
        "prompt": "What % (by mass) of your physical products (MPROD1 + MPROD2 from 0n. Part 1 and 0n. Part 2) are designed along circular economy principles?",
        "items": [
            {"label": "BOTH Category 1 and Category 2", "type": "slider"},
            {"label": "Only Category 1: During use", "type": "slider"},
            {"label": "Only Category 2: End of functional life", "type": "slider"},
            {"label": "Only Category 3: Enabling the circular economy", "type": "slider"},
            {"label": "None of the above", "type": "slider"}
        ],
        "weights": [1.0, 0.5, 0.5, 0.5, 0.0],
        "type": "sliders",
    },
    "6e": {
        "prompt": "Do your product and material outflows (all products, packaging, material processing waste and by-products) (MPROD1 + MPROD2 + MWASTE1 + MWASTE2) (sum of 0n. Part 1, 0n. Part 2, 0o. Part 1, and 0o. Part 2) comply with either of the following chemical restriction lists?",
        "type": "checkbox",
        "options": [
            "No substances from the EU REACH Candidate List nor substances from the ChemSec SIN List have been intentionally added at any concentration or are in any material outflows as contaminants in quantities over 0.1% w/w (1,000 ppm)",
            "Material outflows do not contain any substances from the Cradle to Cradle Certified Products Program Restricted Substances List (RSL) in quantities above the maximum allowable concentration (ppm) defined in the list",
            "No",
            "Data not available"
        ],
        "scores": [1.0, 1.0, 0.0, 0.0]  # each adds 50%; both = 100
    },
    "6f_part1": {
        "prompt": "What % (by mass) of your products and materials (MPROD2 from 0n. Part 2) are recirculated in practice in the following ways (only counting the first cycle of recirculation after initial use):",
        "items": [
            {"label": "Reuse/redistribution", "type": "slider"},
            {"label": "Refurbishment/remanufacture", "type": "slider"},
            {"label": "Recycling", "type": "slider"},
            {"label": "Qualifying nutrient recirculation", "type": "slider"}
        ],
        "weights_upstream": {"reuse": 1.0, "refurb": 1.0, "recycle": 1.0, "nutr": 1.0},
        "weights_other":   {"reuse": 1.0, "refurb": 0.8, "recycle": 0.4, "nutr": 0.4},
        "type": "sliders",
    },
    "6f_part2": {
        "prompt": "For all products and materials that are recirculated through reuse in 6f. Part 1., how many average uses do your products have before reaching the end of functional life?",
        "type": "float",
        "percentage": False
    }
}


theme_7_indicators = {
    "7a_part1": {
        "prompt": "What % of your service revenue is from circular services? ",
        "type": "sliders",
        "items": [
            {"label": "Consultancy & business support", "type": "slider"},
            {"label": "Software (sharing/virtualisation/maintenance/utilisation)", "type": "slider"},
            {"label": "Services using products (PaaS, pay-per-use, etc.)", "type": "slider"},
            {"label": "Recirculation services (refurb/maintenance, buy-back/take-back, waste mgmt, marketplaces)", "type": "slider"},
            {"label": "Other circular service", "type": "slider"}
        ],
        "weights": [1.0,1.0,1.0,1.0,1.0],
    },
    "7a_part2": {
        "prompt": "Select the circular economy principle(s) that the services you highlighted in Part 1 have a positive impact on, and describe the impact. ",
        "type": "grouped_checkbox",
        "group labels": [
                "Eliminate waste & pollution",
                "Keep products & materials in use",
                "Regenerate natural systems"
            ],
            "group sublabels": [
                "All the services that relate to material or products before they are put on the market and that help a circular economy by designing out waste and pollution from the outset. Service activities that offer, enable or facilitate:",
                "All services relating to material or products after they have been used or while in use that help keep materials in the economy, or that help keep the product in use for longer. Service activities that offer, enable or facilitate:",
                "All services that enable keeping nutrients in the (bio)economy, and enhance the health of agricultural and other biological systems the economy relies on. Service activities that offer, enable or facilitate"
            ],
"group options": [
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

        },
}


theme_8_indicators = {
    "8a": {
        "prompt": "For each of the asset groups selected in 0q. Part 2: What % (by mass) of your plant, property, and equipment assets procured in the financial year (as stated in 0a.) were procured with the following circular procurement approaches? ",
        "type": "float_table",
        "rows": [
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
        "columns": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
            "Option 5"
        ],
        "column_descriptions": [
            "Second-hand assets",
            "New assets designed with circular design approaches both during use and end of functional life aspects covered, as defined below",
            """◦
Longevity: Designed for maintenance, longevity, durability in such a way that encourages lengthy
use in practice and at scale (e.g. designed for repair rather than replacement, timeless design with
durable material choices) AND in such a way that does not compromise circular treatment and
end of functional life
◦ Reusability: Designed for multiple uses in such a way that ensures actual reuse in practice and at
scale (e.g. secondary markets, packaging reuse systems, standardised design)
◦ Repairability: Designed for repair in such a way that uses existing systems for repair in practice
and at scale (e.g. network of repair shops, your own repair service). Examples of design choices
are: Modular design / built in predictive maintenance sensors, repair diagnostics etc. / Designed
with right to repair by third parties / Using standardised components across a sector
◦ Regeneratively grown materials of biological origin
◦ Recycled content (only count the % mass that is recycled content)
""",
            """
◦ Leasing model (e.g. assets can be returned at end of use)
◦ Design for disassembly (e.g. Product-component passports, modular design,
reversible connections)
◦ Designed for remanufacturing / refurbishment (e.g. modular design)
◦ Design for recycling (e.g. low materials complexity, low toxicity, ease of separating materials),
whilst prioritising tighter loops (reuse/redistribute, refurbish/remanufacture, and repair) where
possible, in such a way that uses existing recycling systems that operate in practice and at scale
◦ Designed for nutrient recirculation that meets the qualifying conditions (e.g. composting
and anaerobic digestion) in such a way that uses systems in practice and at scale
""",
            "None of the above"
        ],
        "column_weights": [1.0, 1.0, 0.5, 0.5, 0.0],
    },
    "8b": {
        "prompt": "For each of the asset groups selected in 0r. Part 2: Does your company have policies or agreements in place for the end-of-use of existing plant, property and equipment assets (all assets) that enable recirculation in practice?",
        "type": "checkbox_table",
        "rows": [
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
        "columns": [
            "Option 1",
            "Option 2",
            "Option 3",
            "Option 4",
            "Option 5"
        ],
        "column_descriptions": [
            "No, and there are no asset recirculation policies or agreements in place",
            "Work is ongoing to create asset recirculation policies or agreements for some / all assets",
            "Yes, we have asset recirculation policies or agreements, but not for all assets",
            "Yes, and all assets are covered by asset recirculation policies or agreements",
            "Data not available"
        ],
        "col_scores": [0.0, 0.25, 0.50, 1.0, 0.0]
    }
}

theme_9_indicators = {
    "9a": {
        "prompt": "What % (by volume) of your annual water demand (as stated in 0s. Part 1.) is from each of the following sources:",
        "subprompt": """Depending on your responses to 9a, 9b may be relevant.
• Only if you withdraw freshwater (i.e. “Non-potable water from freshwater areas that are not
classified as water-stressed” or “None of the above” are > 0), indicator 9b on water withdrawal
reduction is relevant.""",
        "items": [
            {"label": "Precipitation harvesting", "type": "slider"},
            {"label": "Cascading use of water (direct use of untreated wastewater, in a manner that is safe for the environment and human health)", "type": "slider"},
            {"label": "Internally recirculated water", "type": "slider"},
            {"label": "Seawater", "type": "slider"},
            {"label": "Non-potable water from freshwater areas that are not classified as water-stressed", "type": "slider"},
            {"label": "None of the above (e.g. potable water from freshwater sources, any freshwater sourced from areas classified as water-stressed)", "type": "slider"},
        ],
        "type": "sliders",
        "scores": [1.0,1.0,1.0,1.0,1.0,0.0],
    },
    "9b": {
        "prompt": "Which % (by volume) of your water withdrawal have you reviewed for SMART reduction targets?",
        "subprompt": "This question refers to water withdrawal, which is calculated by the following logic (0s. Part 1. x (Nonpotable water from freshwater areas that are not classified as water-stressed % + None of the above %)):",
        "type": "slider",
    },
    "9c": {
        "prompt": "To what extent do you have plans in place to extract surplus nutrients, metals, chemicals, heat and similar valuable resources before discharging the water used in your processes and operations?",
        "type": "dropdown",
        "options": ["Have not assessed yet","Have assessed, currently developing plans","Processes in place for some of the water used in operations, or for some of the relevant resources","Processes in place for majority of the water used in operations and for majority of the relevant resources "],
        "scores": [0.0, 0.25, 0.50, 0.75],
        "bonus_checkbox": {"label": "With processes in place to extract surplus nutrients, metals, chemicals, heat and similar valuable resources from water used in operations, are the majority of the extracted resources subsequently recirculated (e.g. through heat exchange, as nutrient recirculation that meets the qualifying conditions, etc.)? ", "score_bonus": 0.25}
    },
    "9d": {
        "prompt": "What % (by volume) of water annually used in your operations leaves your infrastructure* (as stated in 0s. Part 2.) in the following ways:",
        "subprompt": "*Including third party monitoring and treatment",
        "items": [
            {"label": "For reuse elsewhere (as part of symbiosis, cascading)", "type": "slider"},
            {"label": 
                """
                Fulfilling all of the following requirements:
                • After volume monitoring
                • AND quality monitoring, ensuring the same or higher quality than the surrounding (healthy) ecosystem,
                • AND in the case of original freshwater, to one of the following purposes:
                    ◦ recharge local aquifers/groundwater
                    ◦ replenish rivers/lakes/wetlands
                    ◦ local societal purposes (e.g. drinking water supply)
                • AND in the case of original saltwater, back to a saltwater body
             """, "type": "slider"},
             {"label":
              """
              None of the above, including any water discharge without water quality monitoring and any water
                discharge without quantity monitoring. Water discharge of original freshwater to a saltwater body
                also counts towards this response option. This also includes evaporation or spillage
            """,  "type": "slider"},
            {"label": "Data not available", "type": "slider"},
        ],
        "type": "sliders",
        "scores": [1.0,1.0,0.0,0.0],
    }
}

theme_10_indicators = {
    "10a": {
        "prompt": "What % of energy (electricity, heat, and fuel) for your operations (as stated in 0t. Part 1.) is renewable energy?",
        "type": "slider",
    },
    "10b": {
        "prompt": "What % of the energy you produce (as stated in 0t. Part 2.) is renewable energy?",
        "type": "slider",
    }
}

theme_11_indicators = {
    "11a": {
        "prompt": "What % of each of the following categories’ total in USD (as stated in 0u.) do you screen positively for circular economy alignment?",
        "subprompt": "Please refer to the EU taxonomy to assess alignment. In addition to this, we include the production of renewable energy. Please provide a description of how the screening is performed.",
        "items": [
            {"label": "Lending", "type": "slider"},
            {"label": "Fixed Income", "type": "slider"},
            {"label": "Private Equity", "type": "slider"},
            {"label": "Listed Equity", "type": "slider"},
            {"label": "Other (specify)", "type": "slider"},
            {"label": "Other (specify)", "type": "slider"},
            {"label": "Other (specify)", "type": "slider"},
        ],
        "type": "sliders",
    },
    "11b": {
               "prompt": "What % of each of the following categories’ total in USD (as stated in 0u.) goes toward financing the circular economy?",
               "subprompt": "Please refer to the EU taxonomy to assess alignment. In addition to this, we would include the production of renewable energy",
                "items": [
                     {"label": "Lending", "type": "slider"},
                     {"label": "Fixed Income", "type": "slider"},
                     {"label": "Private Equity", "type": "slider"},
                     {"label": "Listed Equity", "type": "slider"},
                     {"label": "Other (specify)", "type": "slider"},
            {"label": "Other (specify)", "type": "slider"},
            {"label": "Other (specify)", "type": "slider"},
                ],
        "type": "sliders",
    }
}

theme_indicators = {
    1: theme_1_indicators,
    2: theme_2_indicators,
    3: theme_3_indicators,
    4: theme_4_indicators,
    5: theme_5_indicators,
    6: theme_6_indicators,
    7: theme_7_indicators,
    8: theme_8_indicators,
    9: theme_9_indicators,
    10: theme_10_indicators,
    11: theme_11_indicators}