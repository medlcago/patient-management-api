from enum import StrEnum


class EmployeeRole(StrEnum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    RECEPTIONIST = "receptionist"


admin_only = (EmployeeRole.ADMIN,)
doctor_and_nurse = (EmployeeRole.DOCTOR, EmployeeRole.NURSE)
admin_doctor_nurse = (EmployeeRole.ADMIN, EmployeeRole.DOCTOR, EmployeeRole.NURSE)
all_roles = tuple(EmployeeRole)