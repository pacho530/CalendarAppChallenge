from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
from typing import List, Dict
from app.services.util import generate_unique_id, reminder_not_found_error, event_not_found_error, \
    date_lower_than_today_error, slot_not_available_error


# Clase Reminder
@dataclass
class Reminder:
    # Constantes de clase
    date_time: datetime
    EMAIL: str = "email"
    SYSTEM: str = "system"
    type: str = EMAIL

    def __str__(self) -> str:
        return f"Reminder on {self.date_time} of type {self.type}"


# Clase Event
@dataclass
class Event:
    # Atributos obligatorios
    title: str
    description: str
    date_: date
    start_at: time
    end_at: time

    # Atributo opcional con valor por defecto
    id: str = field(default_factory=generate_unique_id)

    # Lista de recordatorios, valor por defecto lista vacía
    reminders: List[Reminder] = field(default_factory=list)

    def add_reminder(self, date_time: datetime, type_: str = Reminder.EMAIL):
        reminder = Reminder(date_time=date_time, type=type_)
        self.reminders.append(reminder)

    def delete_reminder(self, reminder_index: int):
        if 0 <= reminder_index < len(self.reminders):
            self.reminders.pop(reminder_index)
        else:
            reminder_not_found_error()

    def __str__(self) -> str:
        return f"ID: {self.id}\nEvent title: {self.title}\nDescription: {self.description}\nTime: {self.start_at} - {self.end_at}"


# Clase Day
class Day:
    def __init__(self, date_: date):
        self.date_ = date_
        self.slots: Dict[time, str | None] = {}
        self._init_slots()

    def _init_slots(self):
        # Crear los slots de 00:00 a 23:45 en intervalos de 15 minutos
        t = time(0, 0)
        delta = timedelta(minutes=15)
        while t < time(23, 59):
            self.slots[t] = None
            t = (datetime.combine(date.today(), t) + delta).time()

    def add_event(self, event_id: str, start_at: time, end_at: time):
        # Agregar event_id en los slots disponibles dentro del rango
        for slot in self.slots:
            if start_at <= slot < end_at:
                if self.slots[slot] is not None:
                    slot_not_available_error()
                self.slots[slot] = event_id

    def delete_event(self, event_id: str):
        deleted = False
        for slot, saved_id in self.slots.items():
            if saved_id == event_id:
                self.slots[slot] = None
                deleted = True
        if not deleted:
            event_not_found_error()

    def update_event(self, event_id: str, start_at: time, end_at: time):
        self.delete_event(event_id)
        self.add_event(event_id, start_at, end_at)


# Clase Calendar
class Calendar:
    def __init__(self):
        self.days: Dict[date, Day] = {}
        self.events: Dict[str, Event] = {}

    def add_event(self, title: str, description: str, date_: date, start_at: time, end_at: time) -> str:
        if date_ < datetime.now().date():
            date_lower_than_today_error()

        if date_ not in self.days:
            self.days[date_] = Day(date_)

        event = Event(title=title, description=description, date_=date_, start_at=start_at, end_at=end_at)
        self.days[date_].add_event(event.id, start_at, end_at)
        self.events[event.id] = event
        return event.id

    def add_reminder(self, event_id: str, date_time: datetime, type_: str = Reminder.EMAIL):
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()
        event.add_reminder(date_time, type_)

    def find_available_slots(self, date_: date) -> list[time]:
        day = self.days.get(date_)
        if day:
            return [slot for slot, event_id in day.slots.items() if event_id is None]
        return []

    def update_event(self, event_id: str, title: str, description: str, date_: date, start_at: time, end_at: time):
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()

        is_new_date = event.date_ != date_
        if is_new_date:
            self.delete_event(event_id)
            self.add_event(title, description, date_, start_at, end_at)
        else:
            event.title = title
            event.description = description
            self.days[date_].update_event(event_id, start_at, end_at)

    def delete_event(self, event_id: str):
        event = self.events.pop(event_id, None)
        if not event:
            event_not_found_error()
        if event.date_ in self.days:
            self.days[event.date_].delete_event(event_id)

    def find_events(self, start_at: date, end_at: date) -> Dict[date, List[Event]]:
        return {d: [e for e in self.events.values() if start_at <= e.date_ <= end_at] for d in
                range((end_at - start_at).days)}

    def delete_reminder(self, event_id: str, reminder_index: int):
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()
        event.delete_reminder(reminder_index)

    def list_reminders(self, event_id: str) -> List[Reminder]:
        event = self.events.get(event_id)
        if not event:
            event_not_found_error()
        return event.reminders


# Métodos predefinidos para Day
def delete_event(self, event_id: str):
    deleted = False
    for slot, saved_id in self.slots.items():
        if saved_id == event_id:
            self.slots[slot] = None
            deleted = True
    if not deleted:
        event_not_found_error()


def update_event(self, event_id: str, start_at: time, end_at: time):
    for slot in self.slots:
        if self.slots[slot] == event_id:
            self.slots[slot] = None

    for slot in self.slots:
        if start_at <= slot < end_at:
            if self.slots[slot]:
                slot_not_available_error()
            else:
                self.slots[slot] = event_id











