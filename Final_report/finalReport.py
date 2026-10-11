import pandas as pd

# Load cleaned dataset
df = pd.read_csv("C:\\Users\\Admin\\Desktop\\Final Project\\Report_generation\\data_with_revenue.csv")

# Convert Date column
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")

# Calculate revenue
df["Revenue"] = df["Quantity"] * df["Unit Price"]

# 1. Regional summary
region_summary = df.groupby("Region").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Total_Orders=("Order ID", "nunique")
).reset_index().sort_values("Total_Revenue", ascending=False)

# 2. Top 5 products by revenue
top_products = df.groupby("Product").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Quantity=("Quantity", "sum")
).reset_index().sort_values("Total_Revenue", ascending=False).head(5)

# 3. Top 5 salespersons by revenue
top_salespersons = df.groupby("Salesperson").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Orders=("Order ID", "nunique")
).reset_index().sort_values("Total_Revenue", ascending=False).head(5)

# 4. Daily totals
daily_totals = df.groupby(df["Date"].dt.date).agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Total_Orders=("Order ID", "nunique")
).reset_index()
daily_totals = daily_totals.rename(columns={"Date": "Day"})

# 5. Monthly totals
df["Month"] = df["Date"].dt.to_period("M").astype(str)

monthly_totals = df.groupby("Month").agg(
    Total_Revenue=("Revenue", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Total_Orders=("Order ID", "nunique")
).reset_index()

# 6. Overall summary
overall_summary = pd.DataFrame({
    "Metric": ["Total Revenue", "Total Quantity Sold", "Unique Orders"],
    "Value": [
        df["Revenue"].sum(),
        df["Quantity"].sum(),
        df["Order ID"].nunique()
    ]
})

# Export all reports to one Excel file
with pd.ExcelWriter("Sales_Analysis_Report.xlsx", engine="openpyxl") as writer:
    overall_summary.to_excel(writer, sheet_name="Overall Summary", index=False)
    region_summary.to_excel(writer, sheet_name="Region Summary", index=False)
    top_products.to_excel(writer, sheet_name="Top Products", index=False)
    top_salespersons.to_excel(writer, sheet_name="Top Salespersons", index=False)
    daily_totals.to_excel(writer, sheet_name="Daily Totals", index=False)
    monthly_totals.to_excel(writer, sheet_name="Monthly Totals", index=False)

print("Sales report exported successfully!")
print("File: Sales_Analysis_Report.xlsx")