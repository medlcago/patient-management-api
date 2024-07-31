"""Table initialization

Revision ID: ea25e5643c82
Revises: 
Create Date: 2024-07-31 09:54:30.323171

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'ea25e5643c82'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employees',
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('role', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('is_active', sa.Boolean(), nullable=False),
                    sa.Column('last_login', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_employees')),
                    sa.UniqueConstraint('email', name=op.f('uq_employees_email'))
                    )

    op.create_table('patients',
                    sa.Column('full_name', sa.String(), nullable=False),
                    sa.Column('date_of_birth', sa.Date(), nullable=False),
                    sa.Column('gender', sa.String(), nullable=False),
                    sa.Column('address', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=True),
                    sa.Column('phone_number', sa.String(), nullable=True),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_patients'))
                    )

    op.create_table('health_profiles',
                    sa.Column('patient_id', sa.Integer(), nullable=False),
                    sa.Column('height', sa.Float(), nullable=False),
                    sa.Column('weight', sa.Float(), nullable=False),
                    sa.Column('blood_type', sa.String(), nullable=False),
                    sa.Column('allergies', sa.String(), nullable=False),
                    sa.Column('chronic_conditions', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
                    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'],
                                            name=op.f('fk_health_profiles_patient_id_patients')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_health_profiles')),
                    sa.UniqueConstraint('patient_id', name=op.f('uq_health_profiles_patient_id'))
                    )

    op.create_table('medical_records',
                    sa.Column('patient_id', sa.Integer(), nullable=False),
                    sa.Column('employee_id', sa.Integer(), nullable=False),
                    sa.Column('visit_date', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('diagnosis', sa.String(), nullable=False),
                    sa.Column('treatment', sa.String(), nullable=False),
                    sa.Column('notes', sa.String(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['employee_id'], ['employees.id'],
                                            name=op.f('fk_medical_records_employee_id_employees')),
                    sa.ForeignKeyConstraint(['patient_id'], ['patients.id'],
                                            name=op.f('fk_medical_records_patient_id_patients')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_medical_records'))
                    )

    op.create_table('prescriptions',
                    sa.Column('medical_record_id', sa.Integer(), nullable=False),
                    sa.Column('medication_name', sa.String(), nullable=False),
                    sa.Column('dosage', sa.String(), nullable=False),
                    sa.Column('start_date', sa.Date(), nullable=False),
                    sa.Column('end_date', sa.Date(), nullable=False),
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['medical_record_id'], ['medical_records.id'],
                                            name=op.f('fk_prescriptions_medical_record_id_medical_records')),
                    sa.PrimaryKeyConstraint('id', name=op.f('pk_prescriptions'))
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('prescriptions')
    op.drop_table('medical_records')
    op.drop_table('health_profiles')
    op.drop_table('patients')
    op.drop_table('employees')
    # ### end Alembic commands ###
