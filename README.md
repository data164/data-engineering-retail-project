# Pipeline Data Engineering - Retail Analytics

## À propos du projet

Projet personnel de pipeline ETL complet pour analyser des données retail. L'idée était de créer quelque chose de concret, de bout en bout, pour comprendre vraiment comment fonctionne un pipeline de données en production.

**Objectif** : Automatiser l'ingestion et la transformation de données retail pour générer des KPIs business utilisables (CA, stocks, pricing, promotions).

---

## Architecture

```
📂 Données Brutes (CSV)
    ↓
☁️ Google Cloud Storage (Data Lake)
    ↓
🔄 Apache Airflow (Orchestration)
    ↓
📊 BigQuery (Data Warehouse)
    ↓ Transformation SQL
📈 Data Mart (KPIs quotidiens)
    ↓
📊 Power BI (Visualisation)
```

### Technologies utilisées

- **Orchestration** : Apache Airflow 2.7.3 (déployé localement avec Docker)
- **Cloud** : Google Cloud Platform (Storage + BigQuery)
- **Transformation** : SQL
- **Visualisation** : Power BI
- **Containerisation** : Docker Compose

---

## 📁 Structure du Projet

```
data-engineering-retail-project/
│
├── dags/
│   └── dag_retail.py              # DAG Airflow pour l'orchestration ETL
│
├── sql/
│   └── create_kpis.sql            # Requête de transformation des KPIs
│
├── docker-compose.yaml            # Configuration Docker Airflow
│
├── powerbi/
│   └── retail_dashboard.pbix      # Dashboard Power BI
│
├── config/
│   └── gcp-key-example.json       # Template de clé de service GCP
│
└── README.md
```

---

## Ce que fait le pipeline

### 1. Ingestion des données
Les données retail (transactions, stocks, produits) sont d'abord uploadées sur Google Cloud Storage, puis chargées dans BigQuery. J'ai dû gérer des petits problèmes de format CSV (séparateur `;` au lieu de `,`) car les données venaient d'un dataset anglophone que j'ai adapté.

### 2. Orchestration avec Airflow
J'ai configuré Airflow en local avec Docker Compose pour automatiser le pipeline. Le DAG tourne tous les jours et régénère la table de KPIs à partir des données brutes. Ça m'a pris un moment pour bien configurer la connexion avec GCP (service account, IAM, tout ça).

### 3. Transformation SQL
La partie la plus intéressante : transformer les données brutes en métriques business exploitables. J'agrège par date, magasin, produit et contexte (météo, promotions, saisonnalité) pour calculer :
- Chiffre d'affaires et volumes de vente
- Niveaux de stock et prévisions de demande
- Prix moyens et comparaisons avec la concurrence
- Impact des promotions

### 4. Visualisation Power BI
J'ai créé 3 dashboards pour analyser les résultats :

**Performance Globale**
- CA total : 550M€ sur la période analysée
- 10M d'unités vendues
- Marge brute de 450M€ (taux de marge 81,83%)
- Évolution du CA par catégorie produit

**Gestion Stocks & Promotions**
- Couverture stock : 194 jours en moyenne
- ROI des promotions : 450%
- Écart entre prévisions et ventes réelles : 3,6%

**Analyse Compétitivité**
- Comparaison de nos prix vs concurrence par catégorie
- Écart moyen : -0,02% (on est légèrement moins chers)

---

## Insights Business & Recommandations

Au-delà de la stack technique, l'exploitation de ces données a permis d'identifier plusieurs constats critiques et opportunités stratégiques pour le retail.

### Baisse du Chiffre d'Affaires (2022-2023)

Le CA a significativement diminué entre 2022 et 2023. Quand on voit la courbe descendre comme ça, ça sent pas bon. C'est le type de signal qui doit faire tiquer n'importe quel directeur commercial et nécessite une analyse approfondie des causes : perte de parts de marché face à la concurrence, stratégie pricing inadaptée, mix produit à revoir, ou impact d'événements externes (inflation, pouvoir d'achat).

