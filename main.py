#
# Project 1: Analyzing CTA2 L data in Python
# Dylan Brunelle
#
import sqlite3
import matplotlib.pyplot as plt
##################################################################
#
# print_stats
#
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.
#
def print_stats(db):

 print("General stats:")
 db.execute("Select count(*) From Stations;")
 row = db.fetchone();
 print(" # of stations:", f"{row[0]:,}")
 db.execute("Select count(*) From Stops;")
 row = db.fetchone();
 print(" # of stops:", f"{row[0]:,}")
 db.execute("Select count(*) From Ridership;")
 row = db.fetchone();
 print(" # of ride entries:", f"{row[0]:,}")

 date = "";
 db.execute("Select date(Ride_Date) from Ridership order by date(Ride_Date) asc limit 1");
 row = db.fetchone();
 date += row[0];
 db.execute("Select date(Ride_Date) from Ridership order by date(Ride_Date) desc limit 1")
 row = db.fetchone();
 date += " - " + row[0]
 print(" date range: " + date)

 db.execute("Select sum(Num_Riders) from Ridership")
 row = db.fetchone();
 total = int(row[0]);
 print(" Total Ridership: ", f"{total:,}")

 db.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'W'")
 row = db.fetchone();
 weekday = row[0];
 print(" Weekday Ridership: ", f"{weekday:,}", "(" + f"{((weekday/total) * 100):0.2f}" + "%)")

 db.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'A'")
 row = db.fetchone();
 saturday = row[0];
 print(" Saturday Ridership: ", f"{saturday:,}", "(" + f"{((saturday/total) * 100):0.2f}" + "%)")

 db.execute("Select sum(Num_Riders) from Ridership where Type_of_Day = 'U'")
 row = db.fetchone();
 sunday = row[0];
 print(" Sunday/Holiday Ridership: ", f"{sunday:,}", "(" + f"{((sunday/total) * 100):0.2f}" + "%)")
 print()


### 1: Find Stations via partial names ###
def cmd1(db):
 print()
 station = input("Enter partial station name (wildcards _ and %): ")
 db.execute("Select * from Stations where Station_Name like ? order by Station_Name asc", [station])
 rows = db.fetchall();

 # No matching stations exist? Return.
 if(len(rows) < 1):
  print("**No stations found...")
  return

 for r in rows:
  print(r[0], ":",r[1])

### 2: Ridership of each station ###
def cmd2(db):
 print("** ridership all stations **")
 db.execute("Select sum(Num_Riders) from Ridership")
 total = db.fetchone()[0];
 db.execute("Select Stations.Station_Name, sum(Ridership.Num_Riders) from Stations "
            "join Ridership on Stations.Station_ID = Ridership.Station_ID "
            "group by Stations.Station_Name")
 rows = db.fetchall()
 for r in rows:
  print(r[0], ":",f"{r[1]:,}", f"({((r[1]/total) * 100):.2f}%)")

### 3: Top 10 busiest stations ###
def cmd3(db):
 print("** top-10 stations **")
 db.execute("Select sum(Num_Riders) from Ridership")
 total = db.fetchone()[0];
 db.execute("Select Stations.Station_Name, sum(Ridership.Num_Riders) from Stations "
            "join Ridership on Stations.Station_ID = Ridership.Station_ID "
            "group by Stations.Station_Name order by sum(Ridership.Num_Riders) desc limit 10")
 rows = db.fetchall()
 for r in rows:
  print(r[0], ":", f"{r[1]:,}", f"({((r[1] / total) * 100):.2f}%)")

### 4: The 10 least busiest stations ###
def cmd4(db):
 print("** least-10 stations **")
 db.execute("Select sum(Num_Riders) from Ridership")
 total = db.fetchone()[0];
 db.execute("Select Stations.Station_Name, sum(Ridership.Num_Riders) from Stations "
            "join Ridership on Stations.Station_ID = Ridership.Station_ID "
            "group by Stations.Station_Name order by sum(Ridership.Num_Riders) asc limit 10")
 rows = db.fetchall()
 for r in rows:
  print(r[0], ":", f"{r[1]:,}", f"({((r[1] / total) * 100):.2f}%)")

