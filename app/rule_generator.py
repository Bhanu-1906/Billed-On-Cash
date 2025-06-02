# import psycopg2
# import json
# from datetime import datetime
# from uuid import UUID
# from uuid import uuid4


# DB_CONFIG = {
#     'host': 'localhost',
#     'port': 5432,
#     'dbname': 'schemeengine1',
#     'user': 'postgres',
#     'password': '1234'
# }

# def fetch_data(query, params=None):
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor() as cur:
#             cur.execute(query, params)
#             colnames = [desc[0] for desc in cur.description]
#             return [dict(zip(colnames, row)) for row in cur.fetchall()]

# def store_json_in_db(scheme_id, json_data):
#     with psycopg2.connect(**DB_CONFIG) as conn:
#         with conn.cursor() as cur:
#             cur.execute("""
#                 INSERT INTO scheme_rule_json (id, scheme_id, rule_json, generated_at)
#                 VALUES (%s, %s, %s, %s)
#             """, (str(uuid4()), scheme_id, json.dumps(json_data), datetime.now()))
#         conn.commit()


# def generate_rule_json(scheme_id: UUID):
#     scheme = fetch_data("SELECT * FROM scheme WHERE scheme_id = %s", (str(scheme_id),))
#     if not scheme:
#         raise ValueError("Scheme not found!")
#     scheme = scheme[0]

#     conditions = []

#     for field in ['customer_category', 'region', 'customer_classification']:
#         if scheme.get(field):
#             conditions.append({
#                 "name": field,
#                 "operator": "equal_to",
#                 "value": scheme[field]
#             })

#     applicability = fetch_data("SELECT * FROM scheme_applicability WHERE scheme_id = %s", (str(scheme_id),))
#     for app in applicability:
#         conditions.append({
#             "name": app['criteria'],
#             "operator": "equal_to",
#             "value": app['value']
#         })

#     if scheme['scheme_template'] == 'billed_on_cash':
#         billed = fetch_data("SELECT * FROM scheme_billed_on_cash WHERE scheme_id = %s", (str(scheme_id),))
#         if billed:
#             billed = billed[0]
#             conditions.append({
#                 "name": "ptr_based",
#                 "operator": "equal_to",
#                 "value": billed['ptr_based']
#             })

#     actions = []

#     if scheme['promotion_type'] in ['flat', 'percent']:
#         fp = fetch_data("SELECT * FROM scheme_flat_percent WHERE scheme_id = %s", (str(scheme_id),))
#         if fp:
#             fp = fp[0]
#             action_type = "apply_discount"
#             param_key = "percentage" if fp['discount_type'] == 'percent' else "flat_value"

#             actions.append({
#                 "name": action_type,
#                 "params": {
#                     param_key: float(fp['discount_value']),
#                     "qualifying_value": float(fp['qualifying_value']),
#                     "basis": fp['basis_type'],
#                     "operator": fp['operator']
#                 }
#             })

#             conditions.append({
#                 "name": "purchase_" + fp['basis_type'],
#                 "operator": fp['operator'],
#                 "value": float(fp['qualifying_value'])
#             })

#     elif scheme['promotion_type'] == 'free_product':
#         free = fetch_data("SELECT * FROM scheme_free_product WHERE scheme_id = %s", (str(scheme_id),))
#         if free:
#             free = free[0]
#             actions.append({
#                 "name": "apply_free_product",
#                 "params": {
#                     "product_code": free['free_product_code'],
#                     "product_name": free['free_product_name'],
#                     "free_quantity": free['free_quantity']
#                 }
#             })

#             conditions.append({
#                 "name": "purchase_quantity",
#                 "operator": "greater_than_equal_to",
#                 "value": free['qualifying_quantity']
#             })

#     elif scheme['promotion_type'] == 'slab':
#         slabs = fetch_data("SELECT * FROM scheme_slab WHERE scheme_id = %s", (str(scheme_id),))
#         slab_actions = []
#         for slab in slabs:
#             slab_actions.append({
#                 "from": float(slab['from_value']),
#                 "to": float(slab['to_value']),
#                 "type": slab['discount_type'],
#                 "value": float(slab['discount_value']),
#                 "basis": slab['slab_basis']
#             })

#         actions.append({
#     "name": "apply_slab_discount",
#     "params": {
#         "slabs": json.dumps(slab_actions)  # <<< Convert list to JSON string
#     }
# })


