import pandas as pd
import os
import json

def replace_missing_with_conditional_mean(df, condition_cols, cols):
    s = df.groupby(condition_cols)[cols].transform('mean')
    return df.fillna(s.to_dict('series'))

number =0
path = r"C:\Users\ra200030d\Desktop\public\sets\8"
temp = pd.DataFrame()
for root, dirs, files in os.walk(path):
    for file in files:
        number += 1
        directory = os.path.join(root, file)

        try:
            with open(directory) as file:
                data = json.load(file)
                r = directory[len(path):]
                r = r.split(os.sep)

                if (any(char.isalpha() for char in r[1])):
                    country = r[1]
                    city = r[2]
                    venue = r[4]
                    date = r[3].split('_')
                    if int(date[0]) < 100:
                        if int(date[0]) < 60:
                            date[0] = "20" + date[0]
                        else:
                            date[0] = "19" + date[0]
                    date = date[0] + str(int(date[1])) + str(int(date[2]))

                else:
                    if (any(char.isalpha() for char in r[2])):
                        country = r[2]
                        city = r[3]
                        venue = r[4]
                        date = r[1].split('_')
                        if int(date[0]) < 100:
                            if int(date[0]) < 60:
                                date[0] = "20" + date[0]
                            else:
                                date[0] = "19" + date[0]
                        date = date[0] + str(int(date[1])) + str(int(date[2]))
                    else:
                        if int(r[1]) < 100:
                            if int(r[1]) < 60:
                                r[1] = "20" + r[1]
                            else:
                                r[1] = "19" + r[1]
                        date = r[1] + str(int(r[2])) + str(int(r[3]))
                        country = r[4]
                        city = r[5]
                        venue = r[6]

                venue = (venue.split('.'))[0]
                for d in data:
                    d["Country"] = country
                    d["City"] = city
                    d["Date"] = date
                    d["Venue"] = venue
                data = pd.DataFrame.from_dict(data)
                temp = temp.append(data, ignore_index = True)
                file.close()

        except FileNotFoundError:
            continue
        except ValueError:
            dict = []
            with open(directory) as f:
                for line in f:
                    r = directory[len(path):]
                    r = r.split(os.sep)

                    if (any(char.isalpha() for char in r[1])):
                        country = r[1]
                        city = r[2]
                        venue = r[4]
                        date = r[3].split('_')
                        if int(date[0]) < 100:
                            if int(date[0]) < 60:
                                date[0] = "20" + date[0]
                            else:
                                date[0] = "19" + date[0]
                        date = date[0] + str(int(date[1])) + str(int(date[2]))

                    else:
                        if (any(char.isalpha() for char in r[2])):
                            country = r[2]
                            city = r[3]
                            venue = r[4]
                            date = r[1].split('_')
                            if int(date[0]) < 100:
                                if int(date[0]) < 60:
                                    date[0] = "20" + date[0]
                                else:
                                    date[0] = "19" + date[0]
                            date = date[0] + str(int(date[1])) + str(int(date[2]))
                        else:
                            if int(r[1]) < 100:
                                if int(r[1]) < 60:
                                    r[1] = "20" + r[1]
                                else:
                                    r[1] = "19" + r[1]
                            date = r[1] + str(int(r[2])) + str(int(r[3]))
                            country = r[4]
                            city = r[5]
                            venue = r[6]

                    venue = (venue.split('.'))[0]
                    d = json.loads(line)
                    d["Country"] = country
                    d["City"] = city
                    d["Date"] = date
                    d["Venue"] = venue
                    dict.append(d)
            data = pd.DataFrame.from_dict(dict)
            temp = temp.append(data, ignore_index=True)
        except TypeError:
            dict = []
            with open(directory) as f:
                for line in f:
                    d = json.loads(line)
                    d["Country"] = country
                    d["City"] = city
                    d["Date"] = date
                    d["Venue"] = venue
                    dict.append(d)
            data = pd.DataFrame.from_dict(dict)
            temp = temp.append(data, ignore_index=True)
temp["Country"] = temp["Country"].str.replace('-', '_')
temp["City"] = temp["City"].str.replace('-', '_')
temp["Venue"] = temp["Venue"].str.replace('-', '_')
temp["Country"] = temp["Country"].str.replace('the_', '')
temp = temp.dropna(subset=["band_name"])

temp["is_indie"] = temp["is_indie"].fillna(False)

mean_attendance = temp["attendance"].mean()
temp = replace_missing_with_conditional_mean(temp, ["Venue", "City", "Country"], ['attendance'])
temp["attendance"] = temp["attendance"].fillna(mean_attendance)

s = temp.query('is_indie == True')
s=s.groupby(['City'])['attendance'].agg('sum')
s = s.nlargest(3)
s = s.index
s = list(s)
s = ",".join(s)


print(number)
print(temp["Country"].nunique())
most_common = temp["City"].mode()
most_common.sort_values(key=lambda x: x.str.lower())
print(most_common[0])
print(s)

k = temp.groupby(["City", 'Venue', "Country", "Date"])["is_indie"].any()
keys = list(["City", 'Venue', "Country", "Date"])
i1 = temp.set_index(keys).index
temp = temp[i1.isin(k[k].index)]
temp = temp.groupby(["band_name"])['attendance'].agg("mean")
temp = temp.nlargest(3)
temp = temp.index
temp = list(temp)
temp = ",".join(temp)
print(temp)