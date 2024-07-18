import eventlet
eventlet.monkey_patch()
import flask
from flask import request, jsonify,render_template,redirect
from flask import Flask

# import eventlet
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pymongo
import requests
import time
from datetime import datetime
from private import private
from sende import review_email
app = Flask(__name__)
# socketio = SocketIO(app, async_mode='eventlet')
socketio = SocketIO(app)
scheduler = BackgroundScheduler()

app.secret_key = 'your_secret_key'

uri = "mongodb+srv://Bamidele:1631324de@cluster0.hrdikjw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)
dbs = client['Data']
day = dbs['day']
user = dbs['User Data']
emaild = dbs['email']
messages = dbs['cmessages']
client = MongoClient(uri, server_api=ServerApi('1'))
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def send_database(first,last,number,email,time,appoint):
    timestamp = datetime.now()
    send={
        "first":first,
        "last":last,
        "email":email,
        "number":number,
        "time":time,
        "appoint":appoint,
        "appointment": False,
        "review":False,
        "timestamp":timestamp,
        "messages":f"{first} {last}  wants to booked  an appointment named {appoint} in the {time}"
    }
    messages.insert_one(send)

def send_databases(first, last, number,email, appoint):
    timestamp = datetime.now()
    send={
        "first":first,
        "last":last,
        "email":email,
        "number":number,
        "time":time,
        "appoint":appoint,
        "appointment": False,
        "review": False,
        "timestamp":timestamp,
        "messages": f"{first} {last} wants to booked  an appointment named {appoint} in the {time} "
    }
    messages.insert_one(send)
def send_email(first, last, number, email, time, appoint):
    # Email configuration
    sender_email = "review@cosmeticcreationsspa.com"
    receiver_email = "Rebecca@cosmeticcreationsspa.com"
    password = "fdxi slyq umoh klge"

    # Email content
    subject = "Appointment Details"
    body = f"First Name: {first}\nLast Name: {last}\nPhone Number: {number}\n Email:{email}\n Time: {time}\nAppointment Type: {appoint}"

    # Constructing the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Sending the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
def sends_email(first, last, number, appoint):
    # Email configuration
    sender_email = "review@cosmeticcreationsspa.com"
    receiver_email = "Rebecca@cosmeticcreationsspa.com"
    password = "fdxi slyq umoh klge"
    # Email content
    subject = "Appointment Details"
    body = f"First Name: {first}\nLast Name: {last}\nPhone Number: {number}\nAppointment Type: {appoint}"

    # Constructing the email
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Sending the email
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
@app.route('/inde')
def inde():
    return render_template('index.html')

@app.route('/indexs')
def indexs():
    return render_template('indexs.html')

@app.route('/private', methods=['POST'])
def privatef():
    feedback = request.form.get("feedback")
    name = request.form.get("name")
    email = request.form.get("email")
    phone = request.form.get("phone")
    private(name, email, phone, feedback)
    return redirect("/momew")

@app.route('/gogn')
def gogn():
    return render_template('gogn.html')
@app.route('/bot')
def bot():
    return render_template('bot.html')
@app.route('/cos')
def cos():
    return render_template('cos.html')
@app.route('/momew')
def momew():
    return render_template('momew.html')
@app.route('/review')
def review():
    return render_template('review.html')
@app.route('/ping')
def ping():
    url = 'https://cosmetic-chatbot.onrender.com/bot'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        print(f'Ping successful. Status code: {response.status_code}')
    except requests.exceptions.RequestException as e:
        print(f'Error while pinging: {str(e)}')
@app.route('/review-email', methods=['POST'])
def reviewe():
    try:
        email = request.form.get('email')
        review_email(email)

        # Return a success response
        return redirect("/review")
    except Exception as e:
        # Return an error response in case of exception
        return redirect("/review")
@app.route('/send-email', methods=['POST'])
def email():
    try:
        data = request.get_json()  # Parse the incoming JSON data
        email = data.get('email')

        # Return a success response
        return jsonify({'status': 'success', 'message': f'Email {email} received'})
    except Exception as e:
        # Return an error response in case of exception
        return jsonify({'status': 'error', 'message': str(e)}), 500




