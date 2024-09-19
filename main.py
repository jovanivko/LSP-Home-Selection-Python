from aggregators import *
from attribute_tree import *
from criteria import create_criterion, ContinuousCriterion, QualitativeCriterion, DiscreteCriterion

# ContinuousCriterion, QualitativeCriterion, and DiscreteCriterion class instances

criteria_objects = []

# Example criterion: Удаљеност од радног места оца (continuous criterion)
description_father_work = "Погодност дома у односу на удаљеност од радног места оца."
criterion_father_work = ContinuousCriterion(
    name="Удаљеност од радног места оца",
    description=description_father_work,
    points=[(2, 1.0), (3, 0.7), (5, 0.4), (8, 0.0)]
)
criteria_objects.append(criterion_father_work)

# Example criterion: Удаљеност од радног места мајке (continuous criterion)
description_mother_work = "Погодност дома у односу на удаљеност од радног места мајке."
values_mother_work = [1, 2, 4, 5]
suitabilities_mother_work = [1.0, 0.7, 0.4, 0.0]
criterion_mother_work = ContinuousCriterion(
    name="Удаљеност од радног места мајке",
    description=description_mother_work,
    points=[(1, 1.0), (2, 0.7), (4, 0.4), (5, 0.0)]
)
criteria_objects.append(criterion_mother_work)

# Example criterion: Просечна удаљеност од школа (continuous criterion)
description_school_distance = "Мери просечну удаљеност од школе за оба детета."
points_school_distance = [(0, 1.0), (500, 0.6), (2000, 0.0)]
criterion_school_distance = ContinuousCriterion(
    name="Просечна удаљеност од школа",
    description=description_school_distance,
    points=points_school_distance
)
criteria_objects.append(criterion_school_distance)

# Example criterion: Приступ јавном превозу (discrete criterion)
description_public_transport = "Мери броj различитих врста градског превоза у кругу од 500 метара од jединице."
values_public_transport = [3, 2, 1, 0]
suitabilities_public_transport = [1.0, 0.6, 0.3, 0.0]
criterion_public_transport = DiscreteCriterion(
    name="Приступ јавном превозу",
    description=description_public_transport,
    value_score_mapping=dict(zip(values_public_transport, suitabilities_public_transport))
)
criteria_objects.append(criterion_public_transport)

# Example criterion: Доступност трговине (continuous criterion)
description_shopping_access = "Удаљеност наjближе добро опремљене радње у коjоj се могу пронаћи скоро све потрепштине."
points_shopping_access = [(50, 1.0), (100, 0.7), (200, 0.4), (500, 0.0)]
criterion_shopping_access = ContinuousCriterion(
    name="Доступност трговине",
    description=description_shopping_access,
    points=points_shopping_access
)
criteria_objects.append(criterion_shopping_access)

# Example criterion: Доступност садржаjа за децу (discrete criterion)
description_child_facilities = "Присутност паркова за играње, излетишта, базена, позоришта за децу и биоскопа."
values_child_facilities = [5, 4, 3, 2, 1, 0]
suitabilities_child_facilities = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
criterion_child_facilities = DiscreteCriterion(
    name="Доступност садржаjа за децу",
    description=description_child_facilities,
    value_score_mapping=dict(zip(values_child_facilities, suitabilities_child_facilities))
)
criteria_objects.append(criterion_child_facilities)

# Example criterion: Доступност здравствених установа (discrete criterion)
description_health_access = "Присутност здравствених установа у кругу од два километара."
values_health_access = [4, 3, 2, 1, 0]
suitabilities_health_access = [1.0, 0.75, 0.5, 0.25, 0.0]
criterion_health_access = DiscreteCriterion(
    name="Доступност здравствених установа",
    description=description_health_access,
    value_score_mapping=dict(zip(values_health_access, suitabilities_health_access))
)
criteria_objects.append(criterion_health_access)

