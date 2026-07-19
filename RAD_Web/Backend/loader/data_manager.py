from Backend.loader.excel_reader import load_dictionary, load_rad_routes
from Backend.builders.airway_builder import build_airway_dictionary
from Backend.builders.airport_builder import build_airport_dictionary
from Backend.builders.validation_builder import build_validation_dictionary

import pandas as pd


class DataManager:

    def __init__(self):

        self.airway_dictionary = {}
        self.airport_dictionary = {}
        self.validation_dictionary = {}
        self.rad_routes = pd.DataFrame()

        self.load_all()

    # -------------------------
    # Load Everything
    # -------------------------

    def load_all(self):
        self.load_dictionary()
        self.load_rad()

    # -------------------------
    # Dictionary Workbook
    # -------------------------

    def load_dictionary(self):

        workbook = load_dictionary()

        if workbook is None:
            self.airway_dictionary = {}
            self.airport_dictionary = {}
            self.validation_set = set()
            return


        self.airway_dictionary = build_airway_dictionary(
            workbook["Airways"]
        )

        self.airport_dictionary = build_airport_dictionary(
            workbook["Airports"]
        )

        self.validation_set = build_validation_dictionary(
            workbook["Validation"]
        )

    # -------------------------
    # RAD
    # -------------------------

    def load_rad(self):

        routes = load_rad_routes()

        if routes is None:
            self.rad_routes = pd.DataFrame()
        else:
            self.rad_routes = routes

    # -------------------------
    # Reload
    # -------------------------

    def reload_dictionary(self):
        self.load_dictionary()

    def reload_rad(self):
        self.load_rad()

    def reload_all(self):
        self.load_all()