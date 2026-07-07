from flask import Flask, render_template, request, send_file
import pandas as pd
import os
from Backend.excel_reader import load_airway_dictionary, load_rad_routes
from Backend.airway_lookup import build_airway_dictionary
from Backend.parser import tokenize_route, clean_tokens
from Backend.route_expander import expand_route
from Backend.rad_search import find_routes
from Backend.validator import build_validation_set, validate_route

app = Flask(__name__)

# =====================================
# Load Backend
# =====================================

airway_df = load_airway_dictionary()
default_routes_df = load_rad_routes()
airway_dictionary = build_airway_dictionary(airway_df)


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

    departure_fir = ""
    arrival_fir = ""
    entry_point = ""
    exit_point = ""

    routes = []
    expanded = ""

    if request.method == "POST":

        departure_fir = request.form.get("departure_fir", "").strip().upper()
        arrival_fir = request.form.get("arrival_fir", "").strip().upper()
        entry_point = request.form.get("entry_point", "").strip().upper()
        exit_point = request.form.get("exit_point", "").strip().upper()

        departure = departure_fir or None
        arrival = arrival_fir or None
        entry = entry_point or None
        exit = exit_point or None

        routes = find_routes(
            default_routes_df,
            departure,
            arrival,
            entry,
            exit
        )

        action = request.form.get("action")

        if action == "expand" and routes:

            selected = int(
                request.form.get("selected_route", 0)
            )

            route = routes[selected]["Routes"]

            tokens = tokenize_route(route)
            tokens = clean_tokens(tokens)

            expanded_route = expand_route(
                tokens,
                airway_dictionary
            )

            if expanded_route:
                expanded = " ".join(expanded_route)
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

    expanded = ""
    route = ""

    if request.method == "POST":

        route = request.form["route"]

        tokens = tokenize_route(route)
        tokens = clean_tokens(tokens)

        expanded_route = expand_route(
            tokens,
            airway_dictionary
        )

        if expanded_route:
            expanded = " ".join(expanded_route)
        else:
            expanded = "Route could not be expanded."

    return render_template(
        "expand.html",
        route=route,
        expanded=expanded
    )

# =====================================
# Expand Excel Sheet
# =====================================

@app.route("/expand_excel", methods=["GET", "POST"])
def expand_excel():

    if request.method == "POST":

        uploaded_file = request.files.get("excel_file")
        validation_file = request.files.get("validation_file")

        if not uploaded_file or uploaded_file.filename == "":
            return render_template("expand_excel.html")

        # Read uploaded RAD Excel
        df = pd.read_excel(
            uploaded_file,
            header=1
        )
        print(df.columns.tolist())

        # Read validation file (optional)
        valid_points = None

        if validation_file and validation_file.filename != "":

            # Validation file has NO header
            validation_df = pd.read_excel(
                validation_file,
                header=None
            )

            valid_points = build_validation_set(validation_df)

        expanded_routes = []
        validation_status = []
        invalid_points = []

        # Expand every route
        for _, row in df.iterrows():

            route = str(row["Routes"])

            tokens = tokenize_route(route)
            tokens = clean_tokens(tokens)

            expanded = expand_route(
                tokens,
                airway_dictionary
            )

            if expanded:

                expanded = [
                    str(point).strip().upper()
                    for point in expanded
                    if point and str(point).strip()
                ]

                expanded_routes.append(
                    " ".join(expanded)
                )

                # Default values
                status = ""
                invalid = ""

                # Validate expanded route
                if valid_points is not None:

                    invalid = validate_route(
                        expanded,
                        valid_points
                    )

                    if invalid:
                        status = "Invalid"
                    else:
                        status = "Valid"

                validation_status.append(status)
                invalid_points.append(invalid)

            else:

                expanded_routes.append("")
                validation_status.append("")
                invalid_points.append("")

        # Add columns
        df["Expanded Route"] = expanded_routes
        df["Validation Status"] = validation_status
        df["Invalid Points"] = invalid_points

        # Save output
        filename = uploaded_file.filename.replace(".xlsx", "")
        output_file = f"{filename}_Expanded.xlsx"

        df.to_excel(
            output_file,
            index=False
        )

        return send_file(
            output_file,
            as_attachment=True
        )

    return render_template("expand_excel.html")
    
# =====================================
# Run Application
# =====================================

if __name__ == "__main__":
    app.run(debug=True)
