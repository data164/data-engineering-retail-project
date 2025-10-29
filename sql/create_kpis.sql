-- Transformation des données retail brutes en KPIs quotidiens
-- Cette requête agrège les données par jour, magasin et produit
-- pour générer des métriques exploitables dans Power BI

CREATE OR REPLACE TABLE `pipeline-etl-retail.retail_data_warehouse.retail_daily_kpis` AS

SELECT
    -- Colonnes de dimension (pour filtrer et grouper)
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

    -- Métriques de stock
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
    Date,
    `Store ID`,
    `Product ID`,
    Category,
    Region,
    `Weather Condition`,
    `Holiday_Promotion`,
    Seasonality

ORDER BY
    Date DESC,
    `Store ID`,
    `Product ID`;

-- Notes :
-- - La table est recréée complètement à chaque run (CREATE OR REPLACE)
-- - Les ROUND(, 2) servent à limiter les décimales pour la lisibilité
-- - L'ORDER BY n'est pas strictement nécessaire mais aide au debugging
