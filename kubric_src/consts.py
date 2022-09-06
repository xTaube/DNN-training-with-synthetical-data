from type import enum


CATEGORY = enum(
    "train",
    "airplane",
    "bench",
    "skateboard",
    "bottle",
    "mug",
    "knife",
    "bowl",
    "bag",
    "chair",
    "bed",
    "sofa",
    "computer_keyboard",
    "cellular_telephone",
    "remote_control",
    "laptop",
    "microwave",
    "motorcycle",
    "bus",
    "car",
)

VEHICLES = [CATEGORY.motorcycle, CATEGORY.bus, CATEGORY.car]

HOUSEHOLD_ITEMS = [
    CATEGORY.skateboard,
    CATEGORY.bottle,
    CATEGORY.mug,
    CATEGORY.knife,
    CATEGORY.bowl,
    CATEGORY.bag,
    CATEGORY.chair,
    CATEGORY.computer_keyboard,
    CATEGORY.cellular_telephone,
    CATEGORY.remote_control,
    CATEGORY.laptop,
    CATEGORY.microwave,
]

BACKGROUNDS_TYPE = enum("forest", "city", "outdoor", "indoor", "all")

FOREST_BACKGROUNDS = [
    "abandoned_waterworks",
    "ahornsteig",
    "arboretum",
    "autumn_crossing",
    "autumn_forest_01",
    "autumn_forest_02",
    "autumn_forest_03",
    "autumn_ground",
    "autumn_hockey",
    "autumn_meadow",
    "autumn_park",
    "autumn_road",
    "bergen",
    "birchwood",
    "blau_river",
    "blaubeuren_hillside",
    "blaubeuren_outskirts",
    "blue_grotto",
    "borghese_gardens",
    "brick_factory_01",
    "cloudy_vondelpark",
    "crosswalk",
    "crystal_falls",
    "eilenriede_labyrinth",
    "eilenriede_park",
    "emmarentia",
    "epping_forest_01",
    "epping_forest_02",
    "felsenlabyrinth",
    "flower_hillside",
    "forest_cave",
    "forest_slope",
    "green_sanctuary",
    "greenwich_park_02",
    "greenwich_park_03",
    "herkulessaulen",
    "je_gray_02",
    "lauter_waterfall",
    "lilienstein",
    "lush_dirt_path",
    "lythwood_terrace",
    "missile_launch_facility_02",
    "missile_launch_facility_03",
    "misty_pines",
    "monbachtal_riverbank",
    "monks_forest",
    "mossy_forest",
    "moulton_falls_train_tunnel_east",
    "moulton_station_train_tunnel_west",
    "muddy_autumn_forest",
    "nagoya_wall_path",
    "ninomaru_teien",
    "nkuhlu",
    "phalzer_forest_01",
    "pond",
    "river_rocks",
    "river_walk_1",
    "river_walk_2",
    "shady_patch",
    "small_rural_road_02",
    "snowy_forest_path_01",
    "snowy_forest_path_02",
    "snowy_hillside",
    "sunny_vondelpark",
    "sunset_forest",
    "teufelsberg_ground_2",
    "whipple_creek_regional_park_01",
    "whipple_creek_regional_park_04",
    "woods",
    "xanderklinge",
]

