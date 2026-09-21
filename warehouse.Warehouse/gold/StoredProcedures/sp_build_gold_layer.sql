CREATE   PROCEDURE gold.sp_build_gold_layer
AS
BEGIN
    -- 1. Ensure the gold schema exists
    IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'gold')
    BEGIN
        EXEC('CREATE SCHEMA gold')
    END

    -- 2. Drop existing Gold tables if they exist
    DROP TABLE IF EXISTS gold.fact_sales;
    DROP TABLE IF EXISTS gold.dim_customer;
    DROP TABLE IF EXISTS gold.dim_territory;
    DROP TABLE IF EXISTS gold.dim_product;
    DROP TABLE IF EXISTS gold.dim_date;

    -- 3. Build Customer Dimension
    SELECT 
        CustomerKey,
        FirstName,
        LastName,
        FullName,
        BirthDate,
        MaritalStatus,
        Gender,
        EmailAddress,
        AnnualIncome,
        TotalChildren,
        EducationLevel,
        Occupation,
        HomeOwner
    INTO gold.dim_customer
    FROM silver.customers;

    -- 4. Build Territory Dimension
    SELECT 
        SalesTerritoryKey,
        Region,
        Country,
        Continent
    INTO gold.dim_territory
    FROM silver.adventureworks_territories;

    -- 5. Build Product Dimension
    SELECT 
        p.ProductKey,
        p.ProductSKU,
        p.ProductName,
        p.ModelName,
        p.ProductDescription,
        p.ProductColor,
        p.ProductSize,
        p.ProductStyle,
        p.ProductCost,
        p.ProductPrice,
        sc.SubcategoryName,
        c.CategoryName
    INTO gold.dim_product
    FROM silver.products p
    LEFT JOIN silver.product_subcategories sc ON p.ProductSubcategoryKey = sc.ProductSubcategoryKey
    LEFT JOIN silver.product_categories c ON sc.ProductCategoryKey = c.ProductCategoryKey;

    -- 6. Build Calendar Dimension
    SELECT DISTINCT
        CAST([Date] AS DATE) AS DateKey,
        YEAR(CAST([Date] AS DATE)) AS [Year],
        MONTH(CAST([Date] AS DATE)) AS [Month],
        DAY(CAST([Date] AS DATE)) AS [Day]
    INTO gold.dim_date
    FROM silver.adventureworks_calendar
    WHERE [Date] IS NOT NULL;

    -- 7. Build Fact Sales Table
    SELECT 
        CAST(OrderDate AS DATE) AS OrderDateKey,
        CAST(StockDate AS DATE) AS StockDateKey,
        OrderNumber,
        ProductKey,
        CustomerKey,
        TerritoryKey,
        OrderLineItem,
        OrderQuantity
    INTO gold.fact_sales
    FROM silver.adventureworks_sales_2016

    UNION ALL

    SELECT 
        CAST(OrderDate AS DATE) AS OrderDateKey,
        CAST(StockDate AS DATE) AS StockDateKey,
        OrderNumber,
        ProductKey,
        CustomerKey,
        TerritoryKey,
        OrderLineItem,
        OrderQuantity
    FROM silver.adventureworks_sales_2017;
END

GO