/* ==========================================
  0. Dark Mode / Theme Toggle Logic
========================================== */
const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
const themeToggleBtn = document.getElementById('theme-toggle');

if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
    document.documentElement.classList.add('dark-mode');
    if (themeToggleLightIcon) themeToggleLightIcon.classList.remove('hidden');
} else {
    document.documentElement.classList.remove('dark-mode');
    if (themeToggleDarkIcon) themeToggleDarkIcon.classList.remove('hidden');
}

if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', function() {
        themeToggleDarkIcon.classList.toggle('hidden');
        themeToggleLightIcon.classList.toggle('hidden');

        if (localStorage.getItem('color-theme')) {
            if (localStorage.getItem('color-theme') === 'light') {
                document.documentElement.classList.add('dark-mode');
                localStorage.setItem('color-theme', 'dark');
            } else {
                document.documentElement.classList.remove('dark-mode');
                localStorage.setItem('color-theme', 'light');
            }
        } else {
            if (document.documentElement.classList.contains('dark-mode')) {
                document.documentElement.classList.remove('dark-mode');
                localStorage.setItem('color-theme', 'light');
            } else {
                document.documentElement.classList.add('dark-mode');
                localStorage.setItem('color-theme', 'dark');
            }
        }
    });
}

// 404
window.addEventListener('load', function() {
    const preloader = document.getElementById('preloader');
    if (preloader) {
        preloader.style.opacity = '0';
        setTimeout(() => {
            preloader.style.display = 'none';
        }, 700);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    
    /* ==========================================
      1. Navbar & Search Logic
    ========================================== */
const searchToggle = document.getElementById('search-toggle');
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    let typingTimer;
    const doneTypingInterval = 1000;

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
        searchInput.value = '';

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
            
            if (searchInput.value.trim() === '') return;

            typingTimer = setTimeout(function() {
                searchInput.blur();
                searchForm.submit(); 
            }, doneTypingInterval);
        });

        searchInput.addEventListener('click', function(e) {
            e.stopPropagation();
        });

        document.addEventListener('click', function(e) {
            if (!searchForm.contains(e.target) && !searchToggle.contains(e.target)) {
                searchForm.classList.add('w-0', 'opacity-0');
                searchForm.classList.remove('w-28', 'sm:w-36', 'opacity-100');
            }
        });
    }

/* ==========================================
      2. Auto Sliders Logic (Handles Multiple Sliders)
    ========================================== */
    const sliders = document.querySelectorAll('.auto-slider, #related-slider');
    
    sliders.forEach(slider => {
        let autoScrollReq;
        const scrollSpeed = 1; 

        function autoScroll() {
            if (slider.scrollWidth > slider.clientWidth) {
                slider.scrollLeft -= scrollSpeed; 
                
                const maxScroll = slider.scrollWidth - slider.clientWidth;
                
                if (Math.abs(slider.scrollLeft) >= maxScroll - 1) {
                    slider.scrollLeft = 0; 
                }
            }
            autoScrollReq = requestAnimationFrame(autoScroll);
        }

        function startAutoScroll() {
            if (!autoScrollReq) {
                autoScrollReq = requestAnimationFrame(autoScroll);
            }
        }

        function stopAutoScroll() {
            if (autoScrollReq) {
                cancelAnimationFrame(autoScrollReq);
                autoScrollReq = null;
            }
        }

        startAutoScroll();

        slider.addEventListener('mouseenter', stopAutoScroll);
        slider.addEventListener('touchstart', stopAutoScroll, {passive: true});
        slider.addEventListener('mouseleave', startAutoScroll);
        slider.addEventListener('touchend', startAutoScroll);
    });