CITY_BACKGROUNDS = [
    "beach_parking",
    "belvedere",
    "bethnal_green_entrance",
    "binnenalster",
    "blaubeuren_church_square",
    "cambridge",
    "canary_wharf",
    "cedar_bridge",
    "dresden_moat",
    "dresden_square",
    "dusseldorf_bridge",
    "furry_clouds",
    "future_parking",
    "green_point_park",
    "hamburg_canal",
    "hansaplatz",
    "konigsallee",
    "konzerthaus",
    "leadenhall_market",
    "learner_park",
    "limehouse",
    "museum_of_history",
    "neuer_zollhof",
    "night_bridge",
    "old_tree_in_city_park",
    "outdoor_umbrellas",
    "palermo_park",
    "palermo_sidewalk",
    "palermo_square",
    "park_parking",
    "paul_lobe_haus",
    "pedestrian_overpass",
    "piazza_bologni",
    "piazza_martin_lutero",
    "piazza_san_marco",
    "pump_station",
    "quattro_canti",
    "rathaus",
    "red_wall",
    "residential_garden",
    "rhodes_memorial",
    "roofless_ruins",
    "round_platform",
    "rural_graffiti_tower",
    "san_giuseppe_bridge",
    "satara_night",
    "satara_night_no_lamps",
    "shanghai_bund",
    "shanghai_riverside",
    "simons_town_harbour",
    "snowy_cemetery",
    "snowy_field",
    "solitude_night",
    "spiaggia_di_mondello",
    "stadium_01",
    "sterkspruit_falls",
    "stone_alley",
    "stone_alley_02",
    "stone_alley_03",
    "street_lamp",
    "stuttgart_suburbs",
    "suburban_field_01",
    "suburban_field_02",
    "suburban_parking_area",
    "sunset_jhbcentral",
    "tears_of_steel_bridge",
    "teatro_massimo",
    "teufelsberg_ground_1",
    "the_sky_is_on_fire",
    "tiber_2",
    "tiber_island",
    "ulmer_muenster",
    "umhlanga_sunrise",
    "urban_alley_01",
    "urban_courtyard",
    "urban_courtyard_02",
    "urban_street_01",
    "urban_street_02",
    "urban_street_03",
    "urban_street_04",
    "vatican_road",
    "venetian_crossroads",
    "venice_dawn_1",
    "venice_dawn_2",
    "venice_sunrise",
    "viale_giuseppe_garibaldi",
    "vignaioli",
    "vignaioli_night",
    "wide_street_01",
    "wide_street_02",
    "wooden_motel",
    "xiequ_yuan",
    "zavelstein",
    "zhengyang_gate",
    "zwinger_night",
]