@app.route('/index', methods=['POST'])
def index():
    sorted_data = list(messages.find({}, {'_id': 0}).sort('timestamp', pymongo.DESCENDING))


    return jsonify(sorted_data)
@app.route('/update_checkbox_state', methods=['POST'])
def update_checkbox_state():
    email = request.json.get('email')
    appointment = request.json.get('appointment', False)
    review = request.json.get('review', False)
    message = request.json.get('message')
    messages.update_one(
        {"email": email},
        {"$set": {"messages":message,"appointment": appointment, "review": review}}
    )
    return jsonify(success=True)
@app.route('/get_checkbox_state', methods=['POST'])
def get_checkbox_state():
    message = request.json.get('message')
    email = request.json.get('email')
    result = messages.find_one({"email":email,"messages":message})
    appointment = result.get("appointment")
    review = result.get("review")
    checkbox_state = {
        "appointment": appointment,
        "review": review
    }
    return jsonify(checkbox_state)
@app.route('/', methods=['POST'])
def mainpath():
    # Get the JSON data from the Dialogflow request
    data = request.get_json()
    # Extract the 'intent' from the request data
    intent = data['queryResult']['intent']['displayName']
    if intent == "Start":
        return flask.redirect('/dialog', code=307)
    elif intent == "appointment":
        return flask.redirect('/appointment', code=307)
    elif intent == "patient":
        return flask.redirect('/patient', code=307)
    elif intent == "before":
        return flask.redirect('/before', code=307)
    elif intent == "Spa services":
        return flask.redirect('/Spa', code=307)
    elif intent == "No-spa":
        return flask.redirect('/No-spa', code=307)
    elif intent == "No-spa - next":
        return flask.redirect('/No-spa - next', code=307)
    elif intent == "Med-spa":
        return flask.redirect('/Med-spa', code=307)
    elif intent == "insurance":
        return flask.redirect('/insurance', code=307)
    elif intent == "FAQ":
        return flask.redirect('/FAQ', code=307)
    elif intent == "prices":
        return flask.redirect('/prices', code=307)
    elif intent == "Question":
        return flask.redirect('/question', code=307)
    elif intent == "Question - yes":
        return flask.redirect('/Question - yes', code=307)
    elif intent == "New":
        return flask.redirect('/New', code=307)
    elif intent == "Existing":
        return flask.redirect('/New', code=307)
    elif intent == "Time":
        return flask.redirect('/Times', code=307)
    elif intent == "Monday":
        return flask.redirect('/Time', code=307)
    elif intent == "Tuesday":
        return flask.redirect('/Time', code=307)
    elif intent == "Wednesday":
        return flask.redirect('/Time', code=307)
    elif intent == "Thursday":
        return flask.redirect('/Time', code=307)
    elif intent == "Friday":
        return flask.redirect('/Time', code=307)
    elif intent == "Saturday":
        return flask.redirect('/Time', code=307)
    elif intent == "Yes":
        return flask.redirect('/Yes', code=307)
    elif intent == "unique":
        return flask.redirect('/unique', code=307)
    elif intent == "provider":
        return flask.redirect('/provider', code=307)
    elif intent == "open":
        return flask.redirect('/open', code=307)

    else:
        return jsonify({"fulfillmentText": "Invalid intent. Please try again."})

@app.route('/dialog', methods=['POST'])
def mainpaths():
    fulfillment = {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Hi!\nI am your assistant here at Cosmetic Creations Skin Sanctuary and Med Spa.\nHow can I help you today?"
                        ]
                    }
                },
                {"payload":
                    {
                        "richContent": [
                            [
                                {
                                    "type": "button",
                                    "icon": {
                                      "type": "calendar_month",
                                      "color": "#e82959"
                                    },
                                    "text": "I'd like to request an appointment",
                                    "event": {
                                        "name": "appointment",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "discount",
                                        "color": "#e82959"
                                    },
                                    "text": "Patient Specials",
                                    "event": {
                                        "name": "patient",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "face_retouching_natural",
                                        "color": "#e82959"
                                    },
                                    "text": "Before and After",
                                    "event": {
                                        "name": "before",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "local_hospital",
                                        "color": "#e82959"
                                    },
                                    "text": "What services do you offer",
                                    "event": {
                                        "name": "services",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "volunteer_activism",
                                        "color": "#e82959"
                                    },
                                    "text": "What insurance do you accept",
                                    "event": {
                                        "name": "insurance",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "quiz",
                                        "color": "#e82959"
                                    },
                                    "text": "FAQ",
                                    "event": {
                                        "name": "faq",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                }

                            ]
                        ]
                    }
                }
            ]
        }
    return fulfillment

