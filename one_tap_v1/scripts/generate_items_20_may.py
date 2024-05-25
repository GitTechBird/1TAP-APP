import copy

import frappe
from frappe import _
from frappe.utils import cstr, flt
import time

ACTIVITY_TYPES = [
    "General Trading",
    "Regular Trading",
    "Special Activity",
]
VISA_MIN = 0
VISA_MAX = 4
YEAR_MIN = 1
YEAR_MAX = 5

zone = {
    "0visa_1year": 1123,
    "0visa_2year": 1123,
    "0visa_3year": 0,
    "1visa_1year": 0,
    "1visa_2year": 1123,
    "1visa_3year": 0,
    "2visa_1year": 0,
}


# Create Template per
def create_template_1():
    # Get all zones
    zones = frappe.get_list("OT Zone Master", pluck="name")
    print(zones)
    for name in zones:
        zone = frappe.get_doc("OT Zone Master", name)
        # state info
        state = frappe.get_doc("OT State Master", {"state_name": zone.state_name})
        # country info
        country = frappe.get_doc("OT Country Master", {"country_name": state.country_name})
        country_code = country.country_code
        zone = zone.as_dict()
        for activity_type in ACTIVITY_TYPES:
            template_name = f"{country_code}_{zone['zone_code']}_CompanySetup_{activity_type}"
            # Update Attributes
            attribute_list = []
            visa_year_attr = frappe.get_doc(
                "Item Attribute", "OT Visa Years attributes"
            )
            visa_num_attr = frappe.get_doc(
                "Item Attribute", "OT Visa Number attributes"
            )

            for attr in [visa_num_attr, visa_year_attr]:
                attribute_list.append(
                    {
                        "attribute": attr.attribute_name,
                        "from_range": attr.from_range,
                        "to_range": attr.to_range,
                        "numeric_values": 1,
                        "increment": attr.increment,
                    }
                )

            # attribute_list.append({
            #     "attribute": "OT Visa Number attributes",
            #     "from_range": VISA_MIN,
            #     "to_range": VISA_MAX,
            #     "numeric_values": 1,
            #     "increment": 1
            # })
            # attribute_list.append({
            #     "attribute": "OT Visa Years attributes",
            #     "from_range": YEAR_MIN,
            #     "to_range": YEAR_MAX,
            #     "numeric_values": 1,
            #     "increment": 1
            # })

            # Create item template
            item_template_exists = frappe.db.exists("Item", template_name)
            print("item_tempplate-> ", template_name, "-->", item_template_exists)
            if not item_template_exists:
                frappe.get_doc(
                    {
                        "doctype": "Item",
                        "item_code": template_name,
                        "item_name": template_name,
                        "has_variants": 1,
                        "attributes": attribute_list,
                        "gst_hsn_code": 39269099,
                        "item_group": activity_type
                    }
                ).insert()

                # create variants
                for visa in range(VISA_MIN, VISA_MAX + 1):
                    for year in range(YEAR_MIN, YEAR_MAX + 1):
                        key = f"{visa}visa_{year}year"
                        if zone.get(key) and zone[key]:
                            attribute_values = {
                                "OT Visa Years attributes": str(year),
                                "OT Visa Number attributes": str(visa),
                            }
                            if not get_variant(template_name, args=attribute_values):
                                variant = create_variant(
                                    template_name, attribute_values
                                )
                                variant.save()
                # Create Item Price and update value for item_price
                create_and_update_item_price(template_name, zone["zone_name"], activity_type)
                frappe.db.commit()
                time.sleep(5)
    return "Item Generated Successfully"


def update_args(attr, args):
    attr_doc = frappe.get_doc("Item Attribute", {"attribute_name": attr.attribute})
    for i in range(int(attr_doc.from_range), int(attr_doc.to_range) + 1):
        if attr.attribute not in args:
            args[attr.attribute] = []
        args[attr.attribute].append(str(i))


def create_and_update_item_price(template_name, zone_name, activity_type):
    items = frappe.get_all(
        doctype="Item",
        filters={"variant_of": template_name},
        fields=["name", "item_name"],
    )
    for i in items:
        item = frappe.get_doc("Item", i.name)
        ## Getting the price of the item
        item_attributes = item.attributes
        visa = 0
        year = 1
        for attr in item_attributes:
            if attr.attribute == "OT Visa Number attributes":
                visa = attr.attribute_value
            if attr.attribute == "OT Visa Years attributes":
                year = attr.attribute_value

        filters = {"zone_name": zone_name}
        fieldname = f"{visa}visa_{year}year"
        if activity_type == 'General Trading':
            fieldname = fieldname + "_gt"
        item_zone = frappe.get_list(
            doctype="OT Zone Master", filters=filters, fields=[fieldname]
        )
        # return item_zone
        item_zone_price = 0
        if item_zone:
            temp = item_zone[0]
            item_zone_price = temp[list(temp.keys())[0]]
            item_zone_price = item_zone_price if item_zone_price else 0
        item_total_price = int(item_zone_price)

        # Creating new Item Price
        frappe.get_doc(
            {
                "doctype": "Item Price",
                "item_code": item.item_name,
                "item_name": item.item_name,
                "price_list_rate": item_total_price,
                "price_list": "Standard Selling",
            }
        ).insert()


