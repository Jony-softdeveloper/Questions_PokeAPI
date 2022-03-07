"""The functions which permit make the requests to Pokemon API and

display the results to the users.
"""

def get_option_user() -> int:
    """Get the option of the user.

    Returns
    -------
    option: int
        Number of option selected.
    """
    while True:
        try:
            option: int = int(input("\nElige un número sobre alguna inquietud que tengas de los 'Mountros de bolsillo': "))
        except ValueError:
            print('Solo puedes ingresar números entre 1 y 4. Por favor reintentelo.')
            continue
        else:
            if option <= 0 or option > 4:
                print('Lo siento, está opción no existe. Por favor reintentelo.')
                continue
            break

    return option