import React, { useState } from 'react';
import axios from 'axios';

const SearchBar = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);

  // Function to handle search query and fetch results
  const handleSearch = async () => {
    try {
      const response = await axios.post('http://localhost:5000/search', { query });
      setResults(response.data.results);
    } catch (error) {
      console.error('Error searching:', error);
    }
  };

  return (
    <div>
      <input
        type="text"
        placeholder="Enter your search query...."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>

      {/* Display search results if available */}
      {results.length > 0 && (
        <div>
          <h2>Search Results</h2>
          <ol style={{ listStylePosition: 'inside', paddingLeft: 0 }}>
            {results.map((result, index) => (
              <li key={index} style={{ marginBottom: '10px' }}>
                <a
                  href={result[0]}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{ color: 'white', textDecoration: 'none' }}
                >
                  {result[0]}
                </a>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
};

export default SearchBar;