# Frappe
def get_item_codes_by_attributes(attribute_filters, template_item_code=None):
    items = []

    for attribute, values in attribute_filters.items():
        attribute_values = values

        if not isinstance(attribute_values, list):
            attribute_values = [attribute_values]

        if not attribute_values:
            continue

        wheres = []
        query_values = []
        for attribute_value in attribute_values:
            wheres.append("( attribute = %s and attribute_value = %s )")
            query_values += [attribute, attribute_value]

        attribute_query = " or ".join(wheres)

        if template_item_code:
            variant_of_query = "AND t2.variant_of = %s"
            query_values.append(template_item_code)
        else:
            variant_of_query = ""

        query = """
                        SELECT
                                t1.parent
                        FROM
                                `tabItem Variant Attribute` t1
                        WHERE
                                1 = 1
                                AND (
                                        {attribute_query}
                                )
                                AND EXISTS (
                                        SELECT
                                                1
                                        FROM
                                                `tabItem` t2
                                        WHERE
                                                t2.name = t1.parent
                                                {variant_of_query}
                                )
                        GROUP BY
                                t1.parent
                        ORDER BY
                                NULL
                """.format(
            attribute_query=attribute_query, variant_of_query=variant_of_query
        )

        item_codes = set(
            [r[0] for r in frappe.db.sql(query, query_values)]
        )  # nosemgrep
        items.append(item_codes)

    res = list(set.intersection(*items))

    return res


def get_variant(
    template, args=None, variant=None, manufacturer=None, manufacturer_part_no=None
):
    """Validates Attributes and their Values, then looks for an exactly
    matching Item Variant

    :param item: Template Item
    :param args: A dictionary with "Attribute" as key and "Attribute Value" as value
    """
    item_template = frappe.get_doc("Item", template)

    if item_template.variant_based_on == "Manufacturer" and manufacturer:
        return make_variant_based_on_manufacturer(
            item_template, manufacturer, manufacturer_part_no
        )
    else:
        if isinstance(args, str):
            args = json.loads(args)

        if not args:
            frappe.throw(
                _("Please specify at least one attribute in the Attributes table")
            )
        return find_variant(template, args, variant)


def make_variant_based_on_manufacturer(template, manufacturer, manufacturer_part_no):
    """Make and return a new variant based on manufacturer and
    manufacturer part no"""
    from frappe.model.naming import append_number_if_name_exists

    variant = frappe.new_doc("Item")

    copy_attributes_to_variant(template, variant)

    variant.manufacturer = manufacturer
    variant.manufacturer_part_no = manufacturer_part_no

    variant.item_code = append_number_if_name_exists("Item", template.name)

    return variant


def validate_item_variant_attributes(item, args=None):
    if isinstance(item, str):
        item = frappe.get_doc("Item", item)

    if not args:
        args = {d.attribute.lower(): d.attribute_value for d in item.attributes}

    attribute_values, numeric_values = get_attribute_values(item)

    for attribute, value in args.items():
        if not value:
            continue

        if attribute.lower() in numeric_values:
            numeric_attribute = numeric_values[attribute.lower()]
            validate_is_incremental(numeric_attribute, attribute, value, item.name)

        else:
            attributes_list = attribute_values.get(attribute.lower(), [])
            validate_item_attribute_value(
                attributes_list, attribute, value, item.name, from_variant=True
            )


def validate_is_incremental(numeric_attribute, attribute, value, item):
    from_range = numeric_attribute.from_range
    to_range = numeric_attribute.to_range
    increment = numeric_attribute.increment

    if increment == 0:
        # defensive validation to prevent ZeroDivisionError
        frappe.throw(_("Increment for Attribute {0} cannot be 0").format(attribute))

    is_in_range = from_range <= flt(value) <= to_range
    precision = max(len(cstr(v).split(".")[-1].rstrip("0")) for v in (value, increment))
    # avoid precision error by rounding the remainder
    remainder = flt((flt(value) - from_range) % increment, precision)

    is_incremental = remainder == 0 or remainder == increment

    if not (is_in_range and is_incremental):
        frappe.throw(
            _(
                "Value for Attribute {0} must be within the range of {1} to {2} in the increments of {3} for Item {4}"
            ).format(attribute, from_range, to_range, increment, item),
            frappe.ValidationError,
            title=_("Invalid Attribute"),
        )


