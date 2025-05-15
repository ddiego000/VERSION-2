class NavAirport:
    def __init__(self, name: str, sids: list[int], stars: list[int]):
        self.name = name
        self.sids = sids
        self.stars = stars

    def __repr__(self):
        return f"NavAirport({self.name}, SIDs={self.sids}, STARs={self.stars})"
