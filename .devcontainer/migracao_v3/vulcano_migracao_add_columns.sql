
ALTER TABLE invoices
  ADD COLUMN balance decimal(10,2) DEFAULT 0 AFTER amount_to_pay,
  ADD COLUMN invoiced decimal(10,2) DEFAULT 0 NULL AFTER pap;