Action prioritaire : identifier rapidement les leviers de redressement avant que la tendance ne s'aggrave.

### Surstock Critique (194% de couverture)

La couverture de stock moyenne atteint 194%, soit presque 2 fois plus de stock que nécessaire.

Conséquences business :
- Capital immobilisé : ressources financières bloquées qui pourraient être investies ailleurs
- Coûts de stockage : loyers d'entrepôt, manutention, assurances qui explosent
- Risque de démarque : obsolescence des produits, détérioration, invendus à brader

Calcul approximatif : avec un CA de 550M€ et un taux de marge de 82%, avoir 94% de stock en trop représente environ 38% du capital immobilisé inutilement.

Recommandation : réduire les commandes fournisseurs pour ajuster le stock au niveau optimal, accélérer la rotation via des promotions ciblées sur les produits à forte couverture, améliorer la précision des prévisions de demande.

### ROI Promotionnel Exceptionnel (450%)

Chaque euro investi en promotion rapporte 4,50€. C'est énorme. Ce ROI très élevé n'est pas juste un chiffre, c'est une opportunité stratégique majeure sous-exploitée.

Recommandation stratégique : avec un ROI pareil, on pourrait baisser légèrement les prix de base (exemple : -3 à -5%) et compenser avec encore plus de promotions (fréquence et agressivité accrues).

