# Form 1040 (2024) Field Mapping Dictionary

FIELD_MAPPING = {
    # Personal Information Section
    "FirstName": "f1_01_0_firstname",
    "LastName": "f1_02_0_lastname",
    "SSN": "f1_03_0_ssn",
    "SpouseFirstName": "f1_04_0_spouse_firstname",
    "SpouseLastName": "f1_05_0_spouse_lastname",
    "SpouseSSN": "f1_06_0_spouse_ssn",

    # Address Section
    "Address": "f1_07_0_address",
    "AptNo": "f1_08_0_aptno",
    "City": "f1_09_0_city",
    "State": "f1_10_0_state",
    "ZipCode": "f1_11_0_zipcode",
    "ForeignCountry": "f1_12_0_foreign_country",
    "ForeignProvince": "f1_13_0_foreign_province",
    "ForeignPostalCode": "f1_14_0_foreign_postal_code",

    # Filing Status
    "FilingStatus": {
        "Single": "c1_01_0_single",
        "MarriedJointly": "c1_02_0_married_jointly",
        "MarriedSeparately": "c1_03_0_married_separately",
        "HeadOfHousehold": "c1_04_0_head_household",
        "QualifyingSurvivingSpouse": "c1_05_0_qualifying_surviving_spouse"
    },

    # Digital Assets
    "DigitalAssets": {
        "Yes": "c1_06_0_digital_assets_yes",
        "No": "c1_07_0_digital_assets_no"
    },

    # Dependents Section
    "Dependents": [
        {
            "FirstName": "f1_15_0_dependent1_firstname",
            "LastName": "f1_16_0_dependent1_lastname",
            "SSN": "f1_17_0_dependent1_ssn",
            "Relationship": "f1_18_0_dependent1_relationship",
            "ChildTaxCredit": "c1_08_0_dependent1_child_tax_credit",
            "OtherCredit": "c1_09_0_dependent1_other_credit"
        }
        # More dependents can be added similarly
    ],

    # Income Section
    "Income": {
        "TotalW2Wages": "f1_19_0_total_w2_wages",
        "HouseholdWages": "f1_20_0_household_wages",
        "TipIncome": "f1_21_0_tip_income",
        "MedicaidWaiver": "f1_22_0_medicaid_waiver",
        "DependentCareBenefits": "f1_23_0_dependent_care_benefits",
        "AdoptionBenefits": "f1_24_0_adoption_benefits",
        "WagesForm8919": "f1_25_0_wages_form_8919",
        "OtherEarnedIncome": "f1_26_0_other_earned_income"
    },

    # Other Income
    "OtherIncome": {
        "TaxExemptInterest": "f1_27_0_tax_exempt_interest",
        "TaxableInterest": "f1_28_0_taxable_interest",
        "QualifiedDividends": "f1_29_0_qualified_dividends",
        "OrdinaryDividends": "f1_30_0_ordinary_dividends"
    },

    # Payments and Withholding
    "Payments": {
        "FederalWithholdingW2": "f1_31_0_federal_withholding_w2",
        "FederalWithholding1099": "f1_32_0_federal_withholding_1099",
        "OtherWithholding": "f1_33_0_other_withholding",
        "EstimatedTaxPayments": "f1_34_0_estimated_tax_payments"
    },

    # Direct Deposit Information
    "DirectDeposit": {
        "RoutingNumber": "f1_35_0_routing_number",
        "AccountType": {
            "Checking": "c1_10_0_account_type_checking",
            "Savings": "c1_11_0_account_type_savings"
        },
        "AccountNumber": "f1_36_0_account_number"
    },

    # Signature Section
    "Signature": {
        "TaxpayerSignature": "f1_37_0_taxpayer_signature",
        "TaxpayerSignatureDate": "f1_38_0_taxpayer_date",
        "TaxpayerOccupation": "f1_39_0_taxpayer_occupation",
        "SpouseSignature": "f1_40_0_spouse_signature",
        "SpouseSignatureDate": "f1_41_0_spouse_date",
        "SpouseOccupation": "f1_42_0_spouse_occupation"
    },

    # Third-Party Designee
    "ThirdPartyDesignee": {
        "Name": "f1_43_0_third_party_name",
        "PhoneNumber": "f1_44_0_third_party_phone",
        "PIN": "f1_45_0_third_party_pin"
    }
}