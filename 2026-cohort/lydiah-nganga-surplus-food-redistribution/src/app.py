"""
app.py

Flask app for the Surplus Food Redistribution MVP (Team Catalyst Alliance).

Routes:
  GET  /        -> landing page with embedded vendor intake form (donate or sell)
  POST /submit  -> handles both listing types:
                     - "donate": runs the matching engine + sends an NGO notification,
                                 AND posts to the public board as a visible backup
                     - "sell":   posts directly to the public board (no NGO match needed)
  GET  /browse  -> public board showing every active listing, both types, so an NGO
                    or community member can see and call directly, whether or not
                    the automated match went through
"""

import json
import os
import time

from flask import Flask, render_template, request

from matching_engine import find_best_match
from notify import send_notification, send_community_alert

app = Flask(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PUBLIC_BOARD_PATH = os.path.join(DATA_DIR, "public_board.json")
SUBSCRIBERS_PATH = os.path.join(DATA_DIR, "subscribers.json")

with open(os.path.join(DATA_DIR, "locations.json")) as f:
    LOCATIONS = json.load(f)


def load_subscribers():
    if not os.path.exists(SUBSCRIBERS_PATH):
        with open(SUBSCRIBERS_PATH, "w") as f:
            f.write("[]")
    with open(SUBSCRIBERS_PATH) as f:
        return json.load(f)


def save_subscriber(entry):
    subs = load_subscribers()
    subs.append(entry)
    with open(SUBSCRIBERS_PATH, "w") as f:
        json.dump(subs, f, indent=2)


def notify_matching_subscribers(listing):
    """
    For a new 'sell' listing, alert every subscriber in the same country and
    location. This is the automated version of community notification --
    without it, a new sell listing only reaches whoever happens to visit
    /browse on their own.
    """
    subs = load_subscribers()
    matches = [
        s for s in subs
        if s.get("country") == listing.get("country") and s.get("location") == listing.get("location")
    ]
    for sub in matches:
        send_community_alert(sub, listing)
    return len(matches)


def load_board():
    if not os.path.exists(PUBLIC_BOARD_PATH):
        with open(PUBLIC_BOARD_PATH, "w") as f:
            f.write("[]")
    with open(PUBLIC_BOARD_PATH) as f:
        return json.load(f)


def save_to_board(entry):
    board = load_board()
    entry["posted_at"] = time.time()
    board.append(entry)
    with open(PUBLIC_BOARD_PATH, "w") as f:
        json.dump(board, f, indent=2)


def is_still_active(entry):
    """A listing is active until its expiry window has passed since posting."""
    elapsed_hours = (time.time() - entry.get("posted_at", 0)) / 3600
    return elapsed_hours < float(entry.get("expiry_hours", 0))


def compute_impact_stats():
    """
    Real, cumulative stats pulled from every listing ever posted (not just
    active ones) -- this is genuine usage data from the app itself, not a
    placeholder number.
    """
    board = load_board()
    total_listings = len(board)
    total_kg = sum(float(item.get("quantity_kg", 0)) for item in board)
    donated_kg = sum(
        float(item.get("quantity_kg", 0)) for item in board if item.get("listing_type") == "donate"
    )
    sold_kg = sum(
        float(item.get("quantity_kg", 0)) for item in board if item.get("listing_type") == "sell"
    )
    matched_count = sum(1 for item in board if item.get("matched_ngo"))

    return {
        "total_listings": total_listings,
        "total_kg": round(total_kg, 1),
        "donated_kg": round(donated_kg, 1),
        "sold_kg": round(sold_kg, 1),
        "matched_count": matched_count,
    }


@app.route("/")
def index():
    impact = compute_impact_stats()
    return render_template(
        "index.html",
        countries=list(LOCATIONS.keys()),
        locations_json=json.dumps(LOCATIONS),
        impact=impact,
    )


@app.route("/browse")
def browse():
    board = load_board()
    active = [item for item in board if is_still_active(item)]
    active.reverse()  # most recent first
    return render_template(
        "browse.html",
        listings=active,
        countries=list(LOCATIONS.keys()),
        locations_json=json.dumps(LOCATIONS),
    )


@app.route("/submit", methods=["POST"])
def submit():
    listing_type = request.form.get("listing_type", "donate")
    vendor_name = request.form["vendor_name"]
    vendor_contact = request.form["vendor_contact"]
    food_type = request.form["food_type"]
    quantity_kg = float(request.form["quantity_kg"])
    expiry_hours = float(request.form["expiry_hours"])
    country_name = request.form["country"]
    location_name = request.form["location"]
    coords = LOCATIONS[country_name][location_name]

    if listing_type == "sell":
        sale_price = request.form["sale_price"]

        board_entry = {
            "listing_type": "sell",
            "vendor_name": vendor_name,
            "vendor_contact": vendor_contact,
            "food_type": food_type,
            "quantity_kg": quantity_kg,
            "expiry_hours": expiry_hours,
            "country": country_name,
            "location": location_name,
            "sale_price": sale_price,
            "matched_ngo": None,
        }
        save_to_board(board_entry)

        notified_count = notify_matching_subscribers(board_entry)

        share_message = (
            f"{vendor_name} has {quantity_kg}kg of {food_type} for {sale_price}, "
            f"pickup in {location_name}, {country_name}. Good for {int(expiry_hours)}h. "
            f"Contact: {vendor_contact}. Posted on Baki."
        )

        return render_template(
            "result.html",
            listing_type="sell",
            vendor_name=vendor_name,
            food_type=food_type,
            quantity_kg=quantity_kg,
            location=location_name,
            sale_price=sale_price,
            share_message=share_message,
            notified_count=notified_count,
        )

    # --- donate path: run the matching engine, notify the NGO, and ALSO
    #     post to the public board so it's visible even if the automated
    #     match doesn't work out or the NGO can't collect in time ---
    listing = {
        "vendor_name": vendor_name,
        "vendor_location": location_name,
        "food_type": food_type,
        "quantity_kg": quantity_kg,
        "expiry_hours": expiry_hours,
        "lat": coords["lat"],
        "lon": coords["lon"],
        "country": country_name,
    }

    match = find_best_match(listing)

    message = None
    matched_ngo_name = None
    if match:
        message = send_notification(match["ngo"], listing, match)
        matched_ngo_name = match["ngo"]["name"]

    board_entry = {
        "listing_type": "donate",
        "vendor_name": vendor_name,
        "vendor_contact": vendor_contact,
        "food_type": food_type,
        "quantity_kg": quantity_kg,
        "expiry_hours": expiry_hours,
        "country": country_name,
        "location": location_name,
        "sale_price": None,
        "matched_ngo": matched_ngo_name,
    }
    save_to_board(board_entry)

    return render_template("result.html", listing_type="donate", match=match, message=message)


@app.route("/subscribe", methods=["POST"])
def subscribe():
    entry = {
        "name": request.form["sub_name"],
        "contact": request.form["sub_contact"],
        "country": request.form["sub_country"],
        "location": request.form["sub_location"],
    }
    save_subscriber(entry)
    board = load_board()
    active = [item for item in board if is_still_active(item)]
    active.reverse()
    return render_template(
        "browse.html",
        listings=active,
        countries=list(LOCATIONS.keys()),
        locations_json=json.dumps(LOCATIONS),
        subscribed=True,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)