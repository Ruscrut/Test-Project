document.addEventListener('DOMContentLoaded', function() {
    const expandedItems = document.querySelectorAll('.expanded > ul');
    expandedItems.forEach(item => {
        item.style.transition = 'max-height 0.3s ease';
        item.style.maxHeight = item.scrollHeight + 'px';
    });
});