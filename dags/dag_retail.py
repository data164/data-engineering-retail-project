"""
DAG Airflow - Pipeline ETL Retail
Transformation des données brutes en KPIs quotidiens

Auteur: Mohamed Amhamed
Date: Octobre 2025
"""

from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.operators.bigquery import BigQueryInsertJobOperator

# Configuration du DAG
default_args = {
    'owner': 'mohamed',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
}

dag = DAG(
    dag_id='retail_etl_daily_kpis',
    default_args=default_args,
    description='Pipeline quotidien pour calculer les KPIs retail',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',  # Tourne tous les jours automatiquement
    catchup=False,  # Ne pas rattraper les exécutions passées
    tags=['retail', 'etl', 'bigquery'],
)

# Tâche principale : créer la table de KPIs dans BigQuery
# Cette requête agrège les données brutes (raw_retail) pour générer
# des métriques quotidiennes par magasin, produit et contexte
create_retail_daily_kpis = BigQueryInsertJobOperator(
    task_id='create_retail_daily_kpis_table',
    configuration={
        "query": {
            "query": """
                CREATE OR REPLACE TABLE `pipeline-etl-retail.retail_data_warehouse.retail_daily_kpis` AS
                SELECT
                    -- Dimensions pour grouper les données
                    Date,
                    `Store ID` AS store_id,
                    `Product ID` AS product_id,
                    Category AS product_category,
                    Region AS store_region,
                    `Weather Condition` AS weather_condition,
                    `Holiday_Promotion` AS holiday_promotion_status,
                    Seasonality AS seasonality,

                    -- Métriques de vente
                    ROUND(SUM(`Units Sold`), 2) AS total_units_sold,
                    ROUND(SUM(Price * `Units Sold`), 2) AS daily_revenue,
                    ROUND(SUM(Discount * `Units Sold`), 2) AS total_discount_given,

                    -- Métriques de stock et logistique
                    ROUND(AVG(`Inventory Level`), 2) AS average_inventory_level,
                    ROUND(SUM(`Units Ordered`), 2) AS total_units_ordered,
                    ROUND(AVG(`Demand Forecast`), 2) AS average_demand_forecast,

                    -- Métriques de pricing
                    ROUND(AVG(Price), 2) AS average_product_price,
                    ROUND(AVG(Discount), 2) AS average_discount_rate,
                    ROUND(AVG(`Competitor Pricing`), 2) AS average_competitor_price

                FROM
                    `pipeline-etl-retail.retail_data_warehouse.raw_retail`
                GROUP BY
                    Date, `Store ID`, `Product ID`, Category, Region, 
                    `Weather Condition`, `Holiday_Promotion`, Seasonality
                ORDER BY
                    Date DESC, `Store ID`, `Product ID`
            """,
            "useLegacySql": False
        }
    },
    gcp_conn_id='google_cloud_default',  # Connexion configurée dans Airflow
    location='europe-west9',  # Région Paris
    dag=dag
)

# Le DAG ne contient qu'une tâche pour l'instant
# Possibilités d'amélioration :
# - Ajouter une tâche de validation des données avant transformation
# - Créer une tâche d'archivage ou de backup
# - Implémenter des alertes en cas d'échec

create_retail_daily_kpis
