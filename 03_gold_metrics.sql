-- RetailPulse — Gold business metrics
-- Run in a Databricks SQL cell after the Silver table exists.
CREATE OR REPLACE TABLE workspace.retailpulse.gold_order_status_summary
USING DELTA
AS
SELECT
    order_status,
    COUNT(*) AS order_count,
    ROUND(
      100.0 * COUNT(*) / SUM(COUNT(*)) OVER (),
      2
    ) AS pct_of_orders
FROM workspace.retailpulse.orders_silver
GROUP BY order_status;

SELECT * FROM workspace.retailpulse.gold_order_status_summary
ORDER BY order_count DESC;
