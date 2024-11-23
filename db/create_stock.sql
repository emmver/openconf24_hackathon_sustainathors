CREATE TABLE `sustainathors_database.Stock` AS
SELECT
  ItemID,
  UserID,
  ItemDetailID,
  ItemName,
  Category,
  DATE_ADD(BoughtDate, INTERVAL 21 DAY) AS BoughtDate, -- Add 21 days to BoughtDate
  DATE_ADD(ExpirationDate, INTERVAL 21 DAY) AS ExpirationDate, -- Add 21 days to ExpirationDate
  UsedBeforeExpiry
FROM `sustainathors_database.Items`;
