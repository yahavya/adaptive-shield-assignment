# adaptive-shield-assignment

Repository for the home assessment for AdaptiveShield.

_INSTRUCTIONS_:

1. Copy the repository to your machine.
2. Install all dependencies.
3. RUN THE scraper.py FILE. THIS IS CRUCIAL, BECAUSE OTHERWISE YOU WON'T BE ABLE TO SEE THE BEAUTIFUL RESULTS ON THE WEB PAGE.
4. Run "python -m flask run", this will start the flask application on 127.0.0.1:{port}. Now go to "/" and follow the instructions.

Enjoy!

Some things you should take note of:

- The result mapping of collateral adjectives to animals will be found in the RESULT.txt file.
- Images will be saved to the /tmp directory. I implemented the image downloading function to use 4 threads. The (honest) reason is that I tried 2 threads and it felt too slow. Could ramp it up if need be but this works nicely for now.
- There are animals that have no collateral adjective specified. I have purposely decided to leave them out of the mapping, since leaving them as unmapped seems contradictory to the task's objective in my opinion, but this is a personal preference and can be done otherwise if need be.
