from flask import Flask, render_template, session, g, redirect, request,\
    url_for
from flask_bootstrap import Bootstrap #changed the module's name
from flask_wtf import Form
from wtforms import StringField, SubmitField, BooleanField, SelectField
from wtforms.validators import Required, Length
# for detect text
import os
from google.cloud import vision
from google.protobuf import json_format
# for available langs
from google.cloud import translate_v2 as translate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
bootstrap = Bootstrap(app)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"D:\Wellesley College\Fall'19\WHACK\\key\whack-a6d2eb6d8294.json"

class ImageToText():

    @staticmethod
    def detect_text_uri(uri):
        """Detects text in the file located in Google Cloud Storage or on the Web.
        """
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"D:\Wellesley College\Fall'19\WHACK\\key\whack-a6d2eb6d8294.json"
        client = vision.ImageAnnotatorClient()
        image = vision.types.Image()
        image.source.image_uri = uri

        response = client.text_detection(image=image) # outputs json
        # print(response)
        texts = response.text_annotations
        # print(texts)
        result = texts[0].description
        # print('Texts:')
        # print(result)
        return result
    
    @staticmethod
    def translateText(text, target):
        # Imports the Google Cloud client library
        from google.cloud import translate_v2 as translate
        import os

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"D:\Wellesley College\Fall'19\WHACK\\key\whack-a6d2eb6d8294.json"

        # Instantiates a client
        translate_client = translate.Client()

        # The text to translate
        text = text
        # The target language
        target = target

        translation = translate_client.translate(
            text,
            target_language=target)
        result = translation['translatedText']
        # print(u'Text: {}'.format(text))
        # print(u'Translation: {}'.format(translation['translatedText']))
        return result

class ImageAndLangForm(Form):
    path = StringField('Enter the URL to image',
        validators=[Required(), Length(1,1000)])
    translate_client = translate.Client()
    results = translate_client.get_languages()
    language = SelectField(u'Translate to:', choices=[(language['language'],language['name']) for language in results])
    submit = SubmitField('Submit')

@app.route('/', methods = ['GET','POST'])
def index():
    translation = None
    text = None
    imgPath = None
    form = ImageAndLangForm()
    if form.validate_on_submit():
        imgPath = str(form.path.data)
        targetLang = str(form.language.data)
        text = ImageToText.detect_text_uri(imgPath)
        translation = ImageToText.translateText(text,targetLang)
    return(render_template('mainPage.html', form=form, imgPath=imgPath, text=text, translation=translation))
    
@app.route('/motivationPage')
def motivationPage():
    return(render_template('motivationPage.html'))

if __name__ == '__main__':
    app.run(debug=False)
    