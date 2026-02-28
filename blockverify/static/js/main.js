/**
 * ============================================
 * BlockVerify — Main JavaScript
 * Blockchain-Based Certificate Verification
 * ============================================
 */

document.addEventListener('DOMContentLoaded', function () {

    // ============================================
    // AUTO-DISMISS ALERTS
    // ============================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.opacity = '0';
            alert.style.transform = 'translateY(-10px)';
            setTimeout(function () {
                alert.remove();
            }, 300);
        }, 5000); // Dismiss after 5 seconds
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
                // Show feedback
                var original = el.textContent;
                el.textContent = 'Copied!';
                el.style.color = '#22c55e';
                setTimeout(function () {
                    el.textContent = original;
                    el.style.color = '';
                }, 1500);
            }).catch(function (err) {
                console.error('Failed to copy:', err);
            });
        });
    });

    // ============================================
    // FILE INPUT ENHANCEMENT
    // ============================================
    var uploadZone = document.getElementById('upload-zone');
    if (uploadZone) {
        var fileInput = uploadZone.querySelector('input[type="file"]');

        // Click zone to trigger file input
        uploadZone.addEventListener('click', function (e) {
            if (e.target !== fileInput) {
                fileInput.click();
            }
        });

        // Drag and drop support
        uploadZone.addEventListener('dragover', function (e) {
            e.preventDefault();
            this.style.borderColor = '#4f46e5';
            this.style.background = '#f5f3ff';
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
                // Trigger change event
                var event = new Event('change', { bubbles: true });
                fileInput.dispatchEvent(event);
            }
        });
    }

    // ============================================
    // CONFIRM BEFORE LOGOUT
    // ============================================
    var logoutLinks = document.querySelectorAll('a[href*="logout"]');
    logoutLinks.forEach(function (link) {
        link.addEventListener('click', function (e) {
            if (!confirm('Are you sure you want to logout?')) {
                e.preventDefault();
            }
        });
    });

    // ============================================
    // HASH TRUNCATION TOOLTIPS
    // ============================================
    document.querySelectorAll('.hash-text[title]').forEach(function (el) {
        el.style.cursor = 'help';
    });

    // ============================================
    // FORM VALIDATION HINTS
    // ============================================
    document.querySelectorAll('form').forEach(function (form) {
        form.addEventListener('submit', function () {
            var requiredEmpty = false;
            form.querySelectorAll('[required]').forEach(function (input) {
                if (!input.value.trim()) {
                    requiredEmpty = true;
                    input.style.borderColor = '#ef4444';
                }
            });
            if (requiredEmpty) {
                // Browser default validation will handle it
            }
        });
    });

    console.log('BlockVerify JS loaded successfully.');
});
