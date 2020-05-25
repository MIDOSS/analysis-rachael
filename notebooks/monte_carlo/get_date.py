def get_date(start_date, end_date, delta_time) -> datetime:
    
    import random
    
    # initialize date list with start_date and increment by delta_time
    dates = start_date
    date_array = [start_date]
    while dates < end_date:
        date_array.append(dates)
        dates += delta_time

    # randomly select time based on delta_time increment
    return(random.choice(date_array))