def validate_item_attribute_value(
    attributes_list, attribute, attribute_value, item, from_variant=True
):
    allow_rename_attribute_value = frappe.db.get_single_value(
        "Item Variant Settings", "allow_rename_attribute_value"
    )
    if allow_rename_attribute_value:
        pass
    elif attribute_value not in attributes_list:
        if from_variant:
            frappe.throw(
                _("{0} is not a valid Value for Attribute {1} of Item {2}.").format(
                    frappe.bold(attribute_value),
                    frappe.bold(attribute),
                    frappe.bold(item),
                ),
                frappe.ValidationError,
                title=_("Invalid Value"),
            )
        else:
            msg = _(
                "The value {0} is already assigned to an existing Item {1}."
            ).format(frappe.bold(attribute_value), frappe.bold(item))
            msg += "<br>" + _(
                "To still proceed with editing this Attribute Value, enable {0} in Item Variant Settings."
            ).format(frappe.bold("Allow Rename Attribute Value"))

            frappe.throw(msg, frappe.ValidationError, title=_("Edit Not Allowed"))


def get_attribute_values(item):
    if not frappe.flags.attribute_values:
        attribute_values = {}
        numeric_values = {}
        for t in frappe.get_all(
            "Item Attribute Value", fields=["parent", "attribute_value"]
        ):
            attribute_values.setdefault(t.parent.lower(), []).append(t.attribute_value)

        for t in frappe.get_all(
            "Item Variant Attribute",
            fields=["attribute", "from_range", "to_range", "increment"],
            filters={"numeric_values": 1, "parent": item.variant_of},
        ):
            numeric_values[t.attribute.lower()] = t

        frappe.flags.attribute_values = attribute_values
        frappe.flags.numeric_values = numeric_values

    return frappe.flags.attribute_values, frappe.flags.numeric_values


def find_variant(template, args, variant_item_code=None):
    conditions = [
        """(iv_attribute.attribute={0} and iv_attribute.attribute_value={1})""".format(
            frappe.db.escape(key), frappe.db.escape(cstr(value))
        )
        for key, value in args.items()
    ]

    conditions = " or ".join(conditions)

    # from erpnext.e_commerce.variant_selector.utils import get_item_codes_by_attributes

    possible_variants = [
        i
        for i in get_item_codes_by_attributes(args, template)
        if i != variant_item_code
    ]

    for variant in possible_variants:
        variant = frappe.get_doc("Item", variant)

        if len(args.keys()) == len(variant.get("attributes")):
            # has the same number of attributes and values
            # assuming no duplication as per the validation in Item
            match_count = 0

            for attribute, value in args.items():
                for row in variant.attributes:
                    if row.attribute == attribute and row.attribute_value == cstr(
                        value
                    ):
                        # this row matches
                        match_count += 1
                        break

            if match_count == len(args.keys()):
                return variant.name


def create_variant(item, args):
    if isinstance(args, str):
        args = json.loads(args)

    template = frappe.get_doc("Item", item)
    variant = frappe.new_doc("Item")
    variant.variant_based_on = "Item Attribute"
    variant_attributes = []

    for d in template.attributes:
        variant_attributes.append(
            {"attribute": d.attribute, "attribute_value": args.get(d.attribute)}
        )

    variant.set("attributes", variant_attributes)
    copy_attributes_to_variant(template, variant)
    make_variant_item_code(template.item_code, template.item_name, variant)

    return variant


def create_multiple_variants(item, args):
    count = 0
    if isinstance(args, str):
        args = json.loads(args)

    args_set = generate_keyed_value_combinations(args)

    for attribute_values in args_set:
        if not get_variant(item, args=attribute_values):
            variant = create_variant(item, attribute_values)
            print(vars(variant))
            variant.save()
            count += 1
    return count


