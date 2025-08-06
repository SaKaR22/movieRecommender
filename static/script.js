document.addEventListener('DOMContentLoaded', function() {
    const recommendBtn = document.getElementById('recommend-btn');
    const movieInput = document.getElementById('movie-input');
    const resultsDiv = document.getElementById('results');
    const inputTitle = document.getElementById('input-title');
    const recommendationsList = document.getElementById('recommendations-list');
    
    recommendBtn.addEventListener('click', getRecommendations);
    movieInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            getRecommendations();
        }
    });
    
    function getRecommendations() {
        const title = movieInput.value.trim();
        if (!title) return;
        
        // Show loading state
        recommendationsList.innerHTML = '<div class="loading">Finding recommendations...</div>';
        
        fetch('/recommend', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: `movie_title=${encodeURIComponent(title)}`
        })
        .then(response => response.json())
        .then(data => {
            displayRecommendations(data);
        })
        .catch(error => {
            recommendationsList.innerHTML = '<div class="error">Error fetching recommendations. Please try again.</div>';
            console.error('Error:', error);
        });
    }
    
    function displayRecommendations(data) {
        recommendationsList.innerHTML = '';
        
        if (data.recommendations.length === 0) {
            recommendationsList.innerHTML = '<div class="error">No recommendations found. Try another movie.</div>';
            return;
        }
        
        // Show the input movie
        inputTitle.textContent = data.input;
        document.querySelector('.input-movie').style.display = 'block';
        
        // Display recommendations
        data.recommendations.forEach(movie => {
            const movieCard = document.createElement('div');
            movieCard.className = 'movie-card';
            
            if (movie.match) {
                movieCard.innerHTML = `
                    <div class="match-suggestion">${movie.match}</div>
                    <div class="movie-title">${movie.title}</div>
                `;
            } else {
                movieCard.innerHTML = `
                    <div class="movie-title">${movie.title}</div>
                    <div class="movie-meta">
                        ${movie.genres ? 'Genres: ' + movie.genres : ''}<br>
                        ${movie.director ? 'Director: ' + movie.director : ''}
                    </div>
                `;
            }
            
            recommendationsList.appendChild(movieCard);
        });
    }
});