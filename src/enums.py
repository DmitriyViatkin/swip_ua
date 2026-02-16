"""Enums module."""
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    SUPERADMIN = "superadmin"
    AGENT = "agent"
    DEV = "dev"
    NOTARY = "notary"
    SALES_DEP = "sales_dep"
    CLIENT = "client"


class BuildingStatus(str, Enum):
    APARTMENT = "apartment"
    COTTAGE = "cottage"
    HOUSE = "house"


class BuildingType(str, Enum):
    APARTMENT_BUILDING = "apartment_building"
    PRIVATE_HOUSE = "private_house"


class HomeClass(str, Enum):
    ELITE = "elite"
    BUDGET = "budget"


class ConstructionTechnology(str, Enum):
    MONOLITH_EXPANDED_CLAY = "monolith_expanded_clay"
    BRICK = "brick"


class TerritoryChoice(str, Enum):
    CLOSED_GUARDED = "closed_guarded"
    CLOSED = "closed"
    OPEN_UNGUARDED = "open_unguarded"


class GasChoice(str, Enum):
    YES = "yes"
    NO = "no"


class HeatingChoice(str, Enum):
    CENTRAL = "central"
    INDIVIDUAL = "individual"


class SewerageChoice(str, Enum):
    INDIVIDUAL = "individual"
    CENTRAL = "central"


class WaterSupplyChoice(str, Enum):
    CENTRAL = "central"
    INDIVIDUAL = "individual"


class UtilityBillsChoice(str, Enum):
    FIXED = "fixed"
    BY_METER = "by_meter"


class AppointmentEnum(str, Enum):
    APARTMENTS = "Апартаменты"
    FLAT = "Квартира"
    HOUSE = "Дом"
    STUDIO = "Студия"



class LayoutEnum(str, Enum):
    JOINT = "санузел+ туалет"
    SEPARATE = "Сан узел и туалет роздельно"



class StateEnum(str, Enum):
    HANDED_OVER = "handed over"
    PIT = "pit"



class HeatingEnum(str, Enum):
    CENTRALIZED = "Централизованное"
    AUTONOMOUS = "Автономное"
    INDIVIDUAL = "Индивидуальное"



class PaymentPartyEnum(str, Enum):
    USER = "user"
    DEVELOPER = "developer"
    NOTARY = "notary"
    SALES_DEPARTMENT = "sales_department"


class CommunicationPartyEnum(str, Enum):
    USER = "user"
    DEVELOPER = "developer"
    NOTARY = "notary"
    SALES_DEPARTMENT = "sales_department"


class TypeEnum(str, Enum):
    UP = "up"
    TURBO = "turbo"
    FREE = "free"


class HousingMarketEnum(str, Enum):
    """Типы жилищного рынка."""
    SECONDARY = "вторичный рынок"
    NEW_BUILD = "новострой"
    COTTAGE = "котедж"


class DistrictEnum(str, Enum):
    """Основные районы/дистрикты."""
    CENTER = "центр"
    KHORTYTSKY = "Хортицкий"
    KOSMICHESKY = "Космический"


class MicroDistrictEnum(str, Enum):
    """Микрорайоны, обозначенные числами."""
    ONE = "1"
    TWO = "2"
    THREE = "3"


class FinishingEnum(str, Enum):
    """Типы отделки."""
    ROUGH = "Черновая"
    FINISHED = "Готова"
    OPTION_3 = "3"


class StatusBuildEnum(str, Enum):
    """Статус строительства."""
    HANDED_OVER = "handed over"
    PIT = "pit"


class BuildTypeEnum(str, Enum):
    """Тип строения."""
    APARTMENT_BUILDING = "apartment_building"
    PRIVATE_HOUSE = "private_house"


class PaymentEnum(str, Enum):
    """Способы оплаты."""
    CASH = "cash"
    MORTGAGE = "mortgage"
    INSTALLMENT = "installment"
    MATERNAL_CAPITAL = "maternal_capital"

class ComplaintReasonEnum(str, Enum):
    INCORRECT_PRICE = "Некоректна ціна"
    INCORRECT_PHOTO = "Некоректне фото"
    INCORRECT_DESCRIPTION = "Некоректний опис"
    OTHER = "Інше"

