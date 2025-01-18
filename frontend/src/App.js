import React, { useState } from 'react';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [urlInput, setUrlInput] = useState('');

  // Handle the URL input field change
  const handleInputChange = (e) => {
    setUrlInput(e.target.value);  // Update state with input field value
  };

  // Function to handle URL submission
  const handleUrlSubmit = () => {
    setMessage("Crawling started...");

    // Send the URL as a POST request to the backend
    fetch('http://127.0.0.1:8000/url/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url: urlInput }),  // Send the URL input to the backend
    })
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }

        // If the response is successful, start fetching the crawl data
        fetch('http://127.0.0.1:8000/crawl/?url=' + urlInput)
          .then(response => {
            if (!response.ok) {
              throw new Error(`HTTP error! Status: ${response.status}`);
            }

            // Handle the stream of data
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let result = '';
            let buffer = '';

            reader.read().then(function processText({ done, value }) {
              if (done) {
                // If done, try parsing the final chunk before finishing
                if (buffer) {
                  try {
                    const jsonData = JSON.parse(buffer);
                    setMessage(prev => prev + JSON.stringify(jsonData) + "\n");
                  } catch (error) {
                    console.error('Error parsing final chunk:', error);
                  }
                }
                return;
              }

              // Add the new chunk to the buffer
              buffer += decoder.decode(value, { stream: true });

              // Try parsing the buffer for any complete JSON objects
              try {
                // Attempt to parse the buffer as JSON
                while (buffer) {
                  // Try parsing one JSON object at a time
                  const index = buffer.indexOf('\n');  // Split by newline
                  if (index === -1) break;  // No full object yet

                  const item = buffer.slice(0, index);  // Get the full JSON object
                  buffer = buffer.slice(index + 1);  // Update buffer for the next data

                  // Parse and update UI with each item
                  const jsonData = JSON.parse(item);
                  setMessage(prev => prev + JSON.stringify(jsonData) + "\n");
                }
              } catch (error) {
                console.error('Error parsing chunk:', error);
              }

              reader.read().then(processText);  // Continue reading the stream
            });
          })
          .catch(error => {
            console.error('Error:', error);
            setMessage(`Error submitting URL: ${error.message}`);
          });
      })
      .catch(error => {
        console.error('Error:', error);
        setMessage(`Error submitting URL: ${error.message}`);
      });
  };

  return (
    <div className="App">
      <p>{message}</p>
        // data passing
      <div>
        <input
          type="url"
          value={urlInput}
          onChange={handleInputChange}
          placeholder="Enter a URL"
        />
        <button onClick={handleUrlSubmit}>Submit URL</button>
      </div>
    </div>
  );
}

export default App;
