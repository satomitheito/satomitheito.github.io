function toggleDetails() {
    const details = document.getElementById('projectDetails');
    const button = document.querySelector('.show-more-btn');
  
    if (details.style.display === 'none') {
      details.style.display = 'block';
      button.textContent = 'Show Less'; // Update button text
    } else {
      details.style.display = 'none';
      button.textContent = 'Show More'; // Update button text
    }
  }