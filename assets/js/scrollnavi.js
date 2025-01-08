document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-link");
  
    const observerOptions = {
      root: null,
      threshold: 0.6, // Trigger when 60% of the section is visible
    };
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          // Remove active class from all links
          navLinks.forEach((link) => link.classList.remove("active"));
  
          // Add active class to the corresponding link
          const activeLink = document.querySelector(
            `.nav-link[href="#${entry.target.id}"]`
          );
          if (activeLink) activeLink.classList.add("active");
        }
      });
    }, observerOptions);
  
    // Observe each section
    sections.forEach((section) => observer.observe(section));
  });
  