function toggleDetails(id) {
    const details = document.getElementById(id);
    const button = details.previousElementSibling;
  
    if (details.style.display === 'none') {
      details.style.display = 'block';
      button.textContent = 'Read Less'; 
    } else {
      details.style.display = 'none';
      button.textContent = 'Read More'; 
    }
  }
  