@app.route('/New', methods=['POST'])
def New():
    data = request.get_json()


    first = data['queryResult']['parameters'].get('first')
    last = data['queryResult']['parameters'].get('last')
    number = data['queryResult']['parameters'].get('number')
    email = data['queryResult']['parameters'].get('email')
    appoint = data['queryResult']['parameters'].get('appoint')
    datas = {
        "first": first,
        "last": last,
        "number": number,
        "appoint": appoint,
        "email": email,
        "day": "",
        "time": ""

    }
    emails = {
        "email": email
    }
    user.insert_one(datas)


    emaild.insert_one(emails)


    fulfillment = {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Now let us know what day works best for you.\nKeep in mind we are open by appointment only.\nChoose a day below👇🏼"
                        ]
                    }
                },
                {"payload":
                    {
                        "richContent": [
                            [
                                {
                                    "type": "button",
                                    "icon": {
                                      "type": "calendar_month",
                                      "color": "#e82959"
                                    },
                                    "text": "Monday",
                                    "event": {
                                        "name": "Monday",
                                        "languageCode": "en",
                                        "parameters": {"email": email}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "calendar_month",
                                        "color": "#e82959"
                                    },
                                    "text": "Tuesday",
                                    "event": {
                                        "name": "Tuesday",
                                        "languageCode": "en",
                                        "parameters": {"email": email}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "calendar_month",
                                        "color": "#e82959"
                                    },
                                    "text": "Wednesday",
                                    "event": {
                                        "name": "Wednesday",
                                        "languageCode": "en",
                                        "parameters": {"email": email}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "calendar_month",
                                        "color": "#e82959"
                                    },
                                    "text": "Thursday",
                                    "event": {
                                        "name": "Thursday",
                                        "languageCode": "en",
                                        "parameters": {"email": email}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "calendar_month",
                                        "color": "#e82959"
                                    },
                                    "text": "Friday",
                                    "event": {
                                        "name": "Friday",
                                        "languageCode": "en",
                                        "parameters": {"email": email}
                                    }
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "calendar_month",
                                        "color": "#e82959"
                                    },
                                    "text": "Saturday",
                                    "event": {
                                        "name": "Saturday",
                                        "languageCode": "en",
                                        "parameters": {"email": email}
                                    }
                                }

                            ]
                        ]
                    }
                }
            ]
        }
    return fulfillment

@app.route('/Time', methods=['POST'])
def Time():
    data = request.get_json()
    email = data["queryResult"]["parameters"]["email"]
    emails = {
        "email": email
    }
    emaild.insert_one(emails)

    intent_name = data['queryResult']['intent']['displayName']
    update_operation = {
        "$set": {
            "day": intent_name
        }
    }

    # days = {
    #     "day": intent_name
    # }
    # day.insert_one(days)
    # print(day)
    user.update_one({"email":email}, update_operation)

    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"What time of day works best for you?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Morning",
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://media.botsrv2.com/control/img/320x320/2a/759bf9e5604330a573facc9cce6680/Afternoon-01.webp"
                                            }
                                        },
                                    },
                                    {
                                        "text": "Afternoon",
                                        "image": {
                                            "src": {
                                                "rawUrl": "https://media.botsrv2.com/control/img/320x320/2a/759bf9e5604330a573facc9cce6680/Afternoon-01.webp"
                                            }
                                        },
                                    }
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    }

    return fulfillment
