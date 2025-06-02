# import json
# import os
# from business_rules.engine import run_all
# from business_rules.variables import BaseVariables, string_rule_variable, boolean_rule_variable, numeric_rule_variable
# from business_rules.actions import BaseActions, rule_action
# from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC

# class CustomerVariables(BaseVariables):
#     def __init__(self, customer):
#         self.customer = customer

#     @string_rule_variable(label="Customer Category")
#     def customer_category(self):
#         return self.customer.get("customer_category", "")

#     @string_rule_variable(label="Region")
#     def region(self):
#         return self.customer.get("region", "")

#     @string_rule_variable(label="Customer Classification")
#     def customer_classification(self):
#         return self.customer.get("customer_classification", "")

#     @string_rule_variable(label="Brand")
#     def brand(self):
#         return self.customer.get("brand", "")

#     @string_rule_variable(label="Category")
#     def category(self):
#         return self.customer.get("category", "")

#     @numeric_rule_variable(label="Purchase Value")
#     def purchase_value(self):
#         return self.customer.get("purchase_value", 0)

#     @numeric_rule_variable(label="Purchase Quantity")
#     def purchase_quantity(self):
#         return self.customer.get("purchase_quantity", 0)


# class CustomerActions(BaseActions):
#     def __init__(self, customer):
#         self.customer = customer

   
#     @rule_action(params={
#         "percentage": FIELD_NUMERIC,
#         "qualifying_value": FIELD_NUMERIC,
#         "basis": FIELD_TEXT,
#         "operator": FIELD_TEXT
#     })
#     def apply_discount(self, percentage, qualifying_value, basis, operator):
#         purchase_value = self.customer.get("purchase_value", 0)
#         if basis == "value" and operator == "greater_than_or_equal_to" or operator=="greater_than" and purchase_value >= qualifying_value:
#             discount_amount = purchase_value * (percentage / 100)
#             discounted_price = round(purchase_value - discount_amount, 2)
#             self.customer["flat_discount"] = {
#                 "percentage": percentage,
#                 "discount_amount": discount_amount,
#                 "discounted_price": discounted_price
#             }


#     @rule_action(params={
#         "product_code": FIELD_TEXT,
#         "product_name": FIELD_TEXT,
#         "qualifying_value": FIELD_NUMERIC,
#         "free_quantity": FIELD_NUMERIC
#     })
#     def apply_free_product(self, product_code, product_name,qualifying_value,free_quantity):
#         purchase_qty = self.customer.get("purchase_quantity", 0)
#         multiplier = purchase_qty // qualifying_value
#         total_free = int(multiplier * free_quantity)

#         self.customer["free_product"] = {
#             "code": product_code,
#             "name": product_name,
#             "quantity": total_free
#         }

   
#     @rule_action(params={"slabs": FIELD_TEXT})
#     def apply_slab_discount(self, slabs):
#         try:
#             parsed_slabs = json.loads(slabs)
#         except json.JSONDecodeError:
#             self.customer["slab_discount"] = "Invalid slab format"
#             return

#         value = self.customer.get("purchase_value", 0)

#         for slab in parsed_slabs:
#             slab_from = slab.get("from", 0)
#             slab_to = slab.get("to", float("inf"))
#             discount_value = slab.get("value", 0)
#             discount_type = slab.get("type", "flat")

#             if slab_from <= value <= slab_to:
#                 final_amount = value - discount_value if discount_type == "flat" else value
#                 self.customer["slab_discount"] = {
#                     "type": discount_type,
#                     "value": discount_value,
#                     "slab": f"{slab_from} - {slab_to}",
#                     "final_amount": final_amount
#                 }
#                 break

# def load_all_rules(rule_folder):
#     rules = []
#     for filename in os.listdir(rule_folder):
#         if filename.endswith(".json"):
#             with open(os.path.join(rule_folder, filename), "r") as f:
#                 rule_data = json.load(f)
#                 if isinstance(rule_data, dict):  # single rule
#                     rules.append(rule_data)
#                 elif isinstance(rule_data, list):  # multiple rules
#                     rules.extend(rule_data)
#     return rules


# if __name__ == "__main__":
#     customer_data = {
#   "customer_category": "Retailer",
#   "region": "North",
#   "customer_classification": "red",
#   "brand":"Sleepz",
#   "purchase_quantity":6

# }

