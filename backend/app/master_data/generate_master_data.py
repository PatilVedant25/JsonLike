"""
Generator and manager for Master Data controlled vocabularies.
"""
import os
import json

MASTER_DATA_DIR = os.path.dirname(os.path.abspath(__file__))

def create_fractions_table():
    fractions = {}
    for numerator in range(1, 64):
        decimal = numerator / 64.0
        # Reduce fraction
        def gcd(a, b):
            while b:
                a, b = b, a % b
            return a
        common = gcd(numerator, 64)
        reduced_n = numerator // common
        reduced_d = 64 // common
        frac_str = f"{reduced_n}/{reduced_d}"
        fractions[f"{decimal:.6f}".rstrip('0').rstrip('.')] = frac_str
    
    # Common decimals
    fractions["0.045"] = "0.045"
    fractions["0.040"] = "0.040"
    fractions["0.094"] = "3/32"
    fractions["0.109"] = "7/64"
    fractions["0.125"] = "1/8"
    fractions["0.25"] = "1/4"
    fractions["0.375"] = "3/8"
    fractions["0.5"] = "1/2"
    fractions["0.625"] = "5/8"
    fractions["0.75"] = "3/4"
    fractions["0.875"] = "7/8"
    
    with open(os.path.join(MASTER_DATA_DIR, "fractions_table.json"), "w", encoding="utf-8") as f:
        json.dump(fractions, f, indent=2)

def create_uom_standards():
    uom_data = {
        "approved_uoms": {
            "in": {"type": "length", "capture": "in", "example": "24 in"},
            "ft": {"type": "length", "capture": "ft", "example": "16 ft"},
            "yd": {"type": "length", "capture": "yd", "example": "5 yd"},
            "mm": {"type": "length", "capture": "mm", "example": "20 mm"},
            "cm": {"type": "length", "capture": "cm", "example": "10 cm"},
            "m": {"type": "length", "capture": "m", "example": "2 m"},
            "V": {"type": "voltage", "capture": "V", "example": "120 V"},
            "A": {"type": "amperage", "capture": "A", "example": "15 A"},
            "W": {"type": "wattage", "capture": "W", "example": "60 W"},
            "kW": {"type": "power", "capture": "kW", "example": "1.5 kW"},
            "HP": {"type": "power", "capture": "HP", "example": "2 HP"},
            "kW-hr": {"type": "energy", "capture": "kW-hr", "example": "240 kW-hr"},
            "dBA": {"type": "sound", "capture": "dBA", "example": "47 dBA"},
            "K": {"type": "color_temp", "capture": "K", "example": "2700 K"},
            "lm": {"type": "luminous_flux", "capture": "lm", "example": "800 lm"},
            "Grit": {"type": "abrasive_grit", "capture": "Grit", "example": "220 Grit"},
            "pc": {"type": "count", "capture": "pc", "example": "6 pc"},
            "pk": {"type": "count", "capture": "pk", "example": "4 pk"},
            "Disc/Box": {"type": "packaging", "capture": "Disc/Box", "example": "50 Disc/Box"},
            "Sheets/Box": {"type": "packaging", "capture": "Sheets/Box", "example": "50 Sheets/Box"},
            "CT": {"type": "count", "capture": "CT", "example": "500 CT"},
            "M": {"type": "count", "capture": "M", "example": "4 M"},
            "lb": {"type": "weight", "capture": "lb", "example": "5 lb"},
            "oz": {"type": "weight_volume", "capture": "oz", "example": "24 oz"},
            "cu-ft": {"type": "volume", "capture": "cu-ft", "example": "21 cu-ft"},
            "gal": {"type": "volume", "capture": "gal", "example": "5 gal"},
            "TPI": {"type": "threads", "capture": "TPI", "example": "10 TPI"},
            "rpm": {"type": "speed", "capture": "rpm", "example": "5000 rpm"},
            "deg": {"type": "angle", "capture": "deg", "example": "30 deg"},
            "GA": {"type": "gauge", "capture": "GA", "example": "18 GA"},
            "Ah": {"type": "battery_capacity", "capture": "Ah", "example": "8 Ah"}
        },
        "uom_synonyms": {
            "inch": "in",
            "inches": "in",
            "in.": "in",
            '"': "in",
            "foot": "ft",
            "feet": "ft",
            "ft.": "ft",
            "'": "ft",
            "volt": "V",
            "volts": "V",
            "v": "V",
            "amp": "A",
            "amps": "A",
            "ampere": "A",
            "a": "A",
            "watt": "W",
            "watts": "W",
            "w": "W",
            "kelvin": "K",
            "k": "K",
            "dba": "dBA",
            "db": "dBA",
            "decibel": "dBA",
            "grit": "Grit",
            "piece": "pc",
            "pieces": "pc",
            "pack": "pk",
            "ct": "CT",
            "count": "CT",
            "cf": "cu-ft",
            "cu ft": "cu-ft",
            "ga": "GA",
            "gauge": "GA",
            "ah": "Ah",
            "amp-hour": "Ah"
        },
        "rules": [
            "Always include exactly one space between numerical value and UOM abbreviation (e.g. '24 in', '120 V', '15 A').",
            "Never append periods to unit abbreviations unless part of a sentence.",
            "Always convert decimal inches to standard fractional representations where applicable (e.g. 50.25 in -> 50-1/4 in).",
            "Keep dimension combinations standardized (e.g. '24 in W x 24-1/4 in D', '33-7/16 in H x 23-7/8 in W x 22-5/8 in D')."
        ]
    }
    with open(os.path.join(MASTER_DATA_DIR, "uom_standards.json"), "w", encoding="utf-8") as f:
        json.dump(uom_data, f, indent=2)