### 5: Stops by chosen color ###
def cmd5(db):
 print()
 color = input("Enter a line color (e.g. Red or Yellow): ")
 db.execute("Select Stop_Name, Direction, ADA from Stops "
            "join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID "
            "join Lines on StopDetails.Line_ID = Lines.Line_ID "
            "where Lines.Color like ? order by Stops.Stop_Name asc ", [color])
 rows = db.fetchall()

 # Validate line exists.
 if len(rows) < 1:
  print("**No such line...")
  return

 for r in rows:
  access = "yes"
  if r[2] != 1:
   access = "no"
  print(r[0],": direction =",r[1], "(accessible? " + access + ")")

### 6: Total Ridership by Month ###
def cmd6(db):
 db.execute("Select strftime('%m', date(Ride_Date)) as month, sum(Num_Riders) from Ridership "
            "group by month order by month asc")
 rows = db.fetchall()

 x = []
 y = []

 print("** ridership by month **")
 for r in rows:
  x.append(r[0])
  y.append(r[1])
  print(r[0],":",f"{r[1]:,}")
 print()


 # Prompt for plot
 p = input("Plot? (y/n) ")
 if p == "y":
  plt.xlabel("Month")
  plt.ylabel("Number of riders (*1^8)")
  plt.title("Monthly Ridership")
  plt.plot(x, y)
  plt.show()

### 7: Total Ridership by Year ###
def cmd7(db):
 db.execute("Select strftime('%Y', date(Ride_Date)) as year, sum(Num_Riders) from Ridership "
            "group by year order by year asc")
 rows = db.fetchall()

 x = []
 y = []

 print("** ridership by year **")
 for r in rows:
  yr = r[0]
  x.append(yr[2:])
  y.append(r[1])
  print(r[0],":",f"{r[1]:,}")

 print()
 p = input("Plot? (y/n) ")
 if p == "y":
  plt.xlabel("Year")
  plt.ylabel("Number of riders (*1^8)")
  plt.title("Yearly Ridership")
  plt.plot(x, y)
  plt.show()

### 8: Daily ridership of two stations ###
def cmd8(db):
 ##Get year##
 print()
 yr = input("Year to compare against? ")

 ##Get station 1##
 print()
 s1 = input("Enter station 1 (wildcards _ and %): ")
 db.execute("Select Station_ID, Station_Name from Stations "
            "where Station_Name like ?", [s1])

 #Validate station exists, is specific#
 mult = db.fetchall()
 if len(mult) > 1:
  print("**Multiple stations found...")
  return
 elif len(mult) < 1:
  print("**No station found...")
  return
 else:
  station1 = mult[0]

 ##Get station 2##
 print()
 s2 = input("Enter station 2 (wildcards _ and %): ")
 db.execute("Select Station_ID, Station_Name from Stations "
            "where Station_Name like ?", [s2])
 mult = db.fetchall()

 #Validate station exists, is specific#
 if len(mult) > 1:
  print("**Multiple stations found...")
  return
 elif len(mult) < 1:
  print("**No station found...")
  return
 else:
  station2 = mult[0]

 ##PRINT##
 print("Station 1:", station1[0], station1[1])

 db.execute("Select date(Ride_Date), Num_Riders from Ridership "
            "where strftime('%Y',date(Ride_Date)) = ? and Station_ID = ? "
            "group by date(Ride_Date) order by date(Ride_Date) asc", [yr, station1[0]])

 rows1 = db.fetchall()
 for r in range(0,5):
  print(rows1[r][0], rows1[r][1])
 for r in range(len(rows1) - 5, len(rows1)):
  print(rows1[r][0], rows1[r][1])

 station2 = mult[0]
 print("Station 2:", station2[0], station2[1])

 db.execute("Select date(Ride_Date), Num_Riders from Ridership "
            "where strftime('%Y',date(Ride_Date)) = ? and Station_ID = ? "
            "group by date(Ride_Date) order by date(Ride_Date) asc", [yr, station2[0]])

 rows2 = db.fetchall()
 for r in range(0, 5):
  print(rows2[r][0], rows2[r][1])
 for r in range(len(rows2) - 5, len(rows2)):
  print(rows2[r][0], rows2[r][1])


 # Prompt for plot
 p = input("Plot? (y/n) ")
 if p != "y":
  return


 #else.. PLOT!
 x1 = []
 y1 = []
 x2 = []
 y2 = []

 for r in range(0, len(rows1)):
  x1.append(r)
  x2.append(r)
  y1.append(rows1[r][1])
  y2.append(rows2[r][1])
 plt.xlabel("day")
 plt.ylabel("number of riders")
 plt.title("riders each day of 2020…")
 plt.plot(x1, y1, label=station1[1])
 plt.plot(x2, y2, label=station2[1])
 plt.legend()
 plt.show()

