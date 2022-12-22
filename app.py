from flask import Flask,render_template,request,Response
import requests
from werkzeug.utils  import secure_filename
import json
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER']="/uploads"
baseURL="https://NotSet.com/api"
apiuser="Not Set"
apipass="Not Set"

baseURL=os.getenv('API_SERVER')
apiuser=os.getenv('API_USER')
apipass=os.getenv('API_PASS')


@app.route('/',methods=['GET'])
def mainrouteget():  # put application's code here
    return render_template("main.html")

@app.route('/scannerselector',methods=['GET'])
def scannerselector():  # put application's code here
    return render_template("inputselectorscanner.html")

@app.route('/cameraselector',methods=['GET'])
def cameraselector():  # put application's code here
    return render_template("inputselectorcamera.html")


@app.route('/addpresentmethod',methods=['GET'])
def addpresentmethod():  # put application's code here
    return render_template("addpresentmethod.html")

@app.route('/fullinput',methods=['GET'])
def fullinputget():  # put application's code here
    return render_template("fullinput.html")

@app.route('/guestinput',methods=['GET'])
def guestinputget():  # put application's code here
    return render_template("guestinput.html")

@app.route('/fullinputcamera',methods=['GET'])
def fullinputcameraget():  # put application's code here
    return render_template("fullinputcamera.html")

@app.route('/guestinputcamera',methods=['GET'])
def guestinputcameraget():  # put application's code here
    return render_template("guestinputcamera.html")

@app.route('/inputselector',methods=['GET'])
def inputselector():  # put application's code here
    return render_template("inputselector.html")

@app.route('/toolsselector',methods=['GET'])
def toolselector():  # put application's code here
    return render_template("toolselector.html")

@app.route('/addpresent',methods=['GET'])
def addpresent():  # put application's code here
    uri = (baseURL+"allpeople")
    response = requests.get(uri, auth=(apiuser, apipass))
    try:
        data = json.loads(response.text)
    except:
        data={"No People Added": "No People Added"}

    users = {}

    # Iterate over the list of dictionaries in the data object
    for user in data:
        # Add each dictionary to the dictionary, using the id as the key and the name as the value
        users[user['id']] = user['name']
    print(users)
    return render_template("addpresent.html",people=users)

@app.route('/addpresentcamera',methods=['GET'])
def addpresentcamera():  # put application's code here
    uri = (baseURL+"allpeople")
    response = requests.get(uri, auth=(apiuser, apipass))
    try:
        data = json.loads(response.text)
    except:
        data={"No People Added": "No People Added"}

    users = {}

    # Iterate over the list of dictionaries in the data object
    for user in data:
        # Add each dictionary to the dictionary, using the id as the key and the name as the value
        users[user['id']] = user['name']
    print(users)
    return render_template("addpresentcamera.html",people=users)

@app.route('/viewpeople',methods=['GET'])
def viewpeopleimages():  # put application's code here
    uri = (baseURL+"allpeopleimage")
    response = requests.get(uri, auth=(apiuser, apipass))
    data = json.loads(response.text)

    users = {}
    x=0
    for i in data:

        user={}
        user["id"]=i["id"]
        image=(baseURL+"people/"+i["image"])
        user["image"] = image
        user["name"] = i["name"]
        print(user)
        users[x]=user
        x = x + 1


    # Iterate over the list of dictionaries in the data object

    print(data)
    return render_template("viewpeople.html",people=users)

@app.route('/viewpresents',methods=['GET'])
def viewpresentimages():  # put application's code here
    uri = (baseURL+"allpresentsimage")
    response = requests.get(uri, auth=(apiuser, apipass))
    data = json.loads(response.text)

    users = {}
    x=0
    for i in data:

        user={}
        user["barcode"]=i["barcode"]
        image=(baseURL+"/images/"+i["imagelink"])
        user["image"] = image
        user["itemname"] = i["itemname"]
        user["itemvalue"] = i["itemvalue"]
        user["recipientname"] = i["recipientname"]
        print(user)
        users[x]=user
        x = x + 1


    # Iterate over the list of dictionaries in the data object

    print(data)
    return render_template("viewpresents.html",people=users)

