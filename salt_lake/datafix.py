for date in dates:
   print(date)
   for attr in goodkeys[:-1]:
     thisclxxx = 0
     thisxxx = 0
     for n in range(1,181):
       trgdate = (datetime.strptime(date, '%Y-%m-%d') - timedelta(days=n)).strftime('%Y-%m-%d')
       if trgdate >= minidate:
         x = datad[trgdate][attr]
       else:
         x = float(temp[trgdate][attr])
       if n < 31:
         thisxxx += x
       thisclxxx += x
     datad[date][f'{attr}_30'] = round(thisxxx / 30.0, 1)
     datad[date][f'{attr}_180'] = round(thisclxxx / 180.0, 1)