### 9: Output Station names by line color ###
def cmd9(db):
 print()
 color = input("Enter a line color (e.g. Red or Yellow): ")
 db.execute("Select distinct Station_Name, Latitude, Longitude from Stops "
            "join Stations on Stops.Station_ID = Stations.Station_ID "
            "join StopDetails on Stops.Stop_ID = StopDetails.Stop_ID "
            "join Lines on StopDetails.Line_ID = Lines.Line_ID "
            "where Color like ? "
            "order by Station_Name asc", [color])
 rows = db.fetchall()

 # Validate line exists
 if(len(rows) < 1):
  print("**No such line...")
  return

 x = []
 y = []
 for r in rows:
  x.append(r[2])
  y.append(r[1])
  print(r[0], ":", f"({r[1]:},", f"{r[2]:})")
 print()

 # Prompt for plot
 p = input("Plot? (y/n) ")
 if p != "y":
  return

 # else? PLOT
 # populate x and y lists with (x, y) coordinates --- note that longitude
 # are the X values and latitude are the Y values
 #
 image = plt.imread("chicago.png")
 xydims = [-87.9277, -87.5569, 41.7012, 42.0868]  # area covered by the map:
 plt.imshow(image, extent=xydims)

 plt.title(color + " line")
 #
 # color is the value input by user, we can use that to plot the
 # figure *except* we need to map Purple-Express to Purple:
 #
 if (color.lower() == "purple-express"):
  color = "Purple"  # color="#800080"

 plt.plot(x, y, "o", c=color)
 #
 # annotate each (x, y) coordinate with its station name:
 #
 for r in rows:
  plt.annotate(r[0], (r[2], r[1]))

 plt.xlim([-87.9277, -87.5569])
 plt.ylim([41.7012, 42.0868])

 plt.show()


### Main loop ###
def app(cmd, db):
 if cmd == "1":
  cmd1(db)
 elif cmd == "2":
  cmd2(db)
 elif cmd == "3":
  cmd3(db)
 elif cmd == "4":
  cmd4(db)
 elif cmd == "5":
  cmd5(db)
 elif cmd == "6":
  cmd6(db)
 elif cmd == "7":
  cmd7(db)
 elif cmd == "8":
  cmd8(db)
 elif cmd == "9":
  cmd9(db)
 else:
  print("**Error, unknown command, try again...")

##################################################################
#
# main
#
print('** Welcome to CTA L analysis app **')
print()
dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')
db = dbConn.cursor()
print_stats(db)
cmd = input("Please enter a command (1-9, x to exit): ")
while cmd != "x":
 app(cmd, db)
 print()
 cmd = input("Please enter a command (1-9, x to exit): ")
#
# done
#