#     rules = load_all_rules(r"D:\Billed on Cash\app\rules")
#     print(rules)

#     run_all(
#         rule_list=rules,
#         defined_variables=CustomerVariables(customer_data),
#         defined_actions=CustomerActions(customer_data),
#         stop_on_first_trigger=False
#     )

#     print(json.dumps(customer_data, indent=2))
import json
from business_rules.engine import run_all
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_TEXT, FIELD_NUMERIC

from sqlalchemy.orm import Session
from .models import SchemeRuleJson



class CustomerVariables(BaseVariables):
    def __init__(self, customer: dict):
        self.customer = customer

    @string_rule_variable(label="Customer Category")
    def customer_category(self):
        return self.customer.get("customer_category", "")

    @string_rule_variable(label="Region")
    def region(self):
        return self.customer.get("region", "")

    @string_rule_variable(label="Customer Classification")
    def customer_classification(self):
        return self.customer.get("customer_classification", "")

    @string_rule_variable(label="Brand")
    def brand(self):
        return self.customer.get("brand", "")

    @string_rule_variable(label="Category")
    def category(self):
        return self.customer.get("category", "")

    @numeric_rule_variable(label="Purchase Value")
    def purchase_value(self):
        return self.customer.get("purchase_value", 0)

    @numeric_rule_variable(label="Purchase Quantity")
    def purchase_quantity(self):
        return self.customer.get("purchase_quantity", 0)



class CustomerActions(BaseActions):
    def __init__(self, customer: dict):
        self.customer = customer

    @rule_action(params={
        "percentage": FIELD_NUMERIC,
        "qualifying_value": FIELD_NUMERIC,
        "basis": FIELD_TEXT,
        "operator": FIELD_TEXT
    })
    def apply_discount(self, percentage, qualifying_value, basis, operator):
        purchase_value = self.customer.get("purchase_value", 0)
        if basis == "value" and operator == "greater_than_or_equal_to" or operator=="greater_than" and purchase_value >= qualifying_value:
            discount_amount = purchase_value * (percentage / 100)
            discounted_price = round(purchase_value - discount_amount, 2)
            self.customer["flat_discount"] = {
                "percentage": percentage,
                "discount_amount": discount_amount,
                "discounted_price": discounted_price
            }

    @rule_action(params={
        "product_code": FIELD_TEXT,
        "product_name": FIELD_TEXT,
        "qualifying_value": FIELD_NUMERIC,
        "free_quantity": FIELD_NUMERIC
    })
    def apply_free_product(self, product_code, product_name,qualifying_value,free_quantity):
        purchase_qty = self.customer.get("purchase_quantity", 0)
        multiplier = purchase_qty // qualifying_value
        total_free = int(multiplier * free_quantity)

        self.customer["free_product"] = {
            "code": product_code,
            "name": product_name,
            "quantity": total_free
        }


    @rule_action(params={"slabs": FIELD_TEXT})
    def apply_slab_discount(self, slabs):
        try:
            parsed_slabs = json.loads(slabs)
        except json.JSONDecodeError:
            self.customer["slab_discount"] = "Invalid slab format"
            return

        value = self.customer.get("purchase_value", 0)

        for slab in parsed_slabs:
            slab_from = slab.get("from", 0)
            slab_to = slab.get("to", float("inf"))
            discount_value = slab.get("value", 0)
            discount_type = slab.get("type", "flat")

            if slab_from <= value <= slab_to:
                final_amount = value - discount_value if discount_type == "flat" else value
                self.customer["slab_discount"] = {
                    "type": discount_type,
                    "value": discount_value,
                    "slab": f"{slab_from} - {slab_to}",
                    "final_amount": final_amount
                }
                break

def load_all_rules_from_db(db: Session):
    rules = []
    db_rules = db.query(SchemeRuleJson).all()
    for rule_row in db_rules:
        rule_data = rule_row.rule_json
        if isinstance(rule_data, dict):  # single rule
            rules.append(rule_data)
        elif isinstance(rule_data, list):  # multiple rules
            rules.extend(rule_data)
    return rules


def evaluate_rules_from_db(customer_data: dict, db: Session):
    rules = load_all_rules_from_db(db)
    print(rules)
    run_all(
        rule_list=rules,
        defined_variables=CustomerVariables(customer_data),
        defined_actions=CustomerActions(customer_data),
        stop_on_first_trigger=False
    )
    print(customer_data)
    return customer_data
