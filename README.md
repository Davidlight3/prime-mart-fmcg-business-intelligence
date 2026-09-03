# PrimeMart FMCG Business Intelligence

<p align="center">
  <strong>End-to-End FMCG Business Intelligence & Analytics Solution</strong>
</p>

<p align="center">
  Python • SQL Server • Power BI • DAX • Data Warehousing • Business Intelligence
</p>

---

## 📌 Project Overview

PrimeMart FMCG Business Intelligence is an end-to-end Business Intelligence project designed to demonstrate how transactional FMCG data can be transformed into a structured analytical solution for commercial and operational decision-making.

The project simulates a multi-store FMCG business operating across Nigerian markets and covers the complete analytics lifecycle:

**Data Generation → Data Preparation → Data Warehouse → Data Validation → Analytical Modeling → DAX → Power BI → Business Insights**

The solution integrates:

- Sales analytics
- Profitability analysis
- Customer analytics
- Product performance
- Inventory management
- Procurement analysis
- Supplier analysis
- Store performance
- Geographic performance
- Time-based performance analysis

The project was built using **Python for data generation and preparation, SQL Server for data warehousing and relational modeling, and Power BI for analytical modeling, visualization and business intelligence reporting.**

---

# 🎯 Business Problem

A growing FMCG organization generates large volumes of transactional data across stores, products, customers, employees, suppliers and procurement activities.

Without an integrated Business Intelligence solution, management may struggle to answer critical questions such as:

- Which stores generate the most revenue and profit?
- Which products and categories drive business performance?
- How is profitability changing over time?
- Which customer segments contribute the most value?
- Where is inventory becoming excessive?
- How much capital is tied up in inventory?
- How much is being spent on procurement?
- Which suppliers have longer lead times?
- Which stores are outperforming or underperforming?
- What products require closer inventory monitoring?
- How can management improve revenue, margin and operational efficiency?

PrimeMart FMCG Business Intelligence was designed to address these questions through an integrated analytical data model and interactive Power BI reporting environment.

---

# 💡 Project Objectives

The primary objectives of the project were to:

1. Build a realistic synthetic FMCG dataset at enterprise scale.
2. Develop a structured relational data warehouse using SQL Server.
3. Implement dimensional modeling suitable for Business Intelligence.
4. Establish primary-key and foreign-key relationships across the warehouse.
5. Validate data integrity and relationships.
6. Develop reusable Python data-generation utilities and business rules.
7. Create analytical measures using DAX.
8. Build an interactive Power BI semantic model.
9. Develop management-focused dashboards.
10. Translate analytical results into actionable business insights.
11. Demonstrate an end-to-end BI development workflow suitable for enterprise analytics environments.

---

# 🏗️ Solution Architecture

The project follows a layered Business Intelligence architecture:

```text
                         ┌──────────────────────┐
                         │   Synthetic Data     │
                         │      Generation      │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │       Python         │
                         │ Data Generation &    │
                         │ Business Rules       │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     SQL Server       │
                         │    Data Warehouse    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Dimensional Model    │
                         │                      │
                         │ Dimensions + Facts   │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │      Power BI        │
                         │ Semantic Model + DAX │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Business Intelligence│
                         │ Dashboards & Insights │
                         └──────────────────────┘
