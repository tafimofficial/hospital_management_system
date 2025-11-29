// Mobile menu toggle
document.addEventListener('DOMContentLoaded', function () {
    const burger = document.querySelector('.burger');
    const navLinks = document.querySelector('.nav-links');
    const body = document.body;

    if (burger && navLinks) {
        burger.addEventListener('click', () => {
            navLinks.classList.toggle('nav-active');
            body.classList.toggle('menu-open');

            // Animate Links
            const navItems = document.querySelectorAll('.nav-links li');
            navItems.forEach((link, index) => {
                if (link.style.animation) {
                    link.style.animation = '';
                    link.style.opacity = '0';
                    link.style.transform = 'translateX(20px)';
                } else {
                    link.style.animation = `navLinkFade 0.5s ease forwards ${index / 7 + 0.3}s`;
                }
            });

            burger.classList.toggle('toggle');
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function (event) {
            const navbar = document.querySelector('.navbar');
            if (navbar && !navbar.contains(event.target) && navLinks.classList.contains('nav-active')) {
                navLinks.classList.remove('nav-active');
                body.classList.remove('menu-open');
                burger.classList.remove('toggle');

                // Reset animations
                const navItems = document.querySelectorAll('.nav-links li');
                navItems.forEach(link => {
                    link.style.animation = '';
                    link.style.opacity = '0';
                    link.style.transform = 'translateX(20px)';
                });
            }
        });

        // Handle dropdown clicks in mobile
        const dropdowns = document.querySelectorAll('.dropdown');
        dropdowns.forEach(dropdown => {
            const dropbtn = dropdown.querySelector('.dropbtn');
            if (dropbtn) {
                dropbtn.addEventListener('click', function (e) {
                    if (window.innerWidth <= 768) {
                        e.preventDefault();
                        dropdown.classList.toggle('active');
                    }
                });
            }
        });

        // Close menu when clicking a link
        const navLinksItems = document.querySelectorAll('.nav-links a:not(.dropbtn)');
        navLinksItems.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    navLinks.classList.remove('nav-active');
                    body.classList.remove('menu-open');
                    burger.classList.remove('toggle');
                }
            });
        });
    }
});

// Animation on scroll
const fadeElements = document.querySelectorAll('.fade-in');
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const fadeInObserver = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('appear');
            fadeInObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

fadeElements.forEach(element => {
    fadeInObserver.observe(element);
});

// Auto-hide messages after 5 seconds
setTimeout(() => {
    const messages = document.querySelector('.messages');
    if (messages) {
        messages.style.opacity = '0';
        setTimeout(() => messages.remove(), 500);
    }
}, 5000);

// Notification System
if (document.getElementById('notificationBell')) {
    // Load notifications on page load
    loadNotifications();

    // Refresh notifications every 30 seconds
    setInterval(loadNotifications, 30000);

    // Mark all as read
    document.getElementById('markAllRead')?.addEventListener('click', function () {
        fetch('/api/notifications/mark-all-read/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            }
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    loadNotifications();
                }
            });
    });
}

function loadNotifications() {
    fetch('/api/notifications/')
        .then(response => response.json())
        .then(data => {
            const badge = document.getElementById('notificationBadge');
            const list = document.getElementById('notificationList');

            // Update badge
            if (data.unread_count > 0) {
                badge.textContent = data.unread_count;
                badge.style.display = 'block';
            } else {
                badge.style.display = 'none';
            }

            // Update list
            if (data.notifications.length === 0) {
                list.innerHTML = '<p style="text-align: center; padding: 20px; color: #999;">No notifications</p>';
            } else {
                list.innerHTML = data.notifications.map(n => `
                    <div class="notification-item ${n.is_read ? '' : 'unread'}" onclick="handleNotificationClick(${n.id}, '${n.link}')">
                        <div class="notification-title">${n.title}</div>
                        <div class="notification-message">${n.message}</div>
                        <div class="notification-time">${n.created_at}</div>
                    </div>
                `).join('');
            }
        })
        .catch(error => console.error('Error loading notifications:', error));
}

function handleNotificationClick(notificationId, link) {
    // Mark as read
    fetch(`/api/notifications/${notificationId}/read/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        }
    })
        .then(() => {
            loadNotifications();
            if (link && link !== '#') {
                window.location.href = link;
            }
        });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