# Example criterion: Квадратура унутрашњег простора (continuous criterion)
description_square_footage = "Погодност дома у односу на квадратуру унутрашњег простора."
points_square_footage = [(100, 1.0), (75, 0.7), (50, 0.5), (50, 0.0)]
criterion_square_footage = ContinuousCriterion(
    name="Квадратура унутрашњег простора",
    description=description_square_footage,
    points=points_square_footage
)
criteria_objects.append(criterion_square_footage)

# Continuing the creation of criterion objects for the remaining criteria

# 2.2.1 Број спаваћих соба (discrete criterion)
description_bedrooms = "Погодност дома у односу на број спаваћих соба."
values_bedrooms = [3, 2, 1]
suitabilities_bedrooms = [1.0, 0.5, 0.0]
criterion_bedrooms = DiscreteCriterion(
    name="Број спаваћих соба",
    description=description_bedrooms,
    value_score_mapping=dict(zip(values_bedrooms, suitabilities_bedrooms))
)
criteria_objects.append(criterion_bedrooms)

# 2.2.2 Број купатила (discrete criterion)
description_bathrooms = "Погодност дома у односу на број купатила."
values_bathrooms = [2, 1]
suitabilities_bathrooms = [1.0, 0.5]
criterion_bathrooms = DiscreteCriterion(
    name="Број купатила",
    description=description_bathrooms,
    value_score_mapping=dict(zip(values_bathrooms, suitabilities_bathrooms))
)
criteria_objects.append(criterion_bathrooms)

# 2.2.3 Кухиња (qualitative criterion)
description_kitchen = "Квалитет кухиње: 3 - Пространа и модерна, 2 - Просечне величине и опреме, 1 - Мала или застарела."
values_kitchen = [3, 2, 1]
suitabilities_kitchen = [1.0, 0.7, 0.4]
criterion_kitchen = DiscreteCriterion(
    name="Кухиња",
    description=description_kitchen,
    value_score_mapping=dict(zip(values_kitchen, suitabilities_kitchen))
)
criteria_objects.append(criterion_kitchen)

# 2.2.4 Трпезариjа (qualitative criterion)
description_dining_room = "Погодност дома у односу на квалитет трпезарије."
values_dining_room = ['велика', 'осредња', 'мала', 'нема']
suitabilities_dining_room = [1.0, 0.7, 0.3, 0.0]
criterion_dining_room = QualitativeCriterion(
    name="Трпезариjа",
    description=description_dining_room,
    value_score_mapping=dict(zip(values_dining_room, suitabilities_dining_room))
)
criteria_objects.append(criterion_dining_room)

# 2.2.5 Дневна соба (discrete criterion)
description_living_room = "Квалитет дневне собе: 4 - Пространа са добром осветљеношћу, 0 - Нема посебан дневни боравак."
values_living_room = [4, 3, 2, 1, 0]
suitabilities_living_room = [1.0, 0.8, 0.65, 0.5, 0.0]
criterion_living_room = DiscreteCriterion(
    name="Дневна соба",
    description=description_living_room,
    value_score_mapping=dict(zip(values_living_room, suitabilities_living_room))
)
criteria_objects.append(criterion_living_room)

# 2.2.6 Распоред соба (qualitative criterion)
description_room_layout = "Оптималан распоред соба: 'одличан' - Практичан распоред, 'лош' - Незадовољавајући распоред."
values_room_layout = ['одличан', 'добар', 'лош']
suitabilities_room_layout = [1.0, 0.7, 0.3]
criterion_room_layout = QualitativeCriterion(
    name="Распоред соба",
    description=description_room_layout,
    value_score_mapping=dict(zip(values_room_layout, suitabilities_room_layout))
)
criteria_objects.append(criterion_room_layout)

# 2.3.1 Старост стамбене jединице (continuous criterion)
description_house_age = "Старост стамбене јединице."
points_house_age = [(5, 1.0), (10, 0.7), (20, 0.5), (40, 0.2), (40, 0.0)]
criterion_house_age = ContinuousCriterion(
    name="Старост стамбене jединице",
    description=description_house_age,
    points=points_house_age
)
criteria_objects.append(criterion_house_age)

