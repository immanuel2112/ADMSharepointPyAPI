import sys

from adm.sp.adm_sp_models import ADMSharepointValue


def validate_input(adm_sp_value):
    print(adm_sp_value)


def main():
    # Collect command line arguments
    # Expecting 4 input values:
    # 1. Database server
    # 2. Login
    # 3. Password
    # 4. Load Manager table id
    adm_sp_value = ADMSharepointValue()

    i = 1
    for arg in sys.argv[1:]:
        if i == 1:
            adm_sp_value.database_server = arg
        if i == 2:
            adm_sp_value.login = arg
        if i == 3:
            adm_sp_value.password = arg
        if i == 4:
            adm_sp_value.load_manager_id = arg

        i += 1

    print(adm_sp_value)

    validate_input(adm_sp_value)


if __name__ == "__main__":
    main()