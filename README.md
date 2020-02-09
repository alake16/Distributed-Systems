# Distributed-Systems
Creating a standalone program to model the creation of quiz questions and the tracking of answers from multiple users. Questions are modeled in JSON format for persistent storage. The Flask framework is used to manage communications between the front and back ends of our project.

# Development Server Operation
To deploy the quiz responses server, run the following command from the `app` directory:
```bash
env FLASK_APP=server.py flask run
```

# Unit tests
To run the unit tests you can use the Makefile
```bash
make test
```

# Validating Phase 1 Step-by-Step

1. Clone the repository to your local environment:
```bash
git clone https://github.com/ddpalacios/Distributed-Systems.git
```

2. Once cloned, cd into the project's `app` directory and run the command `env FLASK_APP=server.py flask run`

```bash
> cd Distributed-Systems
> cd app
> env FLASK_APP=server.py flask run
```

Running the `env FLASK_APP=server.py flask run` command will start the project's server on localhost port 5000.  If executed successfully, console output should look as follows:

```bash
> env FLASK_APP=server.py flask run
 * Serving Flask app "server.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

3. The user can now create a new quiz question by making a POST request to the following endpoint: `localhost:5000/activateQuestion` with a JSON payload that conforms to the following JSON structure:

```json
{
    "type": "multiple_choice",
    "prompt": "Worst topping on pizza:",
    "choices": ["Sausage", "Pineapple", "Anchovies"],
    "answer": "Anchovies"
}
```

Below is an example cURL POST call that will successfully POST a new question.  This mimics an instructor providing a questions for his/her students to answer (This is an example of a `multiple_choice` question. The `prompt` attribute is the question, and the `choices` attribute lists the answer choices).


```bash
> curl -i \                                                                                                             
> -H "Content-Type:application/json" \                                                                                  
> -X POST \                                                                                                             
> -d '{"type": "multiple_choice", "prompt": "Worst topping on pizza:", "choices": ["Sausage", "Pineapple", "Anchovies"],
"answer": "Anchovies"}' \                                                                                               
> http://localhost:5000/activateQuestion

```

Which yields the following response: 

```bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current                                         
                                 Dload  Upload   Total   Spent    Left  Speed                                           
100   363  100   227  100   136   1075    644 --:--:-- --:--:-- --:--:--  1720HTTP/1.0 200 OK                           
Content-Type: application/json                                                                                          
Content-Length: 227                                                                                                     
Server: Werkzeug/0.16.1 Python/3.8.1                                                                                    
Date: Sun, 09 Feb 2020 05:46:29 GMT                                                                                     
                                                                                                                        
{"kind": "question", "object_id": "a900e6f0-39f6-46a5-a495-7a83a8aec266", "type": "multiple_choice", "prompt": "Worst to
pping on pizza:", "choices": ["Sausage", "Pineapple", "Anchovies"], "answer": "Anchovies", "responses": []}             
```


4. Step 3 mimics the instructor providing a question to his/her students.  Now, the student can submit an answer by submitting a POST request to the `/recordResponse` endpoint with a JSON body that conforms to the following structure:

```json
{
	"user_id": "ry539h-75fi-je84o-urijf",
	"nickname": "some-COMP439-student",
	"choice": "Anchovies"
}
```

The following cURL call submits a response for a student nicknamed `some-COMP439-student`, with an answer of `Anchovies`:

```bash
$ curl -i \
> -H "Content-Type:application/json" \
> -X POST \
> -d '{ "user_id": "ry539h-75fi-je84o-urijf", "nickname": "Still-Another-COMP439-Student", "choice": "Anchovies" }' \
> http://localhost:5000/recordResponse

```
Which yields the following response from the server:

```bash
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
  0     0    0     0    0     0      0      0 --:--:-- --:--:-- -100   210  100   102  100   108    488    516 --:--:-- --:--:-- --:--:--  1004HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 102
Server: Werkzeug/0.16.1 Python/3.8.1
Date: Sun, 09 Feb 2020 05:56:27 GMT

{"choice":"Anchovies","nickname":"Still-Another-COMP439-Student","user_id":"ry539h-75fi-je84o-urijf"}
```

To mimic additional students answering this question, the same POST request can be made to the endpoint so long as the JSON payload contains a unique `user_id` and `nickname` for each response (this simulates a different student providing each answer). This is demonstrated below:

```bash
$ curl -i \
> -H "Content-Type:application/json" \
> -X POST \
> -d '{ "user_id": "3ed4-4tww-32tedd-ur42f", "nickname": "another-COMP439-Student", "choice": "Sausage" }' \
> http://localhost:5000/recordResponse
```

5. Finally, an instructor can submit a GET request to the `/fetchResponses` endpoint to view all of the student responses.  This can be achieved as follows:

```bash
curl -i -H "Content-Type:application/json" -X GET localhost:5000/fetchResponses
```

Which will yield a list of all of the students and their answers:

```bash
[
    {
        "kind": "response",
        "type": "multiple_choice",
        "choice": "Anchovies",
        "user_id": "ry539h-75fi-je84o-urijf",
        "nickname": "some-COMP439-Student"
    },
    {
        "kind": "response",
        "type": "multiple_choice",
        "choice": "Sausage",
        "user_id": "3ed4-4tww-32tedd-ur42f",
        "nickname": "another-COMP439-Student"
    }
]
```

# Contributors
Vismark Juarez (https://github.com/VismarkJuarez)
Brian Dehlinger (https://github.com/BrianDehlinger)
Daniel Palacios (https://github.com/ddpalacios)
Andrew Lake (https://github.com/alake16)

Mobile-side Android Application Repository: https://github.com/VismarkJuarez/Distributed-Systems-Mobile
