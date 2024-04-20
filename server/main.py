# from flask_pymongo import PyMongo
# from flask import Flask, request, jsonify
# from youtube_transcript_api import YouTubeTranscriptApi  # Refer to documentation for installation
# from googletrans import Translator
# from langdetect import detect
# from deep_translator import GoogleTranslator
# from flask_cors import CORS
# import google.generativeai as genai
# genai.configure(api_key="AIzaSyDJLxPGxm3pnfYCYmfBy56GYxoD3GNVIz4")
# from IPython.display import Markdown
# import json
# import jwt
# import datetime

# app = Flask(__name__)
# CORS(app)
# app.config["MONGO_URI"] = "mongodb://localhost:27017/YoutubeQuiz"  # Adjust connection string if needed
# db = PyMongo(app).db

# app.config['SECRET_KEY'] = 'your_secret_key_here'

# @app.route("/get_transcript", methods=["POST"])
# def get_transcript_and_translate():
#     try:
#         # Retrieve video ID from JSON request
#         video_id = request.json.get('video_id')
#         print(video_id)

#             # return jsonify({"error": "Missing video ID in request data"}), 400

#         # Define language codes for transcript search
#         language_codes = [
#       "af", "ak", "sq", "am", "ar", "hy", "as", "ay", "az", "bn", 
#       "eu", "be", "bho", "bs", "bg", "my", "ca", "ceb", "zh-Hans", 
#       "zh-Hant", "co", "hr", "cs", "da", "dv", "nl", "en", "eo", 
#       "et", "ee", "fil", "fi", "fr", "gl", "lg", "ka", "de", "el", 
#       "gn", "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", 
#       "ig", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", 
#       "ko", "kri", "ku", "ky", "lo", "la", "lv", "ln", "lt", "lb", 
#       "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "ne", "nso", 
#       "no", "ny", "or", "om", "ps", "fa", "pl", "pt", "pa", "qu", 
#       "ro", "ru", "sm", "sa", "gd", "sr", "sn", "sd", "si", "sk", 
#       "sl", "so", "st", "es", "su", "sw", "sv", "tg", "ta", "tt", 
#       "te", "th", "ti", "ts", "tr", "tk", "uk", "ur", "ug", "uz", 
#       "vi", "cy", "fy", "xh", "yi", "yo", "zu"]

#         # Fetch transcript using YouTubeTranscriptApi
#         transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=language_codes)

#         print(transcript)

#         if transcript:
#             model = genai.GenerativeModel('gemini-pro')
#             transcript_text = ' '.join([text['text'] for text in transcript])
#             transcript_text = transcript_text[:1000]
#             # prompt=transcript_text+
#             prompt = transcript_text+"Please make quiz of more than three questions from this text in the json format like \"{ \"quiz\": { \"title\": \"Geography Quiz\", \"description\": \"Test your knowledge on geography!\", \"length\":3, \"questions\": [ { \"question\": \"What is the capital of France?\", \"options\": [ \"Madrid\", \"Paris\", \"London\", \"Berlin\" ], \"answer\": \"Paris\" }, { \"question\": \"Which continent is Brazil located in?\", \"options\": [ \"North America\", \"South America\", \"Europe\", \"Asia\" ], \"answer\": \"South America\" }, { \"question\": \"What is the largest country in the world by land area?\", \"options\": [ \"United States\", \"China\", \"Russia\", \"Canada\" ], \"answer\": \"Russia\" } ] } }"
#             # prompt=transcript_text+""" 
#             #     so this is the text give to you and below is the formate of json object that i need
#             #     {
#             #     "quiz": {
#             #         "title": "Geography Quiz",
#             #         "description": "Test your knowledge on geography!",
#             #         "length":3,
#             #         "questions": [
#             #         {
#             #             "question": "What is the capital of France?",
#             #             "options": [
#             #             "Madrid",
#             #             "Paris",
#             #             "London",
#             #             "Berlin"
#             #             ],
#             #             "answer": "Paris",
#             #             "start":0,
#             #             "end":10
#             #         },
#             #         {
#             #             "question": "Which continent is Brazil located in?",
#             #             "options": [
#             #             "North America",
#             #             "South America",
#             #             "Europe",
#             #             "Asia"
#             #             ],
#             #             "answer": "South America",
#             #             "start":20,
#             #             "end":30
#             #         },
#             #         {
#             #             "question": "What is the largest country in the world by land area?",
#             #             "options": [
#             #             "United States",
#             #             "China",
#             #             "Russia",
#             #             "Canada",
#             #             "start":25,
#             #             "end":50
#             #             ],
#             #             "answer": "Russia"
#             #         }
#             #         ]
#             #     }
#             #     } 
                
