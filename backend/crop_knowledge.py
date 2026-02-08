"""
India Agricultural Knowledge Base
Comprehensive farming guidance based on ICAR, Ministry of Agriculture recommendations
Enhanced with pulses, oilseeds, vegetables and benefit analysis
"""

# Crop-specific knowledge based on Indian agricultural practices
CROP_KNOWLEDGE = {
    # ============ PULSES ============
    "chickpea": {
        "name_hi": "चना",
        "name_te": "శనగలు",
        "category": "Pulses",
        "optimal_season": ["Rabi"],
        "sowing_months": {"Rabi": "October-November"},
        "harvest_months": {"Rabi": "February-March"},
        "water_requirement_mm": 350,
        "optimal_soil": ["Black", "Loamy", "Sandy loam"],
        "optimal_ph": "6.0-8.0",
        "seed_rate_kg_ha": 75,
        "spacing_cm": "30x10",
        "fertilizer_recommendation": {"N": "20 kg/ha", "P": "40 kg/ha", "K": "20 kg/ha"},
        "major_pests": ["Pod borer", "Cutworm", "Aphids"],
        "major_diseases": ["Wilt", "Ascochyta blight", "Root rot"],
        "irrigation_stages": ["Pre-sowing", "Flowering", "Pod formation"],
        "top_states": ["Madhya Pradesh", "Maharashtra", "Rajasthan", "Uttar Pradesh", "Karnataka"],
        "yield_range_kg_ha": {"min": 800, "max": 2000, "avg": 1200},
        "msp_2024": 5440,
        "tips": [
            "Seed treatment with Rhizobium culture increases yield by 15-20%",
            "Avoid waterlogging - chickpea is highly sensitive",
            "One irrigation at flowering critical for pod filling",
            "Use wilt-resistant varieties in endemic areas"
        ],
        "benefits_analysis": {
            "organic_premium": "20-30% higher price for organic chickpea",
            "nitrogen_fixation": "Fixes 50-80 kg N/ha, saves Rs 2000-3000 on next crop fertilizer",
            "intercropping_benefit": "With mustard increases total income by 25%"
        }
    },
    "pigeon_pea": {
        "name_hi": "अरहर/तूर",
        "name_te": "కందులు",
        "category": "Pulses",
        "optimal_season": ["Kharif"],
        "sowing_months": {"Kharif": "June-July"},
        "harvest_months": {"Kharif": "December-February"},
        "water_requirement_mm": 600,
        "optimal_soil": ["Loamy", "Sandy loam", "Red"],
        "optimal_ph": "5.5-7.0",
        "seed_rate_kg_ha": 15,
        "spacing_cm": "60x20",
        "fertilizer_recommendation": {"N": "20 kg/ha", "P": "50 kg/ha", "K": "20 kg/ha"},
        "major_pests": ["Pod borer", "Pod fly", "Blister beetle"],
        "major_diseases": ["Wilt", "Sterility mosaic", "Phytophthora blight"],
        "irrigation_stages": ["Flowering", "Pod development"],
        "top_states": ["Maharashtra", "Karnataka", "Madhya Pradesh", "Uttar Pradesh", "Gujarat"],
        "yield_range_kg_ha": {"min": 600, "max": 1500, "avg": 900},
        "msp_2024": 7000,
        "tips": [
            "Use ICPL 87119 (Asha) for wilt resistance",
            "Nipping at 30 days promotes branching",
            "IPM with pheromone traps reduces pod borer by 40%",
            "Intercrop with sorghum or cotton for better returns"
        ],
        "benefits_analysis": {
            "ipm_benefit": "IPM reduces pesticide cost by 40% and increases yield by 15%",
            "intercropping_income": "Intercropping adds Rs 15,000-20,000/ha additional income",
            "soil_improvement": "Improves soil nitrogen by 40-50 kg/ha"
        }
    },
    "lentil": {
        "name_hi": "मसूर",
        "name_te": "మసూర్ పప్పు",
        "category": "Pulses",
        "optimal_season": ["Rabi"],
        "sowing_months": {"Rabi": "October-November"},
        "harvest_months": {"Rabi": "February-March"},
        "water_requirement_mm": 300,
        "optimal_soil": ["Loamy", "Clay loam", "Alluvial"],
        "optimal_ph": "6.0-7.5",
        "seed_rate_kg_ha": 40,
        "spacing_cm": "25x5",
        "fertilizer_recommendation": {"N": "20 kg/ha", "P": "40 kg/ha", "K": "20 kg/ha"},
        "major_pests": ["Aphids", "Pod borer", "Cutworm"],
        "major_diseases": ["Rust", "Wilt", "Root rot"],
        "irrigation_stages": ["Pre-sowing", "Flowering"],
        "top_states": ["Madhya Pradesh", "Uttar Pradesh", "Bihar", "West Bengal"],
        "yield_range_kg_ha": {"min": 600, "max": 1500, "avg": 900},
        "msp_2024": 6425,
        "tips": [
            "Conserve soil moisture with mulching",
            "Avoid late sowing - reduces yield significantly",
            "Spray 2% urea at flowering for better grain filling",
            "Harvest when 80% pods turn brown"
        ],
        "benefits_analysis": {
            "water_saving": "Requires 40% less water than wheat",
            "export_potential": "Premium quality fetches 30% higher export prices",
            "residue_benefit": "Crop residue adds Rs 3000/ha value as fodder"
        }
    },
    "moong": {
        "name_hi": "मूंग",
        "name_te": "పెసలు",
        "category": "Pulses",
        "optimal_season": ["Kharif", "Zaid"],
        "sowing_months": {"Kharif": "July", "Zaid": "March-April"},
        "harvest_months": {"Kharif": "September-October", "Zaid": "May-June"},
        "water_requirement_mm": 250,
        "optimal_soil": ["Loamy", "Sandy loam", "Alluvial"],
        "optimal_ph": "6.5-7.5",
        "seed_rate_kg_ha": 20,
        "spacing_cm": "30x10",
        "fertilizer_recommendation": {"N": "20 kg/ha", "P": "40 kg/ha", "K": "20 kg/ha"},
        "major_pests": ["Whitefly", "Thrips", "Pod borer"],
        "major_diseases": ["Yellow mosaic virus", "Powdery mildew", "Cercospora leaf spot"],
        "irrigation_stages": ["Flowering", "Pod development"],
        "top_states": ["Rajasthan", "Maharashtra", "Andhra Pradesh", "Karnataka"],
        "yield_range_kg_ha": {"min": 500, "max": 1200, "avg": 800},
        "msp_2024": 8558,
        "tips": [
            "Use virus-resistant varieties (IPM 02-3, SML 668)",
            "Short duration crop - ideal for crop intensification",
            "Yellow sticky traps reduce whitefly by 60%",
            "Pick mature pods every 3-4 days for multiple harvests"
        ],
        "benefits_analysis": {
            "short_duration": "60-65 day crop allows 3 crops per year",
            "premium_price": "Summer moong fetches 20-30% premium",
            "nitrogen_value": "Adds 20-25 kg N/ha to soil worth Rs 1000"
        }
    },
    "urad": {
        "name_hi": "उड़द",
        "name_te": "మినుములు",
        "category": "Pulses",
        "optimal_season": ["Kharif"],
        "sowing_months": {"Kharif": "June-July"},
        "harvest_months": {"Kharif": "September-October"},
        "water_requirement_mm": 300,
        "optimal_soil": ["Loamy", "Clay loam", "Black"],
        "optimal_ph": "6.5-7.8",
        "seed_rate_kg_ha": 20,
        "spacing_cm": "30x10",
        "fertilizer_recommendation": {"N": "20 kg/ha", "P": "40 kg/ha", "K": "20 kg/ha"},
        "major_pests": ["Stem fly", "Whitefly", "Pod borer"],
        "major_diseases": ["Yellow mosaic virus", "Leaf crinkle", "Powdery mildew"],
        "irrigation_stages": ["Flowering", "Pod filling"],
        "top_states": ["Madhya Pradesh", "Uttar Pradesh", "Maharashtra", "Andhra Pradesh"],
        "yield_range_kg_ha": {"min": 500, "max": 1200, "avg": 750},
        "msp_2024": 6950,
        "tips": [
            "Select YMV resistant varieties",
            "Avoid waterlogging at all costs",
            "Seed treatment with Trichoderma prevents root rot",
            "Harvest when 80% pods mature to avoid shattering"
        ],
        "benefits_analysis": {
            "dal_premium": "Whole urad fetches 40% premium over split dal",
            "idli_industry": "Quality urad for idli makers gets 25% premium",
            "crop_rotation": "Excellent rotation crop after paddy"
        }
    },
    # ============ OILSEEDS ============
    "mustard": {
        "name_hi": "सरसों",
        "name_te": "ఆవాలు",
        "category": "Oilseeds",
        "optimal_season": ["Rabi"],
        "sowing_months": {"Rabi": "October-November"},
        "harvest_months": {"Rabi": "February-March"},
        "water_requirement_mm": 350,
        "optimal_soil": ["Loamy", "Sandy loam", "Alluvial"],
        "optimal_ph": "6.0-7.5",
        "seed_rate_kg_ha": 5,
        "spacing_cm": "45x15",
        "fertilizer_recommendation": {"N": "80 kg/ha", "P": "40 kg/ha", "K": "40 kg/ha", "Sulphur": "40 kg/ha"},
        "major_pests": ["Aphids", "Sawfly", "Painted bug"],
        "major_diseases": ["White rust", "Alternaria blight", "Downy mildew"],
        "irrigation_stages": ["Pre-flowering", "Siliqua formation"],
        "top_states": ["Rajasthan", "Uttar Pradesh", "Haryana", "Madhya Pradesh", "Gujarat"],
        "yield_range_kg_ha": {"min": 1000, "max": 2500, "avg": 1500},
        "msp_2024": 5650,
        "tips": [
            "Apply sulphur for higher oil content (increases by 2-3%)",
            "Control aphids before flowering stage",
            "Thiram seed treatment prevents seedling diseases",
            "Harvest when 75% siliquae turn yellow"
        ],
        "benefits_analysis": {
            "sulphur_roi": "Rs 40 spent on sulphur gives Rs 400 additional return",
            "oil_bonus": "Each 1% increase in oil content = Rs 200/quintal premium",
            "bee_keeping": "Bee colonies increase yield by 20% and give honey income"
        }
    },
    "sunflower": {
        "name_hi": "सूरजमुखी",
        "name_te": "పొద్దుతిరుగుడు",
        "category": "Oilseeds",
        "optimal_season": ["Kharif", "Rabi", "Zaid"],
        "sowing_months": {"Kharif": "June-July", "Rabi": "September-October", "Zaid": "January-February"},
        "harvest_months": {"Kharif": "September-October", "Rabi": "January-February", "Zaid": "April-May"},
        "water_requirement_mm": 500,
        "optimal_soil": ["Loamy", "Clay loam", "Black"],
        "optimal_ph": "6.5-8.0",
        "seed_rate_kg_ha": 5,
        "spacing_cm": "60x30",
        "fertilizer_recommendation": {"N": "60 kg/ha", "P": "60 kg/ha", "K": "30 kg/ha"},
        "major_pests": ["Head borer", "Capitulum borer", "Aphids"],
        "major_diseases": ["Alternaria leaf spot", "Rust", "Downy mildew"],
        "irrigation_stages": ["Button stage", "Flowering", "Seed development"],
        "top_states": ["Karnataka", "Andhra Pradesh", "Maharashtra", "Tamil Nadu"],
        "yield_range_kg_ha": {"min": 1000, "max": 2000, "avg": 1400},
        "msp_2024": 6760,
        "tips": [
            "Use hybrids for 30-40% higher yield",
            "Boron application improves seed setting",
            "Bird scaring needed during maturity",
            "Harvest when back of head turns yellow"
        ],
        "benefits_analysis": {
            "hybrid_advantage": "Hybrids give Rs 8000-12000/ha more income",
            "boron_roi": "Rs 100 boron investment gives Rs 1500 return",
            "oil_quality": "High oleic varieties fetch 15% premium"
        }
    },
    "castor": {
        "name_hi": "अरंडी",
        "name_te": "ఆముదం",
        "category": "Oilseeds",
        "optimal_season": ["Kharif"],
        "sowing_months": {"Kharif": "July-August"},
        "harvest_months": {"Kharif": "November-January"},
        "water_requirement_mm": 500,
        "optimal_soil": ["Sandy loam", "Loamy", "Red"],
        "optimal_ph": "5.5-6.5",
        "seed_rate_kg_ha": 10,
        "spacing_cm": "90x60",
        "fertilizer_recommendation": {"N": "60 kg/ha", "P": "40 kg/ha", "K": "20 kg/ha"},
        "major_pests": ["Semilooper", "Capsule borer", "Tobacco caterpillar"],
        "major_diseases": ["Wilt", "Root rot", "Grey rot"],
        "irrigation_stages": ["Branching", "Flowering", "Capsule development"],
        "top_states": ["Gujarat", "Rajasthan", "Andhra Pradesh", "Telangana"],
        "yield_range_kg_ha": {"min": 1000, "max": 2500, "avg": 1500},
        "msp_2024": 5650,
        "tips": [
            "India is world's largest castor producer",
            "Use GCH-7 hybrid for high yield",
            "IPM reduces pest management cost by 50%",
            "Harvest spikes when capsules turn brown"
        ],
        "benefits_analysis": {
            "export_earning": "India exports 80% of world castor oil - stable demand",
            "intercrop_income": "Intercropping with groundnut adds Rs 10,000/ha",
            "industrial_demand": "Industrial oil demand growing 8% annually"
        }
    },
    "sesame": {
        "name_hi": "तिल",
        "name_te": "నువ్వులు",
        "category": "Oilseeds",
        "optimal_season": ["Kharif"],
        "sowing_months": {"Kharif": "June-July"},
        "harvest_months": {"Kharif": "September-October"},
        "water_requirement_mm": 300,
        "optimal_soil": ["Sandy loam", "Loamy", "Alluvial"],
        "optimal_ph": "5.5-8.0",
        "seed_rate_kg_ha": 4,
        "spacing_cm": "45x15",
        "fertilizer_recommendation": {"N": "40 kg/ha", "P": "20 kg/ha", "K": "20 kg/ha"},
        "major_pests": ["Leaf webber", "Gall fly", "Hawk moth"],
        "major_diseases": ["Phyllody", "Bacterial blight", "Alternaria leaf spot"],
        "irrigation_stages": ["Flowering", "Capsule formation"],
        "top_states": ["West Bengal", "Rajasthan", "Gujarat", "Madhya Pradesh"],
        "yield_range_kg_ha": {"min": 300, "max": 800, "avg": 450},
        "msp_2024": 8635,
        "tips": [
            "Drought tolerant - ideal for rainfed areas",
            "White seeded varieties fetch premium",
            "Harvest when lower capsules start browning",
            "Stack harvested plants upside down to dry"
        ],
        "benefits_analysis": {
            "organic_premium": "Organic sesame fetches 50-100% premium",
            "export_quality": "Japan/Korea markets pay 40% premium for quality",
            "low_input": "Minimal input crop - high profit margin"
        }
    },
    # ============ VEGETABLES ============
    "tomato": {
        "name_hi": "टमाटर",
        "name_te": "టమాట",
        "category": "Vegetables",
        "optimal_season": ["Kharif", "Rabi"],
        "sowing_months": {"Kharif": "June-July", "Rabi": "September-October"},
        "harvest_months": {"Kharif": "October-November", "Rabi": "January-March"},
        "water_requirement_mm": 600,
        "optimal_soil": ["Loamy", "Sandy loam", "Red"],
        "optimal_ph": "6.0-7.0",
        "seed_rate_kg_ha": 0.5,
        "spacing_cm": "60x45",
        "fertilizer_recommendation": {"N": "120 kg/ha", "P": "60 kg/ha", "K": "60 kg/ha"},
        "major_pests": ["Fruit borer", "Whitefly", "Leaf miner", "Thrips"],
        "major_diseases": ["Late blight", "Early blight", "Bacterial wilt", "Tomato leaf curl virus"],
        "irrigation_stages": ["Transplanting", "Flowering", "Fruit development"],
        "top_states": ["Andhra Pradesh", "Madhya Pradesh", "Karnataka", "Odisha", "West Bengal"],
        "yield_range_kg_ha": {"min": 20000, "max": 50000, "avg": 30000},
        "tips": [
            "Stake plants for better quality fruits",
            "Drip irrigation increases yield by 30%",
            "Use TLCV resistant hybrids in endemic areas",
            "Harvest at breaker stage for distant markets"
        ],
        "benefits_analysis": {
            "drip_roi": "Drip saves 40% water and increases yield 30%",
            "staking_benefit": "Staking reduces fruit rot by 50%, increases A-grade by 40%",
            "off_season": "Off-season production fetches 200-300% premium",
            "processing": "Processing grade contract gives stable Rs 8-10/kg"
        }
    },
    "potato": {
        "name_hi": "आलू",
        "name_te": "బంగాళాదుంప",
        "category": "Vegetables",
        "optimal_season": ["Rabi"],
        "sowing_months": {"Rabi": "October-November"},
        "harvest_months": {"Rabi": "February-March"},
        "water_requirement_mm": 500,
        "optimal_soil": ["Sandy loam", "Loamy", "Alluvial"],
        "optimal_ph": "5.5-6.5",
        "seed_rate_kg_ha": 2500,
        "spacing_cm": "60x20",
        "fertilizer_recommendation": {"N": "150 kg/ha", "P": "100 kg/ha", "K": "120 kg/ha"},
        "major_pests": ["Aphids", "Cutworm", "Potato tuber moth"],
        "major_diseases": ["Late blight", "Early blight", "Black scurf", "Common scab"],
        "irrigation_stages": ["Stolon formation", "Tuber bulking", "Maturation"],
        "top_states": ["Uttar Pradesh", "West Bengal", "Bihar", "Gujarat", "Punjab"],
        "yield_range_kg_ha": {"min": 15000, "max": 35000, "avg": 22000},
        "tips": [
            "Use certified seed tubers only",
            "Earthing up twice is essential",
            "Stop irrigation 10 days before harvest",
            "Cure tubers before storage"
        ],
        "benefits_analysis": {
            "certified_seed": "Certified seed gives 25-30% higher yield",
            "cold_storage": "Cold storage allows selling at 40-60% premium",
            "chips_variety": "Chips varieties (Chipsona) fetch Rs 3-5/kg premium",
            "export_quality": "EU export grade fetches 50% premium"
        }
    },
    "onion": {
        "name_hi": "प्याज",
        "name_te": "ఉల్లిపాయ",
        "category": "Vegetables",
        "optimal_season": ["Kharif", "Rabi"],
        "sowing_months": {"Kharif": "June-July", "Rabi": "October-November"},
        "harvest_months": {"Kharif": "October-November", "Rabi": "April-May"},
        "water_requirement_mm": 550,
        "optimal_soil": ["Loamy", "Clay loam", "Alluvial"],
        "optimal_ph": "6.0-7.0",
        "seed_rate_kg_ha": 10,
        "spacing_cm": "15x10",
        "fertilizer_recommendation": {"N": "100 kg/ha", "P": "50 kg/ha", "K": "50 kg/ha", "Sulphur": "30 kg/ha"},
        "major_pests": ["Thrips", "Onion fly", "Mites"],
        "major_diseases": ["Purple blotch", "Stemphylium blight", "Basal rot"],
        "irrigation_stages": ["Bulb initiation", "Bulb development"],
        "top_states": ["Maharashtra", "Karnataka", "Madhya Pradesh", "Gujarat", "Rajasthan"],
        "yield_range_kg_ha": {"min": 15000, "max": 30000, "avg": 20000},
        "tips": [
            "Stop irrigation 15 days before harvest",
            "Cure bulbs for 7-10 days before storage",
            "Proper ventilation in storage reduces losses",
            "Grade before selling for better prices"
        ],
        "benefits_analysis": {
            "storage_timing": "3-month storage can give 100-200% price increase",
            "grading_premium": "A-grade onions fetch 30-40% premium",
            "export_window": "Export during June-August gives best returns",
            "dehydration": "Dehydrated onion contract gives stable income"
        }
    },
    "chilli": {
        "name_hi": "मिर्च",
        "name_te": "మిర్చి",
        "category": "Vegetables",
        "optimal_season": ["Kharif", "Rabi"],
        "sowing_months": {"Kharif": "June-July", "Rabi": "September-October"},
        "harvest_months": {"Kharif": "October-February", "Rabi": "January-May"},
        "water_requirement_mm": 600,
        "optimal_soil": ["Loamy", "Sandy loam", "Black"],
        "optimal_ph": "6.0-7.0",
        "seed_rate_kg_ha": 1.5,
        "spacing_cm": "60x45",
        "fertilizer_recommendation": {"N": "100 kg/ha", "P": "50 kg/ha", "K": "50 kg/ha"},
        "major_pests": ["Thrips", "Mites", "Fruit borer", "Aphids"],
        "major_diseases": ["Leaf curl", "Anthracnose", "Powdery mildew", "Bacterial wilt"],
        "irrigation_stages": ["Transplanting", "Flowering", "Fruit development"],
        "top_states": ["Andhra Pradesh", "Telangana", "Karnataka", "Madhya Pradesh", "Maharashtra"],
        "yield_range_kg_ha": {"min": 8000, "max": 20000, "avg": 12000},
        "tips": [
            "Use virus-free seedlings from protected nursery",
            "Mulching reduces thrips and conserves moisture",
            "Pick red chillies at 75% color development",
            "Solar drying gives better color and quality"
        ],
        "benefits_analysis": {
            "mulching_roi": "Mulching increases yield 25% and reduces pesticide 30%",
            "color_value": "High ASTA color fetches Rs 20-30/kg premium",
            "teja_premium": "Teja variety for export gets 40% premium",
            "oleoresin": "Oleoresin grade chilli fetches stable contract price"
        }
    },
    "brinjal": {
        "name_hi": "बैंगन",
        "name_te": "వంకాయ",
        "category": "Vegetables",
        "optimal_season": ["Kharif", "Rabi"],
        "sowing_months": {"Kharif": "June-July", "Rabi": "October-November"},
        "harvest_months": {"Kharif": "September-December", "Rabi": "January-April"},
        "water_requirement_mm": 550,
        "optimal_soil": ["Loamy", "Clay loam", "Alluvial"],
        "optimal_ph": "5.5-6.5",
        "seed_rate_kg_ha": 0.5,
        "spacing_cm": "60x60",
        "fertilizer_recommendation": {"N": "100 kg/ha", "P": "50 kg/ha", "K": "50 kg/ha"},
        "major_pests": ["Shoot and fruit borer", "Jassids", "Aphids", "Whitefly"],
        "major_diseases": ["Bacterial wilt", "Phomopsis blight", "Little leaf"],
        "irrigation_stages": ["Transplanting", "Flowering", "Fruiting"],
        "top_states": ["West Bengal", "Odisha", "Bihar", "Gujarat", "Andhra Pradesh"],
        "yield_range_kg_ha": {"min": 25000, "max": 50000, "avg": 35000},
        "tips": [
            "Use pheromone traps @ 5/acre for borer monitoring",
            "Clip and destroy affected shoots weekly",
            "Harvest at right maturity - shiny fruits",
            "Avoid waterlogging to prevent bacterial wilt"
        ],
        "benefits_analysis": {
            "ipm_benefit": "IPM reduces borer damage 60% and pesticide cost 40%",
            "frequency_picking": "Regular picking increases total yield 20%",
            "local_varieties": "Local varieties fetch premium in traditional markets"
        }
    },
    "okra": {
        "name_hi": "भिंडी",
        "name_te": "బెండకాయ",
        "category": "Vegetables",
        "optimal_season": ["Kharif", "Zaid"],
        "sowing_months": {"Kharif": "June-July", "Zaid": "February-March"},
        "harvest_months": {"Kharif": "August-October", "Zaid": "April-June"},
        "water_requirement_mm": 400,
        "optimal_soil": ["Loamy", "Sandy loam", "Alluvial"],
        "optimal_ph": "6.0-7.0",
        "seed_rate_kg_ha": 10,
        "spacing_cm": "45x30",
        "fertilizer_recommendation": {"N": "100 kg/ha", "P": "60 kg/ha", "K": "50 kg/ha"},
        "major_pests": ["Shoot and fruit borer", "Jassids", "Whitefly", "Mites"],
        "major_diseases": ["Yellow vein mosaic", "Powdery mildew", "Cercospora leaf spot"],
        "irrigation_stages": ["Germination", "Flowering", "Pod development"],
        "top_states": ["Uttar Pradesh", "Bihar", "West Bengal", "Odisha", "Gujarat"],
        "yield_range_kg_ha": {"min": 8000, "max": 15000, "avg": 10000},
        "tips": [
            "Use YVMV resistant varieties",
            "Pick tender fruits every 2-3 days",
            "Seed treatment with Imidacloprid prevents early pest attack",
            "Summer crop fetches premium prices"
        ],
        "benefits_analysis": {
            "frequent_harvest": "Alternate day picking increases yield 25%",
            "summer_premium": "Summer okra fetches 50-100% premium",
            "export_quality": "Tender 6-8cm fruits get export premium"
        }
    },
    "rice": {
        "name_hi": "धान/चावल",
        "name_te": "వరి/బియ్యం",
        "optimal_season": ["Kharif", "Rabi"],
        "sowing_months": {
            "Kharif": "June-July",
            "Rabi": "November-December"
        },
        "harvest_months": {
            "Kharif": "October-November", 
            "Rabi": "April-May"
        },
        "water_requirement_mm": 1200,
        "optimal_soil": ["Alluvial", "Clay", "Loamy"],
        "optimal_ph": "5.5-6.5",
        "seed_rate_kg_ha": 20,
        "spacing_cm": "20x15",
        "fertilizer_recommendation": {
            "N": "120 kg/ha",
            "P": "60 kg/ha", 
            "K": "40 kg/ha"
        },
        "major_pests": ["Stem borer", "Brown planthopper", "Leaf folder"],
        "major_diseases": ["Blast", "Bacterial leaf blight", "Sheath blight"],
        "irrigation_stages": ["Transplanting", "Tillering", "Flowering", "Grain filling"],
        "top_states": ["West Bengal", "Punjab", "Uttar Pradesh", "Andhra Pradesh", "Tamil Nadu"],
        "yield_range_kg_ha": {"min": 2500, "max": 6500, "avg": 4000},
        "tips": [
            "Maintain 5cm water level during vegetative stage",
            "Apply nitrogen in 3 splits: basal, tillering, panicle initiation",
            "Use zinc sulfate @ 25 kg/ha in zinc deficient soils",
            "Drain field 15 days before harvest"
        ]
    },
    "wheat": {
        "name_hi": "गेहूं",
        "name_te": "గోధుమ",
        "optimal_season": ["Rabi"],
        "sowing_months": {
            "Rabi": "October-November"
        },
        "harvest_months": {
            "Rabi": "March-April"
        },
        "water_requirement_mm": 450,
        "optimal_soil": ["Alluvial", "Loamy", "Clay loam"],
        "optimal_ph": "6.0-7.5",
        "seed_rate_kg_ha": 100,
        "spacing_cm": "22.5 row spacing",
        "fertilizer_recommendation": {
            "N": "120 kg/ha",
            "P": "60 kg/ha",
            "K": "40 kg/ha"
        },
        "major_pests": ["Aphids", "Termites", "Pink stem borer"],
        "major_diseases": ["Rust (Yellow, Brown, Black)", "Karnal bunt", "Powdery mildew"],
        "irrigation_stages": ["Crown root initiation (21 days)", "Tillering (45 days)", "Late jointing (65 days)", "Flowering (85 days)", "Milk stage (100 days)"],
        "top_states": ["Uttar Pradesh", "Punjab", "Haryana", "Madhya Pradesh", "Rajasthan"],
        "yield_range_kg_ha": {"min": 2500, "max": 5500, "avg": 3500},
        "tips": [
            "Timely sowing before November 25 for optimal yield",
            "First irrigation at 21 days is critical for crown root development",
            "Apply nitrogen in 2-3 splits",
            "Watch for yellow rust in North India during February"
        ]
    },
    "cotton": {
        "name_hi": "कपास",
        "name_te": "పత్తి",
        "optimal_season": ["Kharif"],
        "sowing_months": {
            "Kharif": "April-May (irrigated), June-July (rainfed)"
        },
        "harvest_months": {
            "Kharif": "October-January"
        },
        "water_requirement_mm": 700,
        "optimal_soil": ["Black", "Alluvial"],
        "optimal_ph": "6.0-8.0",
        "seed_rate_kg_ha": 2.5,
        "spacing_cm": "90x60",
        "fertilizer_recommendation": {
            "N": "60-80 kg/ha",
            "P": "30 kg/ha",
            "K": "30 kg/ha"
        },
        "major_pests": ["Bollworm", "Whitefly", "Pink bollworm", "Jassids"],
        "major_diseases": ["Root rot", "Bacterial blight", "Verticillium wilt"],
        "irrigation_stages": ["Sowing", "Square formation", "Flowering", "Boll development"],
        "top_states": ["Gujarat", "Maharashtra", "Telangana", "Andhra Pradesh", "Haryana"],
        "yield_range_kg_ha": {"min": 1200, "max": 2200, "avg": 1500},
        "tips": [
            "Use Bt cotton varieties for bollworm resistance",
            "Maintain proper plant population (11,000-13,000 plants/ha)",
            "Install pheromone traps for pink bollworm monitoring",
            "Apply potash for better fiber quality"
        ]
    },
    "sugarcane": {
        "name_hi": "गन्ना",
        "name_te": "చెరకు",
        "optimal_season": ["Annual"],
        "sowing_months": {
            "Annual": "February-March (Spring), October (Autumn)"
        },
        "harvest_months": {
            "Annual": "November-April (10-12 months after planting)"
        },
        "water_requirement_mm": 2000,
        "optimal_soil": ["Alluvial", "Loamy", "Black"],
        "optimal_ph": "6.5-7.5",
        "seed_rate_kg_ha": "35,000-40,000 three-budded setts",
        "spacing_cm": "90-120 between rows",
        "fertilizer_recommendation": {
            "N": "250-300 kg/ha",
            "P": "60-80 kg/ha",
            "K": "60 kg/ha"
        },
        "major_pests": ["Early shoot borer", "Top borer", "Pyrilla", "Woolly aphid"],
        "major_diseases": ["Red rot", "Smut", "Ratoon stunting", "Grassy shoot"],
        "irrigation_stages": ["Germination", "Tillering", "Grand growth", "Maturity"],
        "top_states": ["Uttar Pradesh", "Maharashtra", "Karnataka", "Tamil Nadu", "Gujarat"],
        "yield_range_kg_ha": {"min": 50000, "max": 100000, "avg": 75000},
        "tips": [
            "Use disease-free seed material from registered nurseries",
            "Earthing up twice at 90 and 120 days after planting",
            "Stop irrigation 3 weeks before harvest for better sugar recovery",
            "Ratoon management can give 80% of plant crop yield"
        ]
    },
    "groundnut": {
        "name_hi": "मूंगफली",
        "name_te": "వేరుశెనగ",
        "optimal_season": ["Kharif", "Rabi"],
        "sowing_months": {
            "Kharif": "June-July",
            "Rabi": "October-November"
        },
        "harvest_months": {
            "Kharif": "October-November",
            "Rabi": "March-April"
        },
        "water_requirement_mm": 500,
        "optimal_soil": ["Sandy loam", "Red", "Loamy"],
        "optimal_ph": "6.0-6.5",
        "seed_rate_kg_ha": 100,
        "spacing_cm": "30x10",
        "fertilizer_recommendation": {
            "N": "10-20 kg/ha",
            "P": "40 kg/ha",
            "K": "40 kg/ha",
            "Gypsum": "500 kg/ha at flowering"
        },
        "major_pests": ["Leaf miner", "Aphids", "White grub", "Red hairy caterpillar"],
        "major_diseases": ["Tikka disease", "Collar rot", "Stem rot", "Rust"],
        "irrigation_stages": ["Flowering", "Pegging", "Pod development"],
        "top_states": ["Gujarat", "Andhra Pradesh", "Tamil Nadu", "Karnataka", "Rajasthan"],
        "yield_range_kg_ha": {"min": 1000, "max": 2500, "avg": 1500},
        "tips": [
            "Apply gypsum at flowering for better pod filling",
            "Maintain soil moisture during pegging stage",
            "Harvest at 75-80% mature pods",
            "Dry pods to 8-10% moisture before storage"
        ]
    },
    "soybean": {
        "name_hi": "सोयाबीन",
        "name_te": "సోయాబీన్",
        "optimal_season": ["Kharif"],
        "sowing_months": {
            "Kharif": "June-July (with monsoon onset)"
        },
        "harvest_months": {
            "Kharif": "October-November"
        },
        "water_requirement_mm": 450,
        "optimal_soil": ["Black", "Alluvial", "Loamy"],
        "optimal_ph": "6.0-7.5",
        "seed_rate_kg_ha": 75,
        "spacing_cm": "45x5",
        "fertilizer_recommendation": {
            "N": "20-30 kg/ha (starter)",
            "P": "60-80 kg/ha",
            "K": "40 kg/ha"
        },
        "major_pests": ["Stem fly", "Girdle beetle", "Leaf eating caterpillar", "Pod borer"],
        "major_diseases": ["Yellow mosaic virus", "Bacterial pustule", "Charcoal rot", "Rust"],
        "irrigation_stages": ["Flowering", "Pod formation"],
        "top_states": ["Madhya Pradesh", "Maharashtra", "Rajasthan", "Karnataka"],
        "yield_range_kg_ha": {"min": 1500, "max": 2500, "avg": 2000},
        "tips": [
            "Treat seeds with Rhizobium culture before sowing",
            "Ensure good drainage - waterlogging is fatal",
            "Use certified virus-free seeds",
            "Harvest when 95% pods turn brown"
        ]
    },
    "maize": {
        "name_hi": "मक्का",
        "name_te": "మొక్కజొన్న",
        "optimal_season": ["Kharif", "Rabi"],
        "sowing_months": {
            "Kharif": "June-July",
            "Rabi": "October-November"
        },
        "harvest_months": {
            "Kharif": "September-October",
            "Rabi": "February-March"
        },
        "water_requirement_mm": 500,
        "optimal_soil": ["Loamy", "Alluvial", "Black"],
        "optimal_ph": "5.5-7.5",
        "seed_rate_kg_ha": 20,
        "spacing_cm": "60x25",
        "fertilizer_recommendation": {
            "N": "120 kg/ha",
            "P": "60 kg/ha",
            "K": "40 kg/ha"
        },
        "major_pests": ["Fall armyworm", "Stem borer", "Shoot fly"],
        "major_diseases": ["Turcicum leaf blight", "Maydis leaf blight", "Downy mildew"],
        "irrigation_stages": ["Knee height", "Tasseling", "Silking", "Grain filling"],
        "top_states": ["Karnataka", "Andhra Pradesh", "Tamil Nadu", "Bihar", "Maharashtra"],
        "yield_range_kg_ha": {"min": 2500, "max": 6000, "avg": 4000},
        "tips": [
            "Critical water requirement during tasseling and silking",
            "Use single cross hybrids for higher yield",
            "Watch for fall armyworm - spray at first sign",
            "Harvest at 20-25% grain moisture"
        ]
    },
    "bajra": {
        "name_hi": "बाजरा",
        "name_te": "సజ్జ",
        "optimal_season": ["Kharif"],
        "sowing_months": {
            "Kharif": "June-July"
        },
        "harvest_months": {
            "Kharif": "September-October"
        },
        "water_requirement_mm": 350,
        "optimal_soil": ["Sandy", "Sandy loam", "Light soils"],
        "optimal_ph": "6.0-7.0",
        "seed_rate_kg_ha": 4,
        "spacing_cm": "45x15",
        "fertilizer_recommendation": {
            "N": "40-60 kg/ha",
            "P": "20 kg/ha",
            "K": "20 kg/ha"
        },
        "major_pests": ["Shoot fly", "Stem borer", "Blister beetle"],
        "major_diseases": ["Downy mildew", "Ergot", "Smut"],
        "irrigation_stages": ["Seedling", "Flowering", "Grain filling"],
        "top_states": ["Rajasthan", "Uttar Pradesh", "Gujarat", "Haryana", "Maharashtra"],
        "yield_range_kg_ha": {"min": 800, "max": 2000, "avg": 1200},
        "tips": [
            "Best suited for arid and semi-arid regions",
            "Sow with onset of monsoon",
            "Use hybrid varieties for better yield",
            "Good for intercropping with pulses"
        ]
    },
    "jowar": {
        "name_hi": "ज्वार",
        "name_te": "జొన్న",
        "optimal_season": ["Kharif", "Rabi"],
        "sowing_months": {
            "Kharif": "June-July",
            "Rabi": "September-October"
        },
        "harvest_months": {
            "Kharif": "October-November",
            "Rabi": "January-February"
        },
        "water_requirement_mm": 400,
        "optimal_soil": ["Black", "Clay loam", "Medium black"],
        "optimal_ph": "6.0-8.5",
        "seed_rate_kg_ha": 10,
        "spacing_cm": "45x15",
        "fertilizer_recommendation": {
            "N": "80 kg/ha",
            "P": "40 kg/ha",
            "K": "40 kg/ha"
        },
        "major_pests": ["Shoot fly", "Stem borer", "Armyworm"],
        "major_diseases": ["Grain mold", "Charcoal rot", "Downy mildew"],
        "irrigation_stages": ["Boot stage", "Flowering", "Grain filling"],
        "top_states": ["Maharashtra", "Karnataka", "Madhya Pradesh", "Tamil Nadu", "Andhra Pradesh"],
        "yield_range_kg_ha": {"min": 1000, "max": 3000, "avg": 1500},
        "tips": [
            "Rabi jowar gives better grain quality",
            "Deep black soils retain moisture for rabi season",
            "Use shoot fly resistant varieties for kharif",
            "Harvest at physiological maturity for fodder+grain"
        ]
    }
}

