from pathlib import Path

import pandas as pd
from flask import Flask, render_template, request, send_file

from Backend.loader.data_manager import DataManager
from Backend.parser import tokenize_route, clean_tokens
from Backend.route_expander import expand_route
from Backend.rad_search import find_routes
from Backend.validators.waypoint_validator import validate_route


app = Flask(__name__)

# =====================================
# Data Folder
# =====================================

DATA_FOLDER = Path("Data")
DATA_FOLDER.mkdir(exist_ok=True)

# =====================================
# Load Backend
# =====================================

data_manager = DataManager()


# =====================================
# Route Processing
# =====================================

def process_route(route):

    tokens = tokenize_route(route)
    tokens = clean_tokens(tokens)

    return expand_route(
        tokens,
        data_manager.airway_dictionary,
        data_manager.airport_dictionary
    )


# =====================================
# Home
# =====================================

@app.route("/")
def home():
    return render_template("home.html")


# =====================================
# Search RAD
# =====================================

@app.route("/search", methods=["GET", "POST"])
def search():

    if (
        not data_manager.airway_dictionary
        or data_manager.rad_routes.empty
    ):
        return render_template(
            "search.html",
            error="Please upload the Dictionary Workbook and RAD file from the System Files page first."
        )

    departure_fir = ""
    arrival_fir = ""
    entry_point = ""
    exit_point = ""
    routes = []
    expanded = ""

    if request.method == "POST":

        departure_fir = request.form.get(
            "departure_fir", ""
        ).strip().upper()

        arrival_fir = request.form.get(
            "arrival_fir", ""
        ).strip().upper()

        entry_point = request.form.get(
            "entry_point", ""
        ).strip().upper()

        exit_point = request.form.get(
            "exit_point", ""
        ).strip().upper()

        routes = find_routes(
            data_manager.rad_routes,
            departure_fir or None,
            arrival_fir or None,
            entry_point or None,
            exit_point or None
        )

        action = request.form.get("action")

        if action == "expand" and routes:

            selected = int(request.form.get("selected_route", 0))

            route = routes[selected]["Routes"]

            processed_route = process_route(route)

            if processed_route:
                expanded = " ".join(processed_route)
            else:
                expanded = "Route could not be expanded."

    return render_template(
        "search.html",
        departure_fir=departure_fir,
        arrival_fir=arrival_fir,
        entry_point=entry_point,
        exit_point=exit_point,
        routes=routes,
        expanded=expanded
    )


# =====================================
# Expand Route
# =====================================

@app.route("/expand", methods=["GET", "POST"])
def expand():

    if not data_manager.airway_dictionary:
        return render_template(
            "expand.html",
            error="Please upload the Dictionary Workbook first."
        )

    expanded = ""
    route = ""

    if request.method == "POST":

        route = request.form["route"]

        processed_route = process_route(route)

        if processed_route:
            expanded = " ".join(processed_route)
        else:
            expanded = "Route could not be expanded."

    return render_template(
        "expand.html",
        route=route,
        expanded=expanded
    )


# =====================================
# Expand Excel
# =====================================

@app.route("/expand_excel", methods=["GET", "POST"])
def expand_excel():

    if (
        not data_manager.airway_dictionary
        or not data_manager.validation_set
    ):
        return render_template(
            "expand_excel.html",
            error="Please upload the Dictionary Workbook from the System Files page first."
        )

    if request.method == "POST":

        excel_file = request.files.get("excel_file")

        if not excel_file or excel_file.filename == "":
            return render_template(
                "expand_excel.html",
                error="Please select an Excel file."
            )

        df = pd.read_excel(excel_file, header=1)

        valid_points = data_manager.validation_set

        expanded_routes = []
        validation_status = []
        invalid_points = []

        for _, row in df.iterrows():

            route = str(row["Routes"])

            processed_route = process_route(route)

            if processed_route:

                formatted_route = [
                    str(point).strip().upper()
                    for point in processed_route
                    if point and str(point).strip()
                ]

                expanded_routes.append(
                    " ".join(formatted_route)
                )

                invalid = validate_route(
                    formatted_route,
                    valid_points
                )

                if invalid:
                    validation_status.append("Invalid")
                else:
                    validation_status.append("Valid")

                invalid_points.append(invalid)

            else:

                expanded_routes.append("")
                validation_status.append("")
                invalid_points.append("")

        df["Expanded Route"] = expanded_routes
        df["Validation Status"] = validation_status
        df["Invalid Points"] = invalid_points

        output_file = (
            DATA_FOLDER /
            f"{Path(excel_file.filename).stem}_Expanded.xlsx"
        )

        df.to_excel(output_file, index=False)

        return send_file(
            output_file,
            as_attachment=True
        )

    return render_template("expand_excel.html")


# =====================================
# System Files
# =====================================

@app.route("/system_files", methods=["GET", "POST"])
def system_files():

    message = None
    error = None

    if request.method == "POST":

        dictionary_file = request.files.get("dictionary_file")
        rad_file = request.files.get("rad_file")

        if not dictionary_file or dictionary_file.filename == "":
            error = "Please select a Dictionary Workbook."

        elif not rad_file or rad_file.filename == "":
            error = "Please select a RAD Excel file."

        else:

            dictionary_file.save(
                DATA_FOLDER / "Dictionary.xlsx"
            )

            rad_file.save(
                DATA_FOLDER / "RAD.xlsx"
            )

            data_manager.reload_all()

            message = "System files updated successfully."

    return render_template(
        "system_files.html",
        message=message,
        error=error
    )


# =====================================
# Run
# =====================================

if __name__ == "__main__":
    app.run(debug=True)