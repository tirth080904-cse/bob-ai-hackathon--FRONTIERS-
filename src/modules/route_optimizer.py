# modules/route_optimizer.py
# ---------------------------------------------------------------------------
# SupplyChain Guardian — Module 2: Route Optimizer
# ---------------------------------------------------------------------------
# Recommends alternative routes for affected shipments.
#
# What's new vs the original recommender.py:
#   - Cargo-aware: perishable and hazardous shipments get a tailored
#     recommendation list first, then the general alternatives.
#   - Returns a combined list so nothing is ever left without options.
# ---------------------------------------------------------------------------

from data.shipments import ALTERNATIVE_ROUTES


def recommend_routes(affected_shipments):
    """
    Enriches each affected shipment with a tailored list of alternative routes.

    Logic:
      1. Look up the shipment's route in ALTERNATIVE_ROUTES.
      2. Start with cargo-type-specific alternatives (if any exist).
      3. Append the "all" alternatives as additional options.
      4. If the route isn't in the lookup table at all, use a fallback message.

    Parameters:
        affected_shipments (list): output of detect_affected_shipments()

    Returns:
        enriched (list): same shipments, each with an "alternatives" key added
    """
    enriched = []

    for shipment in affected_shipments:
        route      = shipment["route"]       # e.g. "Suez Canal"
        cargo_type = shipment["cargo_type"]  # e.g. "perishable"

        route_options = ALTERNATIVE_ROUTES.get(route)   # None if not found

        if route_options is None:
            # Route not in our lookup table — flag for manual review
            alternatives = ["No pre-defined alternative on file — manual review required"]

        else:
            alternatives = []

            # Step 1: cargo-type-specific options come first (highest relevance)
            if cargo_type in route_options:
                for alt in route_options[cargo_type]:
                    alternatives.append(f"[Recommended for {cargo_type}] {alt}")

            # Step 2: general options apply to all cargo types
            for alt in route_options["all"]:
                alternatives.append(alt)

        # Copy the shipment dict and attach the alternatives list
        enriched_shipment = dict(shipment)
        enriched_shipment["alternatives"] = alternatives
        enriched.append(enriched_shipment)

    return enriched
