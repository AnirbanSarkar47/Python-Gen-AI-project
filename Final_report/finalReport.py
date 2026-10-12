
import pandas as pd
import logging
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent

input_file = PROJECT_DIR / "Report_generation" / "data_with_revenue.csv"
output_file = PROJECT_DIR / "Final_report" / "Sales_Analysis_Report.xlsx"
log_file = PROJECT_DIR / "sales_analysis.log"

logging.basicConfig(
    filename=str(log_file),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    force=True
)

logging.info("Final report generation started")



try:
    df = pd.read_csv(input_file)

    required_columns = [
        "Date", "Quantity", "Unit Price", "Order ID",
        "Region", "Product", "Salesperson"
    ]

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df["Date"] = pd.to_datetime(
        df["Date"], dayfirst=True, errors="coerce"
    )

    df = df.dropna(subset=["Date"])

    df["Revenue"] = df["Quantity"] * df["Unit Price"]

    logging.info("Sales data loaded and validated successfully")

except FileNotFoundError:
    logging.exception("Input sales CSV file not found")
    raise

except Exception:
    logging.exception("Failed to load or prepare sales data")
    raise

 
try:
    # 1. Regional summary
    region_summary = df.groupby("Region").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Total_Orders=("Order ID", "nunique")
    ).reset_index().sort_values(
        "Total_Revenue", ascending=False
    )

    # 2. Top 5 products
    top_products = df.groupby("Product").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Quantity=("Quantity", "sum")
    ).reset_index().sort_values(
        "Total_Revenue", ascending=False
    ).head(5)

    # 3. Top 5 salespersons
    top_salespersons = df.groupby("Salesperson").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Orders=("Order ID", "nunique")
    ).reset_index().sort_values(
        "Total_Revenue", ascending=False
    ).head(5)

    # 4. Daily totals
    daily_totals = df.groupby(df["Date"].dt.date).agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Total_Orders=("Order ID", "nunique")
    ).reset_index()

    daily_totals = daily_totals.rename(
        columns={"Date": "Day"}
    )

    # 5. Monthly totals
    df["Month"] = df["Date"].dt.to_period("M").astype(str)

    monthly_totals = df.groupby("Month").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Quantity=("Quantity", "sum"),
        Total_Orders=("Order ID", "nunique")
    ).reset_index()

    # 6. Overall summary
    overall_summary = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Quantity Sold",
            "Unique Orders"
        ],
        "Value": [
            df["Revenue"].sum(),
            df["Quantity"].sum(),
            df["Order ID"].nunique()
        ]
    })

    logging.info("All six summaries generated successfully")

except Exception:
    logging.exception("Summary calculations failed")
    raise


# Export all reports to one Excel file
try:
    with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
        overall_summary.to_excel(
            writer, sheet_name="Overall Summary", index=False
        )
        region_summary.to_excel(
            writer, sheet_name="Region Summary", index=False
        )
        top_products.to_excel(
            writer, sheet_name="Top Products", index=False
        )
        top_salespersons.to_excel(
            writer, sheet_name="Top Salespersons", index=False
        )
        daily_totals.to_excel(
            writer, sheet_name="Daily Totals", index=False
        )
        monthly_totals.to_excel(
            writer, sheet_name="Monthly Totals", index=False
        )

    logging.info("Excel report exported successfully: %s", output_file)

    print("Sales report exported successfully!")
    print("File:", output_file)

except Exception:
    logging.exception("Failed to export Excel report")
    raise

print("Sales report exported successfully!")
print("File:", output_file)