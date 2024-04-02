import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#load csv and convert to datetime if csv isn't in it already
df = pd.read_csv('avgPrice S&P daily since 05_20_2004 - avgprice-GSPC-1day.csv')
df['Date'] = pd.to_datetime(df['Date'])

start_date = datetime(2007, 2, 23)
end_date = df['Date'].max()

blue_dot_intervals = 1570 #4.3 years in days for first blue dot
red_dot_intervals = 3141 #8.6 years in days

#find date in dataframe that coincides with prediction date
def find_nearest_date(target_date, df_dates):
    nearest = min(df_dates, key=lambda x: abs(x - target_date))
    return nearest

def calculate_future_dots(start_date, blue_start_interval, red_interval, years_forward=50):
    future_red_dots = [start_date + timedelta(days=i) for i in range(0, int(365.25*years_forward), red_interval)]
    first_blue_dot = start_date + timedelta(days=blue_start_interval)
    future_blue_dots = [first_blue_dot + timedelta(days=i) for i in range(0, int(365.25*years_forward), red_interval)]
    return future_red_dots, future_blue_dots

#calculate red and blue dots, including future ones
future_red_dots, future_blue_dots = calculate_future_dots(start_date, blue_dot_intervals, red_dot_intervals)

plt.figure(figsize=(14, 8))
plt.plot(df['Date'], df['AvgPrice'], label='S&P 500 AvgPrice', zorder=1)

handled_labels = []

#generate dates within range
current_date = start_date
dates_for_blue_dots = []
dates_for_red_dots = [start_date]

while current_date <= end_date:
    current_date += timedelta(days=red_dot_intervals)
    if current_date <= end_date:
        dates_for_red_dots.append(current_date)
    potential_blue_dot = current_date + timedelta(days=blue_dot_intervals - red_dot_intervals)
    if potential_blue_dot <= end_date:
        dates_for_blue_dots.append(potential_blue_dot)

#nearest valid date adjustment
valid_dates_for_blue_dots = [find_nearest_date(date, df['Date']) for date in dates_for_blue_dots]
valid_dates_for_red_dots = [find_nearest_date(date, df['Date']) for date in dates_for_red_dots]

#remove blue dots that have close values to red dots
valid_dates_for_blue_dots = [date for date in valid_dates_for_blue_dots if date not in valid_dates_for_red_dots]

#add blue and red dots
for date in valid_dates_for_blue_dots:
    price = df[df['Date'] == date]['AvgPrice'].values[0]
    plt.scatter(date, price, color='blue', s=50, edgecolor='black', zorder=2)
    plt.text(date, price, date.strftime('%Y-%m-%d'), fontsize=8, verticalalignment='bottom', horizontalalignment='right')
    if 'Blue Dots' not in handled_labels:
        plt.scatter([], [], color='blue', s=50, edgecolor='black', label='Panic Date', zorder=2)
        handled_labels.append('Blue Dots')

for date in valid_dates_for_red_dots:
    price = df[df['Date'] == date]['AvgPrice'].values[0]
    plt.scatter(date, price, color='red', s=50, edgecolor='black', zorder=3)
    plt.text(date, price, date.strftime('%Y-%m-%d'), fontsize=8, verticalalignment='bottom', horizontalalignment='right')
    if 'Red Dots' not in handled_labels:
        plt.scatter([], [], color='red', s=50, edgecolor='black', label='Midway/Peak', zorder=3)
        handled_labels.append('Red Dots')

#display dates in table
cell_text = []
for red_dot, blue_dot in zip(future_red_dots, future_blue_dots):
    cell_text.append([red_dot.strftime('%Y-%m-%d'), blue_dot.strftime('%Y-%m-%d')])

#table
columns = ('Midway/Peak', 'Panic Date')
the_table = plt.table(cellText=cell_text, colLabels=columns, loc='bottom', cellLoc='center', colWidths=[0.2, 0.2])

#graph
plt.subplots_adjust(left=0.2, bottom=0.4)
plt.xticks([])
plt.yticks(fontsize=10)
plt.ylabel('Average Price', fontsize=12)
plt.title('S&P 500 Average Price Since 05/20/2004 with ECM Markers', fontsize=14)
plt.legend(fontsize=10)
plt.tight_layout()

plt.show()
