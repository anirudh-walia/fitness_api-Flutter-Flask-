import json
import random

import pandas as pd
import numpy as np
from flask import Flask, request, render_template, send_file
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import operator


def Merge(dict1, dict2):
    res = {**dict1, **dict2}
    return res


stop = stopwords.words('english')

app = Flask(__name__)

fitness_dataset = pd.read_csv(r"C:\Users\aniru\Downloads\fitness_exercises dataset.csv")


def text_preprocessing(column):
    column = column.str.lower()
    column = column.str.replace('http\S+|www.\S+|@|%|:|,|', '', case=False)
    word_tokens = column.str.split()
    keywords = word_tokens.apply(lambda x: [item for item in x if item not in stop])
    for i in range(len(keywords)):
        keywords[i] = " ".join(keywords[i])
        column = keywords

    return column


def recc_workout(name):
    overall_infos = []
    for i in range(0, fitness_dataset.shape[0]):
        overall_infos.append(
            fitness_dataset['equipment'][i] + ' ' + fitness_dataset['name'][i] + ' ' + fitness_dataset['target'][
                i] + ' ' + fitness_dataset['bodyPart'][i])
    fitness_dataset['overall_infos'] = overall_infos
    df_new = fitness_dataset[['id', 'overall_infos']]
    df_new['cleaned_infos'] = text_preprocessing(df_new['overall_infos'])
    CV = CountVectorizer()
    converted_metrix = CV.fit_transform(df_new['cleaned_infos'])
    cosine_similarityy = cosine_similarity(converted_metrix)
    workout_list = {}
    workout_id = fitness_dataset[fitness_dataset['name'] == name]['id'].values[0]
    score = list(enumerate(cosine_similarityy[workout_id]))
    sorted_score = sorted(score, key=lambda x: x[1], reverse=True)
    sorted_score = sorted_score[0:10]
    i = 0
    for item in sorted_score:
        workout_title = fitness_dataset[fitness_dataset['id'] == item[0]]['name'].values[0]
        workout_calories = fitness_dataset[fitness_dataset['id'] == item[0]]['calories 12 reps (cals)'].values[0]
        #         print(i+1,workout_title,'-',workout_calories)
        workout_list.__setitem__(workout_title, workout_calories)
        i = i + 1
        if i > 4:
            break
    return workout_list


def giveworkout(name_list):
    #     print(data_dict['name'])
    out1 = {}
    out2 = {}
    out3 = {}
    out4 = {}

    out1 = recc_workout(name_list[0])
    out1 = dict(sorted(out1.items(), key=operator.itemgetter(1), reverse=True))

    out2 = recc_workout(name_list[1])
    out2 = dict(sorted(out2.items(), key=operator.itemgetter(1), reverse=True))

    out3 = recc_workout(name_list[2])
    out3 = dict(sorted(out3.items(), key=operator.itemgetter(1), reverse=True))

    out4 = recc_workout(name_list[3])
    out4 = dict(sorted(out4.items(), key=operator.itemgetter(1), reverse=True))

    polll = Merge(out1, out2)
    dholll = Merge(out3, out4)
    final_out = Merge(polll, dholll)
    final_out = dict(sorted(final_out.items(), key=operator.itemgetter(1), reverse=True))
    # print(final_out)
    return final_out


def function1(PARAM_BODYPARTS, PARAM_EQUIPMENT, PARAM_TARGETMUSCLES):
    PARAM_EXERCISES = 50
    new_fitness = fitness_dataset.loc[ \
        (fitness_dataset['bodyPart'].isin(PARAM_BODYPARTS)) & \
        (fitness_dataset['equipment'].isin(PARAM_EQUIPMENT)) & \
        (fitness_dataset['target'].isin(PARAM_TARGETMUSCLES)) \
        ].sort_values(by=['target', 'equipment']) \
        .copy(deep=True) \
        .reset_index()

    new_fitness.drop(columns=['index'], inplace=True)
    sampling_num = int(round((PARAM_EXERCISES / len(new_fitness.target.unique()))))
    print(new_fitness.target.unique())
    print(sampling_num)
    df = new_fitness.groupby("target").sample(n=sampling_num, random_state=32, replace=True).drop_duplicates()
    df.reset_index()
    df.sort_values('calories 12 reps (cals)', ascending=False)
    new_res = df.sample(n=4)
    new_res = new_res['name']
    workout_namesss = []
    workout_namesss = new_res.tolist()
    res = giveworkout(workout_namesss)
    # print(res)
    return res


# BODYPARTS = ['waist', 'leg', 'back', 'cardio']
# EQUIPMENT = ['body weight', 'dumbbell', 'barbell']
# TARGETMUSCLES = ['arms muscle','abs','cardio target']


@app.route('/')
def basic():
    return render_template('home.html')


def pick_random_key_from_dict(d: dict):
    """Grab a random key from a dictionary."""
    keys = list(d.keys())
    random_key = random.choice(keys)
    return random_key


def pick_random_item_from_dict(d: dict):
    """Grab a random item from a dictionary."""
    random_key = pick_random_key_from_dict(d)
    random_item = random_key, d[random_key]
    return random_item


def pick_random_value_from_dict(d: dict):
    """Grab a random value from a dictionary."""
    _, random_value = pick_random_item_from_dict(d)
    return random_value


def Convert(tup, di):
    di = dict(tup)
    return di


