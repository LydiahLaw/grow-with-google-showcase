# Surplus Food Redistribution Network

**Team Catalyst Alliance** — Grow with Google x Mentor Me Collective, BUILD Project, 2026 Cohort

## What This Project Does

Vendors (supermarkets, restaurants, market stalls, bakeries) generate surplus food nearing expiry that often goes to waste, while nearby NGOs and community organizations could redistribute it to people in need. The gap isn't food scarcity — it's a coordination gap: no fast, low-friction way for a vendor with surplus today to know which NGO can collect it before it spoils.

This project is a lightweight web platform that lets a vendor log a surplus food listing, automatically matches it to the nearest suitable NGO/collection point based on proximity, urgency (expiry window), and NGO capacity, and sends an automated notification to the matched NGO — closing the loop between "food about to be wasted" and "organization that can use it," in minutes instead of hours.

## Problem Grounding

Food waste is a documented, substantial problem across all three countries represented on our team. According to the UNEP Food Waste Index Report 2024, Kenya has seven household food waste datapoints ranging from 40 to 100 kg per capita per year, with a 2010 JICA study specifically measuring Nairobi at 100 kg per capita per year — the high end of the national range (UNEP, 2024). Nigeria shows the highest household food waste in Sub-Saharan Africa, estimated at 113 kg per capita per year and roughly 24.79 million tonnes nationally, with some methodologies putting the figure as high as 189 kg per capita per year (UNEP, 2024; Pulse Nigeria, 2024). South Africa's national estimate sits at 27 kg per capita per year, though the report notes this masks wide variation, with city-level studies ranging from 8 to 134 kg per capita per year (UNEP, 2024).

Globally, the same report found that of all food wasted in 2022, 60% occurred at the household level, 28% at food service (restaurants, hotels, catering), and 12% at retail (UNEP, 2024). This is directly relevant to our project's focus: while household waste is comparatively well-measured across Kenya, Nigeria, and South Africa, **food service and retail waste — the exact vendor categories our platform targets — remain largely unmeasured at the national level in all three countries.** The report itself identifies this as a global data gap, particularly acute in low- and middle-income countries (UNEP, 2024).

This gap is part of our project's rationale, not just a limitation of the data we could find: if restaurants, small hotels, and groceries in our countries are wasting food at anywhere close to the rate suggested by the food-service/retail share of global waste, there is currently no visibility into it, let alone a system for redirecting it to people who need it. Our MVP targets that specific, under-addressed slice of the problem.

**Sources:**
- United Nations Environment Programme (2024). *Food Waste Index Report 2024: Think Eat Save — Tracking Progress to Halve Global Food Waste.* Nairobi. https://www.unep.org/resources/publication/food-waste-index-report-2024
- "10 African countries that waste the most food in 2024," Pulse Nigeria, 2024. https://www.pulse.ng/story/10-african-countries-that-waste-the-most-food-in-2024-2024072702140403976
- "New report shows mounting food waste as many go to bed hungry," The Star (Kenya), 2024. https://www.the-star.co.ke/counties/nairobi/2024-03-29-new-report-shows-mounting-food-waste-as-many-go-to-bed-hungry/

## UN SDG Alignment

**SDG 2: Zero Hunger** — reducing food waste and improving food access through automated redistribution coordination.

## Grow with Google Resources Used

- *(fill in per teammate — e.g. IT Automation with Python, Data Analytics, Cybersecurity, Digital Marketing, Project Management certificates/coursework used)*

## Team

| Name | Role |
|---|---|
| Oke Oluwatoyin | Project Management |
| Zoliswa Mokopu | Cybersecurity |
| Omoruyi Igbinovia | Data Analytics |
| Lydiah Nganga | IT Automation with Python |
| Esther Vincent | Digital Marketing |

## How It Works

1. A vendor submits a surplus food listing (item, quantity, expiry window, pickup location) through a simple web form.
2. The matching engine scores nearby NGOs by proximity, urgency, and declared capacity, and selects the best match.
3. The matched NGO receives an automated notification (SMS/WhatsApp/email) with pickup details.
4. The match is logged for tracking — kg of food redistributed, response time, and other impact metrics.

## Data Sources

- FAO Food Loss and Waste Database — country-level food loss statistics used to ground the problem and weight urgency scoring by commodity type.
- *(add any additional sources used — FEWS NET, HDX, World Bank, etc.)*

## Tech Stack

- **Backend:** Python, Flask
- **Frontend:** HTML, CSS
- **Data:** JSON seed data (vendors, NGOs) + cleaned FAO dataset for grounding
- **Notifications:** *(Twilio / SMTP — fill in once implemented)*

## Project Structure

```
CatalystAlliance/
├── README.md
├── LICENSE
├── src/
│   ├── app.py
│   ├── matching_engine.py
│   ├── notify.py
│   ├── templates/
│   ├── static/
│   └── data/
└── docs/
    ├── project-summary.pdf
    └── (research notes, screenshots)
```

## How to Run

```bash
# clone the repo and navigate to this folder
cd 2026-cohort/CatalystAlliance/src

# install dependencies
pip install -r requirements.txt

# run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

## Walkthrough Video

*(link to be added — max 5 minutes)*

## Future Ideas

- Expand matching to individual consumers, not just NGOs
- Real-time geolocation instead of dropdown location selection
- SMS-first / WhatsApp bot interface for lower-bandwidth accessibility
- Partner integrations with real NGOs and vendors post-MVP

## License

MIT — see [LICENSE](./LICENSE)