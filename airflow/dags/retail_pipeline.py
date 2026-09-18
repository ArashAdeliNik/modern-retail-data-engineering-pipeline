from datetime import UTC, datetime, timedelta

from airflow.operators.bash import BashOperator

from airflow import DAG

DEFAULT_ARGS = {"owner": "data-engineering", "retries": 2, "retry_delay": timedelta(minutes=2)}

with DAG(
    dag_id="retail_analytics_pipeline",
    description="Generate, validate, load, transform, and test synthetic retail data",
    default_args=DEFAULT_ARGS,
    start_date=datetime(2026, 1, 1, tzinfo=UTC),
    schedule="@daily",
    catchup=False,
    max_active_runs=1,
    tags=["portfolio", "retail", "data-engineering"],
) as dag:
    generate = BashOperator(
        task_id="generate_daily_batch",
        bash_command="cd /opt/project && python -m src.pipeline generate --date {{ ds }} --rows 500",
    )
    ingest = BashOperator(
        task_id="validate_and_ingest",
        bash_command="cd /opt/project && python -m src.pipeline ingest",
    )
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/project/dbt && dbt run --profiles-dir .",
    )
    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/project/dbt && dbt test --profiles-dir .",
    )

    generate >> ingest >> dbt_run >> dbt_test
