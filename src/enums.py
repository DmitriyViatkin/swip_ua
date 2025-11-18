"""Enums module."""
from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "admin"
    AGENT = "agent"
    DEV = "dev"             # Developer / застройщик
    NOTARY = "notary"
    SALES_DEP = "sales_dep" # Sales Department
    CLIENT = "client"


class BuildingStatus(StrEnum):
    APARTMENT = "apartment"
    COTTAGE = "cottage"
    HOUSE = "house"


class BuildingType(StrEnum):
    APARTMENT_BUILDING = "apartment_building"
    PRIVATE_HOUSE = "private_house"


class HomeClass(StrEnum):
    ELITE = "elite"
    BUDGET = "budget"


class ConstructionTechnology(StrEnum):
    MONOLITH_EXPANDED_CLAY = "monolith_expanded_clay"
    BRICK = "brick"


class TerritoryChoice(StrEnum):
    CLOSED_GUARDED = "closed_guarded"
    CLOSED = "closed"
    OPEN_UNGUARDED = "open_unguarded"


class GasChoice(StrEnum):
    YES = "yes"
    NO = "no"


class HeatingChoice(StrEnum):
    CENTRAL = "central"
    INDIVIDUAL = "individual"


class SewerageChoice(StrEnum):
    INDIVIDUAL = "individual"
    CENTRAL = "central"


class WaterSupplyChoice(StrEnum):
    CENTRAL = "central"
    INDIVIDUAL = "individual"


class UtilityBillsChoice(StrEnum):
    FIXED = "fixed"
    BY_METER = "by_meter"



# Соответствует choises_appointment
class AppointmentEnum(StrEnum):
    APARTMENTS = "Апартаменты"
    FLAT = "Квартира"
    HOUSE = "Дом"
    STUDIO = "Студия"

# Соответствует choises_layout
class LayoutEnum(StrEnum):
    JOINT = "санузел+ туалет"
    SEPARATE = "Сан узел и туалет роздельно"

# Соответствует choises_state (Состояние/стадия строительства)
class StateEnum(StrEnum):
    HANDED_OVER = "handed over" # Сдан в эксплуатацию
    PIT = "pit"                 # Котлован / на стадии строительства

# Соответствует choises_heating
class HeatingEnum(StrEnum):
    CENTRALIZED = "Централизованное"
    AUTONOMOUS = "Автономное"
    INDIVIDUAL = "Индивидуальное"

# Соответствует choises_payment (Для кого оплата)
class PaymentPartyEnum(StrEnum):
    USER = "user"
    DEVELOPER = "developer"
    NOTARY = "notary"
    SALES_DEPARTMENT = "sales_department"


class CommunicationPartyEnum(StrEnum):
    USER = "user"
    DEVELOPER = "developer"
    NOTARY = "notary"
    SALES_DEPARTMENT = "sales_department"

class TypeEnum(StrEnum):
    UP= "up"
    TURBO = "turbo"
class HousingMarketEnum(StrEnum):
    """Типы жилищного рынка."""
    SECONDARY = "вторичный рынок"
    NEW_BUILD = "новострой"
    COTTAGE = "котедж"

# =========================================================================
# Соответствует choises_district (первый блок)
# &lt;div style=&quot;text-align: left;&quot;&gt;district&lt;/div&gt;

class DistrictEnum(StrEnum):
    """Основные районы/дистрикты."""
    CENTER = "центр"
    KHORTYTSKY = "Хортицкий"
    KOSMICHESKY = "Космический"

# =========================================================================
# Соответствует choises_microdistrict (второй блок с 'district' с числами 1, 2, 3)
# Примечание: В диаграмме это поле названо "district", но по смыслу, скорее всего,
# оно соответствует полю 'microdistrict' из предыдущего запроса.
# В данном случае, это просто числовые метки.

class MicroDistrictEnum(StrEnum):
    """Микрорайоны, обозначенные числами."""
    ONE = "1"
    TWO = "2"
    THREE = "3"

# =========================================================================
# Соответствует choises_finishing (третий блок с 'district' и отделкой)
# &lt;div style=&quot;text-align: left;&quot;&gt;district&lt;/div&gt;

class FinishingEnum(StrEnum):
    """Типы отделки."""
    ROUGH = "Черновая"
    FINISHED = "Готова"
    OPTION_3 = "3"
