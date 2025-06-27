// Theme Toggle Functionality
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = themeToggle.querySelector('.theme-icon');
const body = document.body;

// Animated Tab Title
function animateTabTitle() {
    const fullTitle = "Satomi Ito";
    const pauseDuration = 2000; // 2 seconds pause when complete
    const typingSpeed = 110; // milliseconds between each character
    
    let currentIndex = 0;
    let isDeleting = false;
    let isPausing = false;
    
    function typeTitle() {
        if (isPausing) {
            setTimeout(() => {
                isPausing = false;
                isDeleting = true;
                typeTitle();
            }, pauseDuration);
            return;
        }
        
        if (!isDeleting && currentIndex <= fullTitle.length) {
            const currentTitle = fullTitle.substring(0, currentIndex);
            document.title = currentTitle || "S"; // Start with "S" instead of empty
            currentIndex++;
            
            if (currentIndex > fullTitle.length) {
                isPausing = true;
            }
            
            setTimeout(typeTitle, typingSpeed);
        } else if (isDeleting && currentIndex > 0) { // Changed >= 0 to > 0
            currentIndex--;
            const currentTitle = fullTitle.substring(0, currentIndex);
            document.title = currentTitle || "S"; // Keep "S" as minimum
            
            if (currentIndex <= 0) {
                isDeleting = false;
                currentIndex = 1; // Start from 1 instead of 0, so we keep the "S"
            }
            
            setTimeout(typeTitle, typingSpeed / 2); // Faster deletion
        }
    }
    
    // Set initial title to "S" to prevent domain showing
    document.title = "S";
    currentIndex = 1; // Start from "S"
    typeTitle();
}

// Start tab title animation immediately and override any default title
document.addEventListener('DOMContentLoaded', () => {
    // Immediately set title to prevent showing domain
    document.title = "S";
    
    // Start animation after a short delay
    setTimeout(animateTabTitle, 500);
});

// Also start on window load as backup
window.addEventListener('load', () => {
    if (document.title === "S" || document.title.includes("github.io") || document.title === " ") {
        setTimeout(animateTabTitle, 100);
    }
});

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';
body.setAttribute('data-theme', currentTheme);

// Update theme icon based on current theme
function updateThemeIcon(theme) {
    themeIcon.textContent = theme === 'dark' ? '☀️' : '🌙';
}

// Initialize theme icon
updateThemeIcon(currentTheme);

// Theme toggle event listener
themeToggle.addEventListener('click', () => {
    const currentTheme = body.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    body.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);
});

// Navigation Active State Management
const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('section[id]');

// Function to update active navigation link
function updateActiveNavLink() {
    let current = '';
    const scrollPosition = window.scrollY + 100; // Add offset for better detection
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        // Check if current scroll position is within this section
        if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });
    
    // If we're at the bottom of the page, make sure contact is active
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight - 10) {
        current = 'contact';
    }
    
    // If no section is detected, default to home
    if (!current) {
        current = 'home';
    }
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

// Update active nav link on scroll
window.addEventListener('scroll', updateActiveNavLink);

// Smooth scroll for navigation links
navLinks.forEach(link => {
    link.addEventListener('click', (e) => {
        const targetId = link.getAttribute('href');
        
        // Skip smooth scroll for external links (like PDF files)
        if (!targetId.startsWith('#')) {
            return; // Let the default behavior handle external links
        }
        
        e.preventDefault();
        const targetSection = document.querySelector(targetId);
        
        if (targetSection) {
            const offsetTop = targetSection.offsetTop - 80; // Account for fixed navbar
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Removed scroll shadow effect from navbar
// let lastScrollTop = 0;
// const navbar = document.querySelector('.navbar');
// 
// window.addEventListener('scroll', () => {
//     const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
//     
//     // Add/remove shadow based on scroll position
//     if (scrollTop > 10) {
//         navbar.style.boxShadow = '0 2px 20px rgba(0, 0, 0, 0.1)';
//     } else {
//         navbar.style.boxShadow = 'none';
//     }
//     
//     lastScrollTop = scrollTop;
// });

// Add loading animation
window.addEventListener('load', () => {
    body.style.opacity = '0';
    body.style.transition = 'opacity 0.5s ease-in-out';
    
    setTimeout(() => {
        body.style.opacity = '1';
    }, 100);
});

// Sequential reveal animation
document.addEventListener('DOMContentLoaded', () => {
    const navbar = document.querySelector('.navbar');
    const heroSubtitle = document.querySelector('.hero-subtitle');
    const heroTitle = document.querySelector('.hero-title');
    const themeToggle = document.querySelector('.theme-toggle');
    
    // Show navigation, subtitle, and theme toggle after typing animation completes
    setTimeout(() => {
        if (navbar) {
            navbar.classList.add('show');
        }
        if (heroSubtitle) {
            heroSubtitle.classList.add('show');
        }
        if (themeToggle) {
            themeToggle.classList.add('show');
        }
        
        // Remove cursor after revealing other elements
        if (heroTitle) {
            heroTitle.classList.add('typing-complete');
        }
    }, 3200); // 0.5s delay + 2s animation + 0.7s buffer for smooth transition
});

// Add intersection observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Parallax Effect for Hero Section
function parallaxEffect() {
    const scrolled = window.pageYOffset;
    const heroSection = document.querySelector('.hero-section');
    const heroTitle = document.querySelector('.hero-title');
    
    if (heroSection) {
        const heroSectionTop = heroSection.offsetTop;
        const heroSectionHeight = heroSection.offsetHeight;
        
        // Only apply parallax when hero section is visible
        if (scrolled <= heroSectionHeight) {
            // Parallax for hero title (slower movement)
            if (heroTitle) {
                const titleParallax = scrolled * 0.5;
                heroTitle.style.transform = `translateY(${titleParallax}px) translateZ(0)`;
            }
        }
    }
}

// Throttle function for better performance
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    }
}

// Add parallax effect on scroll
window.addEventListener('scroll', throttle(parallaxEffect, 16)); // ~60fps

// Observe sections for animations
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.hero-section, .connect-section');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(20px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });
    
    // Initialize parallax effect
    parallaxEffect();
}); 