#             #     generate 5 MCQs in the form of above where start and end is that from which word index(not string index) to which index MCQ is being picked up and make sure that that duration is correct because i am dependet on it Give me in json format only""" 
#             response = model.generate_content(prompt)
#             print(response)
#             print(type(response))
#             # print(response.res÷÷ult)
#             # Extract the MCQs from the response
#             generated_content = response.text
#             mcqs_start_index = generated_content.find("{")
#             mcqs_end_index = generated_content.rfind("}") + 1
#             mcqs_json = generated_content[mcqs_start_index:mcqs_end_index]
#             # Convert MCQs to JSON format
#             mcqs_dict = json.loads(mcqs_json)
#             print(type(mcqs_dict))
#             # Return MCQs in JSON format
#             return jsonify({"mcqs": mcqs_dict})
#             Markdown(response)

#             print(response)
#             # Combine transcript text
#             transcript_text = ' '.join([text['text'] for text in transcript])
#             transcript_text=transcript_text[:1000]
            
#             # Detect source language
#             source_language = detect(transcript_text)
#             print(source_language)
#             # Translate to English using GoogleTranslator
#             translator = GoogleTranslator(source=source_language, target='en')
#             translated_transcript = translator.translate(transcript_text)

#             # If deep_translator returns a string, convert it to an object for consistency
#             if isinstance(translated_transcript, str):
#                 translated_transcript = {'text': translated_transcript}

#             # Return response with transcript and translation in JSON format
#             return jsonify({
#                 "transcript": transcript_text,
#                 "translated_transcript": translated_transcript
#             })
#         else:
#             return jsonify({"message": "Transcript not available in supported languages"}), 404

#     except Exception as e:
#         print(f"An error occurred: {e}")
#         return jsonify({"error": str(e)}), 500


# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         data = request.json
#         name = data.get('name')
#         email = data.get('email')
#         password = data.get('password')
        
#         if db.users.find_one({'email': email}):
#             return jsonify({'error': 'Username already exists'}), 400
#         new_user = {'name':name, 'email': email, 'password': password}
#         db.users.insert_one(new_user)
#         return jsonify({'message': 'Signup successful'}), 201
#     else:
#         return 'Please login.'
    

# @app.route('/login', methods=['POST'])
# def login():
#     try:

#         # Get username and password from request data
#         data = request.json
#         email = data.get('email')
#         password = data.get('password')

#         # Query MongoDB to find user
#         user = db.users.find_one({'email': email})

#         if user:
#             # Check if passwords match
#             if user['password'] == password:
#                 # Successful login
#                 return jsonify({'message': 'Login successful', 'user_id': str(user['_id'])}), 200
#             else:
#                 # Incorrect password
#                 return jsonify({'error': 'Incorrect password'}), 401
#         else:
#             # User not found
#             return jsonify({'error': 'User not found'}), 400
#     except Exception as e:
#         return jsonify({'error': 'An error occurred during login'}), 500

# if __name__ == "__main__":
#     app.run(debug=True, port=8080)




