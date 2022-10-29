import sys
LUNAR = 29.53059
SOLAR = 365.2425

if len(sys.argv) > 2:
  TOLERANCE = float(sys.argv[2])
else:
  TOLERANCE = 0.01

for i in range(1,int(sys.argv[1])+1):
  x = SOLAR * i
  y = x / LUNAR
  if abs(y - round(y)) < float(TOLERANCE):
    print(f'found: year {i}, month {round(y)} ({y/float(i)})')
