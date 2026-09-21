CREATE TABLE [gold].[fact_sales] (
    [OrderDateKey]  DATE           NULL,
    [StockDateKey]  DATE           NULL,
    [OrderNumber]   VARCHAR (8000) NULL,
    [ProductKey]    INT            NULL,
    [CustomerKey]   INT            NULL,
    [TerritoryKey]  INT            NULL,
    [OrderLineItem] INT            NULL,
    [OrderQuantity] INT            NULL
);


GO