def generate_keyed_value_combinations(args):
    """
    From this:

            args = {"attr1": ["a", "b", "c"], "attr2": ["1", "2"], "attr3": ["A"]}

    To this:

            [
                    {u'attr1': u'a', u'attr2': u'1', u'attr3': u'A'},
                    {u'attr1': u'b', u'attr2': u'1', u'attr3': u'A'},
                    {u'attr1': u'c', u'attr2': u'1', u'attr3': u'A'},
                    {u'attr1': u'a', u'attr2': u'2', u'attr3': u'A'},
                    {u'attr1': u'b', u'attr2': u'2', u'attr3': u'A'},
                    {u'attr1': u'c', u'attr2': u'2', u'attr3': u'A'}
            ]

    """
    # Return empty list if empty
    if not args:
        return []

    # Turn `args` into a list of lists of key-value tuples:
    # [
    #       [(u'attr2', u'1'), (u'attr2', u'2')],
    #       [(u'attr3', u'A')],
    #       [(u'attr1', u'a'), (u'attr1', u'b'), (u'attr1', u'c')]
    # ]
    key_value_lists = [[(key, val) for val in args[key]] for key in args.keys()]

    # Store the first, but as objects
    # [{u'attr2': u'1'}, {u'attr2': u'2'}]
    results = key_value_lists.pop(0)
    results = [{d[0]: d[1]} for d in results]

    # Iterate the remaining
    # Take the next list to fuse with existing results
    for l in key_value_lists:
        new_results = []
        for res in results:
            for key_val in l:
                # create a new clone of object in result
                obj = copy.deepcopy(res)
                # to be used with every incoming new value
                obj[key_val[0]] = key_val[1]
                # and pushed into new_results
                new_results.append(obj)
        results = new_results

    return results


def copy_attributes_to_variant(item, variant):
    # copy non no-copy fields

    exclude_fields = [
        "naming_series",
        "item_code",
        "item_name",
        "published_in_website",
        "opening_stock",
        "variant_of",
        "valuation_rate",
    ]

    if item.variant_based_on == "Manufacturer":
        # don't copy manufacturer values if based on part no
        exclude_fields += ["manufacturer", "manufacturer_part_no"]

    allow_fields = [
        d.field_name for d in frappe.get_all("Variant Field", fields=["field_name"])
    ]
    if "variant_based_on" not in allow_fields:
        allow_fields.append("variant_based_on")
    for field in item.meta.fields:
        # "Table" is part of `no_value_field` but we shouldn't ignore tables
        if (
            field.reqd or field.fieldname in allow_fields
        ) and field.fieldname not in exclude_fields:
            if variant.get(field.fieldname) != item.get(field.fieldname):
                if field.fieldtype == "Table":
                    variant.set(field.fieldname, [])
                    for d in item.get(field.fieldname):
                        row = copy.deepcopy(d)
                        if row.get("name"):
                            row.name = None
                        variant.append(field.fieldname, row)
                else:
                    variant.set(field.fieldname, item.get(field.fieldname))

    variant.variant_of = item.name

    if "description" not in allow_fields:
        if not variant.description:
            variant.description = ""
    else:
        if item.variant_based_on == "Item Attribute":
            if variant.attributes:
                attributes_description = item.description + " "
                for d in variant.attributes:
                    attributes_description += (
                        "<div>"
                        + d.attribute
                        + ": "
                        + cstr(d.attribute_value)
                        + "</div>"
                    )

                if attributes_description not in variant.description:
                    variant.description = attributes_description


def make_variant_item_code(template_item_code, template_item_name, variant):
    """Uses template's item code and abbreviations to make variant's item code"""
    if variant.item_code:
        return

    abbreviations = []
    for attr in variant.attributes:
        item_attribute = frappe.db.sql(
            """select i.numeric_values, v.abbr
                        from `tabItem Attribute` i left join `tabItem Attribute Value` v
                                on (i.name=v.parent)
                        where i.name=%(attribute)s and (v.attribute_value=%(attribute_value)s or i.numeric_values = 1)""",
            {"attribute": attr.attribute, "attribute_value": attr.attribute_value},
            as_dict=True,
        )

        if not item_attribute:
            continue
            # frappe.throw(_('Invalid attribute {0} {1}').format(frappe.bold(attr.attribute),
            #       frappe.bold(attr.attribute_value)), title=_('Invalid Attribute'),
            #       exc=InvalidItemAttributeValueError)

        abbr_or_value = (
            cstr(attr.attribute_value)
            if item_attribute[0].numeric_values
            else item_attribute[0].abbr
        )
        abbreviations.append(abbr_or_value)

    if abbreviations:
        variant.item_code = "{0}-{1}".format(
            template_item_code, "-".join(abbreviations)
        )
        variant.item_name = "{0}-{1}".format(
            template_item_name, "-".join(abbreviations)
        )


def create_variant_doc_for_quick_entry(template, args):
    variant_based_on = frappe.db.get_value("Item", template, "variant_based_on")
    args = json.loads(args)
    if variant_based_on == "Manufacturer":
        variant = get_variant(template, **args)
    else:
        existing_variant = get_variant(template, args)
        if existing_variant:
            return existing_variant
        else:
            variant = create_variant(template, args=args)
            variant.name = variant.item_code
            validate_item_variant_attributes(variant, args)
    return variant.as_dict()


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#


# def create_activity_items(a, b):
# @frappe.whitelist()
# def create_activity_items():
def create_activity_items(a, b):
    # return "Hello 1tap"
    return create_template_1()
    # return [a, b]


@frappe.whitelist()
def temp():
    return "hello"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