@app.route('/addperson',methods=['GET'])
def addsperson():  # put application's code here
    return render_template("addperson.html")

@app.route('/addselector',methods=['GET'])
def addselector():  # put application's code here
    return render_template("addselector.html")

@app.route('/uploadbackup',methods=['GET'])
def uploadbackup():  # put application's code here
    return render_template("uploadbackup.html")

@app.route('/downloadbackup',methods=['GET'])
def downloadbackup():
    response = requests.get(baseURL+"export",auth=(apiuser, apipass))

    # Save the file to the local file system
    file_contents = response.content

    # Serve the file to the client

    return Response(file_contents, mimetype="application/zip", headers={"Content-Disposition": "attachment; filename=ChristmasPresentsBackup.zip"})




@app.route('/viewselector',methods=['GET'])
def viewselector():  # put application's code here
    return render_template("viewselector.html")

@app.route('/viewfull',methods=['POST'])
def viewfullpost():
    contents={}
    barcode = request.form['barcode']# put application's code here
    barcode=str(barcode)
    uri=(baseURL+"barcodelookup/" + barcode)
    print(uri)
    response = requests.get(uri, auth=(apiuser, apipass))
    print(response.text)
    imageURL=(baseURL+"images/")
    peopleimageURL = (baseURL + "people/")

    jsonobject=response.json()

    print(jsonobject)

    if jsonobject["status"]=="error":
        contents["status"]="error"
        return render_template("erroritem.html")
    else:
        contents["status"]="present"
        contents["presentimagelink"]=(imageURL+jsonobject["imagelink"])
        contents["personimagelink"]=(peopleimageURL+jsonobject["recipientimage"])
        contents["itemname"] = (jsonobject["itemname"])
        contents["recipientname"] = jsonobject["recipientname"]
        contents["itemvalue"] = jsonobject["itemvalue"]

        return render_template("item.html", contents=contents)



@app.route('/viewguest',methods=['POST'])
def viewguestpost():
    contents={}
    barcode = request.form['barcode']# put application's code here
    barcode=str(barcode)
    uri=(baseURL+"barcodelookup/" + barcode)
    print(uri)
    peopleimageURL = (baseURL + "people/")
    response = requests.get(uri, auth=(apiuser, apipass))
    print(response.text)

    jsonobject=response.json()

    print(jsonobject)

    if jsonobject["status"]=="error":
        contents["status"]="error"
        return render_template("erroritem.html")
    else:
        contents["personimagelink"]=(peopleimageURL+jsonobject["recipientimage"])
        contents["recipientname"] = jsonobject["recipientname"]
        return render_template("itemguest.html", contents=contents)

@app.route('/newperson',methods=['POST'])
def newpersonpost():
    name = request.form['name']  #

    uploaded_file = request.files['fileForm']
    if uploaded_file.filename != '':
        myfilename=(name+".jpg")
        uploaded_file.save(myfilename)
        filename=(myfilename)
    else:
        pass
    url=(baseURL+"uploadpeople/"+name)

    import requests

    # Set the URL of the endpoint you want to send the request to

    # Read the image file and get its content as bytes
    with open(filename, "rb") as img:
        string = base64.b64encode(img.read()).decode('utf-8')

    # Set the "Content-Type" and "Content-Disposition" headers
    # to tell the server that the request contains an image
    api_url = (baseURL+"uploadperson/"+name)
    response = requests.post(url=api_url, json={'user_photo': string},auth=(apiuser, apipass))
    print(response.text)


    data = {
        'imagelink': filename,
        'name': name
    }
    headers = {'Content-Type': 'application/json'}
    url = (baseURL+"/add_person")
    response = requests.post(url, json=data, headers=headers, auth=(apiuser, apipass))

    jsonobject=response.json()

    if jsonobject["status"] == "Success":
        return render_template("goodmessage.html",message="Person Added Successfully")
    else:
        return render_template("badmessage.html",message="Adding Person Failed")