# 2.3.2 Последња реновациjа (discrete criterion)
description_last_renovation = "Погодност дома у односу на последњу реновацију."
values_last_renovation = [5, 10]
suitabilities_last_renovation = [1.0, 0.7, 0.0]
criterion_last_renovation = DiscreteCriterion(
    name="Последња реновациjа",
    description=description_last_renovation,
    value_score_mapping=dict(zip(values_last_renovation, suitabilities_last_renovation))
)
criteria_objects.append(criterion_last_renovation)

# 2.3.3 Квалитет градње (qualitative criterion)
description_build_quality = "Квалитет градње: 'висок' - Висок квалитет, 'низак' - Низак квалитет градње."
values_build_quality = ['висок', 'виши средњи', 'нижи средњи', 'низак']
suitabilities_build_quality = [1.0, 0.7, 0.5, 0.3]
criterion_build_quality = QualitativeCriterion(
    name="Квалитет градње",
    description=description_build_quality,
    value_score_mapping=dict(zip(values_build_quality, suitabilities_build_quality))
)
criteria_objects.append(criterion_build_quality)

# 2.3.4 Енергетска ефикасност (qualitative criterion)
description_energy_efficiency = "Енергетска ефикасност: 'A' - Висока, 'D или мање' - Ниска."
values_energy_efficiency = ['A', 'B', 'C', 'D или мање']
suitabilities_energy_efficiency = [1.0, 0.7, 0.3, 0.0]
criterion_energy_efficiency = QualitativeCriterion(
    name="Енергетска ефикасност",
    description=description_energy_efficiency,
    value_score_mapping=dict(zip(values_energy_efficiency, suitabilities_energy_efficiency))
)
criteria_objects.append(criterion_energy_efficiency)

# 3.1.1.1 Приватна гаража (discrete criterion)
description_private_garage = "Погодност дома у односу на присуство приватне гараже."
values_private_garage = [2, 1, 0]
suitabilities_private_garage = [1.0, 0.5, 0.0]
criterion_private_garage = DiscreteCriterion(
    name="Приватна гаража",
    description=description_private_garage,
    value_score_mapping=dict(zip(values_private_garage, suitabilities_private_garage))
)
criteria_objects.append(criterion_private_garage)

# 3.1.2 Jавни паркинг (discrete criterion)
description_public_parking = "Тип јавног паркинга."
values_public_parking = [3, 2, 1, 0]
suitabilities_public_parking = [1.0, 0.7, 0.5, 0.0]
criterion_public_parking = DiscreteCriterion(
    name="Jавни паркинг",
    description=description_public_parking,
    value_score_mapping=dict(zip(values_public_parking, suitabilities_public_parking))
)
criteria_objects.append(criterion_public_parking)

# 3.2 Површина дворишта (continuous criterion)
description_yard_area = "Погодност дома у односу на површину дворишта."
points_yard_area = [(100, 1.0), (80, 0.85), (50, 0.5), (0, 0.0)]
criterion_yard_area = ContinuousCriterion(
    name="Површина дворишта",
    description=description_yard_area,
    points=points_yard_area
)
criteria_objects.append(criterion_yard_area)

# 3.3 Башта или тераса (discrete criterion)
description_garden_terrace = "Башта или тераса."
values_garden_terrace = [3, 2, 1, 0]
suitabilities_garden_terrace = [1.0, 0.6, 0.5, 0.0]
criterion_garden_terrace = DiscreteCriterion(
    name="Башта или тераса",
    description=description_garden_terrace,
    value_score_mapping=dict(zip(values_garden_terrace, suitabilities_garden_terrace))
)
criteria_objects.append(criterion_garden_terrace)



if __name__ == "__main__":
    for criterion in criteria_objects:
        criterion.display_info()
        criterion.plot_elementary_criterion()

    print(len(criteria_objects))
