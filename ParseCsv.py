

import pandas as pd
import datetime

from dateutil import parser


def parse_epoch(int_time):
    fmt = "%H:%M:%S"

    # local time
    t = datetime.datetime.fromtimestamp(float(int_time) / 1000.)
    return t.strftime(fmt)

# meta_data = pd.read_csv("/Users/milanarezina/PycharmProjects/ActivityBioSpy2018/OpenData_DonneesOuvertes/pub/Bio-Monitor/Bio-M-Challenge-Data/Meta_data_activities.csv", encoding='latin1')
#
# # for t in meta_data["Start_time"]:
# #     print(t)
#
#


# expriation = pd.read_csv("/Users/milanarezina/PycharmProjects/ActivityBioSpy2018/OpenData_DonneesOuvertes/pub/Bio-Monitor/Bio-M-Challenge-Data/Subject_A/Day_1_18h50_dur_3h/77/inspiration.csv", encoding='latin1')
# expriation = [parse_epoch(time) for time in expriation["time [s/1000]"]]
#
# heart_rate = pd.read_csv("/Users/milanarezina/PycharmProjects/ActivityBioSpy2018/OpenData_DonneesOuvertes/pub/Bio-Monitor/Bio-M-Challenge-Data/Subject_A/Day_1_18h50_dur_3h/77/systolic_pressure.csv", encoding='latin1')
# heart_rate = [parse_epoch(time) for time in heart_rate["time [s/1000]"]]
#
# times = zip(heart_rate, expriation)
#
# for i, t in enumerate(times):
#     print("{0} {1} {2}".format(i, t[0], t[1]))




#
# for t in meta_data["Start_time"]:
#     print(t)

# meta_times = [time for time in meta_data["Start_time"]]
# #
# bio_metric = [parse_epoch(time) for time in bio_metric["time [s/1000]"]]
# #
# times = zip(meta_times, bio_metric)
#
# for i, t in enumerate(times):
#
#     print("{2} Meta {0} bio_metric {1}".format(t[0], t[1], i))




def clean_meta(meta_data):
    # data = meta_data[meta_data.Position.notnull() and meta_data.Activity != "end"]
    data = meta_data.query('Position.notnull() and Activity != "end"')

    return data

"""
Times match: heart_rate, step, tidal_volume, cadence, expiration, minute_ventilation, systolic_pressure, 
Tempreture: dude got cold


Offset: RR_interval
"""
biometics = ["heart_rate", "tidal_volume_adjusted", "cadence", "step", "activity", "NN_interval", "temperature_celcius"]

csv_list = ["morning_day2.csv", "after_day2.csv", "morning_day3.csv", "after_day3.csv", "morning_day4.csv"]

save_file = "morning_day2.csv"
subject = "A"
data_folder = "Day_2_9h28_dur_3h/78/"
day = 2

meta_data = pd.read_csv("/Users/milanarezina/PycharmProjects/ActivityBioSpy2018/OpenData_DonneesOuvertes/pub/Bio-Monitor/Bio-M-Challenge-Data/Meta_data_activities.csv", encoding='latin1')
meta_data = clean_meta(meta_data)
# print(meta_data["Position"])
# print(clean_meta(meta_data))

cleaned = pd.DataFrame(columns = biometics)

def format_file(biometric):
    file = "/Users/milanarezina/PycharmProjects/ActivityBioSpy2018/OpenData_DonneesOuvertes/pub/Bio-Monitor/Bio-M-Challenge-Data/Subject_A/" + data_folder
    return file + biometric + ".csv"


# Yeild the start and end time of an activity
def get_range(meta_data):

    rows = meta_data.shape[0]

    for i in range(rows - 1):
            row = meta_data.iloc[[i]]

            if list(row["Day"])[0] == day and list(row["Subject"])[0] == 'A':
                print(row)
                activity = list(row["Activity"])[0]

                time_start = list(row["Start_time"])[0]

                row = meta_data.iloc[[i + 1]]
                time_end = list(row["Start_time"])[0]

                yield time_start, time_end, activity
        # if meta_data.at[i, 'Day'] == 1 and meta_data.at[i, 'Subject'] == 'A':
        #     activity = meta_data.at[i, 'Activity']
        #
        #     time_start = meta_data.at[i, 'Start_time']
        #     time_end = meta_data.at[i + 1, 'Start_time']



# Set the timestamps, assumed to be synced for all biometrics
biometric_data = pd.read_csv(format_file(biometics[0]), encoding='latin1')
# Get the timestamps column
times = biometric_data[biometric_data.columns[0]]
times = [parse_epoch(time) for time in times]
cleaned["time"] = times

for biometric in biometics:

    file = format_file(biometric=biometric)

    biometric_data = pd.read_csv(file, encoding='latin1')

    # Get the biometric column
    data = biometric_data[biometric_data.columns[1]]

    cleaned[biometric] = data

print(cleaned)


cleaned["Activity"] = None

#
for time_start, time_end, activity in get_range(meta_data):

    for i in cleaned.index:
            # print(parser.parse(time_start), parser.parse(cleaned.at[i, 'time']), parser.parse(time_end))

            try:
                if parser.parse(time_start) < parser.parse(cleaned.at[i, 'time']) < parser.parse(time_end):
                    print(time_start, cleaned.at[i, 'time'], time_end)
                    cleaned.at[i, 'Activity'] = activity

            except TypeError as e:
                print(e)


cleaned.to_csv(save_file, sep=',', encoding='latin1')


# def prepare_training(subject, day_file):
#     """
#     Prepares the cleaned csv for a subject, for all their day folders
#     :param subject:
#     :param day_file:
#     :return:
#     """
#     pass