# State-wise agricultural information
STATE_AGRI_INFO = {
    "andhra pradesh": {
        "name_hi": "आंध्र प्रदेश",
        "name_te": "ఆంధ్ర ప్రదేశ్",
        "major_crops": ["Rice", "Cotton", "Groundnut", "Sugarcane", "Maize", "Chillies"],
        "soil_types": ["Alluvial", "Red", "Black", "Laterite"],
        "rainfall_mm": {"min": 500, "max": 1200, "avg": 900},
        "kharif_crops": ["Rice", "Cotton", "Groundnut", "Maize"],
        "rabi_crops": ["Rice", "Groundnut", "Sunflower"],
        "agri_helpline": "1800-180-1551",
        "major_issues": ["Cyclones", "Drought in Rayalaseema", "Pest attacks"],
        "govt_schemes": ["YSR Rythu Bharosa", "YSR Free Crop Insurance"]
    },
    "telangana": {
        "name_hi": "तेलंगाना",
        "name_te": "తెలంగాణ",
        "major_crops": ["Rice", "Cotton", "Maize", "Soybean", "Red gram"],
        "soil_types": ["Red", "Black", "Alluvial"],
        "rainfall_mm": {"min": 700, "max": 1100, "avg": 900},
        "kharif_crops": ["Rice", "Cotton", "Maize", "Soybean"],
        "rabi_crops": ["Rice", "Groundnut", "Maize"],
        "agri_helpline": "1800-599-5553",
        "major_issues": ["Irregular rainfall", "Pink bollworm in cotton"],
        "govt_schemes": ["Rythu Bandhu", "Rythu Bima"]
    },
    "punjab": {
        "name_hi": "पंजाब",
        "name_te": "పంజాబ్",
        "major_crops": ["Wheat", "Rice", "Cotton", "Sugarcane", "Maize"],
        "soil_types": ["Alluvial"],
        "rainfall_mm": {"min": 350, "max": 700, "avg": 500},
        "kharif_crops": ["Rice", "Cotton", "Maize", "Sugarcane"],
        "rabi_crops": ["Wheat", "Potato", "Vegetables"],
        "agri_helpline": "1800-180-1551",
        "major_issues": ["Groundwater depletion", "Stubble burning", "Water logging"],
        "govt_schemes": ["PM-KISAN", "Mera Pani Meri Virasat"]
    },
    "uttar pradesh": {
        "name_hi": "उत्तर प्रदेश",
        "name_te": "ఉత్తర ప్రదేశ్",
        "major_crops": ["Wheat", "Rice", "Sugarcane", "Potato", "Pulses"],
        "soil_types": ["Alluvial"],
        "rainfall_mm": {"min": 600, "max": 1200, "avg": 900},
        "kharif_crops": ["Rice", "Sugarcane", "Maize", "Bajra"],
        "rabi_crops": ["Wheat", "Potato", "Mustard", "Pulses"],
        "agri_helpline": "1800-180-1551",
        "major_issues": ["Floods in eastern UP", "Water scarcity in Bundelkhand"],
        "govt_schemes": ["PM-KISAN", "Pardarshi Kisan Seva Yojana"]
    },
    "maharashtra": {
        "name_hi": "महाराष्ट्र",
        "name_te": "మహారాష్ట్ర",
        "major_crops": ["Cotton", "Sugarcane", "Soybean", "Jowar", "Rice"],
        "soil_types": ["Black", "Laterite", "Alluvial"],
        "rainfall_mm": {"min": 500, "max": 2500, "avg": 1000},
        "kharif_crops": ["Cotton", "Soybean", "Jowar", "Rice"],
        "rabi_crops": ["Wheat", "Jowar", "Gram"],
        "agri_helpline": "1800-233-4000",
        "major_issues": ["Farmer distress", "Erratic monsoon", "Pink bollworm"],
        "govt_schemes": ["Mahatma Phule Shetkari Yojana", "Jalyukt Shivar"]
    },
    "madhya pradesh": {
        "name_hi": "मध्य प्रदेश",
        "name_te": "మధ్య ప్రదేశ్",
        "major_crops": ["Soybean", "Wheat", "Rice", "Cotton", "Pulses"],
        "soil_types": ["Black", "Alluvial", "Red"],
        "rainfall_mm": {"min": 750, "max": 1500, "avg": 1100},
        "kharif_crops": ["Soybean", "Rice", "Cotton", "Maize"],
        "rabi_crops": ["Wheat", "Gram", "Mustard"],
        "agri_helpline": "1800-180-1551",
        "major_issues": ["Irrigation dependency", "Soil degradation"],
        "govt_schemes": ["Mukhyamantri Kisan Kalyan Yojana", "Bhavantar Bhugtan Yojana"]
    },
    "gujarat": {
        "name_hi": "गुजरात",
        "name_te": "గుజరాత్",
        "major_crops": ["Cotton", "Groundnut", "Wheat", "Sugarcane", "Castor"],
        "soil_types": ["Black", "Alluvial", "Sandy"],
        "rainfall_mm": {"min": 300, "max": 1000, "avg": 600},
        "kharif_crops": ["Cotton", "Groundnut", "Castor", "Bajra"],
        "rabi_crops": ["Wheat", "Cumin", "Tobacco"],
        "agri_helpline": "1800-180-1551",
        "major_issues": ["Drought in Saurashtra", "Salinity in coastal areas"],
        "govt_schemes": ["Kisan Suryoday Yojana", "PM-KISAN"]
    },
    "rajasthan": {
        "name_hi": "राजस्थान",
        "name_te": "రాజస్థాన్",
        "major_crops": ["Bajra", "Wheat", "Mustard", "Groundnut", "Cotton"],
        "soil_types": ["Sandy", "Alluvial", "Arid"],
        "rainfall_mm": {"min": 150, "max": 600, "avg": 350},
        "kharif_crops": ["Bajra", "Jowar", "Groundnut", "Cotton"],
        "rabi_crops": ["Wheat", "Mustard", "Gram", "Cumin"],
        "agri_helpline": "1800-180-6127",
        "major_issues": ["Water scarcity", "Desertification", "Locust attacks"],
        "govt_schemes": ["Mukhyamantri Krishak Sathi Yojana"]
    },
    "karnataka": {
        "name_hi": "कर्नाटक",
        "name_te": "కర్ణాటక",
        "major_crops": ["Rice", "Sugarcane", "Maize", "Cotton", "Coffee"],
        "soil_types": ["Red", "Black", "Laterite", "Alluvial"],
        "rainfall_mm": {"min": 500, "max": 4000, "avg": 1200},
        "kharif_crops": ["Rice", "Maize", "Cotton", "Sugarcane"],
        "rabi_crops": ["Rice", "Groundnut", "Jowar"],
        "agri_helpline": "1800-425-1552",
        "major_issues": ["Cauvery water dispute", "Drought in North Karnataka"],
        "govt_schemes": ["Raitha Siri", "PM-KISAN"]
    },
    "tamil nadu": {
        "name_hi": "तमिलनाडु",
        "name_te": "తమిళనాడు",
        "major_crops": ["Rice", "Sugarcane", "Cotton", "Groundnut", "Banana"],
        "soil_types": ["Alluvial", "Red", "Black", "Laterite"],
        "rainfall_mm": {"min": 600, "max": 1500, "avg": 950},
        "kharif_crops": ["Rice", "Cotton", "Maize", "Groundnut"],
        "rabi_crops": ["Rice", "Groundnut", "Pulses"],
        "agri_helpline": "1800-425-1661",
        "major_issues": ["Northeast monsoon dependency", "Cyclones"],
        "govt_schemes": ["Chief Minister's Comprehensive Insurance", "PM-KISAN"]
    }
}

