from flask import Flask, render_template
app =Flask(__name__)

data={
    'name': 'Mauntasir'
}

@app.route("/home")
def hello_world():
    return render_template('index.html', data=data)


@app.route("/about")
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

