def check_eligibility(scheme_key, answers):
    if scheme_key == "pm_kisan":
        # Must answer haan to these
        required_yes = ["is_farmer", "owns_land", "has_aadhaar", "has_bank"]
        # Must answer nahi to these
        required_no = ["is_govt_employee", "pays_income_tax"]

        for key in required_yes:
            if answers.get(key, "").lower() not in ["haan", "yes", "ha", "han"]:
                return False, f"Sorry, PM-KISAN ke liye {key} hona zaroori hai."

        for key in required_no:
            if answers.get(key, "").lower() in ["haan", "yes", "ha", "han"]:
                return False, "Sorry, government employees aur income tax payers PM-KISAN ke liye eligible nahi hain."

        return True, "Congratulations! Aap PM-KISAN ke liye ELIGIBLE hain! Apply karein: https://pmkisan.gov.in"

    return False, "Scheme not found."