### Postman Doc:
https://documenter.getpostman.com/view/16498899/UUy7c4fN

### Chat App Dcoumnetation

As i wasn't able to save the response of the chat endpoint fully
in postman has it is not yet supported, i will be briefly talking about the websocket endpoint to be implemted on the frontend.

1. A websocket connection should be made to the endpoint
    ws://{host}/ws/chat/{recepient_id}/
2. An authorization token should be sent in the request header
    'Authorization': 'Bearer *****'

### Example in action
#### Sender
![socket image](/req_img/sender.png)
#### Receipent
![response image](/req_img/receiver.png)
#### Sample Header
![header smaple](/req_img/headers.png)