@app.route('/Times', methods=['POST'])
def Times():
    data = request.get_json()
    time = data['queryResult']['queryText']
    last_query_result = emaild.find().sort('_id', -1).limit(1)

    # Convert the result to a list and get the first item if available
    last_result = list(last_query_result)
    email = last_result[0].get("email")
    print(email)
    details = user.find_one({"email": email})
    days = details.get("day")
    first = details.get("first")
    last = details.get("last")
    number = details.get("number")
    appoint = details.get("appoint")
    send_email(first, last, number, email, time,  appoint)
    send_database(first, last, number, email, time, appoint)
    socketio.emit('data_update')
    delete_query = {"email": email}

    # Delete documents that match the query


    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"Fantastic! I've marked that you prefer {days} {time} appointment. "
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Please note - *this is only a request... not a confirmed appointment.Our patient coordinator will reach out to you as soon as possible to confirm your appointment! 🙂"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "If this is an emergency, please proceed to the nearest emergency room or call 911.Thanks for choosing our practice."
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "That's all for now 👋🏼 If you need me again for anything, I'll be here!"
                    ]
                }
            }
        ]
    }
    user.delete_many(delete_query)
    emaild.delete_many(delete_query)
    return fulfillment

@app.route('/appointment', methods=['POST'])
def questions():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"Great 😁\nI'm more than happy to help you with that. I just need to collect a few things from you to get started. It'll only take a second..."
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "To start, are you a new or existing patient?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                          {
                            "type": "chips",
                            "options": [
                              {
                                "text": "New",
                              },
                              {
                                "text": "Existing",
                              }
                            ]
                          }
                        ]
                      ]
                }
            }
        ]
    }
    return fulfillment

@app.route('/patient', methods=['POST'])
def patient():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"You're so close to getting your special!\n🎉 Botox is $11 per unit. If you get a filler, we can go as low as $10.\n🎉 IPL Photo Facial only $150 for new customers (first treatment only)\n🎉 Laser packages available!"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "All you have to do is request your appointment with us.\nJust tap the 'Claim Offer' button below to get started!"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                          {
                            "type": "chips",
                            "options": [
                              {
                                "text": "Claim Offer",
                              },
                            ]
                          }
                        ]
                      ]
                }
            }
        ]
    }
    return fulfillment

@app.route('/before', methods=['POST'])
def before():
    fulfillment = {
        "fulfillmentMessages": [

            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "image",
                                "rawUrl": "https://media.botsrv2.com/control/img/optimized/b7/255f9e51ea4eca8b2472180f9d5f95/new-testimonial.webp",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "image",
                                "rawUrl": "https://media.botsrv2.com/control/img/optimized/eb/8187a8d7e04fe1a1ce50886f38b0ea/testimonial_img01.webp",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "info",
                                "subtitle": "Acne/Scar treatment; PROCELL and MICRODERMABRASION",
                            },
                            {
                                "type": "image",
                                "rawUrl": "https://media.botsrv2.com/control/img/optimized/71/d62e453ca34805a7c3db8237e9bb91/testimonial_img02.webp",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "image",
                                "rawUrl": "https://media.botsrv2.com/control/img/optimized/b2/3d58027b0c42eb9b57866be2dded29/testimonial_img03.webp",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "image",
                                "rawUrl": "https://cosmeticcreationsspa.com/wp-content/uploads/2020/03/Microblading-2020-05-scaled.jpg",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "image",
                                "rawUrl": "https://cosmeticcreationsspa.com/wp-content/uploads/2020/03/Microblading-2020-06-scaled.jpg",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "info",
                                "subtitle": "MICROBLADING/NANO/ POWDER BROWS",
                            },
                            {
                                "type": "image",
                                "rawUrl": "https://cosmeticcreationsspa.com/wp-content/uploads/2020/03/Microblading-2020-09-1536x988.jpg",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "image",
                                "rawUrl": "https://cosmeticcreationsspa.com/wp-content/uploads/2020/03/Microblading-2020-10-1536x988.jpg",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "info",
                                "subtitle": "MICROBLADING/NANO/ POWDER BROWS",
                            }
                        ]
                      ]
                }
            }
        ]
    }
    return fulfillment

@app.route('/Spa', methods=['POST'])
def Spa():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f". Waxing\n.Eyelashes & Makeup\n.Airbrush Tanning\n.FacialsMicrodermabra\n.Signature Treament\n.Oxygen\n.Add Ons\n.Massage\nMicroblading/Permanent Make up\nFacials\nMicrodermabrasion\nHydra Facials"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Please contact us to hear more about our services!\n We'd be happy to answer all of your questions. 😉"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Would you like to request an appointment?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Yes",
                                    },
                                    {
                                        "text": "No",
                                    }
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    }
    return fulfillment

