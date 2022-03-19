from db import *
class Timetable:
    def __init__(self,id,slots):
        self.id = id
        self.slots = slots
        self.binary_val = bin(int(id))[2:].zfill(8)
    def __repr__(self) -> str:
        return f'{self.id} {self.slots}'

class Slot:
    def __init__(self,day,slot,room = "1"):
        self.day  = day
        self.slot =  slot
        self.room = room
        self.day_binary = bin(int(day))[2:].zfill(8)
        #self.room_binary = bin(int(room))[2:].zfill(8)
        self.slot_binary = bin(int(slot))[2:].zfill(8)

    def __repr__(self) -> str:
        return f'{self.day} {self.slot} {self.room}'

def store_new_timetable(timetable):
    # Deleting Previous Timetable
    if db.delete_timetable():
        for reg_course in timetable:
            for slot_num in range(0, 2):
                db.insert_reg_course_timetable(reg_course.id, reg_course.slots[slot_num].day,
                                            reg_course.slots[slot_num].slot, reg_course.slots[slot_num].room)    