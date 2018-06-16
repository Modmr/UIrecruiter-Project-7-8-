import apiai
import json
from colorama import init, Fore, Back, Style
init()


access_token = "be72d4a27ad74a288cf3ba3d16fbdacc"
client = apiai.ApiAI(access_token)
# request = client.text_request()

def cprint(msg, foreground = "black", background = "white"):
    fground = foreground.upper()
    bground = background.upper()
    style = getattr(Fore, fground) + getattr(Back, bground)
    print(style + msg + Style.RESET_ALL)



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



def DataToVar(Data):
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

    given_name = Data.get("given-name")
    last_name = Data.get("last-name")
    college_degree = Data.get("college-degree")
    college_major = Data.get("college-major")
    carreer = Data.get("position")
    age = Data.get("age.original")
    # experience = 
    hours = Data.get("hours")
    traits_positive = Data.get("traits-positive")
    traits_neutral = Data.get("traits-neutral")
    traits_negative = Data.get("traits-negative")
    strengths = Data.get("strengths")
    weaknesses = Data.get("weaknesses")

    print("name: ",given_name)
    print(last_name)
    print("degree: ",college_degree)
    print(hours)
    print("age: ",age)
    print(weaknesses)


def Endingmark(Inpt):
    if Inpt == "stop" or Inpt == "break":
        return False
    elif Inpt == "no":
        return True
    else:
        return True
    

cprint("(To start extracting write 'break')","red","yellow")
conversation = True
while(conversation):
    request = client.text_request()
    
    Inpt = input("Enter text here: ")
    conversation = Endingmark(Inpt)

    request.query = Inpt
    byte_response = request.getresponse().read()
    json_response = byte_response.decode('utf8').replace("'", '"') 
    response = json.loads(json_response)
    cprint(response["result"]["fulfillment"]["speech"],"green","black")
    
    # print("looks if shit works*@&*&#*@&#&*@#&*@#&")
    
    dataparameters = response["result"]["contexts"][0]["parameters"]
    # print(dataparameters.get("college-degree"))

DataToVar(dataparameters)
    
    


        
    

     