@app.route('/fitapi', methods=['GET'])
def fitapi():
    workout_dict = {}
    d = {}
    secc = []
    tar_secc = []
    equip_secc = []
    inputt = float(request.args['query'])
    cal = str(request.args['cal'])
    gen = str(request.args['gen'])
    age = str(request.args['age'])
    pain = str(request.args['pain'])
    target = str(request.args['target'])
    equip = str(request.args['equip'])
    # inaweek = str(request.args['inaweek'])
    # confi = str(request.args['confi'])
    call = float(cal)
    total = round(call * inputt, 2)
    # inaweek = int(inaweek)
    # confi = int(confi)
    pain = pain.replace("leg", "'leg'")
    pain = pain.replace("back", "'back'")
    pain = pain.replace("arms", "'arms'")
    pain = pain.replace("waist", "'waist'")
    pain = pain.replace("shoulder", "'shoulder'")
    pain = pain.replace("chest", "'chest'")
    pain = pain.replace("cardio", "'cardio'")
    pain = pain.replace("\'", "\"")

    target = target.replace("cardio target", "'cardio_t'")
    target = target.replace("abs", "'abs'")
    target = target.replace("legs muscle", "'legs muscle'")
    target = target.replace("arms muscle", "'arms muscle'")
    target = target.replace("back muscle", "'back muscle'")
    target = target.replace("chest muscle", "'chest muscle'")
    target = target.replace("delts", "'delts'")
    target = target.replace("glutes", "'glutes'")
    target = target.replace("\'", "\"")

    equip = equip.replace("dumbbell", "'dumbbell'")
    equip = equip.replace("barbell", "'barbell'")
    equip = equip.replace("body weight", "'body weight'")
    equip = equip.replace("\'", "\"")

    res = json.loads(pain)
    tar_res = json.loads(target)
    equip_res = json.loads(equip)
    for key, value in res.items():
        if not value:
            secc.append(key)
    for key, value in tar_res.items():
        if value:
            tar_secc.append(key)
    for key, value in equip_res.items():
        if value:
            equip_secc.append(key)
    print("dictionary= " + str(res))
    print("dictionary= " + str(tar_res))
    print(secc)
    print(tar_secc)
    print(equip_secc)

    workout_dict = function1(secc, equip_secc, tar_secc)
    print(workout_dict)

    workoutname_list1 = []
    workoutval_list1 = []
    for i in range(0, 4):
        workout_1 = pick_random_item_from_dict(workout_dict)
        name = workout_1[0]
        val = workout_1[1]
        workoutname_list1.append(name)
        workoutval_list1.append(val)

    val_1 = sum(workoutval_list1)
    rep1 = 0
    if total > val_1:
        rep1 = rep1 + 1
    total1 = total
    while total1 > 0:
        total1 = total1 - val_1
        rep1 = rep1 + 1
# -------------------------------------------------------------------------------
    workoutname_list2 = []
    workoutval_list2 = []
    for i in range(0, 4):
        workout_2 = pick_random_item_from_dict(workout_dict)
        name = workout_2[0]
        val = workout_2[1]
        workoutname_list2.append(name)
        workoutval_list2.append(val)

    val_2 = sum(workoutval_list2)
    rep2 = 0
    if total > val_2:
        rep2 = rep2 + 1
    total2 = total
    while total2 > 0:
        total2 = total2 - val_2
        rep2 = rep2 + 1

    print(val_2)
    print(rep1)
    print(workoutname_list2)
    print(workoutname_list2[0])
    d['output_cal'] = str(total)

    d['rep1'] = str(rep1)
    d['rep2'] = str(rep2)

    d['val1'] = str(val_1)
    d['val2'] = str(val_2)

    d['work1_1'] = str(workoutname_list1[0])
    d['work1_2'] = str(workoutname_list1[1])
    d['work1_3'] = str(workoutname_list1[2])
    d['work1_4'] = str(workoutname_list1[3])

    d['work2_1'] = str(workoutname_list2[0])
    d['work2_2'] = str(workoutname_list2[1])
    d['work2_3'] = str(workoutname_list2[2])
    d['work2_4'] = str(workoutname_list2[3])

    return d


@app.route('/download')
def download_file():
#     path = "login_test_1.0.0.apk"
    # path = "info.xlsx"
    # path = "simple.docx"
    # path = "sample.txt"
    return send_file(path, as_attachment=True)


# @app.route('/dailyquote')
# def random_quote():
#     dic = {}
#     quote = ['¨The only person you are destined to become is the person you decide to be.¨ – Ralph Waldo Emerson',

#              '“Once you learn to quit, it becomes a habit.¨ ― Vince Lombardi Jr',

#              '¨A year from now you may wish you had started today.¨ – Karen Lamb',

#              '¨Our growing softness, our increasing lack of physical fitness, is a menace to our security.¨— John F. '
#              'Kennedy',
#              '¨Don’t give up on your dreams, or your dreams will give up on you.¨ – John Wooden',

#              '“The last three or four reps is what makes the muscle grow. This area of pain divides a champion from '
#              'someone who is not a champion.”- Arnold Schwarzenegger',

#              '¨Most people fail, not because of lack of desire, but, because of lack of commitment.¨ – Vince Lombardi',

#              '“Success usually comes to those who are too busy to be looking for it.” -Henry David Thoreau',

#              '¨Exercise is labor without weariness.¨ – Samuel Johnson',

#              '¨Some people want it to happen, some wish it would happen, others make it happen.¨ – Michael Jordan']
    daily_quote = random.choice(quote)
    dic['quote'] = str(daily_quote)
    print(dic)
    return dic


if __name__ == '__main__':
    app.run(debug=True) 
