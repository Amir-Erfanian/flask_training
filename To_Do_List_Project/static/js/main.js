// Auto-dismiss alerts after 3 seconds
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 3000);
    });
});

// Confirm before clearing completed todos
document.addEventListener('DOMContentLoaded', function() {
    const clearCompletedBtn = document.querySelector('a[href*="clear-completed"]');
    if (clearCompletedBtn) {
        clearCompletedBtn.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete all completed todos? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    }
});

// Enable form validation styling
(function() {
    'use strict';
    window.addEventListener('load', function() {
        var forms = document.getElementsByClassName('needs-validation');
        Array.prototype.filter.call(forms, function(form) {
            form.addEventListener('submit', function(event) {
                if (form.checkValidity() === false) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }, false);
})();

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + N to focus on new todo title
    if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
        e.preventDefault();
        const titleInput = document.getElementById('title');
        if (titleInput) {
            titleInput.focus();
        }
    }
});

// Character counter for title
document.addEventListener('DOMContentLoaded', function() {
    const titleInput = document.getElementById('title');
    if (titleInput) {
        titleInput.addEventListener('input', function() {
            const maxLength = 100;
            const currentLength = this.value.length;
            
            if (currentLength > maxLength * 0.9) {
                this.style.borderColor = '#ffc107';
            } else {
                this.style.borderColor = '';
            }
        });
    }
});