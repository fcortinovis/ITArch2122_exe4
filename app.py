from flask import Flask, render_template
import paho.mqtt.client as mqtt
import os

#======================================================================================================
# Globals:
#======================================================================================================
mqtt_string = ''


#======================================================================================================
# MQTT client:
#======================================================================================================
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
####client.subscribe("$SYS/#")
    client.subscribe("TestTopic")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    global mqtt_string
    mqtt_string = str(msg.payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.6.110", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
#client.loop_forever()
client.loop_start()


#======================================================================================================
# Web Page:
#======================================================================================================
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/ubuntu/ITArch2122/exe4/test_webapp/qrimage.png'

@app.route('/')
@app.route('/index')

def index():
    global qr_string
    full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'qrimage.jpg')
    return render_template('index.html', processed_text = mqtt_string)

if "__name__" == "__main__":
    app.run(debug=True)
