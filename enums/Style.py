from enum import Enum
from flask import current_app

STYLE_IMAGES_PATH = "/style_images/"


class StyleModel(Enum):
    STARRY_NIGHT = (
        "Starry Night",
        "Vincent Van Gogh",
        1889,
        "starry.pth",
        "the_starry_night.jpg",
    )
    GALATHEA = (
        "Galatea of the Spheres",
        "Salvador Dali",
        1952,
        "galatea_1.pth",
        "galatea_of_the_spheres.jpg",
    )
    UDNIE = ("Udnie", "Francis Picabia", 1913, "udnie.pth", "udnie.jpg")

    # to be trained additionally
    DEMOISELLES_DAVIGNON = (
        "Les Demoiselles d'Avignon",
        "Pablo Picasso",
        1907,
        "tbd1.pth",
        "les_demoiselles_davignon.jpg",
    )
    LIBERTY_LEADING_THE_PEOPLE = (
        "Liberty Leading the People",
        "Eugène Delacroix",
        1830,
        "tbd2.pth",
        "liberty_leading_the_people.jpg",
    )
    LOS_ELEFANTES = (
        "Los Elefantes",
        "Salvador Dali",
        1948,
        "tbd3.pth",
        "los_elefantes.jpg",
    )
    THE_GREAT_WAVE_OFF_KANAGAWA = (
        "The Great Wave off Kanagawa",
        "Katsushika Hokusai",
        1833,
        "tbd4.pth",
        "the_great_wave_off_kanagawa.jpg",
    )
    THE_PERSISTENCE_OF_MEMORY = (
        "The Persistence of Memory",
        "Salvador Dali",
        1931,
        "tbd5.pth",
        "the_persistence_of_memory.jpg",
    )
    CRNI_PANTER = ("Crni Panter", "Petar Lubarda", 1968, "tbd6.pth", "crni_panter.jpg")
    KONJI = ("Konji", "Petar Lubarda", 1953, "tbd7.pth", "konji.jpg")
    VESELA_BRACA = ("Vesela Braca", "Uros Predic", 1887, "tbd8.pth", "vesela_braca.jpg")
    PIJANA_LADJA = (
        "Pijana Ladja",
        "Sava Sumanovic",
        1927,
        "tbd9.pth",
        "pijana_ladja.jpg",
    )
    SOKOLARKA = ("Sokolarka", "Dragos Kalajic", 2001, "tbd10.pth", "sokolarka.jfif")
    HIPERBOREJA = (
        "Hiperboreja",
        "Dragos Kalajic",
        2002,
        "tbd11.pth",
        "hiperboreja.jpg",
    )
    IZ_NASE_UNUTRASNJE_IMPERIJE = (
        "Iz Nase Unutrasnje Imperije",
        "Dragos Kalajic",
        2003,
        "tbd12.pth",
        "iz_nase_unutrasnje_imperije.jpg",
    )
    EVROPA = ("Evropa", "Dragos Kalajic", 2000, "tbd13.pth", "dragos.jpg")
    WOLFGANG = ("Wolfgang", "Dragos Kalajic", 1993, "tbd14.pth", "wolfgang.jpg")

    def __init__(self, title, author, year, model_id, url):
        self.title = title
        self.author = author
        self.year = year
        self.model_id = model_id
        self.url = url

    def read_collection(request):
        return [
            {
                "title": style_model.value[0],
                "author": style_model.value[1],
                "year": style_model.value[2],
                "model_id": style_model.value[3],
                "url": request.host_url.rstrip("/")
                + current_app.static_url_path
                + STYLE_IMAGES_PATH
                + style_model.value[4],
            }
            for style_model in StyleModel
        ]
