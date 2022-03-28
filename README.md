# aptoide-web-scrapping
Python web app that retrieves information about a specific Android application available on the Aptoide mobile application marketplace (https://en.aptoide.com/) and displays it to the user

# Proposed Solution
To tackle the challenge, i took an iterative approach for the implementation. At the first iteration, I started by implementing a small code to check the names of the needed fields and extract them. Next step would have been to implement the flask app to start creating the API. Once the app was in place and tweaked with the corresponding templates, I decided to take the search feature to a more advanced level by adding a search by name functionnality, thus giving the solution some extra flavour. To implement said feature I started doing it using the python googlesearch module which worked perfectly, however, to stay in the spirit of the challenge and to avoid using public APIs as requested in your email, I ended up re-implementing the scrapping myself. At this stage, I was mainly done with the back-end aspect of the project and nothing remained but adding some style to the app. As for the last commit, I implemented some unit tests, modified the architecture and did some code cleaning.

# To execute the unit tests
> python3 test_unittest.py

# To run the app
> python3 app.py

# To run the python type
> mypy app.py && mypy utils.py