from flask_pymongo import PyMongo
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi  # Refer to documentation for installation
from googletrans import Translator
from langdetect import detect
from deep_translator import GoogleTranslator
from flask_cors import CORS
import google.generativeai as genai
genai.configure(api_key="AIzaSyDJLxPGxm3pnfYCYmfBy56GYxoD3GNVIz4")
from IPython.display import Markdown
import json
import jwt
import datetime
from datetime import timezone  # Import timezone


app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/YoutubeQuiz"  # Adjust connection string if needed
app.config['SECRET_KEY'] = 'your_secret_key_here'
db = PyMongo(app).db

app.config['SECRET_KEY'] = 'your_secret_key_here'

@app.route("/get_transcript", methods=["POST"])
def get_transcript_and_translate():
    try:
        # Retrieve video ID from JSON request
        video_id = request.json.get('video_id')
        print(video_id)

            # return jsonify({"error": "Missing video ID in request data"}), 400

        # Define language codes for transcript search
        language_codes = [
      "af", "ak", "sq", "am", "ar", "hy", "as", "ay", "az", "bn", 
      "eu", "be", "bho", "bs", "bg", "my", "ca", "ceb", "zh-Hans", 
      "zh-Hant", "co", "hr", "cs", "da", "dv", "nl", "en", "eo", 
      "et", "ee", "fil", "fi", "fr", "gl", "lg", "ka", "de", "el", 
      "gn", "gu", "ht", "ha", "haw", "iw", "hi", "hmn", "hu", "is", 
      "ig", "id", "ga", "it", "ja", "jv", "kn", "kk", "km", "rw", 
      "ko", "kri", "ku", "ky", "lo", "la", "lv", "ln", "lt", "lb", 
      "mk", "mg", "ms", "ml", "mt", "mi", "mr", "mn", "ne", "nso", 
      "no", "ny", "or", "om", "ps", "fa", "pl", "pt", "pa", "qu", 
      "ro", "ru", "sm", "sa", "gd", "sr", "sn", "sd", "si", "sk", 
      "sl", "so", "st", "es", "su", "sw", "sv", "tg", "ta", "tt", 
      "te", "th", "ti", "ts", "tr", "tk", "uk", "ur", "ug", "uz", 
      "vi", "cy", "fy", "xh", "yi", "yo", "zu"]

        # Fetch transcript using YouTubeTranscriptApi
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=language_codes)

        print(transcript)

        if transcript:
            model = genai.GenerativeModel('gemini-pro')
            transcript_text = ' '.join([text['text'] for text in transcript])
            transcript_text = transcript_text[:1000]
            # prompt=transcript_text+
            prompt = transcript_text+"Please make quiz of more than three questions from this text in the json format like \"{ \"quiz\": { \"title\": \"Geography Quiz\", \"description\": \"Test your knowledge on geography!\", \"length\":3, \"questions\": [ { \"question\": \"What is the capital of France?\", \"options\": [ \"Madrid\", \"Paris\", \"London\", \"Berlin\" ], \"answer\": \"Paris\" }, { \"question\": \"Which continent is Brazil located in?\", \"options\": [ \"North America\", \"South America\", \"Europe\", \"Asia\" ], \"answer\": \"South America\" }, { \"question\": \"What is the largest country in the world by land area?\", \"options\": [ \"United States\", \"China\", \"Russia\", \"Canada\" ], \"answer\": \"Russia\" } ] } }"
            # prompt=transcript_text+""" 
            #     so this is the text give to you and below is the formate of json object that i need
            #     {
            #     "quiz": {
            #         "title": "Geography Quiz",
            #         "description": "Test your knowledge on geography!",
            #         "length":3,
            #         "questions": [
            #         {
            #             "question": "What is the capital of France?",
            #             "options": [
            #             "Madrid",
            #             "Paris",
            #             "London",
            #             "Berlin"
            #             ],
            #             "answer": "Paris",
            #             "start":0,
            #             "end":10
            #         },
            #         {
            #             "question": "Which continent is Brazil located in?",
            #             "options": [
            #             "North America",
            #             "South America",
            #             "Europe",
            #             "Asia"
            #             ],
            #             "answer": "South America",
            #             "start":20,
            #             "end":30
            #         },
            #         {
            #             "question": "What is the largest country in the world by land area?",
            #             "options": [
            #             "United States",
            #             "China",
            #             "Russia",
            #             "Canada",
            #             "start":25,
            #             "end":50
            #             ],
            #             "answer": "Russia"
            #         }
            #         ]
            #     }
            #     } 
                
            #     generate 5 MCQs in the form of above where start and end is that from which word index(not string index) to which index MCQ is being picked up and make sure that that duration is correct because i am dependet on it Give me in json format only""" 
            response = model.generate_content(prompt)
            print(response)
            print(type(response))
            # print(response.res÷÷ult)
            # Extract the MCQs from the response
            generated_content = response.text
            mcqs_start_index = generated_content.find("{")
            mcqs_end_index = generated_content.rfind("}") + 1
            mcqs_json = generated_content[mcqs_start_index:mcqs_end_index]
            # Convert MCQs to JSON format
            mcqs_dict = json.loads(mcqs_json)
            print(type(mcqs_dict))
            # Return MCQs in JSON format
            return jsonify({"mcqs": mcqs_dict})
            Markdown(response)

            print(response)
            # Combine transcript text
            transcript_text = ' '.join([text['text'] for text in transcript])
            transcript_text=transcript_text[:1000]
            
            # Detect source language
            source_language = detect(transcript_text)
            print(source_language)
            # Translate to English using GoogleTranslator
            translator = GoogleTranslator(source=source_language, target='en')
            translated_transcript = translator.translate(transcript_text)

            # If deep_translator returns a string, convert it to an object for consistency
            if isinstance(translated_transcript, str):
                translated_transcript = {'text': translated_transcript}

            # Return response with transcript and translation in JSON format
            return jsonify({
                "transcript": transcript_text,
                "translated_transcript": translated_transcript
            })
        else:
            return jsonify({"message": "Transcript not available in supported languages"}), 404

    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.json
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        
        if db.users.find_one({'email': email}):
            return jsonify({'error': 'Username already exists'}), 400
        new_user = {'name':name, 'email': email, 'password': password}
        db.users.insert_one(new_user)
        return jsonify({'message': 'Signup successful'}), 201
    else:
        return 'Please login.'
    

