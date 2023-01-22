from flask import jsonify,Flask,request
import json
from uuid import uuid4
app = Flask(__name__)


# all students list
#Example
"""
Paste In powershell

$response = Invoke-RestMethod 'http://127.0.0.1:5000/all' -Method 'GET' -Headers $headers
$response | ConvertTo-Json

"""
@app.route("/all")
def students():
    file = open('data.json')
    data = json.load(file)
    file.close()
    return jsonify(data)


# update a student data
"""
Paste In powershell

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("Content-Type", "application/json")

$body = "{
`n    `"name`":`"student_update`",
`n    `"dob`":`"12-01-22`",
`n    `"gender`":`"male`",
`n    `"subjects`":`"update`",
`n    `"pincode`":3435
`n
`n}"

$response = Invoke-RestMethod 'http://127.0.0.1:5000/update/c58f515a-45b8-4127-8b25-48b841b38d2a' -Method 'PUT' -Headers $headers -Body $body
$response | ConvertTo-Json
"""
@app.route("/update/<id>",methods=["PUT"])
def update(id):
    file = open('data.json','r')
    data = json.load(file)
    file.close()
    
    user = request.get_json()
    for stu in data:
        if(stu["id"] == id):
            temp = stu
            if("name" in user):
                stu["name"] = user["name"]
            if("gender" in user):
                stu["gender"] = user["gender"]
            if("dob" in user):
                stu["dob"] = user["dob"]
            if("subjects" in user):
                stu["subjects"] = user["subjects"]
            if("pincode" in user):
                stu["pincode"] = user["pincode"]
            obj = json.dumps(data)
            file = open('data.json','w')
            file.write(obj)       
            file.close()
            return jsonify(temp)
    file.close()
    return jsonify({"info":"No Student data found!"})

# delete a Student data
"""
Paste In powershell

$response = Invoke-RestMethod 'http://127.0.0.1:5000/delete/c58f515a-45b8-4127-8b25-48b841b38d2a' -Method 'DELETE' -Headers $headers
$response | ConvertTo-Json
"""
@app.route("/delete/<id>",methods=["DELETE"])
def delete(id):
    file = open('data.json','r')
    data = json.load(file)
    file.close()
    
    i=0
    for stu in data:
        if(stu["id"] == id):
            data.pop(i)
            obj = json.dumps(data)
            file = open('data.json','w')
            file.write(obj)       
            file.close()
            return jsonify({"Success":"Student data Deleted"})
        i +=1
    return jsonify({"info":"No Student data found!"})

#create a new student
# Example 
"""
Paste In powershell

$headers = New-Object "System.Collections.Generic.Dictionary[[String],[String]]"
$headers.Add("Content-Type", "application/json")

$body = "{
`n    `"name`":`"New Student`",
`n    `"dob`":`"12-01-22`",
`n    `"gender`":`"male`",
`n    `"subjects`":`"New Studnet`",
`n    `"pincode`":3435
`n
`n}"

$response = Invoke-RestMethod 'http://127.0.0.1:5000/create' -Method 'POST' -Headers $headers -Body $body
$response | ConvertTo-Json
"""
@app.route("/create",methods=["POST"])
def create():
    file = open('data.json','r')
    data = json.load(file)
    file.close()
    file = open('data.json','w')
    missing = []
    user = request.get_json()
    print(user["name"])
    if("name" not in user):
        missing.append({"name":"required"})
    if("gender" not in user):
        missing.append({"gender":"required"})
    if("dob" not in user):
        missing.append({"dob":"required"})
    if("subjects" not in user):
        missing.append({"subjects":"required"})
    if("pincode" not in user):
        missing.append({"pincode":"required"})
    if(len(missing)!=0):
        return jsonify(missing)
    user["id"] = str(uuid4())
    data.append(user)
    obj = json.dumps(data)
    file.write(obj)       
    file.close()
    return jsonify({"Success":"Student Object Created"})

if __name__ == "__main__":
    app.run(debug=True)

