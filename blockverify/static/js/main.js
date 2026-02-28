/**
 * ============================================
 * BlockVerify — Premium 3D Interactive JS
 * Particles, Scroll Reveal, 3D Tilt, Counters
 * ============================================
 */

document.addEventListener('DOMContentLoaded', function () {

    // ============================================
    // PARTICLE BACKGROUND
    // ============================================
    (function initParticles() {
        var canvas = document.getElementById('particles-canvas');
        if (!canvas) return;
        var ctx = canvas.getContext('2d');
        var particles = [];
        var particleCount = 60;
        var mouse = { x: null, y: null };

        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        resize();
        window.addEventListener('resize', resize);

        window.addEventListener('mousemove', function (e) {
            mouse.x = e.clientX;
            mouse.y = e.clientY;
        });

        function Particle() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = Math.random() * 2 + 0.5;
            this.speedX = (Math.random() - 0.5) * 0.5;
            this.speedY = (Math.random() - 0.5) * 0.5;
            this.opacity = Math.random() * 0.5 + 0.1;
        }

        Particle.prototype.update = function () {
            this.x += this.speedX;
            this.y += this.speedY;

            if (this.x < 0 || this.x > canvas.width) this.speedX *= -1;
            if (this.y < 0 || this.y > canvas.height) this.speedY *= -1;

            // Mouse interaction — gentle push
            if (mouse.x !== null) {
                var dx = this.x - mouse.x;
                var dy = this.y - mouse.y;
                var dist = Math.sqrt(dx * dx + dy * dy);
                if (dist < 120) {
                    this.x += dx * 0.01;
                    this.y += dy * 0.01;
                }
            }
        };

        Particle.prototype.draw = function () {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fillStyle = 'rgba(99, 102, 241, ' + this.opacity + ')';
            ctx.fill();
        };

        for (var i = 0; i < particleCount; i++) {
            particles.push(new Particle());
        }

        function connectParticles() {
            for (var a = 0; a < particles.length; a++) {
                for (var b = a + 1; b < particles.length; b++) {
                    var dx = particles[a].x - particles[b].x;
                    var dy = particles[a].y - particles[b].y;
                    var dist = Math.sqrt(dx * dx + dy * dy);
                    if (dist < 150) {
                        var opacity = (1 - dist / 150) * 0.15;
                        ctx.beginPath();
                        ctx.strokeStyle = 'rgba(99, 102, 241, ' + opacity + ')';
                        ctx.lineWidth = 0.5;
                        ctx.moveTo(particles[a].x, particles[a].y);
                        ctx.lineTo(particles[b].x, particles[b].y);
                        ctx.stroke();
                    }
                }
            }
        }

        function animate() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            particles.forEach(function (p) {
                p.update();
                p.draw();
            });
            connectParticles();
            requestAnimationFrame(animate);
        }
        animate();
    })();

    // ============================================
    // SCROLL REVEAL ANIMATIONS
    // ============================================
    (function initScrollReveal() {
        var revealElements = document.querySelectorAll('.reveal, .reveal-stagger');
        if (!revealElements.length) return;

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

        revealElements.forEach(function (el) {
            observer.observe(el);
        });
    })();

    // ============================================
    // 3D TILT ON CARDS
    // ============================================
    (function initTilt() {
        var cards = document.querySelectorAll('.feature-card, .action-card, .stat-card');
        cards.forEach(function (card) {
            card.addEventListener('mousemove', function (e) {
                var rect = card.getBoundingClientRect();
                var x = e.clientX - rect.left;
                var y = e.clientY - rect.top;
                var centerX = rect.width / 2;
                var centerY = rect.height / 2;
                var rotateX = ((y - centerY) / centerY) * -6;
                var rotateY = ((x - centerX) / centerX) * 6;
                card.style.transform = 'perspective(1000px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg) translateY(-4px)';
            });

            card.addEventListener('mouseleave', function () {
                card.style.transform = '';
            });
        });
    })();

    // ============================================
    // ANIMATED STAT COUNTERS
    // ============================================
    (function initCounters() {
        var counters = document.querySelectorAll('.stat-number');
        if (!counters.length) return;

        var animated = new Set();

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting && !animated.has(entry.target)) {
                    animated.add(entry.target);
                    var el = entry.target;
                    var target = parseInt(el.textContent, 10);
                    if (isNaN(target)) return;
                    var duration = 1500;
                    var start = 0;
                    var startTime = null;

                    function step(time) {
                        if (!startTime) startTime = time;
                        var progress = Math.min((time - startTime) / duration, 1);
                        // Ease out cubic
                        var eased = 1 - Math.pow(1 - progress, 3);
                        el.textContent = Math.floor(eased * target);
                        if (progress < 1) {
                            requestAnimationFrame(step);
                        } else {
                            el.textContent = target;
                        }
                    }
                    el.textContent = '0';
                    requestAnimationFrame(step);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(function (c) { observer.observe(c); });
    })();

    // ============================================
    // AUTO-DISMISS ALERTS
    // ============================================
    var alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px) scale(0.95)';
            setTimeout(function () {
                alert.remove();
            }, 400);
        }, 5000);
    });

    // ============================================
    // COPY HASH TO CLIPBOARD
    // ============================================
    document.querySelectorAll('.hash-text-full').forEach(function (el) {
        el.style.cursor = 'pointer';
        el.title = 'Click to copy';

        el.addEventListener('click', function () {
            var text = this.textContent.trim();
            navigator.clipboard.writeText(text).then(function () {
                var original = el.textContent;
                el.textContent = '\u2705 Copied!';
                el.style.color = '#6ee7b7';
                setTimeout(function () {
                    el.textContent = original;
                    el.style.color = '';
                }, 1500);
            }).catch(function (err) {
                console.error('Copy failed:', err);
            });
        });
    });

    // ============================================
    // FILE INPUT / DRAG-DROP ENHANCEMENT
    // ============================================
    var uploadZone = document.getElementById('upload-zone');
    if (uploadZone) {
        var fileInput = uploadZone.querySelector('input[type="file"]');
        var fileNameEl = uploadZone.querySelector('.file-name-display');

        uploadZone.addEventListener('click', function (e) {
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });

        function showFileName(name) {
            if (fileNameEl) {
                fileNameEl.textContent = '\uD83D\uDCC4 ' + name;
                fileNameEl.style.display = 'block';
            }
            uploadZone.style.borderColor = 'rgba(99, 102, 241, 0.5)';
            uploadZone.style.boxShadow = '0 0 25px rgba(99, 102, 241, 0.15)';
        }

        if (fileInput) {
            fileInput.addEventListener('change', function () {
                if (this.files.length > 0) {
                    showFileName(this.files[0].name);
                }
            });
        }

        uploadZone.addEventListener('dragover', function (e) {
            e.preventDefault();
            this.style.borderColor = 'rgba(99, 102, 241, 0.6)';
            this.style.background = 'rgba(99, 102, 241, 0.05)';
        });

        uploadZone.addEventListener('dragleave', function () {
            this.style.borderColor = '';
            this.style.background = '';
        });

        uploadZone.addEventListener('drop', function (e) {
            e.preventDefault();
            this.style.borderColor = '';
            this.style.background = '';
            if (e.dataTransfer.files.length > 0) {
                fileInput.files = e.dataTransfer.files;
                showFileName(e.dataTransfer.files[0].name);
                var event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        });
    }

    // ============================================
    // NAVBAR SCROLL EFFECT
    // ============================================
    (function initNavScroll() {
        var navbar = document.querySelector('.navbar');
        if (!navbar) return;
        window.addEventListener('scroll', function () {
            if (window.scrollY > 20) {
                navbar.style.boxShadow = '0 4px 30px rgba(0, 0, 0, 0.3)';
                navbar.style.borderBottomColor = 'rgba(255, 255, 255, 0.06)';
            } else {
                navbar.style.boxShadow = '';
                navbar.style.borderBottomColor = '';
            }
        });
    })();

    // ============================================
    // CONFIRM BEFORE LOGOUT
    // ============================================
    document.querySelectorAll('a[href*="logout"]').forEach(function (link) {
        link.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to logout?')) {
                e.preventDefault();
            }
        });
    });

    // ============================================
    // FORM FOCUS GLOW
    // ============================================
    document.querySelectorAll('.form-control, .form-select').forEach(function (input) {
        input.addEventListener('focus', function () {
            var group = this.closest('.form-group');
            if (group) group.style.transform = 'scale(1.01)';
        });
        input.addEventListener('blur', function () {
            var group = this.closest('.form-group');
            if (group) group.style.transform = '';
        });
    });

    // ============================================
    // SMOOTH PAGE LOAD 
    // ============================================
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    requestAnimationFrame(function () {
        document.body.style.opacity = '1';
    });

    console.log('\u26D3\uFE0F BlockVerify 3D loaded.');
});
