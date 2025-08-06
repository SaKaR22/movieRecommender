from flask import Flask, render_template, request, jsonify
from model.recommender import MovieRecommender
import os

app = Flask(__name__)

# Initialize recommender
recommender = MovieRecommender()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    movie_title = request.form['movie_title']
    recommendations = recommender.get_recommendations(movie_title)
    return jsonify({
        "input": movie_title,
        "recommendations": recommendations.to_dict('records')
    })

if __name__ == '__main__':
    app.run(debug=True)