function toggleDetails(id) {
    const details = document.getElementById(id);
    const button = details.previousElementSibling;
  
    if (details.style.display === 'none') {
      details.style.display = 'block';
      button.textContent = 'Show Less'; // Update button text
    } else {
      details.style.display = 'none';
      button.textContent = 'Show More'; // Update button text
    }
  }
  