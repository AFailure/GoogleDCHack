import React, { useState } from 'react';
import {createRoot} from "react-dom";


const SurveyForm = () => {
  const [formData, setFormData] = useState({
    typeOfPlace: '',
    disabilityAccommodations: '',
    preferenceForSunlight: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const submitForm = (e) => {
    e.preventDefault();

    const submitForm = () => {
        const queryParams = new URLSearchParams({
            type_of_place: formData.typeOfPlace,
            disability_accommodations: formData.disabilityAccommodations,
            location: 'Washington, D.C.' // Example location, replace with actual location data
          }).toString();

          const url = `http://127.0.0.1:8000/api/search/?${queryParams}`;

          // Send the request to the backend using fetch or Axios
          fetch(url)
            .then(response => response.json())
            .then(data => {
              // Handle the response from the backend
              console.log(data);
            })
            .catch(error => {
              console.error('Error submitting form:', error);
            });
        };
  };

  return (
    <div>
      <h2>Survey Form</h2>
      <form onSubmit={submitForm}>
        {/* Form fields */}
        <div>
          <label htmlFor="typeOfPlace">Type of Place:</label>
          {/* Select field for type of place */}
          {/* Add more form fields as needed */}
        </div>
        <div>
          <label htmlFor="disabilityAccommodations">Disability Accommodations:</label>
          {/* Select field for disability accommodations */}
          {/* Add more form fields as needed */}
        </div>
        <div>
          <label htmlFor="preferenceForSunlight">Preference for Sunlight:</label>
          {/* Select field for preference for sunlight */}
          {/* Add more form fields as needed */}
        </div>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

// render(<SurveyForm />, document.getElementById('surveyDiv'));
createRoot(document.getElementById('surveyDiv')).render(<SurveyForm />);

export default SurveyForm;
