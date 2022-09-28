from tools import AutoNumber


class Resource(AutoNumber):
    Brick = ()
    Lumber = ()
    Wool = ()
    Grain = ()
    Ore = ()


class DevelopmentCard(AutoNumber):
    Knight = ()
    RoadBuilding = ()
    YearOfPlenty = ()
    Monopoly = ()
    VictoryPoint = ()


class Space(AutoNumber):
    Hex = ()
    Intersection = ()
    Path = ()
    Null = ()


class Environment(AutoNumber):
    Land = ()
    Sea = ()
    Coast = ()


class CatanBoardObject(AutoNumber):
    ...


class Terrain(CatanBoardObject):  # requires (Hex, Land)
    NoTerrain = ()
    Hill = ()
    Forest = ()
    Pasture = ()
    Field = ()
    Mountain = ()
    Desert = ()


class TradeShip(CatanBoardObject):  # requires (Hex, Sea)
    NoTradeShip = ()
    BrickShip = ()
    LumberShip = ()
    WoolShip = ()
    GrainShip = ()
    OreShip = ()
    AllShip = ()


class Building(CatanBoardObject):  # requires (Intersection/Path, Land)
    NoBuilding = ()
    Settlement = ()
    City = ()
    Road = ()


class Request(AutoNumber):
    BuyDevCard = ()
    Trade = ()
    BuyBuilding = ()
    PlayDevCard = ()
    SelectPlayer = ()
    SelectResource = ()
    SelectTile = ()
    AcceptTrade = ()
    Pass = ()


class Event(AutoNumber):
    Start = ()
    PlaceInitialBuilding1A = ()
    PlaceInitialBuilding1B = ()
    PlaceInitialBuilding2A = ()
    PlaceInitialBuilding2B = ()
    PlayerTurn = ()
    PlaceBuilding = ()
    PlaceRobber = ()
    PickStealTarget = ()
    PickResReceived = ()
    PickTradeOffer = ()
    PickTradeRequest = ()
    PickTradeTargets = ()
    EvaluateTrade = ()
    PickMonopolyResource = ()
    PickDiscard = ()


class DevelopmentEffect:
    HireKnight = ()
    GrantBuildings = ()
    GrantResources = ()
    GrantMonopoly = ()


