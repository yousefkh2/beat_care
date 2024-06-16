"""Initial migration.

Revision ID: bc24484d019b
Revises: 
Create Date: 2024-06-15 00:04:12.369221

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'bc24484d019b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=False),
    sa.Column('last_name', sa.String(length=255), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('sex', sa.String(length=10), nullable=False),
    sa.Column('identification_number', sa.String(length=50), nullable=False),
    sa.Column('phone_number', sa.String(length=50), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.Column('insurance_number', sa.String(length=50), nullable=True),
    sa.Column('insurance_company', sa.String(length=255), nullable=True),
    sa.Column('insurance_type', sa.String(length=50), nullable=True),
    sa.Column('next_of_kin_name', sa.String(length=255), nullable=True),
    sa.Column('next_of_kin_phone', sa.String(length=50), nullable=True),
    sa.Column('next_of_kin_address', sa.String(length=255), nullable=True),
    sa.Column('next_of_kin_relation', sa.String(length=50), nullable=True),
    sa.Column('icd10_code_main', sa.String(length=50), nullable=True),
    sa.Column('icd10_main_symptoms', sa.Text(), nullable=True),
    sa.Column('icd10_code_secondary', sa.String(length=50), nullable=True),
    sa.Column('icd10_secondary_symptoms', sa.Text(), nullable=True),
    sa.Column('primary_medication_name', sa.String(length=255), nullable=True),
    sa.Column('primary_medication_purpose', sa.Text(), nullable=True),
    sa.Column('primary_medication_dosage', sa.Text(), nullable=True),
    sa.Column('primary_medication_side_effects', sa.Text(), nullable=True),
    sa.Column('primary_medication_drug_interactions', sa.Text(), nullable=True),
    sa.Column('primary_medication_food_interactions', sa.Text(), nullable=True),
    sa.Column('secondary_medication_name', sa.String(length=255), nullable=True),
    sa.Column('secondary_medication_purpose', sa.Text(), nullable=True),
    sa.Column('secondary_medication_dosage', sa.Text(), nullable=True),
    sa.Column('secondary_medication_side_effects', sa.Text(), nullable=True),
    sa.Column('secondary_medication_drug_interactions', sa.Text(), nullable=True),
    sa.Column('secondary_medication_food_interactions', sa.Text(), nullable=True),
    sa.Column('date_of_admission', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=150), nullable=False),
    sa.Column('password', sa.String(length=150), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('patients')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patients',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('first_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('last_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('age', mysql.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('sex', mysql.VARCHAR(length=10), nullable=False),
    sa.Column('identification_number', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('phone_number', mysql.VARCHAR(length=50), nullable=False),
    sa.Column('address', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('insurance_number', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('insurance_company', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('insurance_type', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('next_of_kin_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('next_of_kin_phone', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('next_of_kin_address', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('next_of_kin_relation', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('icd10_code_main', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('icd10_main_symptoms', mysql.TEXT(), nullable=True),
    sa.Column('icd10_code_secondary', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('icd10_secondary_symptoms', mysql.TEXT(), nullable=True),
    sa.Column('primary_medication_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('primary_medication_purpose', mysql.TEXT(), nullable=True),
    sa.Column('primary_medication_dosage', mysql.TEXT(), nullable=True),
    sa.Column('primary_medication_side_effects', mysql.TEXT(), nullable=True),
    sa.Column('primary_medication_drug_interactions', mysql.TEXT(), nullable=True),
    sa.Column('primary_medication_food_interactions', mysql.TEXT(), nullable=True),
    sa.Column('secondary_medication_name', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('secondary_medication_purpose', mysql.TEXT(), nullable=True),
    sa.Column('secondary_medication_dosage', mysql.TEXT(), nullable=True),
    sa.Column('secondary_medication_side_effects', mysql.TEXT(), nullable=True),
    sa.Column('secondary_medication_drug_interactions', mysql.TEXT(), nullable=True),
    sa.Column('secondary_medication_food_interactions', mysql.TEXT(), nullable=True),
    sa.Column('date_of_admission', sa.DATE(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('user')
    op.drop_table('patient')
    # ### end Alembic commands ###
