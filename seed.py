from datetime import date
from app.database import SessionLocal
from app.models import Annalakshmi

records = [
    dict(full_name="Lakshmi Narayanan", mobile_number="9876543210",
         email="lakshmi.n@example.com", address="12, 4th Cross, Jayanagar",
         area="Jayanagar", city="Bangalore", state="Karnataka", pin_code="560041",
         cuisine_specialization="South Indian", veg_or_nonveg="veg",
         signature_dishes="Idli, Sambar, Coconut Chutney",
         available_timings="8 AM - 12 PM, 6 PM - 9 PM",
         max_orders_per_day=15, date_joined=date(2026, 1, 10), status="active"),

    dict(full_name="Radha Krishnan", mobile_number="9123456780",
         email="radha.k@example.com", address="45, MG Road",
         area="Indiranagar", city="Bangalore", state="Karnataka", pin_code="560038",
         cuisine_specialization="North Indian", veg_or_nonveg="veg",
         signature_dishes="Paneer Butter Masala, Naan",
         available_timings="9 AM - 1 PM",
         max_orders_per_day=12, date_joined=date(2026, 2, 15), status="active"),

    dict(full_name="Fathima Begum", mobile_number="9988776655",
         email=None, address="22, Frazer Town Main Road",
         area="Frazer Town", city="Bangalore", state="Karnataka", pin_code="560005",
         cuisine_specialization="Hyderabadi", veg_or_nonveg="non-veg",
         signature_dishes="Biryani, Haleem",
         available_timings="11 AM - 3 PM, 7 PM - 10 PM",
         max_orders_per_day=20, date_joined=date(2025, 11, 5), status="active"),

    dict(full_name="Meera Pillai", mobile_number="9012345678",
         email="meera.p@example.com", address="8, Church Street",
         area="Koramangala", city="Bangalore", state="Karnataka", pin_code="560034",
         cuisine_specialization="Kerala", veg_or_nonveg="veg",
         signature_dishes="Appam, Avial",
         available_timings=None,
         max_orders_per_day=10, date_joined=date(2025, 8, 20), status="inactive"),

    dict(full_name="Sunita Rao", mobile_number="9765432109",
         email="sunita.rao@example.com", address="17, Malleswaram 8th Cross",
         area="Malleswaram", city="Bangalore", state="Karnataka", pin_code="560003",
         cuisine_specialization="Konkani", veg_or_nonveg="veg",
         signature_dishes="Fish Curry, Sol Kadhi",
         available_timings="7 AM - 11 AM",
         max_orders_per_day=8, date_joined=date(2026, 3, 1), status="active")
]

db = SessionLocal()
for r in records:
    db.add(Annalakshmi(**r))
db.commit()
db.close()
print(f"Seeded {len(records)} records.")
