import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import matplotlib.dates as mdates
import datetime
import itertools
import calendar

month_names = ['', 'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni', 'Juli', 'August',
        'September', 'Oktober', 'November', 'Dezember']

delimiter = " " * 3
date_parser = lambda s: datetime.datetime.strptime(s.decode(), "%Y-%m-%d %H:%M:%S")
rows = None

datetimes = np.genfromtxt(
    "weatherdata (7).csv", skip_header=1, usecols=(1,), max_rows=rows,
    delimiter=delimiter, converters={1: date_parser}, unpack=True)

# tid, temp_out, temp_water, humidity, pressure, dewpoint, awat = np.genfromtxt(
#     "weatherdata (7).csv", skip_header=1, usecols=(0, 2, 3, 4, 5, 6, 7),
#     max_rows=rows, delimiter=delimiter, converters={1: date_parser}, unpack=True)

data = np.genfromtxt(
    "weatherdata (7).csv", skip_header=1, usecols=(0, 2, 3, 4, 5, 6, 7),
    max_rows=rows, delimiter=delimiter, converters={1: date_parser})

def mask_builder(predicate, data):
    result = np.zeros_like(data, dtype=bool)
    for i, row in enumerate(data):
        if predicate(row):
            result[i] = True
    return result

# Split by days
dates = []
chunks = []
for key, group in itertools.groupby(zip(datetimes, data), lambda pair: pair[0].date()):
    dates.append(key)
    chunk = np.array([item[1] for item in group]) # item[0] is the assoc. datetime
    chunks.append(chunk)

# split by weeks
weeks = []
week_chunks = []
for key, group in itertools.groupby(zip(datetimes, data), lambda pair: pair[0].date().isocalendar()[1]):
    weeks.append(key)
    chunk = np.array([item[1] for item in group]) # item[0] is the assoc. datetime
    week_chunks.append(chunk)

# Split by months
months = []
month_chunks = []
for key, group in itertools.groupby(zip(dates, chunks),
        lambda pair: (pair[0].year, pair[0].month)):
    months.append(key)
    chunk = np.vstack([item[1] for item in group]) # item[0] is the assoc. month
    month_chunks.append(chunk)

# compute monthly means (ignore 1st column since it contains the mean of indices)
month_means = np.array([np.mean(chunk, axis=0) for chunk in month_chunks])
day_means = np.array([np.mean(chunk, axis=0) for chunk in chunks])

day_maxs = np.array([np.max(chunk, axis=0) for chunk in chunks])
day_mins = np.array([np.min(chunk, axis=0) for chunk in chunks])

week_means = np.array([np.mean(chunk, axis=0) for chunk in week_chunks])
week_maxs = np.array([np.max(chunk, axis=0) for chunk in week_chunks])
week_mins = np.array([np.min(chunk, axis=0) for chunk in week_chunks])

month_maxs = np.array([np.max(chunk, axis=0) for chunk in month_chunks])
month_mins = np.array([np.min(chunk, axis=0) for chunk in month_chunks])

MONTH_TEMP_MEAN = False
MONTH_HUMID_PRESS_MEAN = False
DAY_TEMP_MEAN = True
DAY_HUMID_PRESS_MEAN = False
DAY_TEMP_MAX = True
MONTH_TEMP_MAX = True

WEEK_TEMP_MAX = True
WEEK_TEMP_MEAN = True

if MONTH_TEMP_MEAN:
    plt.figure()
    plt.plot(month_means[:, 1], marker='o', label="Außentemperatur")
    plt.plot(month_means[:, 2], marker='o', label="Wassertemperatur")
    xlabels = [calendar.month_abbr[m] for y, m in months]
# plt.xticks(range(len(months)), ["{}-{}".format(y, m) for y, m in months])
    plt.xticks(range(len(months)), xlabels, rotation='vertical')
    plt.xlabel("Monat")
    plt.ylabel("$\\mu_T$ [°C]")
    plt.title("Durchschnittstemperatur")
    plt.legend()
    plt.tight_layout()
    plt.savefig('temp.png')

if DAY_TEMP_MEAN:
    plt.figure()
    plt.plot(dates, day_means[:, 1], label="Außentemperatur")
    plt.plot(dates, day_means[:, 2], label="Wassertemperatur")
    # xlabels = [calendar.month_abbr[m] for y, m in months]
    # plt.xticks(range(len(months)), xlabels, rotation='vertical')
    plt.xlabel("Datum")
    plt.ylabel("$\\mu_T$ [°C]")
    plt.title("Durchschnittstemperatur täglich")
    plt.legend()
    plt.tight_layout()
    plt.savefig('temp_day_mean.png')

