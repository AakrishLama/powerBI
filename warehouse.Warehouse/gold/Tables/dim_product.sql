CREATE TABLE [gold].[dim_product] (
    [ProductKey]         INT            NULL,
    [ProductSKU]         VARCHAR (8000) NULL,
    [ProductName]        VARCHAR (8000) NULL,
    [ModelName]          VARCHAR (8000) NULL,
    [ProductDescription] VARCHAR (8000) NULL,
    [ProductColor]       VARCHAR (8000) NULL,
    [ProductSize]        VARCHAR (8000) NULL,
    [ProductStyle]       VARCHAR (8000) NULL,
    [ProductCost]        FLOAT (53)     NULL,
    [ProductPrice]       FLOAT (53)     NULL,
    [SubcategoryName]    VARCHAR (8000) NULL,
    [CategoryName]       VARCHAR (8000) NULL
);


GO