# Disease and pest control recommendations (ICAR guidelines)
PEST_DISEASE_CONTROL = {
    "yellow_leaves": {
        "possible_causes": [
            "Nitrogen deficiency",
            "Iron deficiency (in alkaline soils)",
            "Waterlogging",
            "Root rot",
            "Viral infection"
        ],
        "diagnosis_tips": [
            "Check if yellowing starts from older leaves (nitrogen deficiency)",
            "Check if yellowing is between veins (iron/zinc deficiency)",
            "Check for waterlogging in field",
            "Examine roots for rot"
        ],
        "recommendations": {
            "nitrogen_deficiency": "Apply urea @ 20-25 kg/ha as foliar spray (2% solution)",
            "iron_deficiency": "Apply ferrous sulfate @ 0.5% foliar spray",
            "waterlogging": "Improve drainage, make channels",
            "general": "Get soil tested, consult local agricultural officer"
        }
    },
    "pest_attack": {
        "stem_borer": {
            "symptoms": "Dead hearts in vegetative stage, white ears in reproductive stage",
            "control": [
                "Apply Carbofuran 3G @ 25 kg/ha in leaf whorls",
                "Release Trichogramma japonicum @ 50,000/ha",
                "Use light traps for moth monitoring"
            ]
        },
        "bollworm": {
            "symptoms": "Bore holes in bolls, excreta visible",
            "control": [
                "Use pheromone traps @ 5/ha",
                "Spray NPV @ 250 LE/ha",
                "Apply Spinosad 45 SC @ 0.3 ml/L"
            ]
        },
        "fall_armyworm": {
            "symptoms": "Leaves eaten, presence of caterpillar in whorls",
            "control": [
                "Apply Emamectin benzoate @ 0.4 g/L",
                "Use sand + lime mixture in whorls",
                "Release Trichogramma chilonis"
            ]
        }
    },
    "diseases": {
        "blast": {
            "crop": "Rice",
            "symptoms": "Diamond shaped lesions on leaves, neck rot",
            "control": [
                "Use resistant varieties",
                "Apply Tricyclazole 75 WP @ 0.6 g/L",
                "Avoid excess nitrogen"
            ]
        },
        "rust": {
            "crop": "Wheat",
            "symptoms": "Orange/brown pustules on leaves",
            "control": [
                "Use resistant varieties",
                "Spray Propiconazole 25 EC @ 0.1%",
                "Early sowing helps escape rust"
            ]
        },
        "red_rot": {
            "crop": "Sugarcane",
            "symptoms": "Drying of leaves, red discoloration inside cane",
            "control": [
                "Use disease-free seed material",
                "Hot water treatment of setts (50°C for 2 hours)",
                "Avoid waterlogging"
            ]
        }
    }
}

