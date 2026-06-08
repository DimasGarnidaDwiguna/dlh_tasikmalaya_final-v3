/* =========================================================
   DLH Tasikmalaya Final Interaction Script
   Stable dropdown, responsive menu, reveal animation, number-only inputs
========================================================= */
document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.getElementById('mobileToggle');
    const menu = document.getElementById('navMenu');
    const scrollTop = document.getElementById('scrollTop');
    const header = document.getElementById('siteHeader');
    const dropdowns = document.querySelectorAll('.dropdown');

    if (toggle && menu) {
        toggle.addEventListener('click', () => {
            menu.classList.toggle('show');
            toggle.setAttribute('aria-expanded', menu.classList.contains('show') ? 'true' : 'false');
        });
    }

    dropdowns.forEach((item) => {
        const link = item.querySelector(':scope > a');
        const submenu = item.querySelector(':scope > .mega-menu');
        if (!link || !submenu) return;

        let closeTimer = null;

        const openMenu = () => {
            clearTimeout(closeTimer);
            dropdowns.forEach((other) => {
                if (other !== item) {
                    other.classList.remove('open', 'is-open');
                    const otherLink = other.querySelector(':scope > a');
                    if (otherLink) otherLink.setAttribute('aria-expanded', 'false');
                }
            });
            item.classList.add('open', 'is-open');
            link.setAttribute('aria-expanded', 'true');
        };

        const closeMenu = () => {
            closeTimer = setTimeout(() => {
                item.classList.remove('open', 'is-open');
                link.setAttribute('aria-expanded', 'false');
            }, 170);
        };

        link.setAttribute('aria-haspopup', 'true');
        link.setAttribute('aria-expanded', 'false');

        item.addEventListener('mouseenter', () => {
            if (window.innerWidth > 1180) openMenu();
        });

        item.addEventListener('mouseleave', () => {
            if (window.innerWidth > 1180) closeMenu();
        });

        link.addEventListener('click', (event) => {
            event.preventDefault();
            if (item.classList.contains('open')) {
                item.classList.remove('open', 'is-open');
                link.setAttribute('aria-expanded', 'false');
            } else {
                openMenu();
            }
        });
    });

    document.addEventListener('click', (event) => {
        if (!event.target.closest('.navbar')) {
            dropdowns.forEach((item) => {
                item.classList.remove('open', 'is-open');
                const link = item.querySelector(':scope > a');
                if (link) link.setAttribute('aria-expanded', 'false');
            });
            if (menu) menu.classList.remove('show');
            if (toggle) toggle.setAttribute('aria-expanded', 'false');
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            dropdowns.forEach((item) => {
                item.classList.remove('open', 'is-open');
                const link = item.querySelector(':scope > a');
                if (link) link.setAttribute('aria-expanded', 'false');
            });
            if (menu) menu.classList.remove('show');
            if (toggle) toggle.setAttribute('aria-expanded', 'false');
        }
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) entry.target.classList.add('visible');
        });
    }, { threshold: 0.12 });

    document.querySelectorAll('.reveal').forEach((item, index) => {
        item.style.transitionDelay = `${Math.min(index * 55, 330)}ms`;
        observer.observe(item);
    });

    const onScroll = () => {
        const active = window.scrollY > 60;
        if (header) header.classList.toggle('scrolled', active);
        if (scrollTop) scrollTop.classList.toggle('show', window.scrollY > 420);
    };

    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    if (scrollTop) {
        scrollTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
    }

    const numberInputs = document.querySelectorAll(
        ".only-number, input[name='phone'], input[name='phone_number'], input[name='whatsapp'], input[name='no_hp'], input[name='telp'], input[data-only-number='true']"
    );

    numberInputs.forEach((input) => {
        input.setAttribute('inputmode', 'numeric');
        input.setAttribute('autocomplete', input.getAttribute('autocomplete') || 'tel');
        input.setAttribute('maxlength', input.getAttribute('maxlength') || '15');

        const cleanValue = () => {
            const max = Number(input.getAttribute('maxlength')) || 15;
            input.value = input.value.replace(/[^0-9]/g, '').slice(0, max);
        };

        input.addEventListener('input', cleanValue);

        input.addEventListener('paste', (event) => {
            event.preventDefault();
            const paste = (event.clipboardData || window.clipboardData).getData('text');
            const max = Number(input.getAttribute('maxlength')) || 15;
            input.value = paste.replace(/[^0-9]/g, '').slice(0, max);
            input.dispatchEvent(new Event('input', { bubbles: true }));
        });

        input.addEventListener('keypress', (event) => {
            const code = event.which || event.keyCode;
            if (code < 48 || code > 57) event.preventDefault();
        });

        cleanValue();
    });
});
