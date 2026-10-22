class Master:
    def __init__(self, master_id):
        self.master_id = master_id


class Service:
    def __init__(self, service_id):
        self.service_id = service_id

def get_master(master_id):
    return Master(master_id) if master_id == 1 else None


def get_service(service_id):
    return Service(service_id) if service_id == 1 else None


class Appointment:
    def __init__(self, appointment_id, client_name, master_id, service_id, time):
        self.id = appointment_id
        self.client_name = client_name
        self.master_id = master_id
        self.service_id = service_id
        self.time = time


appointments = []


def create_appointment(client_name: str, master_id: int, service_id: int, time: str):

    if not client_name or not time:
        return None

    try:
        hour, minute = map(int, time.split(":"))
    except (ValueError, AttributeError):
        return None

    if hour < 8 or hour > 20:
        return None

    master = get_master(master_id)
    service = get_service(service_id)

    if master is None or service is None:
        return None

    appointment = Appointment(
        appointment_id=len(appointments) + 1,
        client_name=client_name,
        master_id=master.master_id,
        service_id=service.service_id,
        time=time,
    )
    appointments.append(appointment)
    return appointment

print("Задание 1")

first_appointment = create_appointment("Иванова А.А.", 1, 1, '10:00')
second_appointment = create_appointment("Петрова А.А.", 1, 1, '11:00')

for appointment in appointments:
    print(f"  {appointment.client_name} — {appointment.time}")

before = len(appointments)
no_correct_appointment = create_appointment("", 1, 1, '12:00')
after = len(appointments)
print(f"  Запись создана? {'Да' if after > before else 'Нет'}")
print(f"  Количество записей в списке: {len(appointments)}")
print(f"  Ожидалось: 2")

print("Задание 2")

for appointment in appointments:
    print(f"  {appointment.client_name} — {appointment.time}")

before = len(appointments)
no_correct_appointment2 = create_appointment("Сидорова А.А.", 1, 1, '00:00')
after = len(appointments)
print(f"  Запись создана? {'Да' if after > before else 'Нет'}")
print(f"  Количество записей в списке: {len(appointments)}")
print(f"  Ожидалось: 2")