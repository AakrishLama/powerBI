CREATE TABLE [gold].[dim_customer] (
    [CustomerKey]    INT             NULL,
    [FirstName]      VARCHAR (8000)  NULL,
    [LastName]       VARCHAR (8000)  NULL,
    [FullName]       VARCHAR (8000)  NULL,
    [BirthDate]      DATE            NULL,
    [MaritalStatus]  VARCHAR (8000)  NULL,
    [Gender]         VARCHAR (8000)  NULL,
    [EmailAddress]   VARCHAR (8000)  NULL,
    [AnnualIncome]   DECIMAL (18, 2) NULL,
    [TotalChildren]  INT             NULL,
    [EducationLevel] VARCHAR (8000)  NULL,
    [Occupation]     VARCHAR (8000)  NULL,
    [HomeOwner]      VARCHAR (8000)  NULL
);


GO