def create_manufacturers_data():
    mfr_brands = {
        "APPDE": {
            "distributor": "Appliance Dealers Cooperative (APPDE)",
            "patterns": [
                {"prefix": "PDSH", "brand": "FRIGIDAIRE®", "manufacturer": "Rheem Manufacturing", "series": "Professional Series", "category": "Dishwashers"},
                {"prefix": "PCFE", "brand": "FRIGIDAIRE®", "manufacturer": "Rheem Manufacturing", "series": "Professional Series", "category": "Ranges"},
                {"prefix": "PMOS", "brand": "FRIGIDAIRE®", "manufacturer": "Rheem Manufacturing", "series": "Professional Series", "category": "Microwaves"},
                {"prefix": "GCFG", "brand": "FRIGIDAIRE®", "manufacturer": "Rheem Manufacturing", "series": "Gallery Series", "category": "Ranges"},
                {"prefix": "PRFS", "brand": "FRIGIDAIRE®", "manufacturer": "Rheem Manufacturing", "series": "Professional Series", "category": "Refrigerators"},
                {"prefix": "WDTS", "brand": "Whirlpool®", "manufacturer": "Whirlpool Corporation", "series": "Eco Series", "category": "Dishwashers"},
                {"prefix": "WSGS", "brand": "Whirlpool®", "manufacturer": "Whirlpool Corporation", "series": "Eco Series", "category": "Ranges"},
                {"prefix": "WMMS", "brand": "Whirlpool®", "manufacturer": "Whirlpool Corporation", "series": "Eco Series", "category": "Microwaves"},
                {"prefix": "MVWP", "brand": "Whirlpool®", "manufacturer": "Whirlpool Corporation", "series": "Commercial Series", "category": "Washing Machines"},
                {"prefix": "KDFM", "brand": "KitchenAid®", "manufacturer": "Whirlpool Corporation", "series": "PrintShield Series", "category": "Dishwashers"},
                {"prefix": "KDTS", "brand": "KitchenAid®", "manufacturer": "Whirlpool Corporation", "series": "Architect Series", "category": "Dishwashers"},
                {"prefix": "KDPS", "brand": "KitchenAid®", "manufacturer": "Whirlpool Corporation", "series": "Color Finish Series", "category": "Dishwashers"},
                {"prefix": "KSES", "brand": "KitchenAid®", "manufacturer": "Whirlpool Corporation", "series": "Architect Series", "category": "Ranges"},
                {"prefix": "KMMF", "brand": "KitchenAid®", "manufacturer": "Whirlpool Corporation", "series": "Architect Series", "category": "Microwaves"},
                {"prefix": "PDT", "brand": "GE Profile™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Profile Series", "category": "Dishwashers"},
                {"prefix": "PDD", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Standard Series", "category": "Dishwashers"},
                {"prefix": "PTD", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Standard Series", "category": "Dryers"},
                {"prefix": "PTW", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Profile Series", "category": "Washing Machines"},
                {"prefix": "PEP", "brand": "GE Profile™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Profile Series", "category": "Cooktops"},
                {"prefix": "PS960", "brand": "GE Profile™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Profile Series", "category": "Ranges"},
                {"prefix": "PB900", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Standard Series", "category": "Ranges"},
                {"prefix": "CHP", "brand": "Café™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Café Series", "category": "Cooktops"},
                {"prefix": "C7CD", "brand": "Café™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Specialty Drip Series", "category": "Coffee Makers"},
                {"prefix": "C7CE", "brand": "Café™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Bellissimo Series", "category": "Espresso Machines"},
                {"prefix": "CES", "brand": "Café™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Café Series", "category": "Ranges"},
                {"prefix": "CVM", "brand": "Café™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Café Series", "category": "Microwaves"},
                {"prefix": "C9TM", "brand": "Café™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Café Series", "category": "Toasters"},
                {"prefix": "C90A", "brand": "Café™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Café Series", "category": "Toaster Ovens"},
                {"prefix": "CVE", "brand": "Café™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Café Series", "category": "Refrigerators"},
                {"prefix": "GDE", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Energy Star Series", "category": "Refrigerators"},
                {"prefix": "FCM", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Chest Freezer Series", "category": "Freezers"},
                {"prefix": "GNE", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "French Door Series", "category": "Refrigerators"},
                {"prefix": "PAD", "brand": "GE Profile™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Door-in-Door Series", "category": "Refrigerators"},
                {"prefix": "PGE", "brand": "GE Profile™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Smart Series", "category": "Refrigerators"},
                {"prefix": "GCST", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Countertop Series", "category": "Microwaves"},
                {"prefix": "PCWK", "brand": "GE Profile™", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Profile Series", "category": "Microwaves"},
                {"prefix": "JXGRILL", "brand": "GE®", "manufacturer": "Haier US Appliance Solutions, Inc.", "series": "Range Accessory", "category": "Range Accessories"},
                {"prefix": "LDPH", "brand": "LG®", "manufacturer": "LG Electronics Inc.", "series": "QuadWash® Series", "category": "Dishwashers"},
                {"prefix": "WKE", "brand": "LG®", "manufacturer": "LG Electronics Inc.", "series": "WashTower™ Series", "category": "Laundry Centers"},
                {"prefix": "MSER", "brand": "LG®", "manufacturer": "LG Electronics Inc.", "series": "NeoChef™ Series", "category": "Microwaves"},
                {"prefix": "LSEL", "brand": "LG®", "manufacturer": "LG Electronics Inc.", "series": "InstaView® Series", "category": "Ranges"},
                {"prefix": "LT18", "brand": "LG®", "manufacturer": "LG Electronics Inc.", "series": "Top Freezer Series", "category": "Refrigerators"},
                {"prefix": "DF7", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "DF7 Series", "category": "Dryers"},
                {"prefix": "DR7", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "DR7 Series", "category": "Dryers"},
                {"prefix": "DV2", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "DV2 Series", "category": "Dryers"},
                {"prefix": "DC5", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "DC5 Series", "category": "Dryers"},
                {"prefix": "FF7", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "FF7 Series", "category": "Washing Machines"},
                {"prefix": "DR5", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "DR5 Series", "category": "Dryers"},
                {"prefix": "TV2", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "TV2 Series", "category": "Washing Machines"},
                {"prefix": "TC5", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "TC5 Series", "category": "Washing Machines"},
                {"prefix": "TR7", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "TR7 Series", "category": "Washing Machines"},
                {"prefix": "TR5", "brand": "Speed Queen®", "manufacturer": "Alliance Laundry Systems LLC", "series": "TR5 Series", "category": "Washing Machines"},
                {"prefix": "WOSP", "brand": "Beko®", "manufacturer": "Beko US Inc.", "series": "Pro Series", "category": "Wall Ovens"},
                {"prefix": "SLER", "brand": "Beko®", "manufacturer": "Beko US Inc.", "series": "Pro Series", "category": "Ranges"},
                {"prefix": "SMC", "brand": "Sharp®", "manufacturer": "Sharp Electronics Corporation", "series": "Carousel® Series", "category": "Microwaves"},
                {"prefix": "SMD", "brand": "Sharp®", "manufacturer": "Sharp Electronics Corporation", "series": "Microwave Drawer®", "category": "Microwave Drawers"},
                {"prefix": "ERFD", "brand": "Element®", "manufacturer": "Element Electronics", "series": "French Door Series", "category": "Refrigerators"},
                {"prefix": "EUF", "brand": "Element®", "manufacturer": "Element Electronics", "series": "Upright Freezer Series", "category": "Freezers"},
                {"prefix": "XOU", "brand": "XO®", "manufacturer": "XO Appliance", "series": "Beverage Center Series", "category": "Beverage Centers"}
            ]
        },
        "Milwaukee Accessory (4031)": {
            "brand": "Milwaukee®",
            "manufacturer": "Milwaukee Electric Tool Corporation",
            "series_keywords": {"M18": "M18™", "M12": "M12™", "PACKOUT": "PACKOUT™", "SHOCKWAVE": "SHOCKWAVE™", "HOLE DOZER": "Hole Dozer™", "SAWZALL": "SAWZALL®", "PERFORM+": "Performance+"}
        },
        "Freud Inc (2435)": {
            "brand": "Diablo®",
            "manufacturer": "Freud America, Inc.",
            "series_keywords": {"STEEL DEMON": "Steel Demon™", "SPEED DEMON": "Speed Demon™", "DEMON": "Demon™"}
        },
        "Jam Industrial Supply LLC (JAMIN)": {
            "brand": "3M®",
            "manufacturer": "3M Company",
            "series_keywords": {"CUBITRON": "Cubitron™ II", "STIKIT": "Stikit™", "775L": "775L"}
        },
        "Mirka Abrasives Inc (MIRUS)": {
            "brand": "Mirka®",
            "manufacturer": "Mirka Abrasives, Inc.",
            "series_keywords": {"ABRANET": "Abranet®", "HIOLIT": "HIOLIT®", "DEOS": "DEOS®", "IRIDIUM": "Iridium®"}
        },
        "Black & Decker/dewlt (2585)": {
            "brand": "DEWALT®",
            "manufacturer": "Stanley Black & Decker, Inc.",
            "series_keywords": {"20V MAX": "20V MAX*", "FLEXVOLT": "FLEXVOLT®", "ATOMIC": "ATOMIC™", "XR": "XR®", "POWERPACK": "POWERPACK™"}
        },
        "Makita Usa Inc (5142)": {
            "brand": "Makita®",
            "manufacturer": "Makita U.S.A., Inc.",
            "series_keywords": {"LXT": "18V LXT®", "XGT": "40V max XGT®", "AVT": "AVT®"}
        },
        "Festool USA (FESTO)": {
            "brand": "Festool®",
            "manufacturer": "Festool USA",
            "series_keywords": {"CLEANTEC": "CLEANTEC®", "SYSTAINER": "Systainer®", "ETSC": "ETSC"}
        },
        "Kreg Tool Company (KRETO)": {
            "brand": "Kreg®",
            "manufacturer": "Kreg Tool Company",
            "series_keywords": {"IONIC": "Ionic™"}
        },
        "Phillips Lighting (5831)": {
            "brand": "Philips®",
            "manufacturer": "Signify North America Corporation",
            "series_keywords": {"WIZ": "WiZ®", "LED": "LED"}
        },
        "Satco Prod Inc (5573)": {
            "brand": "Satco®",
            "manufacturer": "Satco Products, Inc.",
            "series_keywords": {"NUVO": "Nuvo®", "STARFISH": "Starfish™"}
        },
        "Kichler Lighting (KICLI)": {
            "brand": "Kichler®",
            "manufacturer": "Kichler Lighting LLC",
            "series_keywords": {}
        },
        "Leviton Mfg Co (4927)": {
            "brand": "Leviton®",
            "manufacturer": "Leviton Manufacturing Co., Inc.",
            "series_keywords": {"DECORA": "Decora®", "SMART": "Decora Smart®"}
        },
        "Southwire/g Turner (6603)": {
            "brand": "Southwire®",
            "manufacturer": "Southwire Company, LLC",
            "series_keywords": {"ROMAX": "Romex®", "SIMPULL": "SIMpull®"}
        },
        "Boise Cascade Building Materials (BOICA)": {
            "brand": "Trex®",
            "manufacturer": "Trex Company, Inc.",
            "series_keywords": {"LINEAGE": "Transcend® Lineage™", "TRANSCEND": "Transcend®", "ENHANCE NATURALS": "Enhance® Naturals", "ENHANCE BASICS": "Enhance® Basics", "ENHANCE": "Enhance®", "SELECT 2.0": "Select 2.0®", "SELECT": "Select®"}
        },
        "U S Lumber (3073)": {
            "brand": "Trex®",
            "manufacturer": "Trex Company, Inc.",
            "series_keywords": {"LINEAGE": "Transcend® Lineage™", "TRANSCEND": "Transcend®", "SELECT": "Select®"}
        },
        "Parksite (6151)": {
            "brand": "TimberTech®",
            "manufacturer": "The AZEK Company LLC",
            "series_keywords": {"VINTAGE": "Vintage Collection®", "LANDMARK": "Landmark Collection™", "HARVEST": "Harvest Collection®", "AZEK": "AZEK®"}
        },
        "Hunter Fan Co (4381)": {
            "brand": "Hunter®",
            "manufacturer": "Hunter Fan Company",
            "series_keywords": {}
        },
        "Edge Eyewear Inc (EDGSA)": {
            "brand": "Edge®",
            "manufacturer": "Edge Eyewear Inc.",
            "series_keywords": {}
        },
        "Tech Gear 5.7 Inc (TECGE)": {
            "brand": "Mobile Warming®",
            "manufacturer": "Tech Gear 5.7 Inc.",
            "series_keywords": {"UTW PRO": "UTW Pro™", "AERIAL SNOW": "Aerial Snow™"}
        },
        "Certainteed Gypsum (2765)": {
            "brand": "CertainTeed®",
            "manufacturer": "CertainTeed Corporation",
            "series_keywords": {"EASI-LITE": "Easi-Lite®", "FIRELITE": "FireLite®"}
        },
        "Huber Eng Wood LLC (3158)": {
            "brand": "ZIP System®",
            "manufacturer": "Huber Engineered Woods LLC",
            "series_keywords": {"RAINSCREEN": "Rainscreen™", "R-SHEATHING": "R-Sheathing™", "BLUE PLUS": "Advantech Blue Plus®"}
        },
        "James Hardie (JAMESHARDIE)": {
            "brand": "James Hardie®",
            "manufacturer": "James Hardie Building Products Inc.",
            "series_keywords": {"HARDIEPLANK": "HardiePlank®", "HARDIEPANEL": "HardiePanel®"}
        },
        "LP SMARTSIDE": {
            "brand": "LP® SmartSide®",
            "manufacturer": "Louisiana-Pacific Corporation",
            "series_keywords": {"SMART LAP": "SmartSide® Lap Siding", "SMART PAN": "SmartSide® Panel", "SMART VENTED SOFF": "SmartSide® Vented Soffit"}
        },
        "Senco Products Inc (4650)": {
            "brand": "Senco®",
            "manufacturer": "KYOCERA Senco Industrial Tools, Inc.",
            "series_keywords": {}
        },
        "National Nail Corp (7439)": {
            "brand": "National Nail®",
            "manufacturer": "National Nail Corp.",
            "series_keywords": {"PASLODE": "Paslode®"}
        },
        "Marshalltown Trowel (5155)": {
            "brand": "Marshalltown®",
            "manufacturer": "Marshalltown Company",
            "series_keywords": {"WAL-BOARD": "Wal-Board®"}
        },
        "Wera Tools NA Inc (WERTO)": {
            "brand": "Wera®",
            "manufacturer": "Wera Tools Inc.",
            "series_keywords": {"HEX-PLUS": "Hex-Plus®"}
        },
        "Vessel Tools USA Inc (VESTO)": {
            "brand": "Vessel®",
            "manufacturer": "Vessel Tools USA, Inc.",
            "series_keywords": {}
        },
        "Amana Tool Corp (AMATO)": {
            "brand": "Amana Tool®",
            "manufacturer": "Amana Tool Corporation",
            "series_keywords": {}
        },
        "Whiteside Machine & Repair Co (WHIMA)": {
            "brand": "Whiteside®",
            "manufacturer": "Whiteside Machine Company",
            "series_keywords": {}
        },
        "Oliver Machinery Company (OLIMA)": {
            "brand": "Oliver®",
            "manufacturer": "Oliver Machinery Company",
            "series_keywords": {}
        },
        "JPW Industries (JPWIN)": {
            "brand": "JET®",
            "manufacturer": "JPW Industries Inc.",
            "series_keywords": {}
        },
        "Saw Stop LLC (SAWST)": {
            "brand": "SawStop®",
            "manufacturer": "SawStop LLC",
            "series_keywords": {"T-GLIDE": "T-Glide™"}
        },
        "King Canada Inc (KINCA)": {
            "brand": "King Canada®",
            "manufacturer": "King Canada Inc.",
            "series_keywords": {}
        },
        "Woodstock Intl (3658)": {
            "brand": "Grizzly®",
            "manufacturer": "Woodstock International, Inc.",
            "series_keywords": {}
        },
        "Bow Products (BOWPR)": {
            "brand": "BOW Products®",
            "manufacturer": "Bow Products, LLC",
            "series_keywords": {"XTENDER": "XTENDER Fence™"}
        },
        "Woodpeckers Inc (WOODP)": {
            "brand": "Woodpeckers®",
            "manufacturer": "Woodpeckers, Inc.",
            "series_keywords": {"BIGCAL": "BigCal™"}
        },
        "United Window & Door Manufacturing (UNIWI)": {
            "brand": "United Window & Door®",
            "manufacturer": "United Window & Door Mfg.",
            "series_keywords": {"4500": "4500 Series", "3900": "3900 Series"}
        },
        "ProVia (PRODO)": {
            "brand": "ProVia®",
            "manufacturer": "ProVia LLC",
            "series_keywords": {"ECOLITE": "ecoLite™"}
        },
        "Velux America Inc (VELAM)": {
            "brand": "VELUX®",
            "manufacturer": "VELUX America LLC",
            "series_keywords": {}
        },
        "Square D Con Prod Dv (6825)": {
            "brand": "Square D®",
            "manufacturer": "Schneider Electric USA, Inc.",
            "series_keywords": {"HOMELINE": "Homeline™", "QO": "QO™"}
        },
        "First Alert - B R K Brands (2754)": {
            "brand": "First Alert®",
            "manufacturer": "BRK Brands, Inc.",
            "series_keywords": {}
        },
        "Ohio Firewatch Protection Inc (HOLFS)": {
            "brand": "Strike First®",
            "manufacturer": "Ohio Firewatch Protection Inc.",
            "series_keywords": {}
        },
        "Palmer Donavin Mfg Company (PALDO)": {
            "brand": "Owens Corning®",
            "manufacturer": "Owens Corning",
            "series_keywords": {"DURATION": "Duration® TruDefinition®"}
        }
    }
    with open(os.path.join(MASTER_DATA_DIR, "manufacturers.json"), "w", encoding="utf-8") as f:
        json.dump(mfr_brands, f, indent=2)

def create_taxonomies_data():
    taxonomies = {
        "dishwashers": {
            "dept": "Appliances",
            "class": "Large Appliances",
            "fine": "Dishwashers",
            "classpath": "Appliances & Consumer Electronics>Kitchen Appliances>Built-In Dishwashers",
            "product_name": "Dishwasher",
            "default_warranty": "1 Year Manufacturer, 1 Year Labor and Parts",
            "standards": "ASSE 1006|CEE Tier 2 Qualified|cUL Listed|ENERGY STAR Certified|NSF Certified|UL Listed",
            "uom_slots": {
                "Voltage Rating": "V",
                "Amperage Rating": "A",
                "Depth With Door Open": "in",
                "Minimum Height": "in",
                "Maximum Height": "in",
                "Sound Level": "dBA"
            },
            "attribute_order": [
                "Series", "Model", "Number of Wash Cycles", "Voltage Rating", "Amperage Rating",
                "Mounting Type", "Plug Type", "Size", "Depth With Door Open", "Minimum Height",
                "Maximum Height", "Sound Level", "Material", "Color", "Additional Information"
            ]
        },
        "dryers": {
            "dept": "Appliances",
            "class": "Large Appliances",
            "fine": "Dryers",
            "classpath": "Appliances & Consumer Electronics>Laundry Appliances>Dryers",
            "product_name": "Dryer",
            "default_warranty": "3 Year Manufacturer Limited Warranty",
            "attribute_order": ["Series", "Fuel Type", "Capacity", "Voltage Rating", "Color", "Material", "Additional Information"]
        },
        "washers": {
            "dept": "Appliances",
            "class": "Large Appliances",
            "fine": "Washing Machines",
            "classpath": "Appliances & Consumer Electronics>Laundry Appliances>Washing Machines",
            "product_name": "Washing Machine",
            "default_warranty": "3 Year Manufacturer Limited Warranty",
            "attribute_order": ["Series", "Load Type", "Capacity", "Number of Wash Cycles", "Voltage Rating", "Color", "Material", "Additional Information"]
        },
        "ranges": {
            "dept": "Appliances",
            "class": "Large Appliances",
            "fine": "Ranges",
            "classpath": "Appliances & Consumer Electronics>Kitchen Appliances>Ranges",
            "product_name": "Range",
            "default_warranty": "1 Year Limited Warranty",
            "attribute_order": ["Series", "Fuel Type", "Size", "Oven Capacity", "Number of Burners", "Color", "Material", "Additional Information"]
        },
        "refrigerators": {
            "dept": "Appliances",
            "class": "Large Appliances",
            "fine": "Refrigerators",
            "classpath": "Appliances & Consumer Electronics>Kitchen Appliances>Refrigerators",
            "product_name": "Refrigerator",
            "default_warranty": "1 Year Manufacturer Limited Warranty",
            "attribute_order": ["Series", "Total Capacity", "Refrigerator Style", "Size", "Color", "Material", "Energy Star Certified", "Additional Information"]
        },
        "microwaves": {
            "dept": "Appliances",
            "class": "Small Appliances",
            "fine": "Microwaves",
            "classpath": "Appliances & Consumer Electronics>Kitchen Appliances>Microwaves",
            "product_name": "Microwave Oven",
            "default_warranty": "1 Year Limited Warranty",
            "attribute_order": ["Series", "Mounting Type", "Capacity", "Wattage", "Color", "Material", "Additional Information"]
        },
        "coffee_makers": {
            "dept": "Appliances",
            "class": "Small Appliances",
            "fine": "Coffee & Espresso",
            "classpath": "Appliances & Consumer Electronics>Small Appliances>Coffee Makers",
            "product_name": "Coffee Maker",
            "default_warranty": "1 Year Limited Warranty",
            "attribute_order": ["Series", "Type", "Capacity", "Color", "Material", "Additional Information"]
        },
        "saw_blades": {
            "dept": "Tools & Hardware",
            "class": "Power Tool Accessories",
            "fine": "Saw Blades",
            "classpath": "Tools & Hardware>Power Tool Accessories>Saw Blades>Circular Saw Blades",
            "product_name": "Circular Saw Blade",
            "default_warranty": "Limited Lifetime Warranty",
            "attribute_order": ["Diameter", "Number of Teeth", "Arbor Size", "Kerf", "Material Application", "Hook Angle", "Plate Thickness", "Tooth Grind"]
        },
        "abrasives": {
            "dept": "Tools & Hardware",
            "class": "Power Tool Accessories",
            "fine": "Abrasives & Sanding",
            "classpath": "Tools & Hardware>Power Tool Accessories>Abrasives>Sanding Discs & Belts",
            "product_name": "Abrasive Sanding Disc",
            "default_warranty": "Manufacturer Quality Guarantee",
            "attribute_order": ["Diameter", "Grit", "Abrasive Material", "Backing Type", "Attachment Type", "Quantity Per Pack"]
        },
        "power_tools": {
            "dept": "Tools & Hardware",
            "class": "Power Tools",
            "fine": "Cordless Tools",
            "classpath": "Tools & Hardware>Power Tools>Cordless Tools",
            "product_name": "Power Tool",
            "default_warranty": "3 Year Limited Warranty, 1 Year Free Service",
            "attribute_order": ["Voltage Rating", "Motor Type", "Battery System", "Chuck Size", "Maximum Speed", "Tool Weight", "Includes"]
        },
        "decking": {
            "dept": "Building Materials",
            "class": "Lumber & Composites",
            "fine": "Decking",
            "classpath": "Building Materials>Decking & Railing>Composite & PVC Decking",
            "product_name": "Decking Board",
            "default_warranty": "25-50 Year Limited Residential Warranty",
            "attribute_order": ["Collection", "Profile", "Thickness", "Width", "Length", "Color/Finish", "Material Construction", "Grooved/Square Edge"]
        },
        "lighting": {
            "dept": "Lighting & Electrical",
            "class": "Lamps & Bulbs",
            "fine": "LED Bulbs",
            "classpath": "Lighting & Electrical>Lamps & Bulbs>LED Bulbs",
            "product_name": "LED Bulb",
            "default_warranty": "3-5 Year Manufacturer Warranty",
            "attribute_order": ["Bulb Shape", "Base Type", "Wattage Equivalent", "Actual Wattage", "Color Temperature", "Lumens", "Dimmable", "Package Quantity"]
        },
        "electrical": {
            "dept": "Lighting & Electrical",
            "class": "Wiring Devices",
            "fine": "Switches & Outlets",
            "classpath": "Lighting & Electrical>Wiring Devices & Light Controls>Outlets & Switches",
            "product_name": "Wiring Device",
            "default_warranty": "2 Year Limited Warranty",
            "attribute_order": ["Device Type", "Amperage Rating", "Voltage Rating", "NEMA Configuration", "Color", "Material", "Certifications"]
        }
    }
    with open(os.path.join(MASTER_DATA_DIR, "taxonomies.json"), "w", encoding="utf-8") as f:
        json.dump(taxonomies, f, indent=2)

if __name__ == "__main__":
    create_fractions_table()
    create_uom_standards()
    create_manufacturers_data()
    create_taxonomies_data()
    print("Master data generated successfully.")
