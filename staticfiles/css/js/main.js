document.addEventListener('DOMContentLoaded', function() {
    
    /* --- Navbar & Search Logic --- */
    const searchToggle = document.getElementById('search-toggle');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    let typingTimer;
    const doneTypingInterval = 500; 

    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function(e) {
            e.stopPropagation();
            mobileMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', function(e) {
            if (!mobileMenu.contains(e.target) && !menuToggle.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }

    if (searchToggle && searchForm && searchInput) {
        searchToggle.addEventListener('click', function(e) {
            e.stopPropagation(); 
            if (searchForm.classList.contains('w-0')) {
                searchForm.classList.remove('w-0', 'opacity-0');
                searchForm.classList.add('w-28', 'sm:w-36', 'opacity-100'); 
                searchInput.focus(); 
            } else {
                searchForm.classList.add('w-0', 'opacity-0');
                searchForm.classList.remove('w-28', 'sm:w-36', 'opacity-100');
            }
        });

        searchInput.addEventListener('input', function() {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(function() {
                searchForm.submit(); 
            }, doneTypingInterval);
        });

        searchInput.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        document.addEventListener('click', function(e) {
            if (!searchForm.contains(e.target) && !searchToggle.contains(e.target)) {
                const urlParams = new URLSearchParams(window.location.search);
                if (!urlParams.has('q') || urlParams.get('q').trim() === '') {
                    searchForm.classList.add('w-0', 'opacity-0');
                    searchForm.classList.remove('w-28', 'sm:w-36', 'opacity-100');
                }
            }
        });
    }

    /* --- Related Articles Slider Logic --- */
    const slider = document.getElementById('related-slider');
    if (slider) {
        let autoScrollTimer;

        function startAutoScroll() {
            autoScrollTimer = setInterval(function() {
                slider.scrollLeft -= 1; 
                
                if (Math.abs(slider.scrollLeft) >= (slider.scrollWidth - slider.clientWidth) - 2) {
                    slider.scrollLeft = 0; 
                }
            }, 30);
        }

        function stopAutoScroll() {
            clearInterval(autoScrollTimer);
        }

        startAutoScroll();

        slider.addEventListener('mouseenter', stopAutoScroll);
        slider.addEventListener('touchstart', stopAutoScroll, {passive: true});
        slider.addEventListener('mouseleave', startAutoScroll);
        slider.addEventListener('touchend', startAutoScroll);
    }
});