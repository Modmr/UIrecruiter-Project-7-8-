import apiai
import json

access_token = "be72d4a27ad74a288cf3ba3d16fbdacc"
client = apiai.ApiAI(access_token)
request = client.text_request()

conversation = True
while(conversation):
    Inpt = input("Enter text here: ")
    request.query = Inpt 

    # try:
    byte_response = request.getresponse().read()
    json_response = byte_response.decode('utf8').replace("'", '"') 
    response = json.loads(json_response)

    print(json_response)
        
    # except:
    #     print ("Oops there was a error")
    #     cont = input("continue conversation? (Yes or No) : ")
    #     if cont == "yes" or cont== "y":
    #         conversation = True
    #     else:
    #         conversation = False
        
    

     

