import aspose.words as aw
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, render_template,send_file

# url = "https://www.geeksforgeeks.org/how-to-start-learning-machine-learning/"

app = Flask(__name__)

# link = input("Enter the link")
input_data = ""


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    input_data = request.form.get('input_data')
    url = "https://www.geeksforgeeks.org/" + input_data
    req = requests.get(url)

    soup = BeautifulSoup(req.content, "html.parser")
    outerdata = soup.find_all("div", class_="page_content", limit=2) #text - class

    result = ""
    finalResult = ""

    for data in outerdata:
        content = data.getText()
        result = content.split('.')

    for out in result:
        finalResult += "\u2022 " + out + "\n"

    # create document object
    doc = aw.Document()

    # create a document builder object
    builder = aw.DocumentBuilder(doc)

    # add text to the document
    builder.write(finalResult)

    # save document
    doc.save("out.docx")
    return send_file('out.docx',as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