OUTDOOR_BACKGROUNDS = [
    "abandoned_parking",
    "abandoned_church",
    "abandoned_hopper_terminal_01",
    "abandoned_hopper_terminal_02",
    "abandoned_hopper_terminal_03",
    "abandoned_hopper_terminal_04",
    "abandoned_parking",
    "abandoned_pathway",
    "abandoned_slipway",
    "abandoned_tank_farm_01",
    "abandoned_tank_farm_02",
    "abandoned_tank_farm_03",
    "abandoned_tank_farm_04",
    "abandoned_tank_farm_05",
    "air_museum_playground",
    "altanka",
    "approaching_storm",
    "aristea_wreck",
    "balcony",
    "bell_park_dawn",
    "bell_park_pier",
    "between_bridges",
    "bismarckturm",
    "bismarckturm_hillside",
    "blaubeuren_night",
    "blouberg_sunrise_1",
    "blouberg_sunrise_2",
    "blue_lagoon",
    "blue_lagoon_night",
    "brick_factory_02",
    "cannon",
    "cape_hill",
    "castel_st_angelo_roof",
    "cayley_lookout",
    "champagne_castle_1",
    "chinese_garden",
    "circus_maximus_1",
    "circus_maximus_2",
    "cloud_layers",
    "cloudy_cliffside_road",
    "cliffside",
    "colosseum",
    "construction_yard",
    "courtyard",
    "courtyard_night",
    "dam_road",
    "delta_2",
    "derelict_highway_noon",
    "derelict_overpass",
    "derelict_underpass",
    "dikhololo_night",
    "dikhololo_sunset",
    "dirt_bike_track_01",
    "dreifaltigkeitsberg",
    "driving_school",
    "dry_field",
    "dry_hay_field",
    "evening_meadow",
    "evening_road_01",
    "factory_yard",
    "fish_eagle_hill",
    "fish_hoek_beach",
    "flower_road",
    "freight_station",
    "gamrig",
    "goegap",
    "gothic_manor_01",
    "gray_pier",
    "greenwich_park",
    "harties",
    "hilltop_construction",
    "hilly_terrain_01",
    "immenstadter_horn",
    "industrial_sunset",
    "je_gray_park",
    "kiara_1_dawn",
    "kiara_2_sunrise",
    "kiara_3_morning",
    "kiara_4_mid-morning",
    "kiara_5_noon",
    "kiara_6_afternoon",
    "kiara_7_late-afternoon",
    "kiara_8_sunset",
    "kiara_9_dusk",
    "killesberg_park",
    "kloetzle_blei",
    "kloofendal_38d_partly_cloudy",
    "kloofendal_48d_partly_cloudy",
    "kloppenheim_01",
    "kloppenheim_02",
    "kloppenheim_03",
    "kloppenheim_04",
    "kloppenheim_05",
    "kloppenheim_06",
    "kloppenheim_07",
    "lakes",
    "lakeside",
    "lenong_1",
    "lenong_2",
    "lenong_3",
    "lot_01",
    "lot_02",
    "lythwood_field",
    "mall_parking_lot",
    "mealie_road",
    "misty_dawn",
    "monte_scherbelino",
    "moonless_golf",
    "moonlit_golf",
    "mpumalanga_veld",
    "mud_road",
    "museumplein",
    "neurathen_rock_castle",
    "noga",
    "noon_grass",
    "northcliff",
    "oberer_kuhberg",
    "old_outdoor_theater",
    "orbita",
    "ostrich_road",
    "parched_canal",
    "park_bench",
    "partial_eclipse",
    "pink_sunrise",
    "pond_bridge_night",
    "portland_landing_pad",
    "potsdamer_platz",
    "preller_drive",
    "quarry_01",
    "quarry_02",
    "quarry_03",
    "qwantani",
    "railway_bridge_02",
    "railway_bridges",
    "red_hill_curve",
    "red_hill_straight",
    "reichstag_1",
    "reinforced_concrete_02",
    "rocky_ridge",
    "rooftop_night",
    "rooitou_park",
    "ruckenkreuz",
    "rural_landscape",
    "rural_winter_roadside",
    "rustig_koppie",
    "sabie_tent",
    "secluded_beach",
    "shudu_lake",
    "signal_hill_dawn",
    "signal_hill_sunrise",
    "small_harbor_01",
    "small_harbor_02",
    "small_rural_road",
    "snowy_hillside_02",
    "spaichingen_hill",
    "spruit_dawn",
    "spruit_sunrise",
    "stone_pines",
    "straw_rolls_field_01",
    "stream",
    "studio_garden",
    "summer_stage_02",
    "sunflowers",
    "sunset_fairway",
    "sunset_in_the_chalk_quarry",
    "syferfontein_0d_clear",
    "syferfontein_1d_clear",
    "syferfontein_6d_clear",
    "syferfontein_18d_clear",
    "symmetrical_garden",
    "table_mountain_1",
    "table_mountain_2",
    "teufelsberg_roof",
    "the_lost_city",
    "tiergarten",
    "tucker_wreck",
    "turning_area",
    "under_bridge",
    "veld_fire",
    "venice_sunset",
    "versveldpas",
    "wasteland_clouds",
    "waterbuck_trail",
    "whipple_creek_gazebo",
    "white_cliff_top",
    "winter_lake_01",
    "winter_river",
    "winter_sky",
    "wobbly_bridge",
    "yellow_field",
]

