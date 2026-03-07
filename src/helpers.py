from shiny import ui


extra_instructions = """
        This dataset contains Vancouver police crime records from 2023-2025.
        Key columns: TYPE (crime category), YEAR, MONTH, DAY, HOUR, MINUTE,
        HUNDRED_BLOCK (street address), NEIGHBOURHOOD, X (longitude), Y (latitude).
        Crime types include: Break and Enter Commercial, Break and Enter Residential/Other,
        Homicide, Mischief, Offence Against a Person, Other Theft, Theft from Vehicle,
        Theft of Bicycle, Theft of Vehicle, Vehicle Collision or Pedestrian Struck.

        When a user uses informal terms for crime types, map them as follows:
        - 'vandalism' or 'graffiti' or "property damage" = 'Mischief'
        - 'car theft' or 'stolen car' = 'Theft of Vehicle'
        - 'mugging', 'assault', or 'robbery' = 'Offence Against a Person'
        - 'bike theft' or 'stolen bike' = 'Theft of Bicycle'
        - 'break in' or 'burglary' at a house/home/apartment = 'Break and Enter Residential/Other'
        - 'break in' or 'burglary' at a store/shop/office/business = 'Break and Enter Commercial'
        - if unclear whether residential or commercial, query both types

        Valid NEIGHBOURHOOD values are EXACTLY (use these exact strings in SQL queries):
        'Arbutus Ridge', 'Central Business District', 'Dunbar-Southlands', 'Fairview',
        'Grandview-Woodland', 'Hastings-Sunrise', 'Kensington-Cedar Cottage', 'Kerrisdale',
        'Killarney', 'Kitsilano', 'Marpole', 'Mount Pleasant', 'Musqueam', 'Oakridge',
        'Renfrew-Collingwood', 'Riley Park', 'Shaughnessy', 'South Cambie', 'Stanley Park',
        'Strathcona', 'Sunset', 'Victoria-Fraserview', 'West End', 'West Point Grey'

        When a user refers to a neighbourhood using an informal name, map it as follows:
        - 'Downtown' or 'City Centre' = 'Central Business District'
        - 'East Van' or 'East Vancouver' = 'Hastings-Sunrise' or 'Grandview-Woodland'
        - 'Kits' = 'Kitsilano'
        - 'Riley' = 'Riley Park'
        - 'Strathy' = 'Strathcona'
        """


def get_card_header(header, icon="Hover"):
    if icon == "Hover":
        svg = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px;vertical-align:middle"><path d="M22 14a8 8 0 0 1-8 8"/><path d="M18 11v-1a2 2 0 0 0-2-2a2 2 0 0 0-2 2"/><path d="M14 10V9a2 2 0 0 0-2-2a2 2 0 0 0-2 2v1"/><path d="M10 9.5V4a2 2 0 0 0-2-2a2 2 0 0 0-2 2v10"/><path d="M18 11a2 2 0 1 1 4 0v3a8 8 0 0 1-8 8h-2c-2.8 0-4.5-.86-5.99-2.34l-3.6-3.6a2 2 0 0 1 2.83-2.82L7 15"/></svg>'
    elif icon == "Click":
        svg = '<svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-right:4px;vertical-align:middle"><path d="M14 4.1 12 6"/><path d="m5.1 8-2.9-.8"/><path d="m6 12-1.9 2"/><path d="M7.2 2.2 8 5.1"/><path d="M9.037 9.69a.498.498 0 0 1 .653-.653l11 4.5a.5.5 0 0 1-.074.949l-4.349 1.041a1 1 0 0 0-.74.739l-1.04 4.35a.5.5 0 0 1-.95.074z"/></svg>'

    return ui.card_header(
        ui.div(
            header,
            ui.span(
                ui.HTML(svg),
                f"{icon} for more",
                style="margin-left:auto; display:inline-flex; align-items:center;",
                class_="badge-right",
            ),
            style="display:flex; align-items:center; width:100%;",
        ),
    )
