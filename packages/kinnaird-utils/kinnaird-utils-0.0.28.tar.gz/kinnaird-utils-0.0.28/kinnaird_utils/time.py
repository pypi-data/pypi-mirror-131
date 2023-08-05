from datetime import date


def get_year_month_day_string() -> str:
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    return d1

    # # dd/mm/YY, like 16/09/2019
    # d1 = today.strftime("%d/%m/%Y")
    # print("d1 =", d1)
    #
    # # Textual month, day and year, like September 16, 2019
    # d2 = today.strftime("%B %d, %Y")
    # print("d2 =", d2)
    #
    # # mm/dd/y, like 09/16/19
    # d3 = today.strftime("%m/%d/%y")
    # print("d3 =", d3)
    #
    # # Month abbreviation, day and year, like Sep-16-2019
    # d4 = today.strftime("%b-%d-%Y")
    # print("d4 =", d4)