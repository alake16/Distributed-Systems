# Distributed-Systems
Creating a standalone program to model the creation of quiz questions and the tracking of answers from multiple users. Questions are modeled in JSON format for persistent storage. The Flask framework is used to manage communications between the front and back ends of our project.

# Development API Server Operation
To deploy the quiz responses API server, run the following command from the `app` directory:
```bash
env FLASK_APP=server.py flask run --port 5000
```

# Development API Server Operation
To deploy the application's web server, run the following command from the `app` directory:
```bash
env FLASK_APP=routes.py flask run --port 5001
```

# Unit tests
To run the unit tests you can use the Makefile
```bash
make test
```

# Contributors
Vismark Juarez (https://github.com/VismarkJuarez)
Brian Dehlinger (https://github.com/BrianDehlinger)
Daniel Palacios (https://github.com/ddpalacios)
Andrew Lake (https://github.com/alake16)

Mobile-side Android Application Repository: https://github.com/VismarkJuarez/Distributed-Systems-Mobile
