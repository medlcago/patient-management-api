from models import Employee
from repositories.base import SQLAlchemyRepository


class EmployeeRepository(SQLAlchemyRepository[Employee]):
    model = Employee