@app.route('/No-spa', methods=['POST'])
def No():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"No problem!\nI understand that you may want more info before requesting an appointment. 📅"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "To have a better understanding of our practice \nI'll have a patient coordinator reach out to you. 🏃🏼"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "What's your first name?"
                    ]
                }
            },
        ]
    }
    return fulfillment

@app.route('/No-spa - next', methods=['POST'])
def Nospanext():
    data = request.get_json()
    first = data['queryResult']['parameters'].get('first')
    last = data['queryResult']['parameters'].get('last')
    number = data['queryResult']['parameters'].get('number')
    email = data['queryResult']['parameters'].get('email')
    appoint = "Patient Cordinator"
    sends_email(first, last, number, appoint)
    send_databases(first, last, number,email, appoint)
    socketio.emit('data_update')


    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"Got it!\nI'm sending this to my team right now and someone will reach out to you as soon as possible 🏃"
                    ]
                }
            },
        ]
    }
    return fulfillment


@app.route('/Med-spa', methods=['POST'])
def Med():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f".Skin Treatment & Peels\n.Laser Treatments\n.Injectables"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Please contact us to hear more about our services!\n We'd be happy to answer all of your questions. 😉"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Would you like to request an appointment?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Yes",
                                    },
                                    {
                                        "text": "No",
                                    }
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    }
    return fulfillment
@app.route('/insurance', methods=['POST'])
def insurance():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"We do not accept any insurance."
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Please contact us to hear more about our services!\n We'd be happy to answer all of your questions. 😉"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Would you like to request an appointment?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Yes",
                                    },
                                    {
                                        "text": "No",
                                    }
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    }
    return fulfillment
@app.route('/FAQ', methods=['POST'])
def faq():
    fulfillment = {
            "fulfillmentMessages": [
                {
                    "text": {
                        "text": [
                            "Here are the questions we get asked most often by new and long-time patients!"
                        ]
                    }
                },
                {"payload":
                    {
                        "richContent": [
                            [
                                {
                                    "type": "button",
                                    "icon": {
                                      "type": "payments",
                                      "color": "#e82959"
                                    },
                                    "text": "What are your prices?",
                                    "event": {
                                        "name": "prices",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "forum",
                                        "color": "#e82959"
                                    },
                                    "text": "I want a specific question",
                                    "event": {
                                        "name": "question",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "schedule",
                                        "color": "#e82959"
                                    },
                                    "text": "When are you open",
                                    "event": {
                                        "name": "open",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "local_hospital",
                                        "color": "#e82959"
                                    },
                                    "text": "What services do you offer",
                                    "event": {
                                        "name": "services",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "military_tech",
                                        "color": "#e82959"
                                    },
                                    "text": "What makes you unique or standout",
                                    "event": {
                                        "name": "unique",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                },
                                {
                                    "type": "divider"
                                },
                                {
                                    "type": "button",
                                    "icon": {
                                        "type": "check_box",
                                        "color": "#e82959"
                                    },
                                    "text": "What do you say about your provider",
                                    "event": {
                                        "name": "provider",
                                        "languageCode": "en",
                                        "parameters": {}
                                    }
                                }

                            ]
                        ]
                    }
                }
            ]
        }
    return fulfillment
@app.route('/prices', methods=['POST'])
def prices():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"Botox - $11/Unit or with purchase of any filler $10/uni\n \nJuvederm Volbella - $300 5 ml\nJuvederm Ultra XC - $475\nJuvederm Plus XC - $550\nJuvederm Voluma - $750ment\nJuvederm Vollure - $750\nRESTYLANE SILK - $399\nRESTYLANE LYFT - $499\nRADIESSE - $499J\nBELOTERO - $540\nKYBELLA - $600\nVERSA - $399\nSCULPTRA - $700"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Laser Hair Removal (Single Treatment)\n \nBikini Line - $99\nPartial Brazilian Bikini - $110\nPartial Brazilian Bikini - $110\nUpper Lip - $70\nChin - $70\nUpper Lip/ Chin - $999\nCheeks - $65\nNeck - $79\nFull Face - $125\nHands/Feet - $95\nArms / Elbow Down - $165\nArmos / Full - $250\nUpper Legs - $199\nLower Legs - $150\nFull Legs - $299\nFull Back - $250\nChest - $199\nAreola - $70\nButtock - $130\nUnderarm - $99\nHands - $95"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Laser Hair Removal (5 Session Pack)\n \nBikini Line - $395\nPartial Brazilian Bikini - $440\nBrazilian - $460\nUpper Lip - $175\nChin - $200\nUpper Lip/ Chin - $395\nCheeks - $260\nNeck - $315\nFull Face - $440\nHands/Feet - $380\nArms / Elbow Down - $660\nArmos / Full - $995\nUpper Legs - $795\nLower Legs - $600\nFull Legs - $1195\nFull Back - $995\nChest - $795\nAreola - $280\nButtock - $520\nUnderarm - $395\nHands - $380?"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Photo Rejuvenation/IPL\n \nFace - $250\nNeck - $175\nChest - $300]\nSpider Vein Treatment - $300\nFace & Neck - $350\nFace & Chest - $500\nFace/Neck/Chest - $600\nHands - $150"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Would you like to request an appointment?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Yes",
                                    },
                                    {
                                        "text": "No",
                                    }
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    }
    return fulfillment
