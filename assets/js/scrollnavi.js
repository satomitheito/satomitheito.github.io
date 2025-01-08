document.addEventListener("DOMContentLoaded", () => {
    const sections = document.querySelectorAll("section");
    const navLinks = document.querySelectorAll(".nav-link");
  
    const observerOptions = {
      root: null,
      threshold: 0.3, 
    };
  
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          navLinks.forEach((link) => link.classList.remove("active"));

          const activeLink = document.querySelector(
            `.nav-link[href="#${entry.target.id}"]`
          );

          if (entry.target.id == "header") {
            document.getElementById("navbar").style.visibility = "hidden";
          } else {
            document.getElementById("navbar").style.visibility = "visible";
          }
          
          if (activeLink) activeLink.classList.add("active");
        }
      });
    }, observerOptions);
  
    // Observe each section
    sections.forEach((section) => observer.observe(section));
  });
  