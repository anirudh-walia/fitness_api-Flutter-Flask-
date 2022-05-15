from flask import Flask, request, Response, render_template, send_file
import json

app = Flask(__name__)


@app.route('/')
def basic():
    return render_template('home.html')


@app.route('/fitapi', methods=['GET'])
def fitapi():
    d = {}
    secc = []
    tar_secc = []
    inputt = float(request.args['query'])
    cal = str(request.args['cal'])
    gen = str(request.args['gen'])
    age = str(request.args['age'])
    pain = str(request.args['pain'])
    target = str(request.args['target'])
    call = float(cal)
    total = round(call * inputt, 2)
    pain = pain.replace("leg", "'leg'")
    pain = pain.replace("back", "'back'")
    pain = pain.replace("arms", "'arms'")
    pain = pain.replace("butt", "'butt'")
    pain = pain.replace("shoulder", "'shoulder'")
    pain = pain.replace("chest", "'chest'")
    pain = pain.replace("\'", "\"")

    target = target.replace("cardio_t", "'cardio_t'")
    target = target.replace("abs_t", "'abs_t'")
    target = target.replace("legs_t", "'legs_t'")
    target = target.replace("arms_t", "'arms_t'")
    target = target.replace("back_t", "'back_t'")
    target = target.replace("chest_t", "'chest_t'")
    target = target.replace("delts_t", "'delts_t'")
    target = target.replace("glutes_t", "'glutes_t'")
    target = target.replace("\'", "\"")
    d['output_cal'] = str(total)
    d['cal'] = str(cal)
    d['gen'] = str(gen)
    d['age'] = int(age)
    d['pain'] = str(pain)

    res = json.loads(pain)
    tar_res = json.loads(target)
    for key, value in res.items():
        if value:
            secc.append(key)
    for key, value in tar_res.items():
        if value:
            tar_secc.append(key)
    # print(pain)
    # print(target)
    # print(d)
    print("dictionary= " + str(res))
    print("dictionary= " + str(tar_res))
    print(secc)
    print(tar_secc)

    return d


@app.route('/download')
def download_file():
    path = "Technical Reprt-Anirudh Walia.pdf"
    # path = "info.xlsx"
    # path = "simple.docx"
    # path = "sample.txt"
    return send_file(path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True, host='192.168.29.244')  # idhar ip badal na