# Government schemes for farmers
GOVT_SCHEMES = {
    "pm_kisan": {
        "name": "PM-KISAN",
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "benefit": "Rs 6,000 per year in 3 installments",
        "eligibility": "All land-holding farmer families",
        "website": "pmkisan.gov.in"
    },
    "pmfby": {
        "name": "PMFBY",
        "full_name": "Pradhan Mantri Fasal Bima Yojana",
        "benefit": "Crop insurance against natural calamities",
        "premium": "2% for Kharif, 1.5% for Rabi, 5% for commercial crops",
        "website": "pmfby.gov.in"
    },
    "kcc": {
        "name": "Kisan Credit Card",
        "benefit": "Short-term credit at 4% interest (with subsidy)",
        "limit": "Up to Rs 3 lakh at subsidized rate",
        "eligibility": "All farmers including tenant farmers"
    },
    "soil_health_card": {
        "name": "Soil Health Card Scheme",
        "benefit": "Free soil testing and recommendations",
        "website": "soilhealth.dac.gov.in"
    },
    "enam": {
        "name": "e-NAM",
        "full_name": "National Agriculture Market",
        "benefit": "Online trading platform for better prices",
        "website": "enam.gov.in"
    }
}

def get_crop_info(crop_name: str) -> dict:
    """Get detailed crop information"""
    crop_key = crop_name.lower().strip()
    return CROP_KNOWLEDGE.get(crop_key, None)

def get_state_info(state_name: str) -> dict:
    """Get state agricultural information"""
    state_key = state_name.lower().strip()
    return STATE_AGRI_INFO.get(state_key, None)

def get_pest_disease_info(issue: str) -> dict:
    """Get pest/disease control information"""
    return PEST_DISEASE_CONTROL.get(issue, None)
