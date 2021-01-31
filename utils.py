from models import Sensor, SensorType, Base, engine, Session, Actuator
from models.trigger import Trigger, TriggerComparator


def setup_new_db():
    Base.metadata.create_all(engine)

    session = Session()
    ph = Sensor(name="PH", gpio_pin=21, sensor_type=SensorType.I2C)
    conductivity = Sensor(name="Conductivity", gpio_pin=22, sensor_type=SensorType.I2C)
    float_sensor = Sensor(name="Float", gpio_pin=23, sensor_type=SensorType.SWITCH)

    ph_up = Actuator(name="PH Up", gpio_pin=24)
    ph_down = Actuator(name="PH Down", gpio_pin=25)
    nutrients = Actuator(name="Nutrients", gpio_pin=26)

    ph_too_high = Trigger(
        name="PH Too High",
        sensor=ph.id,
        threshold=6.5,
        comparator=TriggerComparator.GREATER_THAN,
        actuator=ph_down.id,
        on_duration_seconds=5,
        period_seconds=600,
    )
    ph_too_low = Trigger(
        name="PH Too Low",
        sensor=ph.id,
        threshold=6.0,
        comparator=TriggerComparator.LESS_THAN,
        actuator=ph_up.id,
        on_duration_seconds=5,
        period_seconds=600,
    )

    nutrients_too_low = Trigger(
        name="Nutrients Too Low",
        sensor=conductivity.id,
        threshold=100.0,  # ?? too calibrate with back-of-the-box instructions
        comparator=TriggerComparator.LESS_THAN,
        actuator=nutrients.id,
        on_duration_seconds=5,
        period_seconds=600,
    )

    session.add(ph)
    session.add(conductivity)
    session.add(float_sensor)
    session.add(ph_up)
    session.add(ph_down)
    session.add(nutrients)
    session.add(ph_too_high)
    session.add(ph_too_low)
    # session.add(nutrients_too_low)

    session.commit()
