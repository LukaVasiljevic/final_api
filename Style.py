from enum import Enum, auto


class StyleModel(Enum):
    STARRY_NIGHT = ("Starry Night", "Vincent Van Gogh", 1889, "starry.pth", "")
    GALATHEA = ("Galatea of the Spheres", "Salvador Dali", 1952, "galathea_1.pth", "")
    UDNIE = ("Udnie", "Francis Picabia", 1913, "udnie.pth", "")

    # to be trained additionally
    DEMOISELLES_DAVIGNON = ("Les Demoiselles d'Avignon", "Pablo Picasso", 1907, "", "")
    LIBERTY_LEADING_THE_PEOPLE = (
        "Liberty Leading the People",
        "Eugène Delacroix",
        1830,
        "",
        "",
    )
    LOS_ELEFANTES = ("Los Elefantes", "Salvador Dali", 1948, "", "")
    THE_GREAT_WAVE_OFF_KANAGAWA = (
        "The Great Wave off Kanagawa",
        "Katsushika Hokusai",
        1833,
        "",
        "",
    )
    THE_PERSISTENCE_OF_MEMORY = (
        "The Persistence of Memory",
        "Salvador Dali",
        1931,
        "",
        "",
    )
    CRNI_PANTER = ("Crni Panter", "Petar Lubarda", 1968, "", "")
    KONJI = ("Konji", "Petar Lubarda", 1953, "", "")
    VESELA_BRACA = ("Vesela Braca", "Uros Predic", 1887, "", "")
    PIJANA_LADJA = ("Pijana Ladja", "Sava Sumanovic", 1927, "", "")
    SOKOLARKA = ("Sokolarka", "Dragos Kalajic", 2001, "", "")
    HIPERBOREJA = ("Hiperboreja", "Dragos Kalajic", 2002, "", "")
    IZ_NASE_UNUTRASNJE_IMPERIJE = (
        "Iz Nase Unutrasnje Imperije",
        "Dragos Kalajic",
        2003,
        "",
        "",
    )
    EVROPA = ("Evropa", "Dragos Kalajic", 2000, "", "")
    WOLFGANG = ("Wolfgang", "Dragos Kalajic", 1993, "", "")

    def __init__(self, title, author, year, model_id, description):
        self.title = title
        self.author = author
        self.year = year
        self.model_id = model_id
        self.description = description

    def read_collection():
        return [
            {
                "title": style_model.value[0],
                "author": style_model.value[1],
                "year": style_model.value[2],
                "model_id": style_model.value[3],
                "description": style_model.value[4],
            }
            for style_model in StyleModel
        ]