Résultat attendu : prix affichés plus attractifs que la concurrence, génération de volume de ventes (et c'est rentable vu le ROI), accélération de la rotation des stocks (bye bye le surstock), marge maintenue voire améliorée grâce au ROI élevé.

Benchmark : c'est exactement la stratégie utilisée par Decathlon, H&M ou Kiabi. Prix corrects + promotions fréquentes = trafic + volume + fidélisation.

### Prévisions de Demande Performantes (3,6% d'écart)

Le modèle de prévision affiche un écart moyen de seulement 3,6% entre les prévisions et les ventes réelles. C'est plutôt bon.

Cependant, une optimisation supplémentaire permettrait de réduire encore l'écart (objectif < 2%), améliorer la précision des commandes fournisseurs, et minimiser les ruptures de stock ET le surstock.

Piste d'amélioration : intégrer des modèles de Machine Learning (ARIMA, Prophet, ou modèles supervisés) pour capturer la saisonnalité et les tendances plus finement.

### Positionnement Prix Neutre (-0,02% vs concurrent)

Prix moyen : 55,14€  
Prix concurrent : 55,15€  
Écart : -0,02%

On est pile au même niveau que la concurrence. Ni plus chers, ni moins chers.

Question stratégique : comment attirer les clients vers nous plutôt que vers eux ?

Recommandation : vu qu'on a un ROI promo de 450%, on peut jouer plus agressivement sur ce levier.

Option 1 : Prix légèrement en dessous + promos fréquentes → image de "bonnes affaires", volume qui augmente, marge compensée par le ROI promo.

Option 2 : Même prix MAIS promos plus agressives → -30%, -40%, -50% réguliers, crée du trafic et de l'urgence, fidélisation (les clients attendent les promos).

Dans les deux cas, on utilise notre atout (ROI promo énorme) pour se différencier sans détruire la marge.

Parce que la vraie question c'est pas "quel prix ?" mais "pourquoi acheter chez nous ?". Et avec les bonnes données, on peut répondre à cette question avec des chiffres, pas des intuitions.

### Synthèse des Leviers d'Action

| Problème Identifié | Impact Business | Action Recommandée |
|---------------------|-----------------|-------------------|
| Baisse CA 2022-2023 | Perte de revenus, alerte stratégique | Analyse causes racines + plan d'action commercial urgent |
| Surstock 194% | Capital immobilisé (38%), coûts de stockage élevés | Réduction commandes + promotions ciblées |
| ROI promo 450% | Opportunité sous-exploitée | Stratégie pricing dynamique (prix base en baisse, promos en hausse) |
| Prix = concurrent | Manque de différenciation | Exploiter le levier promotionnel pour se démarquer |
| Écart prévisions 3,6% | Optimisation possible | Améliorer les modèles de forecast (ML) |

### Ce que ça m'a appris

La data dans le retail, c'est pas juste des chiffres et des dashboards. C'est comprendre des enjeux business concrets : marge, rotation des stocks, élasticité prix, saisonnalité. C'est transformer des lignes Excel en décisions stratégiques actionnables qui impactent directement le CA, les stocks, et la rentabilité.

Et c'est exactement ce qui me plaît dans la data.

---

## Installation

Si vous voulez reproduire le projet ou l'adapter, voici les étapes principales.

### Prérequis
- Docker et Docker Compose
- Un compte Google Cloud Platform (gratuit pour commencer)
- Python 3.8+
- Power BI Desktop pour la visualisation

### Configuration rapide

**1. Setup GCP**

Créer un projet et activer les APIs BigQuery et Cloud Storage :
```bash
gcloud projects create pipeline-etl-retail
gcloud services enable bigquery.googleapis.com storage.googleapis.com
```

Créer un service account avec les permissions nécessaires et télécharger la clé JSON.

**2. Lancer Airflow**

Cloner le repo et démarrer les conteneurs Docker :
```bash
git clone https://github.com/data164/data-engineering-retail-project.git
cd data-engineering-retail-project

# Placer la clé GCP dans config/gcp-key.json
docker-compose up -d
```

Interface Airflow accessible sur `http://localhost:8080` (login: airflow / airflow)

**3. Charger les données**

Uploader le fichier CSV dans Cloud Storage, puis créer la table dans BigQuery :
```sql
LOAD DATA INTO \`pipeline-etl-retail.retail_data_warehouse.raw_retail\`
FROM FILES (
  format = 'CSV',
  uris = ['gs://bucket-retailll/retail_store_data.csv'],
  skip_leading_rows = 1,
  field_delimiter = ';'
);
```

**4. Exécuter le pipeline**

Le DAG s'exécute automatiquement chaque jour, ou vous pouvez le trigger manuellement depuis l'interface Airflow.

---

## Requête SQL principale

La transformation agrège les données brutes pour créer une table de KPIs quotidiens. Voici la logique :

```sql
CREATE OR REPLACE TABLE \`pipeline-etl-retail.retail_data_warehouse.retail_daily_kpis\` AS
SELECT
    -- Dimensions pour le groupement
    Date,
    \`Store ID\` AS store_id,
    \`Product ID\` AS product_id,
    Category AS product_category,
    Region AS store_region,
    \`Weather Condition\` AS weather_condition,
    \`Holiday_Promotion\` AS holiday_promotion_status,
    Seasonality AS seasonality,

    -- Métriques de vente
    ROUND(SUM(\`Units Sold\`), 2) AS total_units_sold,
    ROUND(SUM(Price * \`Units Sold\`), 2) AS daily_revenue,

    -- Métriques de stock
    ROUND(AVG(\`Inventory Level\`), 2) AS average_inventory_level,
    ROUND(SUM(\`Units Ordered\`), 2) AS total_units_ordered,
    ROUND(AVG(\`Demand Forecast\`), 2) AS average_demand_forecast,

    -- Métriques de prix
    ROUND(AVG(Price), 2) AS average_product_price,
    ROUND(AVG(Discount), 2) AS average_discount_rate,
    ROUND(AVG(\`Competitor Pricing\`), 2) AS average_competitor_price

FROM \`pipeline-etl-retail.retail_data_warehouse.raw_retail\`
GROUP BY Date, \`Store ID\`, \`Product ID\`, Category, Region, 
         \`Weather Condition\`, \`Holiday_Promotion\`, Seasonality
ORDER BY Date, \`Store ID\`, \`Product ID\`;
```

Rien de complexe, mais ça permet d'avoir une table propre et agrégée pour alimenter Power BI.

---

## Mesures DAX (Power BI)

Quelques exemples de mesures calculées dans Power BI :

**Chiffre d'Affaires Total**
```dax
CA Total = 
ROUND(
    SUMX(retail_kpi_export, VALUE(SUBSTITUTE([daily_revenue], ".", ","))),
    0
)
```

**Marge Brute**
```dax
Marge Brute = [CA Total] - [Coût Promotions]
```

**ROI Promotions**
```dax
ROI Promotions = 
ROUND(
    VAR CATotal = SUMX(retail_kpi_export, VALUE(SUBSTITUTE([daily_revenue], ".", ",")))
    VAR CoutPromo = SUMX(retail_kpi_export, VALUE(SUBSTITUTE([total_discount_given], ".", ",")))
    RETURN DIVIDE(CATotal - CoutPromo, CoutPromo, 0) * 100,
    1
)
```

**Écart Prévisionnel**
```dax
Écart Prévisionnel % = 
VAR VentesReelles = SUMX(retail_kpi_export, VALUE(SUBSTITUTE([total_units_sold], ".", ",")))
VAR Previsions = SUMX(retail_kpi_export, VALUE(SUBSTITUTE([average_demand_forecast], ".", ",")))
VAR Ecart = ABS(VentesReelles - Previsions)
RETURN ROUND(DIVIDE(Ecart, Previsions, 0) * 100, 1)
```

J'ai dû utiliser SUBSTITUTE pour convertir les points en virgules (problème de format entre BigQuery et Power BI).

---

## Applications concrètes

Le pipeline permet de répondre à plusieurs questions business :

**Optimisation des promotions**  
Les promotions sont-elles rentables ? → ROI de 450% calculé automatiquement

**Gestion des stocks**  
Risque de rupture ou de surstock ? → Indicateur de couverture (194 jours) vs demande prévue

**Positionnement prix**  
Sommes-nous compétitifs ? → Comparaison automatique avec les prix concurrents par catégorie

**Analyse de performance**  
Quels produits/régions performent le mieux ? → Dashboards avec drill-down par catégorie et temporalité

---

## Améliorations possibles

Quelques idées pour aller plus loin (que je n'ai pas eu le temps d'implémenter) :

- Ajouter des tests automatisés pour vérifier la qualité des données
- Migrer vers Cloud Composer (Airflow managé sur GCP)
- Implémenter dbt pour mieux gérer les transformations SQL
- Ajouter des alertes Slack en cas d'anomalie ou d'échec du pipeline
- Créer des modèles de prévision ML pour améliorer la demande forecast

---

## Ce que j'ai appris

Ce projet m'a permis de comprendre concrètement :
- Comment orchestrer un pipeline avec Airflow (galères avec Docker et les connexions GCP incluses)
- L'architecture cloud moderne (Storage, Warehouse, IAM)
- L'importance de la qualité des données (les problèmes de format CSV m'ont fait perdre du temps)
- Comment connecter les différents outils entre eux (GCP, Airflow, Power BI)

Le plus dur n'était pas le code mais la config et l'intégration des différents services.

---

## Contact

**Mohamed Amhamed**  
Étudiant Ingénieur Data - CESI Lille (Bac+3)

Email : mohamed.amhamed@viacesi.fr  
LinkedIn : [linkedin.com/in/mohamed-amhamed](https://linkedin.com/in/mohamed-amhamed)  
GitHub : [github.com/data164](https://github.com/data164)

N'hésitez pas à me contacter pour discuter du projet ou échanger sur le data engineering !

---

*Projet réalisé en Octobre 2025 dans le cadre de mon apprentissage du data engineering*
