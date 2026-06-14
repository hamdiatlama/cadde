"""add vehicle catalog and expert inspection tables

Revision ID: 0003
Revises: 0002
Create Date: 2026-06-14
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003"
down_revision: Union[str, None] = "0002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── Enum types ──
    op.execute("CREATE TYPE report_status AS ENUM ('draft', 'approved', 'cancelled')")
    op.execute("CREATE TYPE check_result AS ENUM ('passed', 'failed', 'warning')")

    # ── 000003: Vehicle Catalog ──

    op.create_table(
        "vehicle_categories",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
        sa.Column("parent_id", sa.SmallInteger(), sa.ForeignKey("vehicle_categories.id"), nullable=True),
        sa.Column("sort_order", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "vehicle_segments",
        sa.Column("code", sa.CHAR(1), nullable=False),
        sa.Column("name", sa.String(50), nullable=False),
        sa.Column("description", sa.String(200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("code"),
    )

    op.create_table(
        "body_types",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "vehicle_brands",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(200), nullable=False, unique=True),
        sa.Column("country", sa.String(100), nullable=True),
        sa.Column("logo_url", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_vbrands_name", "vehicle_brands", ["name"])

    op.create_table(
        "vehicle_models",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("brand_id", sa.Integer(), sa.ForeignKey("vehicle_brands.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("segment_code", sa.CHAR(1), sa.ForeignKey("vehicle_segments.code"), nullable=True),
        sa.Column("production_start", sa.SmallInteger(), nullable=True),
        sa.Column("production_end", sa.SmallInteger(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_vmodels_brand", "vehicle_models", ["brand_id"])
    op.create_index("idx_vmodels_name", "vehicle_models", ["name"])
    op.create_index("idx_vmodels_segment", "vehicle_models", ["segment_code"])

    op.create_table(
        "vehicle_model_body_types",
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("vehicle_models.id", ondelete="CASCADE"), nullable=False),
        sa.Column("body_type_id", sa.SmallInteger(), sa.ForeignKey("body_types.id", ondelete="CASCADE"), nullable=False),
        sa.PrimaryKeyConstraint("model_id", "body_type_id"),
    )

    op.create_table(
        "vehicle_category_models",
        sa.Column("category_id", sa.SmallInteger(), sa.ForeignKey("vehicle_categories.id", ondelete="CASCADE"), nullable=False),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("vehicle_models.id", ondelete="CASCADE"), nullable=False),
        sa.PrimaryKeyConstraint("category_id", "model_id"),
    )

    op.create_table(
        "vehicle_model_years",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("vehicle_models.id", ondelete="CASCADE"), nullable=False),
        sa.Column("year", sa.SmallInteger(), nullable=False),
        sa.Column("trim_name", sa.String(200), nullable=True),
        sa.Column("engine_volume", sa.Numeric(4, 1), nullable=True),
        sa.Column("horsepower", sa.SmallInteger(), nullable=True),
        sa.Column("fuel_type", sa.String(50), nullable=True),
        sa.Column("transmission", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("model_id", "year", "trim_name"),
    )
    op.create_index("idx_vmodelyears_model", "vehicle_model_years", ["model_id"])
    op.create_index("idx_vmodelyears_year", "vehicle_model_years", ["year"])

    op.create_table(
        "feature_groups",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False, unique=True),
        sa.Column("sort_order", sa.SmallInteger(), server_default=sa.text("0"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "features",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("group_id", sa.SmallInteger(), sa.ForeignKey("feature_groups.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("slug", sa.String(200), nullable=False, unique=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "vehicle_model_features",
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("vehicle_models.id", ondelete="CASCADE"), nullable=False),
        sa.Column("feature_id", sa.Integer(), sa.ForeignKey("features.id", ondelete="CASCADE"), nullable=False),
        sa.Column("is_standard", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.PrimaryKeyConstraint("model_id", "feature_id"),
    )

    # ── 000004: Expert Inspection ──

    op.create_table(
        "expert_companies",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("tse_no", sa.String(50), nullable=True),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("address", sa.Text(), nullable=True),
        sa.Column("email", sa.String(100), nullable=True),
        sa.Column("tax_office", sa.String(100), nullable=True),
        sa.Column("tax_no", sa.String(20), nullable=True),
        sa.Column("authorized_person", sa.String(100), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute("ALTER TABLE expert_companies ADD COLUMN location GEOGRAPHY(POINT, 4326)")

    op.create_table(
        "experts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False, unique=True),
        sa.Column("company_id", sa.Integer(), sa.ForeignKey("expert_companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(100), nullable=True),
        sa.Column("signature_data", sa.Text(), nullable=True),
        sa.Column("license_no", sa.String(50), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_experts_user", "experts", ["user_id"])
    op.create_index("ix_experts_company", "experts", ["company_id"])

    op.create_table(
        "expert_packages",
        sa.Column("id", sa.SmallInteger(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), server_default=sa.text("0"), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "expert_vehicles",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("plate", sa.String(20), nullable=False),
        sa.Column("chassis_no", sa.String(50), nullable=False),
        sa.Column("engine_no", sa.String(50), nullable=True),
        sa.Column("brand_id", sa.Integer(), sa.ForeignKey("vehicle_brands.id"), nullable=True),
        sa.Column("model_id", sa.Integer(), sa.ForeignKey("vehicle_models.id"), nullable=True),
        sa.Column("model_year", sa.SmallInteger(), nullable=True),
        sa.Column("color_type", sa.String(20), nullable=True),
        sa.Column("fuel_type", sa.String(20), nullable=True),
        sa.Column("vehicle_type", sa.String(20), nullable=True),
        sa.Column("mileage", sa.Integer(), nullable=True),
        sa.Column("inspection_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plate", "chassis_no"),
    )
    op.create_index("idx_expveh_plate", "expert_vehicles", ["plate"])
    op.create_index("idx_expveh_chassis", "expert_vehicles", ["chassis_no"])

    # Partitioned table: expert_reports
    op.execute("""
        CREATE TABLE expert_reports (
            id BIGSERIAL NOT NULL,
            report_no VARCHAR(50) NOT NULL,
            company_id INT NOT NULL REFERENCES expert_companies(id),
            expert_id INT NOT NULL REFERENCES experts(id),
            vehicle_id INT NOT NULL REFERENCES expert_vehicles(id),
            package_id SMALLINT REFERENCES expert_packages(id),
            report_date TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            key_check BOOLEAN DEFAULT true,
            license_check BOOLEAN DEFAULT true,
            fee NUMERIC(10,2),
            expert_note TEXT,
            overall_result check_result,
            qr_code TEXT,
            validity_date DATE,
            status report_status NOT NULL DEFAULT 'draft',
            created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            UNIQUE (report_no)
        ) PARTITION BY RANGE (report_date)
    """)
    op.create_index("idx_reports_company", "expert_reports", ["company_id"])
    op.create_index("idx_reports_expert", "expert_reports", ["expert_id"])
    op.create_index("idx_reports_vehicle", "expert_reports", ["vehicle_id"])
    op.create_index("idx_reports_no", "expert_reports", ["report_no"])

    # 2026 monthly partitions
    op.execute("CREATE TABLE expert_reports_2026_01 PARTITION OF expert_reports FOR VALUES FROM ('2026-01-01') TO ('2026-02-01')")
    op.execute("CREATE TABLE expert_reports_2026_02 PARTITION OF expert_reports FOR VALUES FROM ('2026-02-01') TO ('2026-03-01')")
    op.execute("CREATE TABLE expert_reports_2026_03 PARTITION OF expert_reports FOR VALUES FROM ('2026-03-01') TO ('2026-04-01')")
    op.execute("CREATE TABLE expert_reports_2026_04 PARTITION OF expert_reports FOR VALUES FROM ('2026-04-01') TO ('2026-05-01')")
    op.execute("CREATE TABLE expert_reports_2026_05 PARTITION OF expert_reports FOR VALUES FROM ('2026-05-01') TO ('2026-06-01')")
    op.execute("CREATE TABLE expert_reports_2026_06 PARTITION OF expert_reports FOR VALUES FROM ('2026-06-01') TO ('2026-07-01')")
    op.execute("CREATE TABLE expert_reports_2026_07 PARTITION OF expert_reports FOR VALUES FROM ('2026-07-01') TO ('2026-08-01')")
    op.execute("CREATE TABLE expert_reports_2026_08 PARTITION OF expert_reports FOR VALUES FROM ('2026-08-01') TO ('2026-09-01')")
    op.execute("CREATE TABLE expert_reports_2026_09 PARTITION OF expert_reports FOR VALUES FROM ('2026-09-01') TO ('2026-10-01')")
    op.execute("CREATE TABLE expert_reports_2026_10 PARTITION OF expert_reports FOR VALUES FROM ('2026-10-01') TO ('2026-11-01')")
    op.execute("CREATE TABLE expert_reports_2026_11 PARTITION OF expert_reports FOR VALUES FROM ('2026-11-01') TO ('2026-12-01')")
    op.execute("CREATE TABLE expert_reports_2026_12 PARTITION OF expert_reports FOR VALUES FROM ('2026-12-01') TO ('2027-01-01')")

    op.create_table(
        "expert_panel_measurements",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("panel_name", sa.String(100), nullable=False),
        sa.Column("status_code", sa.String(50), nullable=True),
        sa.Column("paint_thickness", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.SmallInteger(), server_default=sa.text("0")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_panel_report", "expert_panel_measurements", ["report_id"])

    op.create_table(
        "expert_interior_checks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("check_point", sa.String(100), nullable=False),
        sa.Column("condition", sa.String(20), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_interior_report", "expert_interior_checks", ["report_id"])

    op.create_table(
        "expert_exterior_checks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("part_name", sa.String(100), nullable=False),
        sa.Column("condition", sa.String(20), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_exterior_report", "expert_exterior_checks", ["report_id"])

    op.create_table(
        "expert_mechanical_checks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("test_name", sa.String(100), nullable=False),
        sa.Column("result_value", sa.Text(), nullable=True),
        sa.Column("unit", sa.String(30), nullable=True),
        sa.Column("reference_value", sa.Text(), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_mechanical_report", "expert_mechanical_checks", ["report_id"])

    op.create_table(
        "expert_electronic_checks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("system_name", sa.String(100), nullable=False),
        sa.Column("check_result", sa.Text(), nullable=True),
        sa.Column("error_code", sa.String(20), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_electronic_report", "expert_electronic_checks", ["report_id"])

    op.create_table(
        "expert_tire_checks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("position", sa.String(20), nullable=False),
        sa.Column("tread_depth", sa.Numeric(4, 1), nullable=True),
        sa.Column("rim_condition", sa.String(30), nullable=True),
        sa.Column("tire_brand", sa.String(50), nullable=True),
        sa.Column("tire_size", sa.String(30), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "expert_tramer_records",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("has_accident", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("damage_detail", sa.Text(), nullable=True),
        sa.Column("is_heavy_damage", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("replaced_parts", sa.Text(), nullable=True),
        sa.Column("query_date", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "expert_test_drive",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("steering", sa.Text(), nullable=True),
        sa.Column("cornering", sa.Text(), nullable=True),
        sa.Column("vibration", sa.Text(), nullable=True),
        sa.Column("noise", sa.Text(), nullable=True),
        sa.Column("pulling", sa.Text(), nullable=True),
        sa.Column("overall_note", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "expert_dyno_tests",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("measurement_name", sa.String(100), nullable=False),
        sa.Column("measured_value", sa.Numeric(10, 2), nullable=True),
        sa.Column("unit", sa.String(20), nullable=True),
        sa.Column("factory_value", sa.Numeric(10, 2), nullable=True),
        sa.Column("diff_percent", sa.Numeric(5, 2), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "expert_photos",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=False),
        sa.Column("category", sa.String(50), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.SmallInteger(), server_default=sa.text("0")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_photos_report", "expert_photos", ["report_id"])

    # ── 000014: Expert Legacy Tables ──

    op.create_table(
        "expert_emission_tests",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("co", sa.Numeric(6, 2), nullable=True),
        sa.Column("hc", sa.Numeric(6, 2), nullable=True),
        sa.Column("co2", sa.Numeric(6, 2), nullable=True),
        sa.Column("lambda", sa.Numeric(4, 2), nullable=True),
        sa.Column("dpf_doluluk", sa.Numeric(5, 2), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_emission_report", "expert_emission_tests", ["report_id"])

    op.create_table(
        "expert_fluid_tests",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("test_type", sa.String(50), nullable=False),
        sa.Column("water_ratio", sa.Numeric(5, 2), nullable=True),
        sa.Column("freezing_point", sa.Numeric(5, 2), nullable=True),
        sa.Column("boiling_point", sa.Numeric(5, 2), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_fluid_report", "expert_fluid_tests", ["report_id"])

    op.create_table(
        "expert_handbrake_tests",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("pull_distance", sa.Numeric(5, 1), nullable=True),
        sa.Column("force", sa.Numeric(6, 2), nullable=True),
        sa.Column("efficiency_rate", sa.Numeric(5, 2), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_handbrake_report", "expert_handbrake_tests", ["report_id"])

    op.create_table(
        "expert_four_wheel_drive_checks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("transfer_case", sa.Text(), nullable=True),
        sa.Column("front_diff", sa.Text(), nullable=True),
        sa.Column("rear_diff", sa.Text(), nullable=True),
        sa.Column("torque_distribution", sa.Text(), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_4wd_report", "expert_four_wheel_drive_checks", ["report_id"])

    op.create_table(
        "expert_belt_checks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("belt_type", sa.String(50), nullable=False),
        sa.Column("wear_status", sa.String(50), nullable=True),
        sa.Column("tension_status", sa.String(50), nullable=True),
        sa.Column("is_passed", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_belt_report", "expert_belt_checks", ["report_id"])

    op.create_table(
        "expert_chassis_checks",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("chassis_original", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("labels_present", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("vin_plate_status", sa.String(100), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_chassis_report", "expert_chassis_checks", ["report_id"])

    op.create_table(
        "expert_extra_equipment",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipment_name", sa.String(100), nullable=False),
        sa.Column("is_present", sa.Boolean(), server_default=sa.text("true")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_extra_equip_report", "expert_extra_equipment", ["report_id"])

    op.create_table(
        "expert_mandatory_equipment",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("equipment_name", sa.String(100), nullable=False),
        sa.Column("is_present", sa.Boolean(), server_default=sa.text("false")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_mandatory_equip_report", "expert_mandatory_equipment", ["report_id"])

    op.create_table(
        "expert_acceptance_criteria",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("report_id", sa.BigInteger(), sa.ForeignKey("expert_reports.id", ondelete="CASCADE"), nullable=False),
        sa.Column("brake_balance_deviation_max", sa.Numeric(5, 2), server_default=sa.text("15.00")),
        sa.Column("suspension_efficiency_min", sa.Numeric(5, 2), server_default=sa.text("40.00")),
        sa.Column("handbrake_efficiency_min", sa.Numeric(5, 2), server_default=sa.text("16.00")),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("idx_acceptance_report", "expert_acceptance_criteria", ["report_id"])


def downgrade() -> None:
    # 000014 tables
    op.drop_table("expert_acceptance_criteria")
    op.drop_table("expert_mandatory_equipment")
    op.drop_table("expert_extra_equipment")
    op.drop_table("expert_chassis_checks")
    op.drop_table("expert_belt_checks")
    op.drop_table("expert_four_wheel_drive_checks")
    op.drop_table("expert_handbrake_tests")
    op.drop_table("expert_fluid_tests")
    op.drop_table("expert_emission_tests")

    # 000004 tables
    op.drop_table("expert_photos")
    op.drop_table("expert_dyno_tests")
    op.drop_table("expert_test_drive")
    op.drop_table("expert_tramer_records")
    op.drop_table("expert_tire_checks")
    op.drop_table("expert_electronic_checks")
    op.drop_table("expert_mechanical_checks")
    op.drop_table("expert_exterior_checks")
    op.drop_table("expert_interior_checks")
    op.drop_table("expert_panel_measurements")
    # drop partitions before parent
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_01")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_02")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_03")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_04")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_05")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_06")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_07")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_08")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_09")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_10")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_11")
    op.execute("DROP TABLE IF EXISTS expert_reports_2026_12")
    op.drop_table("expert_reports")
    op.drop_table("expert_vehicles")
    op.drop_table("expert_packages")
    op.drop_table("experts")
    op.drop_table("expert_companies")

    # 000003 tables
    op.drop_table("vehicle_model_features")
    op.drop_table("features")
    op.drop_table("feature_groups")
    op.drop_table("vehicle_model_years")
    op.drop_table("vehicle_category_models")
    op.drop_table("vehicle_model_body_types")
    op.drop_table("vehicle_models")
    op.drop_table("vehicle_brands")
    op.drop_table("body_types")
    op.drop_table("vehicle_segments")
    op.drop_table("vehicle_categories")

    # Enum types
    op.execute("DROP TYPE IF EXISTS check_result")
    op.execute("DROP TYPE IF EXISTS report_status")