# Secret key used to sign the token (keep this secret and don't expose it)



@app.route('/login', methods=['POST'])
def login():
    try:
        # Get email and password from request data
        data = request.json
        email = data.get('email')
        password = data.get('password')

        # Query MongoDB to find user
        user = db.users.find_one({'email': email})

        if user:
            # Check if passwords match
            if user['password'] == password:
                return jsonify({"success": "Ok"})

                # return jsonify({'': access_token})
            else:
                # Incorrect password
                return jsonify({'error': 'Incorrect password'}), 401
        else:
            # User not found
            return jsonify({'error': 'User not found'}), 400
        


    except Exception as e:
        return jsonify({'error': 'An error occurred during login'}), 500
    
    @app.route('/quiz', methods=['POST'])
    def quiz():
    try:
        # Get email and password from request data
        data = request.json
        youtube_id = data.get('')
        question_id= data.get('')
        user_id=data.get('email')

        # Query MongoDB to find user
        user = db.users.find_one({'email': email})

        if user:
            # Check if passwords match
            # if user['password'] == password:
            #     return jsonify({"success": "Ok"})
                return jsonify({"":""})
                # return jsonify({'': access_token})
            # else:
            #     # Incorrect password
            #     return jsonify({'error': 'Incorrect password'}), 401
        else:
            # User not found
            return jsonify({'error': 'User not found'}), 400
        

        
    except Exception as e:
        return jsonify({'error': 'An error occurred during login'}), 500
    

if __name__ == '__main__':
    app.run(debug=True,port=8080)