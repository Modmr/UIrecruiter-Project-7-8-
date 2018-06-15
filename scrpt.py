import apiai
import json


access_token = "be72d4a27ad74a288cf3ba3d16fbdacc"
client = apiai.ApiAI(access_token)
# request = client.text_request()


given_name=""
last_name=""
age = 0
traits_positive = [""]
traits_neutral = [""]
traits_negative = [""]
college_degree = ""
college_major = ""
carreer = ""
experience = 0
strengths = [""]
weaknesses = [""]
hours = 0

# A = ['"given-name": ','"last-name": ']
def ExtractInfoString(Array,response):

    times = int(len(Array)/2)
    ExtractedInfo = ["", "", "","",""]
    itemindex = 0
    for x in range(1,times+1):
        
        index = response.find(Array[itemindex])
        indexrefined = index + len(Array[itemindex])
        index2 = response.find(Array[itemindex+1])
        ExtractedInfo[x-1] = response[indexrefined:index2]
        # print(Array[itemindex])    

        itemindex += 2
    return ExtractedInfo
        
def ExtractInfoInt():
    pass

def VarToReturn():
    pass
def DataToVar(response):
    global given_name
    global last_name
    global age
    global traits_positive
    global traits_neutral
    global traits_negative
    global college_degree
    global college_major
    global carreer
    global experience
    global strengths
    global weaknesses
    global hours

    A = ['"given-name": ','"position.original":','"last-name.original": ',',"weaknesses"','"college-degree":',',"strenghts":','"college-major":',',"college-degree":']
    ExtractedStrings = ExtractInfoString(A,response)
    for x in ExtractedStrings:
        print(x)
    # print("The requested string: ->>>>",ExtractedStrings[2], "<----")

def Endingmark(Inpt):
    if Inpt == "stop" or Inpt == "break":
        return False
    elif Inpt == "no":
        return True
    else:
        return True
    


conversation = True
while(conversation):
    request = client.text_request()
    
    Inpt = input("(To start extracting write 'break')\nEnter text here: ")
    conversation = Endingmark(Inpt)

    request.query = Inpt
    byte_response = request.getresponse().read()
    json_response = byte_response.decode('utf8').replace("'", '"') 
    # response = json.loads(json_response)
    print(json_response)
    
    
print("looks if shit works*@&*&#*@&#&*@#&*@#&")
DataToVar(json_response)

        
    

     