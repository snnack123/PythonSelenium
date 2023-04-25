from booking.booking import Booking

try:
    with Booking(teardown=False) as bot:
        bot.land_first_page()
        bot.change_currency(currency='RON')
        bot.select_place_to_go(place_to_go="Bucharest")
        bot.select_dates(check_in_date='2023-05-20', check_out_date='2023-05-23') #YYYY-MM-DD format
        bot.select_adults(adults=4)
        bot.select_rooms(rooms=2)
        bot.click_search_button()
        bot.apply_filtrations(stars=5)
        bot.report_results()
except Exception as e:
    print("There is a problem running this program from command line interface: " + str(e))