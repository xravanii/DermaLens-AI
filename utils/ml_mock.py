# Mock ML response object representing a skin assessment payload.
# UI elements read dynamic values from this dictionary.

MOCK_RESPONSE = {
    "concern": "Whiteheads",
    "confidence": 87.0,
    "skin_type": "Oily",
    "skin_health": 88,
    "hydration": 72,
    "oil_balance": 81,
    "barrier_health": 90,
    "sensitivity": "Medium",
    
    # Detailed recommendations mapping directly to UI Ingredient Cards
    "recommendations": [
        {
            "name": "Salicylic Acid",
            "benefits": "Unclogs pores & controls sebum production",
            "usage": "Night",
            "frequency": "2–3 times/week"
        },
        {
            "name": "Niacinamide",
            "benefits": "Regulates oil, strengthens skin barrier, reduces redness",
            "usage": "Morning & Night",
            "frequency": "Daily"
        },
        {
            "name": "Oil-Free Moisturizer",
            "benefits": "Provides lightweight hydration without clogging pores",
            "usage": "Morning & Night",
            "frequency": "Daily"
        }
    ],
    
    # Ingredients to avoid list
    "avoid": [
        {
            "name": "Heavy Oils",
            "benefits": "Can clog pores and exacerbate acne/whiteheads",
            "type": "Comedogenic"
        },
        {
            "name": "Alcohol Toners",
            "benefits": "Strip the skin moisture barrier, causing rebound oiliness",
            "type": "Drying Agent"
        },
        {
            "name": "Harsh Scrubs",
            "benefits": "Causes micro-tears and spreads bacteria in active areas",
            "type": "Physical Irritant"
        }
    ],
    
    # Routines
    "morning_routine": [
        {"step": "Gentle Cleanser", "desc": "Cleanse sweat and overnight products without stripping."},
        {"step": "Niacinamide Serum", "desc": "Apply 3-4 drops to balance oil production and strengthen barrier."},
        {"step": "Oil-Free Moisturizer", "desc": "Seal in hydration with a lightweight gel formula."},
        {"step": "SPF 50 Sunscreen", "desc": "Protect against UV damage (crucial when using exfoliating acids)."}
    ],
    
    "night_routine": [
        {"step": "Cleanser", "desc": "Double cleanse if needed to remove sebum, dirt, and pollution."},
        {"step": "Salicylic Acid", "desc": "Apply thin layer to whitehead-prone areas (T-zone)."},
        {"step": "Moisturizer", "desc": "Soothe and restore skin barrier during overnight regeneration."}
    ]
}