INDOOR_BACKGROUNDS = [
    "abandoned_factory_canteen_01",
    "abandoned_factory_canteen_02",
    "abandoned_games_room_01",
    "abandoned_games_room_02",
    "abandoned_greenhouse",
    "abandoned_hall_01",
    "abandoned_workshop",
    "abandoned_workshop_02",
    "adams_place_bridge",
    "aerodynamics_workshop",
    "aft_lounge",
    "aircraft_workshop_01",
    "anniversary_lounge",
    "art_studio",
    "artist_workshop",
    "auto_service",
    "autoshop_01",
    "ballroom",
    "bathroom",
    "birbeck_street_underpass",
    "blender_institute",
    "blinds",
    "boiler_room",
    "bush_restaurant",
    "cabin",
    "carpentry_shop_01",
    "carpentry_shop_02",
    "castle_zavelstein_cellar",
    "cave_wall",
    "cayley_interior",
    "chapmans_drive",
    "childrens_hospital",
    "christmas_photo_studio_01",
    "christmas_photo_studio_02",
    "christmas_photo_studio_04",
    "christmas_photo_studio_05",
    "cinema_hall",
    "cinema_lobby",
    "circus_arena",
    "colorful_studio",
    "combination_room",
    "comfy_cafe",
    "concrete_tunnel",
    "concrete_tunnel_02",
    "country_club",
    "de_balie",
    "decor_shop",
    "drachenfels_cellar",
    "dresden_station_night",
    "empty_warehouse_01",
    "en_suite",
    "entrance_hall",
    "fireplace",
    "floral_tent",
    "garage",
    "georgentor",
    "glass_passage",
    "graffiti_shelter",
    "gym_01",
    "gym_entrance",
    "hall_of_finfish",
    "hall_of_mammals",
    "hamburg_hbf",
    "hikers_cave",
    "hospital_room",
    "hotel_room",
    "indoor_pool",
    "industrial_pipe_and_valve_01",
    "industrial_pipe_and_valve_02",
    "interior_construction",
    "kiara_interior",
    "lapa",
    "large_corridor",
    "lebombo",
    "lookout",
    "lythwood_lounge",
    "lythwood_room",
    "machine_shop_01",
    "machine_shop_02",
    "machine_shop_03",
    "missile_launch_facility_01",
    "modern_buildings",
    "modern_buildings_night",
    "mosaic_tunnel",
    "museum_of_ethnography",
    "music_hall_01",
    "music_hall_02",
    "mutianyu",
    "old_apartments_walkway",
    "old_bus_depot",
    "old_depot",
    "old_hall",
    "old_room",
    "parking_garage",
    "peppermint_powerplant",
    "phone_shop",
    "photo_studio_01",
    "photo_studio_broadway_hall",
    "photo_studio_loft_hall",
    "photo_studio_london_hall",
    "pillars",
    "pool",
    "pump_house",
    "pylons",
    "reading_room",
    "reinforced_concrete_01",
    "roof_garden",
    "rooftop_day",
    "royal_esplanade",
    "schadowplatz",
    "sculpture_exhibition",
    "sepulchral_chapel_basement",
    "sepulchral_chapel_rotunda",
    "short_tunnel",
    "small_hangar_02",
    "st_fagans_interior",
    "storeroom",
    "studio_country_hall",
    "studio_small_01",
    "studio_small_02",
    "studio_small_03",
    "studio_small_04",
    "studio_small_05",
    "studio_small_06",
    "studio_small_07",
    "studio_small_08",
    "studio_small_09",
    "subway_entrance",
    "summer_stage_01",
    "surgery",
    "teufelsberg_inner",
    "teufelsberg_lookout",
    "theater_01",
    "theater_02",
    "tiber_1",
    "tv_studio",
    "veranda",
    "vintage_measuring_lab",
    "vulture_hide",
    "whale_skeleton",
    "winter_evening",
    "wooden_lounge",
]

BACKGROUNDS = [*INDOOR_BACKGROUNDS, *OUTDOOR_BACKGROUNDS]

BACKGROUND_MAPPING = {
    BACKGROUNDS_TYPE.forest: FOREST_BACKGROUNDS,
    BACKGROUNDS_TYPE.city: CITY_BACKGROUNDS,
    BACKGROUNDS_TYPE.outdoor: OUTDOOR_BACKGROUNDS,
    BACKGROUNDS_TYPE.indoor: INDOOR_BACKGROUNDS,
    BACKGROUNDS_TYPE.all: BACKGROUNDS,
}

KUBASIC_URI = "gs://kubric-public/assets/KuBasic/KuBasic.json"
GSO_URI = "gs://kubric-public/assets/GSO.json"
HDRI_HAVEN_URI = "gs://kubric-public/assets/HDRI_haven.json"
SHAPENET_URI = "gs://kubric-unlisted/assets/ShapeNetCore.v2.json"

IMAGE_SHAPE = (600, 600)
DEFAULT_CAMERA_LOOK_AT_NOISE = [0, 0]

DEFAULT_SCALE = [1, 1]
DEFAULT_SPAWN_REGION = [[0, 0, 0], [0, 0, 0]]
DEFAULT_ROTATION = [{"axis": [1, 0, 0], "degrees": [0, 0]}]
DEFAULT_ADDITIONAL_OBJECTS_NUM = 0
DEFAULT_MIN_VISIBILITY = 0