#     rule_json = [{
#         "name": scheme['scheme_name'],
#         "conditions": {
#             "all": conditions
#         },
#         "actions": actions
#     }]

#     store_json_in_db(scheme_id, rule_json)
import psycopg2
import json
from datetime import datetime
from uuid import UUID, uuid4

DB_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'dbname': 'schemeengine1',
    'user': 'postgres',
    'password': '1234'
}

def fetch_data(query, params=None):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            colnames = [desc[0] for desc in cur.description]
            return [dict(zip(colnames, row)) for row in cur.fetchall()]

def store_json_in_db(scheme_id, json_data):
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO scheme_rule_json (id, scheme_id, rule_json, generated_at)
                VALUES (%s, %s, %s, %s)
            """, (str(uuid4()), scheme_id, json.dumps(json_data), datetime.now()))
        conn.commit()

# ✅ Map symbolic operator to text equivalent
def map_operator(op):
    return {
        '>=': 'greater_than_or_equal_to',
        '>': 'greater_than',
        '=': 'equal_to'
    }.get(op, op)  # fallback to original if unmapped

def generate_rule_json(scheme_id: UUID):
    scheme = fetch_data("SELECT * FROM scheme WHERE scheme_id = %s", (str(scheme_id),))
    if not scheme:
        raise ValueError("Scheme not found!")
    scheme = scheme[0]

    conditions = []

    for field in ['customer_category', 'region', 'customer_classification']:
        if scheme.get(field):
            conditions.append({
                "name": field,
                "operator": "equal_to",
                "value": scheme[field]
            })

    applicability = fetch_data("SELECT * FROM scheme_applicability WHERE scheme_id = %s", (str(scheme_id),))
    for app in applicability:
        conditions.append({
            "name": app['criteria'],
            "operator": "equal_to",
            "value": app['value']
        })

    # if scheme['scheme_template'] == 'billed_on_cash':
    #     billed = fetch_data("SELECT * FROM scheme_billed_on_cash WHERE scheme_id = %s", (str(scheme_id),))
    #     if billed:
    #         billed = billed[0]
    #         conditions.append({
    #             "name": "ptr_based",
    #             "operator": "equal_to",
    #             "value": billed['ptr_based']
    #         })

    actions = []

    if scheme['promotion_type'] in ['flat', 'percent']:
        fp = fetch_data("SELECT * FROM scheme_flat_percent WHERE scheme_id = %s", (str(scheme_id),))
        if fp:
            fp = fp[0]
            action_type = "apply_discount"
            param_key = "percentage" if fp['discount_type'] == 'percent' else "flat_value"
            text_operator = map_operator(fp['operator'])

            actions.append({
                "name": action_type,
                "params": {
                    param_key: float(fp['discount_value']),
                    "qualifying_value": float(fp['qualifying_value']),
                    "basis": fp['basis_type'],
                    "operator": text_operator
                }
            })

            conditions.append({
                "name": "purchase_" + fp['basis_type'],
                "operator": text_operator,
                "value": float(fp['qualifying_value'])
            })

    elif scheme['promotion_type'] == 'free_product':
        free = fetch_data("SELECT * FROM scheme_free_product WHERE scheme_id = %s", (str(scheme_id),))
        if free:
            free = free[0]
            actions.append({
                "name": "apply_free_product",
                "params": {
                    "product_code": free['free_product_code'],
                    "product_name": free['free_product_name'],
                    "free_quantity": free['free_quantity'],
                    "qualifying_value":free['qualifying_quantity']

                }
            })

            conditions.append({
                "name": "purchase_quantity",
                "operator": "greater_than_or_equal_to",  # already in text format
                "value": free['qualifying_quantity']
            })

    elif scheme['promotion_type'] == 'slab':
        slabs = fetch_data("SELECT * FROM scheme_slab WHERE scheme_id = %s", (str(scheme_id),))
        slab_actions = []
        for slab in slabs:
            slab_actions.append({
                "from": float(slab['from_value']),
                "to": float(slab['to_value']),
                "type": slab['discount_type'],
                "value": float(slab['discount_value']),
                "basis": slab['slab_basis']
            })

        actions.append({
            "name": "apply_slab_discount",
            "params": {
                "slabs": json.dumps(slab_actions)  # ✅ Convert list to string here
            }
        })


    rule_json = [{
        "name": scheme['scheme_name'],
        "conditions": {
            "all": conditions
        },
        "actions": actions
    }]

    store_json_in_db(scheme_id, rule_json)
