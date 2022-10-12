import untis_tcm_wrapper

data = untis_tcm_wrapper.get(1, 3182, "2022-10-11", 2)

rooms, teachers, lessons = untis_tcm_wrapper.parse_elements(data["elements"])