if WEEK_TEMP_MEAN:
    plt.figure()
    plt.plot(weeks, week_means[:, 1], label="Außentemperatur")
    plt.plot(weeks, week_means[:, 2], label="Wassertemperatur")
    plt.fill_between(weeks, week_mins[:, 1], week_means[:, 1], color='C0', alpha=0.4)
    plt.fill_between(weeks, week_means[:, 1], week_maxs[:, 1], color='C0', alpha=0.4)
    plt.fill_between(weeks, week_mins[:, 2], week_means[:, 2], color='C1', alpha=0.4)
    plt.fill_between(weeks, week_means[:, 2], week_maxs[:, 2], color='C1', alpha=0.4)
    # xlabels = [calendar.month_abbr[m] for y, m in months]
    # plt.xticks(range(len(months)), xlabels, rotation='vertical')
    plt.xlabel("KW")
    plt.ylabel("$\\mu_T$ [°C]")
    plt.title("Durchschnittstemperatur wöchentlich")
    plt.legend()
    plt.tight_layout()
    plt.savefig('temp_week_mean.png')

if WEEK_TEMP_MAX:
    plt.figure()
    plt.xticks(rotation=50)
    plt.plot(weeks, week_maxs[:, 1], label="Außentemperatur maximal", c='C0')
    plt.plot(weeks, week_maxs[:, 2], label="Wassertemperatur maximal", c='C1')
    plt.plot(weeks, week_mins[:, 1], ls='--', label="Außentemperatur minimal", c='C0')
    plt.plot(weeks, week_mins[:, 2], ls='--', label="Wassertemperatur minimal", c='C1')
    # xlabels = [calendar.month_abbr[m] for y, m in months]
    # plt.xticks(range(len(months)), xlabels, rotation='vertical')
    plt.xlabel("KW")
    plt.ylabel("$\\mu_T$ [°C]")
    plt.title("Max/Min wöchentlich")
    plt.legend()
    plt.tight_layout()
    plt.savefig('temp_week_max_min.png', dpi=160)

if DAY_TEMP_MAX:
    plt.figure()
    plt.xticks(rotation=50)
    plt.plot(dates, day_maxs[:, 1], label="Außentemperatur maximal", c='C0')
    plt.plot(dates, day_maxs[:, 2], label="Wassertemperatur maximal", c='C1')
    plt.plot(dates, day_mins[:, 1], ls='--', label="Außentemperatur minimal", c='C0')
    plt.plot(dates, day_mins[:, 2], ls='--', label="Wassertemperatur minimal", c='C1')
    # xlabels = [calendar.month_abbr[m] for y, m in months]
    # plt.xticks(range(len(months)), xlabels, rotation='vertical')
    # plt.xlabel("Datum")
    plt.ylabel("$\\mu_T$ [°C]")
    plt.title("Max/Min täglich")
    plt.legend()
    plt.tight_layout()
    plt.savefig('temp_day_max_min.png', dpi=160)

if MONTH_TEMP_MAX:
    plt.figure()
    plt.xticks(rotation=50)
    plt.plot(month_maxs[:, 1], label="Außentemperatur maximal", c='C0')
    plt.plot(month_maxs[:, 2], label="Wassertemperatur maximal", c='C1')
    plt.plot(month_mins[:, 1], ls='--', label="Außentemperatur minimal", c='C0')
    plt.plot(month_mins[:, 2], ls='--', label="Wassertemperatur minimal", c='C1')
    xlabels = [calendar.month_abbr[m] for y, m in months]
    plt.xticks(range(len(months)), xlabels, rotation='vertical')
    # plt.xlabel("Datum")
    plt.ylabel("$\\mu_T$ [°C]")
    plt.title("Max/Min monatlich")
    plt.legend()
    plt.tight_layout()
    plt.savefig('temp_month_max_min.png', dpi=160)

if MONTH_HUMID_PRESS_MEAN:
    fig, ax1 = plt.subplots(1)
    ax1.plot(month_means[:, 3], marker='o', color='C0')
    ax1.set_xticks(range(len(months)))
    ax1.set_xticklabels(xlabels, rotation='vertical')
    ax1.set_xlabel("Monat")
    ax1.set_ylabel("rel. Luftfeuchtigkeit")
    ax1.tick_params('y', colors='C0')
    ax1.set_title("Durchschnittsluftdruck/-feuchtigkeit")

    ax2 = ax1.twinx()
    ax2.plot(month_means[:, 4], marker='o', color='C1')
    ax2.set_ylabel("Luftdruck [hPa]")
    ax2.tick_params('y', colors='C1')
    fig.tight_layout()
    fig.savefig('pressure_humidity.png')

# plt.show()