@app.route('/newpresent',methods=['POST'])
def newpresentpost():
    import requests
    barcode = request.form['barcode']
    itemname = request.form['name']  #
    itemvalue = request.form['itemvalue']
    recipient = request.form['recipient']
    uri=(baseURL+"person/" + recipient)
    response = requests.get(uri, auth=(apiuser, apipass))
    myjson=response.json()
    if myjson["status"]=="present":
        recipientid=myjson["recipientid"]
    else:
        message = "Unable to Find Recipient"
        return render_template("badmessage.html", message=message)
    imagelink=(barcode+".jpg")
    data = {
        "barcode" : barcode,
        'imagelink':  imagelink,  # This will be the base64 encoded image data
        "recipient" :recipientid,
        "recipientname": recipient,
        'itemname': itemname,
        "itemvalue":itemvalue
    }
    headers = {'Content-Type': 'application/json'}
    url = (baseURL+"add")
    response = requests.post(url, json=data, headers=headers, auth=(apiuser, apipass))
    print(response.text)

    jsonobject=response.json()

    uploaded_file = request.files['fileForm']
    if uploaded_file.filename != '':
        myfilename = (barcode + ".jpg")
        uploaded_file.save(myfilename)
        filename = (myfilename)
    else:
        pass

    import requests

    # Set the URL of the endpoint you want to send the request to

    # Read the image file and get its content as bytes
    with open(filename, "rb") as img:
        string = base64.b64encode(img.read()).decode('utf-8')

    # Set the "Content-Type" and "Content-Disposition" headers
    # to tell the server that the request contains an image
    api_url = (baseURL+"uploadpresent/" + barcode)
    response = requests.post(url=api_url, json={'user_photo': string})
    print(response.text)

    if jsonobject["status"] == "success":
        return render_template("goodmessage.html",message="Item Added Successfully")
    else:
        message=jsonobject["message"]
        return render_template("badmessage.html",message=message)

@app.route('/uploadbackuppost',methods=['POST'])
def uploadbackuppost():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        myfilename = ("backup.zip")
        uploaded_file.save(myfilename)
        with open(myfilename, "rb") as zip_file:
            file_contents = zip_file.read()

            # Send a POST request to the API endpoint with the zip file as the request body
            url = (baseURL+"update-images")
            headers = {'Content-Type': 'application/zip'}
            response = requests.post(url, headers=headers, data=file_contents,auth=(apiuser, apipass))
            return render_template("goodmessage.html", message="Backup Restored! All data restored Successfully")
    else:
        return render_template("badmessage.html", message="No File Selected!")

@app.route('/testpage', methods=['GET'])
def testpage():
    data={
        "baseurl" : baseURL,
        "apiuser" : apiuser

    }# put application's code here
    return render_template("testpage.html", data=data)

@app.route('/test1', methods=['GET'])
def testpage1():
    uri = (baseURL)
    try:
        response = requests.get(uri+"test",auth=(apiuser, apipass))
        print(response.text)
        data = json.loads(response.text)
        return render_template("goodmessage.html", message="API is Reachable")
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return render_template("badmessage.html", message=e)

@app.route('/test2', methods=['GET'])
def testpage2():
    uri = (baseURL+"testdb")
    try:
        response = requests.get(uri,auth=(apiuser, apipass))
        print(response.text)
        data = json.loads(response.text)
        return render_template("goodmessage.html", message=data["status"])
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        return render_template("badmessage.html", message=e)

@app.route('/test3', methods=['GET'])
def testpage3():
    import time
    uri = (baseURL + "testspeed")
    start_time = time.time()
    response = requests.get(uri,auth=(apiuser, apipass))
    print(response.text)
    end_time = time.time()
    elapsed_time = end_time - start_time
    message=("We Reached the Backend API in " + str("{:.2f}".format(elapsed_time)) + " seconds!")
    return render_template("goodmessage.html", message=message)

    # put application's code here

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)
