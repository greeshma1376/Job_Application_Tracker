/**
 * Job & Internship Application Tracker - JavaScript AJAX Fetch Handler
 * Features: AJAX Task Completion & Task Deletion
 */

document.addEventListener('DOMContentLoaded', function() {
    // Utility function to retrieve CSRF token
    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta && meta.content) {
            return meta.content;
        }
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, 10) === ('csrftoken=')) {
                    cookieValue = decodeURIComponent(cookie.substring(10));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Update Dashboard Stats Counters dynamically
    function updateStats(type, delta) {
        const el = document.getElementById(`stat-${type}`);
        if (el) {
            let current = parseInt(el.textContent) || 0;
            el.textContent = Math.max(0, current + delta);
        }
    }

    // Check if cards container is empty and show empty state if needed
    function checkEmptyState() {
        const container = document.getElementById('applications-container');
        if (container) {
            const visibleCards = container.querySelectorAll('.application-card');
            if (visibleCards.length === 0) {
                container.innerHTML = `
                    <div class="empty-state" id="empty-state">
                        <i class="fa-solid fa-folder-open empty-icon"></i>
                        <h3>No Applications Found</h3>
                        <p>You haven't added any job or internship applications yet.</p>
                        <a href="/add/" class="btn btn-primary mt-3">Add Your First Application</a>
                    </div>
                `;
            }
        }
    }

    // Event delegation for Mark Complete buttons (AJAX fetch)
    document.addEventListener('click', function(e) {
        const completeBtn = e.target.closest('.btn-mark-complete');
        if (completeBtn) {
            e.preventDefault();
            const taskId = completeBtn.getAttribute('data-id');
            if (!taskId) return;

            completeBtn.disabled = true;
            completeBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Updating...';

            fetch(`/complete/${taskId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const card = document.getElementById(`task-card-${taskId}`);
                    const badge = document.getElementById(`status-badge-${taskId}`);

                    if (card) {
                        card.classList.add('card-completed');
                    }
                    if (badge) {
                        badge.className = 'status-badge badge-completed';
                        badge.innerHTML = '<i class="fa-solid fa-check"></i> Completed';
                    }

                    // Hide/remove the Mark Complete button
                    completeBtn.style.transition = 'all 0.3s ease';
                    completeBtn.style.opacity = '0';
                    setTimeout(() => {
                        completeBtn.remove();
                    }, 300);

                    // Dynamically update stats
                    updateStats('pending', -1);
                    updateStats('completed', 1);
                } else {
                    alert('Error completing task.');
                    completeBtn.disabled = false;
                    completeBtn.innerHTML = '<i class="fa-solid fa-check-double"></i> Mark Complete';
                }
            })
            .catch(error => {
                console.error('AJAX Error:', error);
                alert('An error occurred while updating status.');
                completeBtn.disabled = false;
                completeBtn.innerHTML = '<i class="fa-solid fa-check-double"></i> Mark Complete';
            });
        }
    });

    // Event delegation for Delete Application buttons (AJAX fetch)
    document.addEventListener('click', function(e) {
        const deleteBtn = e.target.closest('.btn-delete-task');
        if (deleteBtn) {
            e.preventDefault();
            const taskId = deleteBtn.getAttribute('data-id');
            if (!taskId) return;

            if (!confirm('Are you sure you want to delete this application?')) {
                return;
            }

            deleteBtn.disabled = true;
            deleteBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Deleting...';

            fetch(`/delete/${taskId}/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken(),
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const card = document.getElementById(`task-card-${taskId}`);
                    if (card) {
                        const isCompleted = card.classList.contains('card-completed');
                        
                        card.classList.add('fade-out');
                        setTimeout(() => {
                            card.remove();
                            updateStats('total', -1);
                            if (isCompleted) {
                                updateStats('completed', -1);
                            } else {
                                updateStats('pending', -1);
                            }
                            checkEmptyState();
                        }, 300);
                    }
                } else {
                    alert('Error deleting task.');
                    deleteBtn.disabled = false;
                    deleteBtn.innerHTML = '<i class="fa-solid fa-trash-can"></i> Delete';
                }
            })
            .catch(error => {
                console.error('AJAX Error:', error);
                alert('An error occurred while deleting application.');
                deleteBtn.disabled = false;
                deleteBtn.innerHTML = '<i class="fa-solid fa-trash-can"></i> Delete';
            });
        }
    });
});