/* ==========================================
      3. Audio Interactive Transcript Logic (GPU Hardware Accelerated)
    ========================================== */
    const rawTranscript = document.getElementById('raw-transcript');
    const interactiveContainer = document.getElementById('interactive-transcript');
    const audio = document.querySelector('audio');

    if (rawTranscript && interactiveContainer) {
        const lines = rawTranscript.textContent.split('\n');
        let hasTimestamps = false;
        
        lines.forEach(line => {
            const trimmedLine = line.trim();
            if (!trimmedLine) return;

            const match = trimmedLine.match(/\[(\d{1,2}):(\d{2})(?::(\d{2}))?\]/);
            
            if (match) {
                hasTimestamps = true;
                let timeInSeconds = 0;
                
                if (match[3]) {
                    timeInSeconds = parseInt(match[1]) * 3600 + parseInt(match[2]) * 60 + parseInt(match[3]);
                } else {
                    timeInSeconds = parseInt(match[1]) * 60 + parseInt(match[2]);
                }
                
                const text = trimmedLine.replace(match[0], '').trim();
                const p = document.createElement('p');
                
                if (audio) {
                    p.className = 'transcript-line text-gray-400 font-semibold hover:text-gray-500 cursor-pointer transition-all duration-300 transform-gpu origin-right pl-2 leading-loose';
                    p.addEventListener('click', () => {
                        audio.currentTime = timeInSeconds;
                        audio.play();
                    });
                } else {
                    p.className = 'text-gray-700 font-semibold leading-loose mb-2 pl-2';
                }
                
                p.dataset.time = timeInSeconds;
                p.innerHTML = `<span class="text-[10px] sm:text-xs font-bold font-sans text-gray-300 bg-gray-50 px-2 py-0.5 rounded ml-3 inline-block transition-colors duration-300" dir="ltr">${match[0].replace('[', '').replace(']', '')}</span>${text}`;
                
                interactiveContainer.appendChild(p);
            } else {
                const p = document.createElement('p');
                p.className = 'text-gray-700 font-semibold leading-loose';
                p.textContent = trimmedLine;
                interactiveContainer.appendChild(p);
            }
        });

        if (!hasTimestamps) {
            interactiveContainer.innerHTML = rawTranscript.innerHTML.replace(/\n/g, '<br>');
            interactiveContainer.className = "force-wrap-content article-body w-full overflow-hidden text-gray-800 leading-loose mt-4";
        }

        if (hasTimestamps && audio) {
            const transcriptLines = document.querySelectorAll('.transcript-line');
            const lineTimes = Array.from(transcriptLines).map(line => parseFloat(line.dataset.time));
            
            let currentActiveIndex = -1;
            let rafId = null;
            let lastUpdate = 0;
            
            audio.addEventListener('timeupdate', () => {
                const now = Date.now();
                if (now - lastUpdate < 100) return;
                lastUpdate = now;

                const currentTime = audio.currentTime;
                let newActiveIndex = -1;
                
                for (let i = 0; i < lineTimes.length; i++) {
                    if (currentTime >= lineTimes[i]) {
                        newActiveIndex = i;
                    } else {
                        break;
                    }
                }
                
                if (newActiveIndex !== currentActiveIndex) {
                    if (rafId) cancelAnimationFrame(rafId);
                    
                    rafId = requestAnimationFrame(() => {
                        
                        if (currentActiveIndex >= 0 && transcriptLines[currentActiveIndex]) {
                            const oldLine = transcriptLines[currentActiveIndex];
                            const oldSpan = oldLine.querySelector('span');
                            
                            oldLine.classList.add('text-gray-400', 'hover:text-gray-500');
                            oldLine.classList.remove('text-[#cba358]', 'scale-[1.03]', 'drop-shadow-md');
                            
                            if (oldSpan) {
                                oldSpan.classList.replace('bg-[#cba358]/10', 'bg-gray-50');
                                oldSpan.classList.replace('text-[#cba358]', 'text-gray-300');
                            }
                        }
                        
                        if (newActiveIndex >= 0 && transcriptLines[newActiveIndex]) {
                            const newLine = transcriptLines[newActiveIndex];
                            const newSpan = newLine.querySelector('span');
                            
                            newLine.classList.remove('text-gray-400', 'hover:text-gray-500');
                            newLine.classList.add('text-[#cba358]', 'scale-[1.03]', 'drop-shadow-md');
                            
                            if (newSpan) {
                                newSpan.classList.replace('bg-gray-50', 'bg-[#cba358]/10');
                                newSpan.classList.replace('text-gray-300', 'text-[#cba358]');
                            }
                        }
                        
                        currentActiveIndex = newActiveIndex;
                    });
                }
            });
        }
    }
});