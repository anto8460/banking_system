BEGIN;
--
-- Create model Account
--
CREATE TABLE "accounts" ("id" uuid NOT NULL PRIMARY KEY, "account_number" varchar(255) NOT NULL UNIQUE, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NULL);
--
-- Create model AccountType
--
CREATE TABLE "account_types" ("id" uuid NOT NULL PRIMARY KEY, "type" varchar(255) NOT NULL UNIQUE, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NULL);
--
-- Create model Customer
--
CREATE TABLE "customers" ("id" uuid NOT NULL PRIMARY KEY, "first_name" varchar(255) NOT NULL, "last_name" varchar(255) NOT NULL, "email" varchar(255) NOT NULL UNIQUE, "cpr" varchar(10) NOT NULL UNIQUE, "age" integer NOT NULL, "phone_number" varchar(255) NOT NULL UNIQUE, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "user_id" integer NOT NULL UNIQUE);
--
-- Create model Transaction
--
CREATE TABLE "transactions" ("id" uuid NOT NULL PRIMARY KEY, "amount" double precision NOT NULL, "text" varchar(255) NULL, "created_at" timestamp with time zone NOT NULL);
--
-- Create model Loan
--
CREATE TABLE "loans" ("id" uuid NOT NULL PRIMARY KEY, "amount" double precision NOT NULL, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "customer_id" uuid NOT NULL);
--
-- Create model Employee
--
CREATE TABLE "employees" ("id" uuid NOT NULL PRIMARY KEY, "first_name" varchar(255) NOT NULL, "last_name" varchar(255) NOT NULL, "email" varchar(255) NOT NULL UNIQUE, "cpr" varchar(8) NOT NULL UNIQUE, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NOT NULL, "user_id" integer NOT NULL);
--
-- Create model BankDetail
--
CREATE TABLE "bank_details" ("id" uuid NOT NULL PRIMARY KEY, "created_at" timestamp with time zone NOT NULL, "updated_at" timestamp with time zone NULL, "account_id" uuid NOT NULL);
--
-- Add field account_type to account
--
ALTER TABLE "accounts" ADD COLUMN "account_type_id" uuid NOT NULL CONSTRAINT "accounts_account_type_id_d18011b4_fk_account_types_id" REFERENCES "account_types"("id") DEFERRABLE INITIALLY DEFERRED; SET CONSTRAINTS "accounts_account_type_id_d18011b4_fk_account_types_id" IMMEDIATE;
--
-- Add field customer to account
--
ALTER TABLE "accounts" ADD COLUMN "customer_id" uuid NOT NULL CONSTRAINT "accounts_customer_id_0ee1e998_fk_customers_id" REFERENCES "customers"("id") DEFERRABLE INITIALLY DEFERRED; SET CONSTRAINTS "accounts_customer_id_0ee1e998_fk_customers_id" IMMEDIATE;
--
-- Create model AccountsTransaction
--
CREATE TABLE "accounts_transactions" ("account_id" uuid NOT NULL PRIMARY KEY, "transaction_id" uuid NOT NULL);
CREATE INDEX "accounts_account_number_06de8a0d_like" ON "accounts" ("account_number" varchar_pattern_ops);
CREATE INDEX "account_types_type_1e67ae0a_like" ON "account_types" ("type" varchar_pattern_ops);
ALTER TABLE "customers" ADD CONSTRAINT "customers_user_id_28f6c6eb_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "customers_email_af8f39bb_like" ON "customers" ("email" varchar_pattern_ops);
CREATE INDEX "customers_cpr_9a1ceafb_like" ON "customers" ("cpr" varchar_pattern_ops);
CREATE INDEX "customers_phone_number_1e2e2966_like" ON "customers" ("phone_number" varchar_pattern_ops);
ALTER TABLE "loans" ADD CONSTRAINT "loans_customer_id_15c08565_fk_customers_id" FOREIGN KEY ("customer_id") REFERENCES "customers" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "loans_customer_id_15c08565" ON "loans" ("customer_id");
ALTER TABLE "employees" ADD CONSTRAINT "employees_user_id_c7f7a3f4_fk_auth_user_id" FOREIGN KEY ("user_id") REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "employees_email_c3f945b9_like" ON "employees" ("email" varchar_pattern_ops);
CREATE INDEX "employees_cpr_b43a7a0f_like" ON "employees" ("cpr" varchar_pattern_ops);
CREATE INDEX "employees_user_id_c7f7a3f4" ON "employees" ("user_id");
ALTER TABLE "bank_details" ADD CONSTRAINT "bank_details_account_id_2319cb0c_fk_accounts_id" FOREIGN KEY ("account_id") REFERENCES "accounts" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "bank_details_account_id_2319cb0c" ON "bank_details" ("account_id");
CREATE INDEX "accounts_account_type_id_d18011b4" ON "accounts" ("account_type_id");
CREATE INDEX "accounts_customer_id_0ee1e998" ON "accounts" ("customer_id");
ALTER TABLE "accounts_transactions" ADD CONSTRAINT "accounts_transactions_account_id_transaction_id_346d40e8_uniq" UNIQUE ("account_id", "transaction_id");
ALTER TABLE "accounts_transactions" ADD CONSTRAINT "accounts_transactions_account_id_b113aa36_fk_accounts_id" FOREIGN KEY ("account_id") REFERENCES "accounts" ("id") DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "accounts_transactions" ADD CONSTRAINT "accounts_transaction_transaction_id_3e075232_fk_transacti" FOREIGN KEY ("transaction_id") REFERENCES "transactions" ("id") DEFERRABLE INITIALLY DEFERRED;
CREATE INDEX "accounts_transactions_transaction_id_3e075232" ON "accounts_transactions" ("transaction_id");
COMMIT;