@app.route('/question', methods=['POST'])
def question():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"Before you ask your question. We want to collect some quick info so we can answer as soon as possible. 🏃‍♀️"
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "To start, are you a new or existing patient?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                          {
                            "type": "chips",
                            "options": [
                              {
                                "text": "New",
                              },
                              {
                                "text": "Existing",
                              }
                            ]
                          }
                        ]
                      ]
                }
            }
        ]
    }
    return fulfillment
@app.route('/Question - yes', methods=['POST'])
def Questionyes():
    data = request.get_json()
    first = data['queryResult']['parameters'].get('first')
    last = data['queryResult']['parameters'].get('last')
    number = data['queryResult']['parameters'].get('number')
    email = data['queryResult']['parameters'].get('last')
    question = data['queryResult']['parameters'].get('number')
    print(first,last,number,email,question)
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"Thanks for that 👍🏼\nI'll have our patient coordinator get back to you right away 🏃"
                    ]
                }
            },
        ]
    }
    return fulfillment



@app.route('/unique', methods=['POST'])
def unique():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"We offer the most contemporary aesthetic medical procedures and Spa Treatments in a beautiful, serene, unique spa environment, designed to soothe and relax you."
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "We pride ourselves in providing the highest quality care, while offering a wide range of state-of-the-art treatment options in a soothing environment founded on experience and trust."
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "image",
                                "rawUrl": "https://media.botsrv2.com/control/img/optimized/c0/1c892f6b8d408ca7c847ea95fb6620/blob.png",
                                "accessibilityText": "Example logo"
                            },
                            {
                                "type": "info",
                                "subtitle": "Would you like to request an appointment?",
                            },
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Yes",
                                    },
                                    {
                                        "text": "No",
                                    }
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    }
    return fulfillment

@app.route('/provider', methods=['POST'])
def provider():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"Our staff is highly trained and have been with us for years."
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "We aim to make our clients feel comfortable and safe in a very warm and friendly environment."
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Would you like to request an appointment?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Yes",
                                    },
                                    {
                                        "text": "No",
                                    }
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    }
    return fulfillment

@app.route('/open', methods=['POST'])
def open():
    fulfillment = {
        "fulfillmentMessages": [
            {
                "text": {
                    "text": [
                        f"Keep in mind we are open by appointment only."
                    ]
                }
            },
            {
                "text": {
                    "text": [
                        "Would you like to request an appointment?"
                    ]
                }
            },
            {"payload":
                {
                    "richContent": [
                        [
                            {
                                "type": "chips",
                                "options": [
                                    {
                                        "text": "Yes",
                                    },
                                    {
                                        "text": "No",
                                    }
                                ]
                            }
                        ]
                    ]
                }
            }
        ]
    }
    return fulfillment


if __name__ == '__main__':
    scheduler.add_job(ping, 'interval', minutes=10)
    scheduler.start()
    socketio.run(app, host='0.0.0.0', port=8080)