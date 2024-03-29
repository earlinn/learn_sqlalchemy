"""empty message

Revision ID: f111dde6790b
Revises: 
Create Date: 2024-03-26 09:59:04.497236

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "f111dde6790b"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "vacancies",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("compensation", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "workers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "cvs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("compensation", sa.Integer(), nullable=True),
        sa.Column(
            "workload", sa.Enum("parttime", "fulltime", name="workload"), nullable=False
        ),
        sa.Column("worker_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.CheckConstraint("compensation > 0", name="check_compensation_positive"),
        sa.ForeignKeyConstraint(["worker_id"], ["workers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("title_index", "cvs", ["title"], unique=False)
    op.create_table(
        "vacancies_replies",
        sa.Column("cv_id", sa.Integer(), nullable=False),
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.Column("cover_letter", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["cv_id"], ["cvs.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["vacancy_id"], ["vacancies.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("cv_id", "vacancy_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("vacancies_replies")
    op.drop_index("title_index", table_name="cvs")
    op.drop_table("cvs")
    op.drop_table("workers")
    op.drop_table("vacancies")
    op.execute("DROP TYPE workload")
    # ### end Alembic commands ###
