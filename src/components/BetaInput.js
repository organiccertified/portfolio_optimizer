import React from 'react';

function BetaInput({ value, onChange }) {
  const handleChange = (e) => {
    const inputValue = e.target.value;
    // Allow empty string, decimal point, and numbers
    if (inputValue === '' || /^\d*\.?\d*$/.test(inputValue)) {
      onChange(inputValue);
    }
  };

  const handleBlur = () => {
    // Convert to float and validate on blur
    const floatValue = parseFloat(value);
    if (isNaN(floatValue) || floatValue < 0) {
      onChange('0.1');
    } else {
      onChange(floatValue.toString());
    }
  };

  return (
    <div className="beta-input">
      <label>Beta Risk</label>
             <input
         type="text"
         placeholder="0.95"
         value={value}
         onChange={handleChange}
         onBlur={handleBlur}
         className="beta-input-field"
       />
    </div>
  );
}

export default BetaInput;
