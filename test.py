import untis_tcm_wrapper
from gcal_manager import GCalManager

res = untis_tcm_wrapper.get(1, 3182, "2022-10-11", 2)

gcal = GCalManager()
event = gcal.create_event("test name", "test description", "8:00:00", "9:50:00", "2022-10-14")
